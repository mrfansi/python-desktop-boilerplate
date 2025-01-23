from PySide6.QtCore import Slot
from typing import Callable, Any
from .models import Permission
from .middleware import AuthManager

def init_auth_decorators(auth_manager: AuthManager):
    """Initialize Qt-based auth decorators"""
    
    def require_permission(permission: Permission):
        """Create a slot that requires specific permission"""
        def decorator(func: Callable):
            @Slot(result=bool)
            def wrapper(*args, **kwargs) -> Any:
                if not auth_manager.check_permission(permission):
                    return False
                return func(*args, **kwargs)
            return wrapper
        return decorator
        
    def require_authenticated():
        """Create a slot that requires authentication"""
        def decorator(func: Callable):
            @Slot(result=bool)
            def wrapper(*args, **kwargs) -> Any:
                if not auth_manager.is_authenticated():
                    return False
                return func(*args, **kwargs)
            return wrapper
        return decorator
        
    return {
        'require_permission': require_permission,
        'require_authenticated': require_authenticated
    }