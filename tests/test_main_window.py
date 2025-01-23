"""Tests for main window functionality."""

import pytest
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

def test_main_window_initialization(qt_application):
    """Test main window creation and basic properties."""
    from ui.main_window import MainWindow
    from infrastructure.config import Config
    
    config = Config()
    window = MainWindow(config)
    
    assert window.windowTitle() == "Python Desktop App"
    assert window.isVisible() is False
    
    window.show()
    assert window.isVisible() is True

def test_main_window_resize(qt_application):
    """Test window resizing behavior."""
    from ui.main_window import MainWindow
    from infrastructure.config import Config
    
    config = Config()
    window = MainWindow(config)
    window.show()
    
    initial_size = window.size()
    QTest.qWait(100)  # Allow window to initialize
    
    # Test minimum size constraints
    window.resize(200, 200)
    assert window.size().width() >= 800
    assert window.size().height() >= 600
    
    # Test maximum size constraints
    window.resize(2000, 2000)
    assert window.size().width() <= 2000
    assert window.size().height() <= 2000

def test_main_window_close_event(qt_application):
    """Test window close event handling."""
    from ui.main_window import MainWindow
    from infrastructure.config import Config
    
    config = Config()
    window = MainWindow(config)
    window.show()
    
    # Simulate close event
    QTest.keyClick(window, Qt.Key_Escape)
    assert window.isVisible() is True  # Escape key doesn't close window