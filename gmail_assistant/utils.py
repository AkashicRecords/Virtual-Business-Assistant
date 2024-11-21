"""Utility functions and error handling."""
import logging
import os
from functools import wraps

# Set up logging
log_path = os.path.join(os.path.dirname(__file__), 'resources', 'app.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('GmailAssistant')

def handle_errors(func):
    """Decorator for error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper 