import pytest
from gmail_assistant.meetings import MeetingManager

class TestMeetingFeatures:
    @pytest.fixture
    def meeting_manager(self):
        return MeetingManager()

    def test_transcription(self, meeting_manager):
        """Test real-time transcription"""
        audio_chunk = b"sample_audio_data"
        result = meeting_manager.transcribe_chunk(audio_chunk)
        assert isinstance(result, str)

    def test_action_item_extraction(self, meeting_manager):
        """Test action item extraction from transcript"""
        transcript = "John will prepare the report by Friday"
        action_items = meeting_manager.extract_action_items(transcript)
        assert len(action_items) > 0
        assert action_items[0].assignee == "John"
        assert "report" in action_items[0].task 