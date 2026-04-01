from __future__ import annotations

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDockWidget


class SourceTableDock(QDockWidget):
    """Dockable source-table skeleton."""

    source_clicked = pyqtSignal(int)

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.catalog: Any = None

    def populate(self, catalog: Any) -> None:
        """Populate the table from a source catalog."""

        self.catalog = catalog

    def clear_catalog(self) -> None:
        """Clear the table contents and associated catalog."""

        self.catalog = None

    def select_source(self, index: int) -> None:
        """Select a source row programmatically."""

        pass
