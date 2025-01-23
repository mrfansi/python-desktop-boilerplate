"""Tests for main application functionality."""
import pytest
import json
from PySide6.QtWidgets import QApplication
from main import main
from infrastructure.config.config import Config

def test_main_initialization(qt_application, monkeypatch):
    """Test main application initialization."""
    # Patch config path to use test config
    test_config = {
        "app": {
            "name": "Test App",
            "version": "1.0.0"
        },
        "logging": {
            "level": "INFO"
        }
    }
    
    # Create temporary config file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as tmp:
        json.dump(test_config, tmp)
        tmp.flush()
        
        # Patch config path
        monkeypatch.setattr('infrastructure.config.config.CONFIG_PATH', tmp.name)
        
        # Test main window creation
        from main import main
        try:
            with pytest.raises(SystemExit):
                main()
        finally:
            # Clean up QApplication
            app = QApplication.instance()
            if app:
                app.quit()
                del app

def test_main_with_invalid_config(tmp_path, monkeypatch):
    """Test main application with invalid configuration."""
    # Create invalid config file
    bad_config = tmp_path / "bad_config.json"
    bad_config.write_text("{invalid json}")
    
    # Patch config path
    monkeypatch.setattr('infrastructure.config.config.CONFIG_PATH', str(bad_config))
    
    from main import main
    try:
        with pytest.raises((json.JSONDecodeError, SystemExit)):
            main()
    finally:
        # Clean up QApplication
        app = QApplication.instance()
        if app:
            app.quit()
            del app

def test_main_with_missing_config(tmp_path, monkeypatch):
    """Test main application with missing configuration."""
    # Create path to non-existent file
    non_existent_path = tmp_path / "nonexistent.json"
    
    # Patch config path
    monkeypatch.setattr('infrastructure.config.config.CONFIG_PATH', str(non_existent_path))
    
    from main import main
    try:
        with pytest.raises(SystemExit):
            main()
    finally:
        # Clean up QApplication
        app = QApplication.instance()
        if app:
            app.quit()
            del app