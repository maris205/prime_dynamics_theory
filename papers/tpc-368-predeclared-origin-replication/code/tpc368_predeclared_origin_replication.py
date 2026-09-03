#!/usr/bin/env python3
"""TPC-368: replicate the TPC-367 long-window obstruction on a new origin family."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc368_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-367-predeclared-long-window-obstruction/code/"
    "tpc367_predeclared_long_window_obstruction.py")
PARENT_CERT = ROOT / (
    "papers/tpc-367-predeclared-long-window-obstruction/results/"
    "tpc367_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "a4d70e6a62351d41867e014f4a1e7f8792240c5dfcb58df1da192caa8e180899")
PARENT_CERT_SHA256 = (
    "7d5c7d41e6b7c427791f9652dd4837908ffb6bd14576621ade0993ce513ea385")

SCHEMA = "TPC368_PREDECLARED_ORIGIN_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PREDECLARED_ORIGIN_REPLICATION"
ROUND2_CLUE = "TEST_BETA2_THIRD_ORIGIN_FAMILY_OR_COUNT_2048"

CANDIDATE_ORIGINS = tuple(810001 + 353 * j for j in range(41))
ORIGIN_INDICES = (0, 20, 40)
ORIGINS = tuple(CANDIDATE_ORIGINS[index] for index in ORIGIN_INDICES)
COUNTS = (512, 1024)
Q_ANCHORS = (512, 2048, 8192)
EXPONENTS = (1,)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
BETAS = (0, 2)
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (810342, 810355)
EXACT_Q = 4
EXACT_EXPONENT = 1


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


def load_base():
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc368",
                                                  BASE_CODE)
    need(spec is not None and spec.loader is not None, "base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base()


def load_parent() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC367_PREDECLARED_LONG_WINDOW_OBSTRUCTION_V1",
         "parent payload")
    return payload


def weighted_components(values: np.ndarray, q0: int, exponent: int,
                        beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = BASE.shell_for(q0)
    signs = BASE.sign_patterns(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = []
    for index, prime in enumerate(primes):
        weight = (float(prime) / float(q0)) ** beta
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
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrices, geometry, weights


def matrix_metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "finite metrics")
    eigenvalues = np.linalg.eigvalsh(matrix)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(spectral) and spectral > 0.0 and
         spectral <= schur + 2.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 2.0e-9 * max(1.0, frobenius),
         "finite spectral envelopes")
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               beta: int, law: str, components=None) -> dict[str, Any]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    if components is None:
        components = weighted_components(values, q0, exponent, beta)
    primes, matrices, geometry, weights = components
    scale = np.sqrt(geometry[:, None] * geometry[None, :])
    normalized = matrices[law] / scale
    effective = float(np.sum(np.asarray(weights) ** 2) ** 2 /
                      np.sum(np.asarray(weights) ** 4))
    return {
        "origin": origin, "count": count,
        "interval": [origin, origin + count - 1], "Q": q0,
        "kernel_exponent": exponent, "beta": beta, "law": law,
        "height": HEIGHT, "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "weight_effective_count": show(effective),
        "weight_effective_fraction": show(effective / len(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                       np.min(geometry))),
        "raw": matrix_metrics(matrices[law]),
        "normalized": matrix_metrics(normalized),
    }


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for beta in BETAS:
        for origin in ORIGINS:
            for count in COUNTS:
                values = np.arange(origin, origin + count, dtype=np.int64)
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        components = weighted_components(values, q0, exponent,
                                                         beta)
                        for law in LAWS:
                            rows.append(row_record(origin, count, q0,
                                                   exponent, beta, law,
                                                   components))
    need(len(rows) == 144, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_beta: dict[str, Any] = {}
    by_beta_q_count: dict[str, Any] = {}
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        spectra = [float(row["normalized"]["spectral"]) for row in selected]
        by_beta[str(beta)] = {
            "rows": len(selected), "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "spectral_cap_violations": sum(v > SPECTRAL_CAP for v in spectra),
            "schur_max": show(max(float(row["normalized"]["schur"])
                                   for row in selected)),
            "schur_cap_violations": sum(
                float(row["normalized"]["schur"]) > SCHUR_CAP
                for row in selected),
            "effective_fraction_min": show(min(
                float(row["weight_effective_fraction"]) for row in selected)),
        }
        for count in COUNTS:
            for q0 in Q_ANCHORS:
                setting = [row for row in selected
                           if row["count"] == count and row["Q"] == q0]
                values = [float(row["normalized"]["spectral"])
                          for row in setting]
                by_beta_q_count[f"{beta}:{count}:{q0}"] = {
                    "beta": beta, "count": count, "Q": q0,
                    "rows": len(setting), "spectral_min": show(min(values)),
                    "spectral_max": show(max(values)),
                    "spectral_cap_violations": sum(
                        value > SPECTRAL_CAP for value in values),
                    "schur_cap_violations": sum(
                        float(row["normalized"]["schur"]) > SCHUR_CAP
                        for row in setting),
                }
    return {"by_beta": by_beta, "by_beta_q_count": by_beta_q_count,
            "cap_repair_betas": [], "cap": show(SPECTRAL_CAP),
            "schur_cap": show(SCHUR_CAP)}


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = BASE.shell_for(EXACT_Q)

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    anchors: list[dict[str, Any]] = []
    for beta in BETAS:
        matrix: list[list[Fraction]] = []
        geometry: list[Fraction] = []
        for u in values:
            row: list[Fraction] = []
            grow = Fraction(0)
            for t in values:
                total = Fraction(0)
                energy = Fraction(0)
                for prime in primes:
                    if u == t or u % prime == 0 or t % prime == 0:
                        base = Fraction(0)
                    else:
                        centered = Fraction(int((u - t) % prime == 0), 1)
                        centered -= Fraction(1, prime - 1)
                        base = (prime * Fraction(HEIGHT * HEIGHT,
                                                 HEIGHT * HEIGHT + (u - t) ** 2)
                                * centered)
                    weighted = Fraction(prime, EXACT_Q) ** beta * base
                    total += weighted
                    energy += weighted * weighted
                row.append(total)
                grow += energy
            matrix.append(row)
            geometry.append(grow)
        need(all(matrix[i][j] == matrix[j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "exact anchor symmetry")
        need(all(value > 0 for value in geometry), "exact anchor positivity")
        anchors.append({
            "beta": beta, "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
            "kernel_exponent": EXACT_EXPONENT, "shell": primes,
            "matrix_symmetric": True, "geometry_positive": True,
            "matrix_digest": hashlib.sha256(canonical([
                [text(value) for value in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(value) for value in geometry])).hexdigest(),
        })
    return {"anchors": anchors}


def origin_protocol() -> dict[str, Any]:
    return {
        "candidate_origins": list(CANDIDATE_ORIGINS),
        "candidate_count": len(CANDIDATE_ORIGINS),
        "grid_start": CANDIDATE_ORIGINS[0], "grid_step": 353,
        "grid_indices": list(ORIGIN_INDICES),
        "selected_origins": list(ORIGINS),
        "selection_rule": "predeclared equally spaced grid points; no geometry ranking",
        "response_used": False, "geometry_used_for_selection": False,
        "source_used": False,
    }


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
            (BASE_CODE, BASE_CODE_SHA256, "base"),
            (PARENT_CODE, PARENT_CODE_SHA256, "parent code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "parent certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent()
    anchor = exact_anchor()
    rows = build_rows()
    phase = phase_summary(rows)
    parent_max = float(parent["finite_audit"]["predeclared_beta2_max_spectral"])
    beta2_max = float(phase["by_beta"]["2"]["spectral_max"])
    beta2_failures = [
        (row["origin"], row["count"], row["Q"], row["kernel_exponent"],
         row["law"])
        for row in rows if row["beta"] == 2 and
        float(row["normalized"]["spectral"]) > SPECTRAL_CAP
    ]
    expected_pattern = sorted(
        (origin, 1024, q0, 1, "all_plus")
        for origin in ORIGINS for q0 in (2048, 8192))
    need(sorted(beta2_failures) == expected_pattern,
         "replication failure pattern")
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "base_code_sha256": BASE_CODE_SHA256,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
        },
        "origin_protocol": origin_protocol(),
        "protocol": {
            "origins": list(ORIGINS), "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS), "betas": list(BETAS), "height": HEIGHT,
            "spectra_for_all_laws": True, "source_response_used": False,
            "origin_selection_used": False,
            "normalization": "weighted square-energy symmetric congruence",
            "weight_rule": "w_(p,beta)=(p/Q)^beta",
            "parent_panel": "TPC-367 predeclared long-window obstruction",
        },
        "exact_theorem": {
            "origin_protocol": "The three origins are fixed deterministic grid points declared before replay and use no response or geometry score.",
            "geometry": "The weighted geometry is a finite sum of nonnegative rational squares.",
            "congruence": "Positive geometry makes the finite weighted symmetric congruence well-defined.",
            "envelopes": "For finite real T, ||T||_2 <= max row absolute sum and ||T||_2 <= ||T||_F.",
            "replication_scope": "The second-family replication is restricted to counts 512 and 1024, Q in {512,2048,8192}, exponent one, and the three declared origins.",
        },
        "finite_audit": {
            "rows": len(rows), "settings_per_beta": 72,
            "beta_count": len(BETAS), "spectral_rows": len(rows),
            "beta2_rows": sum(row["beta"] == 2 for row in rows),
            "beta2_spectral_cap_violations": phase["by_beta"]["2"][
                "spectral_cap_violations"],
            "beta2_schur_cap_violations": phase["by_beta"]["2"][
                "schur_cap_violations"],
            "baseline_beta0_spectral_cap_violations": phase["by_beta"]["0"][
                "spectral_cap_violations"],
            "baseline_beta0_schur_cap_violations": phase["by_beta"]["0"][
                "schur_cap_violations"],
            "q_min": min(Q_ANCHORS), "q_max": max(Q_ANCHORS),
            "count_min": min(COUNTS), "count_max": max(COUNTS),
            "parent_beta2_max_spectral": show(parent_max),
            "replicated_beta2_max_spectral": show(beta2_max),
            "replicated_minus_parent_max_spectral": show(beta2_max - parent_max),
            "replicated_failure_keys": [list(key) for key in beta2_failures],
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": anchor,
        "claim_firewall": {
            "TPC368_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC368_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
            "TPC368_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
            "TPC368_SECOND_ORIGIN_FAMILY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC368_BETA2_LONG_WINDOW_REPLICATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC368_BETA2_FAILURE_PATTERN": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC368_ORIGIN_UNIFORMITY": "OPEN",
            "TPC368_WINDOW_UNIFORMITY": "OPEN",
            "TPC368_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
            "TPC368_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC368_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC368_SOURCE_UNIFORM_L2": "OPEN",
            "TPC368_ARITHMETIC_ADVANCE": "NO",
            "TPC368_FIXED_POWER_CREDIT": 0,
            "TPC368_FULL_GATE_B": "OPEN",
            "TPC368_TWIN_PRIME_RESULT": "NONE",
        },
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
            print("TPC368_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == build_document(), "certificate replay")
            print("TPC368_CERTIFICATE=PASS rows=144 beta2_rows=72")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC368_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
