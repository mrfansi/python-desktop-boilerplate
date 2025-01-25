"""Base widget with theme support."""

from typing import Dict, Optional
from PySide6.QtWidgets import QWidget
from ui.themes.theme_engine import ThemeEngine

class ThemedWidget(QWidget):
    """Base class for theme-aware widgets."""
    
    def __init__(self, parent=None, component_type: str = ""):
        """Initialize themed widget.
        
        Args:
            parent: Parent widget
            component_type: Type of component for styling
        """
        super().__init__(parent)
        self._component_type = component_type
        self._theme_engine = ThemeEngine.get_instance()
        
        # Subscribe to theme changes if component type specified
        if component_type:
            self._theme_engine.theme_changed.connect(self._on_theme_changed)
            self._apply_initial_theme()
            
    def _apply_initial_theme(self):
        """Apply initial theme data."""
        theme_data = self._theme_engine.theme_data
        self._apply_theme(theme_data)
        
    def _on_theme_changed(self, theme_data: Dict):
        """Handle theme changes."""
        self._apply_theme(theme_data)
    
    def _apply_theme(self, theme_data: Dict):
        """Apply theme styles to widget.
        
        Args:
            theme_data: Theme configuration data
        """
        # Override in subclasses
        pass