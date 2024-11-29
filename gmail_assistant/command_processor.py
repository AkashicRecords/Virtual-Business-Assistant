"""Process voice commands and map to actions."""
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from googleapiclient.errors import HttpError
from .error_handler import handle_errors, GmailAssistantError
import base64
from email.mime.text import MIMEText
import logging
from bs4 import BeautifulSoup
import html2text

logger = logging.getLogger(__name__)

class CommandProcessor:
    def __init__(self):
        self.gmail_service = None
        self.commands = {
            'read': self._handle_read,
            'send': self._handle_send,
            'delete': self._handle_delete,
            'search': self._handle_search,
            'unread': self._handle_unread,
            'important': self._handle_important
        }
    
    def set_gmail_service(self, service):
        """Set Gmail service instance."""
        self.gmail_service = service

    def _get_email_content(self, message):
        """Extract email content from message payload."""
        if 'parts' in message['payload']:
            parts = message['payload']['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode()
                elif part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        html_content = base64.urlsafe_b64decode(data).decode()
                        return html2text.html2text(html_content)
        elif 'body' in message['payload']:
            data = message['payload']['body'].get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode()
        return "No content available"

    @handle_errors
    def _handle_read(self, words):
        """Handle read email commands."""
        try:
            query = ""
            max_results = 1

            if "from" in words:
                sender_idx = words.index("from") + 1
                if sender_idx < len(words):
                    sender = words[sender_idx]
                    query = f"from:{sender}"

            if "subject" in words:
                subject_idx = words.index("subject") + 1
                if subject_idx < len(words):
                    subject = words[subject_idx]
                    query = f"subject:{subject}"

            if "last" in words or "latest" in words:
                try:
                    num_idx = words.index("last") + 1
                    max_results = int(words[num_idx])
                except (ValueError, IndexError):
                    max_results = 1

            results = self.gmail_service.users().messages().list(
                userId='me', maxResults=max_results, q=query).execute()
            messages = results.get('messages', [])

            if not messages:
                return "No emails found."

            response = ""
            for message in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=message['id']).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown sender')
                content = self._get_email_content(msg)

                response += f"\nFrom: {sender}\nSubject: {subject}\n\nContent:\n{content}\n"
                response += "\n" + "-"*50 + "\n"

            return response

        except HttpError as error:
            raise GmailAssistantError(f"Error reading email: {str(error)}")

    @handle_errors
    def _handle_send(self, words):
        """Handle send email commands."""
        # Note: This should be integrated with GUI compose window
        try:
            # Example of sending email programmatically
            message = MIMEText('This is a test email')
            message['to'] = 'recipient@example.com'
            message['subject'] = 'Test Subject'
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self.gmail_service.users().messages().send(
                userId='me', body={'raw': raw}).execute()
            
            return "Email sent successfully"
        except HttpError as error:
            raise GmailAssistantError(f"Error sending email: {str(error)}")

    @handle_errors
    def _handle_delete(self, words):
        """Handle delete email commands."""
        try:
            query = ""
            if "from" in words:
                sender_idx = words.index("from") + 1
                if sender_idx < len(words):
                    sender = words[sender_idx]
                    query = f"from:{sender}"

            results = self.gmail_service.users().messages().list(
                userId='me', maxResults=1, q=query).execute()
            messages = results.get('messages', [])

            if not messages:
                return "No emails found to delete."

            msg = self.gmail_service.users().messages().get(
                userId='me', id=messages[0]['id']).execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown sender')

            # Move to trash instead of permanent deletion
            self.gmail_service.users().messages().trash(
                userId='me', id=messages[0]['id']).execute()

            return f"Moved email to trash - From: {sender}, Subject: {subject}"

        except HttpError as error:
            raise GmailAssistantError(f"Error deleting email: {str(error)}")

    @handle_errors
    def _handle_search(self, words):
        """Handle search email commands."""
        try:
            # Build search query from command
            search_terms = []
            if "from" in words:
                idx = words.index("from") + 1
                if idx < len(words):
                    search_terms.append(f"from:{words[idx]}")
            
            if "subject" in words:
                idx = words.index("subject") + 1
                if idx < len(words):
                    search_terms.append(f"subject:{words[idx]}")
            
            if "after" in words:
                idx = words.index("after") + 1
                if idx < len(words):
                    search_terms.append(f"after:{words[idx]}")

            query = " ".join(search_terms) if search_terms else " ".join(words[words.index("search")+1:])
            
            if not query:
                return "Please specify search terms"

            results = self.gmail_service.users().messages().list(
                userId='me', q=query, maxResults=5).execute()
            messages = results.get('messages', [])

            if not messages:
                return f"No emails found matching '{query}'"

            response = f"Found {len(messages)} emails matching '{query}':\n\n"
            
            for msg_id in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=msg_id['id']).execute()
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown sender')
                date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown date')
                
                response += f"From: {sender}\nDate: {date}\nSubject: {subject}\n"
                response += "-"*50 + "\n"

            return response

        except HttpError as error:
            raise GmailAssistantError(f"Error searching emails: {str(error)}")

    @handle_errors
    def _handle_unread(self, words):
        """Handle unread emails command."""
        try:
            results = self.gmail_service.users().messages().list(
                userId='me', q='is:unread', maxResults=5).execute()
            messages = results.get('messages', [])

            if not messages:
                return "No unread emails found."

            response = f"You have {len(messages)} unread emails:\n\n"
            
            for msg_id in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=msg_id['id']).execute()
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown sender')
                
                response += f"From: {sender}\nSubject: {subject}\n"
                response += "-"*50 + "\n"

            return response

        except HttpError as error:
            raise GmailAssistantError(f"Error fetching unread emails: {str(error)}")

    @handle_errors
    def _handle_important(self, words):
        """Handle important emails command."""
        try:
            results = self.gmail_service.users().messages().list(
                userId='me', q='is:important', maxResults=5).execute()
            messages = results.get('messages', [])

            if not messages:
                return "No important emails found."

            response = f"Found {len(messages)} important emails:\n\n"
            
            for msg_id in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=msg_id['id']).execute()
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown sender')
                
                response += f"From: {sender}\nSubject: {subject}\n"
                response += "-"*50 + "\n"

            return response

        except HttpError as error:
            raise GmailAssistantError(f"Error fetching important emails: {str(error)}") 