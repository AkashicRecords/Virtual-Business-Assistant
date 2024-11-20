from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, value):
        """Wait for and return element"""
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )
    
    def find_clickable_element(self, by, value):
        """Wait for and return clickable element"""
        return self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
    
    def is_element_visible(self, by, value):
        """Check if element is visible"""
        try:
            self.wait.until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False 