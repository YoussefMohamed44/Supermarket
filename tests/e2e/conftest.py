import pytest
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from Super_Market import app, db, bcrypt
from Super_Market.models import User, Product, CartItem, Cart

# --- Server Fixtures ---

@pytest.fixture(scope='session')
def app_port():
    """Returns a free port for the Flask server."""
    return 5005

@pytest.fixture(scope='session')
def live_server_url(app_port):
    """Returns the root URL of the live server."""
    return f'http://localhost:{app_port}'



@pytest.fixture(scope='session', autouse=True)
def run_app_server(app_port):
    """Runs the Flask app in a background thread using an isolated in-memory test database."""
    # E2E tests use in-memory SQLite so they don't touch Orders.db
    # This keeps the production database clean during all test runs
    
    # Configure app for e2e testing with file-based test database (better for threading)
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Go up two levels to reach project root (tests/e2e -> tests -> root)
    # Actually root is where Super_Market is.
    # Let's use app.instance_path if available or hardcode relative to cwd
    db_path = os.path.join(app.root_path, '..', 'instance', 'test_orders.db')
    db_path = os.path.abspath(db_path)
    
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test_secret_e2e_suite'
    
    # Initialize DB and Seed E2E Data in memory
    with app.app_context():
        # Dispose old engine connections
        try:
            db.session.remove()
            db.engine.dispose()
        except Exception:
            pass
            
        db.create_all()
        seed_test_data()

    def start_server():
        # use_reloader=False is important for threading
        # threaded=True is default
        app.run(port=app_port, use_reloader=False, threaded=True)

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Give server time to start
    time.sleep(3) 
    
    yield
    
    # Teardown
    with app.app_context():
        db.session.remove()
        try:
            db.engine.dispose()
        except:
            pass

    # Give some time for file handles to close
    time.sleep(1)
    # Keep the e2e test DB for inspection (do not delete)

def seed_test_data():
    """Seeds the database with initial data for testing."""
    # Clear existing data to prevent IntegrityErrors if DB wasn't clean
    try:
        db.session.query(User).delete()
        db.session.query(Product).delete()
        db.session.commit()
    except:
        db.session.rollback()

    # Create a test user
    hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(username="e2euser", email="e2e@example.com", phone="1112223333", password=hashed_pw)
    
    # Create test products
    p1 = Product(name="E2E Milk", price=4.0, category="Protein", description="Fresh Milk", image_url="/static/images/milk.jpeg")
    p2 = Product(name="E2E Bread", price=2.5, category="Bakery", description="Whole Grain", image_url="/static/images/bread.jpg")
    
    db.session.add(user)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

# --- WebDriver Fixtures ---

@pytest.fixture(scope='function')
def driver():
    """set up chrome driver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--disable-gpu") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5) # Set a default implicit wait
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope='function')
def authorized_driver(driver, live_server_url):
    """Returns a driver instance that is already logged in."""
    driver.get(f"{live_server_url}/login")
    from selenium.webdriver.common.by import By
    
    driver.find_element(By.NAME, "email").send_keys("e2e@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.ID, "login").click() # ID derived from inspection
    
    return driver
