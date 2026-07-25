"""Core conversion orchestrator."""

from __future__ import annotations

import logging
from pathlib import Path

from pdf_to_md.image_handler import ImageHandler
from pdf_to_md.models import ConvertOptions, ConvertResult
from pdf_to_md.post_processor import PostProcessor
from pdf_to_md.text_extractor import TextExtractor

logger = logging.getLogger(__name__)


class Converter:
    """Orchestrates PDF to Markdown conversion.

    Uses pymupdf for text extraction and applies post-processing
    to produce clean Markdown output.
    """

    def __init__(self, options: ConvertOptions) -> None:
        """Initialize the converter.

        Args:
            options: Conversion configuration.
        """
        self.options = options
        self.extractor = TextExtractor()
        self.image_handler = ImageHandler()
        self.post_processor = PostProcessor()

    def convert_file(self, pdf_path: Path) -> ConvertResult:
        """Convert a single PDF file to Markdown.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            ConvertResult with the markdown content.

        Raises:
            FileNotFoundError: If the PDF file does not exist.
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        logger.info("Converting: %s", pdf_path)

        pages = self.extractor.extract(pdf_path)
        raw_markdown = self._pages_to_markdown(pages)

        output_path = self._get_output_path(pdf_path)

        images: list[Path] = []
        if self.options.extract_images:
            images = self.image_handler.extract_images(pdf_path, output_path)

        markdown = self.post_processor.process(raw_markdown)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")

        return ConvertResult(
            input_path=pdf_path,
            output_path=output_path,
            markdown=markdown,
            images=images,
            page_count=len(pages),
            engine_used="pymupdf",
        )

    def convert_directory(self, dir_path: Path) -> list[ConvertResult]:
        """Convert all PDFs in a directory.

        Args:
            dir_path: Path to the directory containing PDFs.

        Returns:
            List of ConvertResult for each converted file.
        """
        pattern = "**/*.pdf" if self.options.recursive else "*.pdf"
        pdf_files = sorted(dir_path.glob(pattern))

        if not pdf_files:
            logger.warning("No PDF files found in %s", dir_path)
            return []

        results: list[ConvertResult] = []
        for pdf_path in pdf_files:
            try:
                result = self.convert_file(pdf_path)
                results.append(result)
            except Exception:
                logger.exception("Failed to convert: %s", pdf_path)

        return results

    def _pages_to_markdown(self, pages: list[dict[str, object]]) -> str:
        """Convert extracted page blocks into Markdown text."""
        parts: list[str] = []

        for page in pages:
            blocks = page.get("blocks", [])  # type: ignore[union-attr]
            for block in blocks:  # type: ignore[union-attr]
                block_type = block.get("type", "paragraph")  # type: ignore[union-attr]
                content = block.get("content", "")  # type: ignore[union-attr]
                level = block.get("level", 0)  # type: ignore[union-attr]

                if block_type == "heading":
                    parts.append(f"{'#' * int(level)} {content}")
                elif block_type == "list":
                    parts.append(content)
                elif block_type == "numbered_list":
                    parts.append(content)
                elif block_type == "bold_paragraph":
                    parts.append(f"**{content.strip()}**")
                else:
                    parts.append(content)

            if parts and parts[-1] != "---":
                parts.append("---\n")

        return "\n\n".join(parts)

    def _get_output_path(self, pdf_path: Path) -> Path:
        """Determine the output path for the markdown file."""
        stem = pdf_path.stem
        if self.options.output_dir:
            return self.options.output_dir / f"{stem}.md"
        return pdf_path.parent / f"{stem}.md"
