import unittest
from unittest.mock import Mock, patch
from gmail_assistant.gmail_voice_assistant_gui import GmailVoiceAssistantGUI

class TestGmailVoiceAssistantGUI(unittest.TestCase):
    def setUp(self):
        self.app = GmailVoiceAssistantGUI()

    def tearDown(self):
        if hasattr(self, 'app'):
            self.app.window.destroy()

    def test_initial_state(self):
        """Test initial GUI state"""
        self.assertEqual(self.app.listening, False)
        self.assertIsNone(self.app.listen_thread)
        self.assertEqual(
            self.app.listen_button.cget("text"),
            "Start Listening"
        )

    @patch('gmail_assistant.gmail_voice_assistant.GmailVoiceAssistant.listen')
    def test_toggle_listening(self, mock_listen):
        """Test listening toggle functionality"""
        # Start listening
        self.app.toggle_listening()
        self.assertTrue(self.app.listening)
        self.assertEqual(
            self.app.listen_button.cget("text"),
            "Stop Listening"
        )
        
        # Stop listening
        self.app.toggle_listening()
        self.assertFalse(self.app.listening)
        self.assertEqual(
            self.app.listen_button.cget("text"),
            "Start Listening"
        )

    def test_log_output(self):
        """Test output logging to GUI"""
        test_text = "Test output message"
        self.app.log_output(test_text)
        output_text = self.app.output_text.get("1.0", "end-1c")
        self.assertIn(test_text, output_text) 