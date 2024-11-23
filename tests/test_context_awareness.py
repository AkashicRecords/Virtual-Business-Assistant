import pytest
from gmail_assistant.context import ContextManager
from gmail_assistant.llm_handler import LLMHandler

class TestContextAwareness:
    @pytest.fixture
    def context_manager(self):
        return ContextManager()

    def test_thread_context_tracking(self, context_manager):
        """Test if context is maintained across thread"""
        thread_id = "123"
        emails = [
            {"subject": "Project Meeting", "content": "Let's schedule a meeting"},
            {"subject": "Re: Project Meeting", "content": "Tuesday works for me"}
        ]
        
        # Add emails to thread
        for email in emails:
            context_manager.update_thread_context(thread_id, email)
            
        # Verify context
        context = context_manager.get_thread_context(thread_id)
        assert "meeting" in context.topics
        assert "Tuesday" in context.dates 