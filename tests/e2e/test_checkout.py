import pytest
from selenium.webdriver.common.by import By

@pytest.mark.e2e
class TestCheckoutFlow:
    
    def test_proceed_to_checkout(self, authorized_driver, live_server_url):
        """Test validation of checkout button (PayPal link)."""
        # Ensure cart has item
        authorized_driver.get(f"{live_server_url}/Shop")
        try:
            btns = authorized_driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
            if btns:
                btns[0].click()
        except:
            pass

        authorized_driver.get(f"{live_server_url}/Cart")
        
        # Verify PayPal button exists
        paypal_btn = authorized_driver.find_element(By.CLASS_NAME, "paypal-button")
        assert paypal_btn.is_displayed()
        
        href = paypal_btn.get_attribute("href")
        assert "paypal.me" in href
