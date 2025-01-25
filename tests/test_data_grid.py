"""Test data grid component."""

import pytest
from PySide6.QtCore import Qt, QModelIndex, QPoint
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QHeaderView
from ui.components.data_grid import DataGrid, DataGridModel
from ui.themes.theme_engine import ThemeEngine

@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35}
    ]

@pytest.fixture
def sample_columns():
    """Sample column configuration."""
    return [
        {"key": "id", "title": "ID", "width": 50},
        {"key": "name", "title": "Name", "width": 100},
        {"key": "age", "title": "Age", "width": 70}
    ]

def test_data_grid_creation(qtbot):
    """Test basic grid creation."""
    grid = DataGrid()
    qtbot.addWidget(grid)
    
    assert grid._table_view is not None
    assert grid._filter_bar is not None
    assert isinstance(grid._model, DataGridModel)

def test_data_loading(qtbot, sample_data, sample_columns):
    """Test loading data into grid."""
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)
    
    grid.load_data(sample_data, sample_columns)
    
    # Verify model data
    assert grid._model.rowCount() == len(sample_data)
    assert grid._model.columnCount() == len(sample_columns)
    
    # Verify displayed data
    name_col = next(i for i, c in enumerate(sample_columns) if c["key"] == "name")
    name_index = grid._model.index(0, name_col)
    assert grid._model.data(name_index, Qt.DisplayRole) == "Alice"

def test_sorting(qtbot, sample_data, sample_columns):
    """Test column sorting."""
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)
    
    grid.load_data(sample_data, sample_columns)
    
    # Get name column index
    name_col = next(i for i, c in enumerate(sample_columns) if c["key"] == "name")
    
    # Get header and click position
    header = grid._table_view.horizontalHeader()
    section_pos = header.sectionPosition(name_col)
    section_size = header.sectionSize(name_col)
    click_point = QPoint(section_pos + section_size // 2, header.height() // 2)
    
    # Click header to sort
    qtbot.mouseClick(header.viewport(), Qt.LeftButton, pos=click_point)
    QTest.qWait(100)
    
    # Verify sort
    first_row_index = grid._proxy_model.index(0, name_col)
    source_index = grid._proxy_model.mapToSource(first_row_index)
    first_name = grid._model.data(source_index, Qt.DisplayRole)
    assert first_name == "Alice"  # Alphabetically first

def test_filtering(qtbot, sample_data, sample_columns):
    """Test grid filtering."""
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)
    
    grid.load_data(sample_data, sample_columns)
    grid.set_filter_columns(["name"])
    
    # Enter search text
    qtbot.keyClicks(grid._filter_bar.search_input, "bob")
    QTest.qWait(100)
    
    # Verify filtered results
    visible_rows = grid._proxy_model.rowCount()
    assert visible_rows == 1  # Only Bob should be visible
    
    name_col = next(i for i, c in enumerate(sample_columns) if c["key"] == "name")
    visible_name = grid._proxy_model.data(grid._proxy_model.index(0, name_col), Qt.DisplayRole)
    assert visible_name == "Bob"

def test_row_selection(qtbot, sample_data, sample_columns):
    """Test row selection events."""
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)

    grid.load_data(sample_data, sample_columns)
    
    # Ensure no sorting is applied
    grid._proxy_model.sort(-1)  # Reset sorting
    QTest.qWait(100)

    # Track selection
    selected_data = None
    def handle_select(data):
        nonlocal selected_data
        selected_data = data
    grid.row_selected.connect(handle_select)

    # Click first row
    first_cell = grid._proxy_model.index(0, 0)
    cell_rect = grid._table_view.visualRect(first_cell)
    qtbot.mouseClick(
        grid._table_view.viewport(),
        Qt.LeftButton,
        pos=cell_rect.center()
    )
    QTest.qWait(100)

    assert selected_data is not None
    assert selected_data["name"] == "Alice"

def test_theme_integration(qtbot, sample_data, sample_columns):
    """Test theme changes."""
    engine = ThemeEngine.get_instance()
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)
    
    grid.load_data(sample_data, sample_columns)
    
    # Get initial style
    initial_style = grid._table_view.styleSheet()
    
    # Switch theme
    engine.switch_theme("dark")
    QTest.qWait(100)
    
    # Verify style updated
    assert grid._table_view.styleSheet() != initial_style
    assert "#212529" in grid._table_view.styleSheet()  # Dark theme background

def test_custom_formatter(qtbot):
    """Test custom cell formatting."""
    data = [{"value": 123.456}]
    columns = [{
        "key": "value",
        "title": "Value",
        "formatter": lambda x: f"${x:.2f}"
    }]
    
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)
    
    grid.load_data(data, columns)
    
    # Verify formatted value
    value_index = grid._proxy_model.index(0, 0)
    assert grid._proxy_model.data(value_index, Qt.DisplayRole) == "$123.46"

def test_clear_filter(qtbot, sample_data, sample_columns):
    """Test clearing filter."""
    grid = DataGrid()
    qtbot.addWidget(grid)
    grid.show()
    QTest.qWait(100)
    
    grid.load_data(sample_data, sample_columns)
    grid.set_filter_columns(["name"])
    
    # Add filter
    qtbot.keyClicks(grid._filter_bar.search_input, "bob")
    QTest.qWait(100)
    
    # Clear filter
    qtbot.mouseClick(grid._filter_bar.clear_btn, Qt.LeftButton)
    QTest.qWait(100)
    
    # Verify all rows visible
    assert grid._proxy_model.rowCount() == len(sample_data)
    assert grid._filter_bar.search_input.text() == ""