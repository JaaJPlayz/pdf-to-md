"""Tests for config loading."""

from __future__ import annotations

from pathlib import Path

from pdf_to_md.config import load_config
from pdf_to_md.models import ConvertOptions


class TestConfig:
    """Tests for configuration loading."""

    def test_load_config_defaults(self, tmp_path: Path) -> None:
        config = load_config(input_path=tmp_path / "test.pdf")
        assert isinstance(config, ConvertOptions)
        assert config.engine == "auto"
        assert config.extract_images is True

    def test_load_config_with_overrides(self, tmp_path: Path) -> None:
        config = load_config(
            input_path=tmp_path / "test.pdf",
            engine="marker",
            output_dir=tmp_path / "out",
            pages="1-5",
            recursive=True,
        )
        assert config.engine == "marker"
        assert config.output_dir == tmp_path / "out"
        assert config.pages == "1-5"
        assert config.recursive is True
