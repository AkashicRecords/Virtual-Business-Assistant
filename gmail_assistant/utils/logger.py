"""Logging configuration for Gmail Assistant."""
import sys
from pathlib import Path
from loguru import logger

# Create logs directory if it doesn't exist
log_dir = Path.home() / ".gmail_assistant" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# Configure loguru
config = {
    "handlers": [
        # Console handler
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": "INFO",
        },
        # File handler
        {
            "sink": log_dir / "gmail_assistant.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            "rotation": "1 day",
            "retention": "7 days",
            "level": "DEBUG",
        },
    ],
}

# Remove default logger and apply new configuration
logger.remove()
for handler in config["handlers"]:
    logger.add(**handler)

# Export logger
__all__ = ["logger"] 