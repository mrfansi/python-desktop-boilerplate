"""Pytest configuration and fixtures."""

import pytest
from PySide6.QtWidgets import QApplication
from dependency_injector import providers

@pytest.fixture(scope="session")
def qt_application():
    """Provide QApplication instance for GUI tests."""
    # Clean up any existing QApplication instance
    existing_app = QApplication.instance()
    if existing_app:
        existing_app.quit()
    
    app = QApplication([])
    try:
        yield app
    finally:
        app.quit()

@pytest.fixture
def config_provider():
    """Provide configuration for testing."""
    from infrastructure.config import Config
    return providers.Singleton(Config)

@pytest.fixture
def logger_provider(config_provider):
    """Provide logger for testing."""
    from infrastructure.logging import Logger
    return providers.Singleton(Logger, config=config_provider)