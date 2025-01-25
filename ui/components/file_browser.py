"""Reusable file browser dialog component."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QFileDialog,
    QDialogButtonBox, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, Signal

class FileBrowserDialog(QDialog):
    """Custom file browser dialog."""
    
    files_selected = Signal(list)
    
    def __init__(self, parent=None, allowed_extensions=None):
        """Initialize file browser.
        
        Args:
            parent: Parent widget
            allowed_extensions: List of allowed file extensions (e.g. ['.txt', '.py'])
        """
        super().__init__(parent)
        self.setWindowTitle("Select Files")
        self.setMinimumSize(600, 400)
        self.allowed_extensions = allowed_extensions or []
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Selected files list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.NoSelection)
        layout.addWidget(self.file_list)
        
        # Button layout
        btn_layout = QHBoxLayout()
        
        # Add files button
        add_btn = QPushButton("Add Files")
        add_btn.clicked.connect(self._add_files)
        btn_layout.addWidget(add_btn)
        
        # Clear selection button
        clear_btn = QPushButton("Clear Selection")
        clear_btn.clicked.connect(self._clear_selection)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._handle_accept)
        buttons.rejected.connect(self._handle_reject)
        layout.addWidget(buttons)

    def _handle_accept(self):
        """Handle dialog acceptance."""
        selected_files = self.get_selected_files()
        self.files_selected.emit(selected_files)
        self.file_list.clear()
        self.done(QDialog.Accepted)

    def _handle_reject(self):
        """Handle dialog rejection."""
        self.file_list.clear()
        self.done(QDialog.Rejected)
        
    def _add_files(self):
        """Open file dialog to add files."""
        from PySide6.QtWidgets import QMessageBox
        
        # Build filter string from allowed extensions
        if self.allowed_extensions:
            filter_str = "Allowed Files ("
            filter_str += " ".join(f"*{ext}" for ext in self.allowed_extensions)
            filter_str += ");;All Files (*)"
        else:
            filter_str = "All Files (*)"
            
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "",
            filter_str
        )
        
        if files:
            invalid_files = []
            for file in files:
                if self.allowed_extensions:
                    ext = "." + file.split(".")[-1].lower()
                    if ext not in self.allowed_extensions:
                        invalid_files.append(file)
                        continue
                self.file_list.addItem(file)
                
            if invalid_files:
                QMessageBox.warning(
                    self,
                    "Invalid Files",
                    f"The following files have invalid extensions:\n"
                    f"{', '.join(invalid_files)}\n"
                    f"Allowed extensions: {', '.join(self.allowed_extensions)}"
                )
                
    def _clear_selection(self):
        """Clear selected files."""
        self.file_list.clear()
        
    def get_selected_files(self) -> list:
        """Get list of selected files.
        
        Returns:
            List of file paths
        """
        return [self.file_list.item(i).text()
                for i in range(self.file_list.count())]