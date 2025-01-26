"""Theme configuration and color palettes."""

from typing import Dict, Any

LIGHT_THEME = {
    # Colors
    "primary": "#007bff",
    "primary_hover": "#0069d9",
    "primary_pressed": "#0056b3",
    "secondary": "#6c757d",
    "secondary_hover": "#5a6268",
    "secondary_pressed": "#4e555b",
    "success": "#28a745",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
    "background": "#ffffff",
    "surface": "#f8f9fa",
    "border": "#ced4da",
    "text": {
        "primary": "#212529",
        "secondary": "#6c757d",
        "disabled": "#868e96"
    },
    
    # Component specific
    "input": {
        "background": "#ffffff",
        "border": "#ced4da",
        "focus_border": "#80bdff",
        "disabled_bg": "#e9ecef",
        "placeholder": "#6c757d"
    },
    "button": {
        "primary_bg": "#007bff",
        "primary_text": "#ffffff",
        "secondary_bg": "#6c757d",
        "secondary_text": "#ffffff",
        "disabled_bg": "#e9ecef",
        "disabled_text": "#6c757d"
    },
    "checkbox": {
        "background": "#ffffff",
        "border": "#ced4da",
        "checked_bg": "#007bff",
        "checked_border": "#007bff",
        "disabled_bg": "#e9ecef",
        "disabled_border": "#dee2e6",
        "text": "#212529"
    },
    "file_browser": {
        "list_bg": "#ffffff",
        "list_border": "#ced4da",
        "item_hover": "#e9ecef",
        "item_selected": "#007bff",
        "item_selected_text": "#ffffff",
        "dialog_bg": "#ffffff",
        "dialog_border": "#ced4da",
        "button_text": "#ffffff"
    }
}

DARK_THEME = {
    # Colors
    "primary": "#0d6efd",
    "primary_hover": "#0b5ed7",
    "primary_pressed": "#0a58ca",
    "secondary": "#6c757d",
    "secondary_hover": "#5c636a",
    "secondary_pressed": "#565e64",
    "success": "#198754",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#0dcaf0",
    "background": "#212529",
    "surface": "#2c3034",
    "border": "#495057",
    "text": {
        "primary": "#f8f9fa",
        "secondary": "#adb5bd",
        "disabled": "#6c757d"
    },
    
    # Component specific
    "input": {
        "background": "#2c3034",
        "border": "#495057",
        "focus_border": "#0d6efd",
        "disabled_bg": "#343a40",
        "placeholder": "#6c757d"
    },
    "button": {
        "primary_bg": "#0d6efd",
        "primary_text": "#ffffff",
        "secondary_bg": "#6c757d",
        "secondary_text": "#ffffff",
        "disabled_bg": "#343a40",
        "disabled_text": "#6c757d"
    },
    "checkbox": {
        "background": "#2c3034",
        "border": "#495057",
        "checked_bg": "#0d6efd",
        "checked_border": "#0d6efd",
        "disabled_bg": "#343a40",
        "disabled_border": "#495057",
        "text": "#f8f9fa"
    },
    "file_browser": {
        "list_bg": "#2c3034",
        "list_border": "#495057",
        "item_hover": "#343a40",
        "item_selected": "#0d6efd",
        "item_selected_text": "#ffffff",
        "dialog_bg": "#212529",
        "dialog_border": "#495057",
        "button_text": "#ffffff"
    }
}

def get_component_styles(theme: Dict[str, Any], component: str) -> str:
    """Get styles for a specific component based on theme.
    
    Args:
        theme: Theme configuration dictionary
        component: Component name to get styles for
        
    Returns:
        str: Component styles as CSS string
    """
    if component == "input":
        return f"""
            QLineEdit {{
                background-color: {theme["input"]["background"]};
                border: 1px solid {theme["input"]["border"]};
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                color: {theme["text"]["primary"]};
            }}
            QLineEdit:focus {{
                border-color: {theme["input"]["focus_border"]};
            }}
            QLineEdit:disabled {{
                background-color: {theme["input"]["disabled_bg"]};
                color: {theme["text"]["disabled"]};
            }}
            QLineEdit::placeholder {{
                color: {theme["input"]["placeholder"]};
            }}
        """
    elif component == "button":
        return f"""
            QPushButton {{
                background-color: {theme["button"]["primary_bg"]};
                color: {theme["button"]["primary_text"]};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {theme["primary_hover"]};
            }}
            QPushButton:pressed {{
                background-color: {theme["primary_pressed"]};
            }}
            QPushButton:disabled {{
                background-color: {theme["button"]["disabled_bg"]};
                color: {theme["button"]["disabled_text"]};
            }}
        """
    elif component == "file_browser":
        return f"""
            QDialog {{
                background-color: {theme["file_browser"]["dialog_bg"]};
                color: {theme["text"]["primary"]};
                border: 1px solid {theme["file_browser"]["dialog_border"]};
            }}
            QListWidget {{
                background-color: {theme["file_browser"]["list_bg"]};
                color: {theme["text"]["primary"]};
                border: 1px solid {theme["file_browser"]["list_border"]};
                border-radius: 4px;
            }}
            QListWidget::item {{
                padding: 8px;
            }}
            QListWidget::item:hover {{
                background-color: {theme["file_browser"]["item_hover"]};
            }}
            QListWidget::item:selected {{
                background-color: {theme["file_browser"]["item_selected"]};
                color: {theme["file_browser"]["item_selected_text"]};
            }}
            QDialogButtonBox QPushButton {{
                background-color: {theme["button"]["primary_bg"]};
                color: {theme["file_browser"]["button_text"]};
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }}
            QDialogButtonBox QPushButton:hover {{
                background-color: {theme["primary_hover"]};
            }}
            QDialogButtonBox QPushButton[text="Cancel"] {{
                background-color: {theme["button"]["secondary_bg"]};
            }}
            QDialogButtonBox QPushButton[text="Cancel"]:hover {{
                background-color: {theme["secondary_hover"]};
            }}
        """
    
    return ""