from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QPainter, QColor, QBrush

class LoadingSpinner(QWidget):
    """Circular loading spinner component"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(20)  # Update every 20ms
        self.setFixedSize(40, 40)
        
    def update_angle(self):
        """Update rotation angle"""
        self.angle = (self.angle + 6) % 360
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event for spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(240, 240, 240)))
        painter.drawEllipse(2, 2, 36, 36)
        
        # Draw spinning arc
        painter.setBrush(QBrush(QColor(0, 123, 255)))
        painter.drawPie(2, 2, 36, 36, self.angle * 16, 120 * 16)
        
    def start(self):
        """Start spinner animation"""
        self.timer.start()
        self.show()
        
    def stop(self):
        """Stop spinner animation"""
        self.timer.stop()
        self.hide()