"""Reusable progress indicator component."""

from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Qt

class ProgressIndicator(QProgressBar):
    """Custom styled progress indicator."""
    
    def __init__(self, parent=None):
        """Initialize progress indicator.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_style()
        
    def _setup_style(self):
        """Configure progress bar styling."""
        self.setStyleSheet("""
            QProgressBar {
                background-color: #e9ecef;
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 4px;
            }
        """)
        
    def set_primary(self):
        """Set primary progress style."""
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #007bff;
            }
        """)
        
    def set_success(self):
        """Set success progress style."""
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #28a745;
            }
        """)
        
    def set_warning(self):
        """Set warning progress style."""
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #ffc107;
            }
        """)
        
    def set_danger(self):
        """Set danger progress style."""
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #dc3545;
            }
        """)