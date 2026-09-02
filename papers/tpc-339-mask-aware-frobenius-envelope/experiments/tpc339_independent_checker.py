#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-339.

The checker imports only the hash-locked reverse-shell engine from TPC-338's
independent experiment, never the TPC-339 producer.
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
RESULT = PROJECT / "results/tpc339_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-338-growing-control-covariance-spectrum/code/"
PARENT_CODE = PARENT_CODE / "tpc338_growing_control_covariance_spectrum.py"
PARENT_CERT = ROOT / "papers/tpc-338-growing-control-covariance-spectrum/results/"
PARENT_CERT = PARENT_CERT / "tpc338_certificate.json"
ENGINE = ROOT / "papers/tpc-338-growing-control-covariance-spectrum/experiments/"
ENGINE = ENGINE / "tpc338_independent_checker.py"
PARENT_CODE_SHA256 = "cb169ac486b4fc858a17f7e98533b387272671d9c8f24589b13c54dfd90b34e4"
PARENT_CERT_SHA256 = "79b7a830f7277e186d73c2e2186412ca26861f47fc332ad9306ae22ec45c4a7d"
ENGINE_SHA256 = "2f3a3a0dcf60f3b2a914708952e3e5aad40763619d644de9346dc96f6e204f46"
SCHEMA = "TPC339_MASK_AWARE_FROBENIUS_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE"
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
    need(digest(ENGINE.read_bytes()) == ENGINE_SHA256,
         "independent engine provenance")
    spec = importlib.util.spec_from_file_location("tpc338_reverse_engine", ENGINE)
    need(spec is not None and spec.loader is not None, "engine import spec")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def recompute(engine: Any, origin: int, scale: int) -> list[dict[str, Any]]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comparison, residual = engine.source_arrays(lo, hi)
    matrix = engine.reverse_matrix(origin, scale)
    column_energy = np.sum(matrix * matrix, axis=0, dtype=np.float64)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[engine.category(value, float(lam[i]),
                              float(comparison[i]))][i] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    records = []
    for control_name, multiplier, offset in CONTROLS:
        permutation = engine.control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            support = np.abs(placed) > 0.0
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            response_energy = float(output @ output)
            response_gain = response_energy / source_l2 if source_l2 else 0.0
            envelope_gain = float(np.sum(column_energy[support]))
            occupancy = response_gain / envelope_gain if envelope_gain else 0.0
            records.append({"control": control_name, "category": category,
                            "support_size": int(support.sum()),
                            "source_l2": source_l2,
                            "response_energy": response_energy,
                            "response_gain": response_gain,
                            "restricted_frobenius_gain": envelope_gain,
                            "envelope_gap": envelope_gain - response_gain,
                            "occupancy": occupancy})
    return records


def close(actual: float, stored: Any, label: str,
          tolerance: float = 3.0e-7) -> None:
    expected = float(stored)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual), abs(expected)),
         label)


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
             "parent code")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
             "parent certificate")
        engine = load_engine()
        need(tuple(engine.CONTROLS) == CONTROLS, "engine control protocol")
        raw = RESULT.read_bytes(); document = json.loads(raw)
        need(raw == canonical(document), "canonicality")
        need(document.get("claim_status") == STATUS, "status")
        payload = document["payload"]
        need(payload["schema"] == SCHEMA and
             document["payload_sha256"] == hashlib.sha256(
                 canonical(payload)).hexdigest(), "payload digest")
        need(payload["finite_audit"] == {
            "rows": 6, "origins": 2, "scales": 3, "controls": 9,
            "categories": 4, "records": 216, "nonempty_records": 198,
            "bound_checks": 216, "bound_violations": 0,
            "broad_mask_records": 162, "fixed_power_credit": 0,
            "arithmetic_advance": "NO"}, "finite audit")
        all_nonempty: list[dict[str, Any]] = []
        for row in payload["rows"]:
            actual = recompute(engine, row["origin"], row["scale"])
            stored = row["records"]
            need(len(actual) == len(stored) == 36, "row record census")
            for item, saved in zip(actual, stored):
                need(item["control"] == saved["control"] and
                     item["category"] == saved["category"] and
                     item["support_size"] == saved["support_size"] and
                     saved["bound_holds"] is True, "record metadata")
                for field in ("source_l2", "response_energy", "response_gain",
                              "restricted_frobenius_gain", "envelope_gap",
                              "occupancy"):
                    close(item[field], saved[field], "record " + field)
                need(item["envelope_gap"] >= -2.0e-10 * max(
                    1.0, item["restricted_frobenius_gain"]), "independent bound")
                if item["source_l2"] > 0:
                    all_nonempty.append(item)
            need(sum(item["source_l2"] > 0 for item in actual) ==
                 row["nonempty_record_count"], "nonempty row census")
        need(len(all_nonempty) == 198, "global nonempty census")
        occupancies = [item["occupancy"] for item in all_nonempty]
        summary = payload["summary"]
        close(min(occupancies), summary["global_occupancy_min"], "minimum")
        close(max(occupancies), summary["global_occupancy_max"], "maximum")
        broad = [item for item in all_nonempty if item["category"] !=
                 "prime_power_shift"]
        close(max(item["occupancy"] for item in broad),
              summary["broad_mask_occupancy_max"], "broad maximum")
        need(max(item["occupancy"] for item in broad) < 0.2 and
             summary["bound_violations"] == 0, "summary guards")
        for category in CATEGORIES:
            selected = [item["occupancy"] for item in all_nonempty
                        if item["category"] == category]
            saved = summary["category_occupancy"][category]
            need(len(selected) == saved["records"], "category census")
            close(min(selected), saved["occupancy_min"], "category min")
            close(max(selected), saved["occupancy_max"], "category max")
        anchor = payload["exact_anchor"]
        need(anchor["equality_exact"] is True and
             anchor["output_energy"] == "45" and
             anchor["source_norm"] == "9" and
             anchor["restricted_frobenius_gain"] == "5", "exact anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC339_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC339_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC339_FULL_GATE_B"] == "OPEN", "firewall")
        print("TPC339_INDEPENDENT_CHECK=PASS rows=6 controls=9 records=216 "
              "bound_violations=0 reverse_shell=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC339_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
