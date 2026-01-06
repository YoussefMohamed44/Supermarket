import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.mark.e2e
class TestMainRoutes:

    def test_about_page(self, driver, live_server_url):
        """Test About Page load."""
        driver.get(f"{live_server_url}/About")
        assert "About" in driver.title
        # Check for some content
        assert "Whole Foods Super Market" in driver.page_source or "Our Journey" in driver.page_source

    # Other tests removed as features are not available in Super_Market (Search, Filter, Product Detail)
