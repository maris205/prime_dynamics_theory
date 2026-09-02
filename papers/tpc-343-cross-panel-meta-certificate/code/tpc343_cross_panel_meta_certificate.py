#!/usr/bin/env python3
"""TPC-343: a cross-panel shared-nuisance meta-certificate.

The TPC-341 protocol and its TPC-342 independent reproduction are treated as
two locked finite panels.  This release compares two explicitly different
stacking models: row-block nuisance coefficients (one coefficient vector per
row) and a shared coefficient vector across all six rows.  The comparison is
descriptive finite linear algebra; it carries no arithmetic credit.
"""

from __future__ import annotations

import argparse
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
RESULT = PROJECT / "results/tpc343_certificate.json"

PARENT_PROJECT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope"
PARENT_CODE = PARENT_PROJECT / "code/tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc340_certificate.json"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

TPC341_PROJECT = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization"
TPC341_CODE = TPC341_PROJECT / "code/tpc341_fresh_holdout_nuisance_orthogonalization.py"
TPC341_CERT = TPC341_PROJECT / "results/tpc341_certificate.json"
TPC341_CODE_SHA256 = "66269d586493a51adefeb8f17638df6b2eccf7e55aeab83e099b26c7768d52ac"
TPC341_CERT_SHA256 = "50f8f81f4c401924187ae90327cf787139489570cbda68707b846e3d89f36218"

TPC342_PROJECT = ROOT / "papers/tpc-342-independent-fresh-holdout-reproduction"
TPC342_CODE = TPC342_PROJECT / "code/tpc342_independent_fresh_holdout_reproduction.py"
TPC342_CERT = TPC342_PROJECT / "results/tpc342_certificate.json"
TPC342_CODE_SHA256 = "1c57ccd3519f20f9283b0a4f678bd2b0f81ef60e94b9db7780f4f263684e6014"
TPC342_CERT_SHA256 = "7dbb39b8d38ef5d09a7b21e829d2e70469f7e9e2a1e1b135588c1413fb7cd52f"

SCHEMA = "TPC343_CROSS_PANEL_META_CERTIFICATE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE"
PANELS = (
    ("TPC341", (48097, 48609, 49217), TPC341_CERT,
     "NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION",
     [48097, 48609, 49217]),
    ("TPC342", (40097, 40609, 41121), TPC342_CERT,
     "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION",
     [40097, 40609, 41121]),
)
SCALES = (1024,)
Q = 54
EXPONENT = 1
HEIGHT = 66
CUTOFF = 50_000
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")
NUISANCE_CATEGORIES = ("non_twin_prime_shift", "prime_power_shift",
                        "zero_support")
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
RANK_TOL_FACTOR = 1.0


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
         "TPC340 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC340 certificate provenance")
    document = json.loads(PARENT_CERT.read_bytes())
    need(PARENT_CERT.read_bytes() == canonical(document) and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 certificate header")
    for _name, _origins, cert, status, expected in PANELS:
        need(cert.is_file(), "panel certificate missing")
        panel_document = json.loads(cert.read_bytes())
        need(cert.read_bytes() == canonical(panel_document) and
             panel_document.get("claim_status") == status,
             "panel certificate header")
        protocol = panel_document.get("payload", {}).get("protocol", {})
        need(protocol.get("origins") == expected and
             protocol.get("scales") == [1024], "panel protocol lock")
    spec = importlib.util.spec_from_file_location("tpc340_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_parent()


def verify_panel_sources() -> None:
    need(digest(TPC341_CODE.read_bytes()) == TPC341_CODE_SHA256,
         "TPC341 producer provenance")
    need(digest(TPC341_CERT.read_bytes()) == TPC341_CERT_SHA256,
         "TPC341 certificate provenance")
    need(digest(TPC342_CODE.read_bytes()) == TPC342_CODE_SHA256,
         "TPC342 producer provenance")
    need(digest(TPC342_CERT.read_bytes()) == TPC342_CERT_SHA256,
         "TPC342 certificate provenance")


def classify(source: Any, value: int, lam: float, comparison: float) -> str:
    if lam * comparison == 0.0:
        return "zero_support"
    power = source.prime_power(value + 2)
    need(power is not None, "prime-power support")
    if power[1] == 1:
        return "twin_prime" if source.is_prime_small(value) else \
            "non_twin_prime_shift"
    return "prime_power_shift"


def control_indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        result = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        result = np.asarray([(multiplier * i + offset) % size
                             for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in result)) == size, "control bijection")
    return result


def projection_metrics(target: np.ndarray,
                        columns: list[np.ndarray]) -> dict[str, Any]:
    need(len(columns) > 0, "projection columns")
    matrix = np.column_stack(columns)
    need(matrix.ndim == 2 and matrix.shape[0] == len(target),
         "projection matrix shape")
    basis_all, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        rank = 0
        basis = np.zeros((len(target), 0), dtype=np.float64)
    else:
        tolerance = (RANK_TOL_FACTOR * max(matrix.shape) *
                     np.finfo(np.float64).eps * singular[0])
        rank = int(np.sum(singular > tolerance))
        basis = basis_all[:, :rank]
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    need(math.isfinite(target_energy) and target_energy > 0.0,
         "projection target")
    need(math.isfinite(projected_energy) and math.isfinite(residual_energy),
         "projection energy")
    gap = target_energy - projected_energy - residual_energy
    need(abs(gap) <= NUMERIC_TOL * max(1.0, target_energy),
         "projection Pythagorean identity")
    condition = (float(singular[0] / singular[rank - 1])
                 if rank else math.inf)
    return {
        "target_energy": show(target_energy),
        "projected_energy": show(projected_energy),
        "residual_energy": show(residual_energy),
        "residual_retention": show(residual_energy / target_energy),
        "removed_fraction": show(1.0 - residual_energy / target_energy),
        "decomposition_gap": show(gap),
        "nuisance_rank": rank,
        "nuisance_singular_values": [show(item) for item in singular],
        "nuisance_condition": show(condition),
        "identity_holds": True,
    }


def row_data(source: Any, origin: int, scale: int) -> tuple[dict[str, Any],
                                                               dict[str, list[np.ndarray]],
                                                               dict[str, np.ndarray]]:
    lo, hi = origin, origin + scale // 2 - 1
    need(hi + 2 < CUTOFF, "row exceeds cutoff")
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comparison, residual, _width = source.source_vectors(lo, hi)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[classify(source, value, float(lam[i]),
                       float(comparison[i]))][i] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs: dict[str, list[np.ndarray]] = {name: [] for name in CATEGORIES}
    raw_records: list[dict[str, Any]] = []
    for control_name, multiplier, offset, _rule in CONTROLS:
        permutation = control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            response_energy = float(output @ output)
            outputs[category].append(output)
            raw_records.append({
                "control": control_name, "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": show(source_l2),
                "response_energy": show(response_energy),
                "response_gain": show(response_energy / source_l2)
                if source_l2 else "0",
            })
    means = {name: np.mean(np.stack(outputs[name]), axis=0)
             for name in CATEGORIES}
    nuisance_means = [means[name] for name in NUISANCE_CATEGORIES]
    in_sample = projection_metrics(means["twin_prime"], nuisance_means)
    expected_rank = sum(float(np.linalg.norm(item)) > 0.0
                        for item in nuisance_means)
    need(in_sample["nuisance_rank"] == expected_rank, "row rank")
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
    nonempty = [item for item in raw_records
                if float(item["source_l2"]) > 0.0]
    need(len(raw_records) == 36 and bool(nonempty), "row record census")
    record = {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(residual),
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
    }
    return record, outputs, means


def common_metrics(rows: list[tuple[dict[str, Any], dict[str, list[np.ndarray]],
                                  dict[str, np.ndarray]]],
                   targets: list[np.ndarray],
                   nuisance_blocks: list[list[np.ndarray]],
                   normalize: bool) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    column_parts: list[list[np.ndarray]] = [[] for _ in NUISANCE_CATEGORIES]
    for target, columns in zip(targets, nuisance_blocks):
        scale = float(np.linalg.norm(target)) if normalize else 1.0
        need(math.isfinite(scale) and scale > 0.0, "meta target norm")
        target_parts.append(target / scale)
        for index, column in enumerate(columns):
            column_parts[index].append(column / scale)
    return projection_metrics(np.concatenate(target_parts),
                              [np.concatenate(parts) for parts in column_parts])


def block_metrics(targets: list[np.ndarray],
                  nuisance_blocks: list[list[np.ndarray]],
                  normalize: bool) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    total = sum(len(target) for target in targets)
    columns = np.zeros((total, len(targets) * len(NUISANCE_CATEGORIES)),
                       dtype=np.float64)
    cursor = 0
    for row_index, (target, row_columns) in enumerate(zip(targets,
                                                            nuisance_blocks)):
        scale = float(np.linalg.norm(target)) if normalize else 1.0
        need(math.isfinite(scale) and scale > 0.0, "block target norm")
        target_parts.append(target / scale)
        size = len(target)
        for nuisance_index, column in enumerate(row_columns):
            columns[cursor:cursor + size,
                    row_index * len(NUISANCE_CATEGORIES) + nuisance_index] = \
                column / scale
        cursor += size
    return projection_metrics(np.concatenate(target_parts),
                              [columns[:, index]
                               for index in range(columns.shape[1])])


def weighted_metrics(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    target = sum(float(item["target_energy"]) for item in metrics)
    projected = sum(float(item["projected_energy"]) for item in metrics)
    residual = sum(float(item["residual_energy"]) for item in metrics)
    gap = target - projected - residual
    need(target > 0.0 and math.isfinite(target), "weighted target")
    return {
        "target_energy": show(target),
        "projected_energy": show(projected),
        "residual_energy": show(residual),
        "residual_retention": show(residual / target),
        "removed_fraction": show(1.0 - residual / target),
        "decomposition_gap": show(gap),
        "component_count": len(metrics),
        "identity_holds": abs(gap) <= NUMERIC_TOL * max(1.0, target),
    }


def exact_anchor() -> dict[str, Any]:
    # Y=(1,1,1,1), n=(1,0,1,0): the shared projection has energy 2.
    target = [1, 1, 1, 1]
    nuisance = [1, 0, 1, 0]
    target_energy = sum(item * item for item in target)
    nuisance_energy = sum(item * item for item in nuisance)
    coefficient = sum(a * b for a, b in zip(target, nuisance)) // nuisance_energy
    projected = [coefficient * item for item in nuisance]
    projected_energy = sum(item * item for item in projected)
    residual_energy = target_energy - projected_energy
    need((target_energy, projected_energy, residual_energy) == (4, 2, 2),
         "exact stacking anchor")
    return {"target": target, "shared_nuisance": nuisance,
            "target_energy": "4", "projected_energy": "2",
            "residual_energy": "2", "residual_retention": "1/2",
            "identity_exact": True}


def build_payload() -> dict[str, Any]:
    verify_panel_sources()
    source = load_parent()
    row_triplets: list[tuple[dict[str, Any], dict[str, list[np.ndarray]],
                             dict[str, np.ndarray]]] = []
    panel_rows: dict[str, list[tuple[dict[str, Any], dict[str, list[np.ndarray]],
                                    dict[str, np.ndarray]]]] = {}
    for panel_name, origins, _cert, _status, expected in PANELS:
        need(list(origins) == expected, "panel origin declaration")
        items = [row_data(source, origin, 1024) for origin in origins]
        panel_rows[panel_name] = items
        row_triplets.extend(items)
    records = [item[0] for item in row_triplets]
    raw = [entry for row in records for entry in row["raw_records"]]
    nonempty = [entry for entry in raw if float(entry["source_l2"]) > 0.0]
    need(len(records) == 6 and len(raw) == 216 and len(nonempty) == 171,
         "global raw census")

    in_targets = [item[2]["twin_prime"] for item in row_triplets]
    in_columns = [[item[2][name] for name in NUISANCE_CATEGORIES]
                  for item in row_triplets]
    local_raw = block_metrics(in_targets, in_columns, normalize=False)
    local_equal = block_metrics(in_targets, in_columns, normalize=True)
    shared_raw = common_metrics(row_triplets, in_targets, in_columns,
                                normalize=False)
    shared_equal = common_metrics(row_triplets, in_targets, in_columns,
                                  normalize=True)

    panel_meta: dict[str, Any] = {}
    for panel_name, items in panel_rows.items():
        targets = [item[2]["twin_prime"] for item in items]
        columns = [[item[2][name] for name in NUISANCE_CATEGORIES]
                   for item in items]
        panel_meta[panel_name] = {
            "row_block": block_metrics(targets, columns, False),
            "shared_raw": common_metrics(items, targets, columns, False),
            "shared_equal_row": common_metrics(items, targets, columns, True),
        }

    holdout_common_raw: list[dict[str, Any]] = []
    holdout_common_equal: list[dict[str, Any]] = []
    holdout_block_components: list[dict[str, Any]] = []
    control_names = [item[0] for item in CONTROLS]
    for omitted, control_name in enumerate(control_names):
        targets: list[np.ndarray] = []
        columns: list[list[np.ndarray]] = []
        for _record, outputs, _means in row_triplets:
            targets.append(outputs["twin_prime"][omitted])
            training = [index for index in range(len(CONTROLS))
                        if index != omitted]
            columns.append([
                np.mean(np.stack([outputs[category][index]
                                  for index in training]), axis=0)
                for category in NUISANCE_CATEGORIES])
        holdout_common_raw.append({
            "omitted_control": control_name,
            "metrics": common_metrics(row_triplets, targets, columns, False),
        })
        holdout_common_equal.append({
            "omitted_control": control_name,
            "metrics": common_metrics(row_triplets, targets, columns, True),
        })
        for target, row_columns in zip(targets, columns):
            holdout_block_components.append(
                projection_metrics(target, row_columns))

    holdout_weighted = weighted_metrics(holdout_block_components)
    all_holdout = [entry for row in records for entry in row["holdout"]]
    in_sample = [row["in_sample"] for row in records]
    need(len(all_holdout) == 54 and len(in_sample) == 6,
         "meta projection census")
    holdout_retention = [float(item["residual_retention"])
                         for item in all_holdout]

    # These are predeclared model-comparison decisions.  The local row-block
    # model passes, while a single shared coefficient vector fails under both
    # raw-energy and equal-row weighting.
    need(float(local_raw["residual_retention"]) < 0.30 and
         float(local_equal["residual_retention"]) < 0.30,
         "row-block meta guard")
    need(float(shared_raw["residual_retention"]) >= 0.30 and
         float(shared_equal["residual_retention"]) >= 0.30,
         "shared-coefficient obstruction disappeared")
    need(min(holdout_retention) > 0.40 and
         min(float(item["metrics"]["residual_retention"])
             for item in holdout_common_raw) > 0.40,
         "holdout meta guard")

    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC340_producer_sha256": PARENT_CODE_SHA256,
            "TPC340_certificate_sha256": PARENT_CERT_SHA256,
            "TPC341_producer_sha256": TPC341_CODE_SHA256,
            "TPC341_certificate_sha256": TPC341_CERT_SHA256,
            "TPC342_producer_sha256": TPC342_CODE_SHA256,
            "TPC342_certificate_sha256": TPC342_CERT_SHA256,
        },
        "protocol": {
            "panels": [{"name": name, "origins": list(origins),
                         "scale": 1024, "certificate_status": status}
                        for name, origins, _cert, status, _expected in PANELS],
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "nuisance_categories": list(NUISANCE_CATEGORIES),
            "controls": [{"name": name, "multiplier": multiplier,
                          "offset": offset, "rule": rule}
                         for name, multiplier, offset, rule in CONTROLS],
            "row_block_model":
                "one nuisance coefficient vector per source row",
            "shared_model":
                "one common nuisance coefficient vector across all six rows",
            "equal_row_normalization":
                "divide each target and its nuisance columns by target L2 norm",
            "in_sample_guard": "residual retention < 0.30",
            "holdout_guard": "residual retention > 0.40",
        },
        "exact_theorem": {
            "stacked_projection":
                "||Y||^2=||P_NY||^2+||(I-P_N)Y||^2",
            "row_block_projection":
                "block-diagonal nuisance spans add their energies exactly",
            "shared_projection":
                "concatenated nuisance columns use one coefficient vector",
            "finite_scope": "all statements concern finite declared vectors",
            "arithmetic_interpretation":
                "none without a growing source-uniform estimate",
        },
        "finite_audit": {
            "panels": 2, "rows": 6, "origins": 6, "scales": 1,
            "controls": 9, "categories": 4, "raw_records": 216,
            "nonempty_raw_records": 171, "in_sample_records": 6,
            "holdout_records": 54, "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "panel_meta": panel_meta,
        "meta": {
            "row_block_raw": local_raw,
            "row_block_equal_row": local_equal,
            "shared_raw": shared_raw,
            "shared_equal_row": shared_equal,
            "holdout_row_block_weighted": holdout_weighted,
            "holdout_shared_raw": holdout_common_raw,
            "holdout_shared_equal_row": holdout_common_equal,
        },
        "summary": {
            "in_sample_retention_min": show(min(float(item["residual_retention"])
                                                 for item in in_sample)),
            "in_sample_retention_max": show(max(float(item["residual_retention"])
                                                 for item in in_sample)),
            "holdout_retention_min": show(min(holdout_retention)),
            "holdout_retention_max": show(max(holdout_retention)),
            "row_block_meta_retention": local_raw["residual_retention"],
            "shared_raw_meta_retention": shared_raw["residual_retention"],
            "shared_equal_row_meta_retention": shared_equal["residual_retention"],
            "shared_holdout_raw_min": show(min(
                float(item["metrics"]["residual_retention"])
                for item in holdout_common_raw)),
            "shared_holdout_raw_max": show(max(
                float(item["metrics"]["residual_retention"])
                for item in holdout_common_raw)),
            "shared_coefficient_guard": "REFUTED_SCOPED",
            "row_block_guard": "PASS_FINITE",
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC343_STACKED_IDENTITY": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC343_ROW_BLOCK_META":
                "NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION",
            "TPC343_SHARED_COEFFICIENT_RAW": "NUMERICAL_OBSERVATION_0.319_TO_0.320",
            "TPC343_SHARED_COEFFICIENT_EQUAL_ROW":
                "NUMERICAL_OBSERVATION_0.354_TO_0.355",
            "TPC343_SHARED_COEFFICIENT_STABILITY": "REFUTED_SCOPED",
            "TPC343_HOLDOUT_META": "NUMERICALLY_CERTIFIED_FINITE_54_RECORDS",
            "TPC343_ARITHMETIC_ADVANCE": "NO",
            "TPC343_FIXED_POWER_CREDIT": 0,
            "TPC343_SOURCE_UNIFORM_L2": "OPEN",
            "TPC343_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC343_FULL_GATE_B": "OPEN",
            "TPC343_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "ALTERNATIVE_NUISANCE_BASIS_OR_PRINCIPAL_ANGLE_AUDIT",
        "rows": records,
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
            print("TPC343_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "TPC343 certificate does not replay")
            print("TPC343_CERTIFICATE=PASS panels=2 rows=6 controls=9 "
                  "raw_records=216 holdout_records=54 shared_guard=REFUTED_SCOPED")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC343_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
