from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import QDialog


class HeaderDialog(QDialog):
    """FITS header viewer skeleton."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.header_text = ""
        self.filter_text = ""

    def set_header_text(self, text: str) -> None:
        """Load the raw header text into the dialog."""

        self.header_text = text

    def set_filter_text(self, text: str) -> None:
        """Update the current filter string."""

        self.filter_text = text

    def apply_filter(self) -> None:
        """Apply the current search filter to the header view."""

        pass

    def clear(self) -> None:
        """Clear dialog state."""

        self.header_text = ""
        self.filter_text = ""
