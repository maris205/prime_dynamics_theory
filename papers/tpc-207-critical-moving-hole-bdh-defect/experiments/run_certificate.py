#!/usr/bin/env python3
"""Write or verify the canonical TPC-207 exact certificate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from moving_hole import build_certificate  # noqa: E402

CERTIFICATE = PROJECT / "results" / "certificate.json"


def reject_nonfinite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite float in certificate")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise TypeError("JSON object key is not a string")
            reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            reject_nonfinite(child)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise TypeError(f"non-JSON value: {type(value).__name__}")


def canonical_text(value: object) -> str:
    reject_nonfinite(value)
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = canonical_text(build_certificate())
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(expected, encoding="utf-8")
        print("TPC207_CERTIFICATE_WRITE=PASS")
        print(f"path={CERTIFICATE.relative_to(PROJECT)}")
        return 0

    if not CERTIFICATE.is_file():
        print("TPC207_CERTIFICATE_CHECK=FAIL missing certificate", file=sys.stderr)
        return 1
    actual = CERTIFICATE.read_text(encoding="utf-8")
    parsed = json.loads(actual, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    reject_nonfinite(parsed)
    if actual != expected:
        print("TPC207_CERTIFICATE_CHECK=FAIL noncanonical or stale certificate", file=sys.stderr)
        return 1
    print("TPC207_CERTIFICATE_CHECK=PASS")
    print("q_rows=2,3,5,7")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
