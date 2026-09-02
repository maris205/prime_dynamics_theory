#!/usr/bin/env python3
"""Independent replay of the TPC-340 hybrid envelope.

The numerical engine is the hash-locked reverse-shell implementation from
TPC-339's independent experiment; this checker does not import the TPC-340
producer.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc340_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope/code/"
PARENT_CODE = PARENT_CODE / "tpc339_mask_aware_frobenius_envelope.py"
PARENT_CERT = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope/results/"
PARENT_CERT = PARENT_CERT / "tpc339_certificate.json"
ENGINE = ROOT / "papers/tpc-339-mask-aware-frobenius-envelope/experiments/"
ENGINE = ENGINE / "tpc339_independent_checker.py"
PARENT_CODE_SHA256 = "df76022bfa5051477ec5bc04fef444aefc22abcb8f76fa02b339b7bc769fad18"
PARENT_CERT_SHA256 = "af6636eb7c9d9c6cbc0d392ae0b9effbaa9610dedafa12ee8d1272163fd48372"
ENGINE_SHA256 = "0fa57252c5f10ef4d79e65890a5e149e16eb65d56d73f95ff027ecca53eae727"
SCHEMA = "TPC340_SCHUR_FROBENIUS_HYBRID_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE"
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0), ("affine_3_11", 3, 11),
    ("affine_5_17", 5, 17), ("affine_7_29", 7, 29),
    ("reversal", -1, -1), ("affine_9_1", 9, 1),
    ("affine_11_13", 11, 13), ("affine_13_17", 13, 17),
    ("affine_17_19", 17, 19),
)


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


def load_engine() -> Any:
    need(digest(ENGINE.read_bytes()) == ENGINE_SHA256, "engine provenance")
    spec = importlib.util.spec_from_file_location("tpc339_reverse_engine", ENGINE)
    need(spec is not None and spec.loader is not None, "engine import")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.load_engine()


def recompute(engine: Any, origin: int, scale: int) -> tuple[float, list[dict[str, Any]]]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comparison, residual = engine.source_arrays(lo, hi)
    matrix = engine.reverse_matrix(origin, scale)
    column_energy = np.sum(matrix * matrix, axis=0, dtype=np.float64)
    row_abs_sum = float(np.max(np.sum(np.abs(matrix), axis=1)))
    schur_gain = row_abs_sum * row_abs_sum
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[engine.category(value, float(lam[i]), float(comparison[i]))][i] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    records = []
    for control_name, multiplier, offset in CONTROLS:
        permutation = engine.control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            support = np.abs(placed) > 0.0
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            energy = float(output @ output)
            response_gain = energy / source_l2 if source_l2 else 0.0
            frobenius_gain = float(np.sum(column_energy[support]))
            hybrid_gain = min(frobenius_gain, schur_gain)
            records.append({
                "control": control_name, "category": category,
                "support_size": int(support.sum()), "source_l2": source_l2,
                "response_energy": energy, "response_gain": response_gain,
                "frobenius_gain": frobenius_gain, "schur_gain": schur_gain,
                "hybrid_gain": hybrid_gain,
                "hybrid_gap": hybrid_gain - response_gain,
                "hybrid_occupancy": response_gain / hybrid_gain if hybrid_gain else 0.0,
                "frobenius_improvement": frobenius_gain / hybrid_gain if hybrid_gain else 1.0,
                "active_branch": "SCHUR" if schur_gain < frobenius_gain else "FROBENIUS",
            })
    return row_abs_sum, records


def close(actual: float, saved: Any, label: str,
          tolerance: float = 4.0e-7) -> None:
    expected = float(saved)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual), abs(expected)),
         label)


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256, "parent code")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent cert")
        engine = load_engine()
        need(tuple(engine.CONTROLS) == CONTROLS, "control protocol")
        raw = RESULT.read_bytes(); document = json.loads(raw)
        need(raw == canonical(document), "canonicality")
        need(document.get("claim_status") == STATUS, "status")
        payload = document["payload"]
        need(payload["schema"] == SCHEMA and
             document["payload_sha256"] == hashlib.sha256(
                 canonical(payload)).hexdigest(), "digest")
        need(payload["finite_audit"] == {
            "rows": 6, "origins": 2, "scales": 3, "controls": 9,
            "categories": 4, "records": 216, "nonempty_records": 198,
            "bound_checks": 216, "bound_violations": 0,
            "schur_branch_records": 54, "frobenius_branch_records": 162,
            "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
        all_nonempty: list[dict[str, Any]] = []
        for row in payload["rows"]:
            row_abs, actual = recompute(engine, row["origin"], row["scale"])
            close(row_abs, row["row_abs_sum"], "row abs sum")
            close(row_abs * row_abs, row["schur_gain"], "Schur gain")
            need(len(actual) == len(row["records"]) == 36, "record census")
            for item, saved in zip(actual, row["records"]):
                need(item["control"] == saved["control"] and
                     item["category"] == saved["category"] and
                     item["support_size"] == saved["support_size"] and
                     item["active_branch"] == saved["active_branch"] and
                     saved["bound_holds"] is True, "record metadata")
                for field in ("source_l2", "response_energy", "response_gain",
                              "frobenius_gain", "schur_gain", "hybrid_gain",
                              "hybrid_gap", "hybrid_occupancy",
                              "frobenius_improvement"):
                    close(item[field], saved[field], "record " + field)
                need(item["hybrid_gap"] >= -3.0e-10 * max(
                    1.0, item["hybrid_gain"]), "hybrid inequality")
                if item["source_l2"] > 0:
                    all_nonempty.append(item)
            need(sum(item["source_l2"] > 0 for item in actual) ==
                 row["nonempty_record_count"], "row nonempty census")
            need(row["branch_counts"] == {
                "SCHUR": sum(item["active_branch"] == "SCHUR" for item in actual),
                "FROBENIUS": sum(item["active_branch"] == "FROBENIUS" for item in actual)},
                 "row branch census")
        need(len(all_nonempty) == 198, "global nonempty census")
        occupancy = [item["hybrid_occupancy"] for item in all_nonempty]
        improvement = [item["frobenius_improvement"] for item in all_nonempty]
        summary = payload["summary"]
        close(min(occupancy), summary["hybrid_occupancy_min"], "occupancy min")
        close(max(occupancy), summary["hybrid_occupancy_max"], "occupancy max")
        close(min(improvement), summary["frobenius_improvement_min"], "improvement min")
        close(max(improvement), summary["frobenius_improvement_max"], "improvement max")
        broad = [item for item in all_nonempty if item["category"] != "prime_power_shift"]
        close(max(item["hybrid_occupancy"] for item in broad),
              summary["broad_hybrid_occupancy_max"], "broad occupancy")
        need(summary["branch_total"] == {"SCHUR": 54, "FROBENIUS": 162} and
             summary["bound_violations"] == 0, "summary guards")
        anchor = payload["exact_anchor"]
        need(anchor["inequality_exact"] is True and anchor["output_energy"] == "0" and
             anchor["source_norm"] == "2" and anchor["schur_gain"] == "4", "anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC340_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC340_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC340_FULL_GATE_B"] == "OPEN", "firewall")
        print("TPC340_INDEPENDENT_CHECK=PASS rows=6 controls=9 records=216 "
              "bound_violations=0 schur_branch=54 reverse_shell=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC340_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
