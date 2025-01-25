"""Dynamic form builder component with theme support."""

import json
from typing import Dict, Any, Optional, List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Signal, Qt
from ui.components.input import StyledInput
from ui.components.button import StyledButton
from ui.themes.theme_engine import ThemeEngine

class FormField:
    """Form field configuration."""
    
    def __init__(self, name: str, field_type: str = "text", 
                 label: str = "", required: bool = False):
        self.name = name
        self.field_type = field_type
        self.label = label
        self.required = required
        self.value = ""
        self.error = ""

class FormBuilder(QWidget):
    """Dynamic form generator that creates UI elements from JSON schema."""
    
    submitted = Signal(dict)  # Emits form data when submitted
    
    def __init__(self, schema: Dict[str, Any], parent=None):
        """Initialize form builder.
        
        Args:
            schema: Form configuration schema
            parent: Parent widget
        """
        super().__init__(parent)
        self._theme_engine = ThemeEngine.get_instance()
        self.fields: Dict[str, FormField] = {}
        self.inputs: Dict[str, StyledInput] = {}
        self.error_labels: Dict[str, QLabel] = {}
        
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        
        # Subscribe to theme changes
        self._theme_engine.theme_changed.connect(self._on_theme_changed)
        
        if schema:
            self.load_schema(schema)
            
    def load_schema(self, schema: Dict[str, Any]):
        """Load and build form from schema definition."""
        self._clear_form()
        
        grid = QGridLayout()
        row = 0
        
        for field_config in schema.get("fields", []):
            field = FormField(
                name=field_config["name"],
                field_type=field_config.get("type", "text"),
                label=field_config.get("label", ""),
                required=field_config.get("required", False)
            )
            self.fields[field.name] = field
            
            # Create and style label
            if field.label:
                label_text = f"{field.label}{'*' if field.required else ''}"
                label = QLabel(label_text)
                self._style_label(label)
                grid.addWidget(label, row, 0, Qt.AlignTop)
            
            # Create input
            input_widget = StyledInput(parent=self)
            if field.field_type == "password":
                input_widget.setEchoMode(StyledInput.Password)
            
            # Connect input changes
            input_widget.textChanged.connect(
                lambda text, name=field.name: self._handle_input_change(name, text)
            )
            
            self.inputs[field.name] = input_widget
            grid.addWidget(input_widget, row, 1)
            
            # Create error label
            error_label = QLabel()
            self._style_error_label(error_label)
            error_label.hide()  # Initially hidden
            self.error_labels[field.name] = error_label
            grid.addWidget(error_label, row + 1, 1)
            
            row += 2
            
        self._layout.addLayout(grid)
        
        # Add submit button
        submit_button = StyledButton("Submit", self)
        submit_button.set_primary()
        submit_button.clicked.connect(self._handle_submit)
        self._layout.addWidget(submit_button)
        
    def _clear_form(self):
        """Clear all form fields."""
        self.fields.clear()
        self.inputs.clear()
        self.error_labels.clear()
        
        # Clear layout
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def _style_label(self, label: QLabel):
        """Apply theme-aware styling to label."""
        theme = self._theme_engine.theme_data
        label.setStyleSheet(f"""
            QLabel {{
                color: {theme["text"]["primary"]};
                font-size: 14px;
                margin-bottom: 4px;
            }}
        """)
        
    def _style_error_label(self, label: QLabel):
        """Apply theme-aware styling to error label."""
        theme = self._theme_engine.theme_data
        label.setStyleSheet(f"""
            QLabel {{
                color: {theme["danger"]};
                font-size: 12px;
                margin-top: 4px;
                padding: 4px 0;
            }}
        """)
        
    def _handle_input_change(self, field_name: str, value: str):
        """Handle input value changes."""
        if field_name in self.fields:
            field = self.fields[field_name]
            field.value = value
            field.error = ""
            
            # Clear error if value is provided for required field
            if field.required and value:
                error_label = self.error_labels.get(field_name)
                if error_label and error_label.isVisible():
                    error_label.hide()
                    
    def _validate_field(self, field_name: str) -> bool:
        """Validate a single field."""
        field = self.fields.get(field_name)
        if not field:
            return False
            
        # Required field validation
        if field.required and not field.value:
            field.error = "This field is required"
            error_label = self.error_labels.get(field_name)
            if error_label:
                error_label.setText(field.error)
                error_label.setVisible(True)  # Explicitly set visible
                error_label.show()  # Ensure visible
            return False
            
        return True
        
    def _handle_submit(self):
        """Validate form and emit data if valid."""
        is_valid = True
        
        # Validate all fields
        for field_name in self.fields:
            if not self._validate_field(field_name):
                is_valid = False
                
        if is_valid:
            data = {
                name: field.value
                for name, field in self.fields.items()
            }
            self.submitted.emit(data)
            
    def _on_theme_changed(self, _):
        """Handle theme changes."""
        for field_name in self.fields:
            if field_name in self.error_labels:
                error_label = self.error_labels[field_name]
                self._style_error_label(error_label)
                
    @classmethod
    def from_json_file(cls, json_path: str, parent=None):
        """Create form from JSON schema file."""
        with open(json_path) as f:
            schema = json.load(f)
        return cls(schema, parent)