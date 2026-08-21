"""Small command-line utilities for project artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .cdli import CDLIClient
from .cdli_manifest import verify_manifest
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


def _verify_cdli(
    path: Path,
    output: Path,
    *,
    base_url: str,
    timeout: float,
    limit: int | None,
) -> int:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be a JSON object")
        verified = verify_manifest(
            manifest,
            CDLIClient(base_url=base_url, timeout=timeout),
            limit=limit,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(verified, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"verification failed: {exc}")
        return 1

    run = verified["verification_run"]
    print(
        "verified CDLI manifest: "
        f"attempted={run['attempted']} resolved={run['resolved']} errors={run['errors']} "
        f"output={output}"
    )
    return 0 if run["errors"] == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ane-context")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate the core references in a Context Package"
    )
    validate_parser.add_argument("path", type=Path)

    cdli_parser = subparsers.add_parser(
        "verify-cdli", help="resolve CDLI metadata for source-pack candidates"
    )
    cdli_parser.add_argument("path", type=Path, help="candidate manifest JSON")
    cdli_parser.add_argument("--output", "-o", type=Path, required=True)
    cdli_parser.add_argument("--base-url", default="https://cdli.earth/")
    cdli_parser.add_argument("--timeout", type=float, default=20.0)
    cdli_parser.add_argument("--limit", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        return _validate(args.path)
    if args.command == "verify-cdli":
        return _verify_cdli(
            args.path,
            args.output,
            base_url=args.base_url,
            timeout=args.timeout,
            limit=args.limit,
        )
    return 2
