from __future__ import annotations

import argparse


def build_arg_parser() -> argparse.ArgumentParser:
    """Create the CLI parser for the application entry point."""

    parser = argparse.ArgumentParser(description="AstroView application entry point.")
    parser.add_argument("path", nargs="?", help="Optional FITS file path.")
    parser.add_argument("--hdu", type=int, default=None, help="Optional HDU index.")
    return parser


def main() -> int:
    """Application bootstrap placeholder."""

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
