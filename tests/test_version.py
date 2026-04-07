from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import sys

REPO_PARENT = Path(__file__).resolve().parents[2]
if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))

from astroview import __version__
from astroview import version as version_module
from astroview.version import read_version


class TestVersion(unittest.TestCase):
    def test_package_version_matches_version_file(self) -> None:
        self.assertEqual(__version__, read_version())

    def test_read_version_prefers_meipass_bundle_when_source_file_is_missing(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package_dir = root / "source" / "astroview"
            bundle_dir = root / "bundle" / "astroview"
            package_dir.mkdir(parents=True)
            bundle_dir.mkdir(parents=True)
            (bundle_dir / "VERSION").write_text("9.9.9\n", encoding="utf-8")

            with patch.object(version_module, "__file__", str(package_dir / "version.py")):
                with patch.object(version_module.sys, "_MEIPASS", str(root / "bundle"), create=True):
                    with patch.object(version_module.sys, "executable", str(root / "AstroView.exe")):
                        self.assertEqual(read_version(), "9.9.9")

    def test_read_version_uses_onedir_bundle_next_to_executable(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package_dir = root / "source" / "astroview"
            bundle_dir = root / "dist" / "_internal" / "astroview"
            package_dir.mkdir(parents=True)
            bundle_dir.mkdir(parents=True)
            (bundle_dir / "VERSION").write_text("2.3.4\n", encoding="utf-8")

            with patch.object(version_module, "__file__", str(package_dir / "version.py")):
                with patch.object(version_module.sys, "_MEIPASS", None, create=True):
                    with patch.object(version_module.sys, "executable", str(root / "dist" / "AstroView.exe")):
                        self.assertEqual(read_version(), "2.3.4")


if __name__ == "__main__":
    unittest.main()
