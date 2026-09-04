#!/usr/bin/env python3
"""TPC-375: finite bandwidth-stability and minimal-cutoff audit."""

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
RESULT = PROJECT / "results/tpc375_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-374-near-block-band-truncation/code/"
    "tpc374_near_block_band_truncation.py")
PARENT_CERT = ROOT / (
    "papers/tpc-374-near-block-band-truncation/results/"
    "tpc374_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "09851134f9c2d2444c42702b1649e49d259cb9316291ee5b7c275a92b96a9cd0")
PARENT_CERT_SHA256 = (
    "c49310bd080f609f90ee03a74beeda7fbd7ebae0b5f25012a06235f42a047c40")

SCHEMA = "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_STABILITY"
ROUND2_CLUE = "TEST_BANDWIDTH_HOLDOUT"

ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(8))
BAND_CUTOFFS = (0, 1, 2, 3)
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
LAW = "all_plus"
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1010346, 1010359)
EXACT_Q = 4


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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc375",
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
         payload.get("schema") == "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_NEAR_BLOCK_BAND_TRUNCATION",
         "parent payload")
    return payload


def weighted_components(values: np.ndarray, q0: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + distance * distance) ** EXPONENT)
    np.fill_diagonal(kernel, 0.0)
    primes = BASE.shell_for(q0)
    signs = BASE.sign_patterns(primes)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
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
        matrix += signs[LAW][index] * block
    matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrix, geometry, weights


def eigenvalues_for(matrix: np.ndarray, cutoff: int | None = None):
    """Use block-local eigensolves for B0, avoiding a false dense shortcut."""
    if cutoff == 0:
        pieces = []
        for block in BLOCK_INDICES:
            lo = block * BLOCK_COUNT
            hi = lo + BLOCK_COUNT
            pieces.append(np.linalg.eigvalsh(matrix[lo:hi, lo:hi]))
        return np.concatenate(pieces)
    return np.linalg.eigvalsh(matrix)


def metrics(matrix: np.ndarray, cutoff: int | None = None,
            eigenvalues: np.ndarray | None = None):
    if eigenvalues is None:
        eigenvalues = eigenvalues_for(matrix, cutoff)
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and schur > 0.0 and frobenius > 0.0 and
         math.isfinite(frobenius) and math.isfinite(spectral) and
         spectral > 0.0 and
         spectral <= schur + 6.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 6.0e-9 * max(1.0, frobenius),
         "finite metric envelope")
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
    }


def cutoff_key(cutoff: int) -> str:
    return str(cutoff)


def band_record(origin: int, q0: int, parent: dict[str, Any]):
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw, geometry, weights = weighted_components(values, q0)
    full = raw / np.sqrt(geometry[:, None] * geometry[None, :])
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    full_eigenvalues, full_vectors = np.linalg.eigh(full)
    full_data = metrics(full, eigenvalues=full_eigenvalues)
    lo, hi = float(full_eigenvalues[0]), float(full_eigenvalues[-1])
    index = 0 if abs(lo) >= abs(hi) else len(full_eigenvalues) - 1
    mode_name = "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue"
    vector = np.asarray(full_vectors[:, index], dtype=np.float64)
    selected = float(full_eigenvalues[index])
    full_residual = float(np.max(np.abs(full @ vector - selected * vector)))
    bands: dict[str, Any] = {}
    band_failure_flags: dict[str, bool] = {}
    mode_by_cutoff: dict[str, Any] = {}
    for cutoff in BAND_CUTOFFS:
        mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= cutoff
        band = np.where(mask, full, 0.0)
        tail = full - band
        band_eigenvalues = eigenvalues_for(band, cutoff)
        bands[cutoff_key(cutoff)] = metrics(
            band, cutoff=cutoff, eigenvalues=band_eigenvalues)
        band_rayleigh = float(vector @ (band @ vector))
        tail_rayleigh = float(vector @ (tail @ vector))
        rayleigh_error = abs(band_rayleigh + tail_rayleigh - selected)
        tail_schur = float(np.max(np.sum(np.abs(tail), axis=1)))
        tail_frobenius = float(np.sqrt(np.sum(tail * tail)))
        tail_symmetry = float(np.max(np.abs(tail - tail.T)))
        need(tail_symmetry <= 1.0e-12 and tail_schur >= 0.0 and
             math.isfinite(tail_frobenius) and rayleigh_error <= 3.0e-12,
             "band/tail identity")
        mode_by_cutoff[cutoff_key(cutoff)] = {
            "band_rayleigh": show(band_rayleigh),
            "tail_rayleigh": show(tail_rayleigh),
            "band_signed_retention": show(band_rayleigh / selected),
            "tail_signed_fraction": show(tail_rayleigh / selected),
            "band_rayleigh_abs_retention": show(
                abs(band_rayleigh) / abs(selected)),
            "tail_rayleigh_abs_fraction": show(
                abs(tail_rayleigh) / abs(selected)),
            "rayleigh_sum_error": show(rayleigh_error),
            "tail_schur": show(tail_schur),
            "tail_frobenius": show(tail_frobenius),
            "tail_symmetry_error": show(tail_symmetry),
        }
        band_failure_flags[cutoff_key(cutoff)] = (
            float(bands[cutoff_key(cutoff)]["spectral"]) > SPECTRAL_CAP)
    parent_failures = parent.get("finite_audit", {}).get("band_failure_keys", [])
    parent_key = [origin, WINDOW_COUNT, q0, EXPONENT, LAW]
    need(parent_key in parent_failures or q0 == Q_ANCHORS[0],
         "parent support inheritance")
    return {
        "origin": origin, "count": WINDOW_COUNT,
        "interval": [origin, origin + WINDOW_COUNT - 1], "Q": q0,
        "kernel_exponent": EXPONENT, "beta": BETA, "law": LAW,
        "height": HEIGHT, "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                       np.min(geometry))),
        "full": full_data, "bands": bands,
        "mode": {
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
            "selected_mode": mode_name,
            "selected_eigenvalue": show(selected),
            "selected_eigenvalue_abs": show(abs(selected)),
            "eigen_residual_inf": show(full_residual),
            "full_mode_norm_error": show(abs(float(np.dot(vector, vector)) - 1.0)),
            "by_cutoff": mode_by_cutoff,
        },
        "band_failure_flags": band_failure_flags,
    }


def build_rows(parent: dict[str, Any]):
    jobs = [(origin, q0) for origin in ORIGINS for q0 in Q_ANCHORS]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda job: band_record(job[0], job[1], parent),
                             jobs))
    need(len(rows) == 9, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]):
    by_cutoff: dict[str, Any] = {}
    by_cutoff_q: dict[str, Any] = {}
    for cutoff in BAND_CUTOFFS:
        key = cutoff_key(cutoff)
        failures = [row for row in rows if row["band_failure_flags"][key]]
        schur_failures = [row for row in rows
                          if float(row["bands"][key]["schur"]) > SCHUR_CAP]
        ret = [float(row["mode"]["by_cutoff"][key]
                     ["band_rayleigh_abs_retention"]) for row in rows]
        tails = [float(row["mode"]["by_cutoff"][key]
                       ["tail_rayleigh_abs_fraction"]) for row in rows]
        by_cutoff[key] = {
            "cutoff": cutoff, "rows": len(rows),
            "spectral_cap_violations": len(failures),
            "schur_cap_violations": len(schur_failures),
            "failure_keys": [[r["origin"], r["count"], r["Q"],
                              r["kernel_exponent"], r["law"]]
                             for r in failures],
            "band_abs_retention_min": show(min(ret)),
            "band_abs_retention_max": show(max(ret)),
            "tail_abs_fraction_max": show(max(tails)),
        }
        for q0 in Q_ANCHORS:
            setting = [r for r in rows if r["Q"] == q0]
            qfail = [r for r in setting if r["band_failure_flags"][key]]
            by_cutoff_q[f"{cutoff}:{q0}"] = {
                "cutoff": cutoff, "Q": q0, "rows": len(setting),
                "spectral_cap_violations": len(qfail),
                "spectral_values": [r["bands"][key]["spectral"]
                                    for r in setting],
            }
    minimal = []
    for row in rows:
        first = next((c for c in BAND_CUTOFFS
                      if row["band_failure_flags"][cutoff_key(c)]), None)
        minimal.append(first)
    return {
        "by_cutoff": by_cutoff, "by_cutoff_q": by_cutoff_q,
        "caps": {"spectral": show(SPECTRAL_CAP), "schur": show(SCHUR_CAP)},
        "cutoffs": list(BAND_CUTOFFS),
        "band_definition": "block distance <= cutoff",
        "minimal_failure_cutoff_census": {
            str(c): minimal.count(c) for c in BAND_CUTOFFS
        },
        "never_failure_rows": minimal.count(None),
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = BASE.shell_for(EXACT_Q)

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

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
                weight = Fraction(prime, EXACT_Q) ** BETA
                weighted = weight * base
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
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": EXPONENT, "beta": BETA, "shell": primes,
        "matrix_symmetric": True, "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [text(value) for value in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


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
    failure_keys = phase["by_cutoff"]["3"]["failure_keys"]
    parent_failure_keys = parent["finite_audit"]["band_failure_keys"]
    need(failure_keys == parent_failure_keys,
         "B3 parent failure support")
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
            "band_cutoffs": list(BAND_CUTOFFS),
            "band_definition": "sum of layers with block distance <= cutoff",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "laws": [LAW], "betas": [BETA], "height": HEIGHT,
            "common_normalization": True, "source_response_used": False,
            "origin_selection_used": False, "row_selection_used": False,
            "component_selection_used": False,
            "panel_complete_before_cutoff_read": True,
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        },
        "exact_theorem": {
            "common_normalization":
                "The full-window square-energy geometry is shared by T and every Bcutoff.",
            "band_identity":
                "For each cutoff c, T=B_c+(T-B_c) entrywise on the finite window.",
            "cutoff_nestedness":
                "The masks are predeclared and nested as c increases from 0 to 3.",
            "rayleigh_identity":
                "For the selected full eigenvector, band and tail Rayleigh terms sum to lambda.",
            "geometry":
                "The full-window geometry is a finite sum of nonnegative rational squares.",
            "anchor_inheritance": {
                "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
                "kernel_exponent": EXPONENT,
                "source_project": "TPC-374 near-block band truncation",
            },
        },
        "finite_audit": {
            "rows": len(rows), "origin_count": len(ORIGINS),
            "q_count": len(Q_ANCHORS), "cutoff_count": len(BAND_CUTOFFS),
            "spectral_rows": len(rows),
            "spectral_cap_violations_by_cutoff": {
                str(c): phase["by_cutoff"][str(c)]["spectral_cap_violations"]
                for c in BAND_CUTOFFS},
            "schur_cap_violations_by_cutoff": {
                str(c): phase["by_cutoff"][str(c)]["schur_cap_violations"]
                for c in BAND_CUTOFFS},
            "failure_keys_by_cutoff": {
                str(c): phase["by_cutoff"][str(c)]["failure_keys"]
                for c in BAND_CUTOFFS},
            "parent_failure_keys": parent_failure_keys,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC375_FULL_WINDOW_PROTOCOL":
                "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
            "TPC375_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
            "TPC375_NESTED_BAND_MASKS": "PROVED_EXACT_FINITE_PREDECLARED",
            "TPC375_BANDWIDTH_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_9_ROWS",
            "TPC375_FAILURE_CUTOFF_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC375_PARENT_SUPPORT_REPRODUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC375_RAYLEIGH_RETENTION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC375_MINIMAL_CUTOFF": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC375_BANDWIDTH_UNIFORMITY": "OPEN",
            "TPC375_CROSS_BLOCK_CAUSALITY": "OPEN",
            "TPC375_ORIGIN_UNIFORMITY": "OPEN",
            "TPC375_WINDOW_UNIFORMITY": "OPEN",
            "TPC375_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC375_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC375_SOURCE_UNIFORM_L2": "OPEN",
            "TPC375_ARITHMETIC_ADVANCE": "NO",
            "TPC375_FIXED_POWER_CREDIT": 0,
            "TPC375_FULL_GATE_B": "OPEN",
            "TPC375_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC375_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            counts = audit["spectral_cap_violations_by_cutoff"]
            print("TPC375_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " failures=" + ",".join(
                      str(counts[str(c)]) for c in BAND_CUTOFFS) +
                  " b3_parent_match=1")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC375_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
