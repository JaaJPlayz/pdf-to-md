"""Tests for the converter module."""

from __future__ import annotations

from pathlib import Path

import pytest

from pdf_to_md.converter import Converter
from pdf_to_md.models import ConvertOptions


class TestConverter:
    """Tests for the Converter class."""

    def test_convert_file_raises_on_missing(self, tmp_path: Path) -> None:
        options = ConvertOptions()
        converter = Converter(options)

        with pytest.raises(FileNotFoundError):
            converter.convert_file(tmp_path / "nonexistent.pdf")

    def test_pages_to_markdown_heading(self, tmp_path: Path) -> None:
        options = ConvertOptions()
        converter = Converter(options)

        pages = [
            {"page_number": 1, "blocks": [
                {"type": "heading", "content": "Title", "level": 1},
                {"type": "paragraph", "content": "Body text.", "level": 0},
            ]}
        ]

        result = converter._pages_to_markdown(pages)
        assert "# Title" in result
        assert "Body text." in result

    def test_pages_to_markdown_list(self, tmp_path: Path) -> None:
        options = ConvertOptions()
        converter = Converter(options)

        pages = [
            {"page_number": 1, "blocks": [
                {"type": "list", "content": "- item one\n- item two", "level": 0},
            ]}
        ]

        result = converter._pages_to_markdown(pages)
        assert "- item one" in result
