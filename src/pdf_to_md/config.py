"""Configuration loading and merging."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from pdf_to_md.models import ConvertOptions

logger = logging.getLogger(__name__)

CONFIG_FILE = "pdf2md.toml"


@dataclass
class Config:
    """Loaded configuration from file and CLI args."""

    input_path: Path
    output_dir: Path | None = None
    engine: str = "auto"
    pages: str | None = None
    extract_images: bool = True
    recursive: bool = False


def load_config(
    input_path: Path,
    output_dir: Path | None = None,
    engine: str = "auto",
    pages: str | None = None,
    extract_images: bool = True,
    recursive: bool = False,
) -> ConvertOptions:
    """Load configuration from TOML file and merge with CLI arguments.

    CLI arguments take precedence over file config.

    Args:
        input_path: Path to input PDF or directory.
        output_dir: Output directory override.
        engine: Engine selection override.
        pages: Page range override.
        extract_images: Whether to extract images.
        recursive: Whether to recurse into directories.

    Returns:
        Merged ConvertOptions.
    """
    file_config = _load_toml(input_path.parent)

    if file_config:
        logger.debug("Loaded config from %s", CONFIG_FILE)

    file_engine = file_config.engine if file_config else "auto"
    file_output = file_config.output_dir if file_config else None
    file_pages = file_config.pages if file_config else None
    file_recursive = file_config.recursive if file_config else False

    return ConvertOptions(
        engine=engine if engine != "auto" else file_engine,
        output_dir=output_dir or file_output,
        pages=pages or file_pages,
        extract_images=extract_images,
        recursive=recursive or file_recursive,
    )


@dataclass
class _FileConfig:
    """Internal representation of the TOML config file."""

    engine: str = "auto"
    output_dir: Path | None = None
    pages: str | None = None
    recursive: bool = False
    extract_images: bool = True


def _load_toml(start_dir: Path) -> _FileConfig | None:
    """Walk up from start_dir looking for pdf2md.toml."""
    current = start_dir.resolve()

    for _ in range(10):  # prevent infinite loop
        config_path = current / CONFIG_FILE
        if config_path.exists():
            return _parse_toml(config_path)
        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def _parse_toml(path: Path) -> _FileConfig:
    """Parse a pdf2md.toml config file."""
    try:
        import tomllib

        with open(path, "rb") as f:
            data = tomllib.load(f)
    except ImportError:
        logger.warning("tomllib not available (requires Python 3.11+)")
        return _FileConfig()
    except Exception:
        logger.warning("Failed to parse %s", path)
        return _FileConfig()

    pdf2md = data.get("pdf2md", {})

    output_dir = pdf2md.get("output_dir")
    if output_dir:
        output_dir = Path(output_dir)

    return _FileConfig(
        engine=pdf2md.get("engine", "auto"),
        output_dir=output_dir,
        pages=pdf2md.get("pages"),
        recursive=pdf2md.get("recursive", False),
        extract_images=pdf2md.get("extract_images", True),
    )
