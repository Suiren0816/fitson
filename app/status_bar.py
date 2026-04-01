from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import QStatusBar


class AppStatusBar(QStatusBar):
    """Status-bar skeleton for cursor, WCS, and zoom information."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def set_pixel_info(self, x: int | None, y: int | None, value: float | None) -> None:
        """Update pixel coordinate and value text."""

        pass

    def set_world_info(self, ra: str | None, dec: str | None) -> None:
        """Update RA/Dec display text."""

        pass

    def set_zoom_info(self, zoom_factor: float | None) -> None:
        """Update the zoom display text."""

        pass

    def clear_data(self) -> None:
        """Reset all displayed status values."""

        pass
