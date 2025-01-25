"""Reusable loading spinner component."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer, Property, QSize
from PySide6.QtGui import QPainter, QColor, QPen

class LoadingSpinner(QWidget):
    """A customizable loading spinner widget."""

    def __init__(self, parent=None):
        """Initialize the loading spinner."""
        super().__init__(parent)
        
        # Spinner configuration
        self._color = QColor("#007AFF")
        self._lines = 8
        self._inner_radius = 10
        self._line_length = 10
        self._line_width = 3
        self._current_angle = 0
        
        # Setup widget
        self.setFixedSize(40, 40)
        self.setVisible(False)
        
        # Setup animation timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._timer.setInterval(100)
            
    def paintEvent(self, event):
        """Paint the spinner animation."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        for i in range(self._lines):
            painter.save()
            
            # Calculate opacity
            opacity = (i + 1) * (255 // self._lines)
            color = QColor(self._color)
            color.setAlpha(opacity)
            
            # Setup pen
            painter.setPen(QPen(color, self._line_width, Qt.SolidLine, Qt.RoundCap))
            
            # Draw line
            painter.translate(center_x, center_y)
            painter.rotate(self._current_angle + (360 / self._lines) * i)
            painter.drawLine(self._inner_radius, 0, self._inner_radius + self._line_length, 0)
            
            painter.restore()
            
    def _rotate(self):
        """Update rotation angle."""
        self._current_angle = (self._current_angle + 45) % 360
        self.update()
        
    def start(self):
        """Start the spinner animation."""
        self.setVisible(True)
        if not self._timer.isActive():
            self._timer.start()
            
    def stop(self):
        """Stop the spinner animation."""
        self.setVisible(False)
        if self._timer.isActive():
            self._timer.stop()
            
    @Property(QColor)
    def color(self):
        """Get spinner color."""
        return self._color
        
    @color.setter
    def color(self, color):
        """Set spinner color."""
        self._color = color