"""Test UI components."""

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from ui.components.button import StyledButton
from ui.components.input import StyledInput
from ui.components.form_builder import FormBuilder
from ui.components.checkbox import Checkbox
from ui.themes.theme_engine import ThemeEngine

def test_form_builder(qtbot):
    """Test form builder component."""
    
    # Sample form schema
    schema = {
        "fields": [
            {
                "name": "username",
                "type": "text",
                "label": "Username",
                "required": True
            },
            {
                "name": "email",
                "type": "email",
                "label": "Email Address",
                "required": True
            },
            {
                "name": "password",
                "type": "password",
                "label": "Password",
                "required": True
            }
        ]
    }
    
    # Create form
    form = FormBuilder(schema)
    qtbot.addWidget(form)
    form.show()  # Make widget visible for testing
    QTest.qWait(100)  # Wait for form to initialize
    
    # Test form creation
    assert len(form.fields) == 3
    assert "username" in form.inputs
    assert "email" in form.inputs
    assert "password" in form.inputs
    
    # Test validation before submit
    assert not form.error_labels["username"].isVisible()
    
    # Test required field validation
    form._handle_submit()  # Should show errors
    QTest.qWait(100)  # Wait for validation
    
    assert form.error_labels["username"].isVisible()
    assert form.error_labels["username"].text() == "This field is required"
    
    # Test input and validation clearing
    qtbot.keyClicks(form.inputs["username"], "testuser")
    QTest.qWait(100)  # Wait for validation
    
    assert form.fields["username"].value == "testuser"
    assert not form.error_labels["username"].isVisible()
    
    # Test full form submission
    submitted_data = None
    def handle_submit(data):
        nonlocal submitted_data
        submitted_data = data
    
    form.submitted.connect(handle_submit)
    
    qtbot.keyClicks(form.inputs["email"], "test@example.com")
    qtbot.keyClicks(form.inputs["password"], "password123")
    QTest.qWait(100)
    
    form._handle_submit()
    QTest.qWait(100)
    
    assert submitted_data == {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }

def test_form_builder_from_json(tmp_path, qtbot):
    """Test creating form from JSON file."""
    
    # Create temp schema file
    schema_file = tmp_path / "test_form.json"
    schema_file.write_text("""
    {
        "fields": [
            {
                "name": "title",
                "type": "text",
                "label": "Title",
                "required": true
            }
        ]
    }
    """)
    
    # Create form from file
    form = FormBuilder.from_json_file(str(schema_file))
    qtbot.addWidget(form)
    form.show()  # Make widget visible for testing
    QTest.qWait(100)
    
    assert len(form.fields) == 1
    assert "title" in form.inputs
    
    # Test validation
    form._handle_submit()
    QTest.qWait(100)
    
    assert form.error_labels["title"].isVisible()
    assert form.error_labels["title"].text() == "This field is required"

def test_checkbox_basic(qtbot):
    """Test basic checkbox functionality."""
    checkbox = Checkbox("Test Checkbox")
    qtbot.addWidget(checkbox)
    
    # Verify initial state
    assert not checkbox.is_checked()
    assert checkbox._checkbox.text() == "Test Checkbox"
    
    # Test state change
    checkbox.set_checked(True)
    assert checkbox.is_checked()
    
    # Test text change
    checkbox.set_text("New Text")
    assert checkbox._checkbox.text() == "New Text"

def test_checkbox_theme(qtbot):
    """Test checkbox theme integration."""
    checkbox = Checkbox("Test")
    qtbot.addWidget(checkbox)
    
    # Verify initial theme
    assert checkbox._checkbox.styleSheet() != ""
    
    # Change theme and verify update
    engine = ThemeEngine.get_instance()
    engine.switch_theme("dark")
    assert checkbox._checkbox.styleSheet() != ""