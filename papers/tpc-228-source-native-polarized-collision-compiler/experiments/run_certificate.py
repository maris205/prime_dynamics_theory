#!/usr/bin/env python3
"""Build or verify the exact TPC-228 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))
from source_native_compiler import CompilerFailure, build_certificate  # noqa: E402

OUTPUT = PROJECT / "results/certificate.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        text = json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n"
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text() != text:
                raise CompilerFailure("committed certificate differs from exact rebuild")
        else:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(text)
    except (OSError, ValueError, CompilerFailure) as error:
        print(f"TPC228_CERTIFICATE=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC228_CERTIFICATE=PASS")
    print("q25_source_fixtures=5")
    print("general_graph_controls=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
