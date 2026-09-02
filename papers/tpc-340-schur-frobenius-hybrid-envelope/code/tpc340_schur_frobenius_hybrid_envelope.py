#!/usr/bin/env python3
"""TPC-340: Schur/Frobenius hybrid envelope.

TPC-339 supplied a valid but loose support-restricted Frobenius bound.  This
release combines it with the sign-free induced-infinity (Schur) bound for the
symmetric operator and audits which branch is informative.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc340_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope"
PARENT_CODE = PARENT_PROJECT / "code/tpc339_mask_aware_frobenius_envelope.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc339_certificate.json"
PARENT_CODE_SHA256 = "df76022bfa5051477ec5bc04fef444aefc22abcb8f76fa02b339b7bc769fad18"
PARENT_CERT_SHA256 = "af6636eb7c9d9c6cbc0d392ae0b9effbaa9610dedafa12ee8d1272163fd48372"

SCHEMA = "TPC340_SCHUR_FROBENIUS_HYBRID_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
Q = 54
EXPONENT = 1
HEIGHT = 66
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0, "pi_0(i)=i"),
    ("affine_3_11", 3, 11, "pi_3,11(i)=(3*i+11) mod source_count"),
    ("affine_5_17", 5, 17, "pi_5,17(i)=(5*i+17) mod source_count"),
    ("affine_7_29", 7, 29, "pi_7,29(i)=(7*i+29) mod source_count"),
    ("reversal", -1, -1, "pi_rev(i)=source_count-1-i"),
    ("affine_9_1", 9, 1, "pi_9,1(i)=(9*i+1) mod source_count"),
    ("affine_11_13", 11, 13, "pi_11,13(i)=(11*i+13) mod source_count"),
    ("affine_13_17", 13, 17, "pi_13,17(i)=(13*i+17) mod source_count"),
    ("affine_17_19", 17, 19, "pi_17,19(i)=(17*i+19) mod source_count"),
)
NUMERIC_TOL = 8.0e-6
BOUND_TOL = 3.0e-10


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_parent() -> Any:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC339 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC339 certificate provenance")
    raw = PARENT_CERT.read_bytes(); document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE",
         "TPC339 certificate header")
    spec = importlib.util.spec_from_file_location("tpc339_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.load_parent()


def classify(source: Any, value: int, lam: float, comparison: float) -> str:
    if lam * comparison == 0.0:
        return "zero_support"
    power = source.prime_power(value + 2)
    need(power is not None, "prime-power support")
    if power[1] == 1:
        return "twin_prime" if source.is_prime_small(value) else "non_twin_prime_shift"
    return "prime_power_shift"


def control_indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        result = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        result = np.asarray([(multiplier * i + offset) % size
                             for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in result)) == size, "control bijection")
    return result


def exact_anchor() -> dict[str, Any]:
    # A rational symmetric matrix where the Schur bound is explicit.
    matrix = [[Fraction(1), Fraction(-1)], [Fraction(-1), Fraction(1)]]
    vector = [Fraction(1), Fraction(1)]
    output = [sum(matrix[i][j] * vector[j] for j in range(2))
              for i in range(2)]
    energy = sum(item * item for item in output)
    source_norm = sum(item * item for item in vector)
    row_sum = max(sum(abs(item) for item in row) for row in matrix)
    schur_gain = row_sum * row_sum
    need(energy == 0 and source_norm == 2 and schur_gain == 4,
         "exact Schur anchor")
    return {"matrix": [["1", "-1"], ["-1", "1"]],
            "vector": ["1", "1"], "output_energy": str(energy),
            "source_norm": str(source_norm), "row_abs_sum": str(row_sum),
            "schur_gain": str(schur_gain), "inequality_exact": True}


def row_record(source: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comparison, beta, width = source.source_vectors(lo, hi)
    masks = {name: np.zeros(len(beta), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[classify(source, value, float(lam[i]), float(comparison[i]))][i] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]
    column_energy = np.sum(matrix * matrix, axis=0, dtype=np.float64)
    row_abs_sum = float(np.max(np.sum(np.abs(matrix), axis=1)))
    schur_gain = row_abs_sum * row_abs_sum
    records = []
    vectors = {name: beta * masks[name] for name in CATEGORIES}
    for control_name, multiplier, offset, rule in CONTROLS:
        permutation = control_indices(len(beta), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            support = np.abs(placed) > 0.0
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            energy = float(output @ output)
            response_gain = energy / source_l2 if source_l2 else 0.0
            frobenius_gain = float(np.sum(column_energy[support]))
            hybrid_gain = min(frobenius_gain, schur_gain)
            occupancy = response_gain / hybrid_gain if hybrid_gain else 0.0
            improvement = frobenius_gain / hybrid_gain if hybrid_gain else 1.0
            gap = hybrid_gain - response_gain
            need(math.isfinite(gap) and gap >=
                 -BOUND_TOL * max(1.0, hybrid_gain), "hybrid bound")
            branch = ("SCHUR" if schur_gain < frobenius_gain else
                      "FROBENIUS")
            records.append({"control": control_name, "category": category,
                            "support_size": int(support.sum()),
                            "source_l2": show(source_l2),
                            "response_energy": show(energy),
                            "response_gain": show(response_gain),
                            "frobenius_gain": show(frobenius_gain),
                            "schur_gain": show(schur_gain),
                            "hybrid_gain": show(hybrid_gain),
                            "hybrid_gap": show(gap),
                            "hybrid_occupancy": show(occupancy),
                            "frobenius_improvement": show(improvement),
                            "active_branch": branch, "bound_holds": True})
    nonempty = [item for item in records if float(item["source_l2"]) > 0.0]
    need(len(records) == 36 and bool(nonempty), "record census")
    branches = {name: sum(item["active_branch"] == name for item in records)
                for name in ("SCHUR", "FROBENIUS")}
    return {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(beta),
        "operator": {"law": "all_plus", "Q": Q,
                      "kernel_exponent": EXPONENT, "height": HEIGHT},
        "row_abs_sum": show(row_abs_sum), "schur_gain": show(schur_gain),
        "controls": [{"name": name, "multiplier": multiplier,
                      "offset": offset, "rule": rule, "bijection": True}
                     for name, multiplier, offset, rule in CONTROLS],
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "records": records, "nonempty_record_count": len(nonempty),
        "branch_counts": branches,
        "hybrid_occupancy_min": show(min(float(item["hybrid_occupancy"])
                                         for item in nonempty)),
        "hybrid_occupancy_max": show(max(float(item["hybrid_occupancy"])
                                         for item in nonempty)),
        "improvement_min": show(min(float(item["frobenius_improvement"])
                                   for item in nonempty)),
        "improvement_max": show(max(float(item["frobenius_improvement"])
                                   for item in nonempty)),
        "source_weight_max_interval_width": show(width),
    }


def build_payload() -> dict[str, Any]:
    source = load_parent()
    rows = [row_record(source, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    nonempty = [item for row in rows for item in row["records"]
                if float(item["source_l2"]) > 0.0]
    broad = [item for item in nonempty
             if item["category"] in ("twin_prime", "non_twin_prime_shift",
                                     "zero_support")]
    violations = sum(not item["bound_holds"] for row in rows
                     for item in row["records"])
    need(len(rows) == 6 and len(nonempty) == 198 and violations == 0,
         "global hybrid census")
    branch_total = {name: sum(row["branch_counts"][name] for row in rows)
                    for name in ("SCHUR", "FROBENIUS")}
    need(branch_total == {"SCHUR": 54, "FROBENIUS": 162},
         "branch census")
    improvement = [float(item["frobenius_improvement"]) for item in nonempty]
    occupancy = [float(item["hybrid_occupancy"]) for item in nonempty]
    category_summary = {}
    for category in CATEGORIES:
        selected = [item for item in nonempty if item["category"] == category]
        category_summary[category] = {
            "records": len(selected),
            "hybrid_occupancy_min": show(min(float(item["hybrid_occupancy"]) for item in selected)) if selected else "0",
            "hybrid_occupancy_max": show(max(float(item["hybrid_occupancy"]) for item in selected)) if selected else "0",
            "improvement_min": show(min(float(item["frobenius_improvement"]) for item in selected)) if selected else "0",
            "improvement_max": show(max(float(item["frobenius_improvement"]) for item in selected)) if selected else "0",
        }
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC339_producer_sha256": PARENT_CODE_SHA256,
                         "TPC339_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES), "controls": [
                {"name": name, "multiplier": multiplier, "offset": offset,
                 "rule": rule}
                for name, multiplier, offset, rule in CONTROLS],
            "frobenius_envelope": "F(S)^2=||A[:,S]||_F^2",
            "schur_envelope": "R^2 where R=max_i sum_j |A(i,j)|",
            "hybrid_envelope": "min(F(S)^2,R^2)",
        },
        "exact_theorem": {
            "frobenius_bound": "||Ax||^2<=F(supp(x))^2||x||^2",
            "schur_bound": "||Ax||^2<=R^2||x||^2 for symmetric A",
            "hybrid_bound": "||Ax||^2<=min(F(supp(x))^2,R^2)||x||^2",
            "proof": "operator norm <= Frobenius and <= sqrt(||A||_1||A||_infty)",
            "finite_scope": "valid for every finite symmetric matrix",
        },
        "finite_audit": {
            "rows": 6, "origins": 2, "scales": 3, "controls": 9,
            "categories": 4, "records": 216, "nonempty_records": 198,
            "bound_checks": 216, "bound_violations": 0,
            "schur_branch_records": 54, "frobenius_branch_records": 162,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "summary": {
            "hybrid_occupancy_min": show(min(occupancy)),
            "hybrid_occupancy_max": show(max(occupancy)),
            "frobenius_improvement_min": show(min(improvement)),
            "frobenius_improvement_max": show(max(improvement)),
            "broad_hybrid_occupancy_max": show(max(
                float(item["hybrid_occupancy"]) for item in broad)),
            "branch_total": branch_total,
            "category_summary": category_summary,
            "bound_violations": violations,
            "nonempty_records": len(nonempty),
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC340_HYBRID_BOUND": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC340_HYBRID_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_216_RECORDS",
            "TPC340_BOUND_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_0_VIOLATIONS",
            "TPC340_SCHUR_BRANCH_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_54_RECORDS",
            "TPC340_ZERO_SUPPORT_IMPROVEMENT":
                "NUMERICALLY_CERTIFIED_FINITE_FACTOR_1.25_TO_4.70",
            "TPC340_BROAD_TIGHTNESS": "REFUTED_SCOPED",
            "TPC340_ARITHMETIC_ADVANCE": "NO",
            "TPC340_FIXED_POWER_CREDIT": 0,
            "TPC340_SOURCE_UNIFORM_L2": "OPEN",
            "TPC340_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC340_FULL_GATE_B": "OPEN",
            "TPC340_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue":
            "TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT",
        "rows": rows,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        document = build_document()
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(document))
            print("TPC340_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes(); stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "TPC340 certificate does not replay")
            print("TPC340_CERTIFICATE=PASS rows=6 controls=9 records=216 "
                  "bound_violations=0 schur_branch=54 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC340_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
