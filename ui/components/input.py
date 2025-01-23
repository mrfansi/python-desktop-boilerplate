from PySide6.QtWidgets import QLineEdit
from typing import Optional

class Input(QLineEdit):
    """Custom input component with consistent styling and behavior"""
    
    def __init__(
        self,
        placeholder: str = "",
        is_password: bool = False,
        parent=None
    ):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumSize(200, 40)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                outline: 0;
                border-width: 2px;
            }
        """)
        
        if is_password:
            self.setEchoMode(QLineEdit.Password)