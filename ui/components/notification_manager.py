from PySide6.QtCore import QObject, Signal, QPoint
from typing import List
from .notification import Notification

class NotificationManager(QObject):
    """Centralized manager for displaying notifications"""
    
    instance = None
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notifications: List[Notification] = []
        self.offset = QPoint(20, 20)
        self.spacing = 10
        
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
        self.notifications.append(notification)
        
        # Connect close event to cleanup
        notification.destroyed.connect(self.cleanup_notifications)
        
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
        """Remove closed notifications from list"""
        self.notifications = [n for n in self.notifications if n.isVisible()]