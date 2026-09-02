#!/usr/bin/env python3
"""TPC-339: a sign-free mask-aware Frobenius envelope.

TPC-338 shows that signed covariance depends on the chosen control ensemble.
This project replaces sign heuristics by the elementary support-restricted
bound ||A x||^2 <= ||A[:,S]||_F^2 ||x||^2 for vectors supported on S.  It
audits the envelope on every masked control placement and measures its slack.
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
RESULT = PROJECT / "results/tpc339_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-338-growing-control-covariance-spectrum"
PARENT_CODE = PARENT_PROJECT / "code/tpc338_growing_control_covariance_spectrum.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc338_certificate.json"
PARENT_CODE_SHA256 = "cb169ac486b4fc858a17f7e98533b387272671d9c8f24589b13c54dfd90b34e4"
PARENT_CERT_SHA256 = "79b7a830f7277e186d73c2e2186412ca26861f47fc332ad9306ae22ec45c4a7d"

SCHEMA = "TPC339_MASK_AWARE_FROBENIUS_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE"
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
BOUND_TOL = 2.0e-10


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
         "TPC338 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC338 certificate provenance")
    raw = PARENT_CERT.read_bytes(); document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM",
         "TPC338 certificate header")
    spec = importlib.util.spec_from_file_location("tpc338_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    source, _ = module.load_parent()
    return source


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
    # A support-restricted Frobenius bound with equality.
    matrix = [[Fraction(1), Fraction(0)], [Fraction(2), Fraction(1)]]
    vector = [Fraction(3), Fraction(0)]
    output = [sum(matrix[i][j] * vector[j] for j in range(2))
              for i in range(2)]
    energy = sum(item * item for item in output)
    source_norm = sum(item * item for item in vector)
    restricted_frobenius = sum(matrix[i][0] * matrix[i][0] for i in range(2))
    need(energy == restricted_frobenius * source_norm,
         "exact envelope anchor")
    return {"matrix": [["1", "0"], ["2", "1"]],
            "vector": ["3", "0"], "support": [0],
            "output_energy": str(energy),
            "source_norm": str(source_norm),
            "restricted_frobenius_gain": str(restricted_frobenius),
            "equality_exact": True}


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
    records: list[dict[str, Any]] = []
    vectors = {name: beta * masks[name] for name in CATEGORIES}
    for control_name, multiplier, offset, rule in CONTROLS:
        permutation = control_indices(len(beta), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            support = np.abs(placed) > 0.0
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            response_energy = float(output @ output)
            actual_gain = response_energy / source_l2 if source_l2 else 0.0
            envelope_gain = float(np.sum(column_energy[support]))
            if envelope_gain:
                occupancy = actual_gain / envelope_gain
            else:
                occupancy = 0.0
            bound_gap = envelope_gain - actual_gain
            need(math.isfinite(actual_gain) and math.isfinite(envelope_gain) and
                 math.isfinite(occupancy) and bound_gap >=
                 -BOUND_TOL * max(1.0, envelope_gain), "support envelope bound")
            records.append({
                "control": control_name, "category": category,
                "support_size": int(support.sum()),
                "source_l2": show(source_l2),
                "response_energy": show(response_energy),
                "response_gain": show(actual_gain),
                "restricted_frobenius_gain": show(envelope_gain),
                "envelope_gap": show(bound_gap),
                "occupancy": show(occupancy),
                "bound_holds": True,
            })
    nonempty = [item for item in records if float(item["source_l2"]) > 0.0]
    need(len(records) == len(CONTROLS) * len(CATEGORIES), "record census")
    need(bool(nonempty), "nonempty envelope records")
    occupancies = [float(item["occupancy"]) for item in nonempty]
    need(min(occupancies) >= -BOUND_TOL and max(occupancies) <= 1.0 + BOUND_TOL,
         "occupancy range")
    by_category = {}
    for category in CATEGORIES:
        selected = [item for item in nonempty if item["category"] == category]
        by_category[category] = {
            "records": len(selected),
            "occupancy_min": show(min(float(item["occupancy"]) for item in selected)) if selected else "0",
            "occupancy_max": show(max(float(item["occupancy"]) for item in selected)) if selected else "0",
            "response_gain_min": show(min(float(item["response_gain"]) for item in selected)) if selected else "0",
            "response_gain_max": show(max(float(item["response_gain"]) for item in selected)) if selected else "0",
        }
    return {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(beta),
        "operator": {"law": "all_plus", "Q": Q,
                      "kernel_exponent": EXPONENT, "height": HEIGHT},
        "controls": [{"name": name, "multiplier": multiplier,
                      "offset": offset, "rule": rule, "bijection": True}
                     for name, multiplier, offset, rule in CONTROLS],
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "records": records,
        "nonempty_record_count": len(nonempty),
        "occupancy_min": show(min(occupancies)),
        "occupancy_max": show(max(occupancies)),
        "category_summary": by_category,
        "source_weight_max_interval_width": show(width),
    }


def build_payload() -> dict[str, Any]:
    source = load_parent()
    rows = [row_record(source, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    nonempty = [item for row in rows for item in row["records"]
                if float(item["source_l2"]) > 0.0]
    occupancy = [float(item["occupancy"]) for item in nonempty]
    violations = sum(not item["bound_holds"] for row in rows
                     for item in row["records"])
    category_summary = {}
    for category in CATEGORIES:
        selected = [item for item in nonempty if item["category"] == category]
        category_summary[category] = {
            "records": len(selected),
            "occupancy_min": show(min(float(item["occupancy"]) for item in selected)) if selected else "0",
            "occupancy_max": show(max(float(item["occupancy"]) for item in selected)) if selected else "0",
        }
    need(len(rows) == 6 and len(nonempty) == 198 and violations == 0,
         "global envelope census")
    need(min(occupancy) >= -BOUND_TOL and max(occupancy) <= 1.0 + BOUND_TOL,
         "global occupancy guard")
    broad = [item for item in nonempty
             if item["category"] in ("twin_prime", "non_twin_prime_shift",
                                     "zero_support")]
    need(max(float(item["occupancy"]) for item in broad) < 0.2,
         "broad-mask slack")
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC338_producer_sha256": PARENT_CODE_SHA256,
                         "TPC338_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "controls": [
                {"name": name, "multiplier": multiplier, "offset": offset,
                 "rule": rule}
                for name, multiplier, offset, rule in CONTROLS],
            "support_envelope":
                "F(S)^2=sum_{t in S} sum_u |A(u,t)|^2",
            "bound": "||A x||_2^2 <= F(supp(x))^2 ||x||_2^2",
            "occupancy": "response_gain/F(supp(x))^2",
        },
        "exact_theorem": {
            "support_restricted_frobenius_bound":
                "||A x||^2 <= ||A[:,S]||_F^2 ||x||^2 for supp(x) subset S",
            "proof": "operator norm <= Frobenius norm",
            "sign_free": True,
            "finite_scope": "valid for every finite matrix and supported vector",
        },
        "finite_audit": {
            "rows": 6, "origins": 2, "scales": 3, "controls": 9,
            "categories": 4, "records": 216, "nonempty_records": 198,
            "bound_checks": 216, "bound_violations": 0,
            "broad_mask_records": len(broad), "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "summary": {
            "global_occupancy_min": show(min(occupancy)),
            "global_occupancy_max": show(max(occupancy)),
            "broad_mask_occupancy_max": show(max(float(item["occupancy"])
                                                  for item in broad)),
            "category_occupancy": category_summary,
            "bound_violations": violations,
            "nonempty_records": len(nonempty),
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC339_SUPPORT_FROBENIUS_BOUND":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC339_MASKED_CONTROL_REPLAY":
                "NUMERICALLY_CERTIFIED_FINITE_216_RECORDS",
            "TPC339_BOUND_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_0_VIOLATIONS",
            "TPC339_BROAD_MASK_SLACK":
                "NUMERICALLY_CERTIFIED_FINITE_OCCUPANCY_BELOW_0.2",
            "TPC339_SIGN_FREE_REPLACEMENT": "PROVED_FINITE_ONLY",
            "TPC339_SIMPLE_ENVELOPE_TIGHTNESS": "REFUTED_SCOPED",
            "TPC339_ARITHMETIC_ADVANCE": "NO",
            "TPC339_FIXED_POWER_CREDIT": 0,
            "TPC339_SOURCE_UNIFORM_L2": "OPEN",
            "TPC339_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC339_FULL_GATE_B": "OPEN",
            "TPC339_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue":
            "TEST_A_SHARPER_MASKED_GRAM_OR_NUISANCE_ORTHOGONALIZATION",
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
            print("TPC339_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes(); stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "TPC339 certificate does not replay")
            print("TPC339_CERTIFICATE=PASS rows=6 controls=9 records=216 "
                  "bound_violations=0 broad_mask_slack=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC339_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
