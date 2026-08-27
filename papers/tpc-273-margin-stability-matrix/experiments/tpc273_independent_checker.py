#!/usr/bin/env python3
"""Independent replay of the TPC-273 finite margin-stability matrix."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-273-margin-stability-matrix"
RESULT = PROJECT / "results/tpc273_certificate.json"
PARENT = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json"
PARENT_SHA = "890167856037b7c1c0356ffa40bfe5f98e3f6974ff14ca3ef7e248682d220f4a"
ENGINE_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION"

spec = importlib.util.spec_from_file_location("tpc268_engine_independent", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("upstream engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def f(value: object) -> Fraction:
    return Fraction(str(value))


def bounds(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = f(value[0]), f(value[1])
    need(0 < lo <= hi, "positive interval")
    return lo, hi


def qtext(value: tuple[Fraction, Fraction]) -> list[str]:
    return [f"{value[0].numerator}/{value[0].denominator}",
            f"{value[1].numerator}/{value[1].denominator}"]


def quotient(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return a[0] / b[1], a[1] / b[0]


def load(path: Path) -> dict:
    raw = path.read_bytes()
    data = json.loads(raw)
    canonical = (json.dumps(data, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "noncanonical JSON: " + path.name)
    return data


def classify(m2: tuple[Fraction, Fraction]) -> str:
    if m2[1] < Fraction(1, 64):
        return "MARGIN_BELOW_ONE_EIGHTH"
    if m2[0] > Fraction(1, 16):
        return "MARGIN_ABOVE_ONE_QUARTER"
    return "MARGIN_MIDDLE_BAND"


def check() -> None:
    parent = load(PARENT)
    parent_payload = parent["payload"]
    parent_canonical = (json.dumps(parent_payload, ensure_ascii=True, sort_keys=True,
                                    separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(parent_canonical).hexdigest() == PARENT_SHA,
         "parent provenance")
    data = load(RESULT)
    need(data["claim_status"] == STATUS, "status")
    payload = data["payload"]
    payload_canonical = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(payload_canonical).hexdigest() == data["payload_sha256"],
         "payload digest")
    need(payload["schema"] == "TPC273_MARGIN_STABILITY_CERTIFICATE_V1" and
         payload["parameters"]["upstream_payload_sha256"] == PARENT_SHA,
         "schema/provenance")
    actual = payload["cases"]
    need(len(actual) == 32, "case count")
    counts = {name: 0 for name in ("MARGIN_BELOW_ONE_EIGHTH",
                                   "MARGIN_MIDDLE_BAND",
                                   "MARGIN_ABOVE_ONE_QUARTER")}
    phases = {name: 0 for name in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS",
                                   "CROSSES_ZERO")}
    for row in actual:
        key = (row["scale"], row["H"], row["Q"], row["kernel_exponent"],
               row["comparison_cutoff_z"])
        # Recompute the locked physical row through the released parent
        # engine.  No TPC-273 producer code or result is imported here.
        source = ENGINE.audit_case(row["scale"], row["H"], row["Q"],
                                   row["kernel_exponent"],
                                   row["comparison_cutoff_z"],
                                   "TPC273_INDEPENDENT_REPLAY")
        m2 = bounds(source["rho_squared_interval"])
        need(row["margin_squared_interval"] == qtext(m2), "margin-square replay")
        m6 = (m2[0] ** 3, m2[1] ** 3)
        need(row["margin_sixth_interval"] == qtext(m6), "margin-sixth replay")
        need(row["classification"] == classify(m2) and
             row["phase"] == source["phase"] and
             row["positive_residual_lanes"] is True and
             row["exact_projection_identity"] is True, "row semantics")
        counts[row["classification"]] += 1
        phases[row["phase"]] += 1
    need(counts == {"MARGIN_BELOW_ONE_EIGHTH": 12,
                   "MARGIN_MIDDLE_BAND": 11,
                   "MARGIN_ABOVE_ONE_QUARTER": 9}, "counts")
    need(phases == {"NEGATIVE_REAL_AXIS": 30, "POSITIVE_REAL_AXIS": 2,
                    "CROSSES_ZERO": 0}, "phase census")
    transitions = payload["transitions"]
    need(len(transitions) == 3, "transition count")
    expected = {
        "N64_E1_Z2_TO_Z5": ("MARGIN_MIDDLE_BAND", "MARGIN_ABOVE_ONE_QUARTER"),
        "N128_E1_Z2_TO_Z3": ("MARGIN_MIDDLE_BAND", "MARGIN_BELOW_ONE_EIGHTH"),
        "N96_Z3_E1_TO_E2": ("MARGIN_ABOVE_ONE_QUARTER", "MARGIN_ABOVE_ONE_QUARTER"),
    }
    for item in transitions:
        need(item["label"] in expected and
             (item["low_classification"], item["high_classification"]) ==
             expected[item["label"]], "transition classification")
        need(item["phase_low"] in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS") and
             item["phase_high"] in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS"),
             "transition phase")
    need(payload["finite_theorem"]["status"] == "NUMERICALLY_CERTIFIED_FINITE" and
         payload["firewall"]["TPC273_FIXED_POWER_CREDIT"] == 0 and
         payload["firewall"]["TPC273_SOURCE_LEVEL_MARGIN"] == "OPEN_ASYMPTOTIC" and
         payload["firewall"]["TPC273_FULL_GATE_B"] == "OPEN", "firewall")
    print("TPC273_INDEPENDENT_CHECK=PASS cases=32 low=12 middle=11 high=9 "
          "phase_negative=30 phase_positive=2 cutoff_flips=2 source_margin=OPEN")


if __name__ == "__main__":
    try:
        check()
    except Exception as exc:
        print("TPC273_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
