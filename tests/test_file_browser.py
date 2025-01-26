"""Test file browser dialog component."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMessageBox, QFileDialog, QDialogButtonBox
from ui.components.file_browser import FileBrowserDialog
from ui.themes.theme_engine import ThemeEngine

def test_file_browser_creation(qtbot):
    """Test file browser creation and theming."""
    dialog = FileBrowserDialog()
    qtbot.addWidget(dialog)
    
    assert hasattr(dialog, 'file_list')
    assert hasattr(dialog, 'add_btn')
    assert hasattr(dialog, 'clear_btn')
    assert hasattr(dialog, 'button_box')
    
    # Verify initial theme is applied
    assert dialog.styleSheet() != ""
    assert "QListWidget" in dialog.styleSheet()
    assert "QDialogButtonBox" in dialog.styleSheet()
    assert "background-color" in dialog.styleSheet()

def test_theme_changes(qtbot):
    """Test theme updates."""
    engine = ThemeEngine.get_instance()
    dialog = FileBrowserDialog()
    qtbot.addWidget(dialog)
    dialog.show()
    QTest.qWait(100)
    
    # Get initial styles
    initial_style = dialog.styleSheet()
    
    # Change theme
    engine.switch_theme("dark")
    QTest.qWait(100)
    
    # Verify styles updated
    assert dialog.styleSheet() != initial_style
    assert "#2c3034" in dialog.styleSheet()  # Dark theme background for list
    assert "#212529" in dialog.styleSheet()  # Dark theme dialog background

def test_file_selection(qtbot, monkeypatch):
    """Test file selection functionality with theming."""
    # Mock file dialog
    mock_files = ["/path/to/file1.txt", "/path/to/file2.txt"]
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda *args, **kwargs: (mock_files, "")
    )
    
    dialog = FileBrowserDialog(allowed_extensions=['.txt'])
    qtbot.addWidget(dialog)
    dialog.show()
    QTest.qWait(100)
    
    # Click add files button
    qtbot.mouseClick(dialog.add_btn, Qt.LeftButton)
    QTest.qWait(100)
    
    # Verify files added
    assert dialog.file_list.count() == 2
    assert dialog.get_selected_files() == mock_files

def test_clear_selection(qtbot, monkeypatch):
    """Test clearing selection with theming."""
    # Mock file dialog
    mock_files = ["/path/to/file1.txt", "/path/to/file2.txt"]
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda *args, **kwargs: (mock_files, "")
    )
    
    dialog = FileBrowserDialog()
    qtbot.addWidget(dialog)
    dialog.show()
    QTest.qWait(100)
    
    # Add files
    qtbot.mouseClick(dialog.add_btn, Qt.LeftButton)
    QTest.qWait(100)
    assert dialog.file_list.count() == 2
    
    # Clear selection
    qtbot.mouseClick(dialog.clear_btn, Qt.LeftButton)
    QTest.qWait(100)
    assert dialog.file_list.count() == 0

def test_invalid_extensions(qtbot, monkeypatch):
    """Test invalid file extension handling."""
    # Mock file dialog
    mock_files = ["/path/to/file1.txt", "/path/to/file2.pdf"]
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda *args, **kwargs: (mock_files, "")
    )
    
    # Track warning calls
    warning_shown = False
    def mock_warning(*args, **kwargs):
        nonlocal warning_shown
        warning_shown = True
    monkeypatch.setattr(QMessageBox, "warning", mock_warning)
    
    dialog = FileBrowserDialog(allowed_extensions=['.txt'])
    qtbot.addWidget(dialog)
    dialog.show()
    QTest.qWait(100)
    
    # Add files
    qtbot.mouseClick(dialog.add_btn, Qt.LeftButton)
    QTest.qWait(100)
    
    # Verify only valid files added
    assert dialog.file_list.count() == 1
    assert dialog.get_selected_files() == ["/path/to/file1.txt"]
    
    # Verify warning shown
    assert warning_shown

def test_dialog_buttons(qtbot):
    """Test dialog buttons with theming."""
    selected_files = []
    
    dialog = FileBrowserDialog()
    qtbot.addWidget(dialog)
    dialog.show()
    QTest.qWait(100)
    
    # Connect to signal
    def handle_files(files):
        nonlocal selected_files
        selected_files = files
    dialog.files_selected.connect(handle_files)
    
    # Add a file
    dialog.file_list.addItem("/path/to/file.txt")
    
    # Click OK button
    ok_button = dialog.button_box.button(QDialogButtonBox.StandardButton.Ok)
    qtbot.mouseClick(ok_button, Qt.LeftButton)
    QTest.qWait(100)
    
    # Verify signal emitted
    assert selected_files == ["/path/to/file.txt"]
    assert dialog.file_list.count() == 0

    # Test Cancel button
    dialog.file_list.addItem("/path/to/file2.txt")
    cancel_button = dialog.button_box.button(QDialogButtonBox.StandardButton.Cancel)
    qtbot.mouseClick(cancel_button, Qt.LeftButton)
    QTest.qWait(100)
    
    # Verify list cleared but signal not emitted again
    assert dialog.file_list.count() == 0
    assert selected_files == ["/path/to/file.txt"]  # Unchanged