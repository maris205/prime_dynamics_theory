#!/usr/bin/env python3
"""Independent reverse-shell replay for the TPC-375 bandwidth audit."""

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
PROJECT = ROOT / "papers/tpc-375-bandwidth-stability-minimal-cutoff"
CERTIFICATE = PROJECT / "results/tpc375_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-374-near-block-band-truncation/code/"
    "tpc374_near_block_band_truncation.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-374-near-block-band-truncation/results/"
    "tpc374_certificate.json")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "09851134f9c2d2444c42702b1649e49d259cb9316291ee5b7c275a92b96a9cd0")
PARENT_CERTIFICATE_SHA256 = (
    "c49310bd080f609f90ee03a74beeda7fbd7ebae0b5f25012a06235f42a047c40")

SCHEMA = "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_STABILITY"
ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BAND_CUTOFFS = (0, 1, 2, 3)
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
LAW = "all_plus"
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1010346, 1010359)


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
          tolerance: float = 2.0e-5) -> None:
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


def reverse_components(values: np.ndarray, q0: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = float(HEIGHT * HEIGHT) / (HEIGHT * HEIGHT +
                                         distance * distance)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = [0.0] * len(primes)
    # Descending shell order is deliberately independent of the producer.
    for index in range(len(primes) - 1, -1, -1):
        prime = primes[index]
        weight = (float(prime) / float(q0)) ** BETA
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


def eigenvalues_for(matrix: np.ndarray, cutoff: int | None = None):
    if cutoff == 0:
        pieces = []
        for block in range(8):
            lo = block * BLOCK_COUNT
            pieces.append(np.linalg.eigvalsh(matrix[lo:lo + BLOCK_COUNT,
                                                    lo:lo + BLOCK_COUNT]))
        return np.concatenate(pieces)
    return np.linalg.eigvalsh(matrix)


def metrics(matrix: np.ndarray, eigenvalues: np.ndarray,
            label: str) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral > 0 and
         spectral <= schur + 7.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 7.0e-9 * max(1.0, frobenius),
         label + " envelope")
    return {"schur": schur, "frobenius": frobenius, "spectral": spectral,
            "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
            "symmetry_error": symmetry,
            "spectral_over_schur": spectral / schur,
            "spectral_over_frobenius": spectral / frobenius,
            "schur_row_index": int(np.argmax(row_mass))}


def replay_row(origin: int, q0: int):
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw, geometry, weights = reverse_components(values, q0)
    full = raw / np.sqrt(geometry[:, None] * geometry[None, :])
    full_eigenvalues, full_vectors = np.linalg.eigh(full)
    full_data = metrics(full, full_eigenvalues, "full")
    lo, hi = float(full_eigenvalues[0]), float(full_eigenvalues[-1])
    index = 0 if abs(lo) >= abs(hi) else len(full_eigenvalues) - 1
    mode_name = "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue"
    vector = np.asarray(full_vectors[:, index], dtype=np.float64)
    selected = float(full_eigenvalues[index])
    residual = float(np.max(np.abs(full @ vector - selected * vector)))
    bands: dict[str, Any] = {}
    mode_by_cutoff: dict[str, Any] = {}
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    for cutoff in BAND_CUTOFFS:
        key = str(cutoff)
        mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= cutoff
        band = np.where(mask, full, 0.0)
        tail = full - band
        vals = eigenvalues_for(band, cutoff)
        bands[key] = metrics(band, vals, "band " + key)
        band_rayleigh = float(vector @ (band @ vector))
        tail_rayleigh = float(vector @ (tail @ vector))
        tail_schur = float(np.max(np.sum(np.abs(tail), axis=1)))
        tail_frobenius = float(np.sqrt(np.sum(tail * tail)))
        tail_symmetry = float(np.max(np.abs(tail - tail.T)))
        error = abs(band_rayleigh + tail_rayleigh - selected)
        need(tail_symmetry <= 1.0e-12 and math.isfinite(error) and
             error <= 5.0e-12, "Rayleigh identity")
        mode_by_cutoff[key] = {
            "band_rayleigh": band_rayleigh,
            "tail_rayleigh": tail_rayleigh,
            "band_signed_retention": band_rayleigh / selected,
            "tail_signed_fraction": tail_rayleigh / selected,
            "band_rayleigh_abs_retention": abs(band_rayleigh) / abs(selected),
            "tail_rayleigh_abs_fraction": abs(tail_rayleigh) / abs(selected),
            "rayleigh_sum_error": error,
            "tail_schur": tail_schur,
            "tail_frobenius": tail_frobenius,
            "tail_symmetry_error": tail_symmetry,
        }
    return (origin, q0, primes, geometry, weights, full_data, bands,
            mode_name, selected, residual,
            abs(float(np.dot(vector, vector)) - 1.0), mode_by_cutoff)


def expected_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell_for(4)

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
                weight = Fraction(prime, 4) ** BETA
                weighted = weight * base
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
    return {
        "interval": list(EXACT_INTERVAL), "Q": 4,
        "kernel_exponent": EXPONENT, "beta": BETA, "shell": primes,
        "matrix_symmetric": True, "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [text(value) for value in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


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
        "parent_schema": "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1",
        "parent_round2_clue": "TEST_BANDWIDTH_STABILITY",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol == {
        "origins": list(ORIGINS), "window_count": WINDOW_COUNT,
        "block_count": BLOCK_COUNT, "block_indices": list(range(8)),
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
    }, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, EXPONENT, BETA, LAW)
                for o in ORIGINS for q in Q_ANCHORS}
    need(isinstance(rows, list) and len(rows) == 9 and
         {(r.get("origin"), r.get("Q"), r.get("kernel_exponent"),
           r.get("beta"), r.get("law")) for r in rows} == expected,
         "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    jobs = [(row["origin"], row["Q"]) for row in rows]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda job: replay_row(*job), jobs))
    by_key = {(item[0], item[1]): item for item in results}
    for row in rows:
        item = by_key[(row["origin"], row["Q"])]
        (_, _, primes, geometry, weights, full_data, bands, mode_name,
         selected, residual, norm_error, mode_by_cutoff) = item
        need(row["shell"] == primes and
             row["shell_cardinality"] == len(primes), "shell")
        close(min(weights), row["weight_min"], "weight min")
        close(max(weights), row["weight_max"], "weight max")
        close(float(np.min(geometry)), row["geometry_min"], "geometry min")
        close(float(np.max(geometry)), row["geometry_max"], "geometry max")
        close(float(np.max(geometry) / np.min(geometry)),
              row["geometry_spread"], "geometry spread")
        for name, actual in full_data.items():
            if name == "schur_row_index":
                need(actual == row["full"][name], "full index")
            else:
                close(actual, row["full"][name], "full " + name)
        for cutoff in BAND_CUTOFFS:
            key = str(cutoff)
            for name, actual in bands[key].items():
                if name == "schur_row_index":
                    need(actual == row["bands"][key][name],
                         "band index " + key)
                else:
                    close(actual, row["bands"][key][name],
                          "band " + key + " " + name)
            recorded = row["mode"]["by_cutoff"][key]
            for name, actual in mode_by_cutoff[key].items():
                close(actual, recorded[name],
                      "mode " + key + " " + name)
        need(row["mode"]["mode_rule"] ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             row["mode"]["selected_mode"] == mode_name, "mode rule")
        close(selected, row["mode"]["selected_eigenvalue"],
              "selected eigenvalue")
        close(abs(selected), row["mode"]["selected_eigenvalue_abs"],
              "selected eigenvalue abs")
        close(residual, row["mode"]["eigen_residual_inf"],
              "eigen residual", 3.0e-5)
        close(norm_error, row["mode"]["full_mode_norm_error"],
              "mode norm", 3.0e-5)
        for key, value in row["band_failure_flags"].items():
            need(value is (float(row["bands"][key]["spectral"]) >
                           SPECTRAL_CAP), "row failure flag")

    phase = payload.get("phase_summary", {})
    need(phase.get("cutoffs") == list(BAND_CUTOFFS) and
         phase.get("band_definition") == "block distance <= cutoff" and
         phase.get("caps") == {"spectral": "0.64000000000000001",
                                "schur": "0.82999999999999996"},
         "phase header")
    for cutoff in BAND_CUTOFFS:
        key = str(cutoff)
        item = phase.get("by_cutoff", {}).get(key, {})
        failure_rows = [r for r in rows if r["band_failure_flags"][key]]
        schur_rows = [r for r in rows
                      if float(r["bands"][key]["schur"]) > SCHUR_CAP]
        ret = [float(r["mode"]["by_cutoff"][key]
                     ["band_rayleigh_abs_retention"]) for r in rows]
        tails = [float(r["mode"]["by_cutoff"][key]
                       ["tail_rayleigh_abs_fraction"]) for r in rows]
        expected_failures = [[r["origin"], r["count"], r["Q"],
                              r["kernel_exponent"], r["law"]]
                             for r in failure_rows]
        need(item.get("cutoff") == cutoff and item.get("rows") == 9 and
             item.get("spectral_cap_violations") == len(failure_rows) and
             item.get("schur_cap_violations") == len(schur_rows) and
             item.get("failure_keys") == expected_failures, "phase cutoff")
        close(min(ret), item["band_abs_retention_min"],
              "phase retention min")
        close(max(ret), item["band_abs_retention_max"],
              "phase retention max")
        close(max(tails), item["tail_abs_fraction_max"],
              "phase tail max")
        for q0 in Q_ANCHORS:
            qitem = phase.get("by_cutoff_q", {}).get(f"{cutoff}:{q0}", {})
            setting = [r for r in rows if r["Q"] == q0]
            need(qitem.get("cutoff") == cutoff and qitem.get("Q") == q0 and
                 qitem.get("rows") == 3 and
                 qitem.get("spectral_cap_violations") == sum(
                     r["band_failure_flags"][key] for r in setting) and
                 qitem.get("spectral_values") ==
                 [r["bands"][key]["spectral"] for r in setting],
                 "phase Q")
    first = []
    for row in rows:
        first.append(next((c for c in BAND_CUTOFFS
                           if row["band_failure_flags"][str(c)]), None))
    need(phase.get("minimal_failure_cutoff_census") == {
        str(c): first.count(c) for c in BAND_CUTOFFS},
         "minimal cutoff census")
    need(phase.get("never_failure_rows") == first.count(None),
         "never-failure census")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 9 and audit.get("origin_count") == 3 and
         audit.get("q_count") == 3 and audit.get("cutoff_count") == 4 and
         audit.get("spectral_rows") == 9 and
         audit.get("spectral_cap_violations_by_cutoff") == {
             str(c): phase["by_cutoff"][str(c)]["spectral_cap_violations"]
             for c in BAND_CUTOFFS} and
         audit.get("schur_cap_violations_by_cutoff") == {
             str(c): phase["by_cutoff"][str(c)]["schur_cap_violations"]
             for c in BAND_CUTOFFS} and
         audit.get("failure_keys_by_cutoff") == {
             str(c): phase["by_cutoff"][str(c)]["failure_keys"]
             for c in BAND_CUTOFFS} and
         audit.get("parent_failure_keys") ==
         parent["payload"]["finite_audit"]["band_failure_keys"] and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("exact_anchor") == expected_anchor(), "exact anchor")
    expected_firewall = {
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
    }
    need(payload.get("claim_firewall") == expected_firewall, "firewall")
    need(payload.get("round2_clue") == "TEST_BANDWIDTH_HOLDOUT", "clue")
    return payload


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        payload = validate(document)
        counts = payload["finite_audit"]["spectral_cap_violations_by_cutoff"]
        print("TPC375_INDEPENDENT_CHECK=PASS rows=9 failures=" + ",".join(
            str(counts[str(c)]) for c in BAND_CUTOFFS) +
              " b3_parent_match=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC375_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
