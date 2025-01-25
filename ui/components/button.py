from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Slot, Property
from typing import Optional, Callable
from .loading_spinner import LoadingSpinner

class Button(QPushButton):
    """Custom button component with consistent styling and behavior"""
    
    def __init__(
        self,
        text: str,
        on_click: Optional[Callable] = None,
        parent=None
    ):
        super().__init__(parent)
        self._loading = False
        self._text = text
        
        # Main layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(12, 8, 12, 8)
        self.layout.setSpacing(8)
        
        # Text label
        self.text_widget = QPushButton(text, self)
        self.text_widget.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 0;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.text_widget)
        
        # Loading spinner
        self.spinner = LoadingSpinner(self)
        self.spinner.hide()
        self.layout.addWidget(self.spinner)
        
        self.setLayout(self.layout)
        
        # Styling
        self.setMinimumSize(100, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 4px;
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
        
        if on_click:
            self.clicked.connect(on_click)
            
    @Property(bool)
    def loading(self) -> bool:
        return self._loading
        
    @loading.setter
    def loading(self, value: bool):
        self._loading = value
        self.setEnabled(not value)
        self.text_widget.setVisible(not value)
        self.spinner.setVisible(value)
        if value:
            self.spinner.start()
        else:
            self.spinner.stop()
            
    @Slot()
    def click(self):
        """Programmatically trigger click event"""
        self.clicked.emit()