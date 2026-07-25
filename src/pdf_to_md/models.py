"""Data models for pdf-to-md."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConvertOptions:
    """Configuration options for a conversion run."""

    engine: str = "auto"
    output_dir: Path | None = None
    pages: str | None = None
    extract_images: bool = True
    recursive: bool = False


@dataclass
class PageResult:
    """Result of converting a single page."""

    page_number: int
    markdown: str
    images: list[Path] = field(default_factory=list)


@dataclass
class ConvertResult:
    """Result of converting a complete PDF file."""

    input_path: Path
    output_path: Path
    markdown: str
    images: list[Path] = field(default_factory=list)
    page_count: int = 0
    engine_used: str = ""
