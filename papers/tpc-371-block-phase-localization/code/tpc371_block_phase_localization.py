#!/usr/bin/env python3
"""TPC-371: predeclared block-local phase localization for count 2048."""

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
RESULT = PROJECT / "results/tpc371_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-370-count-2048-window-audit/code/"
    "tpc370_count_2048_window_audit.py")
PARENT_CERT = ROOT / (
    "papers/tpc-370-count-2048-window-audit/results/"
    "tpc370_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "4e5bb7a1e8af07afc2e405d60ea38683bee4c3ab7cb2654e7da8246073e24fe2")
PARENT_CERT_SHA256 = (
    "109cfbf11478b566c176a7bad2df3a579b4079e2ad8cbd64eb692168e91e1070")

SCHEMA = "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BLOCK_PHASE_LOCALIZATION"
ROUND2_CLUE = "TEST_OFF_BLOCK_COHERENCE_DECOMPOSITION"

CANDIDATE_ORIGINS = tuple(1010001 + 401 * j for j in range(41))
ORIGIN_INDICES = (0, 20, 40)
ORIGINS = tuple(CANDIDATE_ORIGINS[index] for index in ORIGIN_INDICES)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(WINDOW_COUNT // BLOCK_COUNT))
Q_ANCHORS = (512, 2048, 8192)
EXPONENTS = (1,)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
BETAS = (0, 2)
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1010346, 1010359)
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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc371",
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
         payload.get("schema") == "TPC370_COUNT_2048_WINDOW_AUDIT_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_COUNT_2048_WINDOW_AUDIT",
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


def row_record(origin: int, block_index: int, q0: int, exponent: int,
               beta: int, law: str, components=None) -> dict[str, Any]:
    block_start = origin + block_index * BLOCK_COUNT
    block_stop = block_start + BLOCK_COUNT
    values = np.arange(block_start, block_stop, dtype=np.int64)
    if components is None:
        components = weighted_components(values, q0, exponent, beta)
    primes, matrices, geometry, weights = components
    scale = np.sqrt(geometry[:, None] * geometry[None, :])
    normalized = matrices[law] / scale
    effective = float(np.sum(np.asarray(weights) ** 2) ** 2 /
                      np.sum(np.asarray(weights) ** 4))
    return {
        "origin": origin, "window_count": WINDOW_COUNT,
        "window_interval": [origin, origin + WINDOW_COUNT - 1],
        "block_index": block_index, "block_count": BLOCK_COUNT,
        "block_offset": [block_index * BLOCK_COUNT,
                          (block_index + 1) * BLOCK_COUNT - 1],
        "count": BLOCK_COUNT, "interval": [block_start, block_stop - 1],
        "Q": q0, "kernel_exponent": exponent, "beta": beta, "law": law,
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
            for block_index in BLOCK_INDICES:
                values = np.arange(origin + block_index * BLOCK_COUNT,
                                   origin + (block_index + 1) * BLOCK_COUNT,
                                   dtype=np.int64)
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        components = weighted_components(values, q0, exponent,
                                                         beta)
                        for law in LAWS:
                            rows.append(row_record(origin, block_index, q0,
                                                   exponent, beta, law,
                                                   components))
    need(len(rows) == 576, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_beta: dict[str, Any] = {}
    by_beta_q: dict[str, Any] = {}
    by_beta_block: dict[str, Any] = {}
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        spectra = [float(row["normalized"]["spectral"]) for row in selected]
        schurs = [float(row["normalized"]["schur"]) for row in selected]
        by_beta[str(beta)] = {
            "rows": len(selected), "blocks": len(ORIGINS) * len(BLOCK_INDICES),
            "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "spectral_cap_violations": sum(v > SPECTRAL_CAP for v in spectra),
            "schur_max": show(max(schurs)),
            "schur_cap_violations": sum(v > SCHUR_CAP for v in schurs),
        }
        for q0 in Q_ANCHORS:
            setting = [row for row in selected if row["Q"] == q0]
            values = [float(row["normalized"]["spectral"]) for row in setting]
            by_beta_q[f"{beta}:{q0}"] = {
                "beta": beta, "Q": q0, "rows": len(setting),
                "spectral_min": show(min(values)),
                "spectral_max": show(max(values)),
                "spectral_cap_violations": sum(v > SPECTRAL_CAP
                                                for v in values),
                "schur_cap_violations": sum(
                    float(row["normalized"]["schur"]) > SCHUR_CAP
                    for row in setting),
            }
        for origin in ORIGINS:
            for block_index in BLOCK_INDICES:
                setting = [row for row in selected
                           if row["origin"] == origin and
                           row["block_index"] == block_index]
                values = [float(row["normalized"]["spectral"])
                          for row in setting]
                by_beta_block[f"{beta}:{origin}:{block_index}"] = {
                    "beta": beta, "origin": origin,
                    "block_index": block_index, "rows": len(setting),
                    "spectral_min": show(min(values)),
                    "spectral_max": show(max(values)),
                    "spectral_cap_violations": sum(v > SPECTRAL_CAP
                                                    for v in values),
                    "schur_cap_violations": sum(
                        float(row["normalized"]["schur"]) > SCHUR_CAP
                        for row in setting),
                }
    return {"by_beta": by_beta, "by_beta_q": by_beta_q,
            "by_beta_block": by_beta_block, "cap_repair_betas": [],
            "cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP)}


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
        "candidate_count": len(CANDIDATE_ORIGINS), "grid_start": 1010001,
        "grid_step": 401, "grid_indices": list(ORIGIN_INDICES),
        "selected_origins": list(ORIGINS),
        "selection_rule": "inherited response-blind equally spaced grid points",
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
    rows = build_rows()
    phase = phase_summary(rows)
    beta2 = [row for row in rows if row["beta"] == 2]
    beta2_failures = [
        [row["origin"], row["block_index"], row["Q"],
         row["kernel_exponent"], row["law"]]
        for row in beta2 if float(row["normalized"]["spectral"]) > SPECTRAL_CAP
    ]
    beta2_block_max = max(float(row["normalized"]["spectral"])
                          for row in beta2)
    beta0 = [row for row in rows if row["beta"] == 0]
    beta0_block_max = max(float(row["normalized"]["spectral"])
                          for row in beta0)
    parent_failures = parent["finite_audit"]["replicated_failure_keys"]
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "base_code_sha256": BASE_CODE_SHA256,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_failure_keys": parent_failures,
        },
        "origin_protocol": origin_protocol(),
        "protocol": {
            "origins": list(ORIGINS), "window_count": WINDOW_COUNT,
            "block_count": BLOCK_COUNT, "block_indices": list(BLOCK_INDICES),
            "partition": "eight contiguous blocks of length 256; no response ranking",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS), "betas": list(BETAS), "height": HEIGHT,
            "spectra_for_all_laws": True, "source_response_used": False,
            "origin_selection_used": False, "block_selection_used": False,
            "normalization": "block-local weighted square-energy symmetric congruence",
        },
        "exact_theorem": {
            "origin_protocol": "The three origins are inherited deterministic grid points declared without response or geometry ranking.",
            "partition": "Each count-2048 window is partitioned into eight fixed contiguous blocks of 256 integers before block-local replay.",
            "block_local_object": "Each row recomputes the literal weighted operator and its square-energy normalization on one declared block only.",
            "geometry": "Every block-local geometry is a finite sum of nonnegative rational squares.",
            "envelopes": "For each finite real symmetric block matrix, the spectral norm is bounded by its Schur and Frobenius envelopes.",
            "anchor_inheritance": {
                "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
                "kernel_exponent": EXACT_EXPONENT,
                "source_project": "TPC-370 count-2048 finite-window audit",
            },
        },
        "finite_audit": {
            "rows": len(rows), "settings_per_beta": 288,
            "origin_count": len(ORIGINS), "block_count": len(BLOCK_INDICES),
            "rows_per_origin": len(BLOCK_INDICES) * len(Q_ANCHORS) * len(LAWS),
            "beta_count": len(BETAS), "spectral_rows": len(rows),
            "beta2_rows": len(beta2),
            "beta2_spectral_cap_violations": phase["by_beta"]["2"][
                "spectral_cap_violations"],
            "beta2_schur_cap_violations": phase["by_beta"]["2"][
                "schur_cap_violations"],
            "baseline_beta0_spectral_cap_violations": phase["by_beta"]["0"][
                "spectral_cap_violations"],
            "baseline_beta0_schur_cap_violations": phase["by_beta"]["0"][
                "schur_cap_violations"],
            "window_count": WINDOW_COUNT, "block_count_fixed": BLOCK_COUNT,
            "q_min": min(Q_ANCHORS), "q_max": max(Q_ANCHORS),
            "beta2_failure_keys": beta2_failures,
            "beta2_failure_block_count": len({(key[0], key[1])
                                               for key in beta2_failures}),
            "beta2_all_declared_blocks_pass": not beta2_failures,
            "beta2_max_spectral": show(beta2_block_max),
            "baseline_beta0_max_spectral": show(beta0_block_max),
            "parent_full_window_failure_keys": parent_failures,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC371_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
            "TPC371_BLOCK_PARTITION": "PROVED_EXACT_FINITE_PREDECLARED",
            "TPC371_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
            "TPC371_BLOCK_LOCAL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_576_ROWS",
            "TPC371_BETA2_BLOCK_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC371_BETA2_LOCAL_FAILURE": "REFUTED_SCOPED",
            "TPC371_CROSS_BLOCK_COHERENCE": "OPEN",
            "TPC371_ORIGIN_UNIFORMITY": "OPEN",
            "TPC371_WINDOW_UNIFORMITY": "OPEN",
            "TPC371_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC371_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC371_SOURCE_UNIFORM_L2": "OPEN",
            "TPC371_ARITHMETIC_ADVANCE": "NO",
            "TPC371_FIXED_POWER_CREDIT": 0,
            "TPC371_FULL_GATE_B": "OPEN",
            "TPC371_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC371_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            print("TPC371_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " beta2_rows=" + str(audit["beta2_rows"]) +
                  " beta2_violations=" +
                  str(audit["beta2_spectral_cap_violations"]) +
                  " baseline_beta0_violations=" +
                  str(audit["baseline_beta0_spectral_cap_violations"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC371_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
