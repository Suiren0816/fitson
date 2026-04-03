# Changelog

## Unreleased

### Added
- Added `tests/run_tests.ps1` and `tests/run_tests.bat` for one-click test execution in the conda `astro` environment.
- Added `app/file_load_worker.py` for background multi-file FITS loading.
- Added `app/frame_render_worker.py` for background frame rendering with progressive preview/full-resolution updates.
- Added targeted tests for background file loading, background frame rendering, and main-window loading/render scheduling.
- Added a repository-root compatibility launcher so `python -m astroview` works from both the package parent directory and the repository root.
- Added shared render helpers in `core/fits_service.py` for full-resolution and low-resolution preview rendering.

### Changed
- Expanded the test baseline from a handful of partial tests to a broader executable suite covering FITS loading, rendering, SEP, source catalogs, file loading, and frame rendering.
- Moved multi-file FITS loading off the UI thread to keep the main window responsive while importing large datasets.
- Changed first-image presentation to use a fast preview-first strategy before full-resolution rendering completes.
- Changed dirty-frame activation and frame switching to use background rendering instead of synchronous UI-thread rendering.
- Updated the README to document the current startup behavior, test workflow, architecture additions, and recent GPT-5.4 contributions.

### Validated
- Verified the test suite in the conda `astro` environment with `python -m unittest discover -s tests -v`.
- Verified large-sample responsiveness against `tests/data` with background loading, progressive first-frame rendering, and background frame switching.
