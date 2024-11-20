from selenium.webdriver.common.by import By
from .base_page import BasePage

class EmailComposePage(BasePage):
    # Locators
    EMAIL_WINDOW = (By.CLASS_NAME, "email-window")
    TO_FIELD = (By.NAME, "to")
    SUBJECT_FIELD = (By.NAME, "subject")
    BODY_FIELD = (By.NAME, "body")
    SEND_BUTTON = (By.CLASS_NAME, "send-button")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.verify_page()
    
    def verify_page(self):
        """Verify email composition window elements"""
        assert self.is_element_visible(*self.EMAIL_WINDOW)
        assert self.is_element_visible(*self.TO_FIELD)
        assert self.is_element_visible(*self.SUBJECT_FIELD)
        assert self.is_element_visible(*self.BODY_FIELD)
    
    def compose_email(self, to, subject, body):
        """Fill in email fields"""
        self.find_element(*self.TO_FIELD).send_keys(to)
        self.find_element(*self.SUBJECT_FIELD).send_keys(subject)
        self.find_element(*self.BODY_FIELD).send_keys(body)
    
    def send_email(self):
        """Click send button"""
        self.find_clickable_element(*self.SEND_BUTTON).click() 