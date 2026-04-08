# Changelog

## Unreleased

## 1.2.8 - 2026-04-08

### Added
- Added a SEP background / residual view mode toggle: `F1` switches between original and background, `F2` between original and residual; both modes share a per-frame cache so toggling is instant after the first compute.
- Added asynchronous background computation via `app/frame_bkg_worker.py` so SEP background extraction never blocks the UI; the status bar shows `正在计算背景...` while a worker runs and adjacent frames are pre-warmed for smoother stepping.
- Added `SEPService.compute_background()` as the single entry point for SEP background/residual computation, with new `bkg_box_size` and `bkg_filter_size` parameters exposed in the SEP panel; changing either invalidates the cached background and triggers a re-render.
- Added a persistent view-mode badge (`BKG` / `RESIDUAL`) in the status bar plus a `[BKG]` / `[RESIDUAL]` suffix in the window title so the active view is always visible.
- Added `Background` and `Residual` cutout-review modes that slice from the same cached background/residual frames used by the main view.
- Added auto-selection of the only source after a SEP extraction returns exactly one record, so the canvas highlight, table row, and cutout preview update without an extra click.
- Added a hover-to-highlight signal in the source table: hovering a row temporarily highlights the corresponding source on the canvas without disturbing the click selection or cutout preview.
- Added a custom dock title bar with dock/undock and close buttons; floating docks now also gain native minimize / maximize / close window controls so each panel can be used as a standalone window.
- Added an image-orientation property with all 8 D4 transforms (identity, flip H/V, rotate 90/180/270, transpose, anti-transpose) under `视图 → 图像方向`. Orientation is persisted via `QSettings` (`view/orientation`) and applied as the primary display property: every loaded frame is presented in the chosen orientation from the start.
- Added `app/compass_overlay.py`, a small `CompassOverlay` widget anchored to the canvas top-right that paints the displayed-frame directions of the original `+X` and `+Y` axes and updates whenever the orientation changes.

### Changed
- `MainWindow._render_data_for_index()` is now cache-only and never blocks the UI thread on SEP computation; cache misses dispatch a `FrameBkgWorker` and the canvas updates when the result lands.
- `_invalidate_bkg_caches()` centralizes background/residual cache invalidation, cancels in-flight workers, and re-renders only the frames that actually depend on the cache.
- `ImageCanvas.draw_sources()` now consults an optional position-transform callable so source overlays follow the active orientation while the underlying catalog stays in original-image coordinates.
- Cursor sampling and ROI extraction now inverse-map displayed coordinates back to the original frame, so SEP, cutout, header, and pixel-value lookups always operate on the unrotated data regardless of the active view mode or orientation.
- Closing a file resets the view mode to original, clears the orientation badge, and cancels any in-flight background workers.

### Fixed
- Fixed a crash when switching image orientation on PySide6 builds where `QImage.mirrored()` rejects keyword arguments; orientation changes now use a Qt-compatible transform path.
- Fixed oriented frame rendering so the displayed `QImage` transform matches the catalog/cursor coordinate mapping for all 8 supported D4 orientations.
- Added regression coverage for all 8 image-orientation transforms so future orientation refactors do not reintroduce display/coordinate mismatches.

## 1.2.7 - 2026-04-07

### Added
- Added `app/theme.py` providing Fusion-based light and dark themes with full QSS coverage (menus, toolbars, docks, buttons, inputs, tables, scrollbars, tabs, sliders, progress bars).
- Added a `视图 → 主题` submenu with `浅色 / 深色` exclusive switching; the selection is persisted via `QSettings` under `ui/theme` and restored on next launch. Default theme is light.
- Added runtime-generated chevron arrow icons for `QSpinBox` / `QDoubleSpinBox`, rendered with `QPainter` to PNG in a temp cache directory and referenced from QSS for reliable cross-DPI display.
- Added a `Connected Region` view in cutout review so the selected source's segmentation region can be inspected directly.

### Changed
- `main.py` now applies the saved theme immediately after creating the `QApplication`.
- Removed the hard-coded global font size from the stylesheet so fonts follow the system setting and scale correctly on high-DPI displays.
- Widened spinbox up/down buttons with distinct hover/pressed states and a separator between them for clearer interaction affordance.

### Fixed
- Fixed packaged app version reporting so rebuilt installers no longer ship an older bundled app version.
- Fixed Windows packaged startup failures by collecting the required PySide6/Shiboken runtime DLLs and NumPy 2.4 modules.

### Validated
- Verified source table, source catalog, SEP, and main-window loading tests for the connected-region cutout workflow.
- Verified the rebuilt frozen Windows app starts successfully after the packaging fixes.

## 1.2.6 - 2026-04-06

### Added
- Added `VERSION`, `setup.py`, `pyproject.toml`, `MANIFEST.in`, and `environment.yml` so the project has explicit metadata, a reproducible environment definition, and a single version source.
- Added `scripts/build_windows.ps1` and GitHub Actions workflows for automated tests and Windows release builds.
- Added runtime file logging and unhandled-exception hooks so unexpected GUI failures leave a diagnostic trail for support.
- Added `tests/run_tests.ps1` and `tests/run_tests.bat` for one-click test execution in the conda `astro` environment.
- Added `app/file_load_worker.py` for background multi-file FITS loading.
- Added `app/frame_render_worker.py` for background frame rendering with progressive preview/full-resolution updates.
- Added `app/histogram_dock.py` to expose image histograms and manual display-range controls in the UI.
- Added `app/sep_extract_worker.py` so SEP source extraction runs off the UI thread.
- Added a `Check for Updates...` action in the Help menu with a background GitHub release/tag check worker.
- Added targeted tests for background file loading, background frame rendering, and main-window loading/render scheduling.
- Added a repository-root compatibility launcher so `python -m astroview` works from both the package parent directory and the repository root.
- Added shared render helpers in `core/fits_service.py` for full-resolution and low-resolution preview rendering.
- Added a source-detail panel with per-target field inspection and cutout preview in the `Source Table` dock.
- Added canvas-to-table source selection sync so double-clicking a source overlay selects the matching row in `Source Table`.

### Changed
- Changed package metadata and installer versioning to read from the repository `VERSION` file instead of repeating literal version strings.
- Changed test and build workflows to prefer the active Python environment rather than hard-coded local Miniforge paths.
- Expanded the test baseline from a handful of partial tests to a broader executable suite covering FITS loading, rendering, SEP, source catalogs, file loading, and frame rendering.
- Moved multi-file FITS loading off the UI thread to keep the main window responsive while importing large datasets.
- Changed first-image presentation to use a fast preview-first strategy before full-resolution rendering completes.
- Changed dirty-frame activation and frame switching to use background rendering instead of synchronous UI-thread rendering.
- Changed display defaults for newly opened FITS files to `Stretch=Linear` and `Interval=ZScale`.
- Changed the rendering pipeline to support manual interval limits alongside the existing stretch/interval presets.
- Changed extracted source tables to always expose `ID`, `X`, and `Y`, with persistent sorting/filtering state and richer source metrics such as `NPix` and `BkgRMS`.
- Changed source export workflow to standardize on CSV, with the former `Ctrl+Shift+E` region-export shortcut now routed to the same CSV export action.
- Changed the main window title to show the current application version and fixed packaged FITS loading for non-contiguous preview buffers that previously left the window blank after `Open`.
- Changed the update checker to bypass system proxy settings and fixed packaged HTTPS support by bundling the required SSL runtime files.
- Updated the README to document the current startup behavior, test workflow, architecture additions, and recent GPT-5.4 contributions.

### Validated
- Verified the test suite in the conda `astro` environment with `python -m unittest discover -s tests -v`.
- Verified large-sample responsiveness against `tests/data` with background loading, progressive first-frame rendering, and background frame switching.
