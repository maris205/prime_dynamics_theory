#!/usr/bin/env python3
"""Reverse-shell independent checker for TPC-346.

This file does not import the TPC-346 producer.  It uses the separately
hash-locked TPC-340 reverse engine, rebuilds all three panels, and recomputes
the fresh-panel, nested-model, transfer, and hostile-control statistics.
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
RESULT = PROJECT / "results/tpc346_certificate.json"
PRODUCER = PROJECT / "code/tpc346_third_panel_hostile_replication.py"
PRODUCER_SHA256 = "2c0bb5fd2e8738fa18dc419491a91b29c5a1fb8cc4f5fabaaec19e0a45752d4a"

ENGINE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py"
ENGINE_SHA256 = "4cff79b0f5c300357af4889e87a0734bbfdcc7f538ee19d313d8f2176a1b583c"
PARENT_CODE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/results/tpc340_certificate.json"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"
TPC345_CODE = ROOT / "papers/tpc-345-principal-angle-grassmann-audit/code/tpc345_principal_angle_grassmann_audit.py"
TPC345_CERT = ROOT / "papers/tpc-345-principal-angle-grassmann-audit/results/tpc345_certificate.json"
TPC345_CODE_SHA256 = "da6e4a72f3aee7a744cb2d15e9060260c380c25568efd19204968fd5ed63df9e"
TPC345_CERT_SHA256 = "b50a54ac77f4ec9a02d9223a5eab97c55f49203b8f921b4e2696ae014a06c3a2"

PANELS = (
    ("TPC341", (48097, 48609, 49217), "parent"),
    ("TPC342", (40097, 40609, 41121), "parent"),
    ("TPC346", (44097, 44609, 45217), "fresh"),
)
SCALE = 1024
Q = 54
EXPONENT = 1
CUTOFF = 50_000
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")
NUISANCE = ("non_twin_prime_shift", "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0), ("affine_3_11", 3, 11),
    ("affine_5_17", 5, 17), ("affine_7_29", 7, 29),
    ("reversal", -1, -1), ("affine_9_1", 9, 1),
    ("affine_11_13", 11, 13), ("affine_13_17", 13, 17),
    ("affine_17_19", 17, 19),
)
TOL = 9.0e-7
SHEAR = np.asarray([[1.0, 1.0, 0.0],
                    [0.0, 1.0, 1.0],
                    [0.0, 0.0, 1.0]], dtype=np.float64)


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


def close(actual: float, expected: Any, label: str,
          tolerance: float = TOL) -> None:
    a = float(actual)
    b = float(expected)
    need(math.isfinite(a) and math.isfinite(b) and
         abs(a - b) <= tolerance * max(1.0, abs(a), abs(b)), label)


def locked(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def load_engine() -> Any:
    need(PRODUCER_SHA256 != "TO_BE_FILLED", "producer hash not sealed")
    locked(PRODUCER, PRODUCER_SHA256, "TPC346 producer")
    locked(ENGINE, ENGINE_SHA256, "reverse engine")
    for path, expected, label in (
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC340 producer"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC340 certificate"),
            (TPC345_CODE, TPC345_CODE_SHA256, "TPC345 producer"),
            (TPC345_CERT, TPC345_CERT_SHA256, "TPC345 certificate")):
        locked(path, expected, label)
    parent = json.loads(PARENT_CERT.read_bytes())
    need(PARENT_CERT.read_bytes() == canonical(parent) and
         parent.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 certificate header")
    prior = json.loads(TPC345_CERT.read_bytes())
    need(TPC345_CERT.read_bytes() == canonical(prior) and
         prior.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT",
         "TPC345 certificate header")
    need(prior.get("payload", {}).get("round2_clue") ==
         "FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE", "TPC345 clue")
    spec = importlib.util.spec_from_file_location("tpc340_reverse", ENGINE)
    need(spec is not None and spec.loader is not None, "engine import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_engine()


def orthonormal(matrix: np.ndarray
                ) -> tuple[np.ndarray, np.ndarray, int]:
    need(matrix.ndim == 2 and matrix.shape[1] > 0, "basis matrix")
    left, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    threshold = (max(matrix.shape) * np.finfo(np.float64).eps *
                 singular[0]) if len(singular) else 0.0
    rank = int(np.count_nonzero(singular > threshold)) if len(singular) else 0
    return left[:, :rank], singular, rank


def projection(target: np.ndarray, matrix: np.ndarray
               ) -> tuple[dict[str, Any], np.ndarray, np.ndarray, int]:
    basis, singular, rank = orthonormal(matrix)
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    gap = target_energy - projected_energy - residual_energy
    need(target_energy > 0.0 and math.isfinite(target_energy), "target")
    need(abs(gap) <= 8.0e-6 * max(1.0, target_energy),
         "projection identity")
    return ({
        "target_energy": target_energy,
        "projected_energy": projected_energy,
        "residual_energy": residual_energy,
        "residual_retention": residual_energy / target_energy,
        "removed_fraction": 1.0 - residual_energy / target_energy,
        "decomposition_gap": gap,
        "nuisance_rank": rank,
        "nuisance_singular_values": singular,
        "nuisance_condition": float(singular[0] / singular[rank - 1])
        if rank else math.inf,
        "identity_holds": True,
    }, basis, singular, rank)


def row(engine: Any, origin: int
        ) -> tuple[dict[str, Any], dict[str, list[np.ndarray]],
                   dict[str, np.ndarray]]:
    lo, hi = origin, origin + SCALE // 2 - 1
    need(hi + 2 < CUTOFF, "cutoff")
    lam, comparison, residual = engine.source_arrays(lo, hi)
    matrix = engine.reverse_matrix(origin, SCALE)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for index, value in enumerate(range(lo, hi + 1)):
        masks[engine.category(value, float(lam[index]),
                              float(comparison[index]))][index] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs: dict[str, list[np.ndarray]] = {name: [] for name in CATEGORIES}
    records: list[dict[str, Any]] = []
    for control, multiplier, offset in CONTROLS:
        permutation = engine.control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            energy = float(output @ output)
            outputs[category].append(output)
            records.append({
                "control": control,
                "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": source_l2,
                "response_energy": energy,
            })
    means = {name: np.mean(np.stack(outputs[name]), axis=0)
             for name in CATEGORIES}
    need(len(records) == 36, "row records")
    return ({
        "origin": origin,
        "source_interval": [lo, hi],
        "cutoff_safe": hi + 2 < CUTOFF,
        "raw_records": records,
        "nonempty_raw_record_count":
            sum(item["source_l2"] > 0.0 for item in records),
    }, outputs, means)


def panel_data(rows: list[tuple[dict[str, Any],
                                dict[str, list[np.ndarray]],
                                dict[str, np.ndarray]]],
               equal_row: bool
               ) -> tuple[np.ndarray, np.ndarray]:
    targets: list[np.ndarray] = []
    parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    for _record, _outputs, means in rows:
        target = means["twin_prime"]
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(scale > 0.0 and math.isfinite(scale), "panel scale")
        targets.append(target / scale)
        for index, name in enumerate(NUISANCE):
            parts[index].append(means[name] / scale)
    return np.concatenate(targets), np.column_stack(
        [np.concatenate(item) for item in parts])


def block_matrix(matrices: list[np.ndarray]) -> np.ndarray:
    total = sum(item.shape[0] for item in matrices)
    result = np.zeros((total, len(matrices) * len(NUISANCE)),
                      dtype=np.float64)
    cursor = 0
    for panel_index, matrix in enumerate(matrices):
        size = matrix.shape[0]
        start = panel_index * len(NUISANCE)
        result[cursor:cursor + size, start:start + len(NUISANCE)] = matrix
        cursor += size
    return result


def geometry(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    left_q, left_s, left_r = orthonormal(left)
    right_q, right_s, right_r = orthonormal(right)
    cosines = np.linalg.svd(left_q.T @ right_q, compute_uv=False)
    angles = np.asarray([
        math.degrees(math.acos(min(1.0, max(-1.0, float(item)))))
        for item in cosines
    ])
    delta = left_q @ left_q.T - right_q @ right_q.T
    return {
        "left_rank": left_r,
        "right_rank": right_r,
        "principal_cosines": cosines,
        "principal_angles_degrees": angles,
        "projector_frobenius_distance":
            float(np.linalg.norm(delta, ord="fro")),
        "projector_spectral_distance": float(np.linalg.norm(delta, ord=2)),
    }


def prediction(train: list[tuple[np.ndarray, np.ndarray]],
               target: tuple[np.ndarray, np.ndarray]) -> dict[str, Any]:
    train_y = np.concatenate([item[0] for item in train])
    train_matrix = np.vstack([item[1] for item in train])
    target_y, target_matrix = target
    coefficient = np.linalg.lstsq(train_matrix, train_y, rcond=None)[0]
    residual = target_y - target_matrix @ coefficient
    singular = np.linalg.svd(train_matrix, compute_uv=False)
    rank = int(np.count_nonzero(
        singular > max(train_matrix.shape) * np.finfo(np.float64).eps *
        singular[0]))
    return {
        "training_panel_count": len(train),
        "target_panel_count": 1,
        "training_rank": rank,
        "training_condition": float(singular[0] / singular[rank - 1]),
        "coefficients": coefficient,
        "prediction_residual_retention":
            float(residual @ residual) / float(target_y @ target_y),
    }


def fresh_loo(rows: list[tuple[dict[str, Any],
                               dict[str, list[np.ndarray]],
                               dict[str, np.ndarray]]],
              equal_row: bool) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for omitted, control in enumerate(item[0] for item in CONTROLS):
        targets: list[np.ndarray] = []
        parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
        training = [index for index in range(len(CONTROLS))
                    if index != omitted]
        for _record, outputs, _means in rows:
            target = outputs["twin_prime"][omitted]
            scale = float(np.linalg.norm(target)) if equal_row else 1.0
            need(scale > 0.0 and math.isfinite(scale), "LOO scale")
            targets.append(target / scale)
            for index, name in enumerate(NUISANCE):
                mean = np.mean(np.stack(
                    [outputs[name][control_index]
                     for control_index in training]), axis=0)
                parts[index].append(mean / scale)
        metrics, _basis, _singular, _rank = projection(
            np.concatenate(targets),
            np.column_stack([np.concatenate(item) for item in parts]))
        metrics["omitted_control"] = control
        metrics["training_control_count"] = len(training)
        result.append(metrics)
    return result


def compare_projection(saved: dict[str, Any],
                       actual: dict[str, Any], label: str) -> None:
    for key in ("target_energy", "projected_energy", "residual_energy",
                "residual_retention", "removed_fraction",
                "decomposition_gap", "nuisance_condition"):
        close(actual[key], saved[key], label + ":" + key)
    need(int(actual["nuisance_rank"]) == int(saved["nuisance_rank"]),
         label + ":rank")


def compare_geometry(saved: dict[str, Any],
                     actual: dict[str, Any], label: str) -> None:
    need(int(saved["left_rank"]) == int(actual["left_rank"]) and
         int(saved["right_rank"]) == int(actual["right_rank"]),
         label + ":rank")
    for key in ("projector_frobenius_distance",
                "projector_spectral_distance"):
        close(actual[key], saved[key], label + ":" + key)
    for key in ("principal_cosines", "principal_angles_degrees"):
        need(len(saved[key]) == len(actual[key]), label + ":" + key)
        for index, value in enumerate(actual[key]):
            close(value, saved[key][index],
                  label + ":" + key + ":" + str(index))


def compare_prediction(saved: dict[str, Any],
                       actual: dict[str, Any], label: str) -> None:
    for key in ("training_panel_count", "target_panel_count",
                "training_rank"):
        need(int(saved[key]) == int(actual[key]), label + ":" + key)
    for key in ("training_condition", "prediction_residual_retention"):
        close(actual[key], saved[key], label + ":" + key)
    need(len(saved["coefficients"]) == len(actual["coefficients"]),
         label + ":coefficient length")
    for index, value in enumerate(actual["coefficients"]):
        close(value, saved["coefficients"][index],
              label + ":coefficient:" + str(index))


def main() -> int:
    try:
        engine = load_engine()
        need(tuple(engine.CONTROLS) == tuple(item[:3] for item in CONTROLS),
             "control protocol")
        panel_rows = {
            name: [row(engine, origin) for origin in origins]
            for name, origins, _kind in PANELS
        }
        raw_certificate = RESULT.read_bytes()
        document = json.loads(raw_certificate)
        need(raw_certificate == canonical(document), "certificate canonicality")
        need(document.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION",
             "certificate status")
        payload = document["payload"]
        need(payload.get("schema") ==
             "TPC346_THIRD_PANEL_HOSTILE_REPLICATION_V1",
             "schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        need(payload.get("finite_audit") == {
            "panels": 3, "rows": 9, "origins": 9, "controls": 9,
            "categories": 4, "raw_records": 324,
            "nonempty_raw_records": 261, "weightings": 2,
            "pairwise_geometry_comparisons": 6,
            "directed_panel_predictions_per_weighting": 6,
            "leave_one_panel_out_per_weighting": 3,
            "fresh_control_loo_per_weighting": 9,
            "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")

        all_rows = [item for name, _origins, _kind in PANELS
                    for item in panel_rows[name]]
        records = [record for rec, _outputs, _means in all_rows
                   for record in rec["raw_records"]]
        need(len(records) == 324 and
             sum(item["source_l2"] > 0.0 for item in records) == 261,
             "record census")
        cert_rows = payload.get("rows", [])
        need(len(cert_rows) == 9 and
             [item.get("origin") for item in cert_rows] ==
             [origin for _name, origins, _kind in PANELS for origin in origins],
             "row origins")
        for index, ((rec, _outputs, _means), saved) in enumerate(
                zip(all_rows, cert_rows)):
            need(saved.get("source_interval") ==
                 [saved["origin"], saved["origin"] + 511] and
                 saved.get("cutoff_safe") is True and
                 len(saved.get("raw_records", [])) == 36,
                 "row geometry " + str(index))
            for got, want in zip(rec["raw_records"], saved["raw_records"]):
                need(got["control"] == want["control"] and
                     got["category"] == want["category"] and
                     got["support_size"] == want["support_size"],
                     "record labels")
                close(got["source_l2"], want["source_l2"], "source_l2")
                close(got["response_energy"], want["response_energy"],
                      "response energy")

        saved_weightings = payload["weighting_results"]
        need([item["label"] for item in saved_weightings] ==
             ["raw", "equal_row"], "weighting labels")
        for weighting_index, equal_row in enumerate((False, True)):
            matrices: list[np.ndarray] = []
            targets: list[np.ndarray] = []
            saved = saved_weightings[weighting_index]
            panel_meta = saved["panel_geometry"]
            for panel_index, (name, _origins, kind) in enumerate(PANELS):
                target, matrix = panel_data(panel_rows[name], equal_row)
                targets.append(target); matrices.append(matrix)
                own, basis, _singular, _rank = projection(target, matrix)
                item = panel_meta[panel_index]
                need(item["name"] == name and item["kind"] == kind,
                     "panel metadata")
                compare_projection(item["target_projection"], own,
                                   name + ":own")
                changed, _s, changed_rank = orthonormal(matrix @ SHEAR)
                error = float(np.max(np.abs(
                    basis @ basis.T - changed @ changed.T)))
                need(changed_rank == own["nuisance_rank"] and error <= 2e-9,
                     name + ":basis invariance")

            combined_target = np.concatenate(targets)
            shared, _q, _s, _r = projection(combined_target,
                                            np.vstack(matrices))
            adaptive, _q, _s, _r = projection(combined_target,
                                              block_matrix(matrices))
            compare_projection(saved["shared_three_panel"], shared,
                               "shared")
            compare_projection(saved["panel_adaptive_three_panel"], adaptive,
                               "adaptive")
            pair_saved = saved["pairwise_geometry"]
            need(len(pair_saved) == 3, "pair count")
            cursor = 0
            for left in range(3):
                for right in range(left + 1, 3):
                    entry = pair_saved[cursor]; cursor += 1
                    need(entry["left"] == PANELS[left][0] and
                         entry["right"] == PANELS[right][0], "pair labels")
                    compare_geometry(entry["geometry"],
                                     geometry(matrices[left], matrices[right]),
                                     "pair geometry")
                    left_metrics, _q, _s, _r = projection(
                        targets[left], matrices[right])
                    right_metrics, _q, _s, _r = projection(
                        targets[right], matrices[left])
                    compare_projection(entry["left_target_on_right"],
                                       left_metrics, "left transfer")
                    compare_projection(entry["right_target_on_left"],
                                       right_metrics, "right transfer")

            directed = []
            for left in range(3):
                for right in range(3):
                    if left != right:
                        directed.append((left, right))
            saved_directed = saved["directed_predictions"]
            need(len(saved_directed) == 6, "directed prediction count")
            for entry, (left, right) in zip(saved_directed, directed):
                need(entry["training_panel"] == PANELS[left][0] and
                     entry["target_panel"] == PANELS[right][0],
                     "directed labels")
                compare_prediction(
                    entry["metrics"],
                    prediction([(targets[left], matrices[left])],
                               (targets[right], matrices[right])),
                    "directed prediction")

            saved_loo = saved["leave_one_panel_out"]
            need(len(saved_loo) == 3, "panel LOO count")
            for target_index, entry in enumerate(saved_loo):
                train_indices = [i for i in range(3) if i != target_index]
                need(entry["target_panel"] == PANELS[target_index][0] and
                     entry["training_panels"] ==
                     [PANELS[i][0] for i in train_indices],
                     "panel LOO labels")
                compare_prediction(
                    entry["metrics"],
                    prediction([(targets[i], matrices[i])
                                for i in train_indices],
                               (targets[target_index],
                                matrices[target_index])),
                    "panel LOO prediction")

            fresh = fresh_loo(panel_rows["TPC346"], equal_row)
            saved_fresh = saved["fresh_control_loo"]
            need(len(saved_fresh) == 9, "fresh LOO count")
            for got, want in zip(saved_fresh, fresh):
                need(got["omitted_control"] == want["omitted_control"] and
                     got["training_control_count"] ==
                     want["training_control_count"],
                     "fresh LOO labels")
                compare_projection(got, want, "fresh LOO")

        summary = payload["summary"]
        need(summary["panel_adaptive_raw_guard"] ==
             "PASS_FINITE_SCOPED" and
             summary["panel_adaptive_equal_row_guard"] ==
             "REFUTED_SCOPED" and
             summary["fresh_panel_own_fit"] == "REFUTED_SCOPED" and
             summary["third_panel_transfer"] == "REFUTED_SCOPED",
             "summary firewall")
        close(summary["panel_adaptive_three_panel_raw_retention"],
              saved_weightings[0]["panel_adaptive_three_panel"][
                  "residual_retention"], "summary raw")
        close(summary["panel_adaptive_three_panel_equal_row_retention"],
              saved_weightings[1]["panel_adaptive_three_panel"][
                  "residual_retention"], "summary equal")
        firewall = payload["claim_firewall"]
        need(firewall["TPC346_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC346_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC346_FULL_GATE_B"] == "OPEN" and
             firewall["TPC346_TWIN_PRIME_RESULT"] == "NONE",
             "claim firewall")
        print("TPC346_INDEPENDENT_CHECK=PASS panels=3 rows=9 "
              "raw_records=324 nonempty=261 "
              "adaptive_raw=0.2999630725662 "
              "adaptive_equal_row=0.3222362713305 "
              "fresh_loo_pairs=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC346_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
