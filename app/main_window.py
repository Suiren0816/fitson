from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Top-level application window skeleton."""

    def __init__(self, initial_path: str | None = None, initial_hdu: int | None = None) -> None:
        super().__init__()
        self.initial_path = initial_path
        self.initial_hdu = initial_hdu

        self.canvas: Any = None
        self.source_table_dock: Any = None
        self.sep_panel: Any = None
        self.header_dialog: Any = None
        self.app_status_bar: Any = None

        self.fits_service: Any = None
        self.sep_service: Any = None
        self.current_catalog: Any = None

    def build_ui(self) -> None:
        """Create menus, toolbars, central widgets, and docks."""

        pass

    def create_actions(self) -> None:
        """Create all window actions and shortcuts."""

        pass

    def connect_signals(self) -> None:
        """Connect UI signals to the window controller methods."""

        pass

    def open_file(self, path: str | None = None, hdu_index: int | None = None) -> None:
        """Open a FITS file and load the selected HDU."""

        pass

    def close_current_file(self) -> None:
        """Close the current FITS file and reset the window state."""

        pass

    def refresh_image(self) -> None:
        """Re-render and refresh the central image view."""

        pass

    def export_catalog(self) -> None:
        """Export the current source catalog to CSV."""

        pass

    def show_header_dialog(self) -> None:
        """Open the FITS header viewer."""

        pass

    def handle_roi_selected(self, x0: int, y0: int, width: int, height: int) -> None:
        """Handle ROI selection from the canvas and trigger SEP extraction."""

        pass

    def handle_source_clicked(self, index: int) -> None:
        """Handle source-table row selection and synchronize the canvas."""

        pass

    def update_status_from_cursor(self, x: float, y: float) -> None:
        """Update status-bar information from the current cursor position."""

        pass

    def show_error(self, title: str, detail: str) -> None:
        """Show an error message to the user."""

        pass
