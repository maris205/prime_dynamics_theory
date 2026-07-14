#!/usr/bin/env python3
"""Zero-dependency tests for the exact TPC-9 certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from exact_zero_mellin_certificate import (
    build_certificate,
    canonical_json_bytes,
    direct_expression,
    collapsed_expression,
    euler_factor_checks,
    verify_divisor_identity,
    verify_target_reindexing,
)


HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "data" / "exact-zero-mellin-certificate.json"


def test_divisor_identity() -> None:
    assert verify_divisor_identity(1, 500)


def test_direct_and_collapsed_expressions() -> None:
    for h in (-4, -1, 1, 2, 6):
        assert direct_expression(50, 350, h) == collapsed_expression(50, 350, h)


def test_small_large_split() -> None:
    full = direct_expression(100, 400, 2)
    small = direct_expression(100, 400, 2, lambda n: n <= 17)
    large = direct_expression(100, 400, 2, lambda n: n > 17)
    combined = dict(small)
    for key, value in large.items():
        combined[key] = combined.get(key, 0) + value
        if combined[key] == 0:
            del combined[key]
    assert combined == full


def test_target_reindexing() -> None:
    for h in (-3, 2, 7):
        for d in range(1, 40):
            assert verify_target_reindexing(100, 500, h, d)


def test_local_euler_factors() -> None:
    for h in (1, 2, 6, 30):
        assert all(row["equal"] for row in euler_factor_checks(43, h))


def test_zero_shift_rejected() -> None:
    try:
        build_certificate(h=0)
    except ValueError:
        return
    raise AssertionError("h=0 must be rejected")


def test_reference_certificate() -> None:
    expected = build_certificate()
    actual = json.loads(REFERENCE.read_text(encoding="ascii"))
    assert actual == expected


def test_canonical_payload_hash() -> None:
    certificate = build_certificate()
    claimed = certificate.pop("canonical_payload_sha256")
    actual = hashlib.sha256(canonical_json_bytes(certificate)).hexdigest().upper()
    assert actual == claimed


def main() -> None:
    tests = [
        test_divisor_identity,
        test_direct_and_collapsed_expressions,
        test_small_large_split,
        test_target_reindexing,
        test_local_euler_factors,
        test_zero_shift_rejected,
        test_reference_certificate,
        test_canonical_payload_hash,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    main()
