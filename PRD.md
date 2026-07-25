# Product Requirements Document: pdf-to-md

## Overview

A Python CLI tool that converts PDF documents into well-structured Markdown files using traditional text extraction. No AI/ML dependencies — uses `pymupdf` for text and structure extraction.

## Goals

- Convert any text-based PDF into clean, readable Markdown
- Preserve document structure: headings, paragraphs, lists, tables
- Extract embedded images and reference them in the Markdown
- Support batch conversion of multiple PDFs
- Provide a simple CLI interface and a reusable Python API
- Process PDFs efficiently with progress reporting

## Target Users

- Developers digitizing documentation
- Researchers converting papers to editable format
- Teams migrating document archives to Markdown-based wikis

## Core Features

### 1. Single PDF Conversion
- Accept a PDF file path as input
- Output a `.md` file in the same directory or a specified output directory
- Preserve page structure with optional page breaks (`---`)

### 2. Text Extraction
- Use `pymupdf` for extracting text with layout awareness
- Detect headings based on font size and weight
- Detect lists, blockquotes, and code blocks by formatting cues

### 3. Batch Processing
- Accept a directory of PDFs
- Convert all `.pdf` files recursively
- Mirror the input directory structure in the output

### 4. Image Extraction
- Extract images embedded in the PDF
- Save them to an `images/` subdirectory alongside the Markdown
- Reference images using relative paths in the Markdown

### 5. Table Detection
- Detect tabular data using pymupdf's text block positioning
- Convert tables to GitHub-Flavored Markdown (GFM) table syntax

### 6. Configuration
- Configurable via CLI flags and/or a `pdf2md.toml` config file
- Options: output directory, page range, image quality, verbosity

## Non-Goals

- OCR for scanned/image-based PDFs (future feature)
- Real-time streaming conversion
- PDF editing or creation
- Multi-language OCR

## Technical Architecture

```
src/pdf_to_md/
├── __init__.py          # Package init, version
├── __main__.py          # CLI entry point
├── cli.py               # CLI argument parsing (click)
├── converter.py         # Core conversion orchestrator
├── text_extractor.py    # pymupdf-based text extraction
├── post_processor.py    # Markdown cleanup and formatting
├── image_handler.py     # Image extraction and referencing
├── config.py            # Configuration loading (TOML + CLI args)
├── models.py            # Data classes for options/results
└── exceptions.py        # Custom exceptions
```

## Dependencies

| Package | Purpose |
|---|---|
| `pymupdf` | PDF text extraction, image extraction, layout analysis |
| `click` | CLI framework |
| `rich` | Progress bars and formatted output |

## CLI Interface

```bash
# Single file conversion
pdf2md input.pdf

# Specify output directory
pdf2md input.pdf -o ./output/

# Batch convert a directory
pdf2md ./pdfs/ -o ./markdown/ --recursive

# Page range
pdf2md input.pdf --pages 1-10

# Verbose output
pdf2md input.pdf -v

# Skip images
pdf2md input.pdf --no-images
```

## Success Metrics

- Converts 90%+ of common PDF layouts accurately to Markdown
- Processes a 50-page PDF in under 10 seconds
- Produces Markdown that renders correctly on GitHub/GitLab
- Zero data loss from source PDF text content

## Out of Scope (Future)

- OCR for scanned PDFs (would require pytesseract or similar)
- PDF/A archival format support
- Web UI or API server mode
