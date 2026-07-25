# AGENTS.md - AI Agent Instructions for pdf-to-md

## Project Overview

A Python CLI tool that converts PDF documents into Markdown using `pymupdf` for text extraction. No AI/ML dependencies.

## Build & Run Commands

```bash
# Install all dependencies (editable mode)
uv sync --all-extras

# Run the CLI
uv run python -m pdf_to_md input.pdf
# or via entry point:
uv run pdf2md input.pdf

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=pdf_to_md --cov-report=term-missing

# Type checking
uv run mypy src/pdf_to_md/

# Linting
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Format check (no changes, just report)
uv run ruff format --check src/ tests/
```

## Code Style & Conventions

- **Python version**: 3.14 (specified in `.python-version`)
- **Formatter/Linter**: Ruff (replaces black, isort, flake8)
- **Type hints**: Required on all public functions and methods. Use `from __future__ import annotations` for PEP 604 union syntax.
- **Docstrings**: Google-style docstrings on all public APIs
- **Imports**: Grouped as stdlib → third-party → local, separated by blank lines (Ruff handles this)
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
- **Max line length**: 88 characters (Ruff default)

## Project Structure

```
src/pdf_to_md/          # Main package (src layout)
├── __init__.py         # Package version
├── __main__.py         # python -m pdf_to_md entry point
├── cli.py              # Click CLI definition
├── converter.py        # Orchestrator: extracts text, builds markdown, post-processes
├── text_extractor.py   # pymupdf-based text and image extraction
├── post_processor.py   # Markdown cleanup, formatting fixes
├── image_handler.py    # Image extraction from PDF, saving, relative path refs
├── config.py           # Load pdf2md.toml, merge with CLI args
├── models.py           # Dataclasses: ConvertOptions, ConvertResult, etc.
└── exceptions.py       # Custom exceptions
tests/                  # Test suite (mirrors src/ structure)
├── conftest.py
├── test_converter.py
├── test_text_extractor.py
├── test_post_processor.py
├── test_image_handler.py
├── test_cli.py
└── fixtures/           # Sample PDFs for testing
```

## Architecture Patterns

- **Dataclasses for I/O**: Use `ConvertOptions` (input config) and `ConvertResult` (output) dataclasses in `models.py` for all inter-module communication. No raw dicts.
- **Error handling**: Raise specific custom exceptions from `exceptions.py`. Never catch broadly and swallow errors. Use `click.ClickException` in CLI layer only.
- **Logging**: Use `logging` module, not print(). Configure in CLI layer. Log progress and warnings.
- **No side effects in constructors**: Handlers receive config via constructor but don't perform I/O until explicit methods are called.

## Key Design Decisions

1. **pymupdf is the sole extraction engine** — it handles text block detection, font analysis, and image extraction in one library. No ML dependencies.
2. **Heading detection** is done by comparing font sizes against the page median. Larger fonts map to lower heading levels.
3. **Images are extracted separately** by pymupdf to give us control over naming and deduplication.
4. **Post-processing** is always run to normalize Markdown output (fix heading levels, clean whitespace, normalize tables).
5. **No OCR in v1** — scanned/image-only PDFs are out of scope. This keeps dependencies light.

## Testing

- Use `pytest` with `pytest-cov` for coverage
- Fixtures in `tests/fixtures/` contain small sample PDFs (committed to repo, keep under 1MB total)
- Mock pymupdf calls in unit tests using `unittest.mock`
- Target: 80%+ line coverage

## Common Tasks

### Adding a new CLI option
1. Add flag to `cli.py` Click command
2. Add field to `ConvertOptions` dataclass in `models.py`
3. Pass through in `converter.py`
4. Add to `config.py` TOML mapping
5. Update tests

### Adding OCR support (future)
1. Add `pytesseract` as optional dependency
2. Create `src/pdf_to_md/ocr_engine.py`
3. Detect image-only PDFs in `converter.py` (pages with no text blocks)
4. Fall back to OCR for those pages

## Dependencies

Core:
- `pymupdf` - PDF text extraction, image extraction, layout analysis
- `click` - CLI framework
- `rich` - Progress bars, colored output

Dev:
- `pytest` - Testing
- `pytest-cov` - Coverage
- `mypy` - Static type checking
- `ruff` - Linting and formatting
