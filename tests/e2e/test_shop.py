import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.e2e
class TestProductBrowsing:
    
    def test_view_products_page(self, driver, live_server_url):
        """Test accessing the shop page."""
        driver.get(f"{live_server_url}/Shop")
        assert "Shop" in driver.title
        
        # Verify products are present
        products = driver.find_elements(By.CLASS_NAME, "product")
        assert len(products) > 0, "No products displayed on Shop page"

    def test_product_visibility(self, driver, live_server_url):
        """Verify product name and price visibility."""
        driver.get(f"{live_server_url}/Shop")
        
        # Check first product details
        first_product = driver.find_element(By.CLASS_NAME, "product")
        name = first_product.find_element(By.CLASS_NAME, "product-name").text
        # Price is in a p tag with class product-description (based on template reading line 47)
        descs = first_product.find_elements(By.CLASS_NAME, "product-description") 
        # Line 46 is desc, Line 47 is price. 
        
        assert name != ""
        assert len(descs) >= 2
        assert "$" in descs[1].text  # Verifying price format
