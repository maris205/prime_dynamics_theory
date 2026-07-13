#!/usr/bin/env python3
"""Generate the deterministic small-box reference grid for Paper 12.

The checked-in CSV is a definition and regression artifact, not a scale study.
Every row is obtained by complete finite enumeration and full finite SVD.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from reference_kernel import (
    DEFAULT_SEED,
    INTERPRETATION_WARNING,
    BoxSpec,
    analyze_small_box,
)
from shift_completion_reference import default_theorem_4_3_certificate


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "data" / "reference-grid.csv"
DEFAULT_CERTIFICATE_OUTPUT = HERE / "data" / "theorem-4.3-certificate.json"
SCHEMA_VERSION = 1


@dataclass(frozen=True)
class GridCase:
    case_id: str
    spec: BoxSpec


# The first four cases have exactly the same ambient box and base modulus.
# They expose the distinction between the fixed unit support and the
# shift-dependent active prime set.  The last case is a complete F_5^x period.
REFERENCE_GRID: tuple[GridCase, ...] = (
    GridCase("base-h2", BoxSpec(101, 30, 151, 28, 2, 13, 2)),
    GridCase("base-h6", BoxSpec(101, 30, 151, 28, 2, 13, 6)),
    GridCase("base-h30", BoxSpec(101, 30, 151, 28, 2, 13, 30)),
    GridCase("base-h-minus6", BoxSpec(101, 30, 151, 28, 2, 13, -6)),
    GridCase("translated-h2", BoxSpec(317, 31, 509, 29, 3, 19, 2)),
    GridCase("translated-h10", BoxSpec(317, 31, 509, 29, 3, 19, 10)),
    GridCase("complete-p5", BoxSpec(1, 4, 1, 4, 3, 5, 2)),
)


FIELDNAMES: tuple[str, ...] = (
    "schema_version",
    "case_id",
    "reference_seed",
    "m_start",
    "m_length",
    "n_start",
    "n_length",
    "w",
    "y",
    "h",
    "base_primes",
    "active_primes",
    "inactive_prime_divisors_of_h",
    "kappa_exact",
    "survivor_rows",
    "survivor_columns",
    "allowed_kernel_entries",
    "raw_centered_sum_exact",
    "raw_interval_normalized_exact",
    "raw_interval_normalized_float",
    "survivor_normalized_exact",
    "survivor_normalized_float",
    "raw_interval_operator_normalization",
    "survivor_operator_normalization",
    "survivor_double_centered_operator_normalization",
    "exact_zero_margins",
    "two_constructions_agree",
)


def format_float(value: float) -> str:
    """Suppress irrelevant last-bit differences between LAPACK backends."""

    return format(value, ".12g")


def _prime_text(values: Sequence[int]) -> str:
    return ";".join(str(value) for value in values)


def grid_row(case: GridCase) -> dict[str, Any]:
    report = analyze_small_box(case.spec)
    local = report["local_data"]
    support = report["support"]
    raw = report["raw_centered_sum"]
    svd = report["svd"]
    double = report["double_centering"]
    validation = report["validation"]
    base_primes = tuple(local["primes"])
    active_primes = tuple(local["active_primes_excluding_divisors_of_h"])
    active_set = set(active_primes)
    inactive = tuple(p for p in base_primes if p not in active_set)

    return {
        "schema_version": SCHEMA_VERSION,
        "case_id": case.case_id,
        "reference_seed": DEFAULT_SEED,
        "m_start": case.spec.m_start,
        "m_length": case.spec.m_length,
        "n_start": case.spec.n_start,
        "n_length": case.spec.n_length,
        "w": case.spec.w,
        "y": case.spec.y,
        "h": case.spec.h,
        "base_primes": _prime_text(base_primes),
        "active_primes": _prime_text(active_primes),
        "inactive_prime_divisors_of_h": _prime_text(inactive),
        "kappa_exact": local["kappa_exact"],
        "survivor_rows": support["survivor_rows"],
        "survivor_columns": support["survivor_columns"],
        "allowed_kernel_entries": support["allowed_kernel_entries"],
        "raw_centered_sum_exact": raw["exact"],
        "raw_interval_normalized_exact": raw[
            "raw_interval_normalized_exact"
        ],
        "raw_interval_normalized_float": format_float(
            raw["raw_interval_normalized_float"]
        ),
        "survivor_normalized_exact": raw["survivor_normalized_exact"],
        "survivor_normalized_float": format_float(
            raw["survivor_normalized_float"]
        ),
        "raw_interval_operator_normalization": format_float(
            svd["raw_interval_operator_normalization"]
        ),
        "survivor_operator_normalization": format_float(
            svd["survivor_operator_normalization"]
        ),
        "survivor_double_centered_operator_normalization": format_float(
            svd["survivor_double_centered_operator_normalization"]
        ),
        "exact_zero_margins": str(
            bool(double["exact_zero_row_and_column_sums"])
        ).lower(),
        "two_constructions_agree": str(
            bool(validation["prime_loop_equals_direct_active_modulus"])
        ).lower(),
    }


def render_reference_grid() -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for case in REFERENCE_GRID:
        writer.writerow(grid_row(case))
    return output.getvalue()


def render_theorem_4_3_certificate() -> str:
    payload = default_theorem_4_3_certificate().as_dict()
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or check the deterministic Paper 12 reference grid."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"CSV destination (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--certificate-output",
        type=Path,
        default=DEFAULT_CERTIFICATE_OUTPUT,
        help=f"theorem certificate destination (default: {DEFAULT_CERTIFICATE_OUTPUT})",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare generated bytes with the existing output instead of writing",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    rendered = render_reference_grid()
    rendered_certificate = render_theorem_4_3_certificate()
    print(f"WARNING: {INTERPRETATION_WARNING}", file=sys.stderr)

    if args.check:
        missing = [
            path for path in (args.output, args.certificate_output) if not path.exists()
        ]
        if missing:
            print(
                "error: checked data product is missing: "
                + ", ".join(str(path) for path in missing),
                file=sys.stderr,
            )
            return 2
        existing = args.output.read_text(encoding="utf-8")
        existing_certificate = args.certificate_output.read_text(encoding="utf-8")
        if existing != rendered or existing_certificate != rendered_certificate:
            print(
                "error: a checked data product differs from regeneration: "
                f"{args.output}, {args.certificate_output}",
                file=sys.stderr,
            )
            return 1
        print(
            "reference products match "
            f"{args.output} and {args.certificate_output} "
            f"({len(REFERENCE_GRID)} grid rows)",
            file=sys.stderr,
        )
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8", newline="")
    args.certificate_output.parent.mkdir(parents=True, exist_ok=True)
    args.certificate_output.write_text(
        rendered_certificate, encoding="utf-8", newline=""
    )
    print(
        f"wrote {args.output} ({len(REFERENCE_GRID)} rows) and "
        f"{args.certificate_output}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
