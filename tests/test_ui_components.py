"""Tests for UI components."""
from PySide6.QtWidgets import QApplication
import pytest

@pytest.fixture(scope="session")
def qt_application():
    """Fixture providing QApplication instance."""
    app = QApplication.instance() or QApplication([])
    yield app
    # Don't quit the application to maintain singleton

def test_button_component(qt_application):
    """Test button component initialization."""
    from ui.components.button import StyledButton
    
    button = StyledButton("Test")
    assert button.text() == "Test"
    assert button.isEnabled()

def test_label_component(qt_application):
    """Test label component initialization."""
    from ui.components.label import StyledLabel
    
    label = StyledLabel("Test Label")
    label.show()
    assert label.text() == "Test Label"
    assert label.isVisible()

def test_file_browser_dialog(qt_application):
    """Test file browser dialog initialization."""
    from ui.components.file_browser import FileBrowserDialog
    
    dialog = FileBrowserDialog(None)
    dialog.setModal(True)
    assert dialog.windowTitle() == "Select Files"
    assert dialog.isModal()

def test_input_component(qt_application):
    """Test input component initialization."""
    from ui.components.input import StyledInput
    
    input_field = StyledInput()
    assert input_field.placeholderText() == ""
    assert input_field.isEnabled()
    
    input_field.setPlaceholderText("Enter text")
    assert input_field.placeholderText() == "Enter text"