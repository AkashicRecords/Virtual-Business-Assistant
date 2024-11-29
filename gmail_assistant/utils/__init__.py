"""Utility functions and decorators for Gmail Assistant."""
import functools
from .logger import logger

def handle_errors(func):
    """Decorator to handle and log errors."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

__all__ = ['logger', 'handle_errors'] 