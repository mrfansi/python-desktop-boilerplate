"""Error handling decorators and utilities."""

import functools
import logging
from typing import Callable, Any

def handle_errors(func: Callable) -> Callable:
    """Decorator to handle and log errors in service methods.
    
    Args:
        func: Function to wrap with error handling
        
    Returns:
        Wrapped function with error handling
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(
                f"Error in {func.__name__}: {str(e)}",
                exc_info=True
            )
            raise  # Re-raise after logging
            
    return wrapper