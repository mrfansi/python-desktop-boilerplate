"""Theme engine for managing application-wide theming."""

from typing import Dict, Any, Optional
from PySide6.QtCore import QObject, Signal
from ui.themes.theme_config import LIGHT_THEME, DARK_THEME, get_component_styles

class ThemeEngine(QObject):
    """Manages application-wide theme settings."""
    
    # Signals
    theme_changed = Signal(dict)  # Emitted when theme changes
    
    _instance: Optional['ThemeEngine'] = None
    
    def __new__(cls):
        """Ensure single instance (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        """Initialize theme engine if not already initialized."""
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
            self._current_theme = "light"
            self._theme_data = LIGHT_THEME.copy()
            
    @property
    def current_theme(self) -> str:
        """Get current theme name."""
        return self._current_theme
        
    @property
    def theme_data(self) -> Dict[str, Any]:
        """Get current theme data."""
        return self._theme_data.copy()  # Return copy to prevent modification
        
    def switch_theme(self, theme_name: str):
        """Switch to a different theme."""
        if theme_name not in ['light', 'dark']:
            raise ValueError("Theme must be 'light' or 'dark'")
            
        if theme_name == self._current_theme:
            return
            
        self._current_theme = theme_name
        self._theme_data = (LIGHT_THEME if theme_name == 'light' else DARK_THEME).copy()
        
        # Emit theme changed signal with new theme data
        self.theme_changed.emit(self._theme_data)
        
    def get_color(self, color_key: str) -> str:
        """Get color value from current theme."""
        return self._theme_data.get(color_key, "")
        
    def get_text_color(self, type_key: str = "primary") -> str:
        """Get text color from current theme."""
        return self._theme_data.get("text", {}).get(type_key, "")
        
    def get_component_style(self, component: str) -> str:
        """Get component-specific styles."""
        return get_component_styles(self._theme_data, component)
        
    @classmethod
    def get_instance(cls) -> 'ThemeEngine':
        """Get or create theme engine instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def apply_theme_to_widget(self, widget: 'QWidget', component_type: str):
        """Apply current theme to a widget."""
        style = self.get_component_style(component_type)
        if style:
            widget.setStyleSheet(style)