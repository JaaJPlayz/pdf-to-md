# pdf-to-md

Convert PDF documents to clean Markdown files.

## Features

- **Text extraction**: Uses `pymupdf` for accurate text and layout extraction
- **Heading detection**: Automatically detects headings from font sizes
- **Image extraction**: Pulls embedded images and references them in Markdown
- **Batch processing**: Convert entire directories recursively
- **Post-processing**: Normalizes headings, whitespace, and formatting

## Installation

```bash
uv sync --all-extras
```

## Usage

```bash
# Single file
pdf2md input.pdf

# With output directory
pdf2md input.pdf -o ./output/

# Batch convert
pdf2md ./pdfs/ -r -o ./markdown/

# Page range
pdf2md input.pdf --pages 1-10

# Verbose
pdf2md input.pdf -v
```

## Configuration

Create a `pdf2md.toml` in your project root:

```toml
[pdf2md]
extract_images = true
recursive = false
# output_dir = "./output"
# pages = "1-10"
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Type check
uv run mypy src/pdf_to_md/

# Lint
uv run ruff check src/ tests/
```

## License

MIT
