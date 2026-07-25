"""Image extraction from PDFs."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageHandler:
    """Handles extracting and saving images from PDF files."""

    def extract_images(self, pdf_path: Path, md_output_path: Path) -> list[Path]:
        """Extract images from a PDF and save them alongside the Markdown.

        Args:
            pdf_path: Path to the source PDF.
            md_output_path: Path where the Markdown file will be written.

        Returns:
            List of paths to extracted image files.
        """
        import pymupdf

        images_dir = md_output_path.parent / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        extracted: list[Path] = []

        try:
            doc = pymupdf.open(str(pdf_path))
        except Exception:
            logger.warning("Could not open PDF for image extraction: %s", pdf_path)
            return extracted

        stem = md_output_path.stem

        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                except Exception:
                    logger.debug("Could not extract image xref=%d", xref)
                    continue

                if not base_image or not base_image.get("image"):
                    continue

                ext = base_image.get("ext", "png")
                img_filename = f"{stem}_p{page_num + 1}_img{img_index + 1}.{ext}"
                img_path = images_dir / img_filename

                img_path.write_bytes(base_image["image"])
                extracted.append(img_path)

        doc.close()
        logger.info("Extracted %d images from %s", len(extracted), pdf_path.name)

        return extracted
