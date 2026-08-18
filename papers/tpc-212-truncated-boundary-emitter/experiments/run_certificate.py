#!/usr/bin/env python3
"""Produce or verify the canonical TPC-212 finite certificate."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from boundary_emitter import build_certificate  # noqa: E402


CERTIFICATE = PROJECT / "results" / "certificate.json"


def canonical_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def reject_nonfinite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite float")
    if isinstance(value, dict):
        for key, child in value.items():
            if type(key) is not str:
                raise TypeError("non-string JSON key")
            reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            reject_nonfinite(child)
    elif value is not None and type(value) not in (str, int, float, bool):
        raise TypeError(f"non-JSON value: {type(value).__name__}")


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = canonical_text(build_certificate())
    if args.write:
        CERTIFICATE.write_text(expected, encoding="utf-8")
        print("TPC212_CERTIFICATE_WRITE=PASS")
        print("schema=TPC212_TRUNCATED_BOUNDARY_EMITTER_CERTIFICATE_V1")
        return 0

    if not CERTIFICATE.is_file():
        print("TPC212_CERTIFICATE_CHECK=FAIL missing certificate")
        return 1
    actual = CERTIFICATE.read_text(encoding="utf-8")
    try:
        parsed = json.loads(
            actual,
            object_pairs_hook=unique_object,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
        reject_nonfinite(parsed)
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"TPC212_CERTIFICATE_CHECK=FAIL invalid JSON: {error}")
        return 1
    if actual != expected:
        print("TPC212_CERTIFICATE_CHECK=FAIL stale or noncanonical")
        return 1
    print("TPC212_CERTIFICATE_CHECK=PASS")
    print("boundary_cases=4")
    print("emitter_cases=3")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED_BOUNDARY_EMITTER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
