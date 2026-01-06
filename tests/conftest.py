import pytest
import os

# Mark that we're running in test mode (before importing app)
os.environ['TESTING_MODE'] = '1'
# Force safe database for ALL tests (Unit, Integration, E2E)
os.environ['TEST_DATABASE_URI'] = 'sqlite:///test_orders.db'

from Super_Market import app, db, bcrypt
from Super_Market.models import User, Product, Cart, CartItem
import os
import json
import time
from datetime import datetime

@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for easier form testing
    app.config['SECRET_KEY'] = 'test_secret'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def init_database(client):
    # Create initial data for tests
    hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(username="testuser", email="test@example.com", phone="12345678901", password=hashed_pw)
    product = Product(name="Test Vitamin", price=20.0, category="Health", description="Test Desc")
    db.session.add(user)
    db.session.add(product)
    db.session.commit()
    db.session.commit()
    return db

def pytest_sessionstart(session):
    session.start_time = time.time()
    # also store on config so other hooks can access it
    try:
        session.config.start_time = session.start_time
    except Exception:
        pass

def pytest_sessionfinish(session, exitstatus):
    # 1. History Handling
    reporter = session.config.pluginmanager.get_plugin('terminalreporter')
    if reporter:
        passed = len(reporter.stats.get('passed', []))
        failed = len(reporter.stats.get('failed', []))
        skipped = len(reporter.stats.get('skipped', []))
        error = len(reporter.stats.get('error', []))
        total = passed + failed + skipped + error
        
        duration = time.time() - session.start_time if hasattr(session, 'start_time') else 0.0
        
        history_file = os.path.join(session.config.rootdir, 'test_dashboard', 'history.json')
        
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "passed": passed,
            "failed": failed,
            "total": total,
            "duration": duration
        }
        
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
            except:
                pass
        
        history.append(new_entry)
        # Keep last 50
        history = history[-50:]
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4)

@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):

    # Zero Coverage Handling (runs after plugins)
    # Exit code 5 means NO_TESTS_COLLECTED
    if exitstatus == 5:
        coverage_file = os.path.join(config.rootdir, 'test_dashboard', 'coverage.json')
        zero_cov = {
            "totals": {
                "percent_covered_display": "0",
                "covered_lines": 0,
                "num_statements": 0,
                "missing_lines": 0
            }
        }
        with open(coverage_file, 'w') as f:
            json.dump(zero_cov, f)

    # Print a concise test report to the terminal (non-intrusive)
    try:
        stats = getattr(terminalreporter, 'stats', {}) or {}
        passed = len(stats.get('passed', []))
        failed = len(stats.get('failed', []))
        skipped = len(stats.get('skipped', []))
        error = len(stats.get('error', []))
        total = passed + failed + skipped + error
        duration = 0.0
        try:
            duration = time.time() - getattr(config, 'start_time', 0.0)
        except Exception:
            duration = 0.0

        terminalreporter.write_sep('=', 'Test Summary')
        terminalreporter.write_line(f'Passed: {passed}  Failed: {failed}  Skipped: {skipped}  Errors: {error}  Total: {total}')
        terminalreporter.write_line(f'Duration: {duration:.2f}s')
        history_file = os.path.join(config.rootdir, 'test_dashboard', 'history.json')
        terminalreporter.write_line(f'History: {history_file}')
        terminalreporter.write_sep('=', '')
    except Exception:
        # Do not interfere with pytest if printing fails
        pass
