"""Tests for models."""

from pathlib import Path

from pdf_to_md.models import ConvertOptions, ConvertResult, PageResult


class TestModels:
    """Tests for data models."""

    def test_convert_options_defaults(self) -> None:
        opts = ConvertOptions()
        assert opts.engine == "auto"
        assert opts.extract_images is True
        assert opts.recursive is False

    def test_convert_result_creation(self) -> None:
        result = ConvertResult(
            input_path=Path("test.pdf"),
            output_path=Path("test.md"),
            markdown="# Hello",
            page_count=1,
            engine_used="marker",
        )
        assert result.page_count == 1
        assert result.images == []

    def test_page_result_creation(self) -> None:
        pr = PageResult(page_number=1, markdown="## Page 1")
        assert pr.images == []
