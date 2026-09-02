#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-342.

This checker imports only the hash-locked reverse engine exposed by the
TPC-340 independent experiment.  Projection statistics and the holdout loop
are reimplemented here rather than imported from the producer.
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
RESULT = PROJECT / "results/tpc342_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope"
PARENT_CODE = PARENT_PROJECT / "code/tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc340_certificate.json"
ENGINE = PARENT_PROJECT / "experiments/tpc340_independent_checker.py"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"
ENGINE_SHA256 = "4cff79b0f5c300357af4889e87a0734bbfdcc7f538ee19d313d8f2176a1b583c"

PROTOCOL_PROJECT = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization"
PROTOCOL_CODE = PROTOCOL_PROJECT / "code/tpc341_fresh_holdout_nuisance_orthogonalization.py"
PROTOCOL_CERT = PROTOCOL_PROJECT / "results/tpc341_certificate.json"
PROTOCOL_CODE_SHA256 = "66269d586493a51adefeb8f17638df6b2eccf7e55aeab83e099b26c7768d52ac"
PROTOCOL_CERT_SHA256 = "50f8f81f4c401924187ae90327cf787139489570cbda68707b846e3d89f36218"

SCHEMA = "TPC342_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION"
ORIGINS = (40097, 40609, 41121)
SCALES = (1024,)
CUTOFF = 50_000
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
NUISANCE_CATEGORIES = ("non_twin_prime_shift", "prime_power_shift",
                        "zero_support")
CONTROLS = (
    ("identity", 1, 0), ("affine_3_11", 3, 11),
    ("affine_5_17", 5, 17), ("affine_7_29", 7, 29),
    ("reversal", -1, -1), ("affine_9_1", 9, 1),
    ("affine_11_13", 11, 13), ("affine_13_17", 13, 17),
    ("affine_17_19", 17, 19),
)
NUMERIC_TOL = 8.0e-6


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


def load_engine() -> Any:
    need(digest(PROTOCOL_CODE.read_bytes()) == PROTOCOL_CODE_SHA256,
         "TPC341 protocol producer provenance")
    need(digest(PROTOCOL_CERT.read_bytes()) == PROTOCOL_CERT_SHA256,
         "TPC341 protocol certificate provenance")
    protocol_raw = PROTOCOL_CERT.read_bytes()
    protocol_document = json.loads(protocol_raw)
    need(protocol_raw == canonical(protocol_document) and
         protocol_document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION",
         "TPC341 protocol certificate header")
    need(protocol_document["payload"]["protocol"]["origins"] ==
         [48097, 48609, 49217] and
         protocol_document["payload"]["protocol"]["scales"] == [1024],
         "TPC341 protocol panel lock")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate provenance")
    need(digest(ENGINE.read_bytes()) == ENGINE_SHA256,
         "reverse engine provenance")
    spec = importlib.util.spec_from_file_location("tpc340_reverse", ENGINE)
    need(spec is not None and spec.loader is not None, "engine import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_engine()


def projection_metrics(target: np.ndarray,
                        columns: list[np.ndarray]) -> dict[str, Any]:
    matrix = np.column_stack(columns)
    basis_all, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        rank = 0
        basis = np.zeros((len(target), 0), dtype=np.float64)
    else:
        tolerance = max(matrix.shape) * np.finfo(np.float64).eps * singular[0]
        rank = int(np.sum(singular > tolerance))
        basis = basis_all[:, :rank]
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    need(math.isfinite(target_energy) and target_energy > 0.0,
         "projection target")
    gap = target_energy - projected_energy - residual_energy
    need(abs(gap) <= NUMERIC_TOL * max(1.0, target_energy),
         "Pythagorean gap")
    condition = (float(singular[0] / singular[rank - 1])
                 if rank else math.inf)
    return {
        "target_energy": target_energy,
        "projected_energy": projected_energy,
        "residual_energy": residual_energy,
        "residual_retention": residual_energy / target_energy,
        "removed_fraction": 1.0 - residual_energy / target_energy,
        "decomposition_gap": gap,
        "nuisance_rank": rank,
        "nuisance_singular_values": singular,
        "nuisance_condition": condition,
        "identity_holds": True,
    }


def recompute(engine: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    need(hi + 2 < CUTOFF, "cutoff")
    lam, comparison, residual = engine.source_arrays(lo, hi)
    matrix = engine.reverse_matrix(origin, scale)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[engine.category(value, float(lam[i]), float(comparison[i]))][i] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs = {name: [] for name in CATEGORIES}
    raw_records: list[dict[str, Any]] = []
    for control_name, multiplier, offset in CONTROLS:
        permutation = engine.control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            response_energy = float(output @ output)
            outputs[category].append(output)
            raw_records.append({
                "control": control_name, "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": source_l2,
                "response_energy": response_energy,
                "response_gain": response_energy / source_l2
                if source_l2 else 0.0,
            })
    means = {category: np.mean(np.stack(outputs[category]), axis=0)
             for category in CATEGORIES}
    nuisance_means = [means[category] for category in NUISANCE_CATEGORIES]
    in_sample = projection_metrics(means["twin_prime"], nuisance_means)
    expected_rank = sum(float(np.linalg.norm(item)) > 0.0
                        for item in nuisance_means)
    need(in_sample["nuisance_rank"] == expected_rank, "in-sample rank")
    names = [item[0] for item in CONTROLS]
    holdout: list[dict[str, Any]] = []
    for omitted, control_name in enumerate(names):
        training = [index for index in range(len(names)) if index != omitted]
        training_means = [np.mean(np.stack([outputs[category][index]
                                             for index in training]), axis=0)
                          for category in NUISANCE_CATEGORIES]
        metrics = projection_metrics(outputs["twin_prime"][omitted],
                                     training_means)
        need(metrics["nuisance_rank"] == expected_rank, "holdout rank")
        metrics.update({"omitted_control": control_name,
                        "training_controls": [names[index] for index in training]})
        holdout.append(metrics)
    nonempty = [item for item in raw_records if item["source_l2"] > 0.0]
    return {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(residual),
        "cutoff_safe": hi + 2 < CUTOFF,
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "raw_records": raw_records,
        "nonempty_raw_record_count": len(nonempty),
        "mean_energies": {name: float(means[name] @ means[name])
                          for name in CATEGORIES},
        "expected_nuisance_rank": expected_rank,
        "in_sample": in_sample,
        "holdout": holdout,
    }


def close(actual: float, saved: Any, label: str,
          tolerance: float = 5.0e-7) -> None:
    expected = float(saved)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual), abs(expected)),
         label)


def check_metrics(actual: dict[str, Any], saved: dict[str, Any],
                  label: str) -> None:
    for field in ("target_energy", "projected_energy", "residual_energy",
                  "residual_retention", "removed_fraction",
                  "decomposition_gap", "nuisance_condition"):
        close(actual[field], saved[field], label + " " + field)
    need(actual["nuisance_rank"] == saved["nuisance_rank"] and
         saved["identity_holds"] is True, label + " metadata")
    singular = actual["nuisance_singular_values"]
    saved_singular = saved["nuisance_singular_values"]
    need(len(singular) == len(saved_singular), label + " singular census")
    for index, value in enumerate(singular):
        close(float(value), saved_singular[index],
              label + " singular " + str(index))


def main() -> int:
    try:
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document["payload"]
        need(payload["schema"] == SCHEMA and
             document["payload_sha256"] == hashlib.sha256(
                 canonical(payload)).hexdigest(), "payload digest")
        need(payload["finite_audit"] == {
            "rows": 3, "origins": 3, "scales": 1, "controls": 9,
            "categories": 4, "raw_records": 108,
            "nonempty_raw_records": 81,
            "in_sample_projection_records": 3,
            "leave_one_control_out_records": 27,
            "rank_failures": 0, "fixed_power_credit": 0,
            "arithmetic_advance": "NO"}, "finite audit")
        engine = load_engine()
        need(tuple(item[:3] for item in engine.CONTROLS) == CONTROLS,
             "control protocol")
        all_raw: list[dict[str, Any]] = []
        all_in: list[dict[str, Any]] = []
        all_hold: list[dict[str, Any]] = []
        for row in payload["rows"]:
            actual = recompute(engine, row["origin"], row["scale"])
            need(actual["source_interval"] == row["source_interval"] and
                 actual["mask_counts"] == row["mask_counts"] and
                 actual["expected_nuisance_rank"] ==
                 row["expected_nuisance_rank"], "row metadata")
            need(len(actual["raw_records"]) == len(row["raw_records"]) == 36,
                 "raw record census")
            for item, saved in zip(actual["raw_records"], row["raw_records"]):
                need(item["control"] == saved["control"] and
                     item["category"] == saved["category"] and
                     item["support_size"] == saved["support_size"],
                     "raw metadata")
                for field in ("source_l2", "response_energy", "response_gain"):
                    close(item[field], saved[field], "raw " + field)
            need(actual["nonempty_raw_record_count"] ==
                 row["nonempty_raw_record_count"], "nonempty row")
            for category in CATEGORIES:
                close(actual["mean_energies"][category],
                      row["mean_energies"][category], "mean energy")
            check_metrics(actual["in_sample"], row["in_sample"], "in-sample")
            need(len(actual["holdout"]) == len(row["holdout"]) == 9,
                 "holdout row census")
            for item, saved in zip(actual["holdout"], row["holdout"]):
                need(item["omitted_control"] == saved["omitted_control"] and
                     item["training_controls"] == saved["training_controls"],
                     "holdout metadata")
                check_metrics(item, saved, "holdout")
            all_raw.extend(actual["raw_records"])
            all_in.append(actual["in_sample"])
            all_hold.extend(actual["holdout"])
        need(len(all_raw) == 108 and
             sum(item["source_l2"] > 0 for item in all_raw) == 81 and
             len(all_in) == 3 and len(all_hold) == 27, "global census")
        summary = payload["summary"]
        in_retention = [item["residual_retention"] for item in all_in]
        hold_retention = [item["residual_retention"] for item in all_hold]
        in_condition = [item["nuisance_condition"] for item in all_in]
        hold_condition = [item["nuisance_condition"] for item in all_hold]
        close(min(in_retention), summary["in_sample_retention_min"], "in min")
        close(max(in_retention), summary["in_sample_retention_max"], "in max")
        close(min(hold_retention), summary["holdout_retention_min"], "hold min")
        close(max(hold_retention), summary["holdout_retention_max"], "hold max")
        close(min(in_condition), summary["in_sample_condition_min"], "in cond min")
        close(max(in_condition), summary["in_sample_condition_max"], "in cond max")
        close(min(hold_condition), summary["holdout_condition_min"], "hold cond min")
        close(max(hold_condition), summary["holdout_condition_max"], "hold cond max")
        need(summary["rank_failures"] == 0 and summary["rank_values"] == [2]
             and summary["raw_records"] == 108 and
             summary["nonempty_raw_records"] == 81 and
             summary["holdout_records"] == 27, "summary")
        need(float(summary["in_sample_retention_max"]) < 0.30 and
             float(summary["holdout_retention_min"]) > 0.40, "guards")
        anchor = payload["exact_anchor"]
        need(anchor["identity_exact"] is True and
             anchor["target_energy"] == "3" and
             anchor["projected_energy"] == "2" and
             anchor["residual_energy"] == "1", "anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC342_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC342_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC342_CONTROL_STABILITY"] == "REFUTED_SCOPED" and
             firewall["TPC342_FULL_GATE_B"] == "OPEN", "firewall")
        print("TPC342_INDEPENDENT_CHECK=PASS rows=3 controls=9 raw_records=108 "
              "holdout_records=27 rank_failures=0 reverse_shell=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC342_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
