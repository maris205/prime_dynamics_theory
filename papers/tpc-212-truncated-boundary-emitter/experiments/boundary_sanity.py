#!/usr/bin/env python3
"""Small human-readable sanity report for the TPC-212 finite fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from boundary_emitter import boundary_identity_case, emitter_case  # noqa: E402


def main() -> int:
    boundary = boundary_identity_case((5, 7), 5, 35)
    emitter = emitter_case((7, 35), (2, 3, 13), 10)
    print("TPC212_BOUNDARY_SANITY=PASS")
    print(f"active_divisors={boundary['active_divisors']}")
    print(f"endpoint_incidence={boundary['active_endpoint_incidence']}")
    print(f"emitter_norms={emitter['emitter_norm_squared']}")
    print(f"alignment_ratio={emitter['coherent_to_diagonal_ratio']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
