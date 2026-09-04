#!/usr/bin/env python3
"""TPC-380: a finite c=1 law-control count replay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc380_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-379-c1-crossholdout-law-control/code/"
    "tpc379_c1_crossholdout_law_control.py")
PARENT_CERT = ROOT / (
    "papers/tpc-379-c1-crossholdout-law-control/results/"
    "tpc379_certificate.json")

PARENT_CODE_SHA256 = (
    "5f4a32af562127a158dcb9232ecc6e380717c27145857b1f814734c5d0597b82")
PARENT_CERT_SHA256 = (
    "a41800cb32f59b2d025a808b92fb52567fbef661181f89889074b861c40504c7")

SCHEMA = "TPC380_C1_LAW_CONTROL_COUNT_REPLAY_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_COUNT_REPLAY"
ROUND2_CLUE = "TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY"

GRID_START = 1_300_001
GRID_STEP = 401
GRID_COUNT = 41
ORIGIN_INDICES = (0, 20, 40)
ORIGINS = tuple(GRID_START + GRID_STEP * i for i in ORIGIN_INDICES)
WINDOW_COUNT = 2048
BLOCK_LENGTH = 256
BLOCK_COUNT = WINDOW_COUNT // BLOCK_LENGTH
BAND_CUTOFF = 1
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
# The q=8 shell has two distinct prime-mod-4 signs, making the exact anchor
# audit the law-control interface as well as the common geometry.
# The first 13-point subinterval is residue-degenerate for the q=8 shell;
# freeze the first positive anchor found inside the already selected window.
EXACT_INTERVAL = (ORIGINS[0] + 13, ORIGINS[0] + 26)
EXACT_Q = 8

CLAIM_FIREWALL = {
    "TPC380_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC380_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC380_COMMON_GEOMETRY": "PROVED_EXACT_FINITE_LAW_INDEPENDENT",
    "TPC380_LAW_FAMILY": "PROVED_EXACT_FINITE_PREDECLARED",
    "TPC380_COUNT_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_36_ROWS",
    "TPC380_ALL_PLUS_FAILURE_PROFILE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC380_SIGNED_CONTROL_SUBCAP":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC380_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC380_LAW_UNIFORMITY": "OPEN",
    "TPC380_ORIGIN_UNIFORMITY": "OPEN",
    "TPC380_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC380_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC380_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC380_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC380_SOURCE_UNIFORM_L2": "OPEN",
    "TPC380_ARITHMETIC_ADVANCE": "NO",
    "TPC380_FIXED_POWER_CREDIT": 0,
    "TPC380_FULL_GATE_B": "OPEN",
    "TPC380_TWIN_PRIME_RESULT": "NONE",
}


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_parent_module():
    spec = importlib.util.spec_from_file_location(
        "tpc379_parent_for_tpc380", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PARENT = load_parent_module()
BASE = PARENT.BASE


def load_parent_payload() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") ==
         "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL",
         "parent payload")
    return payload


def prior_intervals() -> list[tuple[int, int]]:
    return [
        (1012006, 1012006 + 2048),
        (1016016, 1016016 + 2048),
        (1022031, 1022031 + 2048),
        (1100001, 1100001 + 2048),
        (1108021, 1108021 + 2048),
        (1116041, 1116041 + 2048),
        (1200001, 1200001 + 1024),
        (1208021, 1208021 + 1024),
        (1216041, 1216041 + 1024),
    ]


def coordinate_disjointness() -> bool:
    current = [(origin, origin + WINDOW_COUNT) for origin in ORIGINS]
    intervals = current + prior_intervals()
    return all(a[1] <= b[0] or b[1] <= a[0]
               for i, a in enumerate(intervals)
               for b in intervals[i + 1:])


def weighted_components(values: np.ndarray, q0: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + distance * distance) ** EXPONENT)
    np.fill_diagonal(kernel, 0.0)
    primes = BASE.shell_for(q0)
    signs = BASE.sign_patterns(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = []
    for index, prime in enumerate(primes):
        weight = (float(prime) / float(q0)) ** BETA
        weights.append(weight)
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for law in LAWS:
        matrices[law][:] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrices, geometry, weights


def metrics(matrix: np.ndarray, eigenvalues: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and schur > 0.0 and frobenius > 0.0 and
         math.isfinite(frobenius) and math.isfinite(spectral) and
         spectral > 0.0 and
         spectral <= schur + 8.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 8.0e-9 * max(1.0, frobenius),
         "finite metric envelope")
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
    }


def record(origin: int, q0: int, law: str, components=None) -> dict[str, Any]:
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    if components is None:
        components = weighted_components(values, q0)
    primes, matrices, geometry, weights = components
    full = matrices[law] / np.sqrt(geometry[:, None] * geometry[None, :])
    eigenvalues, eigenvectors = np.linalg.eigh(full)
    full_data = metrics(full, eigenvalues)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    index = 0 if abs(lo) >= abs(hi) else len(eigenvalues) - 1
    mode_name = "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue"
    vector = np.asarray(eigenvectors[:, index], dtype=np.float64)
    selected = float(eigenvalues[index])
    residual = float(np.max(np.abs(full @ vector - selected * vector)))
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_LENGTH
    mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= BAND_CUTOFF
    band = np.where(mask, full, 0.0)
    tail = full - band
    band_eigenvalues = np.linalg.eigvalsh(band)
    band_data = metrics(band, band_eigenvalues)
    tail_symmetry = float(np.max(np.abs(tail - tail.T)))
    tail_frobenius = float(np.sqrt(np.sum(tail * tail)))
    tail_schur = float(np.max(np.sum(np.abs(tail), axis=1)))
    band_rayleigh = float(vector @ (band @ vector))
    tail_rayleigh = float(vector @ (tail @ vector))
    norm_error = abs(float(np.dot(vector, vector)) - 1.0)
    rayleigh_error = abs(band_rayleigh + tail_rayleigh - selected)
    need(residual <= 1.0e-10 and norm_error <= 1.0e-10 and
         rayleigh_error <= 2.0e-11 and tail_symmetry <= 2.0e-12,
         "eigen/rayleigh identity")
    return {
        "Q": q0, "origin": origin, "count": WINDOW_COUNT,
        "interval": [origin, origin + WINDOW_COUNT], "law": law,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "block_length": BLOCK_LENGTH, "block_count": BLOCK_COUNT,
        "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                         np.min(geometry))),
        "full": full_data, "band": band_data,
        "tail": {"frobenius": show(tail_frobenius),
                 "schur": show(tail_schur),
                 "symmetry_error": show(tail_symmetry)},
        "mode": {
            "selected_mode": mode_name,
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
            "selected_eigenvalue": show(selected),
            "selected_eigenvalue_abs": show(abs(selected)),
            "eigen_residual_inf": show(residual),
            "full_mode_norm_error": show(norm_error),
            "band_rayleigh": show(band_rayleigh),
            "tail_rayleigh": show(tail_rayleigh),
            "rayleigh_sum_error": show(rayleigh_error),
            "band_signed_retention": show(band_rayleigh / selected),
            "band_rayleigh_abs_retention": show(
                abs(band_rayleigh) / abs(selected)),
            "tail_signed_fraction": show(tail_rayleigh / selected),
            "tail_rayleigh_abs_fraction": show(
                abs(tail_rayleigh) / abs(selected)),
        },
        "full_failure": float(full_data["spectral"]) > SPECTRAL_CAP,
        "band_failure": float(band_data["spectral"]) > SPECTRAL_CAP,
        "schur_failure": float(band_data["schur"]) > SCHUR_CAP,
    }


def build_rows() -> list[dict[str, Any]]:
    jobs = [(origin, q0) for origin in ORIGINS for q0 in Q_ANCHORS]

    def one(job):
        origin, q0 = job
        values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
        components = weighted_components(values, q0)
        return [record(origin, q0, law, components) for law in LAWS]

    with ThreadPoolExecutor(max_workers=3) as pool:
        groups = list(pool.map(one, jobs))
    rows = [row for group in groups for row in group]
    need(len(rows) == 36, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_law: list[dict[str, Any]] = []
    profile: dict[str, list[int]] = {}
    maxima: dict[str, str] = {}
    minima: dict[str, str] = {}
    for law in LAWS:
        law_rows = [row for row in rows if row["law"] == law]
        q_rows: list[dict[str, Any]] = []
        for q0 in Q_ANCHORS:
            setting = [row for row in law_rows if row["Q"] == q0]
            values = [row["band"]["spectral"] for row in setting]
            q_rows.append({
                "Q": q0, "rows": len(setting),
                "spectral_cap_violations":
                    sum(bool(row["band_failure"]) for row in setting),
                "schur_cap_violations":
                    sum(bool(row["schur_failure"]) for row in setting),
                "spectral_values": values,
            })
        profile[law] = [q["spectral_cap_violations"] for q in q_rows]
        maxima[law] = show(max(float(row["band"]["spectral"])
                               for row in law_rows))
        minima[law] = show(min(float(row["band"]["spectral"])
                               for row in law_rows))
        by_law.append({
            "law": law, "rows": len(law_rows), "by_Q": q_rows,
            "failure_profile_by_Q": profile[law],
            "spectral_cap_violations": sum(
                bool(row["band_failure"]) for row in law_rows),
            "schur_cap_violations": sum(
                bool(row["schur_failure"]) for row in law_rows),
        })
    retentions = [float(row["mode"]["band_rayleigh_abs_retention"])
                  for row in rows]
    tails = [float(row["mode"]["tail_rayleigh_abs_fraction"])
             for row in rows]
    return {
        "rows": len(rows), "laws": list(LAWS), "law_count": len(LAWS),
        "band_cutoff": BAND_CUTOFF,
        "band_definition": "block distance <= 1",
        "caps": {"spectral": show(SPECTRAL_CAP),
                 "schur": show(SCHUR_CAP)},
        "spectral_cap_violations": sum(bool(row["band_failure"])
                                        for row in rows),
        "schur_cap_violations": sum(bool(row["schur_failure"])
                                     for row in rows),
        "by_law": by_law,
        "failure_profile_by_law_Q": profile,
        "law_max_band_spectral": maxima,
        "law_min_band_spectral": minima,
        "all_plus_failure_profile": profile["all_plus"],
        "signed_control_failure_profiles": {
            law: profile[law] for law in LAWS if law != "all_plus"},
        "signed_controls_all_below_spectral_cap": all(
            all(value == 0 for value in profile[law])
            for law in LAWS if law != "all_plus"),
        "band_abs_retention_min": show(min(retentions)),
        "band_abs_retention_max": show(max(retentions)),
        "tail_abs_fraction_max": show(max(tails)),
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = BASE.shell_for(EXACT_Q)

    def as_text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    signs = BASE.sign_patterns(primes)
    matrices = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        rows = {law: [] for law in LAWS}
        grow = Fraction(0)
        for t in values:
            components: list[Fraction] = []
            for prime in primes:
                if u == t or u % prime == 0 or t % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(prime, EXACT_Q) ** BETA *
                            Fraction(HEIGHT * HEIGHT,
                                     HEIGHT * HEIGHT + (u - t) ** 2) *
                            centered)
                components.append(base)
            grow += sum(value * value for value in components)
            for law in LAWS:
                signed = sum(Fraction(int(signs[law][index])) * value
                             for index, value in enumerate(components))
                rows[law].append(signed)
        geometry.append(grow)
        for law in LAWS:
            matrices[law].append(rows[law])
    for law in LAWS:
        need(all(matrices[law][i][j] == matrices[law][j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "anchor symmetry")
    need(all(value > 0 for value in geometry), "anchor positivity")
    law_digests = {
        law: hashlib.sha256(canonical([
            [as_text(value) for value in row] for row in matrices[law]
        ])).hexdigest() for law in LAWS}
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "shell": primes, "laws": list(LAWS),
        "matrix_symmetric_by_law": {law: True for law in LAWS},
        "law_matrix_digests": law_digests,
        "geometry_positive": True,
        "geometry_digest": hashlib.sha256(canonical(
            [as_text(value) for value in geometry])).hexdigest(),
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    parent = load_parent_payload()
    need(coordinate_disjointness(), "coordinate disjointness")
    rows = build_rows()
    phase = phase_summary(rows)
    expected = {
        "all_plus": [0, 3, 3],
        "alternating_index": [0, 0, 0],
        "mod4_character": [0, 0, 0],
        "half_split": [0, 0, 0],
    }
    need(phase["failure_profile_by_law_Q"] == expected,
         "law-control profile")
    need(phase["spectral_cap_violations"] == 6 and
         phase["schur_cap_violations"] == 0 and
         phase["signed_controls_all_below_spectral_cap"] is True,
         "law-control census")
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_round2_clue": parent["round2_clue"],
            "parent_profile": [0, 3, 3],
        },
        "selection_protocol": {
            "grid_start": GRID_START, "grid_step": GRID_STEP,
            "grid_count": GRID_COUNT,
            "candidate_origins": [GRID_START + GRID_STEP * i
                                   for i in range(GRID_COUNT)],
            "origin_indices": list(ORIGIN_INDICES),
            "origins": list(ORIGINS),
            "origin_rule":
                "new coordinate-disjoint affine grid, endpoints fixed before response",
            "window_count": WINDOW_COUNT,
            "block_length": BLOCK_LENGTH, "block_count": BLOCK_COUNT,
            "q_anchors": list(Q_ANCHORS), "laws": list(LAWS),
            "law_rule": "all four sign laws fixed before any response is read",
            "response_used_for_selection": False,
            "signed_metric_used_for_selection": False,
            "panel_complete_before_metric_read": True,
        },
        "protocol": {
            "origins": list(ORIGINS), "window_count": WINDOW_COUNT,
            "block_length": BLOCK_LENGTH, "block_count": BLOCK_COUNT,
            "partition": "eight contiguous 256-point blocks",
            "band_cutoff": BAND_CUTOFF,
            "band_definition": "sum of layers with block distance <= 1",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "laws": list(LAWS), "betas": [BETA], "height": HEIGHT,
            "common_geometry": True, "source_response_used": False,
            "origin_selection_used": False, "law_selection_used": False,
            "row_selection_used": False,
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        },
        "exact_theorem": {
            "coordinate_disjointness":
                "All declared current and inherited finite intervals are disjoint by integer endpoint inequalities.",
            "common_geometry":
                "The square-energy normalization is independent of the declared sign law.",
            "law_family":
                "The four sign vectors are fixed from prime order, prime mod 4, or shell half-split before metric readout.",
            "common_band_rule":
                "The c=1 block-distance mask is identical for every law.",
            "rayleigh_identity":
                "For each selected full eigenvector, band and tail Rayleigh terms sum to its eigenvalue.",
        },
        "finite_audit": {
            "rows": len(rows), "origin_count": len(ORIGINS),
            "q_count": len(Q_ANCHORS), "law_count": len(LAWS),
            "spectral_rows": len(rows),
            "spectral_cap_violations": phase["spectral_cap_violations"],
            "schur_cap_violations": phase["schur_cap_violations"],
            "failure_profile_by_law_Q": phase["failure_profile_by_law_Q"],
            "all_plus_failure_profile": phase["all_plus_failure_profile"],
            "signed_control_failure_profiles":
                phase["signed_control_failure_profiles"],
            "coordinate_disjoint_from_prior": True,
            "law_control_complete": True,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": CLAIM_FIREWALL,
        "round2_clue": ROUND2_CLUE,
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
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(build_document()))
            print("TPC380_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            profiles = audit["failure_profile_by_law_Q"]
            compact = ";".join(
                law + ":" + ",".join(str(x) for x in profiles[law])
                for law in LAWS)
            print("TPC380_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " failures=" + str(audit["spectral_cap_violations"]) +
                  " profiles=" + compact)
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC380_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
