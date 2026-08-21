"""Small command-line utilities for project artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .validation import ValidationError, validate_context_package


def _validate(path: Path) -> int:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        validate_context_package(payload)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"invalid: {exc}")
        return 1

    print(f"valid: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ane-context")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser(
        "validate", help="validate the core references in a Context Package"
    )
    validate_parser.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        return _validate(args.path)
    return 2
