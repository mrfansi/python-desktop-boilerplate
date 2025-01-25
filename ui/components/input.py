"""Reusable input field component with theme support."""

from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from ui.themes.theme_engine import ThemeEngine

class StyledInput(QLineEdit):
    """Custom styled input field with theme support."""
    
    enter_pressed = Signal()
    
    def __init__(self, placeholder: str = "", parent=None):
        """Initialize styled input.
        
        Args:
            placeholder: Input placeholder text
            parent: Parent widget
        """
        super().__init__(parent)
        self._theme_engine = ThemeEngine.get_instance()
        self._setup_input(placeholder)
        
        # Subscribe to theme changes
        self._theme_engine.theme_changed.connect(self._on_theme_changed)
        
    def _setup_input(self, placeholder: str):
        """Configure input widget."""
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self._apply_theme()
        
    def _on_theme_changed(self, _):
        """Handle theme changes."""
        self._apply_theme()
        
    def _apply_theme(self):
        """Apply current theme styles."""
        self._theme_engine.apply_theme_to_widget(self, "input")
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enter_pressed.emit()
        super().keyPressEvent(event)