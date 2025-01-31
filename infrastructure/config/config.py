"""Configuration management system."""

import json
from pathlib import Path
from typing import Any, Dict

# Default configuration file path
CONFIG_PATH = "config.json"

class Config:
    """Application configuration manager."""
    
    def __init__(self, config_path: str = CONFIG_PATH):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self._config = self._load_config()
        
    def __contains__(self, key: str) -> bool:
        """Check if key exists in configuration."""
        if '.' in key:
            # Handle nested keys
            keys = key.split('.')
            current = self._config
            try:
                for k in keys:
                    current = current[k]
                return True
            except (KeyError, TypeError):
                return False
        else:
            # Handle top-level keys
            return key in self._config
            
    def __iter__(self):
        """Iterate over configuration keys."""
        return iter(self._config)
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Dictionary containing configuration values
        """
        if not self.config_path.exists():
            return self._create_default_config()
            
        with open(self.config_path, "r") as f:
            return json.load(f)
            
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration file.
        
        Returns:
            Dictionary containing default configuration values
        """
        default_config = {
            "app": {
                "name": "Python Desktop App",
                "version": "1.0.0"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
        
        with open(self.config_path, "w") as f:
            json.dump(default_config, f, indent=4)
            
        return default_config
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key in dot notation
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

def load_config() -> Config:
    """Load application configuration.
    
    Returns:
        Config instance
    """
    return Config()