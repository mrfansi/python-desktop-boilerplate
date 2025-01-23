"""Internationalization service for the application."""

from PySide6.QtCore import QLocale, QTranslator
from PySide6.QtWidgets import QApplication
from pathlib import Path
from typing import Optional

class I18nService:
    """Handles application internationalization."""
    
    def __init__(self, app: QApplication, locale_dir: Path):
        self.app = app
        self.locale_dir = locale_dir
        self.translators = []
        
    def set_language(self, language: str) -> bool:
        """Set application language."""
        # Remove existing translators
        for translator in self.translators:
            self.app.removeTranslator(translator)
        self.translators.clear()
        
        # Load new translations
        locale = QLocale(language)
        QLocale.setDefault(locale)
        
        # Load Qt translations
        qt_translator = QTranslator()
        if qt_translator.load(locale, "qtbase", "_", str(self.locale_dir)):
            self.app.installTranslator(qt_translator)
            self.translators.append(qt_translator)
            
        # Load application translations
        app_translator = QTranslator()
        if app_translator.load(locale, "app", "_", str(self.locale_dir)):
            self.app.installTranslator(app_translator)
            self.translators.append(app_translator)
            
        return bool(self.translators)
        
    def available_languages(self) -> list[str]:
        """Get list of available languages."""
        return [f.stem.split('_')[-1] 
                for f in self.locale_dir.glob('app_*.qm')]