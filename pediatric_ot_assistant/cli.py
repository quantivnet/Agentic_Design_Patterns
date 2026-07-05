"""Command-line interface.

Exit codes: 0 ok, 1 runtime/API/case-file error, 2 blocking intake
issues, 3 output-file collision, 4 PHI leak detected post-generation.

The document goes to stdout (or -o FILE); all diagnostics go to stderr,
so output can be piped safely.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from . import pipeline
from .client import OTAssistError, OTClient, default_model
from .intake import run_intake
from .models import CaseFile, DocumentType
from .review import findings_as_notes

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_BLOCKING_INTAKE = 2
EXIT_OUTPUT_COLLISION = 3
EXIT_PHI_LEAK = 4

# Seam for tests: monkeypatch this to inject a fake client.
_client_factory = OTClient


def _err(message: str) -> None:
    print(message, file=sys.stderr)


def load_case(path: str) -> CaseFile:
    case_path = Path(path)
    if not case_path.exists():
        raise OTAssistError(f"Case file not found: {path}")
    try:
        data = yaml.safe_load(case_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise OTAssistError(f"Could not parse YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise OTAssistError(f"{path} does not contain a case-file mapping.")
    try:
        return CaseFile.model_validate(data)
    except ValidationError as exc:
        raise OTAssistError(f"Invalid case file {path}:\n{exc}") from exc


def _print_intake(report, header: str = "Intake findings:") -> None:
    if not report.issues:
        return
    _err(header)
    for issue in report.issues:
        _err(f"  [{issue.severity}] {issue.field}: {issue.message}")


def cmd_generate(args: argparse.Namespace) -> int:
    out_path = Path(args.output) if args.output else None
    if out_path and out_path.exists() and not args.force:
        _err(f"refusing to overwrite {out_path} (use --force)")
        return EXIT_OUTPUT_COLLISION

    case = load_case(args.case)
    doc_type = DocumentType(args.format)

    result = pipeline.run(
        case,
        doc_type,
        client=_client_factory(),
        model=args.model,
        redact=args.redact,
        allow_missing=args.allow_missing,
        deep=args.deep_intake,
        do_review=not args.no_review,
        verbose=args.verbose,
    )

    _print_intake(result.intake)
    if result.token_map:
        _err("Redaction map (placeholders in the document; NOT written to output):")
        for token, placeholder in sorted(result.token_map.items()):
            _err(f"  {placeholder} <- {token}")
    if result.review is not None:
        if result.review.findings:
            _err("Reviewer findings:")
            _err(findings_as_notes(result.review))
        else:
            _err("Reviewer: no findings.")
    for warning in result.warnings:
        _err(f"Warning: {warning}")

    document = result.document if result.document.endswith("\n") else result.document + "\n"
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(document, encoding="utf-8")
        _err(f"Wrote {out_path}")
    else:
        print(document, end="")
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    _err(f"Case file OK: {args.case}")

    if args.format:
        report = run_intake(case, DocumentType(args.format))
        _print_intake(report, header=f"Intake findings for '{args.format}':")
        if report.blocking():
            return EXIT_BLOCKING_INTAKE
        if not report.issues:
            _err("No issues found.")
        return EXIT_OK

    for doc_type in DocumentType:
        report = run_intake(case, doc_type)
        blocking, warning = len(report.blocking()), len(report.warnings())
        status = "BLOCKED" if blocking else "ready"
        _err(
            f"  {doc_type.value:<18} {status:<8} "
            f"({blocking} blocking, {warning} warnings)"
        )
    return EXIT_OK


def cmd_formats(_args: argparse.Namespace) -> int:
    for doc_type in DocumentType:
        print(f"{doc_type.value:<18} {doc_type.description}")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ot-assist",
        description=(
            "Drafting assistant for school-based pediatric occupational "
            "therapy documentation. All output is a draft for review by a "
            "licensed OT."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    formats = [d.value for d in DocumentType]

    gen = sub.add_parser("generate", help="Generate a document from a case file")
    gen.add_argument("--case", required=True, help="Path to a YAML case file")
    gen.add_argument("--format", required=True, choices=formats)
    gen.add_argument("-o", "--output", help="Output file (default: stdout)")
    gen.add_argument(
        "--redact",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Override the case file's privacy.redact setting",
    )
    gen.add_argument(
        "--allow-missing",
        action="store_true",
        help="Draft even with blocking gaps (they become flagged warnings)",
    )
    gen.add_argument(
        "--deep-intake",
        action="store_true",
        help="Extra LLM pass for qualitative data gaps (one more API call)",
    )
    gen.add_argument(
        "--no-review",
        action="store_true",
        help="Skip the LLM review/guardrail pass",
    )
    gen.add_argument("--model", default=None, help=f"Model id (default: {default_model()})")
    gen.add_argument("--force", action="store_true", help="Overwrite existing output file")
    gen.add_argument(
        "--verbose", action="store_true", help="Stream generation to stderr live"
    )
    gen.set_defaults(func=cmd_generate)

    val = sub.add_parser(
        "validate", help="Validate a case file and show intake findings (offline)"
    )
    val.add_argument("--case", required=True)
    val.add_argument("--format", choices=formats, default=None)
    val.set_defaults(func=cmd_validate)

    fmt = sub.add_parser("formats", help="List available document types")
    fmt.set_defaults(func=cmd_formats)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except pipeline.BlockingIntakeError as exc:
        _err(str(exc))
        return EXIT_BLOCKING_INTAKE
    except pipeline.PHILeakError as exc:
        _err(str(exc))
        return EXIT_PHI_LEAK
    except OTAssistError as exc:
        _err(str(exc))
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
