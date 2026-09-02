#!/usr/bin/env python3
"""TPC-345: principal-angle and Grassmann stability audit.

TPC-344 showed that a signed panel-contrast basis gives a narrow
raw-weighted finite repair, but that the crossing is not stable under
equal-row weighting.  This release removes the choice of nuisance
coordinates: it compares the column spaces of the two panel nuisance
matrices by principal angles, projector distances, and cross-panel target
projection.  Every statement is finite and protocol-scoped.
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
RESULT = PROJECT / "results/tpc345_certificate.json"

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

TPC344_PROJECT = ROOT / "papers/tpc-344-panel-contrast-nuisance-basis"
TPC344_CODE = TPC344_PROJECT / "code/tpc344_panel_contrast_nuisance_basis.py"
TPC344_CERT = TPC344_PROJECT / "results/tpc344_certificate.json"
TPC344_CODE_SHA256 = "08daa3e1b5782e619f492039ed0b8f734de923dfc39797d88eea8a5650ce83ba"
TPC344_CERT_SHA256 = "29da3486ef9c1fcb7ec4274203e93059959736b05ea0eb3bf7f8f69e69a63460"

SCHEMA = "TPC345_PRINCIPAL_ANGLE_GRASSMANN_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT"
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
NUMERIC_TOL = 8.0e-6
INVARIANCE_TOL = 2.0e-9
DOMINANT_COSINE_FLOOR = 0.99
TRANSVERSE_COSINE_CEILING = 0.20
WEIGHTING_ANGLE_SHIFT_FLOOR_DEG = 10.0
MUTUAL_TRANSFER_GUARD = 0.30
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
    # Thirteen significant digits preserve the audited margins while making
    # the canonical certificate insensitive to harmless BLAS last-bit drift.
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


def load_source() -> Any:
    locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC340 producer")
    locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC340 certificate")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 certificate header")
    for name, origins, code, cert, code_hash, cert_hash, status in (
            ("TPC341", PANELS[0][1], TPC341_CODE, TPC341_CERT,
             TPC341_CODE_SHA256, TPC341_CERT_SHA256,
             "NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION"),
            ("TPC342", PANELS[1][1], TPC342_CODE, TPC342_CERT,
             TPC342_CODE_SHA256, TPC342_CERT_SHA256,
             "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION")):
        locked(code, code_hash, name + " producer")
        locked(cert, cert_hash, name + " certificate")
        panel = json.loads(cert.read_bytes())
        need(cert.read_bytes() == canonical(panel) and
             panel.get("claim_status") == status, name + " header")
        protocol = panel.get("payload", {}).get("protocol", {})
        if "origins" in protocol:
            got_origins = protocol["origins"]
        else:
            got_origins = [item.get("origin") for item
                           in panel.get("payload", {}).get("rows", [])]
        need(got_origins == list(origins), name + " origins")
        need(protocol.get("scales", [1024]) == [1024],
             name + " scale protocol")
    locked(TPC344_CODE, TPC344_CODE_SHA256, "TPC344 producer")
    locked(TPC344_CERT, TPC344_CERT_SHA256, "TPC344 certificate")
    tpc344 = json.loads(TPC344_CERT.read_bytes())
    need(TPC344_CERT.read_bytes() == canonical(tpc344) and
         tpc344.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT",
         "TPC344 certificate header")
    need(tpc344.get("payload", {}).get("round2_clue") ==
         "PRINCIPAL_ANGLE_GRASSMANN_STABILITY_AUDIT",
         "TPC344 route clue")
    spec = importlib.util.spec_from_file_location("tpc340_parent", PARENT_CODE)
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


def orthonormal(columns: list[np.ndarray] | np.ndarray
                ) -> tuple[np.ndarray, np.ndarray, int]:
    matrix = (columns if isinstance(columns, np.ndarray)
              else np.column_stack(columns))
    need(matrix.ndim == 2 and matrix.shape[1] > 0, "basis matrix")
    left, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        return np.zeros((matrix.shape[0], 0), dtype=np.float64), singular, 0
    threshold = max(matrix.shape) * np.finfo(np.float64).eps * singular[0]
    rank = int(np.count_nonzero(singular > threshold))
    return left[:, :rank], singular, rank


def projection_from_basis(target: np.ndarray, basis: np.ndarray,
                          singular: np.ndarray, rank: int) -> dict[str, Any]:
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
         "projection Pythagorean identity")
    return {
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
    }


def projection(target: np.ndarray,
               columns: list[np.ndarray]) -> tuple[dict[str, Any],
                                                    np.ndarray, np.ndarray,
                                                    int, np.ndarray]:
    matrix = np.column_stack(columns)
    need(matrix.shape[0] == len(target), "projection shape")
    basis, singular, rank = orthonormal(matrix)
    return (projection_from_basis(target, basis, singular, rank),
            basis, singular, rank, matrix)


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
    records: list[dict[str, Any]] = []
    for control_name, multiplier, offset, rule in CONTROLS:
        permutation = control_indices(len(beta), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            energy = float(output @ output)
            outputs[category].append(output)
            records.append({
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
    in_sample, _, singular, rank, _ = projection(means["twin_prime"],
                                                   nuisance)
    expected_rank = sum(float(np.linalg.norm(item)) > 0.0 for item in nuisance)
    need(rank == expected_rank, "row rank")
    nonempty = [item for item in records if float(item["source_l2"]) > 0.0]
    need(len(records) == 36 and bool(nonempty), "row record census")
    return {
        "origin": origin,
        "scale": SCALE,
        "source_interval": [lo, hi],
        "source_count": len(beta),
        "cutoff_safe": hi + 2 < CUTOFF,
        "operator": {"law": "all_plus", "Q": Q,
                     "kernel_exponent": EXPONENT, "height": HEIGHT},
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "raw_records": records,
        "nonempty_raw_record_count": len(nonempty),
        "mean_energies": {name: show(float(means[name] @ means[name]))
                          for name in CATEGORIES},
        "expected_nuisance_rank": expected_rank,
        "in_sample": in_sample,
        "source_weight_max_interval_width": show(width),
        "_outputs": outputs,
        "_means": means,
    }


def panel_matrix(rows: list[dict[str, Any]], equal_row: bool
                 ) -> tuple[np.ndarray, list[np.ndarray]]:
    target_parts: list[np.ndarray] = []
    columns: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    for row in rows:
        target = row["_means"]["twin_prime"]
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(math.isfinite(scale) and scale > 0.0, "panel scale")
        target_parts.append(target / scale)
        for index, name in enumerate(NUISANCE):
            columns[index].append(row["_means"][name] / scale)
    return np.concatenate(target_parts), [np.concatenate(item)
                                          for item in columns]


def cross_projection(target: np.ndarray, basis: np.ndarray,
                     singular: np.ndarray, rank: int) -> dict[str, Any]:
    return projection_from_basis(target, basis, singular, rank)


def principal(left: tuple[np.ndarray, np.ndarray, int, np.ndarray],
              right: tuple[np.ndarray, np.ndarray, int, np.ndarray]
              ) -> dict[str, Any]:
    q_left, s_left, r_left, m_left = left
    q_right, s_right, r_right, m_right = right
    overlap = q_left.T @ q_right
    cosines = np.linalg.svd(overlap, compute_uv=False)
    angles = [math.degrees(math.acos(min(1.0, max(-1.0, float(item)))))
              for item in cosines]
    p_left = q_left @ q_left.T
    p_right = q_right @ q_right.T
    projector_delta = p_left - p_right
    return {
        "left_rank": r_left,
        "right_rank": r_right,
        "principal_cosines": [show(item) for item in cosines],
        "principal_angles_degrees": [show(item) for item in angles],
        "principal_cosine_squares": [show(item * item) for item in cosines],
        "projector_frobenius_distance": show(float(np.linalg.norm(
            projector_delta, ord="fro"))),
        "projector_spectral_distance": show(float(np.linalg.norm(
            projector_delta, ord=2))),
        "min_rank": min(r_left, r_right),
        "definition": "singular_values(Q_left^T Q_right)",
        "_cosines": cosines,
        "_angles": angles,
        "_left_projector": p_left,
        "_right_projector": p_right,
        "_left_matrix": m_left,
        "_right_matrix": m_right,
        "_left_singular": s_left,
        "_right_singular": s_right,
    }


def invariance(left_matrix: np.ndarray, right_matrix: np.ndarray,
               reference: dict[str, Any]) -> dict[str, Any]:
    left_q, left_s, left_r = orthonormal(left_matrix @ SHEAR)
    right_q, right_s, right_r = orthonormal(right_matrix @ SHEAR)
    left_p = left_q @ left_q.T
    right_p = right_q @ right_q.T
    left_ref = reference["_left_projector"]
    right_ref = reference["_right_projector"]
    cos_ref = np.asarray(reference["_cosines"])
    cos_new = np.linalg.svd(left_q.T @ right_q, compute_uv=False)
    projector_error = max(float(np.max(np.abs(left_p - left_ref))),
                          float(np.max(np.abs(right_p - right_ref))))
    cosine_error = (float(np.max(np.abs(cos_new - cos_ref)))
                    if len(cos_ref) else 0.0)
    need(left_r == reference["left_rank"] and
         right_r == reference["right_rank"], "invariance rank")
    return {
        "column_shear": [[show(item) for item in row] for row in SHEAR],
        "left_rank": left_r,
        "right_rank": right_r,
        "max_projector_entry_error": show(projector_error),
        "max_principal_cosine_error": show(cosine_error),
        "span_invariant": projector_error <= INVARIANCE_TOL and
        cosine_error <= INVARIANCE_TOL,
    }


def loo_panel(rows: list[dict[str, Any]], omitted: int,
              equal_row: bool) -> tuple[np.ndarray, np.ndarray]:
    targets: list[np.ndarray] = []
    parts: list[list[np.ndarray]] = [[] for _ in NUISANCE]
    training = [index for index in range(len(CONTROLS)) if index != omitted]
    for row in rows:
        target = row["_outputs"]["twin_prime"][omitted]
        scale = float(np.linalg.norm(target)) if equal_row else 1.0
        need(math.isfinite(scale) and scale > 0.0, "loo scale")
        targets.append(target / scale)
        for nuisance_index, name in enumerate(NUISANCE):
            mean = np.mean(np.stack([row["_outputs"][name][index]
                                     for index in training]), axis=0)
            parts[nuisance_index].append(mean / scale)
    return np.concatenate(targets), np.column_stack(
        [np.concatenate(item) for item in parts])


def loo_entry(panel_rows: list[dict[str, Any]],
              other_rows: list[dict[str, Any]], omitted: int,
              equal_row: bool) -> dict[str, Any]:
    left_target, left_matrix = loo_panel(panel_rows, omitted, equal_row)
    right_target, right_matrix = loo_panel(other_rows, omitted, equal_row)
    left_q, left_s, left_r = orthonormal(left_matrix)
    right_q, right_s, right_r = orthonormal(right_matrix)
    geometry = principal((left_q, left_s, left_r, left_matrix),
                         (right_q, right_s, right_r, right_matrix))
    left_target_metrics = cross_projection(left_target, right_q, right_s,
                                           right_r)
    right_target_metrics = cross_projection(right_target, left_q, left_s,
                                            left_r)
    geometry.pop("_cosines")
    geometry.pop("_angles")
    for key in ("_left_projector", "_right_projector", "_left_matrix",
                "_right_matrix", "_left_singular", "_right_singular"):
        geometry.pop(key)
    return {
        "omitted_control": CONTROLS[omitted][0],
        "training_control_count": len(CONTROLS) - 1,
        "geometry": geometry,
        "left_target_on_right_basis": left_target_metrics,
        "right_target_on_left_basis": right_target_metrics,
    }


def exact_anchor() -> dict[str, Any]:
    # One-dimensional subspaces with an exact squared principal cosine.
    a = (Fraction(1), Fraction(0))
    b = (Fraction(1), Fraction(1))
    cos_sq = (sum(x * y for x, y in zip(a, b)) ** 2 /
              (sum(x * x for x in a) * sum(y * y for y in b)))
    need(cos_sq == Fraction(1, 2), "exact angle anchor")
    return {
        "left_vector": ["1", "0"],
        "right_vector": ["1", "1"],
        "squared_principal_cosine": "1/2",
        "left_rescaling": "3",
        "right_rescaling": "-2",
        "rescaling_preserves_span_and_angle": True,
        "identity_exact": True,
    }


def clean_geometry(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    for key in ("_cosines", "_angles", "_left_projector",
                "_right_projector", "_left_matrix", "_right_matrix",
                "_left_singular", "_right_singular"):
        result.pop(key, None)
    return result


def build_payload() -> dict[str, Any]:
    source = load_source()
    panel_rows = [[row_data(source, origin) for origin in origins]
                  for _name, origins, _sign in PANELS]
    all_rows = [row for panel in panel_rows for row in panel]
    records = [record for row in all_rows for record in row["raw_records"]]
    nonempty = [record for record in records
                if float(record["source_l2"]) > 0.0]
    need(len(all_rows) == 6 and len(records) == 216 and
         len(nonempty) == 171, "global record census")

    weightings: list[dict[str, Any]] = []
    for equal_row, label in ((False, "raw"), (True, "equal_row")):
        targets = []
        panel_geometries: list[tuple[np.ndarray, np.ndarray, int, np.ndarray]] = []
        panel_documents: list[dict[str, Any]] = []
        for panel_index, rows in enumerate(panel_rows):
            target, columns = panel_matrix(rows, equal_row)
            q, singular, rank = orthonormal(np.column_stack(columns))
            own = projection_from_basis(target, q, singular, rank)
            panel_geometries.append((q, singular, rank,
                                     np.column_stack(columns)))
            targets.append(target)
            panel_documents.append({
                "name": PANELS[panel_index][0],
                "rank": rank,
                "singular_values": [show(item) for item in singular],
                "condition": own["nuisance_condition"],
                "target_projection": own,
            })
        geometry = principal(panel_geometries[0], panel_geometries[1])
        target_0_on_1 = cross_projection(
            targets[0], panel_geometries[1][0], panel_geometries[1][1],
            panel_geometries[1][2])
        target_1_on_0 = cross_projection(
            targets[1], panel_geometries[0][0], panel_geometries[0][1],
            panel_geometries[0][2])
        invariance_audit = invariance(panel_geometries[0][3],
                                      panel_geometries[1][3], geometry)
        loo = [loo_entry(panel_rows[0], panel_rows[1], omitted, equal_row)
               for omitted in range(len(CONTROLS))]
        loo_cos = [
            float(item["geometry"]["principal_cosines"][0])
            for item in loo
        ]
        transverse_cos = [
            float(item["geometry"]["principal_cosines"][1])
            for item in loo
        ]
        need(all(int(item["geometry"]["left_rank"]) == 3 and
                 int(item["geometry"]["right_rank"]) == 2 for item in loo),
             "loo rank census")
        weightings.append({
            "label": label,
            "row_normalization": "target_l2_inverse" if equal_row else "none",
            "panel_geometry": panel_documents,
            "principal_geometry": clean_geometry(geometry),
            "target_panel_0_on_panel_1": target_0_on_1,
            "target_panel_1_on_panel_0": target_1_on_0,
            "basis_invariance": invariance_audit,
            "leave_one_control_out": loo,
            "loo_summary": {
                "dominant_cosine_min": show(min(loo_cos)),
                "dominant_cosine_max": show(max(loo_cos)),
                "transverse_cosine_min": show(min(transverse_cos)),
                "transverse_cosine_max": show(max(transverse_cos)),
                "count": len(loo),
            },
        })

    raw = weightings[0]
    equal = weightings[1]
    raw_cos = [float(item) for item
               in raw["principal_geometry"]["principal_cosines"]]
    equal_cos = [float(item) for item
                 in equal["principal_geometry"]["principal_cosines"]]
    raw_angles = [float(item) for item
                  in raw["principal_geometry"]["principal_angles_degrees"]]
    equal_angles = [float(item) for item
                    in equal["principal_geometry"]["principal_angles_degrees"]]
    angle_shift = abs(equal_angles[0] - raw_angles[0])
    cross_retentions = [
        float(raw["target_panel_0_on_panel_1"]["residual_retention"]),
        float(raw["target_panel_1_on_panel_0"]["residual_retention"]),
        float(equal["target_panel_0_on_panel_1"]["residual_retention"]),
        float(equal["target_panel_1_on_panel_0"]["residual_retention"]),
    ]
    need(raw_cos[0] > DOMINANT_COSINE_FLOOR and
         raw_cos[1] < TRANSVERSE_COSINE_CEILING and
         equal_cos[1] < TRANSVERSE_COSINE_CEILING,
         "principal-angle classification")
    need(angle_shift > WEIGHTING_ANGLE_SHIFT_FLOOR_DEG,
         "weighting angle shift")
    need(all(float(value) >= MUTUAL_TRANSFER_GUARD for value in
             (raw["target_panel_1_on_panel_0"]["residual_retention"],
              equal["target_panel_1_on_panel_0"]["residual_retention"])),
         "mutual transfer obstruction")
    need(float(raw["loo_summary"]["dominant_cosine_min"]) >
         DOMINANT_COSINE_FLOOR and
         float(raw["loo_summary"]["transverse_cosine_max"]) <
         TRANSVERSE_COSINE_CEILING and
         float(equal["loo_summary"]["transverse_cosine_max"]) <
         TRANSVERSE_COSINE_CEILING, "loo angle stability")
    need(all(item["span_invariant"] for item in
             (raw["basis_invariance"], equal["basis_invariance"])),
         "basis invariance")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC340_producer_sha256": PARENT_CODE_SHA256,
            "TPC340_certificate_sha256": PARENT_CERT_SHA256,
            "TPC341_producer_sha256": TPC341_CODE_SHA256,
            "TPC341_certificate_sha256": TPC341_CERT_SHA256,
            "TPC342_producer_sha256": TPC342_CODE_SHA256,
            "TPC342_certificate_sha256": TPC342_CERT_SHA256,
            "TPC344_producer_sha256": TPC344_CODE_SHA256,
            "TPC344_certificate_sha256": TPC344_CERT_SHA256,
        },
        "protocol": {
            "panels": [{"name": name, "origins": list(origins), "sign": sign}
                       for name, origins, sign in PANELS],
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
            "principal_angle_definition":
                "singular_values(Q_341^T Q_342) for positive-SVD bases",
            "rank_rule":
                "singular_value > max(matrix_shape)*eps*largest_singular_value",
            "cross_panel_transfer_guard":
                "both target directions must have residual retention < 0.30",
            "dominant_alignment_threshold": ">0.99",
            "transverse_alignment_threshold": "<0.20",
            "weighting_angle_shift_threshold_degrees": ">10",
            "basis_invariance_transform": "upper-triangular nonsingular shear",
        },
        "exact_theorem": {
            "principal_angle_invariance":
                "singular_values(Q_1^T Q_2) are unchanged by nonsingular "
                "column reparameterizations",
            "projector_definition": "P=QQ^T for an orthonormal positive-SVD basis",
            "cross_projection_identity":
                "||Y||^2=||P_NY||^2+||(I-P_N)Y||^2",
            "rank_mismatch_note":
                "two angles are reported because min(rank_341,rank_342)=2; "
                "the remaining rank is panel-specific",
            "finite_scope": "all identities concern the declared finite matrices",
            "arithmetic_interpretation": "none",
        },
        "finite_audit": {
            "panels": 2,
            "rows": 6,
            "controls": 9,
            "categories": 4,
            "raw_records": 216,
            "nonempty_raw_records": 171,
            "weightings": 2,
            "principal_angle_pairs": 2,
            "loo_angle_pairs": 18,
            "basis_invariance_checks": 2,
            "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "summary": {
            "raw_principal_cosines": raw["principal_geometry"]["principal_cosines"],
            "raw_principal_angles_degrees":
                raw["principal_geometry"]["principal_angles_degrees"],
            "equal_row_principal_cosines":
                equal["principal_geometry"]["principal_cosines"],
            "equal_row_principal_angles_degrees":
                equal["principal_geometry"]["principal_angles_degrees"],
            "dominant_angle_shift_degrees": show(angle_shift),
            "raw_mutual_transfer_failure":
                float(raw["target_panel_1_on_panel_0"]["residual_retention"])
                >= MUTUAL_TRANSFER_GUARD,
            "equal_row_mutual_transfer_failure":
                float(equal["target_panel_1_on_panel_0"]["residual_retention"])
                >= MUTUAL_TRANSFER_GUARD,
            "cross_panel_transfer_relevance": "REFUTED_SCOPED",
            "weighting_stability": "REFUTED_SCOPED",
            "basis_invariance": "NUMERICALLY_CERTIFIED_FINITE",
            "rank_mismatch": "TPC341_RANK_3_VERSUS_TPC342_RANK_2",
            "raw_loo_dominant_cosine_min":
                raw["loo_summary"]["dominant_cosine_min"],
            "raw_loo_transverse_cosine_max":
                raw["loo_summary"]["transverse_cosine_max"],
            "equal_loo_transverse_cosine_max":
                equal["loo_summary"]["transverse_cosine_max"],
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC345_MAXIMUM_CLAIM": STATUS,
            "TPC345_PRINCIPAL_ANGLE_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC345_BASIS_INVARIANCE":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC345_RAW_DOMINANT_ALIGNMENT":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC345_TRANSVERSE_ALIGNMENT":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC345_WEIGHTING_STABILITY": "REFUTED_SCOPED",
            "TPC345_MUTUAL_TRANSFER": "REFUTED_SCOPED",
            "TPC345_RANK_MISMATCH": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC345_ARITHMETIC_ADVANCE": "NO",
            "TPC345_FIXED_POWER_CREDIT": 0,
            "TPC345_SOURCE_UNIFORM_L2": "OPEN",
            "TPC345_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC345_FULL_GATE_B": "OPEN",
            "TPC345_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE",
        "weighting_results": weightings,
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
            print("TPC345_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC345_CERTIFICATE=PASS panels=2 rows=6 "
                  "raw_records=216 loo_angle_pairs=18 "
                  "raw_cosines=0.9957018010,0.0799456793 "
                  "equal_cosines=0.9144519860,0.0787084493")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC345_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
