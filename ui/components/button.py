"""Reusable styled button component with theme support."""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize
from ui.themes.theme_engine import ThemeEngine

class StyledButton(QPushButton):
    """Custom styled button component with theme support."""
    
    def __init__(self, text: str = "", parent=None):
        """Initialize styled button.
        
        Args:
            text: Button text
            parent: Parent widget
        """
        super().__init__(text, parent)
        self._theme_engine = ThemeEngine.get_instance()
        self._variant = "primary"  # Default to primary style
        self._setup_button()
        
        # Subscribe to theme changes
        self._theme_engine.theme_changed.connect(self._on_theme_changed)
        
    def _setup_button(self):
        """Configure button widget."""
        self.setMinimumSize(QSize(100, 40))
        self.setCursor(Qt.PointingHandCursor)
        self._apply_current_style()
        
    def _on_theme_changed(self, _):
        """Handle theme changes."""
        self._apply_current_style()
        
    def _apply_current_style(self):
        """Apply current style based on variant."""
        theme = self._theme_engine.theme_data
        variant_bg = theme["button"]["primary_bg"] if self._variant == "primary" else theme["button"]["secondary_bg"]
        variant_hover = theme["primary_hover"] if self._variant == "primary" else theme["secondary_hover"]
        variant_pressed = theme["primary_pressed"] if self._variant == "primary" else theme["secondary_pressed"]
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {variant_bg};
                color: {theme["button"]["primary_text"]};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {variant_hover};
            }}
            QPushButton:pressed {{
                background-color: {variant_pressed};
            }}
            QPushButton:disabled {{
                background-color: {theme["button"]["disabled_bg"]};
                color: {theme["button"]["disabled_text"]};
            }}
        """)
        
    def set_primary(self):
        """Set primary button style."""
        self._variant = "primary"
        self._apply_current_style()
        
    def set_secondary(self):
        """Set secondary button style."""
        self._variant = "secondary"
        self._apply_current_style()