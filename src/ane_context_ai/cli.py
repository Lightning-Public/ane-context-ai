"""Small command-line utilities for project artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .cdli import CDLIClient
from .cdli_manifest import verify_manifest
from .learning_view import build_learning_view
from .review import (
    validate_context_promotion,
    validate_review_record,
    validate_source_pack_promotions,
)
from .validation import ValidationError, validate_context_package


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _load_review_records(paths: list[Path]) -> list[dict[str, Any]]:
    return [_load_object(path) for path in paths]


def _validate(path: Path) -> int:
    try:
        validate_context_package(_load_object(path))
    except (OSError, json.JSONDecodeError, ValueError, ValidationError) as exc:
        print(f"invalid: {exc}")
        return 1

    print(f"valid: {path}")
    return 0


def _validate_review(path: Path) -> int:
    try:
        validate_review_record(_load_object(path))
    except (OSError, json.JSONDecodeError, ValueError, ValidationError) as exc:
        print(f"invalid review record: {exc}")
        return 1

    print(f"valid review record: {path}")
    return 0


def _validate_promotion(path: Path, review_paths: list[Path]) -> int:
    try:
        package = _load_object(path)
        records = _load_review_records(review_paths)
        validate_context_promotion(package, records)
    except (OSError, json.JSONDecodeError, ValueError, ValidationError) as exc:
        print(f"invalid promotion: {exc}")
        return 1

    print(
        f"valid context promotion: package={path} review_records={len(review_paths)}"
    )
    return 0


def _validate_source_pack(path: Path, review_paths: list[Path]) -> int:
    try:
        manifest = _load_object(path)
        records = _load_review_records(review_paths)
        validate_source_pack_promotions(manifest, records)
    except (OSError, json.JSONDecodeError, ValueError, ValidationError) as exc:
        print(f"invalid source-pack promotion: {exc}")
        return 1

    print(
        f"valid source-pack promotions: manifest={path} review_records={len(review_paths)}"
    )
    return 0


def _build_learning_view(path: Path, output: Path) -> int:
    try:
        view = build_learning_view(_load_object(path))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(view, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError, ValidationError) as exc:
        print(f"learning view build failed: {exc}")
        return 1

    print(f"built learning view: source={path} output={output}")
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
        manifest = _load_object(path)
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


def _add_review_record_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--review-record",
        action="append",
        dest="review_records",
        type=Path,
        default=[],
        required=True,
        help="machine-readable review record JSON; repeat for multiple records",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ane-context")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate the core references in a Context Package"
    )
    validate_parser.add_argument("path", type=Path)

    review_parser = subparsers.add_parser(
        "validate-review", help="validate a machine-readable review record"
    )
    review_parser.add_argument("path", type=Path)

    promotion_parser = subparsers.add_parser(
        "validate-promotion",
        help="validate human-review evidence for a promoted Context Package",
    )
    promotion_parser.add_argument("path", type=Path)
    _add_review_record_args(promotion_parser)

    source_pack_parser = subparsers.add_parser(
        "validate-source-pack",
        help="validate human-review evidence for verified source-pack artifacts",
    )
    source_pack_parser.add_argument("path", type=Path)
    _add_review_record_args(source_pack_parser)

    learning_parser = subparsers.add_parser(
        "build-learning-view",
        help="build a beginner-facing view model from a Context Package",
    )
    learning_parser.add_argument("path", type=Path)
    learning_parser.add_argument("--output", "-o", type=Path, required=True)

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
    if args.command == "validate-review":
        return _validate_review(args.path)
    if args.command == "validate-promotion":
        return _validate_promotion(args.path, args.review_records)
    if args.command == "validate-source-pack":
        return _validate_source_pack(args.path, args.review_records)
    if args.command == "build-learning-view":
        return _build_learning_view(args.path, args.output)
    if args.command == "verify-cdli":
        return _verify_cdli(
            args.path,
            args.output,
            base_url=args.base_url,
            timeout=args.timeout,
            limit=args.limit,
        )
    return 2
