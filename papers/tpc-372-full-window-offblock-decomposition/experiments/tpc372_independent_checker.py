#!/usr/bin/env python3
"""Independent full-window replay for the TPC-372 decomposition audit."""

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
PROJECT = ROOT / "papers/tpc-372-full-window-offblock-decomposition"
CERTIFICATE = PROJECT / "results/tpc372_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-371-block-phase-localization/code/"
    "tpc371_block_phase_localization.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-371-block-phase-localization/results/tpc371_certificate.json")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "a2190210a2d43eefb1f37f81f55b2240b6b254fd4f9afa1c26cd5e0c097d8462")
PARENT_CERTIFICATE_SHA256 = (
    "01ba3b91db1f2a58b70da6b5334127f07350244f07b34772bf83dc4e69ac1ba3")

SCHEMA = "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_FULL_WINDOW_DECOMPOSITION"
ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(8))
Q_ANCHORS = (512, 2048, 8192)
EXPONENTS = (1,)
BETAS = (0, 2)
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


def parent_payload() -> dict[str, Any]:
    raw = PARENT_CERTIFICATE.read_bytes()
    need(digest(raw) == PARENT_CERTIFICATE_SHA256,
         "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload", {})
    need(payload.get("schema") ==
         "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1",
         "parent schema")
    return payload


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


def sign_patterns(primes: list[int]) -> np.ndarray:
    return np.ones(len(primes), dtype=np.float64)


def reverse_components(values: np.ndarray, q0: int, exponent: int,
                       beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    geometry = np.zeros(len(values), dtype=np.float64)
    weights = [0.0] * len(primes)
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
        matrix += signs[index] * block
    matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrix, geometry, weights


def metrics(matrix: np.ndarray) -> dict[str, float | int]:
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
         spectral <= schur + 5.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 5.0e-9 * max(1.0, frobenius),
         "spectral envelopes")
    return {"schur": schur, "frobenius": frobenius, "spectral": spectral,
            "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
            "symmetry_error": symmetry,
            "spectral_over_schur": spectral / schur,
            "spectral_over_frobenius": spectral / frobenius,
            "schur_row_index": int(np.argmax(row_mass))}


def close(actual: float, recorded: Any, label: str) -> None:
    target = float(recorded)
    need(abs(actual - target) <= 7.0e-6 *
         max(1.0, abs(actual), abs(target)), label)


def exact_anchor_expected() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell_for(4)
    anchors: list[dict[str, Any]] = []

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

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
             "exact anchor symmetry")
        need(all(value > 0 for value in geometry), "exact anchor positivity")
        anchors.append({
            "beta": beta, "interval": list(EXACT_INTERVAL), "Q": 4,
            "kernel_exponent": 1, "shell": primes,
            "matrix_symmetric": True, "geometry_positive": True,
            "matrix_digest": hashlib.sha256(canonical([
                [text(value) for value in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(value) for value in geometry])).hexdigest()})
    return {"anchors": anchors}


def validate_header(document: dict[str, Any]) -> dict[str, Any]:
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
    parent = parent_payload()
    lock = payload.get("parent_lock", {})
    need(lock.get("base_code_sha256") == BASE_SHA256 and
         lock.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         lock.get("parent_certificate_sha256") == PARENT_CERTIFICATE_SHA256 and
         lock.get("parent_schema") ==
         "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1", "parent lock")
    need(lock.get("parent_block_phase") ==
         parent.get("finite_audit", {}).get("beta2_all_declared_blocks_pass"),
         "parent phase lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("window_count") == WINDOW_COUNT and
         protocol.get("block_count") == BLOCK_COUNT and
         protocol.get("block_indices") == list(BLOCK_INDICES) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == ["all_plus"] and
         protocol.get("betas") == list(BETAS) and protocol.get("height") == HEIGHT and
         protocol.get("common_normalization") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("component_selection_used") is False, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, beta, "all_plus")
                for beta in BETAS for o in ORIGINS for q in Q_ANCHORS}
    need(isinstance(rows, list) and len(rows) == 18 and
         {(row.get("origin"), row.get("Q"), row.get("kernel_exponent"),
           row.get("beta"), row.get("law")) for row in rows} == expected,
         "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("cap_repair_betas") == [], "phase caps")
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 9 and
             item.get("full_spectral_cap_violations") == sum(
                 float(row["full"]["spectral"]) > SPECTRAL_CAP
                 for row in selected) and
             item.get("full_schur_cap_violations") == sum(
                 float(row["full"]["schur"]) > SCHUR_CAP
                 for row in selected) and
             item.get("block_diagonal_spectral_cap_violations") == sum(
                 float(row["block_diagonal"]["spectral"]) > SPECTRAL_CAP
                 for row in selected) and
             item.get("off_block_spectral_cap_violations") == sum(
                 float(row["off_block"]["spectral"]) > SPECTRAL_CAP
                 for row in selected), "phase beta")
        for q0 in Q_ANCHORS:
            setting = [row for row in selected if row["Q"] == q0]
            qitem = phase.get("by_beta_q", {}).get(f"{beta}:{q0}", {})
            need(qitem.get("rows") == 3 and
                 qitem.get("full_spectral_cap_violations") == sum(
                     float(row["full"]["spectral"]) > SPECTRAL_CAP
                     for row in setting) and
                 qitem.get("block_diagonal_spectral_cap_violations") == sum(
                     float(row["block_diagonal"]["spectral"]) > SPECTRAL_CAP
                     for row in setting) and
                 qitem.get("off_block_spectral_cap_violations") == sum(
                     float(row["off_block"]["spectral"]) > SPECTRAL_CAP
                     for row in setting), "phase q")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("beta2_rows") == 9 and
         audit.get("baseline_beta0_rows") == 9 and
         audit.get("origin_count") == 3 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 18 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    for beta, prefix in ((2, "beta2"), (0, "baseline_beta0")):
        item = phase["by_beta"][str(beta)]
        need(audit.get(prefix + "_full_spectral_cap_violations") ==
             item["full_spectral_cap_violations"] and
             audit.get(prefix + "_full_schur_cap_violations") ==
             item["full_schur_cap_violations"], "audit phase")
    actual_full = [[row["origin"], row["count"], row["Q"],
                    row["kernel_exponent"], row["law"]]
                   for row in rows if row["beta"] == 2 and
                   float(row["full"]["spectral"]) > SPECTRAL_CAP]
    actual_diag = [[row["origin"], row["Q"]] for row in rows
                   if row["beta"] == 2 and
                   float(row["block_diagonal"]["spectral"]) > SPECTRAL_CAP]
    actual_required = [[row["origin"], row["Q"]] for row in rows
                       if row["beta"] == 2 and
                       float(row["full"]["spectral"]) > SPECTRAL_CAP and
                       float(row["block_diagonal"]["spectral"]) <= SPECTRAL_CAP]
    need(audit.get("full_failure_keys") == actual_full and
         audit.get("block_diagonal_beta2_failure_keys") == actual_diag and
         audit.get("required_off_block_keys") == actual_required and
         float(audit.get("decomposition_max_error")) <= 1.0e-15,
         "decomposition census")
    need(payload.get("exact_theorem", {}).get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-371 block-local phase localization",
    }, "anchor inheritance")
    expected_firewall = {
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
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall " + key)
    need(payload.get("round2_clue") == "TEST_EIGENMODE_BLOCK_SEPARATION",
         "clue")
    return payload


def check_setting(job: tuple[int, int, int], recorded: dict) -> tuple[int, int]:
    beta, origin, q0 = job
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw, geometry, weights = reverse_components(
        values, q0, 1, beta)
    scale = np.sqrt(geometry[:, None] * geometry[None, :])
    full = raw / scale
    diagonal = np.zeros_like(full)
    for block_index in BLOCK_INDICES:
        lo = block_index * BLOCK_COUNT
        hi = lo + BLOCK_COUNT
        diagonal[lo:hi, lo:hi] = full[lo:hi, lo:hi]
    off = full - diagonal
    key = (origin, q0, 1, beta, "all_plus")
    row = recorded[key]
    need(row["shell"] == primes and row["shell_cardinality"] == len(primes),
         "shell")
    close(min(weights), row["weight_min"], "weight min")
    close(max(weights), row["weight_max"], "weight max")
    effective = sum(x * x for x in weights) ** 2 / sum(x ** 4 for x in weights)
    close(effective, row["weight_effective_count"], "effective count")
    close(float(np.min(geometry)), row["geometry_min"], "geometry min")
    close(float(np.max(geometry)), row["geometry_max"], "geometry max")
    close(float(np.max(geometry) / np.min(geometry)), row["geometry_spread"],
          "geometry spread")
    computed = {}
    for label, matrix in (("full", full), ("block_diagonal", diagonal),
                          ("off_block", off)):
        actual = metrics(matrix)
        computed[label] = actual
        target = row[label]
        for field in ("schur", "frobenius", "spectral", "minimum_eigenvalue",
                      "maximum_eigenvalue", "symmetry_error",
                      "spectral_over_schur", "spectral_over_frobenius"):
            close(actual[field], target[field], label + " " + field)
        need(actual["schur_row_index"] == target["schur_row_index"],
             label + " row index")
    error = float(np.max(np.abs(full - diagonal - off)))
    close(error, row["decomposition_error"], "decomposition error")
    close(float(computed["full"]["spectral"] -
               computed["block_diagonal"]["spectral"]),
          row["lower_bound_off_spectral"], "lower bound")
    close(float(computed["off_block"]["spectral"] -
               computed["full"]["spectral"] +
               computed["block_diagonal"]["spectral"]),
          row["off_minus_lower_bound"], "off remainder")
    return (int(float(row["full"]["spectral"]) > SPECTRAL_CAP),
            int(float(row["full"]["schur"]) > SCHUR_CAP))


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        payload = validate_header(document)
        need(payload.get("exact_anchor") == exact_anchor_expected(),
             "exact anchor")
        recorded = {(row["origin"], row["Q"], row["kernel_exponent"],
                     row["beta"], row["law"]): row for row in payload["rows"]}
        jobs = [(beta, origin, q0) for beta in BETAS for origin in ORIGINS
                for q0 in Q_ANCHORS]
        with ThreadPoolExecutor(max_workers=4) as pool:
            checked = list(pool.map(lambda job: check_setting(job, recorded),
                                    jobs))
        spectral = {beta: 0 for beta in BETAS}
        schur = {beta: 0 for beta in BETAS}
        for job, result in zip(jobs, checked):
            spectral[job[0]] += result[0]
            schur[job[0]] += result[1]
        phase = payload["phase_summary"]["by_beta"]
        need(len(checked) == 18 and spectral == {
            beta: phase[str(beta)]["full_spectral_cap_violations"]
            for beta in BETAS} and schur == {
            beta: phase[str(beta)]["full_schur_cap_violations"]
            for beta in BETAS}, "phase census")
        audit = payload["finite_audit"]
        print("TPC372_INDEPENDENT_CHECK=PASS rows=18 beta2_rows=9 "
              "beta2_violations=" +
              str(audit["beta2_full_spectral_cap_violations"]) +
              " diagonal_beta2_violations=" +
              str(audit["beta2_block_diagonal_spectral_cap_violations"]))
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC372_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
