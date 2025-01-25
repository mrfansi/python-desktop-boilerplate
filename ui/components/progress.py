"""Reusable progress bar component."""

import logging
from PySide6.QtWidgets import (
    QProgressBar, QWidget, QVBoxLayout,
    QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, Property, Signal
from PySide6.QtGui import QColor
from infrastructure.error_handling.handlers import handle_errors

logger = logging.getLogger(__name__)

class StyledProgressBar(QProgressBar):
    """A customizable progress bar widget."""
    
    valueChanged = Signal(int)
    
    def __init__(self, parent=None, show_percentage=True, show_text=False):
        """Initialize progress bar.
        
        Args:
            parent: Parent widget
            show_percentage: Whether to show percentage text
            show_text: Whether to show custom text
        """
        super().__init__(parent)
        
        # Configuration
        self._color = QColor("#007AFF")
        self._height = 40
        self._show_percentage = show_percentage
        self._show_text = show_text
        self._custom_text = ""
        self._animate = True
        
        # Setup progress bar
        self.setTextVisible(show_percentage)
        self.setMinimumHeight(self._height)
        self.setMaximumHeight(self._height)
        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(100)
        
        # Set size policy
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        
        # Apply base style
        self._update_style()
        
    @handle_errors
    def _update_style(self):
        """Update progress bar styling."""
        try:
            style = f"""
                QProgressBar {{
                    border: none;
                    border-radius: {self._height // 2}px;
                    background-color: {self._color.name()}20;
                    text-align: center;
                }}
                
                QProgressBar::chunk {{
                    border-radius: {self._height // 2}px;
                    background-color: {self._color.name()};
                }}
            """
            self.setStyleSheet(style)
        except Exception as e:
            logger.error(f"Error updating progress bar style: {str(e)}", exc_info=True)
            raise
        
    @handle_errors
    def setValue(self, value):
        """Set progress value (0-100)."""
        try:
            if not isinstance(value, (int, float)):
                raise ValueError(f"Progress value must be a number, got {type(value)}")
            
            if not 0 <= value <= 100:
                raise ValueError(f"Progress value must be between 0 and 100, got {value}")
                
            logger.debug(f"Setting progress value to: {value}")
            super().setValue(value)
            self.valueChanged.emit(value)
            
            if self._show_text and self._custom_text:
                self.setFormat(f"{self._custom_text} ({value}%)")
            elif self._show_percentage:
                self.setFormat(f"{value}%")
                
        except Exception as e:
            logger.error(f"Error setting progress value: {str(e)}", exc_info=True)
            raise
            
    @Property(str)
    def text(self):
        """Get custom text."""
        return self._custom_text
        
    @text.setter
    def text(self, text):
        """Set custom text."""
        self._custom_text = text
        if self._show_text:
            self.setFormat(f"{text} ({self.value()}%)")
            
    @Property(QColor)
    def color(self):
        """Get progress bar color."""
        return self._color
        
    @color.setter
    def color(self, color):
        """Set progress bar color."""
        self._color = color
        self._update_style()
        
    @Property(int)
    def bar_height(self):
        """Get progress bar height."""
        return self._height
        
    @bar_height.setter
    def bar_height(self, height):
        """Set progress bar height."""
        self._height = height
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self._update_style()

class ProgressBarWithLabel(QWidget):
    """Progress bar with an optional label."""
    
    def __init__(self, parent=None, label="", show_percentage=True, show_text=False):
        """Initialize progress bar with label.
        
        Args:
            parent: Parent widget
            label: Text label above progress bar
            show_percentage: Whether to show percentage in progress bar
            show_text: Whether to show custom text in progress bar
        """
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.setLayout(layout)
        
        # Add label if provided
        if label:
            self.label = QLabel(label)
            self.label.setAlignment(Qt.AlignLeft)
            layout.addWidget(self.label)
            
        # Add progress bar
        self.progress_bar = StyledProgressBar(
            self,
            show_percentage=show_percentage,
            show_text=show_text
        )
        layout.addWidget(self.progress_bar)
        
    def setValue(self, value):
        """Set progress value (0-100)."""
        self.progress_bar.setValue(value)
        
    def setColor(self, color):
        """Set progress bar color."""
        self.progress_bar.color = color
        
    def setText(self, text):
        """Set custom text."""
        self.progress_bar.text = text
        
    def setBarHeight(self, height):
        """Set progress bar height."""
        self.progress_bar.bar_height = height