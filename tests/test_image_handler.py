"""Tests for the image handler."""

from __future__ import annotations

from pathlib import Path

from pdf_to_md.image_handler import ImageHandler


class TestImageHandler:
    """Tests for ImageHandler."""

    def test_extract_images_returns_list(self, tmp_path: Path) -> None:
        handler = ImageHandler()
        # Non-existent PDF should return empty list gracefully
        result = handler.extract_images(tmp_path / "fake.pdf", tmp_path / "out.md")
        assert isinstance(result, list)
