"""Reusable card container component."""

from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt

class Card(QFrame):
    """Custom styled card container."""
    
    def __init__(self, parent=None):
        """Initialize card container.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_style()
        self._setup_layout()
        
    def _setup_style(self):
        """Configure card styling."""
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 16px;
            }
        """)
        
    def _setup_layout(self):
        """Configure card layout."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.setLayout(self.layout)
        
    def add_widget(self, widget):
        """Add widget to card.
        
        Args:
            widget: Widget to add
        """
        self.layout.addWidget(widget)