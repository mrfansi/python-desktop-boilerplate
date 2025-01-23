"""Central stylesheet management."""

class Styles:
    """Application-wide styles and themes."""
    
    @staticmethod
    def get_stylesheet() -> str:
        """Get base application stylesheet.
        
        Returns:
            CSS stylesheet as string
        """
        return """
            /* Global styles */
            QWidget {
                background-color: #ffffff;
                color: #212529;
                font-family: sans-serif;
            }
            
            /* Window styles */
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            /* Button styles */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
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
            
            /* Input styles */
            QLineEdit, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                color: #212529;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
            
            /* Card styles */
            QFrame[class="card"] {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 16px;
            }
            
            /* Progress bar styles */
            QProgressBar {
                background-color: #e9ecef;
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 4px;
            }
            
            /* Status colors */
            .success {
                color: #28a745;
            }
            
            .warning {
                color: #ffc107;
            }
            
            .danger {
                color: #dc3545;
            }
            
            /* File browser styles */
            QTreeView {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 4px;
            }
            
            QTreeView::item {
                padding: 4px;
            }
            
            QTreeView::item:hover {
                background-color: #f8f9fa;
            }
            
            QTreeView::item:selected {
                background-color: #007bff;
                color: white;
            }
            
            QComboBox {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 4px;
                min-width: 120px;
            }
        """
        
    @staticmethod
    def get_dark_theme() -> str:
        """Get dark theme stylesheet.
        
        Returns:
            CSS stylesheet as string
        """
        return """
            QWidget {
                background-color: #212529;
                color: #f8f9fa;
            }
            
            QMainWindow {
                background-color: #343a40;
            }
            
            QPushButton {
                background-color: #6c757d;
            }
            
            QPushButton:hover {
                background-color: #5a6268;
            }
            
            QPushButton:pressed {
                background-color: #4e555b;
            }
            
            QLineEdit, QTextEdit {
                background-color: #343a40;
                border-color: #495057;
                color: #f8f9fa;
            }
        """