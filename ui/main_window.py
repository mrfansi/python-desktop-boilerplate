"""Main application window implementation."""

from typing import Any
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from ui.components.file_browser import FileBrowserDialog
from ui.components.button import StyledButton
from ui.components.loading_spinner import LoadingSpinner
from ui.components.progress import ProgressBarWithLabel

class MainWindow(QMainWindow):
    """Main application window class."""
    
    def __init__(self, config: Any, i18n=None):
        """Initialize main window with configuration."""
        super().__init__()
        self.config = config
        self.i18n = i18n
        self.setWindowTitle("Python Desktop App")
        self.setMinimumSize(800, 600)
        
        # Set window flags
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowMaximizeButtonHint
        )
        
        # Initialize UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup window UI components."""
        # Menu bar
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        help_menu = menubar.addMenu("&Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self._show_about)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # App title
        from ui.components.label import StyledLabel
        title = StyledLabel(f"Python Desktop App v1.0.0")
        title.set_heading(1)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Demo components section
        demo_container = QWidget()
        demo_layout = QVBoxLayout(demo_container)
        demo_layout.setAlignment(Qt.AlignCenter)
        
        # File browser button
        file_btn = StyledButton("Open File Browser")
        file_btn.clicked.connect(self._show_file_browser)
        demo_layout.addWidget(file_btn)
        
        # Loading spinner section
        spinner_btn = StyledButton("Toggle Loading")
        spinner_btn.clicked.connect(self._toggle_spinner)
        demo_layout.addWidget(spinner_btn)
        
        # Spinner container
        spinner_container = QWidget()
        spinner_container.setFixedHeight(60)
        spinner_layout = QVBoxLayout(spinner_container)
        spinner_layout.setAlignment(Qt.AlignCenter)
        
        self.spinner = LoadingSpinner()
        self.spinner.color = QColor("#007AFF")
        spinner_layout.addWidget(self.spinner)
        demo_layout.addWidget(spinner_container)
        
        # Progress bar
        self.progress = ProgressBarWithLabel(
            label="Download Progress",
            show_percentage=True,
            show_text=True
        )
        self.progress.setColor(QColor("#28a745"))
        self.progress.setText("Downloading...")
        self.progress.setValue(50)
        demo_layout.addWidget(self.progress)
        
        # Add demo container
        layout.addWidget(demo_container)
        
    def _show_file_browser(self):
        """Show file browser dialog."""
        browser = FileBrowserDialog(self, allowed_extensions=['.txt', '.py'])
        if browser.exec():
            files = browser.get_selected_files()
            if files:
                self.statusBar().showMessage(f"Selected: {', '.join(files)}")

    def _toggle_spinner(self):
        """Toggle loading spinner visibility."""
        if self.spinner.isVisible():
            self.spinner.stop()
        else:
            self.spinner.start()
            
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About",
            "Python Desktop App\nVersion 1.0.0\n\nA sample desktop application"
        )