"""Hot reload functionality for development."""

import os
import sys
import logging
from pathlib import Path
from typing import Callable, Dict, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)

class HotReloader(QObject, FileSystemEventHandler):
    """Handle file system events for hot reloading."""
    
    reload_requested = Signal()  # Signal to emit when reload is needed
    
    def __init__(self):
        """Initialize the reloader."""
        super().__init__()
        self.last_reloaded: Dict[str, float] = {}
        self._cached_modules: Set[str] = set()
        self._cache_loaded_modules()
        
    def _cache_loaded_modules(self):
        """Cache initially loaded application modules."""
        base_path = Path(__file__).parent.parent
        for name, module in list(sys.modules.items()):
            if hasattr(module, '__file__') and module.__file__:
                module_path = Path(module.__file__)
                if base_path in module_path.parents:
                    self._cached_modules.add(name)
                    
    def _reload_module(self, module_name: str):
        """Reload a specific module and its dependencies.
        
        Args:
            module_name: Name of module to reload
        """
        try:
            # Reload the module
            if module_name in sys.modules:
                logger.info(f"Reloading module: {module_name}")
                import importlib
                importlib.reload(sys.modules[module_name])
                
            # Reload dependent modules
            for name in self._cached_modules:
                module = sys.modules.get(name)
                if module and hasattr(module, '__file__'):
                    try:
                        importlib.reload(module)
                    except Exception as e:
                        if "spec not found" not in str(e):  # Ignore __main__ module
                            logger.error(f"Error reloading dependent module {name}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error reloading {module_name}: {str(e)}")
            
    def on_modified(self, event):
        """Handle file modification events.
        
        Args:
            event: File system event
        """
        if not isinstance(event, FileModifiedEvent):
            return
            
        if not event.src_path.endswith('.py'):
            return
            
        # Convert path to module name
        file_path = Path(event.src_path).resolve()
        base_path = Path(__file__).parent.parent
        
        if base_path not in file_path.parents:
            return
            
        rel_path = file_path.relative_to(base_path)
        module_name = '.'.join(rel_path.with_suffix('').parts)
        
        # Avoid reloading too frequently
        current_time = event.time_stamp if hasattr(event, 'time_stamp') else os.path.getmtime(event.src_path)
        last_time = self.last_reloaded.get(module_name, 0)
        if current_time - last_time < 1.0:  # Debounce reloads
            return
            
        self.last_reloaded[module_name] = current_time
        
        # Perform reload
        self._reload_module(module_name)
        
        # Emit signal to trigger UI update on main thread
        self.reload_requested.emit()

def start_hot_reload(callback: Callable[[], None] = None) -> Observer:
    """Start the hot reload observer.
    
    Args:
        callback: Optional callback function to execute after modules are reloaded.
                 The callback takes no arguments and returns nothing.
        
    Returns:
        The file system observer
    """
    base_path = Path(__file__).parent.parent
    
    # Setup reloader
    reloader = HotReloader()
    if callback:
        reloader.reload_requested.connect(callback)
    
    # Setup observer
    observer = Observer()
    observer.schedule(reloader, str(base_path), recursive=True)
    
    # Start watching
    observer.start()
    logger.info("Hot reload observer started")
    return observer