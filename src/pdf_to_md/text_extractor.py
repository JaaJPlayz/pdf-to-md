"""PDF text extraction using pymupdf."""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extracts structured text from PDF pages using pymupdf.

    Analyzes font sizes and weights to detect headings, and uses
    block positioning to detect lists and tables.
    """

    def extract(self, pdf_path: Path) -> list[dict[str, object]]:
        """Extract structured text from all pages of a PDF.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of page dicts, each with 'page_number' and 'blocks'.
        """
        import pymupdf

        doc = pymupdf.open(str(pdf_path))
        pages: list[dict[str, object]] = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = self._extract_page(page)
            pages.append({"page_number": page_num + 1, "blocks": blocks})

        doc.close()
        logger.info("Extracted %d pages from %s", len(pages), pdf_path.name)
        return pages

    def extract_images(self, pdf_path: Path) -> list[dict[str, object]]:
        """Extract all images from a PDF.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of image dicts with 'page', 'xref', 'bytes', 'ext'.
        """
        import pymupdf

        doc = pymupdf.open(str(pdf_path))
        images: list[dict[str, object]] = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)

            for img in image_list:
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                except Exception:
                    logger.debug("Could not extract image xref=%d", xref)
                    continue

                if not base_image or not base_image.get("image"):
                    continue

                images.append({
                    "page": page_num + 1,
                    "xref": xref,
                    "bytes": base_image["image"],
                    "ext": base_image.get("ext", "png"),
                })

        doc.close()
        logger.info("Extracted %d images from %s", len(images), pdf_path.name)
        return images

    def _extract_page(self, page: object) -> list[dict[str, object]]:
        """Extract text blocks from a single page.

        Each block contains: type (text/table/list/heading), content, and level.
        """
        blocks: list[dict[str, object]] = []
        text_dict = page.get_text("dict", flags=0)  # type: ignore[attr-defined]

        font_sizes: list[float] = []
        for block in text_dict.get("blocks", []):  # type: ignore[attr-defined]
            if block.get("type") != 0:  # text block
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = span.get("size", 12.0)
                    if size > 0:
                        font_sizes.append(size)

        median_size = _median(font_sizes) if font_sizes else 12.0

        for block in text_dict.get("blocks", []):  # type: ignore[attr-defined]
            if block.get("type") != 0:  # text block
                continue

            block_text = self._extract_block_text(block)
            if not block_text.strip():
                continue

            block_info = self._classify_block(block, block_text, median_size)
            blocks.append(block_info)

        return blocks

    def _extract_block_text(self, block: dict[str, object]) -> str:
        """Extract text content from a block, joining lines."""
        lines: list[str] = []
        for line in block.get("lines", []):  # type: ignore[union-attr]
            spans_text = ""
            for span in line.get("spans", []):  # type: ignore[union-attr]
                spans_text += span.get("text", "")  # type: ignore[arg-type]
            lines.append(spans_text)
        return "\n".join(lines)

    def _classify_block(
        self,
        block: dict[str, object],
        text: str,
        median_size: float,
    ) -> dict[str, object]:
        """Classify a text block as heading, list, or paragraph."""
        spans = []
        for line in block.get("lines", []):  # type: ignore[union-attr]
            for span in line.get("spans", []):  # type: ignore[union-attr]
                spans.append(span)

        if not spans:
            return {"type": "paragraph", "content": text, "level": 0}

        max_size = max(s.get("size", 12.0) for s in spans)  # type: ignore[arg-type]
        avg_weight = _avg_weight(spans)

        if max_size > median_size * 1.3:
            level = self._size_to_heading_level(max_size, median_size)
            return {"type": "heading", "content": text, "level": level}

        has_bold_flag = all(
            s.get("flags", 0) & 16 for s in spans if s.get("text", "").strip()
        )
        if avg_weight >= 600 or has_bold_flag:
            return {"type": "bold_paragraph", "content": text, "level": 0}

        lines = text.split("\n")
        if lines and re.match(r"^\s*[-*•]\s", lines[0]):
            return {"type": "list", "content": text, "level": 0}
        if lines and re.match(r"^\s*\d+[.)]\s", lines[0]):
            return {"type": "numbered_list", "content": text, "level": 0}

        return {"type": "paragraph", "content": text, "level": 0}

    def _size_to_heading_level(self, size: float, median: float) -> int:
        """Map font size relative to median into a heading level (1-6)."""
        ratio = size / median
        if ratio >= 1.8:
            return 1
        if ratio >= 1.5:
            return 2
        if ratio >= 1.3:
            return 3
        return 4


def _median(values: list[float]) -> float:
    """Compute median of a list of floats."""
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def _avg_weight(spans: list[dict[str, object]]) -> float:
    """Compute average font weight from spans."""
    weights = [s.get("weight", 400) for s in spans]  # type: ignore[union-attr]
    if not weights:
        return 400.0
    return sum(weights) / len(weights)  # type: ignore[arg-type]
