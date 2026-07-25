"""Tests for the post-processor module."""

from pdf_to_md.post_processor import PostProcessor


class TestPostProcessor:
    """Tests for PostProcessor."""

    def test_process_strips_trailing_whitespace(self) -> None:
        pp = PostProcessor()
        input_md = "Hello   \nWorld   \n"
        result = pp.process(input_md)
        assert result == "Hello\nWorld\n"

    def test_fix_heading_levels(self) -> None:
        pp = PostProcessor()
        input_md = "## Title\n### Subtitle\nBody"
        result = pp.process(input_md)
        assert result.startswith("# Title\n## Subtitle\n")

    def test_clean_blank_lines(self) -> None:
        pp = PostProcessor()
        input_md = "A\n\n\n\n\nB\n"
        result = pp.process(input_md)
        assert "\n\n\n" not in result

    def test_normalize_tables_adds_trailing_pipe(self) -> None:
        pp = PostProcessor()
        input_md = "| A | B\n|---|---|\n| 1 | 2 |\n"
        result = pp.process(input_md)
        assert "| A | B |" in result

    def test_process_strips_and_adds_newline(self) -> None:
        pp = PostProcessor()
        result = pp.process("Hello\n")
        assert result.endswith("\n")
        assert not result.startswith("\n")
