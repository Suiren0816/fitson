from __future__ import annotations

import unittest
from unittest.mock import patch

import numpy as np

from core.fits_data import FITSData
from core.fits_service import FITSService, _subsample, render_preview_u8


class _IdentityStretch:
    def __call__(self, data: np.ndarray) -> np.ndarray:
        return data


class _FixedInterval:
    def __init__(self, vmin: float, vmax: float) -> None:
        self.vmin = vmin
        self.vmax = vmax

    def get_limits(self, data: np.ndarray) -> tuple[float, float]:
        return self.vmin, self.vmax


class TestFITSService(unittest.TestCase):
    def test_open_file_loads_and_stores_current_data(self) -> None:
        service = FITSService()
        loaded = FITSData(path="demo.fits")

        with patch("core.fits_service.FITSData.load", return_value=loaded) as load_mock:
            result = service.open_file("demo.fits", hdu_index=2)

        self.assertIs(result, loaded)
        self.assertIs(service.current_data, loaded)
        load_mock.assert_called_once_with("demo.fits", 2)

    def test_build_render_request_reflects_selected_controls(self) -> None:
        service = FITSService()

        service.set_stretch("Asinh")
        service.set_interval("99%")
        request = service.build_render_request()

        self.assertEqual(request.stretch_name, "Asinh")
        self.assertEqual(request.interval_name, "99%")

    def test_render_returns_empty_result_when_no_image_is_loaded(self) -> None:
        service = FITSService()

        result = service.render()

        self.assertIsNone(result.image_u8)
        self.assertEqual(result.width, 0)
        self.assertEqual(result.height, 0)

    def test_render_normalizes_clips_and_preserves_dimensions(self) -> None:
        service = FITSService()
        service.current_data = FITSData(
            data=np.array([[0.0, 5.0], [10.0, 15.0]], dtype=np.float32)
        )

        with patch("core.fits_service._build_interval", return_value=_FixedInterval(0.0, 10.0)):
            with patch("core.fits_service._build_stretch", return_value=_IdentityStretch()):
                result = service.render()

        expected = np.array([[0, 127], [255, 255]], dtype=np.uint8)
        self.assertEqual(result.width, 2)
        self.assertEqual(result.height, 2)
        self.assertTrue(np.array_equal(result.image_u8, expected))

    def test_header_text_and_current_wcs_proxy_active_data(self) -> None:
        service = FITSService()
        wcs = object()
        service.current_data = FITSData(header={"NAXIS": 2}, wcs=wcs, has_wcs=True)

        with patch("core.fits_data.FITSData.header_as_text", return_value="SIMPLE  = T"):
            self.assertEqual(service.header_text(), "SIMPLE  = T")

        self.assertIs(service.current_wcs(), wcs)

    def test_render_preview_u8_returns_none_for_small_images(self) -> None:
        data = FITSData(data=np.arange(16, dtype=np.float32).reshape(4, 4))

        preview = render_preview_u8(data, "Linear", "ZScale", max_dimension=8)

        self.assertIsNone(preview)

    def test_render_preview_u8_upscales_preview_back_to_full_shape(self) -> None:
        data = FITSData(data=np.arange(16, dtype=np.float32).reshape(4, 4))
        preview_tile = np.array([[10, 20], [30, 40]], dtype=np.uint8)

        with patch("core.fits_service.render_image_u8", return_value=preview_tile) as render_mock:
            preview = render_preview_u8(data, "Linear", "ZScale", max_dimension=2)

        self.assertEqual(preview.shape, (4, 4))
        self.assertTrue(np.array_equal(
            preview,
            np.array(
                [[10, 10, 20, 20], [10, 10, 20, 20], [30, 30, 40, 40], [30, 30, 40, 40]],
                dtype=np.uint8,
            ),
        ))
        render_data = render_mock.call_args.args[0]
        self.assertEqual(render_data.data.shape, (2, 2))

    def test_subsample_strides_large_arrays(self) -> None:
        data = np.arange(2_000 * 1_500, dtype=np.float32).reshape(2_000, 1_500)

        sample = _subsample(data, max_size=1_000)

        self.assertEqual(sample.shape, (1_000, 1_500))
        self.assertTrue(np.array_equal(sample, data[::2, ::1]))


if __name__ == "__main__":
    unittest.main()
