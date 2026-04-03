from __future__ import annotations

import unittest
from unittest.mock import patch

import sys
from pathlib import Path

REPO_PARENT = Path(__file__).resolve().parents[2]
if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))

from astroview.app.frame_render_worker import FrameRenderWorker
from astroview.core.fits_data import FITSData


class _FakeThread:
    def __init__(self) -> None:
        self.interrupted = False

    def isInterruptionRequested(self) -> bool:
        return self.interrupted


class TestFrameRenderWorker(unittest.TestCase):
    def test_run_emits_preview_then_full_render(self) -> None:
        worker = FrameRenderWorker(
            request_id=7,
            generation=2,
            frame_index=3,
            data=FITSData(path="demo.fits"),
            stretch_name="Linear",
            interval_name="ZScale",
        )
        previews: list[tuple[int, int, int, object]] = []
        renders: list[tuple[int, int, int, object]] = []
        finished: list[int] = []

        worker.preview_ready.connect(lambda req, gen, idx, img: previews.append((req, gen, idx, img)))
        worker.render_ready.connect(lambda req, gen, idx, img: renders.append((req, gen, idx, img)))
        worker.finished.connect(finished.append)

        with patch("astroview.app.frame_render_worker.QThread.currentThread", return_value=_FakeThread()):
            with patch("astroview.app.frame_render_worker.render_preview_u8", return_value="preview") as preview_mock:
                with patch("astroview.app.frame_render_worker.render_image_u8", return_value="full") as full_mock:
                    worker.run()

        self.assertEqual(previews, [(7, 2, 3, "preview")])
        self.assertEqual(renders, [(7, 2, 3, "full")])
        self.assertEqual(finished, [7])
        preview_mock.assert_called_once()
        full_mock.assert_called_once()

    def test_run_skips_full_render_after_interruption(self) -> None:
        fake_thread = _FakeThread()
        worker = FrameRenderWorker(
            request_id=1,
            generation=1,
            frame_index=0,
            data=FITSData(path="demo.fits"),
            stretch_name="Linear",
            interval_name="ZScale",
        )
        renders: list[tuple[int, int, int, object]] = []

        worker.render_ready.connect(lambda req, gen, idx, img: renders.append((req, gen, idx, img)))

        def preview_side_effect(*args, **kwargs):
            fake_thread.interrupted = True
            return "preview"

        with patch("astroview.app.frame_render_worker.QThread.currentThread", return_value=fake_thread):
            with patch("astroview.app.frame_render_worker.render_preview_u8", side_effect=preview_side_effect):
                with patch("astroview.app.frame_render_worker.render_image_u8") as full_mock:
                    worker.run()

        self.assertEqual(renders, [])
        full_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
