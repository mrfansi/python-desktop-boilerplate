"""Reusable styled label component."""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class StyledLabel(QLabel):
    """Custom styled label component."""
    
    def __init__(self, text: str = "", parent=None):
        """Initialize styled label.
        
        Args:
            text: Label text
            parent: Parent widget
        """
        super().__init__(text, parent)
        self._setup_base_style()
        
    def _setup_base_style(self):
        """Configure base label styling."""
        self.setStyleSheet("""
            QLabel {
                color: #212529;
                font-size: 14px;
                margin: 4px 0;
            }
        """)
        
    def set_heading(self, level: int = 1):
        """Set heading style.
        
        Args:
            level: Heading level (1-6)
        """
        sizes = [32, 28, 24, 20, 18, 16]
        weight = QFont.Weight.Bold
        
        if 1 <= level <= 6:
            self.setStyleSheet(f"""
                QLabel {{
                    font-size: {sizes[level-1]}px;
                    font-weight: {weight};
                    margin: 8px 0;
                }}
            """)
            
    def set_muted(self):
        """Set muted text style."""
        self.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                margin: 4px 0;
            }
        """)