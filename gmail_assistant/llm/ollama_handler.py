"""Ollama LLM integration."""
import requests
from ..utils import handle_errors, logger

class OllamaHandler:
    def __init__(self, model="llama2"):
        self.base_url = "http://localhost:11434/api"
        self.model = model

    @handle_errors
    def generate(self, prompt, context=None):
        """Generate response using Ollama"""
        url = f"{self.base_url}/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "context": context,
            "stream": False
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['response']

    @handle_errors
    def analyze_command(self, text, context=None):
        """Analyze voice command with context"""
        prompt = f"""
        Analyze this voice command: "{text}"
        Previous context: {context if context else 'None'}
        
        Determine:
        1. Command intent
        2. Required actions
        3. Needed parameters
        4. Context requirements
        
        Return analysis in a clear, structured way.
        """
        return self.generate(prompt) 