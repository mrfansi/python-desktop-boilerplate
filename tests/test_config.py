"""Tests for configuration handling."""
import pytest
from infrastructure.config.config import Config

def test_config_loading():
    """Test loading configuration from config.json."""
    config = Config()
    
    # Test basic configuration
    assert 'app' in config
    assert config.get('app.name') is not None
    assert config.get('app.version') is not None
    
    # Test contains method for top-level keys
    assert 'app' in config
    assert 'logging' in config
    assert 'nonexistent' not in config

def test_config_missing_file(tmp_path):
    """Test handling of missing config file."""
    non_existent_path = tmp_path / "nonexistent.json"
    config = Config(config_path=str(non_existent_path))
    
    # Verify default config was created
    assert non_existent_path.exists()
    assert 'app' in config
    assert config.get('app.name') == "Python Desktop App"

def test_config_invalid_json(tmp_path):
    """Test handling of invalid JSON in config file."""
    bad_config = tmp_path / "bad_config.json"
    bad_config.write_text("{invalid json}")
    
    with pytest.raises(ValueError):
        Config(config_path=str(bad_config))

def test_config_get_with_default():
    """Test Config.get() with default values."""
    config = Config()
    
    # Test existing key
    assert config.get('app.name') is not None
    
    # Test non-existent key with default
    assert config.get('nonexistent.key', 'default') == 'default'