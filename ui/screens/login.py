from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ..components.notification_manager import NotificationManager
from PySide6.QtCore import Signal
from infrastructure.auth.middleware import AuthManager
from ..components.button import Button
from ..components.input import Input

class LoginForm(QWidget):
    """Reusable login form component with configurable authentication.
    
    Args:
        auth_manager: Authentication manager instance
        parent: Optional parent widget
        show_register: Whether to show register link
        show_forgot_password: Whether to show forgot password link
    """
    
    login_success = Signal(str)  # Emits user_id on success
    login_failed = Signal(str)  # Emits error message on failure
    
    def __init__(
        self,
        auth_manager: AuthManager,
        parent=None,
        show_register: bool = False,
        show_forgot_password: bool = False
    ):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.show_register = show_register
        self.show_forgot_password = show_forgot_password
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Username field
        self.username_input = Input(
            placeholder="Username",
            parent=self
        )
        layout.addWidget(self.username_input)
        
        # Password field
        self.password_input = Input(
            placeholder="Password",
            is_password=True,
            parent=self
        )
        layout.addWidget(self.password_input)
        
        # Login button
        self.login_btn = Button(
            text="Login",
            on_click=self.attempt_login,
            parent=self
        )
        layout.addWidget(self.login_btn)
        
        # Status label
        self.status_label = QLabel(self)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def attempt_login(self):
        """Handle login attempt with proper validation and error handling"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validate inputs
        if not username or not password:
            error_msg = "Please enter both username and password"
            self.login_failed.emit(error_msg)
            NotificationManager.get_instance().show_notification(
                error_msg,
                type="error"
            )
            return
            
        try:
            # TODO: Implement actual authentication
            # For now, use a mock user ID
            user_id = f"user_{username}"  # Replace with actual authentication
            self.auth_manager.login(user_id)
            self.login_success.emit(user_id)
            self.status_label.setText("Login successful!")
            
        except Exception as e:
            error_msg = f"Login failed: {str(e)}"
            self.login_failed.emit(error_msg)
            QMessageBox.critical(self, "Login Error", error_msg)