"""Handle application errors and exceptions."""
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailAssistantError(Exception):
    """Base exception class for Gmail Assistant."""
    pass

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise GmailAssistantError(f"Operation failed: {str(e)}")
    return wrapper 