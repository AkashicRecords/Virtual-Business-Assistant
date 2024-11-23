import pytest
from gmail_assistant.llm_handler import LLMHandler

class TestLLMFeatures:
    @pytest.fixture
    def llm_handler(self):
        return LLMHandler()

    def test_email_generation(self, llm_handler):
        """Test LLM email generation"""
        prompt = "Write a project update email"
        context = {
            "project": "Website Redesign",
            "recent_updates": ["Design completed", "Testing started"]
        }
        
        response = llm_handler.generate_email(prompt, context)
        assert "Website Redesign" in response
        assert "Design" in response
        assert "Testing" in response 