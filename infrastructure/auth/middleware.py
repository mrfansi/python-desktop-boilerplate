from PySide6.QtCore import QObject, Signal
from typing import Optional
from .models import Permission, has_permission

class AuthManager(QObject):
    """Qt-based authentication and authorization manager"""
    
    authentication_changed = Signal(bool)  # Emits when auth state changes
    permission_changed = Signal(str, bool)  # Emits when permissions change (permission_name, has_permission)
    
    def __init__(self, get_roles_for_user: callable, parent=None):
        super().__init__(parent)
        self.get_roles_for_user = get_roles_for_user
        self._current_user = None
        
    def login(self, user_id: str):
        """Set current authenticated user"""
        self._current_user = user_id
        self.authentication_changed.emit(True)
        self._emit_permission_changes()
        
    def logout(self):
        """Clear current authenticated user"""
        self._current_user = None
        self.authentication_changed.emit(False)
        self._emit_permission_changes()
        
    def check_permission(self, permission: Permission) -> bool:
        """Check if current user has specified permission"""
        if not self._current_user:
            return False
        roles = self.get_roles_for_user(self._current_user)
        return has_permission(roles, permission)
        
    def _emit_permission_changes(self):
        """Emit signals for all permission changes"""
        for permission in Permission:
            has_perm = self.check_permission(permission)
            self.permission_changed.emit(permission.value, has_perm)