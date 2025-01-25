"""Theme-aware checkbox component."""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QCheckBox, QWidget
from ui.components.base_themed_widget import ThemedWidget

class Checkbox(ThemedWidget):
    """Custom checkbox with theme support and enhanced features."""
    
    # Signals
    state_changed = Signal(bool)  # Emits new checked state
    
    def __init__(self, text: str = "", parent: QWidget = None):
        super().__init__(parent, component_type="checkbox")
        self._checkbox = QCheckBox(text, self)
        self._init_ui()
        self._connect_signals()
        
    def _init_ui(self):
        """Initialize UI components."""
        layout = self._create_layout()
        layout.addWidget(self._checkbox)
        self.setLayout(layout)
        
    def _connect_signals(self):
        """Connect internal signals."""
        self._checkbox.stateChanged.connect(
            lambda state: self.state_changed.emit(state == Qt.Checked)
        )
        
    def is_checked(self) -> bool:
        """Get current checked state."""
        return self._checkbox.isChecked()
    
    def set_checked(self, checked: bool):
        """Set checked state."""
        self._checkbox.setChecked(checked)
        
    def set_text(self, text: str):
        """Set checkbox label text."""
        self._checkbox.setText(text)
        
    def _apply_theme(self, theme_data: dict):
        """Apply theme styles to checkbox."""
        if not hasattr(self, '_checkbox'):
            return
            
        checkbox_theme = theme_data.get("checkbox", {})
        style = f"""
            QCheckBox {{
                color: {checkbox_theme.get("text", "#212529")};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {checkbox_theme.get("border", "#ced4da")};
                border-radius: 3px;
                background-color: {checkbox_theme.get("background", "#ffffff")};
            }}
            QCheckBox::indicator:checked {{
                background-color: {checkbox_theme.get("checked_bg", "#007bff")};
                border-color: {checkbox_theme.get("checked_border", "#007bff")};
            }}
            QCheckBox::indicator:disabled {{
                background-color: {checkbox_theme.get("disabled_bg", "#e9ecef")};
                border-color: {checkbox_theme.get("disabled_border", "#dee2e6")};
            }}
        """
        self._checkbox.setStyleSheet(style)