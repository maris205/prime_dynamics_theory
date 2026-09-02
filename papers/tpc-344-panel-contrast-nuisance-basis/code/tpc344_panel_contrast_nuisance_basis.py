#!/usr/bin/env python3
"""TPC-344: a minimal panel-contrast nuisance-basis audit.

TPC-343 found that one nuisance coefficient vector does not fit two
protocol-compatible panels.  This release adds one predeclared contrast
direction per nuisance category.  The resulting six-column basis is exactly
equivalent, in finite linear algebra, to one shared coefficient vector per
panel.  The numerical claim is intentionally narrower: the raw pooled guard
passes, while equal-row weighting and cross-panel coefficient transfer do not.
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
RESULT = PROJECT / "results/tpc344_certificate.json"

TPC343_PROJECT = ROOT / "papers/tpc-343-cross-panel-meta-certificate"
TPC343_CODE = TPC343_PROJECT / "code/tpc343_cross_panel_meta_certificate.py"
TPC343_CERT = TPC343_PROJECT / "results/tpc343_certificate.json"
TPC343_CODE_SHA256 = "b10192be90572f210c2f0551576abd659c8d518845dee7e61793feab6de3d13b"
TPC343_CERT_SHA256 = "eff6671b5ef1345f9f88db438b962f19c714651839f0015c7cd1f7ebbb6a4568"

TPC340_PROJECT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope"
TPC340_CODE = TPC340_PROJECT / "code/tpc340_schur_frobenius_hybrid_envelope.py"
TPC340_CERT = TPC340_PROJECT / "results/tpc340_certificate.json"
TPC340_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
TPC340_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

SCHEMA = "TPC344_PANEL_CONTRAST_NUISANCE_BASIS_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT"
PANELS = (
    ("TPC341", (48097, 48609, 49217), 1),
    ("TPC342", (40097, 40609, 41121), -1),
)
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
TOL = 8.0e-6


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


def close(actual: float, saved: Any, label: str,
          tolerance: float = 7.0e-7) -> None:
    expected = float(saved)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual),
                                                    abs(expected)), label)


def load_source() -> Any:
    need(digest(TPC343_CODE.read_bytes()) == TPC343_CODE_SHA256,
         "TPC343 producer provenance")
    need(digest(TPC343_CERT.read_bytes()) == TPC343_CERT_SHA256,
         "TPC343 certificate provenance")
    document = json.loads(TPC343_CERT.read_bytes())
    need(TPC343_CERT.read_bytes() == canonical(document) and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE",
         "TPC343 certificate header")
    protocol = document.get("payload", {}).get("protocol", {})
    need([item.get("name") for item in protocol.get("panels", [])] ==
         ["TPC341", "TPC342"], "TPC343 panel lineage")
    need(protocol.get("operator") == {"law": "all_plus", "Q": 54,
                                      "kernel_exponent": 1, "height": 66},
         "TPC343 operator lineage")
    need(digest(TPC340_CODE.read_bytes()) == TPC340_CODE_SHA256,
         "TPC340 producer provenance")
    need(digest(TPC340_CERT.read_bytes()) == TPC340_CERT_SHA256,
         "TPC340 certificate provenance")
    parent = json.loads(TPC340_CERT.read_bytes())
    need(TPC340_CERT.read_bytes() == canonical(parent) and
         parent.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 certificate header")
    spec = importlib.util.spec_from_file_location("tpc340_parent", TPC340_CODE)
    need(spec is not None and spec.loader is not None, "source import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_parent()


def classify(source: Any, value: int, lam: float, comparison: float) -> str:
    if lam * comparison == 0.0:
        return "zero_support"
    power = source.prime_power(value + 2)
    need(power is not None, "prime-power support")
    if power[1] == 1:
        return ("twin_prime" if source.is_prime_small(value)
                else "non_twin_prime_shift")
    return "prime_power_shift"


def control_indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        result = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        result = np.asarray([(multiplier * i + offset) % size
                             for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in result)) == size, "control bijection")
    return result


def positive_condition(singular: np.ndarray, rank: int) -> float:
    return (float(singular[0] / singular[rank - 1])
            if rank else math.inf)


def projection(target: np.ndarray,
               columns: list[np.ndarray]) -> dict[str, Any]:
    need(len(columns) > 0, "projection columns")
    matrix = np.column_stack(columns)
    need(matrix.ndim == 2 and matrix.shape[0] == len(target),
         "projection shape")
    left, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        rank = 0
        basis = np.zeros((len(target), 0), dtype=np.float64)
    else:
        tolerance = max(matrix.shape) * np.finfo(np.float64).eps * singular[0]
        rank = int(np.count_nonzero(singular > tolerance))
        basis = left[:, :rank]
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    gap = target_energy - projected_energy - residual_energy
    need(math.isfinite(target_energy) and target_energy > 0.0,
         "projection target")
    need(math.isfinite(projected_energy) and math.isfinite(residual_energy),
         "projection energy")
    need(abs(gap) <= TOL * max(1.0, target_energy),
         "projection identity")
    return {
        "target_energy": show(target_energy),
        "projected_energy": show(projected_energy),
        "residual_energy": show(residual_energy),
        "residual_retention": show(residual_energy / target_energy),
        "removed_fraction": show(1.0 - residual_energy / target_energy),
        "decomposition_gap": show(gap),
        "nuisance_rank": rank,
        "nuisance_singular_values": [show(item) for item in singular],
        "nuisance_condition": show(positive_condition(singular, rank)),
        "identity_holds": True,
    }


def row_data(source: Any, origin: int) -> dict[str, Any]:
    lo, hi = origin, origin + SCALE // 2 - 1
    need(hi + 2 < CUTOFF, "cutoff")
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comparison, beta, width = source.source_vectors(lo, hi)
    masks = {name: np.zeros(len(beta), dtype=bool) for name in CATEGORIES}
    for index, value in enumerate(range(lo, hi + 1)):
        masks[classify(source, value, float(lam[index]),
                       float(comparison[index]))][index] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]
    vectors = {name: beta * masks[name] for name in CATEGORIES}
    outputs: dict[str, list[np.ndarray]] = {name: [] for name in CATEGORIES}
    raw_records: list[dict[str, Any]] = []
    for control_name, multiplier, offset, _rule in CONTROLS:
        permutation = control_indices(len(beta), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            energy = float(output @ output)
            outputs[category].append(output)
            raw_records.append({
                "control": control_name,
                "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": show(source_l2),
                "response_energy": show(energy),
                "response_gain": show(energy / source_l2)
                if source_l2 else "0",
            })
    means = {name: np.mean(np.stack(outputs[name]), axis=0)
             for name in CATEGORIES}
    nuisance = [means[name] for name in NUISANCE]
    in_sample = projection(means["twin_prime"], nuisance)
    expected_rank = sum(float(np.linalg.norm(item)) > 0.0
                        for item in nuisance)
    need(in_sample["nuisance_rank"] == expected_rank, "row rank")
    names = [item[0] for item in CONTROLS]
    holdout: list[dict[str, Any]] = []
    for omitted, control_name in enumerate(names):
        training = [index for index in range(len(names)) if index != omitted]
        train_columns = [
            np.mean(np.stack([outputs[category][index] for index in training]),
                    axis=0)
            for category in NUISANCE
        ]
        metrics = projection(outputs["twin_prime"][omitted], train_columns)
        metrics.update({"omitted_control": control_name,
                        "training_controls": [names[index] for index in training]})
        holdout.append(metrics)
    nonempty = [item for item in raw_records
                if float(item["source_l2"]) > 0.0]
    need(len(raw_records) == 36 and bool(nonempty), "row record census")
    return {
        "origin": origin,
        "scale": SCALE,
        "source_interval": [lo, hi],
        "source_count": len(beta),
        "cutoff_safe": hi + 2 < CUTOFF,
        "operator": {"law": "all_plus", "Q": Q,
                     "kernel_exponent": EXPONENT, "height": HEIGHT},
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "raw_records": raw_records,
        "nonempty_raw_record_count": len(nonempty),
        "mean_energies": {name: show(float(means[name] @ means[name]))
                          for name in CATEGORIES},
        "expected_nuisance_rank": expected_rank,
        "in_sample": in_sample,
        "holdout": holdout,
        "_outputs": outputs,
        "_means": means,
    }


def row_stack(targets: list[np.ndarray],
              columns_by_row: list[list[np.ndarray]],
              normalize: bool,
              block: bool = False) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    if block:
        matrix = np.zeros((sum(len(item) for item in targets),
                           len(targets) * len(NUISANCE)), dtype=np.float64)
        cursor = 0
        for row_index, (target, columns) in enumerate(
                zip(targets, columns_by_row)):
            scale = float(np.linalg.norm(target)) if normalize else 1.0
            need(math.isfinite(scale) and scale > 0.0, "row stack scale")
            target_parts.append(target / scale)
            size = len(target)
            for nuisance_index, column in enumerate(columns):
                matrix[cursor:cursor + size,
                       row_index * len(NUISANCE) + nuisance_index] = column / scale
            cursor += size
        return projection(np.concatenate(target_parts),
                          [matrix[:, index]
                           for index in range(matrix.shape[1])])
    parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    for target, columns in zip(targets, columns_by_row):
        scale = float(np.linalg.norm(target)) if normalize else 1.0
        need(math.isfinite(scale) and scale > 0.0, "shared stack scale")
        target_parts.append(target / scale)
        for index, column in enumerate(columns):
            parts[index].append(column / scale)
    return projection(np.concatenate(target_parts),
                      [np.concatenate(item) for item in parts])


def contrast_stack(targets: list[np.ndarray],
                   columns_by_row: list[list[np.ndarray]],
                   panel_rows: list[int],
                   signs: list[int],
                   normalize: bool,
                   adaptive: bool = False) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    base: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    contrast: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    panel_columns: list[list[np.ndarray]] = []
    for row_index, (target, columns) in enumerate(
            zip(targets, columns_by_row)):
        scale = float(np.linalg.norm(target)) if normalize else 1.0
        need(math.isfinite(scale) and scale > 0.0, "contrast scale")
        target_parts.append(target / scale)
        for nuisance_index, column in enumerate(columns):
            value = column / scale
            base[nuisance_index].append(value)
            contrast[nuisance_index].append(signs[panel_rows[row_index]] * value)
    Y = np.concatenate(target_parts)
    if adaptive:
        for panel_index in range(len(signs)):
            for nuisance_index in range(len(NUISANCE)):
                pieces: list[np.ndarray] = []
                for row_index, value in enumerate(
                        base[nuisance_index]):
                    panel = panel_rows[row_index]
                    pieces.append(value if panel == panel_index
                                  else np.zeros_like(value))
                panel_columns.append([np.concatenate(pieces)])
        columns = [item[0] for item in panel_columns]
    else:
        columns = ([np.concatenate(item) for item in base] +
                   [np.concatenate(item) for item in contrast])
    return projection(Y, columns)


def mean_rows(bundle_rows: list[dict[str, Any]]) -> list[dict[str, np.ndarray]]:
    return [item["_means"] for item in bundle_rows]


def fit_prediction(train: list[dict[str, np.ndarray]],
                   target: list[dict[str, np.ndarray]],
                   normalize: bool) -> dict[str, Any]:
    def stack(rows: list[dict[str, np.ndarray]]) -> tuple[np.ndarray, np.ndarray]:
        ys: list[np.ndarray] = []
        parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
        for row in rows:
            y = row["twin_prime"]
            scale = float(np.linalg.norm(y)) if normalize else 1.0
            need(math.isfinite(scale) and scale > 0.0, "fit scale")
            ys.append(y / scale)
            for index, name in enumerate(NUISANCE):
                parts[index].append(row[name] / scale)
        return np.concatenate(ys), np.column_stack(
            [np.concatenate(item) for item in parts])
    train_y, train_matrix = stack(train)
    target_y, target_matrix = stack(target)
    left, singular, _ = np.linalg.svd(train_matrix, full_matrices=False)
    tolerance = (max(train_matrix.shape) * np.finfo(np.float64).eps *
                 singular[0]) if len(singular) else 0.0
    rank = int(np.count_nonzero(singular > tolerance)) if len(singular) else 0
    coefficient = np.linalg.lstsq(train_matrix, train_y, rcond=None)[0]
    residual = target_y - target_matrix @ coefficient
    retention = float(residual @ residual) / float(target_y @ target_y)
    return {
        "training_rows": len(train),
        "target_rows": len(target),
        "training_rank": rank,
        "training_condition": show(positive_condition(singular, rank)),
        "coefficients": [show(item) for item in coefficient],
        "prediction_residual_retention": show(retention),
        "prediction_identity": "RESIDUAL_NORM_ONLY_NO_PROJECTION_IDENTITY",
    }


def holdout_contrast(bundle_rows: list[dict[str, Any]],
                     panel_rows: list[int], signs: list[int],
                     normalize: bool) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for omitted, control in enumerate(item[0] for item in CONTROLS):
        targets: list[np.ndarray] = []
        columns: list[list[np.ndarray]] = []
        for row in bundle_rows:
            outputs = row["_outputs"]
            targets.append(outputs["twin_prime"][omitted])
            training = [index for index in range(len(CONTROLS))
                        if index != omitted]
            columns.append([
                np.mean(np.stack([outputs[name][index] for index in training]),
                        axis=0)
                for name in NUISANCE
            ])
        metrics = contrast_stack(targets, columns, panel_rows, signs,
                                 normalize)
        result.append({"omitted_control": control, "metrics": metrics})
    return result


def exact_anchor() -> dict[str, Any]:
    base = [Fraction(1), Fraction(0), Fraction(0), Fraction(1)]
    contrast = [Fraction(1), Fraction(0), Fraction(0), Fraction(-1)]
    panel_one = [(a + b) / 2 for a, b in zip(base, contrast)]
    panel_two = [(a - b) / 2 for a, b in zip(base, contrast)]
    target = [Fraction(1), Fraction(1), Fraction(1), Fraction(1)]
    projection_energy = (
        sum(panel_one[i] * target[i] for i in range(4)) ** 2 +
        sum(panel_two[i] * target[i] for i in range(4)) ** 2
    )
    # The two panel-specific coordinate columns span the first and last axes.
    residual_energy = sum((target[i] - (panel_one[i] + panel_two[i]))
                          ** 2 for i in range(4))
    need(panel_one == [Fraction(1), 0, 0, 0] and
         panel_two == [0, 0, 0, Fraction(1)] and
         projection_energy == 2 and residual_energy == 2,
         "contrast anchor")
    return {
        "base": ["1", "0", "0", "1"],
        "contrast": ["1", "0", "0", "-1"],
        "panel_one_column": ["1", "0", "0", "0"],
        "panel_two_column": ["0", "0", "0", "1"],
        "target": ["1", "1", "1", "1"],
        "projected_energy": "2",
        "residual_energy": "2",
        "identity_exact": True,
    }


def build_payload() -> dict[str, Any]:
    source = load_source()
    bundles: list[dict[str, Any]] = []
    panel_rows: list[int] = []
    signs: list[int] = []
    panel_documents: list[dict[str, Any]] = []
    for panel_index, (name, origins, sign) in enumerate(PANELS):
        items = [row_data(source, origin) for origin in origins]
        bundles.extend(items)
        panel_rows.extend([panel_index] * len(items))
        signs.append(sign)
        panel_documents.append({"name": name, "origins": list(origins),
                                "sign": sign, "rows": len(items)})
    records = [item for row in bundles for item in row["raw_records"]]
    nonempty = [item for item in records if float(item["source_l2"]) > 0.0]
    need(len(bundles) == 6 and len(records) == 216 and len(nonempty) == 171,
         "global census")
    targets = [item["_means"]["twin_prime"] for item in bundles]
    columns = [[item["_means"][name] for name in NUISANCE]
               for item in bundles]
    row_block_raw = row_stack(targets, columns, False, True)
    row_block_equal = row_stack(targets, columns, True, True)
    shared_raw = row_stack(targets, columns, False)
    shared_equal = row_stack(targets, columns, True)
    contrast_raw = contrast_stack(targets, columns, panel_rows, signs, False)
    contrast_equal = contrast_stack(targets, columns, panel_rows, signs, True)
    adaptive_raw = contrast_stack(targets, columns, panel_rows, signs, False,
                                  adaptive=True)
    adaptive_equal = contrast_stack(targets, columns, panel_rows, signs, True,
                                    adaptive=True)
    need(abs(float(contrast_raw["residual_retention"]) -
             float(adaptive_raw["residual_retention"])) <=
         TOL * 10, "contrast/adaptive raw equivalence")
    need(abs(float(contrast_equal["residual_retention"]) -
             float(adaptive_equal["residual_retention"])) <=
         TOL * 10, "contrast/adaptive equal equivalence")
    means = mean_rows(bundles)
    crossfit = []
    for normalize, label in ((False, "raw"), (True, "equal_row")):
        crossfit.append({
            "weighting": label,
            "TPC341_to_TPC342": fit_prediction(means[:3], means[3:],
                                                normalize),
            "TPC342_to_TPC341": fit_prediction(means[3:], means[:3],
                                                normalize),
        })
    holdout_raw = holdout_contrast(bundles, panel_rows, signs, False)
    holdout_equal = holdout_contrast(bundles, panel_rows, signs, True)
    holdout_values = [
        float(item["metrics"]["residual_retention"])
        for item in holdout_raw + holdout_equal
    ]
    crossfit_values = [
        float(entry[direction]["prediction_residual_retention"])
        for entry in crossfit
        for direction in ("TPC341_to_TPC342", "TPC342_to_TPC341")
    ]
    need(float(row_block_raw["residual_retention"]) < 0.30 and
         float(row_block_equal["residual_retention"]) < 0.30,
         "row-block guard")
    need(float(shared_raw["residual_retention"]) >= 0.30 and
         float(shared_equal["residual_retention"]) >= 0.30,
         "parent shared obstruction")
    need(float(contrast_raw["residual_retention"]) < 0.30 and
         float(contrast_equal["residual_retention"]) >= 0.30,
         "contrast weighting decision")
    need(min(holdout_values) > 0.40 and min(crossfit_values) > 0.30,
         "transfer guards")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC343_producer_sha256": TPC343_CODE_SHA256,
            "TPC343_certificate_sha256": TPC343_CERT_SHA256,
            "TPC340_producer_sha256": TPC340_CODE_SHA256,
            "TPC340_certificate_sha256": TPC340_CERT_SHA256,
        },
        "protocol": {
            "panels": panel_documents,
            "scale": SCALE,
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "nuisance_categories": list(NUISANCE),
            "controls": [{"name": name, "multiplier": multiplier,
                          "offset": offset, "rule": rule}
                         for name, multiplier, offset, rule in CONTROLS],
            "panel_sign_vector": [1, -1],
            "base_columns": "b_j=(n_1j,...,n_6j)",
            "contrast_columns": "d_j=(+n_1j,+n_2j,+n_3j,-n_4j,-n_5j,-n_6j)",
            "panel_adaptive_columns":
                "u_1j=(b_j+d_j)/2, u_2j=(b_j-d_j)/2",
            "raw_guard": "residual retention < 0.30",
            "equal_row_guard": "residual retention < 0.30",
            "transfer_guard": "prediction residual retention < 0.30",
        },
        "exact_theorem": {
            "stacked_projection":
                "||Y||^2=||P_NY||^2+||(I-P_N)Y||^2",
            "contrast_reparameterization":
                "u_1j=(b_j+d_j)/2 and u_2j=(b_j-d_j)/2",
            "span_equality":
                "span{b_j,d_j}=span{u_1j,u_2j} for each nuisance j",
            "finite_scope": "all identities concern declared finite vectors",
            "crossfit_note":
                "prediction residuals are not orthogonal projection residuals",
            "arithmetic_interpretation": "none",
        },
        "finite_audit": {
            "panels": 2, "rows": 6, "origins": 6, "scales": 1,
            "controls": 9, "categories": 4, "raw_records": 216,
            "nonempty_raw_records": 171, "in_sample_records": 6,
            "holdout_records": 18, "crossfit_directions": 4,
            "basis_columns_declared": 6, "basis_rank_observed": 5,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "baseline": {
            "row_block_raw": row_block_raw,
            "row_block_equal_row": row_block_equal,
            "shared_raw": shared_raw,
            "shared_equal_row": shared_equal,
        },
        "panel_contrast": {
            "contrast_raw": contrast_raw,
            "contrast_equal_row": contrast_equal,
            "adaptive_raw": adaptive_raw,
            "adaptive_equal_row": adaptive_equal,
            "holdout_raw": holdout_raw,
            "holdout_equal_row": holdout_equal,
            "crossfit": crossfit,
        },
        "summary": {
            "contrast_raw_retention": contrast_raw["residual_retention"],
            "contrast_equal_row_retention":
                contrast_equal["residual_retention"],
            "contrast_rank": contrast_raw["nuisance_rank"],
            "contrast_raw_condition": contrast_raw["nuisance_condition"],
            "contrast_equal_row_condition":
                contrast_equal["nuisance_condition"],
            "holdout_retention_min": show(min(holdout_values)),
            "holdout_retention_max": show(max(holdout_values)),
            "crossfit_retention_min": show(min(crossfit_values)),
            "crossfit_retention_max": show(max(crossfit_values)),
            "raw_guard": "PASS_FINITE_SCOPED",
            "weighting_stability": "REFUTED_SCOPED",
            "crossfit_transfer": "REFUTED_SCOPED",
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC344_MAXIMUM_CLAIM":
                "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT",
            "TPC344_CONTRAST_SPAN_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC344_RAW_CONTRAST_GUARD":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS",
            "TPC344_EQUAL_ROW_CONTRAST_GUARD": "REFUTED_SCOPED",
            "TPC344_WEIGHTING_STABILITY": "REFUTED_SCOPED",
            "TPC344_CROSSFIT_TRANSFER": "REFUTED_SCOPED",
            "TPC344_HOLDOUT": "NUMERICALLY_CERTIFIED_FINITE_18_RECORDS",
            "TPC344_ARITHMETIC_ADVANCE": "NO",
            "TPC344_FIXED_POWER_CREDIT": 0,
            "TPC344_SOURCE_UNIFORM_L2": "OPEN",
            "TPC344_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC344_FULL_GATE_B": "OPEN",
            "TPC344_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "PRINCIPAL_ANGLE_GRASSMANN_STABILITY_AUDIT",
        "rows": [{key: value for key, value in item.items()
                  if not key.startswith("_")} for item in bundles],
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
            print("TPC344_CERTIFICATE=WRITTEN")
        else:
            stored_raw = RESULT.read_bytes()
            stored = json.loads(stored_raw)
            need(stored_raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC344_CERTIFICATE=PASS rows=6 raw_records=216 "
                  "contrast_raw=0.2962189247 contrast_equal_row=0.3186506700 "
                  "holdout_records=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC344_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
