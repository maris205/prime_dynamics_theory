#!/usr/bin/env python3
"""Independent reverse-shell replay for the TPC-374 band audit."""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-374-near-block-band-truncation"
CERTIFICATE = PROJECT / "results/tpc374_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-373-eigenmode-block-separation/code/"
    "tpc373_eigenmode_block_separation.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-373-eigenmode-block-separation/results/tpc373_certificate.json")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "770877d4375f65b5eae61101e3bc8c8340737a19e3e2f22defc4f75c1640df49")
PARENT_CERTIFICATE_SHA256 = (
    "7f54603589c49085ec6f35bf7752a505e85f2f2e9f979d448f42a8e7776a80e5")

SCHEMA = "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_NEAR_BLOCK_BAND_TRUNCATION"
ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
Q_ANCHORS = (512, 2048, 8192)
BETAS = (0, 2)
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1010346, 1010359)
BLOCK_INDICES = tuple(range(8))
BAND_CUTOFF = 3


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


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 1.0e-5) -> None:
    target = float(recorded)
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label + " actual=" + repr(actual) + " recorded=" + repr(target))


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(50_000)


def shell_for(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def reverse_components(values: np.ndarray, q0: int, beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = float(HEIGHT * HEIGHT) / (HEIGHT * HEIGHT +
                                         distance * distance)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    geometry = np.zeros(len(values), dtype=np.float64)
    weights = [0.0] * len(primes)
    # Reverse order and an independent sieve distinguish this replay from the
    # producer's ascending shell accumulation.
    for index in range(len(primes) - 1, -1, -1):
        prime = primes[index]
        weight = (float(prime) / float(q0)) ** beta
        weights[index] = weight
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        matrix += block
    matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrix, geometry, weights


def spectral_metrics(matrix: np.ndarray, vectors: bool = False):
    if vectors:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    else:
        eigenvalues = np.linalg.eigvalsh(matrix)
        eigenvectors = None
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and schur > 0 and
         math.isfinite(frobenius) and frobenius > 0 and
         math.isfinite(spectral) and spectral > 0 and
         spectral <= schur + 6.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 6.0e-9 * max(1.0, frobenius),
         "spectral envelopes")
    return ({"schur": schur, "frobenius": frobenius, "spectral": spectral,
             "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
             "symmetry_error": symmetry,
             "spectral_over_schur": spectral / schur,
             "spectral_over_frobenius": spectral / frobenius,
             "schur_row_index": int(np.argmax(row_mass))},
            eigenvalues, eigenvectors)


def replay_row(beta: int, origin: int, q0: int):
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw, geometry, weights = reverse_components(values, q0, beta)
    full = raw / np.sqrt(geometry[:, None] * geometry[None, :])
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= BAND_CUTOFF
    band = np.where(mask, full, 0.0)
    tail = full - band
    full_data, eigenvalues, vectors = spectral_metrics(full, vectors=True)
    band_data, _, _ = spectral_metrics(band, vectors=False)
    tail_symmetry = float(np.max(np.abs(tail - tail.T)))
    tail_schur = float(np.max(np.sum(np.abs(tail), axis=1)))
    tail_frobenius = float(np.sqrt(np.sum(tail * tail)))
    need(tail_symmetry <= 1.0e-12 and tail_schur > 0 and
         math.isfinite(tail_frobenius) and tail_frobenius > 0,
         "tail metrics")
    index = 0 if abs(float(eigenvalues[0])) >= abs(float(eigenvalues[-1])) \
        else len(eigenvalues) - 1
    mode = "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue"
    vector = np.asarray(vectors[:, index], dtype=np.float64)
    selected = float(eigenvalues[index])
    band_rayleigh = float(vector @ (band @ vector))
    tail_rayleigh = float(vector @ (tail @ vector))
    return (beta, origin, q0, primes, geometry, weights, full_data,
            band_data, tail_schur, tail_frobenius, mode, selected,
            vector, band_rayleigh, tail_rayleigh,
            abs(band_rayleigh + tail_rayleigh - selected),
            abs(float(np.dot(vector, vector)) - 1.0),
            float(np.max(np.abs(full @ vector - selected * vector))),
            tail_symmetry)


def expected_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell_for(4)

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
                    weighted = Fraction(prime, 4) ** beta * base
                    total += weighted
                    energy += weighted * weighted
                row.append(total)
                grow += energy
            matrix.append(row)
            geometry.append(grow)
        need(all(matrix[i][j] == matrix[j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "anchor symmetry")
        need(all(value > 0 for value in geometry), "anchor positivity")
        anchors.append({
            "beta": beta, "interval": list(EXACT_INTERVAL), "Q": 4,
            "kernel_exponent": 1, "shell": primes,
            "matrix_symmetric": True, "geometry_positive": True,
            "matrix_digest": hashlib.sha256(canonical([
                [text(value) for value in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(value) for value in geometry])).hexdigest(),
        })
    return {"anchors": anchors}


def validate(document: dict[str, Any]) -> dict[str, Any]:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema/status")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(digest(BASE_CODE.read_bytes()) == BASE_SHA256, "base provenance")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    parent_raw = PARENT_CERTIFICATE.read_bytes()
    need(digest(parent_raw) == PARENT_CERTIFICATE_SHA256,
         "parent certificate provenance")
    parent = json.loads(parent_raw)
    need(parent_raw == canonical(parent), "parent certificate canonicality")
    lock = payload.get("parent_lock", {})
    need(lock == {
        "base_code_sha256": BASE_SHA256,
        "parent_code_sha256": PARENT_CODE_SHA256,
        "parent_certificate_sha256": PARENT_CERTIFICATE_SHA256,
        "parent_schema": "TPC373_EIGENMODE_BLOCK_SEPARATION_V1",
        "parent_round2_clue": "TEST_LAYERWISE_CROSS_BLOCK_DECAY",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("window_count") == WINDOW_COUNT and
         protocol.get("block_count") == BLOCK_COUNT and
         protocol.get("block_indices") == list(BLOCK_INDICES) and
         protocol.get("partition") ==
         "fixed eight contiguous 256-point blocks" and
         protocol.get("band_cutoff") == BAND_CUTOFF and
         protocol.get("band_definition") ==
         "sum of layers with block distance <= 3" and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus"] and
         protocol.get("betas") == list(BETAS) and protocol.get("height") == HEIGHT and
         protocol.get("common_normalization") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("row_selection_used") is False and
         protocol.get("component_selection_used") is False and
         protocol.get("panel_complete_before_mode_read") is True and
         protocol.get("mode_rule") ==
         "largest absolute eigenvalue; minimum mode wins ties", "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, beta, "all_plus")
                for beta in BETAS for o in ORIGINS for q in Q_ANCHORS}
    need(isinstance(rows, list) and len(rows) == 18 and
         {(r.get("origin"), r.get("Q"), r.get("kernel_exponent"),
           r.get("beta"), r.get("law")) for r in rows} == expected,
         "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    jobs = [(row["beta"], row["origin"], row["Q"]) for row in rows]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda job: replay_row(*job), jobs))
    by_key = {(item[1], item[2], item[0]): item for item in results}
    parent_failures = parent["payload"]["finite_audit"]["full_failure_keys"]
    for row in rows:
        item = by_key[(row["origin"], row["Q"], row["beta"])]
        (_, _, _, primes, geometry, weights, full_data, band_data,
         tail_schur, tail_frobenius, mode, selected, vector,
         band_rayleigh, tail_rayleigh, rayleigh_error, norm_error,
         eigen_residual, tail_symmetry) = item
        need(row["shell"] == primes and row["shell_cardinality"] == len(primes),
             "shell")
        close(min(weights), row["weight_min"], "weight min")
        close(max(weights), row["weight_max"], "weight max")
        close(float(np.min(geometry)), row["geometry_min"], "geometry min")
        close(float(np.max(geometry)), row["geometry_max"], "geometry max")
        close(float(np.max(geometry) / np.min(geometry)),
              row["geometry_spread"], "geometry spread")
        for component, actual in (("full", full_data), ("band", band_data)):
            recorded = row[component]
            for name in ("schur", "frobenius", "spectral",
                         "minimum_eigenvalue", "maximum_eigenvalue",
                         "symmetry_error", "spectral_over_schur",
                         "spectral_over_frobenius"):
                close(actual[name], recorded[name], component + " " + name)
            need(actual["schur_row_index"] == recorded["schur_row_index"],
                 component + " index")
        tail = row["tail"]
        close(tail_schur, tail["schur"], "tail schur")
        close(tail_frobenius, tail["frobenius"], "tail frobenius")
        close(tail_symmetry, tail["symmetry_error"], "tail symmetry", 1.0e-12)
        recorded_mode = row["mode"]
        need(recorded_mode["mode_rule"] ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             recorded_mode["selected_mode"] == mode, "mode rule")
        for name, actual in (
                ("selected_eigenvalue", selected),
                ("selected_eigenvalue_abs", abs(selected)),
                ("eigen_residual_inf", eigen_residual),
                ("full_mode_norm_error", norm_error),
                ("band_rayleigh", band_rayleigh),
                ("tail_rayleigh", tail_rayleigh),
                ("band_signed_retention", band_rayleigh / selected),
                ("tail_signed_fraction", tail_rayleigh / selected),
                ("band_rayleigh_abs_retention", abs(band_rayleigh) / abs(selected)),
                ("tail_rayleigh_abs_fraction", abs(tail_rayleigh) / abs(selected)),
                ("rayleigh_sum_error", rayleigh_error)):
            close(actual, recorded_mode[name], "mode " + name, 2.0e-5)
        need(eigen_residual <= 3.0e-9 and norm_error <= 2.0e-11,
             "mode residual audit")
        expected_parent = [row["origin"], row["count"], row["Q"],
                           row["kernel_exponent"], row["law"]] in parent_failures
        need(row["parent_failure"] is expected_parent, "parent flag")

    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("band_cutoff") == BAND_CUTOFF and
         phase.get("band_definition") ==
         "sum of layers with block distance <= 3" and
         phase.get("cap_repair_betas") == [], "phase header")
    for beta in BETAS:
        selected = [r for r in rows if r["beta"] == beta]
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 9 and
             item.get("full_spectral_cap_violations") == sum(
                 float(r["full"]["spectral"]) > SPECTRAL_CAP for r in selected) and
             item.get("full_schur_cap_violations") == sum(
                 float(r["full"]["schur"]) > SCHUR_CAP for r in selected) and
             item.get("band_spectral_cap_violations") == sum(
                 float(r["band"]["spectral"]) > SPECTRAL_CAP for r in selected) and
             item.get("band_schur_cap_violations") == sum(
                 float(r["band"]["schur"]) > SCHUR_CAP for r in selected) and
             item.get("minimum_mode_rows") == 9,
             "phase beta")
    audit = payload.get("finite_audit", {})
    beta2 = [r for r in rows if r["beta"] == 2]
    beta0 = [r for r in rows if r["beta"] == 0]
    actual_failures = [[r["origin"], r["count"], r["Q"],
                        r["kernel_exponent"], r["law"]]
                       for r in beta2 if float(r["full"]["spectral"]) > .64]
    actual_bands = [[r["origin"], r["count"], r["Q"],
                     r["kernel_exponent"], r["law"]]
                    for r in beta2 if float(r["band"]["spectral"]) > .64]
    need(audit.get("rows") == 18 and audit.get("beta2_rows") == 9 and
         audit.get("baseline_beta0_rows") == 9 and audit.get("origin_count") == 3 and
         audit.get("q_count") == 3 and audit.get("spectral_rows") == 18 and
         audit.get("beta2_full_spectral_cap_violations") == len(actual_failures) and
         audit.get("beta2_full_schur_cap_violations") == sum(
             float(r["full"]["schur"]) > SCHUR_CAP for r in beta2) and
         audit.get("beta2_band_spectral_cap_violations") == len(actual_bands) and
         audit.get("beta2_band_schur_cap_violations") == sum(
             float(r["band"]["schur"]) > SCHUR_CAP for r in beta2) and
         audit.get("baseline_beta0_full_spectral_cap_violations") == sum(
             float(r["full"]["spectral"]) > SPECTRAL_CAP for r in beta0) and
         audit.get("baseline_beta0_full_schur_cap_violations") == sum(
             float(r["full"]["schur"]) > SCHUR_CAP for r in beta0) and
         audit.get("full_failure_keys") == actual_failures and
         audit.get("band_failure_keys") == actual_bands and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    need(payload.get("exact_anchor") == expected_anchor(), "exact anchor")
    expected_firewall = {
        "TPC374_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC374_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC374_NEAR_BLOCK_BAND": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC374_BAND_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC374_BAND_FAILURE_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_PARENT_FAILURE_REPRODUCTION":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_RAYLEIGH_RETENTION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_TAIL_PROFILE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
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
    }
    need(payload.get("claim_firewall") == expected_firewall, "firewall")
    need(payload.get("round2_clue") == "TEST_BANDWIDTH_STABILITY", "clue")
    return payload


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        payload = validate(document)
        print("TPC374_INDEPENDENT_CHECK=PASS rows=18 beta2_rows=9 "
              "beta2_violations=" + str(
                  payload["finite_audit"][
                      "beta2_full_spectral_cap_violations"]) +
              " band_beta2_violations=" + str(
                  payload["finite_audit"][
                      "beta2_band_spectral_cap_violations"]))
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC374_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
