#!/usr/bin/env python3
"""Write or check the deterministic TPC-237 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from finite_window_physical_reassembly import build_certificate  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "results" / "certificate.json"
    generated = build_certificate()
    if args.write:
        target.write_text(json.dumps(generated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("TPC237_CERTIFICATE=WRITTEN")
    elif args.check:
        stored = json.loads(target.read_text(encoding="utf-8"))
        if stored != generated:
            raise SystemExit("TPC237_CERTIFICATE=FAIL: certificate mismatch")
        print("TPC237_CERTIFICATE=PASS")
    else:
        print(json.dumps(generated, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
