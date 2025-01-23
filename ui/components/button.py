"""Reusable styled button component."""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor

class StyledButton(QPushButton):
    """Custom styled button component."""
    
    def __init__(self, text: str = "", parent=None):
        """Initialize styled button.
        
        Args:
            text: Button text
            parent: Parent widget
        """
        super().__init__(text, parent)
        self._setup_style()
        
    def _setup_style(self):
        """Configure button styling."""
        self.setMinimumSize(QSize(100, 40))
        self.setCursor(Qt.PointingHandCursor)
        
        # Base style
        self.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
    def set_primary(self):
        """Set primary button style."""
        self.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        
    def set_secondary(self):
        """Set secondary button style."""
        self.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #4e555b;
            }
        """)