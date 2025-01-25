"""Structured logging setup."""

import logging
from typing import Any
from infrastructure.config import Config

def setup_logging(config: Config):
    """Configure application logging.
    
    Args:
        config: Application configuration
    """
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    # Suppress unnecessary messages
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('PySide6').setLevel(logging.WARNING)
    
    # Log application startup
    logging.info("Application starting up...")