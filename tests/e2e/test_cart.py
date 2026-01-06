import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.e2e
class TestCartFlow:
    
    def test_add_to_cart(self, authorized_driver, live_server_url):
        """Test adding an item to the cart."""
        authorized_driver.get(f"{live_server_url}/Shop")
        
        # Click "Add to cart" on first product
        # The button is inside an anchor tag
        add_btns = authorized_driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
        add_btns[0].click()
        
        # Verify redirected to Shop (as per route logic)
        # Check title
        assert "Shop" in authorized_driver.title
        
        # Navigate to Cart to verify
        authorized_driver.get(f"{live_server_url}/Cart")
        assert "Cart" in authorized_driver.title
        
        # Check item is in list
        cart_items = authorized_driver.find_elements(By.TAG_NAME, "li")
        # Empty cart has 1 li saying "empty". Non-empty has items.
        # We expect at least 1 item + maybe total? 
        # Actually template says: <ul> {% for item %} <li>...</li> {% endfor %} </ul>
        # So cart_items length should be >= 1 and text shouldn't be "empty"
        
        assert len(cart_items) > 0
        assert "Your cart is empty" not in authorized_driver.page_source

    def test_increase_quantity(self, authorized_driver, live_server_url):
        """Test increasing quantity by adding item again."""
        # 1. Clear Cart to ensure clean state
        authorized_driver.get(f"{live_server_url}/Cart")
        try:
            # Try to click clear button if it exists
            clear_btn = authorized_driver.find_element(By.CLASS_NAME, "btn-danger")
            clear_btn.click()
            try:
                authorized_driver.switch_to.alert.accept()
            except:
                pass
            WebDriverWait(authorized_driver, 5).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Your cart is empty")
            )
        except:
            # Button not found implies empty cart
            pass

        # 2. Add first item
        authorized_driver.get(f"{live_server_url}/Shop")
        add_btns = authorized_driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
        add_btns[0].click()
        # Wait for redirect to Shop
        WebDriverWait(authorized_driver, 5).until(EC.title_contains("Shop"))
        
        # 3. Add same item again
        add_btns = authorized_driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
        add_btns[0].click()
        WebDriverWait(authorized_driver, 5).until(EC.title_contains("Shop"))
        
        # 4. Check Cart
        authorized_driver.get(f"{live_server_url}/Cart")
        
        # 5. Verify Quantity: 2
        page_text = authorized_driver.find_element(By.TAG_NAME, "body").text
        assert "Quantity: 2" in page_text
        


    def test_clear_cart(self, authorized_driver, live_server_url):
        """Test clearing the cart."""
        # Ensure something is in cart
        authorized_driver.get(f"{live_server_url}/Shop")
        try:
             authorized_driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")[0].click()
        except:
            pass # might already be there

        authorized_driver.get(f"{live_server_url}/Cart")
        
        # Click Clear Cart if it exists
        try:
            clear_btn = authorized_driver.find_element(By.CLASS_NAME, "btn-danger") 
            # Confirm dialog handling
            clear_btn.click()
            
            # The button has 'onclick="return confirm..."', Selenium handles alerts
            try:
                alert = authorized_driver.switch_to.alert
                alert.accept()
            except:
                pass
                
            WebDriverWait(authorized_driver, 5).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Your cart is empty")
            )
        except Exception as e:

            pass
            
        assert "Your cart is empty" in authorized_driver.page_source