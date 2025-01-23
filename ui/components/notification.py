from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QColor, QLinearGradient, QBrush, QPainter
from typing import Optional

class Notification(QWidget):
    """Reusable notification component for displaying messages"""
    
    def __init__(
        self,
        message: str,
        type: str = "info",  # info, success, warning, error
        duration: int = 3000,  # milliseconds
        parent=None
    ):
        super().__init__(parent)
        self.type = type
        self.duration = duration
        self.init_ui(message)
        
    def init_ui(self, message: str):
        """Initialize notification UI"""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 80)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Message label
        self.label = QLabel(message, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        
        # Set background color based on type
        self.set_background_color()
        
        # Auto-close timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(self.duration)
        
    def set_background_color(self):
        """Set background color based on notification type"""
        colors = {
            "info": QColor(23, 162, 184),
            "success": QColor(40, 167, 69),
            "warning": QColor(255, 193, 7),
            "error": QColor(220, 53, 69)
        }
        self.bg_color = colors.get(self.type, colors["info"])
        
    def paintEvent(self, event):
        """Custom paint event for rounded corners and gradient"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, self.bg_color.lighter(120))
        gradient.setColorAt(1, self.bg_color.darker(120))
        
        # Draw rounded rect
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
    def show(self):
        """Show notification with animation"""
        super().show()
        self.animate_show()
        
    def animate_show(self):
        """Animate notification appearance"""
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()