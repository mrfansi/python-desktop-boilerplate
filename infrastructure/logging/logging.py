"""Structured logging setup."""

import logging
from typing import Any
from infrastructure.config import Config

def setup_logging(config: Config):
    """Configure application logging.
    
    Args:
        config: Application configuration
    """
    logging_config = {
        "level": config.get("logging.level", "INFO"),
        "format": config.get("logging.format"),
        "handlers": [
            logging.StreamHandler()
        ]
    }
    
    logging.basicConfig(**logging_config)
    logging.info("Logging configured successfully")