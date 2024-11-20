from selenium.webdriver.common.by import By
from .base_page import BasePage

class MainPage(BasePage):
    # Locators
    STATUS_LABEL = (By.CLASS_NAME, "status-label")
    LISTEN_BUTTON = (By.CLASS_NAME, "listen-button")
    OUTPUT_TEXT = (By.CLASS_NAME, "output-text")
    COMPOSE_BUTTON = (By.CLASS_NAME, "compose-button")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.verify_page()
    
    def verify_page(self):
        """Verify main page elements are present"""
        assert self.is_element_visible(*self.STATUS_LABEL)
        assert self.is_element_visible(*self.LISTEN_BUTTON)
        assert self.is_element_visible(*self.OUTPUT_TEXT)
    
    def get_status_text(self):
        """Get status label text"""
        return self.find_element(*self.STATUS_LABEL).text
    
    def get_listen_button_text(self):
        """Get listen button text"""
        return self.find_element(*self.LISTEN_BUTTON).text
    
    def toggle_listening(self):
        """Click listen button"""
        self.find_clickable_element(*self.LISTEN_BUTTON).click()
    
    def get_output_text(self):
        """Get output text area content"""
        return self.find_element(*self.OUTPUT_TEXT).text
    
    def open_compose_email(self):
        """Click compose button and return EmailComposePage"""
        self.find_clickable_element(*self.COMPOSE_BUTTON).click()
        from .email_compose_page import EmailComposePage
        return EmailComposePage(self.driver) 