#!/usr/bin/env python3
"""Produce or read-only verify the TPC-224 exact certificate."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CODE = PROJECT / "code"
sys.path.insert(0, str(CODE))

from literal_compatibility import build_certificate  # noqa: E402


OUTPUT = PROJECT / "results" / "certificate.json"


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def main() -> int:
    expected = build_certificate()
    if "--check" in sys.argv:
        observed = json.loads(OUTPUT.read_text())
        if observed != expected:
            print("TPC224_CERTIFICATE=FAIL: stored certificate differs", file=sys.stderr)
            return 1
        print("TPC224_CERTIFICATE=PASS")
    else:
        OUTPUT.write_text(canonical(expected))
        print("TPC224_CERTIFICATE=WRITTEN")
    source = expected["source_clock"]["records"]
    stress = expected["collision_stress_clock"]["records"]
    print(f"source_scales={len(source)}")
    print(f"stress_scales={len(stress)}")
    print("sharp_constant=PJ/(P+J)")
    print("unit_interface=REFUTED_SCOPED")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
