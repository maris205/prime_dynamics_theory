#!/usr/bin/env python3
"""Materialize or check the canonical TPC-217 finite-window certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from finite_window_attachment import AuditFailure, build_fixture  # noqa: E402


CERTIFICATE = ROOT / "results/certificate.json"


def canonical(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected = canonical(build_fixture())
        if args.check:
            if not CERTIFICATE.is_file():
                raise AuditFailure("certificate missing")
            if CERTIFICATE.read_text(encoding="utf-8") != expected:
                raise AuditFailure("certificate is stale")
        else:
            CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
            CERTIFICATE.write_text(expected, encoding="utf-8")
    except (AuditFailure, OSError, ValueError, ZeroDivisionError) as error:
        print(f"TPC217_CERTIFICATE=FAIL {error}", file=sys.stderr)
        return 1
    data = json.loads(expected)
    fixture = data["finite_fixture"]
    adversary = data["frequency_crowding_adversary"]
    print("TPC217_CERTIFICATE=PASS")
    print("active_divisors=", len(fixture["divisors"]))
    print("reduced_denominators=", len(fixture["reduced_denominators"]))
    print("intervals=", len(fixture["intervals"]))
    print("crowding_ratio=", adversary["window_to_diagonal_ratio"])
    print("normalized_exponent=11/32")
    print("claim_level=PROVED_STRUCTURAL_L1_FINITE_WINDOW_ATTACHMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
