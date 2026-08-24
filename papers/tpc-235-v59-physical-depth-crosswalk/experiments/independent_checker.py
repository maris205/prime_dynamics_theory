#!/usr/bin/env python3
"""Independent exact-fraction reconstruction for TPC-235."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "results" / "certificate.json").read_text(encoding="utf-8"))
    floor_record = {
        "Q": 10, "H": 63, "h": 21, "q": 17, "m": 5,
        "lambda": str(Fraction(21 * 10, 63)),
        "physical_cutoff": (21 * 17) // 63,
        "depth_cutoff": int(Fraction(21 * 10, 63) * 17 / 10),
        "profile_argument": str(Fraction(63 * 5, 21 * 17)),
        "modulus_matched_model_depth": str(Fraction(21, 40)),
        "modulus_matched_model_cutoff": int(Fraction(21, 40) * 17 / 10),
    }
    surrogate = {"Q": 25, "L": 4, "H": 2500, "h": 400, "rows": [{"q": 37, "cutoff": 5}, {"q": 47, "cutoff": 7}], "compatible": True}
    exponents = {"Q": "1/3", "H": "21/32", "U": "133/400", "Q2_over_H": "1/96", "H_over_Q": "31/96", "UQ_over_H": "23/2400"}
    raw = (9, 5, 1, 5)
    polarization = {
        "beta": 1, "w": 2,
        "raw_packet_squared_norms": list(raw),
        "raw_polarized_value": [str(Fraction(raw[0] - raw[2], 4)), str(Fraction(raw[1] - raw[3], 4))],
        "unit_output_squared_norms": [1, 1, 1, 1],
        "unit_output_polarized_value": ["0", "0"],
        "target_cross_term": ["2", "0"],
    }
    records = {"floor_profile": floor_record, "surrogate": surrogate, "exponents": exponents, "polarization": polarization}
    if records != payload["finite_reproduction"]["records"]:
        raise SystemExit("TPC235 independent records mismatch")
    digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if digest != payload["finite_reproduction"]["digest"]:
        raise SystemExit("TPC235 digest mismatch")
    print("TPC235_INDEPENDENT_CHECK=PASS")
    print("physical_depth=10/3")
    print("polarization=2_TO_0_UNDER_OUTPUT_NORMALIZATION")


if __name__ == "__main__":
    main()
