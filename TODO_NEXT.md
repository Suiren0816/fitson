# Next-Step Todo

This file tracks the next performance and product-quality tasks worth doing after the current loading/rendering refactor.

## Rendering and Playback
- Prewarm the next frame preview during playback so frame stepping and autoplay feel more continuous.
- Add a small render queue/prioritization policy so the current frame always wins over stale background render requests.
- Consider a multi-stage preview pipeline for very large images, such as 1024 px preview, then 2048 px preview, then full render.
- Revisit whether full-resolution background render results should preserve zoom/viewport position more explicitly during fast frame switches.

## Data Loading
- Profile FITS files with real WCS payloads and compressed HDUs to see whether WCS construction or HDU scanning needs its own optimization path.
- Consider optional metadata-only preloading for large frame sets so playback can start before every frame is fully opened.
- Decide whether append-frame loading should surface a richer in-UI progress indicator than the current status-bar text.

## UI and UX
- Add an explicit busy/loading indicator in the canvas for frames that are still rendering in the background.
- Expose a user-facing preference for preview aggressiveness or maximum preview dimension.
- Review whether frame-player controls should be temporarily throttled or visually annotated while a requested frame is still rendering.

## Robustness and Testing
- Add integration-style Qt tests that exercise real `QThread` worker scheduling and signal delivery without relying only on mocked call paths.
- Add regression tests around repeated stretch/interval changes while background renders are in flight.
- Add tests for cancellation behavior when closing the window or opening a new file set during active background loading/rendering.
- Validate packaged Windows builds after the new worker-based rendering changes.
