"""Shared test fixtures for pdf-to-md."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    """Provide a temporary output directory."""
    out = tmp_path / "output"
    out.mkdir()
    return out


@pytest.fixture
def sample_markdown() -> str:
    """Sample markdown for post-processor tests."""
    return """## Introduction

This is a test document.

### Section 1

Some content here.


More content.

### Section 2

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
