"""Main application entry point."""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from infrastructure.config import load_config
from infrastructure.logging import setup_logging
from infrastructure.security.env_validator import EnvironmentValidator
from infrastructure.auth.middleware import AuthManager
from infrastructure.auth.decorators import init_auth_decorators

def get_roles_for_user(user_id: str):
    """Example implementation of role provider"""
    # This should be replaced with actual role fetching logic
    from infrastructure.auth.models import Role, Permission
    return [
        Role(
            id='admin-role',
            name='Admin',
            description='System administrator',
            permissions=[Permission.MANAGE_USERS, Permission.MANAGE_ROLES]
        )
    ]
from services.i18n_service import I18nService

def main():
    """Initialize and run the application."""
    try:
        # Validate environment variables
        env_config = EnvironmentValidator.validate()
        
        # Load configuration
        config = load_config()
        
        # Setup logging
        setup_logging(config)
        
        # Initialize authentication system
        auth_manager = AuthManager(get_roles_for_user)
        auth_decorators = init_auth_decorators(auth_manager)
        
        # Create or get existing application instance
        app = QApplication.instance() or QApplication([])
        
        # Initialize i18n
        locale_dir = Path(__file__).parent / "locales"
        i18n = I18nService(app, locale_dir)
        i18n.set_language(config.get("language", "en"))
        
        # Create main window with authentication
        window = MainWindow(config, auth_manager, i18n)
        window.show()
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        # Show error message if initialization fails
        app = QApplication.instance() or QApplication([])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Application Initialization Failed")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        msg.exec()
        sys.exit(1)

if __name__ == "__main__":
    main()