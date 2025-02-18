"""Command-line interface for the PDFlex package."""

import argparse
import sys
from pathlib import Path
from typing import List

from rich.console import Console

from pdflex.logger import Logger
from pdflex.merge import merge_pdfs
from pdflex.search import search_numeric_prefixed_pdfs, search_pdfs

console = Console()
logger = Logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description=(
            "PDFlex: A comprehensive PDF processing toolkit. "
            "Merge PDFs by providing paths directly or searching directories."
        )
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Merge command
    merge_parser = subparsers.add_parser(
        "merge",
        help="Merge multiple PDF files into a single document",
        description="Merge multiple PDF files into a single document",
    )
    merge_parser.add_argument(
        "files",
        nargs="+",
        help="List of PDF files to merge, in order",
    )
    merge_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output path for merged PDF",
    )
    merge_parser.add_argument(
        "--landscape",
        action="store_true",
        help="Add separator pages in landscape orientation",
    )

    # Search and merge command
    search_parser = subparsers.add_parser(
        "search",
        help="Search directory for PDFs and merge them",
        description="Search for PDFs in a directory and merge them",
    )
    search_parser.add_argument(
        "directory",
        help="Directory to search for PDF files",
    )
    search_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output path for merged PDF",
    )
    search_parser.add_argument(
        "--prefix",
        default="",
        help="Filter PDFs by filename prefix",
    )
    search_parser.add_argument(
        "--suffix",
        default="",
        help="Filter PDFs by filename suffix",
    )
    search_parser.add_argument(
        "--lecture",
        action="store_true",
        help="Search for PDFs with numeric prefixes (e.g., 1.2_) and merge in order",
    )

    return parser


def validate_pdf_paths(paths: List[str]) -> List[Path]:
    """Validate that all provided paths exist and are PDF files.

    Args:
        paths: List of file paths to validate

    Returns:
        List of validated Path objects

    Raises:
        FileNotFoundError: If a file doesn't exist
        ValueError: If a file is not a PDF
    """
    validated = []
    for path_str in paths:
        path = Path(path_str).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {path}")
        validated.append(path)
    return validated


def merge_command(args: argparse.Namespace) -> int:
    """Handle the merge command.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        pdf_paths = validate_pdf_paths(args.files)
        output_path = Path(args.output)

        if output_path.exists():
            logger.warning(
                f"Output file {output_path} already exists, will be overwritten"
            )

        merge_pdfs(
            pdf_paths=[str(p) for p in pdf_paths],
            output_path=str(output_path),
            landscape=args.landscape,
        )

        console.print(f"[green]Successfully merged PDFs to {output_path}[/]")
        return 0

    except Exception as e:
        console.print(f"[red]Error merging PDFs: {e}[/]")
        return 1


def search_command(args: argparse.Namespace) -> int:
    """Handle the search command.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        directory = Path(args.directory)
        if not directory.is_dir():
            raise NotADirectoryError(f"Directory not found: {directory}")

        if args.lecture:
            pdf_paths = search_numeric_prefixed_pdfs(str(directory))
            if not pdf_paths:
                console.print(
                    f"[yellow]No numeric-prefixed PDFs found in {directory}[/]"
                )
                return 1
        else:
            pdf_paths = search_pdfs(str(directory), args.prefix, args.suffix)
            if not pdf_paths:
                console.print(
                    f"[yellow]No PDFs found in {directory} "
                    f"(prefix='{args.prefix}', suffix='{args.suffix}')[/]"
                )
                return 1

        merge_pdfs(
            pdf_paths=pdf_paths,
            output_path=args.output,
            landscape=args.lecture,
        )

        console.print(f"[green]Successfully merged PDFs to {args.output}[/]")
        return 0

    except Exception as e:
        console.print(f"[red]Error processing PDFs: {e}[/]")
        return 1


def main() -> int | None:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "merge":
            return merge_command(args)
        elif args.command == "search":
            return search_command(args)
        return 0

    except Exception as e:
        logger.error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
