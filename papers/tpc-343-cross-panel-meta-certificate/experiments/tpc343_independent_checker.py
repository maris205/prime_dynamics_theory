#!/usr/bin/env python3
"""Independent reverse-shell checker for TPC-343.

This file never imports the TPC-343 producer.  It uses the hash-locked
TPC-340 reverse engine, rebuilds both panels, and recomputes the stacked
projection statistics from the resulting vectors.
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
RESULT = PROJECT / "results/tpc343_certificate.json"
PRODUCER = PROJECT / "code/tpc343_cross_panel_meta_certificate.py"
ENGINE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py"
ENGINE_SHA256 = "4cff79b0f5c300357af4889e87a0734bbfdcc7f538ee19d313d8f2176a1b583c"
PRODUCER_SHA256 = "b10192be90572f210c2f0551576abd659c8d518845dee7e61793feab6de3d13b"

PARENT_CODE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/results/tpc340_certificate.json"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

TPC341_CODE = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py"
TPC341_CERT = ROOT / "papers/tpc-341-fresh-holdout-nuisance-orthogonalization/results/tpc341_certificate.json"
TPC341_CODE_SHA256 = "66269d586493a51adefeb8f17638df6b2eccf7e55aeab83e099b26c7768d52ac"
TPC341_CERT_SHA256 = "50f8f81f4c401924187ae90327cf787139489570cbda68707b846e3d89f36218"
TPC342_CODE = ROOT / "papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py"
TPC342_CERT = ROOT / "papers/tpc-342-independent-fresh-holdout-reproduction/results/tpc342_certificate.json"
TPC342_CODE_SHA256 = "1c57ccd3519f20f9283b0a4f678bd2b0f81ef60e94b9db7780f4f263684e6014"
TPC342_CERT_SHA256 = "7dbb39b8d38ef5d09a7b21e829d2e70469f7e9e2a1e1b135588c1413fb7cd52f"

SCHEMA = "TPC343_CROSS_PANEL_META_CERTIFICATE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE"
PANELS = (
    ("TPC341", (48097, 48609, 49217), TPC341_CERT,
     "NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION"),
    ("TPC342", (40097, 40609, 41121), TPC342_CERT,
     "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION"),
)
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


def close(actual: float, saved: Any, label: str,
          tolerance: float = 6.0e-7) -> None:
    expected = float(saved)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual),
                                                    abs(expected)), label)


def check_locked_parent(path: Path, expected: str, label: str) -> None:
    need(digest(path.read_bytes()) == expected, label + " provenance")


def load_engine() -> Any:
    check_locked_parent(PRODUCER, PRODUCER_SHA256, "TPC343 producer")
    check_locked_parent(PARENT_CODE, PARENT_CODE_SHA256, "TPC340 producer")
    check_locked_parent(PARENT_CERT, PARENT_CERT_SHA256, "TPC340 certificate")
    check_locked_parent(TPC341_CODE, TPC341_CODE_SHA256, "TPC341 producer")
    check_locked_parent(TPC341_CERT, TPC341_CERT_SHA256, "TPC341 certificate")
    check_locked_parent(TPC342_CODE, TPC342_CODE_SHA256, "TPC342 producer")
    check_locked_parent(TPC342_CERT, TPC342_CERT_SHA256, "TPC342 certificate")
    parent = json.loads(PARENT_CERT.read_bytes())
    need(PARENT_CERT.read_bytes() == canonical(parent) and
         parent.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 header")
    for name, origins, cert, status in PANELS:
        document = json.loads(cert.read_bytes())
        need(cert.read_bytes() == canonical(document) and
             document.get("claim_status") == status,
             name + " header")
        protocol = document.get("payload", {}).get("protocol", {})
        need(protocol.get("origins") == list(origins) and
             protocol.get("scales") == [1024], name + " protocol")
    need(digest(ENGINE.read_bytes()) == ENGINE_SHA256, "reverse engine")
    spec = importlib.util.spec_from_file_location("tpc340_reverse", ENGINE)
    need(spec is not None and spec.loader is not None, "engine import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_engine()


def projection(target: np.ndarray,
               columns: list[np.ndarray]) -> dict[str, Any]:
    matrix = np.column_stack(columns)
    basis_all, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        rank = 0
        basis = np.zeros((len(target), 0), dtype=np.float64)
    else:
        threshold = max(matrix.shape) * np.finfo(np.float64).eps * singular[0]
        rank = int(np.sum(singular > threshold))
        basis = basis_all[:, :rank]
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    gap = target_energy - projected_energy - residual_energy
    need(target_energy > 0.0 and math.isfinite(target_energy), "target")
    need(abs(gap) <= TOL * max(1.0, target_energy), "projection identity")
    return {
        "target_energy": target_energy,
        "projected_energy": projected_energy,
        "residual_energy": residual_energy,
        "residual_retention": residual_energy / target_energy,
        "removed_fraction": 1.0 - residual_energy / target_energy,
        "decomposition_gap": gap,
        "nuisance_rank": rank,
        "nuisance_singular_values": singular,
        "nuisance_condition": (float(singular[0] / singular[rank - 1])
                                if rank else math.inf),
        "identity_holds": True,
    }


def row(engine: Any, origin: int, scale: int) -> tuple[dict[str, Any],
                                                        dict[str, list[np.ndarray]],
                                                        dict[str, np.ndarray]]:
    lo, hi = origin, origin + scale // 2 - 1
    need(hi + 2 < 50_000, "cutoff")
    lam, comparison, residual = engine.source_arrays(lo, hi)
    matrix = engine.reverse_matrix(origin, scale)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[engine.category(value, float(lam[i]),
                              float(comparison[i]))][i] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs: dict[str, list[np.ndarray]] = {name: [] for name in CATEGORIES}
    raw: list[dict[str, Any]] = []
    for control, multiplier, offset in CONTROLS:
        permutation = engine.control_indices(len(residual), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            energy = float(output @ output)
            outputs[category].append(output)
            raw.append({"control": control, "category": category,
                        "support_size": int(np.count_nonzero(placed)),
                        "source_l2": source_l2,
                        "response_energy": energy,
                        "response_gain": energy / source_l2
                        if source_l2 else 0.0})
    means = {name: np.mean(np.stack(outputs[name]), axis=0)
             for name in CATEGORIES}
    in_sample = projection(means["twin_prime"],
                           [means[name] for name in NUISANCE])
    expected_rank = sum(float(np.linalg.norm(means[name])) > 0.0
                        for name in NUISANCE)
    need(in_sample["nuisance_rank"] == expected_rank, "in-sample rank")
    holdout: list[dict[str, Any]] = []
    names = [item[0] for item in CONTROLS]
    for omitted, control in enumerate(names):
        training = [index for index in range(len(names)) if index != omitted]
        columns = [np.mean(np.stack([outputs[name][index]
                                     for index in training]), axis=0)
                   for name in NUISANCE]
        metrics = projection(outputs["twin_prime"][omitted], columns)
        need(metrics["nuisance_rank"] == expected_rank, "holdout rank")
        metrics.update({"omitted_control": control,
                        "training_controls": [names[index] for index in training]})
        holdout.append(metrics)
    record = {
        "origin": origin, "scale": scale, "source_interval": [lo, hi],
        "source_count": len(residual), "cutoff_safe": hi + 2 < 50_000,
        "operator": {"law": "all_plus", "Q": 54,
                     "kernel_exponent": 1, "height": 66},
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "raw_records": raw,
        "nonempty_raw_record_count": sum(item["source_l2"] > 0.0
                                          for item in raw),
        "mean_energies": {name: float(means[name] @ means[name])
                          for name in CATEGORIES},
        "expected_nuisance_rank": expected_rank,
        "in_sample": in_sample, "holdout": holdout,
    }
    return record, outputs, means


def common(targets: list[np.ndarray], columns: list[list[np.ndarray]],
           equal_row: bool) -> dict[str, Any]:
    target_parts: list[np.ndarray] = []
    column_parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    for target, row_columns in zip(targets, columns):
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(scale > 0.0 and math.isfinite(scale), "meta scale")
        target_parts.append(target / scale)
        for index, column in enumerate(row_columns):
            column_parts[index].append(column / scale)
    return projection(np.concatenate(target_parts),
                       [np.concatenate(parts) for parts in column_parts])


def block(targets: list[np.ndarray], columns: list[list[np.ndarray]],
          equal_row: bool) -> dict[str, Any]:
    total = sum(len(target) for target in targets)
    matrix = np.zeros((total, len(targets) * len(NUISANCE)), dtype=np.float64)
    target_parts: list[np.ndarray] = []
    cursor = 0
    for row_index, (target, row_columns) in enumerate(zip(targets, columns)):
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(scale > 0.0 and math.isfinite(scale), "block scale")
        target_parts.append(target / scale)
        size = len(target)
        for nuisance_index, column in enumerate(row_columns):
            matrix[cursor:cursor + size,
                   row_index * len(NUISANCE) + nuisance_index] = column / scale
        cursor += size
    return projection(np.concatenate(target_parts),
                      [matrix[:, index] for index in range(matrix.shape[1])])


def weighted(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    target = sum(item["target_energy"] for item in metrics)
    projected = sum(item["projected_energy"] for item in metrics)
    residual = sum(item["residual_energy"] for item in metrics)
    gap = target - projected - residual
    return {"target_energy": target, "projected_energy": projected,
            "residual_energy": residual,
            "residual_retention": residual / target,
            "removed_fraction": 1.0 - residual / target,
            "decomposition_gap": gap, "component_count": len(metrics),
            "identity_holds": abs(gap) <= TOL * max(1.0, target)}


def check_metrics(actual: dict[str, Any], saved: dict[str, Any],
                  label: str) -> None:
    for field in ("target_energy", "projected_energy", "residual_energy",
                  "residual_retention", "removed_fraction",
                  "decomposition_gap", "nuisance_condition"):
        close(actual[field], saved[field], label + " " + field)
    need(saved.get("identity_holds") is True and
         actual["nuisance_rank"] == saved.get("nuisance_rank"),
         label + " metadata")
    singular = actual["nuisance_singular_values"]
    saved_singular = saved.get("nuisance_singular_values", [])
    need(len(singular) == len(saved_singular), label + " singular census")
    for index, value in enumerate(singular):
        close(float(value), saved_singular[index],
              label + " singular " + str(index))


def check_weighted(actual: dict[str, Any], saved: dict[str, Any],
                   label: str) -> None:
    for field in ("target_energy", "projected_energy", "residual_energy",
                  "residual_retention", "removed_fraction",
                  "decomposition_gap"):
        close(actual[field], saved[field], label + " " + field)
    need(actual["component_count"] == saved["component_count"] == 54 and
         saved["identity_holds"] is True, label + " metadata")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document) and document.get("certificate_version") == 1
             and document.get("claim_status") == STATUS, "certificate header")
        payload = document["payload"]
        need(payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "payload digest")
        engine = load_engine()
        need(tuple(item[:3] for item in engine.CONTROLS) == CONTROLS,
             "control protocol")
        rows: list[tuple[dict[str, Any], dict[str, list[np.ndarray]],
                       dict[str, np.ndarray]]] = []
        for panel_name, origins, _cert, _status in PANELS:
            for origin in origins:
                rows.append(row(engine, origin, 1024))
        saved_rows = payload["rows"]
        need(len(rows) == len(saved_rows) == 6, "row census")
        all_in: list[dict[str, Any]] = []
        all_hold: list[dict[str, Any]] = []
        for actual_triplet, saved in zip(rows, saved_rows):
            actual, outputs, means = actual_triplet
            need(actual["origin"] == saved["origin"] and
                 actual["source_interval"] == saved["source_interval"] and
                 actual["mask_counts"] == saved["mask_counts"] and
                 actual["expected_nuisance_rank"] ==
                 saved["expected_nuisance_rank"] and
                 len(actual["raw_records"]) == len(saved["raw_records"]) == 36,
                 "row metadata")
            for got, want in zip(actual["raw_records"], saved["raw_records"]):
                need(got["control"] == want["control"] and
                     got["category"] == want["category"] and
                     got["support_size"] == want["support_size"],
                     "raw metadata")
                for field in ("source_l2", "response_energy", "response_gain"):
                    close(got[field], want[field], "raw " + field)
            need(actual["nonempty_raw_record_count"] ==
                 saved["nonempty_raw_record_count"], "nonempty row")
            check_metrics(actual["in_sample"], saved["in_sample"],
                          "in-sample")
            need(len(actual["holdout"]) == len(saved["holdout"]) == 9,
                 "holdout census")
            for got, want in zip(actual["holdout"], saved["holdout"]):
                need(got["omitted_control"] == want["omitted_control"] and
                     got["training_controls"] == want["training_controls"],
                     "holdout metadata")
                check_metrics(got, want, "holdout")
            all_in.append(actual["in_sample"])
            all_hold.extend(actual["holdout"])

        in_targets = [triplet[2]["twin_prime"] for triplet in rows]
        in_columns = [[triplet[2][name] for name in NUISANCE]
                      for triplet in rows]
        meta = payload["meta"]
        actual_block_raw = block(in_targets, in_columns, False)
        actual_block_equal = block(in_targets, in_columns, True)
        actual_shared_raw = common(in_targets, in_columns, False)
        actual_shared_equal = common(in_targets, in_columns, True)
        check_metrics(actual_block_raw, meta["row_block_raw"], "row-block raw")
        check_metrics(actual_block_equal, meta["row_block_equal_row"],
                      "row-block equal")
        check_metrics(actual_shared_raw, meta["shared_raw"], "shared raw")
        check_metrics(actual_shared_equal, meta["shared_equal_row"],
                      "shared equal")

        for panel_index, (panel_name, _origins, _cert, _status) in enumerate(PANELS):
            subset = rows[panel_index * 3:(panel_index + 1) * 3]
            targets = [item[2]["twin_prime"] for item in subset]
            columns = [[item[2][name] for name in NUISANCE] for item in subset]
            saved_panel = payload["panel_meta"][panel_name]
            check_metrics(block(targets, columns, False),
                          saved_panel["row_block"], panel_name + " block")
            check_metrics(common(targets, columns, False),
                          saved_panel["shared_raw"], panel_name + " shared")
            check_metrics(common(targets, columns, True),
                          saved_panel["shared_equal_row"],
                          panel_name + " equal")

        common_raw: list[dict[str, Any]] = []
        common_equal: list[dict[str, Any]] = []
        hold_components: list[dict[str, Any]] = []
        for omitted, control in enumerate(item[0] for item in CONTROLS):
            targets = [triplet[1]["twin_prime"][omitted] for triplet in rows]
            columns: list[list[np.ndarray]] = []
            for _record, outputs, _means in rows:
                training = [index for index in range(9) if index != omitted]
                columns.append([np.mean(np.stack([outputs[name][index]
                                                   for index in training]), axis=0)
                                for name in NUISANCE])
            common_raw.append({"omitted_control": control,
                               "metrics": common(targets, columns, False)})
            common_equal.append({"omitted_control": control,
                                 "metrics": common(targets, columns, True)})
            hold_components.extend(projection(target, row_columns)
                                   for target, row_columns in zip(targets,
                                                                    columns))
        for got, want in zip(common_raw, meta["holdout_shared_raw"]):
            need(got["omitted_control"] == want["omitted_control"],
                 "shared holdout label")
            check_metrics(got["metrics"], want["metrics"],
                          "shared holdout raw")
        for got, want in zip(common_equal, meta["holdout_shared_equal_row"]):
            need(got["omitted_control"] == want["omitted_control"],
                 "equal holdout label")
            check_metrics(got["metrics"], want["metrics"],
                          "shared holdout equal")
        check_weighted(weighted(hold_components),
                       meta["holdout_row_block_weighted"], "holdout weighted")

        audit = payload["finite_audit"]
        need(audit == {"panels": 2, "rows": 6, "origins": 6, "scales": 1,
                       "controls": 9, "categories": 4, "raw_records": 216,
                       "nonempty_raw_records": 171, "in_sample_records": 6,
                       "holdout_records": 54, "fixed_power_credit": 0,
                       "arithmetic_advance": "NO"}, "audit")
        summary = payload["summary"]
        close(min(item["residual_retention"] for item in all_in),
              summary["in_sample_retention_min"], "summary in min")
        close(max(item["residual_retention"] for item in all_in),
              summary["in_sample_retention_max"], "summary in max")
        close(min(item["residual_retention"] for item in all_hold),
              summary["holdout_retention_min"], "summary hold min")
        close(max(item["residual_retention"] for item in all_hold),
              summary["holdout_retention_max"], "summary hold max")
        close(actual_block_raw["residual_retention"],
              summary["row_block_meta_retention"], "summary block")
        close(actual_shared_raw["residual_retention"],
              summary["shared_raw_meta_retention"], "summary shared")
        close(actual_shared_equal["residual_retention"],
              summary["shared_equal_row_meta_retention"], "summary equal")
        need(float(summary["row_block_meta_retention"]) < 0.30 and
             float(summary["shared_raw_meta_retention"]) >= 0.30 and
             float(summary["shared_equal_row_meta_retention"]) >= 0.30 and
             float(summary["shared_holdout_raw_min"]) > 0.40,
             "meta guards")
        anchor = payload["exact_anchor"]
        need(anchor == {"target": [1, 1, 1, 1],
                        "shared_nuisance": [1, 0, 1, 0],
                        "target_energy": "4", "projected_energy": "2",
                        "residual_energy": "2", "residual_retention": "1/2",
                        "identity_exact": True}, "anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC343_SHARED_COEFFICIENT_STABILITY"] ==
             "REFUTED_SCOPED" and firewall["TPC343_ARITHMETIC_ADVANCE"] == "NO"
             and firewall["TPC343_FIXED_POWER_CREDIT"] == 0
             and firewall["TPC343_FULL_GATE_B"] == "OPEN", "firewall")
        print("TPC343_INDEPENDENT_CHECK=PASS panels=2 rows=6 controls=9 "
              "raw_records=216 holdout_records=54 shared_guard=REFUTED_SCOPED")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC343_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
