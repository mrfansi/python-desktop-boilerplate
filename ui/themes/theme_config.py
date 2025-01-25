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
    
    return ""