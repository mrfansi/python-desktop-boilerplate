"""Test theme engine and themed components."""

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from ui.themes.theme_engine import ThemeEngine
from ui.components.input import StyledInput
from ui.components.button import StyledButton

def test_theme_engine_singleton():
    """Test theme engine singleton pattern."""
    engine1 = ThemeEngine.get_instance()
    engine2 = ThemeEngine.get_instance()
    assert engine1 is engine2

def test_theme_switching():
    """Test theme switching functionality."""
    engine = ThemeEngine.get_instance()
    
    # Test initial theme
    assert engine.current_theme == "light"
    
    # Test switching to dark theme
    engine.switch_theme("dark")
    assert engine.current_theme == "dark"
    assert engine.get_color("background") == "#212529"
    
    # Test switching back to light theme
    engine.switch_theme("light")
    assert engine.current_theme == "light"
    assert engine.get_color("background") == "#ffffff"
    
    # Test invalid theme
    with pytest.raises(ValueError):
        engine.switch_theme("invalid")

def test_themed_input(qtbot):
    """Test themed input component."""
    engine = ThemeEngine.get_instance()
    # Start with light theme
    engine.switch_theme("light")
    
    input_widget = StyledInput(placeholder="Test Input")
    qtbot.addWidget(input_widget)
    
    # Get initial style
    initial_style = input_widget.styleSheet()
    
    # Switch theme
    engine.switch_theme("dark")
    QTest.qWait(100)  # Wait for signal propagation
    
    # Style should have changed
    assert input_widget.styleSheet() != initial_style
    assert "#2c3034" in input_widget.styleSheet()  # Dark theme input background

def test_themed_button(qtbot):
    """Test themed button component."""
    engine = ThemeEngine.get_instance()
    engine.switch_theme("light")  # Start with light theme
    
    button = StyledButton("Test Button")
    qtbot.addWidget(button)
    
    # Test primary style in light theme
    button.set_primary()
    QTest.qWait(100)
    light_primary_style = button.styleSheet()
    assert "#007bff" in light_primary_style  # Light theme primary color
    
    # Test secondary style in light theme
    button.set_secondary()
    QTest.qWait(100)
    light_secondary_style = button.styleSheet()
    assert "#6c757d" in light_secondary_style  # Light theme secondary color
    assert light_primary_style != light_secondary_style
    
    # Test primary style in dark theme
    engine.switch_theme("dark")
    QTest.qWait(100)
    button.set_primary()  # Need to set primary again to test dark primary color
    QTest.qWait(100)
    dark_primary_style = button.styleSheet()
    assert dark_primary_style != light_primary_style
    assert "#0d6efd" in dark_primary_style  # Dark theme primary color
    
    # Test secondary style in dark theme
    button.set_secondary()
    QTest.qWait(100)
    dark_secondary_style = button.styleSheet()
    assert "#6c757d" in dark_secondary_style  # Dark theme secondary color
    assert dark_primary_style != dark_secondary_style

def test_theme_change_event(qtbot):
    """Test theme change event handling."""
    engine = ThemeEngine.get_instance()
    engine.switch_theme("light")  # Ensure starting state
    
    # Track theme changes
    theme_changed = False
    def on_theme_change(theme_data):
        nonlocal theme_changed
        theme_changed = True
        assert isinstance(theme_data, dict)
        assert "background" in theme_data
    
    engine.theme_changed.connect(on_theme_change)
    
    # Switch theme
    engine.switch_theme("dark")
    QTest.qWait(100)  # Wait for signal propagation
    assert theme_changed

def test_component_theme_persistence(qtbot):
    """Test theme persistence across component instances."""
    engine = ThemeEngine.get_instance()
    engine.switch_theme("dark")
    QTest.qWait(100)
    
    # Create components
    input1 = StyledInput()
    input2 = StyledInput()
    qtbot.addWidget(input1)
    qtbot.addWidget(input2)
    
    QTest.qWait(100)  # Wait for styles to apply
    
    # Both should have dark theme
    assert input1.styleSheet() == input2.styleSheet()
    assert "#2c3034" in input1.styleSheet()  # Dark theme input background