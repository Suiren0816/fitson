from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .source_catalog import SourceCatalog


@dataclass(slots=True)
class SEPParameters:
    """User-facing SEP parameters for Phase 1."""

    thresh: float = 3.0
    minarea: int = 5
    deblend_nthresh: int = 32
    deblend_cont: float = 0.005
    clean: bool = True
    clean_param: float = 1.0


class SEPService:
    """SEP extraction service skeleton."""

    def __init__(self) -> None:
        self.params = SEPParameters()

    def default_params(self) -> SEPParameters:
        """Return the default parameter set."""

        return SEPParameters()

    def validate_params(self, params: SEPParameters) -> None:
        """Validate a parameter set before extraction."""

        pass

    def extract(
        self,
        data_subarray: np.ndarray,
        params: SEPParameters | None = None,
        *,
        x_offset: int = 0,
        y_offset: int = 0,
        wcs: Any = None,
    ) -> SourceCatalog:
        """Run SEP extraction on the given ROI and return a catalog."""

        return SourceCatalog()
