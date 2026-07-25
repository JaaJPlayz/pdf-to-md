"""Tests for CLI module."""

from __future__ import annotations

from click.testing import CliRunner

from pdf_to_md.cli import cli


class TestCli:
    """Tests for the CLI interface."""

    def test_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Convert PDF files to Markdown" in result.output

    def test_version(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
