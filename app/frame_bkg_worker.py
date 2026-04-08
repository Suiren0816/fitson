from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Signal, Slot

from ..core.sep_service import SEPParameters, SEPService


class FrameBkgWorker(QObject):
    """Background worker that computes SEP background/residual for one frame."""

    bkg_ready = Signal(int, int, object, object)  # frame_index, generation, bkg, residual
    bkg_error = Signal(int, int, str)
    finished = Signal(int)

    def __init__(
        self,
        *,
        frame_index: int,
        generation: int,
        data: Any,
        sep_service: SEPService,
        params: SEPParameters,
    ) -> None:
        super().__init__()
        self.frame_index = frame_index
        self.generation = generation
        self.data = data
        self.sep_service = sep_service
        self.params = params

    @Slot()
    def run(self) -> None:
        try:
            bkg, residual, _rms = self.sep_service.compute_background(self.data, self.params)
            self.bkg_ready.emit(self.frame_index, self.generation, bkg, residual)
        except Exception as exc:
            self.bkg_error.emit(self.frame_index, self.generation, str(exc))
        finally:
            self.finished.emit(self.frame_index)
