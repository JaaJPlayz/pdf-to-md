"""CLI interface for pdf-to-md."""

from __future__ import annotations

import logging
from pathlib import Path

import click
from rich.console import Console
from rich.logging import RichHandler

from pdf_to_md.config import load_config
from pdf_to_md.converter import Converter

console = Console()
logger = logging.getLogger("pdf_to_md")


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory. Defaults to same directory as input.",
)
@click.option(
    "--engine",
    type=click.Choice(["auto", "marker", "pymupdf"]),
    default="auto",
    help="Conversion engine. Auto-detects by default.",
)
@click.option(
    "--pages",
    type=str,
    default=None,
    help="Page range to convert, e.g. '1-10' or '1,3,5-7'.",
)
@click.option(
    "--no-images",
    is_flag=True,
    default=False,
    help="Skip image extraction.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    default=False,
    help="Recursively process directories.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose logging.",
)
@click.version_option(package_name="pdf-to-md")
def cli(
    input_path: Path,
    output: Path | None,
    engine: str,
    pages: str | None,
    no_images: bool,
    recursive: bool,
    verbose: bool,
) -> None:
    """Convert PDF files to Markdown.

    INPUT_PATH can be a single PDF file or a directory of PDFs.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    config = load_config(
        input_path=input_path,
        output_dir=output,
        engine=engine,
        pages=pages,
        extract_images=not no_images,
        recursive=recursive,
    )

    converter = Converter(config)

    if input_path.is_file():
        result = converter.convert_file(input_path)
        console.print(f"[green]✓[/green] Converted: {result.output_path}")
    elif input_path.is_dir():
        results = converter.convert_directory(input_path)
        console.print(f"[green]✓[/green] Converted {len(results)} files.")
    else:
        raise click.ClickException(f"Unsupported input type: {input_path}")


if __name__ == "__main__":
    cli()
