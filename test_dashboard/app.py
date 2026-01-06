from flask import Flask, render_template, jsonify, redirect, url_for
import os
import json
import subprocess
from datetime import datetime

app = Flask(__name__)

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
REPORT_FILE = os.path.join(BASE_DIR, 'report.json')
COVERAGE_FILE = os.path.join(BASE_DIR, 'coverage.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'history.json')
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, 'tests', 'ui')

@app.route('/')
def index():
    # Load latest report
    report = {}
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r') as f:
            report = json.load(f)
            
    # Load coverage
    coverage = {}
    if os.path.exists(COVERAGE_FILE):
        with open(COVERAGE_FILE, 'r') as f:
            coverage = json.load(f)

    # Load history
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)

    # Find screenshots
    screenshots = []
    if os.path.exists(SCREENSHOTS_DIR):
        for file in os.listdir(SCREENSHOTS_DIR):
            if file.endswith('.png'):
                screenshots.append(file)

    return render_template('index.html', report=report, coverage=coverage, history=history, screenshots=screenshots)

@app.route('/run')
def run_tests():
    """Execute tests and update reports."""
    # 1. Run Pytest with JSON report
    cmd_test = [
        "python", "-m", "pytest",
        "tests/",
        "--json-report",
        f"--json-report-file={REPORT_FILE}",
        "--quiet"
    ]
    try:
        subprocess.run(cmd_test, cwd=PROJECT_ROOT, check=False) # check=False because tests might fail
    except Exception as e:
        print(f"Test Execution Failed: {e}")

    # 2. Run Coverage
    cmd_cov = f"coverage run --branch --source=Super_Market -m pytest tests/ && coverage json -o {COVERAGE_FILE}"
    # Using shell=True for chain, but simpler to just run coverage json separate if needed
    # Let's just do coverage json generation assuming .coverage exists from previous step? 
    # Actually, let's run coverage separately to be safe/clean
    # Better: just use the coverage run command to generate the report json
    # subprocess.run("coverage json -o " + COVERAGE_FILE, shell=True, cwd=PROJECT_ROOT)
    # Re-running tests for coverage might be slow. Let's assume the first run was coverage run.
    
    # Let's do a single run that does both: coverage run ... --json-report ...
    cmd_full = [
        "coverage", "run", "--branch", "--source=Super_Market",
        "-m", "pytest", "tests/",
        "--json-report",
        f"--json-report-file={REPORT_FILE}"
    ]
    subprocess.run(cmd_full, cwd=PROJECT_ROOT, check=False)
    
    # Generate coverage JSON
    subprocess.run(["coverage", "json", "-o", COVERAGE_FILE], cwd=PROJECT_ROOT, check=False)

    # 3. Update History
    update_history()

    return redirect(url_for('index'))

def update_history():
    if not os.path.exists(REPORT_FILE):
        return

    with open(REPORT_FILE, 'r') as f:
        data = json.load(f)
    
    summary = data.get('summary', {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    entry = {
        'timestamp': timestamp,
        'passed': summary.get('passed', 0),
        'failed': summary.get('failed', 0),
        'total': summary.get('total', 0),
        'duration': data.get('duration', 0)
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except:
                pass
    
    history.append(entry)
    # Keep last 10
    history = history[-10:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    from flask import send_from_directory
    return send_from_directory(SCREENSHOTS_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
