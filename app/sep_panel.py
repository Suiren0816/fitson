from __future__ import annotations

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


class SEPParamsPanel(QWidget):
    """SEP parameter configuration panel skeleton."""

    params_changed = pyqtSignal(object)

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._params: Any = None

    def current_params(self) -> Any:
        """Return the current SEP parameter object."""

        return self._params

    def load_params(self, params: Any) -> None:
        """Load a parameter object into the panel."""

        self._params = params

    def reset_defaults(self) -> None:
        """Reset all controls to the default SEP parameters."""

        pass
