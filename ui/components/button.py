from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Slot
from typing import Optional, Callable

class Button(QPushButton):
    """Custom button component with consistent styling and behavior"""
    
    def __init__(
        self,
        text: str,
        on_click: Optional[Callable] = None,
        parent=None
    ):
        super().__init__(text, parent)
        self.setMinimumSize(100, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
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
        """)
        
        if on_click:
            self.clicked.connect(on_click)
            
    @Slot()
    def click(self):
        """Programmatically trigger click event"""
        self.clicked.emit()