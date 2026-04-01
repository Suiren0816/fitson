from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(slots=True)
class HDUInfo:
    """Metadata for a selectable image HDU."""

    index: int
    name: str
    dimensions: tuple[int, ...] = ()
    dtype_name: str = ""


@dataclass(slots=True)
class FITSData:
    """Container for the current FITS image, header, and WCS state."""

    path: str | None = None
    hdu_index: int | None = None
    data: np.ndarray | None = None
    header: Any = None
    wcs: Any = None
    has_wcs: bool = False
    invalid_pixels: bool = False
    available_hdus: list[HDUInfo] = field(default_factory=list)

    @classmethod
    def load(cls, path: str, hdu_index: int | None = None) -> "FITSData":
        """Load FITS data from disk into the container."""

        return cls(path=path, hdu_index=hdu_index)

    def get_data(self) -> np.ndarray | None:
        """Return the current image array."""

        return self.data

    def get_header(self) -> Any:
        """Return the current FITS header object."""

        return self.header

    def get_wcs(self) -> Any:
        """Return the current WCS object."""

        return self.wcs

    def pixel_to_world(self, x: float, y: float) -> Any:
        """Convert a pixel coordinate to world coordinates."""

        return None
