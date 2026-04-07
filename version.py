from __future__ import annotations

from pathlib import Path
import sys


def _version_file() -> Path:
    """Return the first available runtime version file."""

    package_dir = Path(__file__).resolve().parent
    candidates = [package_dir / "VERSION"]

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "astroview" / "VERSION")

    executable = getattr(sys, "executable", None)
    if executable:
        exe_dir = Path(executable).resolve().parent
        candidates.append(exe_dir / "_internal" / "astroview" / "VERSION")
        candidates.append(exe_dir / "astroview" / "VERSION")

    seen: set[Path] = set()
    searched: list[Path] = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        searched.append(resolved)
        if resolved.is_file():
            return resolved

    raise FileNotFoundError(
        "Could not locate VERSION file. Searched: "
        + ", ".join(str(path) for path in searched)
    )


def read_version() -> str:
    """Read the application version from the runtime version file."""

    return _version_file().read_text(encoding="utf-8").strip()


__version__ = read_version()
