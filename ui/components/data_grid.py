"""Reusable data grid component for tabular data display."""

from typing import Any, Dict, List, Optional
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal, QSortFilterProxyModel, QPoint
from PySide6.QtWidgets import (
    QTableView, QHeaderView, QWidget, QVBoxLayout, QHBoxLayout, 
    QToolButton, QLabel, QLineEdit
)
from ui.themes.theme_engine import ThemeEngine
from ui.components.base_themed_widget import ThemedWidget
from ui.components.button import StyledButton

class DataGridModel(QAbstractTableModel):
    """Custom table model for efficient data handling."""
    
    def __init__(self, data: List[Dict], columns: List[Dict], parent=None):
        super().__init__(parent)
        self._data = data
        self._columns = columns
        self._theme_engine = ThemeEngine.get_instance()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._columns)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
            
        col_config = self._columns[index.column()]
        item = self._data[index.row()].get(col_config["key"], "")
        
        if role == Qt.DisplayRole:
            formatter = col_config.get("formatter")
            return formatter(item) if formatter else str(item)
        elif role == Qt.TextAlignmentRole:
            return col_config.get("align", Qt.AlignLeft | Qt.AlignVCenter)
        elif role == Qt.ForegroundRole:
            return self._theme_engine.get_color("text")
        elif role == Qt.BackgroundRole:
            return self._theme_engine.get_color(
                "alternate_bg" if index.row() % 2 else "background"
            )
            
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section]["title"]
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder):
        """Sort data by column."""
        self.layoutAboutToBeChanged.emit()
        col_key = self._columns[column]["key"]
        reverse = order == Qt.DescendingOrder
        self._data.sort(
            key=lambda x: str(x.get(col_key, "")),
            reverse=reverse
        )
        self.layoutChanged.emit()

class FilterBar(ThemedWidget):
    """Search/filter bar for DataGrid."""
    
    filter_changed = Signal(str)
    
    def __init__(self, parent=None):
        # Create widgets before theme initialization
        self.search_input = QLineEdit()
        self.clear_btn = StyledButton("Clear")
        
        # Initialize themed widget
        super().__init__(parent, component_type="filter_bar")
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 8)
        
        # Configure search input
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.filter_changed)
        
        # Configure clear button
        self.clear_btn.set_secondary()
        self.clear_btn.clicked.connect(self._clear_filter)
        
        layout.addWidget(self.search_input)
        layout.addWidget(self.clear_btn)
        self.setLayout(layout)
        
    def _clear_filter(self):
        """Clear search input."""
        self.search_input.clear()

    def _apply_theme(self, theme_data: Dict):
        """Apply theme to filter bar."""
        if not hasattr(self, 'search_input'):
            return
            
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {theme_data.get("input_bg", "#ffffff")};
                color: {theme_data.get("text", "#212529")};
                border: 1px solid {theme_data.get("border", "#ced4da")};
                border-radius: 4px;
                padding: 6px 12px;
            }}
        """)

class DataGrid(ThemedWidget):
    """Theme-aware data grid component with sorting and filtering."""
    
    row_selected = Signal(dict)  # Emits selected row data
    row_double_clicked = Signal(dict)  # Emits double-clicked row data
    column_sorted = Signal(str, Qt.SortOrder)  # Emits (column_key, order)
    
    def __init__(self, parent=None):
        # Create components before theme initialization
        self._table_view = QTableView()
        self._proxy_model = QSortFilterProxyModel()
        self._model = DataGridModel([], [], None)
        self._filter_bar = FilterBar()
        
        # Initialize themed widget
        super().__init__(parent, component_type="data_grid")
        
        self._data: List[Dict] = []
        self._columns: List[Dict] = []
        
        self._init_ui()
        self._connect_signals()
        
    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add filter bar
        layout.addWidget(self._filter_bar)
        
        # Configure table view
        self._table_view.setModel(self._proxy_model)
        self._proxy_model.setSourceModel(self._model)
        
        header = self._table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        
        self._table_view.verticalHeader().hide()
        self._table_view.setSelectionBehavior(QTableView.SelectRows)
        self._table_view.setSelectionMode(QTableView.SingleSelection)
        self._table_view.setAlternatingRowColors(True)
        self._table_view.setSortingEnabled(True)
        
        layout.addWidget(self._table_view)
        self.setLayout(layout)
        
    def _connect_signals(self):
        """Connect internal signals."""
        self._table_view.doubleClicked.connect(self._handle_double_click)
        self._table_view.clicked.connect(self._handle_click)
        self._filter_bar.filter_changed.connect(self._handle_filter)
        
    def _handle_click(self, index: QModelIndex):
        """Handle row selection."""
        source_index = self._proxy_model.mapToSource(index)
        row = source_index.row()
        if 0 <= row < len(self._data):
            # Get the actual row data
            data = dict(self._data[row])
            self.row_selected.emit(data)
        
    def _handle_double_click(self, index: QModelIndex):
        """Handle row double click."""
        source_index = self._proxy_model.mapToSource(index)
        row = source_index.row()
        if 0 <= row < len(self._data):
            # Get the actual row data
            data = dict(self._data[row])
            self.row_double_clicked.emit(data)
        
    def _handle_filter(self, text: str):
        """Apply filter to proxy model."""
        self._proxy_model.setFilterFixedString(text)
        
    def load_data(self, data: List[Dict], columns: List[Dict]):
        """Load data into the grid."""
        self._data = list(data)  # Create a copy to prevent external modification
        self._columns = list(columns)  # Create a copy to prevent external modification
        self._model = DataGridModel(self._data, self._columns, self)
        self._proxy_model.setSourceModel(self._model)
        self._update_columns()
        
    def _update_columns(self):
        """Update column headers and sizing."""
        header = self._table_view.horizontalHeader()
        for i, col in enumerate(self._columns):
            # Set width if specified
            if "width" in col:
                header.resizeSection(i, col["width"])
            # Set resize mode
            mode = QHeaderView.ResizeToContents if col.get("auto_size") else QHeaderView.Interactive
            header.setSectionResizeMode(i, mode)
            
    def set_filter_columns(self, columns: List[str]):
        """Set which columns are searchable."""
        def filter_func(source_row: int, source_parent: QModelIndex) -> bool:
            filter_text = self._proxy_model.filterRegExp().pattern().lower()
            if not filter_text:
                return True
                
            # Check each filterable column
            for col_key in columns:
                col_idx = next(
                    (i for i, c in enumerate(self._columns) if c["key"] == col_key),
                    None
                )
                if col_idx is not None:
                    value = str(self._model.data(
                        self._model.index(source_row, col_idx),
                        Qt.DisplayRole
                    )).lower()
                    if filter_text in value:
                        return True
            return False
            
        self._proxy_model.setFilterKeyColumn(-1)  # Search all columns
        self._proxy_model.setFilterRole(Qt.DisplayRole)
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self._proxy_model.setFilterFixedString("")
        
    def refresh(self):
        """Force refresh of the grid."""
        self._model.layoutChanged.emit()

    def _apply_theme(self, theme_data: Dict):
        """Apply theme styles to the grid."""
        if not hasattr(self, '_table_view'):
            return
            
        style = f"""
            QTableView {{
                background-color: {theme_data.get("background", "#ffffff")};
                alternate-background-color: {theme_data.get("alternate_bg", "#f8f9fa")};
                gridline-color: {theme_data.get("border", "#dee2e6")};
                color: {theme_data.get("text", "#212529")};
                border: 1px solid {theme_data.get("border", "#dee2e6")};
            }}
            QHeaderView::section {{
                background-color: {theme_data.get("header_bg", "#e9ecef")};
                color: {theme_data.get("text", "#212529")};
                padding: 8px;
                border: none;
                border-right: 1px solid {theme_data.get("border", "#dee2e6")};
                border-bottom: 1px solid {theme_data.get("border", "#dee2e6")};
            }}
            QTableView::item {{
                padding: 8px;
            }}
            QTableView::item:selected {{
                background-color: {theme_data.get("primary", "#007bff")};
                color: {theme_data.get("text_light", "#ffffff")};
            }}
        """
        self._table_view.setStyleSheet(style)