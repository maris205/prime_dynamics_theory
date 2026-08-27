#!/usr/bin/env python3
"""TPC-273 finite margin-stability matrix on the locked V59 interface."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-273-margin-stability-matrix"
RESULT = PROJECT / "results/tpc273_certificate.json"
UPSTREAM_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"
UPSTREAM_RESULT = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json"
UPSTREAM_PAYLOAD_SHA256 = "890167856037b7c1c0356ffa40bfe5f98e3f6974ff14ca3ef7e248682d220f4a"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION"
ROUND2_CLUE = "TEST_SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF"

spec = importlib.util.spec_from_file_location("tpc268_engine", UPSTREAM_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("upstream engine unavailable")
UPSTREAM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(UPSTREAM)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


Interval = tuple[Fraction, Fraction]


def f(value: object) -> Fraction:
    return Fraction(str(value))


def bounds(value: object, positive: bool = True) -> Interval:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = f(value[0]), f(value[1])
    need(lo <= hi, "interval order")
    if positive:
        need(lo > 0, "positive interval")
    return lo, hi


def cube(value: Fraction) -> Fraction:
    return value * value * value


def cube_interval(value: Interval) -> Interval:
    need(value[0] >= 0, "cube sign")
    return cube(value[0]), cube(value[1])


def exact_interval(value: Interval) -> list[str]:
    return [f"{value[0].numerator}/{value[0].denominator}",
            f"{value[1].numerator}/{value[1].denominator}"]


def load_parent() -> dict[str, Any]:
    raw = UPSTREAM_RESULT.read_bytes()
    data = json.loads(raw)
    need(data.get("payload_sha256") == UPSTREAM_PAYLOAD_SHA256,
         "parent payload provenance")
    payload = data.get("payload")
    need(isinstance(payload, dict), "parent payload")
    canonical = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(canonical).hexdigest() == UPSTREAM_PAYLOAD_SHA256,
         "parent payload digest")
    return data


BASE_ROWS = ((64, 15, 4), (96, 20, 5), (128, 24, 5), (192, 32, 6))
CUTOFFS = (2, 3, 4, 5)
EXPONENTS = (1, 2)


def classification(m2: Interval) -> str:
    low = Fraction(1, 64)
    high = Fraction(1, 16)
    if m2[1] < low:
        return "MARGIN_BELOW_ONE_EIGHTH"
    if m2[0] > high:
        return "MARGIN_ABOVE_ONE_QUARTER"
    return "MARGIN_MIDDLE_BAND"


def case_record(scale: int, height: int, q0: int, exponent: int,
                cutoff: int) -> dict[str, Any]:
    row = UPSTREAM.audit_case(scale, height, q0, exponent, cutoff,
                              "TPC273_GRID")
    m2 = bounds(row["rho_squared_interval"])
    m6 = cube_interval(m2)
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "kernel_exponent": exponent,
        "comparison_cutoff_z": cutoff,
        "role": "DECLARED_CUTOFF_KERNEL_GRID",
        "margin_squared_interval": exact_interval(m2),
        "margin_sixth_interval": exact_interval(m6),
        "phase": row["phase"],
        "classification": classification(m2),
        "residual_scalar_interval": row["residual_scalar_interval"],
        "radius_squared_interval": row["radius_squared_interval"],
        "positive_residual_lanes": True,
        "exact_projection_identity": True,
        "parent_schema": "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1",
    }


def transition_record(low: dict[str, Any], high: dict[str, Any],
                      label: str, perturbation: str) -> dict[str, Any]:
    a = bounds(low["margin_squared_interval"])
    b = bounds(high["margin_squared_interval"])
    ratio = (b[0] / a[1], b[1] / a[0])
    return {
        "label": label,
        "perturbation": perturbation,
        "low_case": [low["scale"], low["comparison_cutoff_z"], low["kernel_exponent"]],
        "high_case": [high["scale"], high["comparison_cutoff_z"], high["kernel_exponent"]],
        "margin_squared_ratio_interval": exact_interval(ratio),
        "low_classification": low["classification"],
        "high_classification": high["classification"],
        "phase_low": low["phase"],
        "phase_high": high["phase"],
    }


def build_payload() -> dict[str, Any]:
    parent = load_parent()
    cases = [case_record(n, h, q, e, z)
             for n, h, q in BASE_ROWS
             for z in CUTOFFS
             for e in EXPONENTS]
    counts = {name: sum(row["classification"] == name for row in cases)
              for name in ("MARGIN_BELOW_ONE_EIGHTH", "MARGIN_MIDDLE_BAND",
                           "MARGIN_ABOVE_ONE_QUARTER")}
    phase_counts = {name: sum(row["phase"] == name for row in cases)
                    for name in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS",
                                 "CROSSES_ZERO")}
    by_key = {(r["scale"], r["comparison_cutoff_z"], r["kernel_exponent"]): r
              for r in cases}
    transitions = [
        transition_record(by_key[(64, 2, 1)], by_key[(64, 5, 1)],
                          "N64_E1_Z2_TO_Z5", "cutoff-only"),
        transition_record(by_key[(128, 2, 1)], by_key[(128, 3, 1)],
                          "N128_E1_Z2_TO_Z3", "cutoff-only"),
        transition_record(by_key[(96, 3, 1)], by_key[(96, 3, 2)],
                          "N96_Z3_E1_TO_E2", "kernel-only"),
    ]
    need(counts == {"MARGIN_BELOW_ONE_EIGHTH": 12,
                   "MARGIN_MIDDLE_BAND": 11,
                   "MARGIN_ABOVE_ONE_QUARTER": 9}, "classification counts")
    need(phase_counts == {"NEGATIVE_REAL_AXIS": 30,
                          "POSITIVE_REAL_AXIS": 2,
                          "CROSSES_ZERO": 0}, "phase counts")
    need(transitions[0]["low_classification"] == "MARGIN_MIDDLE_BAND" and
         transitions[0]["high_classification"] == "MARGIN_ABOVE_ONE_QUARTER",
         "N64 cutoff flip")
    need(transitions[1]["low_classification"] == "MARGIN_MIDDLE_BAND" and
         transitions[1]["high_classification"] == "MARGIN_BELOW_ONE_EIGHTH",
         "N128 cutoff flip")
    return {
        "schema": "TPC273_MARGIN_STABILITY_CERTIFICATE_V1",
        "parameters": {
            "upstream_schema": "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1",
            "upstream_payload_sha256": UPSTREAM_PAYLOAD_SHA256,
            "operator": "TPC267 literal V59 finite operator",
            "registered_scales": [64, 96, 128, 192],
            "cutoff_grid": [2, 3, 4, 5],
            "kernel_exponents": [1, 2],
            "margin_squared_thresholds": {
                "low": "1/64",
                "high": "1/16",
            },
            "interpretation": "m^2=rho^2 on positive residual rows",
        },
        "finite_theorem": {
            "total_cases": len(cases),
            "low_margin_cases": counts["MARGIN_BELOW_ONE_EIGHTH"],
            "middle_margin_cases": counts["MARGIN_MIDDLE_BAND"],
            "high_margin_cases": counts["MARGIN_ABOVE_ONE_QUARTER"],
            "negative_phase_cases": phase_counts["NEGATIVE_REAL_AXIS"],
            "positive_phase_cases": phase_counts["POSITIVE_REAL_AXIS"],
            "cutoff_flip_transitions": 2,
            "kernel_transition_records": 1,
            "status": "NUMERICALLY_CERTIFIED_FINITE",
            "claim": "declared finite perturbations cross quantitative margin bands",
        },
        "cases": cases,
        "transitions": transitions,
        "firewall": {
            "TPC273_MARGIN_STABILITY_OBSTRUCTION": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC273_CUTOFF_FLIPS": "NUMERICALLY_CERTIFIED",
            "TPC273_PHASE_FLIP": "NUMERICALLY_CERTIFIED_FINITE_TWO_ROWS",
            "TPC273_SOURCE_LEVEL_MARGIN": "OPEN_ASYMPTOTIC",
            "TPC273_GROWING_UNIFORMITY": "OPEN_ASYMPTOTIC",
            "TPC273_FIXED_POWER_CREDIT": 0,
            "TPC273_ARITHMETIC_ADVANCE": "NO",
            "TPC273_L2": "NONE",
            "TPC273_FULL_GATE_B": "OPEN",
            "TPC273_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC273_TWIN_PRIME_RESULT": "NONE",
            "TPC273_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
        "parent_certificate_status": parent["claim_status"],
    }


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload).encode("ascii")).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(canonical(document()), encoding="utf-8")


def check() -> None:
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    need(stored == document(), "certificate mismatch")
    need(raw == canonical(stored), "certificate canonicality")
    theorem = stored["payload"]["finite_theorem"]
    print("TPC273_CERTIFICATE=PASS "
          f"cases={theorem['total_cases']} low={theorem['low_margin_cases']} "
          f"middle={theorem['middle_margin_cases']} high={theorem['high_margin_cases']} "
          "cutoff_flips=2 phase_positive_rows=2")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC273_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
