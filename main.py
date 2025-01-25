"""Main application entry point."""

import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, QTimer, Qt, Slot
from ui.main_window import MainWindow
from infrastructure.config import load_config
from infrastructure.logging import setup_logging
from infrastructure.security.env_validator import EnvironmentValidator
from services.i18n_service import I18nService

logger = logging.getLogger(__name__)

class Application(QObject):
    """Application wrapper with hot reload support."""
    
    def __init__(self):
        """Initialize application."""
        super().__init__()
        self.app = None
        self.window = None
        self.config = None
        self.i18n = None
        self._reload_timer = None
        self._hot_reload_observer = None
        
    def initialize(self):
        """Initialize application components."""
        try:
            # Load environment variables
            load_dotenv()
            
            # Load configuration
            self.config = load_config()
            
            # Setup logging
            setup_logging(self.config)
            
            # Validate environment
            EnvironmentValidator.validate()
            
            # Create application instance
            self.app = QApplication.instance() or QApplication(sys.argv)
            
            # Initialize i18n
            locale_dir = Path(__file__).parent / "locales"
            self.i18n = I18nService(self.app, locale_dir)
            self.i18n.set_language(self.config.get("language", "en"))
            
            # Setup reload timer
            self._reload_timer = QTimer(self)
            self._reload_timer.setSingleShot(True)
            self._reload_timer.setInterval(100)  # Small delay to batch updates
            self._reload_timer.timeout.connect(self._do_reload_window)
            
            return True
            
        except Exception as e:
            self._show_error("Initialization Error", str(e))
            return False
            
    def create_window(self):
        """Create main application window."""
        try:
            # Create and show window
            self.window = MainWindow(self.config, self.i18n)
            self.window.show()
            
        except Exception as e:
            self._show_error("Window Creation Error", str(e))
            
    @Slot()
    def schedule_reload(self):
        """Schedule window reload from any thread."""
        if not self._reload_timer.isActive():
            self._reload_timer.start()
            
    def _do_reload_window(self):
        """Perform the window reload on main thread."""
        if self.window:
            try:
                logger.info("Reloading main window")
                # Store window state
                geometry = self.window.geometry()
                is_maximized = self.window.isMaximized()
                is_fullscreen = self.window.isFullScreen()
                
                # Create new window
                new_window = MainWindow(self.config, self.i18n)
                
                # Restore window state
                if is_fullscreen:
                    new_window.showFullScreen()
                elif is_maximized:
                    new_window.showMaximized()
                else:
                    new_window.setGeometry(geometry)
                    new_window.show()
                
                # Close old window
                old_window = self.window
                self.window = new_window
                old_window.close()
                old_window.deleteLater()
                
            except Exception as e:
                logger.error(f"Error reloading window: {str(e)}")
            
    def _show_error(self, title: str, message: str):
        """Show error message dialog."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec()
        
    def setup_hot_reload(self):
        """Setup hot reload if in development mode."""
        if self.config.get("env") != "production":
            try:
                from infrastructure.hot_reload import start_hot_reload
                self._hot_reload_observer = start_hot_reload(self.schedule_reload)
                logger.info("Hot reload enabled")
            except Exception as e:
                logger.error(f"Hot reload setup failed: {str(e)}")
        
def main():
    """Application entry point."""
    app = Application()
    
    if not app.initialize():
        sys.exit(1)
        
    app.create_window()
    app.setup_hot_reload()
    
    # Run application
    sys.exit(app.app.exec())

if __name__ == "__main__":
    main()