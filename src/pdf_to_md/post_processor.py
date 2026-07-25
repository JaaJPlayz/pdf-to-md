"""Post-processing for Markdown output."""

from __future__ import annotations

import re


class PostProcessor:
    """Cleans up and normalizes Markdown output from conversion engines."""

    def process(self, markdown: str) -> str:
        """Run all post-processing steps on the Markdown content.

        Args:
            markdown: Raw Markdown from the conversion engine.

        Returns:
            Cleaned and normalized Markdown.
        """
        markdown = self._normalize_whitespace(markdown)
        markdown = self._fix_heading_levels(markdown)
        markdown = self._clean_blank_lines(markdown)
        markdown = self._normalize_tables(markdown)
        return markdown.strip() + "\n"

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize trailing whitespace and tabs."""
        lines = text.split("\n")
        return "\n".join(line.rstrip() for line in lines)

    def _fix_heading_levels(self, text: str) -> str:
        """Ensure heading levels are consistent.

        If content starts with h2 or h3, shift everything up to start at h1.
        """
        lines = text.split("\n")
        min_level = 6

        for line in lines:
            match = re.match(r"^(#{1,6})\s", line)
            if match:
                level = len(match.group(1))
                if level < min_level:
                    min_level = level

        if min_level > 1:
            shift = min_level - 1
            new_lines = []
            for line in lines:
                match = re.match(r"^(#{1,6})\s(.*)", line)
                if match:
                    new_level = len(match.group(1)) - shift
                    new_level = max(1, new_level)
                    new_lines.append(f"{'#' * new_level} {match.group(2)}")
                else:
                    new_lines.append(line)
            return "\n".join(new_lines)

        return text

    def _clean_blank_lines(self, text: str) -> str:
        """Collapse 3+ consecutive blank lines into 2."""
        return re.sub(r"\n{3,}", "\n\n", text)

    def _normalize_tables(self, text: str) -> str:
        """Ensure table rows have consistent pipe formatting."""
        lines = text.split("\n")
        result: list[str] = []

        for line in lines:
            stripped = line.strip()
            if "|" in stripped and stripped.startswith("|"):
                if not stripped.endswith("|"):
                    stripped = stripped + " |"
            result.append(stripped if stripped != line.strip() else line)

        return "\n".join(result)
