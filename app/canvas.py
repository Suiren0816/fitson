from __future__ import annotations

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QGraphicsView


class ImageCanvas(QGraphicsView):
    """Image display and interaction skeleton."""

    mouse_moved = pyqtSignal(float, float)
    roi_selected = pyqtSignal(int, int, int, int)
    zoom_changed = pyqtSignal(float)

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.current_image: QImage | None = None
        self.current_catalog: Any = None

    def set_image(self, image: QImage | None) -> None:
        """Set the current image shown on the canvas."""

        self.current_image = image

    def clear_image(self) -> None:
        """Clear the currently displayed image."""

        self.current_image = None

    def fit_to_window(self) -> None:
        """Scale the image to fit the current viewport."""

        pass

    def show_actual_pixels(self) -> None:
        """Reset the view to 1:1 pixel scale."""

        pass

    def zoom_in(self) -> None:
        """Zoom in from the current scale."""

        pass

    def zoom_out(self) -> None:
        """Zoom out from the current scale."""

        pass

    def draw_sources(self, catalog: Any) -> None:
        """Draw source overlays for the given catalog."""

        self.current_catalog = catalog

    def clear_sources(self) -> None:
        """Clear all source overlays."""

        self.current_catalog = None

    def highlight_source(self, index: int) -> None:
        """Highlight a single source overlay."""

        pass
