"""LLM integration for enhanced email processing."""
from openai import OpenAI
from .utils import handle_errors, logger
from .config import OPENAI_API_KEY

class LLMHandler:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    @handle_errors
    def generate_email(self, prompt):
        """Generate email content using GPT"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an email writing assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    @handle_errors
    def summarize_email(self, email_content):
        """Summarize email content"""
        prompt = f"Summarize this email concisely:\n{email_content}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content 