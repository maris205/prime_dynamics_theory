#!/usr/bin/env python3
"""TPC-346: third-panel hostile replication and finite route-freeze test.

TPC-345 found a weighting-sensitive principal-angle obstruction for two
panels.  This release adds a disjoint third panel and asks whether the
panel-adaptive nuisance model survives a fresh panel and leave-one-panel-out
prediction.  Every claim is finite and protocol-scoped.
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
RESULT = PROJECT / "results/tpc346_certificate.json"

TPC345_PROJECT = ROOT / "papers/tpc-345-principal-angle-grassmann-audit"
TPC345_CODE = TPC345_PROJECT / "code/tpc345_principal_angle_grassmann_audit.py"
TPC345_CERT = TPC345_PROJECT / "results/tpc345_certificate.json"
TPC345_CODE_SHA256 = "da6e4a72f3aee7a744cb2d15e9060260c380c25568efd19204968fd5ed63df9e"
TPC345_CERT_SHA256 = "b50a54ac77f4ec9a02d9223a5eab97c55f49203b8f921b4e2696ae014a06c3a2"

TPC340_CODE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py"
TPC340_CERT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/results/tpc340_certificate.json"
TPC340_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
TPC340_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

SCHEMA = "TPC346_THIRD_PANEL_HOSTILE_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION"
PANELS = (
    ("TPC341", (48097, 48609, 49217), "parent"),
    ("TPC342", (40097, 40609, 41121), "parent"),
    ("TPC346", (44097, 44609, 45217), "fresh"),
)
PANEL_KINDS = {name: kind for name, _origins, kind in PANELS}
SCALE = 1024
Q = 54
EXPONENT = 1
HEIGHT = 66
CUTOFF = 50_000
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")
NUISANCE = ("non_twin_prime_shift", "prime_power_shift", "zero_support")
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
MODEL_GUARD = 0.30
PREDICTION_GUARD = 0.30
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


def show(value: float) -> str:
    # Keep the certificate stable under harmless BLAS last-bit variation.
    return format(float(value), ".13g")


def close(actual: float, expected: Any, label: str,
          tolerance: float = 8.0e-7) -> None:
    value = float(expected)
    need(math.isfinite(actual) and math.isfinite(value) and
         abs(actual - value) <= tolerance * max(1.0, abs(actual), abs(value)),
         label)


def locked(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def load_source() -> tuple[Any, Any]:
    locked(TPC345_CODE, TPC345_CODE_SHA256, "TPC345 producer")
    locked(TPC345_CERT, TPC345_CERT_SHA256, "TPC345 certificate")
    locked(TPC340_CODE, TPC340_CODE_SHA256, "TPC340 producer")
    locked(TPC340_CERT, TPC340_CERT_SHA256, "TPC340 certificate")
    raw = TPC345_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT",
         "TPC345 certificate header")
    protocol = document.get("payload", {}).get("protocol", {})
    need([item.get("name") for item in protocol.get("panels", [])] ==
         ["TPC341", "TPC342"], "TPC345 parent panels")
    need(document.get("payload", {}).get("round2_clue") ==
         "FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE", "TPC345 clue")
    spec = importlib.util.spec_from_file_location("tpc345_parent", TPC345_CODE)
    need(spec is not None and spec.loader is not None, "TPC345 import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.load_source()


def orthonormal(matrix: np.ndarray
                ) -> tuple[np.ndarray, np.ndarray, int]:
    need(matrix.ndim == 2 and matrix.shape[1] > 0, "basis matrix")
    left, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        return np.zeros((matrix.shape[0], 0), dtype=np.float64), singular, 0
    threshold = max(matrix.shape) * np.finfo(np.float64).eps * singular[0]
    rank = int(np.count_nonzero(singular > threshold))
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
    need(math.isfinite(target_energy) and target_energy > 0.0,
         "projection target")
    need(math.isfinite(projected_energy) and math.isfinite(residual_energy),
         "projection energies")
    need(abs(gap) <= NUMERIC_TOL * max(1.0, target_energy),
         "projection identity")
    return ({
        "target_energy": show(target_energy),
        "projected_energy": show(projected_energy),
        "residual_energy": show(residual_energy),
        "residual_retention": show(residual_energy / target_energy),
        "removed_fraction": show(1.0 - residual_energy / target_energy),
        "decomposition_gap": show(gap),
        "nuisance_rank": rank,
        "nuisance_singular_values": [show(item) for item in singular],
        "nuisance_condition": show(float(singular[0] / singular[rank - 1]))
        if rank else "inf",
        "identity_holds": True,
    }, basis, singular, rank)


def panel_data(rows: list[dict[str, Any]], equal_row: bool
               ) -> tuple[np.ndarray, np.ndarray]:
    targets: list[np.ndarray] = []
    parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    for row in rows:
        target = row["_means"]["twin_prime"]
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(math.isfinite(scale) and scale > 0.0, "panel scale")
        targets.append(target / scale)
        for index, name in enumerate(NUISANCE):
            parts[index].append(row["_means"][name] / scale)
    return np.concatenate(targets), np.column_stack(
        [np.concatenate(item) for item in parts])


def block_matrix(matrices: list[np.ndarray]) -> np.ndarray:
    total = sum(item.shape[0] for item in matrices)
    width = len(matrices) * len(NUISANCE)
    result = np.zeros((total, width), dtype=np.float64)
    cursor = 0
    for panel_index, matrix in enumerate(matrices):
        size = matrix.shape[0]
        start = panel_index * len(NUISANCE)
        result[cursor:cursor + size, start:start + len(NUISANCE)] = matrix
        cursor += size
    return result


def clean(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items()
            if not key.startswith("_")}


def geometry(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    left_q, left_s, left_r = orthonormal(left)
    right_q, right_s, right_r = orthonormal(right)
    cosines = np.linalg.svd(left_q.T @ right_q, compute_uv=False)
    angles = [math.degrees(math.acos(min(1.0, max(-1.0, float(item)))))
              for item in cosines]
    delta = left_q @ left_q.T - right_q @ right_q.T
    return {
        "left_rank": left_r,
        "right_rank": right_r,
        "principal_cosines": [show(item) for item in cosines],
        "principal_angles_degrees": [show(item) for item in angles],
        "projector_frobenius_distance": show(float(np.linalg.norm(
            delta, ord="fro"))),
        "projector_spectral_distance": show(float(np.linalg.norm(
            delta, ord=2))),
        "min_rank": min(left_r, right_r),
        "definition": "singular_values(Q_left^T Q_right)",
        "_left_basis": left_q,
        "_right_basis": right_q,
        "_left_singular": left_s,
        "_right_singular": right_s,
        "_left_rank": left_r,
        "_right_rank": right_r,
    }


def transfer(target: np.ndarray, matrix: np.ndarray) -> dict[str, Any]:
    metrics, _basis, _singular, _rank = projection(target, matrix)
    return metrics


def prediction(train: list[tuple[np.ndarray, np.ndarray]],
               target: tuple[np.ndarray, np.ndarray]) -> dict[str, Any]:
    train_y = np.concatenate([item[0] for item in train])
    train_matrix = np.vstack([item[1] for item in train])
    target_y, target_matrix = target
    coefficient = np.linalg.lstsq(train_matrix, train_y, rcond=None)[0]
    residual = target_y - target_matrix @ coefficient
    retention = float(residual @ residual) / float(target_y @ target_y)
    singular = np.linalg.svd(train_matrix, compute_uv=False)
    rank = int(np.linalg.matrix_rank(train_matrix))
    condition = float(singular[0] / singular[rank - 1]) if rank else math.inf
    return {
        "training_panel_count": len(train),
        "target_panel_count": 1,
        "training_rank": rank,
        "training_condition": show(condition),
        "coefficients": [show(item) for item in coefficient],
        "prediction_residual_retention": show(retention),
        "prediction_identity":
            "RESIDUAL_NORM_ONLY_NO_ORTHOGONAL_PROJECTION_IDENTITY",
    }


def fresh_control_loo(rows: list[dict[str, Any]],
                      equal_row: bool) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for omitted, control in enumerate(item[0] for item in CONTROLS):
        targets: list[np.ndarray] = []
        parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
        training = [index for index in range(len(CONTROLS))
                    if index != omitted]
        for row in rows:
            target = row["_outputs"]["twin_prime"][omitted]
            scale = float(np.linalg.norm(target)) if equal_row else 1.0
            need(math.isfinite(scale) and scale > 0.0, "LOO scale")
            targets.append(target / scale)
            for index, name in enumerate(NUISANCE):
                mean = np.mean(np.stack(
                    [row["_outputs"][name][control_index]
                     for control_index in training]), axis=0)
                parts[index].append(mean / scale)
        target = np.concatenate(targets)
        matrix = np.column_stack([np.concatenate(item) for item in parts])
        metrics, _basis, _singular, _rank = projection(target, matrix)
        metrics["omitted_control"] = control
        metrics["training_control_count"] = len(training)
        result.append(metrics)
    return result


def invariance(matrix: np.ndarray, reference: dict[str, Any]) -> dict[str, Any]:
    basis, _singular, rank = orthonormal(matrix)
    changed, _changed_s, changed_rank = orthonormal(matrix @ SHEAR)
    old_projector = basis @ basis.T
    new_projector = changed @ changed.T
    error = float(np.max(np.abs(old_projector - new_projector)))
    need(rank == changed_rank, "shear rank")
    return {
        "rank": rank,
        "changed_rank": changed_rank,
        "max_projector_entry_error": show(error),
        "reference_rank": reference["nuisance_rank"],
        "span_invariant": error <= 2.0e-9,
    }


def exact_anchor() -> dict[str, Any]:
    # A rational nested-model example: panel-specific columns add one
    # contrast direction to a shared column.
    b = [Fraction(1), Fraction(0), Fraction(1), Fraction(0)]
    d = [Fraction(0), Fraction(1), Fraction(0), Fraction(-1)]
    u1 = [(x + y) / 2 for x, y in zip(b, d)]
    u2 = [(x - y) / 2 for x, y in zip(b, d)]
    target = [Fraction(1), Fraction(1), Fraction(1), Fraction(0)]
    shared_energy = (sum(x * y for x, y in zip(b, target)) ** 2 /
                     sum(x * x for x in b))
    contrast_energy = (sum(x * y for x, y in zip(d, target)) ** 2 /
                       sum(x * x for x in d))
    need(u1 == [Fraction(1, 2), Fraction(1, 2), Fraction(1, 2),
                Fraction(-1, 2)] and
        u2 == [Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2),
                Fraction(1, 2)] and
         shared_energy == 2 and contrast_energy == Fraction(1, 2),
         "nested anchor")
    return {
        "shared_column": ["1", "0", "1", "0"],
        "contrast_column": ["0", "1", "0", "-1"],
        "panel_one_column": ["1/2", "1/2", "1/2", "-1/2"],
        "panel_two_column": ["1/2", "-1/2", "1/2", "1/2"],
        "target": ["1", "1", "1", "0"],
        "shared_projected_energy": "2",
        "additional_contrast_energy": "1/2",
        "identity_exact": True,
    }


def build_payload() -> dict[str, Any]:
    parent_module, source = load_source()
    panel_rows = {
        name: [parent_module.row_data(source, origin) for origin in origins]
        for name, origins, _kind in PANELS
    }
    all_rows = [row for name, _origins, _kind in PANELS
                for row in panel_rows[name]]
    records = [record for row in all_rows for record in row["raw_records"]]
    nonempty = [record for record in records
                if float(record["source_l2"]) > 0.0]
    need(len(all_rows) == 9 and len(records) == 324 and
         len(nonempty) == 261, "global record census")

    weighting_results: list[dict[str, Any]] = []
    for equal_row, label in ((False, "raw"), (True, "equal_row")):
        panel_matrices: list[np.ndarray] = []
        panel_targets: list[np.ndarray] = []
        panel_documents: list[dict[str, Any]] = []
        for name, _origins, _kind in PANELS:
            target, matrix = panel_data(panel_rows[name], equal_row)
            panel_targets.append(target)
            panel_matrices.append(matrix)
            own, _basis, _singular, _rank = projection(target, matrix)
            inv = invariance(matrix, own)
            panel_documents.append({
               "name": name,
                "kind": PANEL_KINDS[name],
                "rank": own["nuisance_rank"],
                "singular_values": own["nuisance_singular_values"],
                "condition": own["nuisance_condition"],
                "target_projection": own,
                "basis_invariance": inv,
            })

        combined_target = np.concatenate(panel_targets)
        shared_matrix = np.vstack(panel_matrices)
        shared, _shared_basis, _shared_singular, _shared_rank = projection(
            combined_target, shared_matrix)
        adaptive_matrix = block_matrix(panel_matrices)
        adaptive, _adaptive_basis, _adaptive_singular, _adaptive_rank = projection(
            combined_target, adaptive_matrix)
        need(float(adaptive["residual_retention"]) <=
             float(shared["residual_retention"]) + NUMERIC_TOL,
             "nested model monotonicity")

        pairwise: list[dict[str, Any]] = []
        for left_index in range(len(PANELS)):
            for right_index in range(left_index + 1, len(PANELS)):
                left_name = PANELS[left_index][0]
                right_name = PANELS[right_index][0]
                geom = geometry(panel_matrices[left_index],
                                panel_matrices[right_index])
                pairwise.append({
                    "left": left_name,
                    "right": right_name,
                    "geometry": clean(geom),
                    "left_target_on_right": transfer(
                        panel_targets[left_index], panel_matrices[right_index]),
                    "right_target_on_left": transfer(
                        panel_targets[right_index], panel_matrices[left_index]),
                })

        directed_predictions: list[dict[str, Any]] = []
        for train_index in range(len(PANELS)):
            for target_index in range(len(PANELS)):
                if train_index == target_index:
                    continue
                train_name = PANELS[train_index][0]
                target_name = PANELS[target_index][0]
                directed_predictions.append({
                    "training_panel": train_name,
                    "target_panel": target_name,
                    "metrics": prediction(
                        [(panel_targets[train_index],
                          panel_matrices[train_index])],
                        (panel_targets[target_index],
                         panel_matrices[target_index])),
                })

        leave_one_out_panels: list[dict[str, Any]] = []
        for target_index in range(len(PANELS)):
            train = [(panel_targets[index], panel_matrices[index])
                     for index in range(len(PANELS))
                     if index != target_index]
            leave_one_out_panels.append({
                "training_panels": [PANELS[index][0]
                                    for index in range(len(PANELS))
                                    if index != target_index],
                "target_panel": PANELS[target_index][0],
                "metrics": prediction(train, (panel_targets[target_index],
                                               panel_matrices[target_index])),
            })

        fresh_loo = fresh_control_loo(panel_rows["TPC346"], equal_row)
        weighting_results.append({
            "label": label,
            "row_normalization": "target_l2_inverse" if equal_row else "none",
            "panel_geometry": panel_documents,
            "shared_three_panel": shared,
            "panel_adaptive_three_panel": adaptive,
            "pairwise_geometry": pairwise,
            "directed_predictions": directed_predictions,
            "leave_one_panel_out": leave_one_out_panels,
            "fresh_control_loo": fresh_loo,
        })

    raw = weighting_results[0]
    equal = weighting_results[1]
    fresh_raw = raw["panel_geometry"][2]["target_projection"]
    fresh_equal = equal["panel_geometry"][2]["target_projection"]
    adaptive_raw = raw["panel_adaptive_three_panel"]
    adaptive_equal = equal["panel_adaptive_three_panel"]
    shared_raw = raw["shared_three_panel"]
    shared_equal = equal["shared_three_panel"]
    prediction_values = [
        float(entry["metrics"]["prediction_residual_retention"])
        for result in weighting_results
        for entry in result["directed_predictions"]
    ]
    leave_values = [
        float(entry["metrics"]["prediction_residual_retention"])
        for result in weighting_results
        for entry in result["leave_one_panel_out"]
    ]
    fresh_loo_values = [
        float(entry["residual_retention"])
        for result in weighting_results
        for entry in result["fresh_control_loo"]
    ]
    need(float(fresh_raw["residual_retention"]) >= MODEL_GUARD and
         float(fresh_equal["residual_retention"]) >= MODEL_GUARD,
         "fresh own-fit obstruction")
    need(float(shared_raw["residual_retention"]) >= MODEL_GUARD and
         float(shared_equal["residual_retention"]) >= MODEL_GUARD,
         "shared three-panel obstruction")
    need(float(adaptive_raw["residual_retention"]) < MODEL_GUARD and
         float(adaptive_equal["residual_retention"]) >= MODEL_GUARD,
         "adaptive weighting decision")
    need(min(prediction_values) > PREDICTION_GUARD and
         min(leave_values) > PREDICTION_GUARD and
         min(fresh_loo_values) > PREDICTION_GUARD,
         "hostile prediction guards")

    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC340_producer_sha256": TPC340_CODE_SHA256,
            "TPC340_certificate_sha256": TPC340_CERT_SHA256,
            "TPC345_producer_sha256": TPC345_CODE_SHA256,
            "TPC345_certificate_sha256": TPC345_CERT_SHA256,
        },
        "protocol": {
            "panels": [{"name": name, "origins": list(origins), "kind": kind}
                       for name, origins, kind in PANELS],
            "fresh_panel": "TPC346",
            "scale": SCALE,
            "operator": {"law": "all_plus", "Q": Q,
                         "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "nuisance_categories": list(NUISANCE),
            "controls": [{"name": name, "multiplier": multiplier,
                          "offset": offset, "rule": rule}
                         for name, multiplier, offset, rule in CONTROLS],
            "weightings": {
                "raw": "stacked rows without row rescaling",
                "equal_row": "each row divided by its twin-target L2 norm",
            },
            "rank_rule":
                "singular_value > max(matrix_shape)*eps*largest_singular_value",
            "shared_model":
                "one nuisance coefficient vector across all three panels",
            "panel_adaptive_model":
                "one nuisance coefficient vector per panel",
            "model_guard": "residual retention < 0.30",
            "prediction_guard": "prediction residual retention < 0.30",
            "hostile_control_loo":
                "fresh-panel target uses one omitted control and nuisance means "
                "over the other eight controls",
        },
        "exact_theorem": {
            "nested_model_monotonicity":
                "a panel-shared column space is contained in the "
                "panel-adaptive block space",
            "projection_identity":
                "||Y||^2=||PY||^2+||(I-P)Y||^2",
            "prediction_definition":
                "least-squares coefficient trained on source panels and "
                "evaluated on a held-out panel",
            "basis_invariance":
                "nonsingular column changes preserve a finite column space",
            "finite_scope": "all identities concern declared finite matrices",
            "arithmetic_interpretation": "none",
        },
        "finite_audit": {
            "panels": 3,
            "rows": 9,
            "origins": 9,
            "controls": 9,
            "categories": 4,
            "raw_records": 324,
            "nonempty_raw_records": 261,
            "weightings": 2,
            "pairwise_geometry_comparisons": 6,
            "directed_panel_predictions_per_weighting": 6,
            "leave_one_panel_out_per_weighting": 3,
            "fresh_control_loo_per_weighting": 9,
            "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "summary": {
            "fresh_panel_raw_retention": fresh_raw["residual_retention"],
            "fresh_panel_equal_row_retention":
                fresh_equal["residual_retention"],
            "shared_three_panel_raw_retention":
                shared_raw["residual_retention"],
            "shared_three_panel_equal_row_retention":
                shared_equal["residual_retention"],
            "panel_adaptive_three_panel_raw_retention":
                adaptive_raw["residual_retention"],
            "panel_adaptive_three_panel_equal_row_retention":
                adaptive_equal["residual_retention"],
            "panel_adaptive_raw_guard": "PASS_FINITE_SCOPED",
            "panel_adaptive_equal_row_guard": "REFUTED_SCOPED",
            "fresh_panel_own_fit": "REFUTED_SCOPED",
            "panel_adaptive_weighting_stability": "REFUTED_SCOPED",
            "third_panel_transfer": "REFUTED_SCOPED",
            "directed_prediction_min": show(min(prediction_values)),
            "directed_prediction_max": show(max(prediction_values)),
            "leave_one_panel_out_min": show(min(leave_values)),
            "leave_one_panel_out_max": show(max(leave_values)),
            "fresh_control_loo_min": show(min(fresh_loo_values)),
            "fresh_control_loo_max": show(max(fresh_loo_values)),
            "three_panel_shared_obstruction": "REFUTED_SCOPED",
            "route_decision": "FREEZE_PANEL_ADAPTIVE_ROUTE_FINITE_SCOPED",
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC346_MAXIMUM_CLAIM": STATUS,
            "TPC346_NESTED_MODEL_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC346_FRESH_PANEL_OWN_FIT": "REFUTED_SCOPED",
            "TPC346_SHARED_THREE_PANEL": "REFUTED_SCOPED",
            "TPC346_PANEL_ADAPTIVE_RAW":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS",
            "TPC346_PANEL_ADAPTIVE_EQUAL_ROW": "REFUTED_SCOPED",
            "TPC346_PANEL_ADAPTIVE_WEIGHTING_STABILITY":
                "REFUTED_SCOPED",
            "TPC346_THIRD_PANEL_TRANSFER": "REFUTED_SCOPED",
            "TPC346_ARITHMETIC_ADVANCE": "NO",
            "TPC346_FIXED_POWER_CREDIT": 0,
            "TPC346_SOURCE_UNIFORM_L2": "OPEN",
            "TPC346_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC346_FULL_GATE_B": "OPEN",
            "TPC346_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue":
            "FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2",
        "weighting_results": weighting_results,
        "rows": [{key: value for key, value in row.items()
                  if not key.startswith("_")} for row in all_rows],
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
            print("TPC346_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC346_CERTIFICATE=PASS panels=3 rows=9 "
                  "raw_records=324 nonempty=261 "
                  "adaptive_raw=0.2999630725662 "
                  "adaptive_equal_row=0.3222362713305 "
                  "fresh_loo_pairs=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC346_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
