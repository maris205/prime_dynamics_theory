#!/usr/bin/env python3
"""Reverse-shell independent checker for TPC-345.

The checker does not import the TPC-345 producer.  It uses only the
hash-locked TPC-340 reverse engine, reconstructs the two panels, and
recomputes the principal-angle, projector, transfer, and leave-one-control-
out statistics.
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
RESULT = PROJECT / "results/tpc345_certificate.json"
PRODUCER = PROJECT / "code/tpc345_principal_angle_grassmann_audit.py"
PRODUCER_SHA256 = "da6e4a72f3aee7a744cb2d15e9060260c380c25568efd19204968fd5ed63df9e"

ENGINE = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py"
ENGINE_SHA256 = "4cff79b0f5c300357af4889e87a0734bbfdcc7f538ee19d313d8f2176a1b583c"
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
TPC344_CODE = ROOT / "papers/tpc-344-panel-contrast-nuisance-basis/code/tpc344_panel_contrast_nuisance_basis.py"
TPC344_CERT = ROOT / "papers/tpc-344-panel-contrast-nuisance-basis/results/tpc344_certificate.json"
TPC344_CODE_SHA256 = "08daa3e1b5782e619f492039ed0b8f734de923dfc39797d88eea8a5650ce83ba"
TPC344_CERT_SHA256 = "29da3486ef9c1fcb7ec4274203e93059959736b05ea0eb3bf7f8f69e69a63460"

PANELS = (
    ("TPC341", (48097, 48609, 49217)),
    ("TPC342", (40097, 40609, 41121)),
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
INVARIANCE_TOL = 2.0e-9
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
    actual_value = float(actual)
    value = float(expected)
    need(math.isfinite(actual_value) and math.isfinite(value) and
         abs(actual_value - value) <= tolerance * max(1.0, abs(actual_value),
                                                       abs(value)),
         label)


def locked(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def load_engine() -> Any:
    need(PRODUCER_SHA256 != "TO_BE_FILLED", "producer hash not sealed")
    locked(PRODUCER, PRODUCER_SHA256, "TPC345 producer")
    locked(ENGINE, ENGINE_SHA256, "reverse engine")
    for path, expected, label in (
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC340 producer"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC340 certificate"),
            (TPC341_CODE, TPC341_CODE_SHA256, "TPC341 producer"),
            (TPC341_CERT, TPC341_CERT_SHA256, "TPC341 certificate"),
            (TPC342_CODE, TPC342_CODE_SHA256, "TPC342 producer"),
            (TPC342_CERT, TPC342_CERT_SHA256, "TPC342 certificate"),
            (TPC344_CODE, TPC344_CODE_SHA256, "TPC344 producer"),
            (TPC344_CERT, TPC344_CERT_SHA256, "TPC344 certificate")):
        locked(path, expected, label)
    parent = json.loads(PARENT_CERT.read_bytes())
    need(PARENT_CERT.read_bytes() == canonical(parent) and
         parent.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 header")
    for name, origins, cert, status in (
            ("TPC341", PANELS[0][1], TPC341_CERT,
             "NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION"),
            ("TPC342", PANELS[1][1], TPC342_CERT,
             "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION")):
        document = json.loads(cert.read_bytes())
        need(cert.read_bytes() == canonical(document) and
             document.get("claim_status") == status, name + " header")
        protocol = document.get("payload", {}).get("protocol", {})
        got = protocol.get("origins")
        if got is None:
            got = [item.get("origin")
                   for item in document.get("payload", {}).get("rows", [])]
        need(got == list(origins), name + " origins")
    tpc344 = json.loads(TPC344_CERT.read_bytes())
    need(TPC344_CERT.read_bytes() == canonical(tpc344) and
         tpc344.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT",
         "TPC344 header")
    need(tpc344["payload"]["round2_clue"] ==
         "PRINCIPAL_ANGLE_GRASSMANN_STABILITY_AUDIT", "TPC344 clue")
    spec = importlib.util.spec_from_file_location("tpc340_reverse", ENGINE)
    need(spec is not None and spec.loader is not None, "engine import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_engine()


def orthonormal(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    need(matrix.ndim == 2 and matrix.shape[1] > 0, "matrix")
    left, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    threshold = (max(matrix.shape) * np.finfo(np.float64).eps *
                 singular[0]) if len(singular) else 0.0
    rank = int(np.count_nonzero(singular > threshold)) if len(singular) else 0
    return left[:, :rank], singular, rank


def projection(target: np.ndarray, basis: np.ndarray, rank: int
               ) -> dict[str, float | int]:
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    gap = target_energy - projected_energy - residual_energy
    need(target_energy > 0.0 and math.isfinite(target_energy), "target")
    need(abs(gap) <= 8.0e-6 * max(1.0, target_energy), "projection gap")
    return {
        "target_energy": target_energy,
        "projected_energy": projected_energy,
        "residual_energy": residual_energy,
        "residual_retention": residual_energy / target_energy,
        "removed_fraction": 1.0 - residual_energy / target_energy,
        "decomposition_gap": gap,
        "nuisance_rank": rank,
        "identity_holds": True,
    }


def row(engine: Any, origin: int) -> tuple[dict[str, Any],
                                             dict[str, list[np.ndarray]],
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
                "control": control, "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": source_l2, "response_energy": energy,
            })
    means = {name: np.mean(np.stack(outputs[name]), axis=0)
             for name in CATEGORIES}
    need(len(records) == 36, "row census")
    return ({"origin": origin, "raw_records": records,
             "nonempty_raw_record_count":
                 sum(float(item["source_l2"]) > 0.0 for item in records)},
            outputs, means)


def panel_data(rows: list[tuple[dict[str, Any],
                                dict[str, list[np.ndarray]],
                                dict[str, np.ndarray]]],
               equal_row: bool) -> tuple[np.ndarray, np.ndarray]:
    targets: list[np.ndarray] = []
    columns: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    for _record, _outputs, means in rows:
        target = means["twin_prime"]
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(scale > 0.0 and math.isfinite(scale), "panel scale")
        targets.append(target / scale)
        for index, name in enumerate(NUISANCE):
            columns[index].append(means[name] / scale)
    return np.concatenate(targets), np.column_stack(
        [np.concatenate(item) for item in columns])


def principal(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    q_left, s_left, r_left = orthonormal(left)
    q_right, s_right, r_right = orthonormal(right)
    cosines = np.linalg.svd(q_left.T @ q_right, compute_uv=False)
    angles = [math.degrees(math.acos(min(1.0, max(-1.0, float(item)))))
              for item in cosines]
    delta = q_left @ q_left.T - q_right @ q_right.T
    return {
        "left_rank": r_left, "right_rank": r_right,
        "principal_cosines": cosines,
        "principal_angles_degrees": np.asarray(angles),
        "projector_frobenius_distance": float(np.linalg.norm(delta, "fro")),
        "projector_spectral_distance": float(np.linalg.norm(delta, 2)),
        "_left_basis": q_left, "_right_basis": q_right,
        "_left_singular": s_left, "_right_singular": s_right,
        "_left_rank": r_left, "_right_rank": r_right,
    }


def loo_matrix(rows: list[tuple[dict[str, Any],
                                dict[str, list[np.ndarray]],
                                dict[str, np.ndarray]]],
               omitted: int, equal_row: bool
               ) -> tuple[np.ndarray, np.ndarray]:
    targets: list[np.ndarray] = []
    parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    training = [index for index in range(len(CONTROLS)) if index != omitted]
    for _record, outputs, _means in rows:
        target = outputs["twin_prime"][omitted]
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(scale > 0.0 and math.isfinite(scale), "loo scale")
        targets.append(target / scale)
        for j, name in enumerate(NUISANCE):
            mean = np.mean(np.stack([outputs[name][index]
                                     for index in training]), axis=0)
            parts[j].append(mean / scale)
    return np.concatenate(targets), np.column_stack(
        [np.concatenate(item) for item in parts])


def compare_projection(actual: dict[str, Any], expected: dict[str, Any],
                       label: str) -> None:
    for key in ("target_energy", "projected_energy", "residual_energy",
                "residual_retention", "removed_fraction",
                "decomposition_gap"):
        close(float(actual[key]), expected[key], label + ":" + key)
    need(int(actual["nuisance_rank"]) == int(expected["nuisance_rank"]),
         label + ":rank")


def compare_float_list(actual: list[Any], expected: np.ndarray,
                       label: str) -> None:
    need(len(actual) == len(expected), label + ":length")
    for index, value in enumerate(expected):
        close(float(actual[index]), float(value), label + ":" + str(index))


def main() -> int:
    try:
        engine = load_engine()
        panel_rows = [[row(engine, origin) for origin in origins]
                      for _name, origins in PANELS]
        document = json.loads(RESULT.read_bytes())
        raw_certificate = RESULT.read_bytes()
        need(raw_certificate == canonical(document), "certificate canonicality")
        need(document.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT",
             "certificate status")
        payload = document["payload"]
        need(hashlib.sha256(canonical(payload)).hexdigest() ==
             document["payload_sha256"], "payload digest")
        all_rows = [item for panel in panel_rows for item in panel]
        records = [record for rec, _outputs, _means in all_rows
                   for record in rec["raw_records"]]
        need(len(all_rows) == 6 and len(records) == 216 and
             sum(float(item["source_l2"]) > 0.0 for item in records) == 171,
             "global census")
        cert_rows = payload["rows"]
        need(len(cert_rows) == len(all_rows), "certificate row count")
        for row_index, ((record, _outputs, _means), saved) in enumerate(
                zip(all_rows, cert_rows)):
            need(record["origin"] == saved["origin"],
                 "row origin " + str(row_index))
            saved_records = saved["raw_records"]
            need(len(saved_records) == len(record["raw_records"]),
                 "row record count " + str(row_index))
            for item_index, (got, want) in enumerate(
                    zip(record["raw_records"], saved_records)):
                need(got["control"] == want["control"] and
                     got["category"] == want["category"] and
                     got["support_size"] == want["support_size"],
                     "record labels")
                close(got["source_l2"], want["source_l2"], "source_l2")
                close(got["response_energy"], want["response_energy"],
                      "response_energy")

        saved_weightings = payload["weighting_results"]
        need([item["label"] for item in saved_weightings] ==
             ["raw", "equal_row"], "weighting labels")
        computed: list[dict[str, Any]] = []
        for weighting_index, equal_row in enumerate((False, True)):
            targets: list[np.ndarray] = []
            matrices: list[np.ndarray] = []
            panel_meta: list[dict[str, Any]] = []
            for panel in panel_rows:
                target, matrix = panel_data(panel, equal_row)
                targets.append(target); matrices.append(matrix)
                q, singular, rank = orthonormal(matrix)
                panel_meta.append({"q": q, "s": singular, "rank": rank})
            geom = principal(matrices[0], matrices[1])
            p0 = projection(targets[0], panel_meta[1]["q"],
                            panel_meta[1]["rank"])
            p1 = projection(targets[1], panel_meta[0]["q"],
                            panel_meta[0]["rank"])
            changed_left, changed_s, changed_r = orthonormal(
                matrices[0] @ SHEAR)
            changed_right, changed_t, changed_u = orthonormal(
                matrices[1] @ SHEAR)
            old_left = panel_meta[0]["q"]; old_right = panel_meta[1]["q"]
            projector_error = max(
                float(np.max(np.abs(changed_left @ changed_left.T -
                                    old_left @ old_left.T))),
                float(np.max(np.abs(changed_right @ changed_right.T -
                                    old_right @ old_right.T))))
            old_cos = geom["principal_cosines"]
            new_cos = np.linalg.svd(changed_left.T @ changed_right,
                                    compute_uv=False)
            cosine_error = float(np.max(np.abs(old_cos - new_cos)))
            loo: list[dict[str, Any]] = []
            for omitted in range(len(CONTROLS)):
                left_target, left_matrix = loo_matrix(panel_rows[0],
                                                       omitted, equal_row)
                right_target, right_matrix = loo_matrix(panel_rows[1],
                                                        omitted, equal_row)
                loo_geom = principal(left_matrix, right_matrix)
                left_q = loo_geom["_left_basis"]
                right_q = loo_geom["_right_basis"]
                loo.append({
                    "geometry": loo_geom,
                    "left_target_on_right": projection(
                        left_target, right_q, loo_geom["_right_rank"]),
                    "right_target_on_left": projection(
                        right_target, left_q, loo_geom["_left_rank"]),
                })
            computed.append({"geometry": geom, "p0": p0, "p1": p1,
                             "projector_error": projector_error,
                             "cosine_error": cosine_error,
                             "changed_ranks": (changed_r, changed_u),
                             "loo": loo})
            saved = saved_weightings[weighting_index]
            need(saved["label"] == ("equal_row" if equal_row else "raw"),
                 "saved weighting")
            saved_geom = saved["principal_geometry"]
            compare_float_list(saved_geom["principal_cosines"],
                               geom["principal_cosines"], "principal cosines")
            compare_float_list(saved_geom["principal_angles_degrees"],
                               geom["principal_angles_degrees"],
                               "principal angles")
            close(saved_geom["projector_frobenius_distance"],
                  geom["projector_frobenius_distance"], "projector frob")
            close(saved_geom["projector_spectral_distance"],
                  geom["projector_spectral_distance"], "projector spectral")
            compare_projection(saved["target_panel_0_on_panel_1"], p0,
                               "panel0 transfer")
            compare_projection(saved["target_panel_1_on_panel_0"], p1,
                               "panel1 transfer")
            inv = saved["basis_invariance"]
            close(inv["max_projector_entry_error"], projector_error,
                  "invariance projector")
            close(inv["max_principal_cosine_error"], cosine_error,
                  "invariance cosine")
            need(bool(inv["span_invariant"]) and
                 changed_r == geom["left_rank"] and
                 changed_u == geom["right_rank"], "invariance guard")
            saved_loo = saved["leave_one_control_out"]
            need(len(saved_loo) == len(loo), "loo count")
            for got, want in zip(saved_loo, loo):
                saved_geo = got["geometry"]; want_geo = want["geometry"]
                compare_float_list(saved_geo["principal_cosines"],
                                   want_geo["principal_cosines"], "loo cosine")
                compare_float_list(saved_geo["principal_angles_degrees"],
                                   want_geo["principal_angles_degrees"],
                                   "loo angle")
                need(saved_geo["left_rank"] == want_geo["left_rank"] and
                     saved_geo["right_rank"] == want_geo["right_rank"],
                     "loo ranks")
                compare_projection(got["left_target_on_right_basis"],
                                   want["left_target_on_right"],
                                   "loo left transfer")
                compare_projection(got["right_target_on_left_basis"],
                                   want["right_target_on_left"],
                                   "loo right transfer")
        summary = payload["summary"]
        raw_geom = computed[0]["geometry"]
        equal_geom = computed[1]["geometry"]
        compare_float_list(summary["raw_principal_cosines"],
                           raw_geom["principal_cosines"], "summary raw cos")
        compare_float_list(summary["equal_row_principal_cosines"],
                           equal_geom["principal_cosines"], "summary equal cos")
        close(summary["dominant_angle_shift_degrees"],
              abs(float(equal_geom["principal_angles_degrees"][0]) -
                  float(raw_geom["principal_angles_degrees"][0])),
              "summary angle shift")
        need(summary["basis_invariance"] == "NUMERICALLY_CERTIFIED_FINITE",
             "summary invariance label")
        need(summary["weighting_stability"] == "REFUTED_SCOPED" and
             summary["cross_panel_transfer_relevance"] == "REFUTED_SCOPED",
             "summary firewall")
        print("TPC345_INDEPENDENT_CHECK=PASS panels=2 rows=6 "
              "raw_records=216 loo_angle_pairs=18 "
              "raw_cosines=0.9957018010,0.0799456793 "
              "equal_cosines=0.9144519860,0.0787084493")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC345_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
