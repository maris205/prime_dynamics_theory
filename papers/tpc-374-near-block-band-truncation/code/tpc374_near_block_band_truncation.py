#!/usr/bin/env python3
"""TPC-374: common-normalization near-block band truncation audit."""

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
RESULT = PROJECT / "results/tpc374_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-373-eigenmode-block-separation/code/"
    "tpc373_eigenmode_block_separation.py")
PARENT_CERT = ROOT / (
    "papers/tpc-373-eigenmode-block-separation/results/"
    "tpc373_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "770877d4375f65b5eae61101e3bc8c8340737a19e3e2f22defc4f75c1640df49")
PARENT_CERT_SHA256 = (
    "7f54603589c49085ec6f35bf7752a505e85f2f2e9f979d448f42a8e7776a80e5")

SCHEMA = "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_NEAR_BLOCK_BAND_TRUNCATION"
ROUND2_CLUE = "TEST_BANDWIDTH_STABILITY"

ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(8))
BAND_CUTOFF = 3
Q_ANCHORS = (512, 2048, 8192)
EXPONENTS = (1,)
LAWS = ("all_plus",)
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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc374",
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
         payload.get("schema") == "TPC373_EIGENMODE_BLOCK_SEPARATION_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_EIGENMODE_BLOCK_SEPARATION",
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
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
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
        matrix += signs["all_plus"][index] * block
    matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrix, geometry, weights


def metrics(matrix: np.ndarray, eigenvalues: np.ndarray | None = None,
            compute_eigen: bool = True) -> tuple[dict[str, Any], np.ndarray,
                                                  np.ndarray | None]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    if compute_eigen:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    else:
        need(eigenvalues is not None, "eigenvalue input")
        eigenvectors = None
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0 and
         math.isfinite(spectral) and spectral > 0.0 and
         spectral <= schur + 5.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 5.0e-9 * max(1.0, frobenius),
         "finite metrics")
    return ({
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
    }, eigenvalues, eigenvectors)


def band_record(origin: int, q0: int, beta: int,
                parent: dict[str, Any]) -> dict[str, Any]:
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw, geometry, weights = weighted_components(
        values, q0, EXPONENTS[0], beta)
    scale = np.sqrt(geometry[:, None] * geometry[None, :])
    full = raw / scale
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    band_mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= BAND_CUTOFF
    band = np.where(band_mask, full, 0.0)
    tail = full - band
    full_metrics, full_eigenvalues, full_vectors = metrics(full)
    band_metrics, _, _ = metrics(band)
    tail_symmetry = float(np.max(np.abs(tail - tail.T)))
    tail_schur = float(np.max(np.sum(np.abs(tail), axis=1)))
    tail_frobenius = float(np.sqrt(np.sum(tail * tail)))
    need(tail_symmetry <= 1.0e-12 and tail_schur > 0 and
         math.isfinite(tail_frobenius) and tail_frobenius > 0,
         "tail metrics")
    lo, hi = float(full_eigenvalues[0]), float(full_eigenvalues[-1])
    if abs(lo) >= abs(hi):
        index = 0
        mode_name = "minimum_eigenvalue"
    else:
        index = len(full_eigenvalues) - 1
        mode_name = "maximum_eigenvalue"
    vector = np.asarray(full_vectors[:, index], dtype=np.float64)
    selected = float(full_eigenvalues[index])
    full_residual = float(np.max(np.abs(full @ vector - selected * vector)))
    band_rayleigh = float(vector @ (band @ vector))
    tail_rayleigh = float(vector @ (tail @ vector))
    rayleigh_error = abs(band_rayleigh + tail_rayleigh - selected)
    need(full_residual <= 3.0e-9 and
         abs(float(np.dot(vector, vector)) - 1.0) <= 2.0e-11 and
         math.isfinite(rayleigh_error) and rayleigh_error <= 2.0e-12,
         "mode/band identity")
    parent_failures = parent.get("finite_audit", {}).get("full_failure_keys", [])
    key = [origin, WINDOW_COUNT, q0, 1, "all_plus"]
    return {
        "origin": origin, "count": WINDOW_COUNT,
        "interval": [origin, origin + WINDOW_COUNT - 1], "Q": q0,
        "kernel_exponent": 1, "beta": beta, "law": "all_plus",
        "height": HEIGHT, "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "weight_effective_count": show(
            float(np.sum(np.asarray(weights) ** 2) ** 2 /
                  np.sum(np.asarray(weights) ** 4))),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                       np.min(geometry))),
        "full": full_metrics, "band": band_metrics,
        "tail": {"schur": show(tail_schur),
                  "frobenius": show(tail_frobenius),
                  "symmetry_error": show(tail_symmetry)},
        "mode": {
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
            "selected_mode": mode_name,
            "selected_eigenvalue": show(selected),
            "selected_eigenvalue_abs": show(abs(selected)),
            "eigen_residual_inf": show(full_residual),
            "full_mode_norm_error": show(abs(float(np.dot(vector, vector)) - 1.0)),
            "band_rayleigh": show(band_rayleigh),
            "tail_rayleigh": show(tail_rayleigh),
            "band_signed_retention": show(band_rayleigh / selected),
            "tail_signed_fraction": show(tail_rayleigh / selected),
            "band_rayleigh_abs_retention": show(abs(band_rayleigh) / abs(selected)),
            "tail_rayleigh_abs_fraction": show(abs(tail_rayleigh) / abs(selected)),
            "rayleigh_sum_error": show(rayleigh_error),
        },
        "parent_failure": key in parent_failures,
    }


def build_rows(parent: dict[str, Any]) -> list[dict[str, Any]]:
    jobs = [(beta, origin, q0) for beta in BETAS for origin in ORIGINS
            for q0 in Q_ANCHORS]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(
            lambda job: band_record(job[1], job[2], job[0], parent), jobs))
    need(len(rows) == 18, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_beta: dict[str, Any] = {}
    by_beta_q: dict[str, Any] = {}
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        band_retention = [float(row["mode"]["band_signed_retention"])
                          for row in selected]
        abs_tail = [float(row["mode"]["tail_rayleigh_abs_fraction"])
                    for row in selected]
        by_beta[str(beta)] = {
            "rows": len(selected),
            "full_spectral_cap_violations": sum(
                float(row["full"]["spectral"]) > SPECTRAL_CAP
                for row in selected),
            "full_schur_cap_violations": sum(
                float(row["full"]["schur"]) > SCHUR_CAP
                for row in selected),
            "band_spectral_cap_violations": sum(
                float(row["band"]["spectral"]) > SPECTRAL_CAP
                for row in selected),
            "band_schur_cap_violations": sum(
                float(row["band"]["schur"]) > SCHUR_CAP
                for row in selected),
            "minimum_mode_rows": sum(
                row["mode"]["selected_mode"] == "minimum_eigenvalue"
                for row in selected),
            "band_signed_retention_min": show(min(band_retention)),
            "band_signed_retention_max": show(max(band_retention)),
            "band_abs_retention_min": show(min(
                float(row["mode"]["band_rayleigh_abs_retention"])
                for row in selected)),
            "band_abs_retention_max": show(max(
                float(row["mode"]["band_rayleigh_abs_retention"])
                for row in selected)),
            "tail_abs_fraction_max": show(max(abs_tail)),
        }
        for q0 in Q_ANCHORS:
            setting = [row for row in selected if row["Q"] == q0]
            by_beta_q[f"{beta}:{q0}"] = {
                "beta": beta, "Q": q0, "rows": len(setting),
                "full_spectral_cap_violations": sum(
                    float(row["full"]["spectral"]) > SPECTRAL_CAP
                    for row in setting),
                "band_spectral_cap_violations": sum(
                    float(row["band"]["spectral"]) > SPECTRAL_CAP
                    for row in setting),
                "band_signed_retention_min": show(min(
                    float(row["mode"]["band_signed_retention"])
                    for row in setting)),
                "band_signed_retention_max": show(max(
                    float(row["mode"]["band_signed_retention"])
                    for row in setting)),
                "band_spectral_values": [row["band"]["spectral"]
                                         for row in setting],
            }
    return {"by_beta": by_beta, "by_beta_q": by_beta_q,
            "cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
            "band_cutoff": BAND_CUTOFF,
            "band_definition": "sum of layers with block distance <= 3",
            "cap_repair_betas": []}


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


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
            (BASE_CODE, BASE_CODE_SHA256, "base"),
            (PARENT_CODE, PARENT_CODE_SHA256, "parent code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "parent certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent()
    rows = build_rows(parent)
    phase = phase_summary(rows)
    beta2 = [row for row in rows if row["beta"] == 2]
    beta0 = [row for row in rows if row["beta"] == 0]
    full_failures = [[row["origin"], row["count"], row["Q"],
                      row["kernel_exponent"], row["law"]]
                     for row in beta2
                     if float(row["full"]["spectral"]) > SPECTRAL_CAP]
    band_failures = [[row["origin"], row["count"], row["Q"],
                      row["kernel_exponent"], row["law"]]
                     for row in beta2
                     if float(row["band"]["spectral"]) > SPECTRAL_CAP]
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "base_code_sha256": BASE_CODE_SHA256,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_round2_clue": parent["round2_clue"],
        },
        "protocol": {
            "origins": list(ORIGINS), "window_count": WINDOW_COUNT,
            "block_count": BLOCK_COUNT, "block_indices": list(BLOCK_INDICES),
            "partition": "fixed eight contiguous 256-point blocks",
            "band_cutoff": BAND_CUTOFF,
            "band_definition": "sum of layers with block distance <= 3",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS), "betas": list(BETAS), "height": HEIGHT,
            "common_normalization": True, "source_response_used": False,
            "origin_selection_used": False, "row_selection_used": False,
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
            "component_selection_used": False,
            "panel_complete_before_mode_read": True,
        },
        "exact_theorem": {
            "common_normalization":
                "The full-window square-energy geometry is used for T, B3, and T-B3.",
            "band_identity":
                "The fixed distance mask gives the exact finite identity T=B3+(T-B3).",
            "rayleigh_identity":
                "For the selected full-matrix eigenvector, the band and tail Rayleigh terms sum to its eigenvalue.",
            "eigenmode_rule":
                "The largest absolute eigenvalue is selected, with the minimum mode winning ties.",
            "geometry":
                "The full-window geometry is a finite sum of nonnegative rational squares.",
            "anchor_inheritance": {
                "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
                "kernel_exponent": EXACT_EXPONENT,
                "source_project": "TPC-373 eigenmode block separation",
            },
        },
        "finite_audit": {
            "rows": len(rows), "beta2_rows": len(beta2),
            "baseline_beta0_rows": len(beta0), "origin_count": len(ORIGINS),
            "q_count": len(Q_ANCHORS), "spectral_rows": len(rows),
            "beta2_full_spectral_cap_violations": phase["by_beta"]["2"][
                "full_spectral_cap_violations"],
            "beta2_full_schur_cap_violations": phase["by_beta"]["2"][
                "full_schur_cap_violations"],
            "beta2_band_spectral_cap_violations": phase["by_beta"]["2"][
                "band_spectral_cap_violations"],
            "beta2_band_schur_cap_violations": phase["by_beta"]["2"][
                "band_schur_cap_violations"],
            "baseline_beta0_full_spectral_cap_violations": phase["by_beta"]["0"][
                "full_spectral_cap_violations"],
            "baseline_beta0_full_schur_cap_violations": phase["by_beta"]["0"][
                "full_schur_cap_violations"],
            "full_failure_keys": full_failures,
            "band_failure_keys": band_failures,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase, "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC374_FULL_WINDOW_PROTOCOL":
                "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
            "TPC374_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
            "TPC374_NEAR_BLOCK_BAND":
                "PROVED_EXACT_FINITE_PREDECLARED",
            "TPC374_BAND_REPLAY":
                "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
            "TPC374_BAND_FAILURE_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC374_PARENT_FAILURE_REPRODUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC374_RAYLEIGH_RETENTION":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC374_TAIL_PROFILE":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC374_BAND_OPERATOR_UNIFORMITY": "OPEN",
            "TPC374_CROSS_BLOCK_CAUSALITY": "OPEN",
            "TPC374_ORIGIN_UNIFORMITY": "OPEN",
            "TPC374_WINDOW_UNIFORMITY": "OPEN",
            "TPC374_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC374_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC374_SOURCE_UNIFORM_L2": "OPEN",
            "TPC374_ARITHMETIC_ADVANCE": "NO",
            "TPC374_FIXED_POWER_CREDIT": 0,
            "TPC374_FULL_GATE_B": "OPEN",
            "TPC374_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC374_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            print("TPC374_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " beta2_rows=" + str(audit["beta2_rows"]) +
                  " beta2_violations=" + str(
                      audit["beta2_full_spectral_cap_violations"]) +
                  " band_beta2_violations=" + str(
                      audit["beta2_band_spectral_cap_violations"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC374_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
