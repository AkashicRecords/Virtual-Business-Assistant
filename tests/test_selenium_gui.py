import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
from gmail_assistant.gmail_voice_assistant_gui import GmailVoiceAssistantGUI
from .pages.main_page import MainPage
from .pages.email_compose_page import EmailComposePage

class TestGUISelenium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize webdriver
        cls.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        
        # Start GUI in separate thread
        cls.gui_thread = threading.Thread(target=cls.run_gui)
        cls.gui_thread.daemon = True
        cls.gui_thread.start()
        
        # Wait for GUI to start
        time.sleep(2)
        
        # Initialize main page
        cls.main_page = MainPage(cls.driver)

    @classmethod
    def run_gui(cls):
        cls.app = GmailVoiceAssistantGUI()
        cls.app.run()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        if hasattr(cls, 'app'):
            cls.app.window.destroy()

    def test_initial_window_state(self):
        """Test initial window state"""
        self.assertEqual(self.main_page.get_status_text(), "Status: Ready")
        self.assertEqual(self.main_page.get_listen_button_text(), "Start Listening")

    def test_listen_button_toggle(self):
        """Test listen button functionality"""
        # Start listening
        self.main_page.toggle_listening()
        time.sleep(1)
        self.assertEqual(self.main_page.get_listen_button_text(), "Stop Listening")
        
        # Stop listening
        self.main_page.toggle_listening()
        time.sleep(1)
        self.assertEqual(self.main_page.get_listen_button_text(), "Start Listening")

    def test_output_text_update(self):
        """Test output text updates"""
        test_message = "Test message"
        self.app.log_output(test_message)
        time.sleep(1)
        self.assertIn(test_message, self.main_page.get_output_text())

    def test_email_composition(self):
        """Test email composition window"""
        email_page = self.main_page.open_compose_email()
        
        # Test email composition
        test_email = {
            "to": "test@example.com",
            "subject": "Test Subject",
            "body": "Test email body"
        }
        email_page.compose_email(**test_email)
        email_page.send_email() 