#!/usr/bin/env python3
"""TPC-372: common-normalization block/off-block decomposition."""

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
RESULT = PROJECT / "results/tpc372_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-371-block-phase-localization/code/"
    "tpc371_block_phase_localization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-371-block-phase-localization/results/tpc371_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "a2190210a2d43eefb1f37f81f55b2240b6b254fd4f9afa1c26cd5e0c097d8462")
PARENT_CERT_SHA256 = (
    "01ba3b91db1f2a58b70da6b5334127f07350244f07b34772bf83dc4e69ac1ba3")

SCHEMA = "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_FULL_WINDOW_DECOMPOSITION"
ROUND2_CLUE = "TEST_EIGENMODE_BLOCK_SEPARATION"

ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(8))
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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc372",
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
         payload.get("schema") == "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_BLOCK_PHASE_LOCALIZATION",
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
         spectral <= schur + 3.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 3.0e-9 * max(1.0, frobenius),
         "finite spectral envelopes")
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
    }


def decomposition_record(origin: int, q0: int, beta: int,
                          parent: dict[str, Any]) -> dict[str, Any]:
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw_matrix, geometry, weights = weighted_components(
        values, q0, EXPONENTS[0], beta)
    scale = np.sqrt(geometry[:, None] * geometry[None, :])
    full = raw_matrix / scale
    diagonal = np.zeros_like(full)
    for block_index in BLOCK_INDICES:
        lo = block_index * BLOCK_COUNT
        hi = lo + BLOCK_COUNT
        diagonal[lo:hi, lo:hi] = full[lo:hi, lo:hi]
    off = full - diagonal
    full_metrics = matrix_metrics(full)
    diagonal_metrics = matrix_metrics(diagonal)
    off_metrics = matrix_metrics(off)
    reconstruction_error = float(np.max(np.abs(full - diagonal - off)))
    need(math.isfinite(reconstruction_error) and reconstruction_error <= 1.0e-15,
         "decomposition identity")
    parent_keys = parent.get("finite_audit", {}).get(
        "parent_full_window_failure_keys", [])
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
        "full": full_metrics, "block_diagonal": diagonal_metrics,
        "off_block": off_metrics,
        "lower_bound_off_spectral": show(
            float(full_metrics["spectral"]) -
            float(diagonal_metrics["spectral"])),
        "off_minus_lower_bound": show(
            float(off_metrics["spectral"]) -
            float(full_metrics["spectral"]) +
            float(diagonal_metrics["spectral"])),
        "decomposition_error": show(reconstruction_error),
        "parent_failure_keys": parent_keys,
    }


def build_rows(parent: dict[str, Any]) -> list[dict[str, Any]]:
    jobs = [(beta, origin, q0) for beta in BETAS for origin in ORIGINS
            for q0 in Q_ANCHORS]
    # Each setting is independent.  One BLAS thread per worker keeps the
    # replay reproducible while using the available server CPUs.
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(
            lambda job: decomposition_record(job[1], job[2], job[0], parent),
            jobs))
    need(len(rows) == 18, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_beta: dict[str, Any] = {}
    by_beta_q: dict[str, Any] = {}
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        by_beta[str(beta)] = {
            "rows": len(selected),
            "full_spectral_cap_violations": sum(
                float(row["full"]["spectral"]) > SPECTRAL_CAP
                for row in selected),
            "full_schur_cap_violations": sum(
                float(row["full"]["schur"]) > SCHUR_CAP
                for row in selected),
            "block_diagonal_spectral_cap_violations": sum(
                float(row["block_diagonal"]["spectral"]) > SPECTRAL_CAP
                for row in selected),
            "block_diagonal_schur_cap_violations": sum(
                float(row["block_diagonal"]["schur"]) > SCHUR_CAP
                for row in selected),
            "off_block_spectral_cap_violations": sum(
                float(row["off_block"]["spectral"]) > SPECTRAL_CAP
                for row in selected),
            "full_spectral_max": show(max(
                float(row["full"]["spectral"]) for row in selected)),
            "block_diagonal_spectral_max": show(max(
                float(row["block_diagonal"]["spectral"]) for row in selected)),
            "off_block_spectral_max": show(max(
                float(row["off_block"]["spectral"]) for row in selected)),
            "lower_bound_off_max": show(max(
                float(row["lower_bound_off_spectral"]) for row in selected)),
        }
        for q0 in Q_ANCHORS:
            setting = [row for row in selected if row["Q"] == q0]
            by_beta_q[f"{beta}:{q0}"] = {
                "beta": beta, "Q": q0, "rows": len(setting),
                "full_spectral_cap_violations": sum(
                    float(row["full"]["spectral"]) > SPECTRAL_CAP
                    for row in setting),
                "block_diagonal_spectral_cap_violations": sum(
                    float(row["block_diagonal"]["spectral"]) > SPECTRAL_CAP
                    for row in setting),
                "off_block_spectral_cap_violations": sum(
                    float(row["off_block"]["spectral"]) > SPECTRAL_CAP
                    for row in setting),
                "full_spectral_max": show(max(
                    float(row["full"]["spectral"]) for row in setting)),
                "block_diagonal_spectral_max": show(max(
                    float(row["block_diagonal"]["spectral"]) for row in setting)),
                "off_block_spectral_max": show(max(
                    float(row["off_block"]["spectral"]) for row in setting)),
            }
    return {"by_beta": by_beta, "by_beta_q": by_beta_q,
            "cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
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
    diagonal_failures = [[row["origin"], row["Q"]]
                         for row in beta2
                         if float(row["block_diagonal"]["spectral"]) > SPECTRAL_CAP]
    required_off = [[row["origin"], row["Q"]]
                    for row in beta2
                    if float(row["full"]["spectral"]) > SPECTRAL_CAP and
                    float(row["block_diagonal"]["spectral"]) <= SPECTRAL_CAP]
    max_error = max(float(row["decomposition_error"]) for row in rows)
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "base_code_sha256": BASE_CODE_SHA256,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_block_phase": parent["finite_audit"][
                "beta2_all_declared_blocks_pass"],
        },
        "protocol": {
            "origins": list(ORIGINS), "window_count": WINDOW_COUNT,
            "block_count": BLOCK_COUNT, "block_indices": list(BLOCK_INDICES),
            "partition": "fixed eight contiguous 256-point blocks",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS), "betas": list(BETAS), "height": HEIGHT,
            "common_normalization": True, "source_response_used": False,
            "origin_selection_used": False, "component_selection_used": False,
            "decomposition": "full normalized matrix = block diagonal + off block",
        },
        "exact_theorem": {
            "common_normalization": "The full-window square-energy geometry is used for A, D, and R.",
            "decomposition": "The fixed block mask gives the exact finite identity A=D+R.",
            "triangle_bound": "The reverse triangle inequality gives ||R||_2 >= ||A||_2-||D||_2.",
            "geometry": "The full-window geometry is a finite sum of nonnegative rational squares.",
            "anchor_inheritance": {
                "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
                "kernel_exponent": EXACT_EXPONENT,
                "source_project": "TPC-371 block-local phase localization",
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
            "beta2_block_diagonal_spectral_cap_violations": phase["by_beta"]["2"][
                "block_diagonal_spectral_cap_violations"],
            "beta2_block_diagonal_schur_cap_violations": phase["by_beta"]["2"][
                "block_diagonal_schur_cap_violations"],
            "beta2_off_block_spectral_cap_violations": phase["by_beta"]["2"][
                "off_block_spectral_cap_violations"],
            "baseline_beta0_full_spectral_cap_violations": phase["by_beta"]["0"][
                "full_spectral_cap_violations"],
            "baseline_beta0_full_schur_cap_violations": phase["by_beta"]["0"][
                "full_schur_cap_violations"],
            "full_failure_keys": full_failures,
            "block_diagonal_beta2_failure_keys": diagonal_failures,
            "required_off_block_keys": required_off,
            "decomposition_max_error": show(max_error),
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase, "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC372_FULL_WINDOW_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
            "TPC372_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
            "TPC372_DECOMPOSITION_IDENTITY": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC372_FULL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
            "TPC372_BETA2_FULL_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC372_BLOCK_DIAGONAL_PHASE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC372_OFF_BLOCK_NECESSITY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC372_CROSS_BLOCK_CAUSALITY": "OPEN",
            "TPC372_ORIGIN_UNIFORMITY": "OPEN",
            "TPC372_WINDOW_UNIFORMITY": "OPEN",
            "TPC372_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC372_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC372_SOURCE_UNIFORM_L2": "OPEN",
            "TPC372_ARITHMETIC_ADVANCE": "NO",
            "TPC372_FIXED_POWER_CREDIT": 0,
            "TPC372_FULL_GATE_B": "OPEN",
            "TPC372_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC372_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            print("TPC372_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " beta2_rows=" + str(audit["beta2_rows"]) +
                  " beta2_violations=" + str(
                      audit["beta2_full_spectral_cap_violations"]) +
                  " diagonal_beta2_violations=" + str(
                      audit["beta2_block_diagonal_spectral_cap_violations"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC372_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
