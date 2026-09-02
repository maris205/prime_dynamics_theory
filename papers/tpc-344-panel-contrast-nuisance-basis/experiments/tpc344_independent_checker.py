#!/usr/bin/env python3
"""Independent reverse-shell checker for TPC-344.

The producer is never imported.  Source vectors and the all-plus operator are
rebuilt through the hash-locked reverse engine used by the earlier finite
certificate, while every projection, contrast column, holdout, and cross-fit
calculation is reimplemented here.
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
RESULT = PROJECT / "results/tpc344_certificate.json"
PRODUCER = PROJECT / "code/tpc344_panel_contrast_nuisance_basis.py"

ENGINE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py"
ENGINE_SHA256 = "4cff79b0f5c300357af4889e87a0734bbfdcc7f538ee19d313d8f2176a1b583c"
TPC343_CODE = ROOT / "papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py"
TPC343_CERT = ROOT / "papers/tpc-343-cross-panel-meta-certificate/results/tpc343_certificate.json"
TPC343_CODE_SHA256 = "b10192be90572f210c2f0551576abd659c8d518845dee7e61793feab6de3d13b"
TPC343_CERT_SHA256 = "eff6671b5ef1345f9f88db438b962f19c714651839f0015c7cd1f7ebbb6a4568"
TPC340_CODE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py"
TPC340_CERT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/results/tpc340_certificate.json"
TPC340_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
TPC340_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

SCHEMA = "TPC344_PANEL_CONTRAST_NUISANCE_BASIS_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT"
ORIGINS = (48097, 48609, 49217, 40097, 40609, 41121)
PANEL_ROWS = (0, 0, 0, 1, 1, 1)
PANEL_SIGNS = (1, -1)
SCALE = 1024
Q = 54
EXPONENT = 1
HEIGHT = 66
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")
NUISANCE = ("non_twin_prime_shift", "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0),
    ("affine_3_11", 3, 11),
    ("affine_5_17", 5, 17),
    ("affine_7_29", 7, 29),
    ("reversal", -1, -1),
    ("affine_9_1", 9, 1),
    ("affine_11_13", 11, 13),
    ("affine_13_17", 13, 17),
    ("affine_17_19", 17, 19),
)
TOL = 9.0e-6


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


def close(actual: float, saved: Any, label: str,
          tolerance: float = 8.0e-7) -> None:
    expected = float(saved)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual),
                                                    abs(expected)), label)


def positive_condition(singular: np.ndarray, rank: int) -> float:
    return (float(singular[0] / singular[rank - 1])
            if rank else math.inf)


def projection(target: np.ndarray,
               columns: list[np.ndarray]) -> dict[str, Any]:
    need(len(columns) > 0, "projection columns")
    matrix = np.column_stack(columns)
    left, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        rank = 0
        basis = np.zeros((len(target), 0), dtype=np.float64)
    else:
        threshold = max(matrix.shape) * np.finfo(np.float64).eps * singular[0]
        rank = int(np.count_nonzero(singular > threshold))
        basis = left[:, :rank]
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    gap = target_energy - projected_energy - residual_energy
    need(target_energy > 0.0 and math.isfinite(target_energy),
         "projection target")
    need(math.isfinite(projected_energy) and math.isfinite(residual_energy),
         "projection energy")
    need(abs(gap) <= TOL * max(1.0, target_energy),
         "projection identity")
    return {
        "target_energy": format(target_energy, ".17g"),
        "projected_energy": format(projected_energy, ".17g"),
        "residual_energy": format(residual_energy, ".17g"),
        "residual_retention": format(residual_energy / target_energy, ".17g"),
        "removed_fraction": format(1.0 - residual_energy / target_energy,
                                   ".17g"),
        "decomposition_gap": format(gap, ".17g"),
        "nuisance_rank": rank,
        "nuisance_singular_values": [format(item, ".17g")
                                     for item in singular],
        "nuisance_condition": format(positive_condition(singular, rank),
                                     ".17g"),
        "identity_holds": True,
    }


def check_path(path: Path, expected: str, label: str) -> None:
    need(path.is_file() and digest(path.read_bytes()) == expected,
         label + " provenance")


PRODUCER_SHA256 = "08daa3e1b5782e619f492039ed0b8f734de923dfc39797d88eea8a5650ce83ba"


def load_reverse_engine() -> Any:
    need(digest(PRODUCER.read_bytes()) == PRODUCER_SHA256,
         "TPC344 producer provenance")
    check_path(ENGINE, ENGINE_SHA256, "reverse engine")
    check_path(TPC343_CODE, TPC343_CODE_SHA256, "TPC343 producer")
    check_path(TPC343_CERT, TPC343_CERT_SHA256, "TPC343 certificate")
    check_path(TPC340_CODE, TPC340_CODE_SHA256, "TPC340 producer")
    check_path(TPC340_CERT, TPC340_CERT_SHA256, "TPC340 certificate")
    prior = json.loads(TPC343_CERT.read_bytes())
    need(TPC343_CERT.read_bytes() == canonical(prior) and
         prior.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE",
         "TPC343 header")
    parent = json.loads(TPC340_CERT.read_bytes())
    need(TPC340_CERT.read_bytes() == canonical(parent) and
         parent.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 header")
    spec = importlib.util.spec_from_file_location("tpc340_reverse_checker",
                                                  ENGINE)
    need(spec is not None and spec.loader is not None, "engine spec")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker.load_engine()


def row_data(engine: Any, origin: int) -> dict[str, Any]:
    lo, hi = origin, origin + SCALE // 2 - 1
    lam, comparison, residual = engine.source_arrays(lo, hi)
    matrix = engine.reverse_matrix(origin, SCALE)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for index, value in enumerate(range(lo, hi + 1)):
        category = engine.category(value, float(lam[index]),
                                   float(comparison[index]))
        masks[category][index] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs: dict[str, list[np.ndarray]] = {name: [] for name in CATEGORIES}
    raw: list[dict[str, Any]] = []
    for control, multiplier, offset in CONTROLS:
        permutation = engine.control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            response = matrix @ placed
            energy = float(response @ response)
            outputs[category].append(response)
            raw.append({
                "control": control,
                "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": source_l2,
                "response_energy": energy,
                "response_gain": energy / source_l2 if source_l2 else 0.0,
            })
    means = {name: np.mean(np.stack(outputs[name]), axis=0)
             for name in CATEGORIES}
    nuisance = [means[name] for name in NUISANCE]
    in_sample = projection(means["twin_prime"], nuisance)
    rank = sum(float(np.linalg.norm(item)) > 0.0 for item in nuisance)
    need(in_sample["nuisance_rank"] == rank, "row rank")
    holdout: list[dict[str, Any]] = []
    controls = [item[0] for item in CONTROLS]
    for omitted, control in enumerate(controls):
        training = [i for i in range(len(controls)) if i != omitted]
        nuisance_holdout = [
            np.mean(np.stack([outputs[name][i] for i in training]), axis=0)
            for name in NUISANCE
        ]
        metric = projection(outputs["twin_prime"][omitted],
                            nuisance_holdout)
        metric.update({"omitted_control": control,
                       "training_controls": [controls[i] for i in training]})
        holdout.append(metric)
    return {
        "origin": origin,
        "scale": SCALE,
        "source_interval": [lo, hi],
        "source_count": len(residual),
        "cutoff_safe": hi + 2 < 50_000,
        "operator": {"law": "all_plus", "Q": Q,
                     "kernel_exponent": EXPONENT, "height": HEIGHT},
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "raw_records": raw,
        "nonempty_raw_record_count": sum(
            float(item["source_l2"]) > 0.0 for item in raw),
        "mean_energies": {name: format(float(means[name] @ means[name]),
                                       ".17g")
                          for name in CATEGORIES},
        "expected_nuisance_rank": rank,
        "in_sample": in_sample,
        "holdout": holdout,
        "_outputs": outputs,
        "_means": means,
    }


def stack(targets: list[np.ndarray],
          columns: list[list[np.ndarray]],
          normalize: bool,
          block: bool = False) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    if block:
        total = sum(len(item) for item in targets)
        matrix = np.zeros((total, len(targets) * len(NUISANCE)),
                          dtype=np.float64)
        cursor = 0
        for row, (target, row_columns) in enumerate(zip(targets, columns)):
            scale = float(np.linalg.norm(target)) if normalize else 1.0
            need(scale > 0.0 and math.isfinite(scale), "block scale")
            target_parts.append(target / scale)
            size = len(target)
            for j, column in enumerate(row_columns):
                matrix[cursor:cursor + size,
                       row * len(NUISANCE) + j] = column / scale
            cursor += size
        return projection(np.concatenate(target_parts),
                          [matrix[:, j] for j in range(matrix.shape[1])])
    parts = [[] for _ in NUISANCE]
    for target, row_columns in zip(targets, columns):
        scale = float(np.linalg.norm(target)) if normalize else 1.0
        need(scale > 0.0 and math.isfinite(scale), "shared scale")
        target_parts.append(target / scale)
        for j, column in enumerate(row_columns):
            parts[j].append(column / scale)
    return projection(np.concatenate(target_parts),
                      [np.concatenate(item) for item in parts])


def contrast(targets: list[np.ndarray],
             columns: list[list[np.ndarray]],
             normalize: bool,
             adaptive: bool = False) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    base = [[] for _ in NUISANCE]
    signed = [[] for _ in NUISANCE]
    for row, (target, row_columns) in enumerate(zip(targets, columns)):
        scale = float(np.linalg.norm(target)) if normalize else 1.0
        need(scale > 0.0 and math.isfinite(scale), "contrast scale")
        target_parts.append(target / scale)
        for j, column in enumerate(row_columns):
            value = column / scale
            base[j].append(value)
            signed[j].append(PANEL_SIGNS[PANEL_ROWS[row]] * value)
    y = np.concatenate(target_parts)
    if not adaptive:
        matrix_columns = ([np.concatenate(item) for item in base] +
                          [np.concatenate(item) for item in signed])
    else:
        matrix_columns = []
        for panel in range(2):
            for j in range(len(NUISANCE)):
                pieces = []
                for row, value in enumerate(base[j]):
                    pieces.append(value if PANEL_ROWS[row] == panel
                                  else np.zeros_like(value))
                matrix_columns.append(np.concatenate(pieces))
    return projection(y, matrix_columns)


def fit_prediction(train: list[dict[str, np.ndarray]],
                   target: list[dict[str, np.ndarray]],
                   normalize: bool) -> dict[str, Any]:
    def make(rows: list[dict[str, np.ndarray]]) -> tuple[np.ndarray, np.ndarray]:
        ys = []
        columns = [[] for _ in NUISANCE]
        for row in rows:
            y = row["twin_prime"]
            scale = float(np.linalg.norm(y)) if normalize else 1.0
            need(scale > 0.0 and math.isfinite(scale), "fit norm")
            ys.append(y / scale)
            for j, name in enumerate(NUISANCE):
                columns[j].append(row[name] / scale)
        return np.concatenate(ys), np.column_stack(
            [np.concatenate(item) for item in columns])
    train_y, train_matrix = make(train)
    target_y, target_matrix = make(target)
    singular = np.linalg.svd(train_matrix, compute_uv=False)
    threshold = (max(train_matrix.shape) * np.finfo(np.float64).eps *
                 singular[0]) if len(singular) else 0.0
    rank = int(np.count_nonzero(singular > threshold)) if len(singular) else 0
    coefficient = np.linalg.lstsq(train_matrix, train_y, rcond=None)[0]
    error = target_y - target_matrix @ coefficient
    retention = float(error @ error) / float(target_y @ target_y)
    return {
        "training_rows": len(train),
        "target_rows": len(target),
        "training_rank": rank,
        "training_condition": format(positive_condition(singular, rank),
                                     ".17g"),
        "coefficients": [format(item, ".17g") for item in coefficient],
        "prediction_residual_retention": format(retention, ".17g"),
        "prediction_identity": "RESIDUAL_NORM_ONLY_NO_PROJECTION_IDENTITY",
    }


def holdout(rows: list[dict[str, Any]], normalize: bool) -> list[dict[str, Any]]:
    result = []
    for omitted, control in enumerate(item[0] for item in CONTROLS):
        targets = []
        columns = []
        for row in rows:
            outputs = row["_outputs"]
            targets.append(outputs["twin_prime"][omitted])
            training = [i for i in range(len(CONTROLS)) if i != omitted]
            columns.append([
                np.mean(np.stack([outputs[name][i] for i in training]), axis=0)
                for name in NUISANCE
            ])
        result.append({"omitted_control": control,
                       "metrics": contrast(targets, columns, normalize)})
    return result


def close_metric(actual: dict[str, Any], saved: dict[str, Any],
                 label: str) -> None:
    for field in ("target_energy", "projected_energy", "residual_energy",
                  "residual_retention", "removed_fraction",
                  "decomposition_gap", "nuisance_condition"):
        close(float(actual[field]), saved[field], label + " " + field)
    need(actual["nuisance_rank"] == saved["nuisance_rank"],
         label + " rank")
    need(actual["identity_holds"] is True and
         saved["identity_holds"] is True, label + " identity flag")
    need(len(actual["nuisance_singular_values"]) ==
         len(saved["nuisance_singular_values"]), label + " singular count")
    for index, value in enumerate(actual["nuisance_singular_values"]):
        close(float(value), saved["nuisance_singular_values"][index],
              label + " singular")


def reject_nonfinite(value: Any, label: str = "json") -> None:
    if isinstance(value, float):
        need(math.isfinite(value), label + " nonfinite")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_nonfinite(item, label + "." + str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_nonfinite(item, label + "[" + str(index) + "]")


def main() -> int:
    try:
        engine = load_reverse_engine()
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        reject_nonfinite(document)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document["payload"]
        need(payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "certificate digest")
        need(payload["parent_lock"] == {
            "TPC340_certificate_sha256": TPC340_CERT_SHA256,
            "TPC340_producer_sha256": TPC340_CODE_SHA256,
            "TPC343_certificate_sha256": TPC343_CERT_SHA256,
            "TPC343_producer_sha256": TPC343_CODE_SHA256,
        }, "parent lock")
        need(payload["finite_audit"] == {
            "panels": 2, "rows": 6, "origins": 6, "scales": 1,
            "controls": 9, "categories": 4, "raw_records": 216,
            "nonempty_raw_records": 171, "in_sample_records": 6,
            "holdout_records": 18, "crossfit_directions": 4,
            "basis_columns_declared": 6, "basis_rank_observed": 5,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        }, "finite audit")
        protocol = payload["protocol"]
        need(protocol["panel_sign_vector"] == [1, -1] and
             protocol["scale"] == 1024 and
             protocol["operator"] == {"law": "all_plus", "Q": 54,
                                      "kernel_exponent": 1, "height": 66},
             "protocol")
        rows = payload["rows"]
        need([row["origin"] for row in rows] == list(ORIGINS),
             "origin order")
        actual_rows = [row_data(engine, origin) for origin in ORIGINS]
        all_raw = 0
        all_nonempty = 0
        for index, (actual, saved) in enumerate(zip(actual_rows, rows)):
            need(saved["source_interval"] == [ORIGINS[index], ORIGINS[index] + 511],
                 "row interval")
            need(saved["cutoff_safe"] is True and actual["cutoff_safe"] is True,
                 "row cutoff")
            need(saved["operator"] == actual["operator"], "row operator")
            need(saved["mask_counts"] == actual["mask_counts"], "mask counts")
            need(len(saved["raw_records"]) == len(actual["raw_records"]) == 36,
                 "raw row census")
            for j, (a, b) in enumerate(zip(actual["raw_records"],
                                           saved["raw_records"])):
                need(a["control"] == b["control"] and
                     a["category"] == b["category"] and
                     a["support_size"] == b["support_size"],
                     "raw metadata")
                for field in ("source_l2", "response_energy", "response_gain"):
                    close(a[field], b[field], "raw " + str(j) + " " + field,
                          tolerance=9.0e-7)
            need(saved["nonempty_raw_record_count"] ==
                 actual["nonempty_raw_record_count"], "row nonempty")
            close_metric(actual["in_sample"], saved["in_sample"],
                         "row in-sample")
            need(len(saved["holdout"]) == len(actual["holdout"]) == 9,
                 "row holdout census")
            for j, (a, b) in enumerate(zip(actual["holdout"], saved["holdout"])):
                need(a["omitted_control"] == b["omitted_control"] and
                     a["training_controls"] == b["training_controls"],
                     "row holdout metadata")
                close_metric(a, b, "row holdout " + str(j))
            all_raw += len(actual["raw_records"])
            all_nonempty += actual["nonempty_raw_record_count"]
        need(all_raw == 216 and all_nonempty == 171, "global row census")

        targets = [row["_means"]["twin_prime"] for row in actual_rows]
        columns = [[row["_means"][name] for name in NUISANCE]
                   for row in actual_rows]
        actual_baseline = {
            "row_block_raw": stack(targets, columns, False, True),
            "row_block_equal_row": stack(targets, columns, True, True),
            "shared_raw": stack(targets, columns, False),
            "shared_equal_row": stack(targets, columns, True),
        }
        actual_contrast = {
            "contrast_raw": contrast(targets, columns, False),
            "contrast_equal_row": contrast(targets, columns, True),
            "adaptive_raw": contrast(targets, columns, False, True),
            "adaptive_equal_row": contrast(targets, columns, True, True),
        }
        for key, value in actual_baseline.items():
            close_metric(value, payload["baseline"][key], "baseline " + key)
        for key, value in actual_contrast.items():
            close_metric(value, payload["panel_contrast"][key],
                         "contrast " + key)
        for weighting, normalize in (("raw", False), ("equal_row", True)):
            actual_holdout = holdout(actual_rows, normalize)
            saved_holdout = payload["panel_contrast"][
                "holdout_raw" if not normalize else "holdout_equal_row"]
            for index, (a, b) in enumerate(zip(actual_holdout, saved_holdout)):
                need(a["omitted_control"] == b["omitted_control"],
                     "meta holdout control")
                close_metric(a["metrics"], b["metrics"],
                             "meta holdout " + weighting + " " + str(index))
        means = [{name: row["_means"][name] for name in CATEGORIES}
                 for row in actual_rows]
        actual_crossfit = []
        for normalize, label in ((False, "raw"), (True, "equal_row")):
            actual_crossfit.append({
                "weighting": label,
                "TPC341_to_TPC342": fit_prediction(means[:3], means[3:],
                                                    normalize),
                "TPC342_to_TPC341": fit_prediction(means[3:], means[:3],
                                                    normalize),
            })
        for a, b in zip(actual_crossfit,
                        payload["panel_contrast"]["crossfit"]):
            need(a["weighting"] == b["weighting"], "crossfit weighting")
            for direction in ("TPC341_to_TPC342", "TPC342_to_TPC341"):
                aa, bb = a[direction], b[direction]
                need(aa["training_rows"] == bb["training_rows"] and
                     aa["target_rows"] == bb["target_rows"] and
                     aa["training_rank"] == bb["training_rank"] and
                     aa["prediction_identity"] == bb["prediction_identity"],
                     "crossfit metadata")
                close(float(aa["training_condition"]),
                      bb["training_condition"], "crossfit condition")
                close(float(aa["prediction_residual_retention"]),
                      bb["prediction_residual_retention"], "crossfit residual")
                need(len(aa["coefficients"]) == len(bb["coefficients"]),
                     "crossfit coefficient count")
                for x, y in zip(aa["coefficients"], bb["coefficients"]):
                    close(float(x), y, "crossfit coefficient")

        summary = payload["summary"]
        close(float(actual_contrast["contrast_raw"]["residual_retention"]),
              summary["contrast_raw_retention"], "summary raw")
        close(float(actual_contrast["contrast_equal_row"]["residual_retention"]),
              summary["contrast_equal_row_retention"], "summary equal")
        holdout_values = [
            float(item["metrics"]["residual_retention"])
            for key in ("holdout_raw", "holdout_equal_row")
            for item in payload["panel_contrast"][key]
        ]
        crossfit_values = [
            float(item[direction]["prediction_residual_retention"])
            for item in payload["panel_contrast"]["crossfit"]
            for direction in ("TPC341_to_TPC342", "TPC342_to_TPC341")
        ]
        close(min(holdout_values), summary["holdout_retention_min"],
              "summary holdout min")
        close(max(holdout_values), summary["holdout_retention_max"],
              "summary holdout max")
        close(min(crossfit_values), summary["crossfit_retention_min"],
              "summary crossfit min")
        close(max(crossfit_values), summary["crossfit_retention_max"],
              "summary crossfit max")
        need(float(summary["contrast_raw_retention"]) < 0.30 and
             float(summary["contrast_equal_row_retention"]) >= 0.30 and
             float(summary["holdout_retention_min"]) > 0.40 and
             float(summary["crossfit_retention_min"]) > 0.30 and
             summary["weighting_stability"] == "REFUTED_SCOPED" and
             summary["crossfit_transfer"] == "REFUTED_SCOPED",
             "summary guards")
        anchor = payload["exact_anchor"]
        need(anchor == {
            "base": ["1", "0", "0", "1"],
            "contrast": ["1", "0", "0", "-1"],
            "panel_one_column": ["1", "0", "0", "0"],
            "panel_two_column": ["0", "0", "0", "1"],
            "target": ["1", "1", "1", "1"],
            "projected_energy": "2", "residual_energy": "2",
            "identity_exact": True}, "exact anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC344_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC344_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC344_EQUAL_ROW_CONTRAST_GUARD"] == "REFUTED_SCOPED" and
             firewall["TPC344_FULL_GATE_B"] == "OPEN" and
             firewall["TPC344_TWIN_PRIME_RESULT"] == "NONE",
             "firewall")
        print("TPC344_INDEPENDENT_CHECK=PASS rows=6 raw_records=216 "
              "contrast_raw=0.2962189247 contrast_equal_row=0.3186506700 "
              "holdout_records=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC344_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
