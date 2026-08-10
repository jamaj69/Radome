"""Shared paths for temporary figure-master build artifacts."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"


def ensure_build_dir() -> Path:
    BUILD.mkdir(exist_ok=True)
    return BUILD


def build_output(name: str) -> Path:
    return ensure_build_dir() / name

