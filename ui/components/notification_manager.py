from PySide6.QtCore import QObject, Signal, QPoint, QTimer
from typing import List
from weakref import WeakSet
from .notification import Notification

class NotificationManager(QObject):
    """Centralized manager for displaying notifications"""
    
    instance = None
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notifications = WeakSet()
        self.offset = QPoint(20, 20)
        self.spacing = 10
        
        # Setup cleanup timer
        self.cleanup_timer = QTimer(self)
        self.cleanup_timer.timeout.connect(self.cleanup_notifications)
        self.cleanup_timer.start(1000)  # Check every second
        
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls.instance is None:
            cls.instance = NotificationManager()
        return cls.instance
        
    def show_notification(
        self,
        message: str,
        type: str = "info",
        duration: int = 3000
    ):
        """Show a new notification"""
        notification = Notification(message, type, duration)
        self.position_notification(notification)
        notification.show()
        self.notifications.add(notification)
        
    def position_notification(self, notification):
        """Position notification in bottom-right corner"""
        screen_geometry = notification.screen().availableGeometry()
        x = screen_geometry.width() - notification.width() - self.offset.x()
        y = screen_geometry.height() - notification.height() - self.offset.y()
        
        # Stack notifications
        for n in self.notifications:
            y -= n.height() + self.spacing
            
        notification.move(x, y)
        
    def cleanup_notifications(self):
        """Remove closed notifications from weak set"""
        # WeakSet automatically removes collected objects
        pass