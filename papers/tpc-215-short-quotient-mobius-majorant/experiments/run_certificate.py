#!/usr/bin/env python3
"""Materialize or check the deterministic TPC-215 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from short_quotient_majorant import AuditFailure, build_certificate  # noqa: E402


CERTIFICATE = ROOT / "results/certificate.json"


def canonical(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected = canonical(build_certificate())
        if args.check:
            if not CERTIFICATE.is_file():
                raise AuditFailure("certificate missing")
            if CERTIFICATE.read_text(encoding="utf-8") != expected:
                raise AuditFailure("certificate is stale")
        else:
            CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
            CERTIFICATE.write_text(expected, encoding="utf-8")
    except (AuditFailure, OSError, ValueError, ZeroDivisionError) as error:
        print(f"TPC215_CERTIFICATE=FAIL {error}", file=sys.stderr)
        return 1
    data = json.loads(expected)
    fixture = data["finite_fixture"]
    print("TPC215_CERTIFICATE=PASS")
    print("active_denominators=", len(fixture["active_denominators"]))
    print("activation_floor=", fixture["activation_floor"])
    print("actual_max_quotient=", fixture["actual_max_quotient"])
    print("global_ratio=", fixture["cluster_to_direct_ratio"])
    print("claim_level=PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
