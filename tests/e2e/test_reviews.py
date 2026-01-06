import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.e2e
class TestReviews:

    def test_create_review(self, authorized_driver, live_server_url):
        """Test creating a review."""
        authorized_driver.get(f"{live_server_url}/Reviews")
        
        # Fill Form
        authorized_driver.find_element(By.ID, "title").send_keys("Amazing Product")
        authorized_driver.find_element(By.ID, "content").send_keys("I really loved the results. Highly recommended!")
        authorized_driver.find_element(By.ID, "submit").click()
        
        # Verify Success Message
        WebDriverWait(authorized_driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Review added!"))
        
        # Verify Review in List
        assert "Amazing Product" in authorized_driver.page_source
        assert "I really loved the results" in authorized_driver.page_source
