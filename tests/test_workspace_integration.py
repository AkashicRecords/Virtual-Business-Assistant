import pytest
from gmail_assistant.workspace import WorkspaceManager

class TestWorkspaceIntegration:
    @pytest.fixture
    def workspace_manager(self):
        return WorkspaceManager()

    def test_cross_service_context(self, workspace_manager):
        """Test context awareness across services"""
        project_name = "Website Launch"
        
        # Add different types of content
        workspace_manager.add_email({"subject": "Website Launch Timeline"})
        workspace_manager.add_document({"title": "Launch Plan"})
        workspace_manager.add_event({"summary": "Launch Meeting"})
        
        # Test context retrieval
        context = workspace_manager.get_project_context(project_name)
        assert len(context.related_items) > 0
        assert any(item.type == "email" for item in context.related_items)
        assert any(item.type == "document" for item in context.related_items) 