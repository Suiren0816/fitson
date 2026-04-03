from __future__ import annotations

import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

import sys
from pathlib import Path

REPO_PARENT = Path(__file__).resolve().parents[2]
if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))

from astroview.app.main_window import MainWindow
from astroview.core.fits_data import FITSData


class TestMainWindowLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._app = QApplication.instance() or QApplication([])

    def test_open_file_with_explicit_path_starts_background_load(self) -> None:
        window = MainWindow()
        try:
            with patch.object(window, "_start_frame_load") as start_mock:
                window.open_file(path="tests/data/1.FITS", hdu_index=2)

            start_mock.assert_called_once_with(["tests/data/1.FITS"], hdu_index=2, append=False)
        finally:
            window.deleteLater()

    def test_handle_loaded_frame_activates_first_frame(self) -> None:
        window = MainWindow()
        window.app_status_bar = Mock()
        try:
            with patch.object(window, "_activate_frame") as activate_mock:
                with patch.object(window, "_sync_frame_player") as sync_mock:
                    window._handle_loaded_frame(FITSData(path="first.fits"), None)

            self.assertEqual(len(window._frames), 1)
            self.assertEqual(len(window._frame_images), 1)
            self.assertEqual(window._frame_dirty, [True])
            activate_mock.assert_called_once_with(0)
            sync_mock.assert_called_once_with()
            window.app_status_bar.set_frame_info.assert_called_once_with(0, 1)
        finally:
            window.deleteLater()

    def test_handle_loaded_frame_preserves_current_frame_during_append(self) -> None:
        window = MainWindow()
        window.app_status_bar = Mock()
        window._frames = [FITSData(path="existing.fits")]
        window._frame_images = [None]
        window._frame_dirty = [False]
        window._current_frame_index = 0
        try:
            with patch.object(window, "_activate_frame") as activate_mock:
                with patch.object(window, "_sync_frame_player") as sync_mock:
                    window._handle_loaded_frame(FITSData(path="appended.fits"), None)

            self.assertEqual([frame.path for frame in window._frames], ["existing.fits", "appended.fits"])
            self.assertEqual(window._frame_images, [None, None])
            self.assertEqual(window._frame_dirty, [False, True])
            activate_mock.assert_not_called()
            sync_mock.assert_called_once_with()
            window.app_status_bar.set_frame_info.assert_called_once_with(0, 2)
        finally:
            window.deleteLater()

    def test_handle_loaded_frame_uses_preview_image_and_keeps_frame_dirty(self) -> None:
        window = MainWindow()
        window.app_status_bar = Mock()
        try:
            with patch.object(window, "_qimage_from_u8", return_value="preview-image") as qimage_mock:
                with patch.object(window, "_activate_frame") as activate_mock:
                    with patch.object(window, "_sync_frame_player") as sync_mock:
                        window._handle_loaded_frame(FITSData(path="first.fits"), preview_image_u8="preview-u8")

            self.assertEqual(window._frame_images, ["preview-image"])
            self.assertEqual(window._frame_dirty, [True])
            qimage_mock.assert_called_once_with("preview-u8")
            activate_mock.assert_called_once_with(0)
            sync_mock.assert_called_once_with()
        finally:
            window.deleteLater()

    def test_activate_frame_schedules_background_render_for_dirty_frame(self) -> None:
        window = MainWindow()
        window._frames = [FITSData(path="first.fits")]
        window._frame_images = [None]
        window._frame_dirty = [True]
        try:
            with patch.object(window, "_schedule_frame_render") as schedule_mock:
                window._activate_frame(0)

            schedule_mock.assert_called_once_with(0)
        finally:
            window.deleteLater()

    def test_handle_frame_preview_rendered_updates_current_image(self) -> None:
        window = MainWindow()
        window._frames = [FITSData(path="frame.fits")]
        window._frame_images = [None]
        window._frame_dirty = [True]
        window._current_frame_index = 0
        window._render_generation = 3
        window._latest_render_request_by_index[0] = 11
        try:
            with patch.object(window, "_qimage_from_u8", return_value="preview-image") as qimage_mock:
                with patch.object(window, "_show_current_frame_image") as show_mock:
                    window._handle_frame_preview_rendered(11, 3, 0, "preview-u8")

            self.assertEqual(window._frame_images, ["preview-image"])
            self.assertEqual(window._frame_dirty, [True])
            qimage_mock.assert_called_once_with("preview-u8")
            show_mock.assert_called_once_with()
        finally:
            window.deleteLater()

    def test_handle_frame_rendered_marks_frame_clean(self) -> None:
        window = MainWindow()
        window._frames = [FITSData(path="frame.fits")]
        window._frame_images = [None]
        window._frame_dirty = [True]
        window._current_frame_index = 0
        window._render_generation = 3
        window._latest_render_request_by_index[0] = 12
        try:
            with patch.object(window, "_qimage_from_u8", return_value="final-image") as qimage_mock:
                with patch.object(window, "_show_current_frame_image") as show_mock:
                    window._handle_frame_rendered(12, 3, 0, "full-u8")

            self.assertEqual(window._frame_images, ["final-image"])
            self.assertEqual(window._frame_dirty, [False])
            qimage_mock.assert_called_once_with("full-u8")
            show_mock.assert_called_once_with()
        finally:
            window.deleteLater()


if __name__ == "__main__":
    unittest.main()
