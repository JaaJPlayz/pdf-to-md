"""Custom exceptions for pdf-to-md."""

from __future__ import annotations


class PdfToMdError(Exception):
    """Base exception for pdf-to-md errors."""


class ConversionError(PdfToMdError):
    """Raised when PDF conversion fails."""


class EngineError(PdfToMdError):
    """Raised when a conversion engine fails or is unavailable."""


class ConfigError(PdfToMdError):
    """Raised when configuration is invalid."""
