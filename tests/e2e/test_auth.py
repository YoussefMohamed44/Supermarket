import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.e2e
class TestAuthentication:
    
    def test_registration_success(self, driver, live_server_url):
        """Test that a new user can register successfully."""
        driver.get(f"{live_server_url}/register")
        
        # Fill Form
        driver.find_element(By.ID, "username").send_keys("newuser")
        driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        driver.find_element(By.ID, "phone").send_keys("01234567890")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm_password").send_keys("password123")
        
        # Submit
        driver.find_element(By.ID, "submit").click()
        
        # Verify redirect to Login or Home (Assuming redirect to login after signup, or home)
        # Checking for success message is more robust
        try:
             WebDriverWait(driver, 10).until(EC.url_contains("/login"))
             assert "login" in driver.current_url.lower()
        except:
             assert "Account created" in driver.page_source or "login" in driver.current_url.lower()

    def test_login_success(self, driver, live_server_url):
        """Test that a registered user can login."""
        driver.get(f"{live_server_url}/login")
        
        driver.find_element(By.ID, "email").send_keys("e2e@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "login").click()
        
        # Verify Login Success (e.g., "Logout" button exists or redirected to shop/home)
        # Assuming redirect to Home
        WebDriverWait(driver, 5).until(EC.title_contains("Home"))
        assert "Home" in driver.title

    def test_login_invalid(self, driver, live_server_url):
        """Test login with invalid credentials."""
        driver.get(f"{live_server_url}/login")
        
        driver.find_element(By.ID, "email").send_keys("wrong@example.com")
        driver.find_element(By.ID, "password").send_keys("wrongpass")
        driver.find_element(By.ID, "login").click()
        
        # Verify still on login page or error message
        # Checking for "Log In" legend or invalid-feedback
        page_source = driver.page_source
        assert "Log In" in page_source
        # If the app shows flash messages or field errors, check for them.
        # Based on login.html, it shows 'is-invalid' class if form errors
        # But for 'Login Unsuccessful', it might be a Flash message.
        # This test is basic sanity check.
