from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

class Permission(Enum):
    """System permissions enumeration"""
    READ = 'read'
    WRITE = 'write'
    DELETE = 'delete'
    MANAGE_USERS = 'manage_users'
    MANAGE_ROLES = 'manage_roles'
    MANAGE_SETTINGS = 'manage_settings'

@dataclass
class Role:
    """Role model with associated permissions"""
    id: str
    name: str
    description: str
    permissions: List[Permission]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

@dataclass
class UserRole:
    """Mapping between users and roles"""
    user_id: str
    role_id: str
    assigned_at: datetime = datetime.now()

def has_permission(roles: List[Role], required_permission: Permission) -> bool:
    """Check if any role has the required permission"""
    return any(
        required_permission in role.permissions
        for role in roles
    )

def get_role_by_name(roles: List[Role], name: str) -> Optional[Role]:
    """Get role by name from list of roles"""
    return next((role for role in roles if role.name == name), None)