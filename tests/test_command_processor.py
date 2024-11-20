import unittest
from unittest.mock import Mock, patch
from gmail_assistant.command_processor import CommandProcessor

class TestCommandProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = CommandProcessor()

    def test_process_read_email_command(self):
        """Test processing 'read email' command"""
        commands = [
            "read my email",
            "read latest email",
            "check email",
            "show my emails"
        ]
        
        for command in commands:
            with self.subTest(command=command):
                result = self.processor.process_command(command)
                self.assertEqual(result.intent, "read_email")

    def test_process_send_email_command(self):
        """Test processing 'send email' command"""
        commands = [
            "send an email",
            "compose email",
            "write email",
            "new email"
        ]
        
        for command in commands:
            with self.subTest(command=command):
                result = self.processor.process_command(command)
                self.assertEqual(result.intent, "send_email")

    def test_process_invalid_command(self):
        """Test processing invalid commands"""
        commands = [
            "invalid command",
            "do something",
            "random text"
        ]
        
        for command in commands:
            with self.subTest(command=command):
                result = self.processor.process_command(command)
                self.assertEqual(result.intent, "unknown") 