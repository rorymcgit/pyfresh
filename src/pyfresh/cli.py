"""Command-line interface for the Python Project Generator."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .generator import PyfreshProjectGenerator
from .config import Config


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate Python project structures with configurable templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-project                    # Interactive mode
  %(prog)s my-project --author "John Doe" --email "john@example.com"
  %(prog)s my-project --template minimal --tool uv
  %(prog)s my-project --config my-config.yaml
        """
    )

    parser.add_argument(
        "project_name",
        help="Name of the project to create"
    )

    parser.add_argument(
        "--author",
        help="Project author name (default: from config or prompt)"
    )

    parser.add_argument(
        "--email",
        help="Project author email (default: from config or prompt)"
    )

    parser.add_argument(
        "--description",
        help="Project description (default: empty)"
    )

    parser.add_argument(
        "--template",
        choices=["standard", "minimal", "cli", "web"],
        default="standard",
        help="Project template to use (default: standard)"
    )

    parser.add_argument(
        "--tool",
        choices=["poetry", "uv"],
        default="poetry",
        help="Dependency management tool (default: poetry)"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Output directory for the project (default: current directory)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing project directory"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating files"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Load configuration
        config = Config.load(args.config)

        # Create generator
        generator = PyfreshProjectGenerator(config)

        # Generate project
        success = generator.generate(
            project_name=args.project_name,
            author=args.author,
            email=args.email,
            description=args.description,
            template=args.template,
            tool=args.tool,
            output_dir=args.output_dir,
            force=args.force,
            dry_run=args.dry_run
        )

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
