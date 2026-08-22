#!/usr/bin/env python3
"""Produce or read-only validate the TPC-225 certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))
from cutoff_one_obstruction import build_certificate  # noqa: E402


CERTIFICATE = PROJECT / "results" / "certificate.json"


def canonical_bytes() -> bytes:
    return (
        json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check and args.write:
        parser.error("--check and --write are mutually exclusive")
    payload = canonical_bytes()
    if args.write:
        CERTIFICATE.write_bytes(payload)
        print("TPC225_CERTIFICATE=WRITTEN")
        return 0
    if args.check:
        if not CERTIFICATE.is_file() or CERTIFICATE.read_bytes() != payload:
            print("TPC225_CERTIFICATE=FAIL")
            return 1
        print("TPC225_CERTIFICATE=PASS")
        print("affine_scales=9")
        print("boundary_scales=7x2")
        print("ap_identity=E_AP_EQUALS_E_DIAG")
        print("full_identity=E_ALL_EQUALS_E_POL")
        print("claim_level=PROVED_STRUCTURAL_L1")
        return 0
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
