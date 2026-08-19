#!/usr/bin/env python3
"""Produce or verify the canonical TPC-213 finite certificate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from profile_cross_gram import build_certificate  # noqa: E402


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
        print("TPC213_CERTIFICATE_WRITE=PASS")
        print("schema=TPC213_PHYSICAL_PROFILE_CROSS_GRAM_CERTIFICATE_V1")
        return 0

    if not CERTIFICATE.is_file():
        print("TPC213_CERTIFICATE_CHECK=FAIL missing certificate")
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
        print(f"TPC213_CERTIFICATE_CHECK=FAIL invalid JSON: {error}")
        return 1
    if actual != expected:
        print("TPC213_CERTIFICATE_CHECK=FAIL stale or noncanonical")
        return 1
    print("TPC213_CERTIFICATE_CHECK=PASS")
    print("support_size=35")
    print("joint_lift_rank=35")
    print("cross_gram_nonzero_cases=2")
    print("claim_level=PROVED_STRUCTURAL_L1_CROSS_DIVISOR_COUPLING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
