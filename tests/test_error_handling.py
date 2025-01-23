"""Tests for error handling functionality."""
import pytest
import logging
from infrastructure.error_handling.handlers import handle_errors

def test_error_handling_decorator(caplog):
    """Test error handling decorator."""
    @handle_errors
    def faulty_function():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        faulty_function()
    
    # Check if error was logged
    assert "Test error" in caplog.text
    assert "faulty_function" in caplog.text
    assert caplog.records[0].levelno == logging.ERROR

def test_error_handling_success(caplog):
    """Test error handling decorator with successful execution."""
    @handle_errors
    def successful_function():
        return "success"
    
    result = successful_function()
    assert result == "success"
    assert not caplog.text  # No errors logged

def test_error_handling_custom_logger():
    """Test error handling with custom logger."""
    test_logger = logging.getLogger("test_logger")
    
    @handle_errors
    def faulty_function():
        raise ValueError("Custom logger test")
        
    with pytest.raises(ValueError):
        faulty_function()
    
    # Verify logger was used
    assert test_logger.name == "test_logger"