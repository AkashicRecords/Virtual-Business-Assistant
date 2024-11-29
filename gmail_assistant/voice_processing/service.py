"""Voice processing service for the Gmail Assistant."""
import speech_recognition as sr
from dataclasses import dataclass
from ..utils import logger, handle_errors

@dataclass
class AudioResult:
    text: str
    confidence: float = 0.0

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000  # Adjust if needed
        
    @handle_errors
    def process_audio(self, audio_data):
        """Process audio data and return recognized text"""
        try:
            text = self.recognizer.recognize_google(audio_data)
            logger.info(f"Recognized text: {text}")
            return AudioResult(text=text.lower(), confidence=0.9)
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {str(e)}")
            return None 