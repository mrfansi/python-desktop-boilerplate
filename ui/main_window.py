"""Main application window implementation."""

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget
from .screens.login import LoginForm
from infrastructure.auth.middleware import AuthManager
from PySide6.QtCore import Qt
from typing import Any
from ui.components.file_browser import FileBrowserDialog

class MainWindow(QMainWindow):
    """Main application window class."""
    
    def __init__(self, config: Any, auth_manager: AuthManager, i18n=None):
        """Initialize main window with configuration.
        
        Args:
            config: Application configuration object
            auth_manager: Authentication manager instance
            i18n: Optional internationalization service
        """
        super().__init__()
        self.config = config
        self.auth_manager = auth_manager
        self.i18n = i18n
        self.setWindowTitle("Python Desktop App")
        self.setMinimumSize(800, 600)
        
        # Create stacked widget for login/main content
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize login form
        self.login_form = LoginForm(self.auth_manager)
        self.login_form.login_success.connect(self.show_main_content)
        self.stacked_widget.addWidget(self.login_form)
        
        # Initialize main content
        self.main_content = QWidget()
        self.stacked_widget.addWidget(self.main_content)
        
        # Show login form by default
        self.stacked_widget.setCurrentWidget(self.login_form)
        
    def show_main_content(self):
        """Switch to main content after successful login"""
        # Initialize main UI components
        self._init_main_ui()
        self.stacked_widget.setCurrentWidget(self.main_content)
        
    def _init_main_ui(self):
        """Initialize main UI components"""
        # Add existing UI components here
        pass
        
        # Set window flags for native integration
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowMaximizeButtonHint
        )
        
        # Initialize UI components
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup window UI components."""
        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self._show_about)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Main content
        from PySide6.QtWidgets import (
            QWidget, QVBoxLayout, QLabel,
            QTextEdit, QPushButton
        )
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Apply base stylesheet
        from ui.styles import Styles
        self.setStyleSheet(Styles.get_stylesheet())
        
        # Add app info
        from ui.components.label import StyledLabel
        app_name = self.config.get("app.name", "Python Desktop App")
        app_version = self.config.get("app.version", "1.0.0")
        title_label = StyledLabel(f"{app_name} v{app_version}")
        title_label.set_heading(1)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Add placeholder content
        placeholder = StyledLabel("Your application content goes here")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder)
        
        # Add file browser button
        from ui.components.button import Button
        from ui.components.file_browser import FileBrowserDialog
        
        file_btn = Button("Open File Browser")
        file_btn.clicked.connect(self._show_file_browser)
        layout.addWidget(file_btn)
        
    def _show_file_browser(self):
        """Show file browser dialog."""
        from PySide6.QtCore import QTimer
        
        # Use QTimer to prevent multiple dialogs
        QTimer.singleShot(0, lambda: self._open_file_browser())
        
    def _open_file_browser(self):
        """Handle file browser dialog."""
        browser = FileBrowserDialog(self, allowed_extensions=['.txt', '.py'])
        if browser.exec():
            files = browser.get_selected_files()
            if files:
                self.statusBar().showMessage(f"Selected: {', '.join(files)}")
        browser.exec()
        
            
    def _show_about(self):
        """Show about dialog."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(self, "About",
            "Python Desktop App\nVersion 1.0.0\n\nA sample desktop application")