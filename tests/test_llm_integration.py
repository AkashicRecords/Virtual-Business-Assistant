import pytest
from unittest.mock import patch
from gmail_assistant.llm.ollama_handler import OllamaHandler

class TestOllamaIntegration:
    @pytest.fixture
    def ollama_handler(self):
        return OllamaHandler()

    @patch('requests.post')
    def test_command_analysis(self, mock_post, ollama_handler):
        """Test LLM command analysis"""
        mock_post.return_value.json.return_value = {
            'response': 'Command intent: read email'
        }
        
        result = ollama_handler.analyze_command("read my latest email")
        assert "read email" in result.lower() 