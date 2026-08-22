#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from collision_schur import build_certificate  # noqa: E402

OUT = ROOT / "results" / "certificate.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build_certificate()
    if args.check:
        if json.loads(OUT.read_text()) != expected:
            raise SystemExit("TPC221 certificate mismatch")
    else:
        OUT.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    print("TPC221_CERTIFICATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
