from __future__ import annotations

from typing import Any

import numpy as np

from .fits_data import FITSData, HDUInfo


class FITSService:
    """FITS loading and rendering service skeleton."""

    AVAILABLE_STRETCHES = ("Linear", "Log", "Asinh", "Sqrt")
    AVAILABLE_INTERVALS = ("ZScale", "MinMax", "99.5%", "99%", "98%", "95%")

    def __init__(self) -> None:
        self.current_data: FITSData | None = None
        self.current_stretch = self.AVAILABLE_STRETCHES[0]
        self.current_interval = self.AVAILABLE_INTERVALS[0]

    def list_image_hdus(self, path: str) -> list[HDUInfo]:
        """Inspect a FITS file and list image HDUs."""

        return []

    def open_file(self, path: str, hdu_index: int | None = None) -> FITSData:
        """Open a FITS file and store it as the active dataset."""

        self.current_data = FITSData.load(path, hdu_index)
        return self.current_data

    def close_file(self) -> None:
        """Release the current FITS dataset."""

        self.current_data = None

    def set_stretch(self, name: str) -> None:
        """Update the active stretch mode."""

        self.current_stretch = name

    def set_interval(self, name: str) -> None:
        """Update the active interval mode."""

        self.current_interval = name

    def render(self) -> np.ndarray | None:
        """Render the active FITS dataset to an 8-bit display array."""

        return None

    def header_text(self) -> str:
        """Return the active header as plain text."""

        return ""

    def current_wcs(self) -> Any:
        """Return the active WCS object."""

        if self.current_data is None:
            return None
        return self.current_data.get_wcs()
