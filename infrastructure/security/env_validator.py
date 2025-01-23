"""Environment variable validation and management."""

import os
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class EnvironmentConfig:
    """Validated environment configuration."""
    app_name: str
    app_version: str
    debug_mode: bool
    secret_key: str
    database_url: Optional[str] = None

class EnvironmentValidator:
    """Validate and load environment variables."""
    
    REQUIRED_VARS = {
        'APP_NAME': str,
        'APP_VERSION': str,
        'SECRET_KEY': str,
    }
    
    OPTIONAL_VARS = {
        'DEBUG_MODE': bool,
        'DATABASE_URL': str,
    }
    
    @classmethod
    def validate(cls) -> EnvironmentConfig:
        """Validate environment variables and return configuration."""
        missing = [var for var in cls.REQUIRED_VARS if var not in os.environ]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
            
        return EnvironmentConfig(
            app_name=os.environ['APP_NAME'],
            app_version=os.environ['APP_VERSION'],
            secret_key=os.environ['SECRET_KEY'],
            debug_mode=cls._parse_bool(os.environ.get('DEBUG_MODE', 'false')),
            database_url=os.environ.get('DATABASE_URL')
        )
    
    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Parse string boolean values."""
        return value.lower() in ('true', '1', 't', 'y', 'yes')