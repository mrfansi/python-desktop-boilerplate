"""Reusable input field component."""

from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal

class StyledInput(QLineEdit):
    """Custom styled input field."""
    
    enter_pressed = Signal()
    
    def __init__(self, placeholder: str = "", parent=None):
        """Initialize styled input.
        
        Args:
            placeholder: Input placeholder text
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_style(placeholder)
        
    def _setup_style(self, placeholder: str):
        """Configure input styling."""
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                color: #212529;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
            QLineEdit:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """)
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enter_pressed.emit()
        super().keyPressEvent(event)