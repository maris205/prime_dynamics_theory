#!/usr/bin/env python3
"""Independent reverse-order replay for the TPC-366 certificate."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-366-beta2-higher-q-ladder"
CERTIFICATE = PROJECT / "results/tpc366_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")

SCHEMA = "TPC366_BETA2_HIGHER_Q_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BETA2_HIGHER_Q_LADDER"
CANDIDATE_ORIGINS = tuple(620001 + 307 * j for j in range(41))
PILOT_COUNT = 256
ORIGINS = (623071, 631360, 629211)
COUNTS = (256, 512)
Q_ANCHORS = (512, 1024, 2048, 4096, 8192)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
BETAS = (0, 2)
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
MIN_SEPARATION = 2048
SELECTION_BETA = 2
EXACT_INTERVAL = (623372, 623385)


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


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(50_000)


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if index % 2 == 0 else -1.0
             for index in range(len(primes))], dtype=np.float64),
        "mod4_character": np.asarray(
            [1.0 if prime % 4 == 1 else -1.0
             for prime in primes], dtype=np.float64),
        "half_split": np.asarray(
            [1.0 if index < len(primes) / 2 else -1.0
             for index in range(len(primes))], dtype=np.float64),
    }


def reverse_geometry(values: np.ndarray, q0: int, exponent: int,
                     beta: int) -> np.ndarray:
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    geometry = np.zeros(len(values), dtype=np.float64)
    for prime in reversed(shell_for(q0)):
        weight = (float(prime) / float(q0)) ** beta
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "selection geometry")
    return geometry


def reproduce_selection() -> list[int]:
    records: list[tuple[float, int]] = []
    for origin in CANDIDATE_ORIGINS:
        values = np.arange(origin, origin + PILOT_COUNT, dtype=np.int64)
        spreads: list[float] = []
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                geometry = reverse_geometry(values, q0, exponent,
                                            SELECTION_BETA)
                spreads.append(float(np.max(geometry) / np.min(geometry)))
        records.append((max(spreads), origin))
    ranked = sorted(records, key=lambda item: (-item[0], item[1]))
    chosen: list[int] = []
    for score, origin in ranked:
        del score
        if all(abs(origin - old) >= MIN_SEPARATION for old in chosen):
            chosen.append(origin)
        if len(chosen) == len(ORIGINS):
            break
    need(tuple(chosen) == ORIGINS, "selection result")
    return chosen


def reverse_components(values: np.ndarray, q0: int, exponent: int,
                       beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = [0.0] * len(primes)
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
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry")
    return primes, matrices, geometry, weights


def metrics(matrix: np.ndarray) -> dict[str, float | int]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "metrics")
    eigenvalues = np.linalg.eigvalsh(matrix)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(spectral) and spectral > 0.0 and
         spectral <= schur + 3.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 3.0e-9 * max(1.0, frobenius),
         "spectral envelopes")
    return {
        "schur": schur, "frobenius": frobenius, "spectral": spectral,
        "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
        "symmetry_error": symmetry,
        "spectral_over_schur": spectral / schur,
        "spectral_over_frobenius": spectral / frobenius,
        "schur_row_index": int(np.argmax(row_mass)),
    }


def close(actual: float, recorded: Any, label: str) -> None:
    target = float(recorded)
    need(abs(float(actual) - target) <= 4.0e-6 *
         max(1.0, abs(float(actual)), abs(target)), label)


def exact_anchor_expected() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell_for(4)
    text = lambda value: f"{value.numerator}/{value.denominator}"
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
                        base = (Fraction(int((u - t) % prime == 0), 1) -
                                Fraction(1, prime - 1))
                        base *= Fraction(prime * HEIGHT * HEIGHT,
                                          HEIGHT * HEIGHT + (u - t) ** 2)
                    weighted = Fraction(prime, 4) ** beta * base
                    total += weighted
                    energy += weighted * weighted
                row.append(total)
                grow += energy
            matrix.append(row)
            geometry.append(grow)
        need(all(matrix[i][j] == matrix[j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "exact symmetry")
        need(all(value > 0 for value in geometry), "exact positivity")
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


def validate_header(document: dict[str, Any]) -> dict[str, Any]:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == list(LAWS) and
         protocol.get("betas") == list(BETAS) and
         protocol.get("selection_beta") == SELECTION_BETA and
         protocol.get("pilot_count") == PILOT_COUNT and
         protocol.get("minimum_separation") == MIN_SEPARATION and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("selection_response_blind") is True, "protocol")
    need(digest(BASE_CODE.read_bytes()) == BASE_SHA256, "base provenance")
    selection = payload.get("selection", {})
    need(selection.get("candidate_origins") == list(CANDIDATE_ORIGINS) and
         selection.get("candidate_count") == len(CANDIDATE_ORIGINS) and
         selection.get("selected_origins") == list(ORIGINS) and
         selection.get("selection_beta") == SELECTION_BETA and
         selection.get("pilot_count") == PILOT_COUNT and
         selection.get("minimum_separation") == MIN_SEPARATION, "selection")
    need(reproduce_selection() == list(ORIGINS), "independent selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 480, "rows")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows}
    need(len(keys) == 480, "row keys")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [2], "repair beta")
    for beta, violations, schur_violations in ((0, 60, 60), (2, 0, 0)):
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 240 and
             item.get("spectral_cap_violations") == violations and
             item.get("schur_cap_violations") == schur_violations,
             "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 480 and
         audit.get("settings_per_beta") == 240 and
         audit.get("beta_count") == 2 and
         audit.get("spectral_rows") == 480 and
         audit.get("beta2_rows") == 240 and
         audit.get("beta2_cap_violations") == 0 and
         audit.get("beta2_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_cap_violations") == 60 and
         audit.get("baseline_beta0_schur_cap_violations") == 60 and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    firewall = payload.get("claim_firewall", {})
    expected_firewall = {
        "TPC366_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC366_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC366_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_480_ROWS",
        "TPC366_HIGHER_Q_LADDER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC366_BETA2_HIGHER_Q_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC366_BETA2_SCALE_UNIFORMITY": "OPEN",
        "TPC366_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC366_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC366_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC366_SOURCE_UNIFORM_L2": "OPEN",
        "TPC366_ARITHMETIC_ADVANCE": "NO",
        "TPC366_FIXED_POWER_CREDIT": 0,
        "TPC366_FULL_GATE_B": "OPEN", "TPC366_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall " + key)
    return payload


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
        recorded = {(row["origin"], row["count"], row["Q"],
                     row["kernel_exponent"], row["beta"], row["law"]): row
                    for row in payload["rows"]}
        checked = 0
        violations = {beta: 0 for beta in BETAS}
        schur_violations = {beta: 0 for beta in BETAS}
        for beta in BETAS:
            for origin in ORIGINS:
                for count in COUNTS:
                    values = np.arange(origin, origin + count,
                                       dtype=np.int64)
                    for q0 in Q_ANCHORS:
                        for exponent in EXPONENTS:
                            primes, matrices, geometry, weights = \
                                reverse_components(values, q0, exponent, beta)
                            scale = np.sqrt(geometry[:, None] * geometry[None, :])
                            for law in LAWS:
                                key = (origin, count, q0, exponent, beta, law)
                                row = recorded[key]
                                need(row["shell"] == primes and
                                     row["shell_cardinality"] == len(primes),
                                     "shell")
                                close(min(weights), row["weight_min"],
                                      "weight min")
                                close(max(weights), row["weight_max"],
                                      "weight max")
                                effective = (sum(x * x for x in weights) ** 2 /
                                             sum(x ** 4 for x in weights))
                                close(effective, row["weight_effective_count"],
                                      "effective count")
                                close(float(np.min(geometry)), row["geometry_min"],
                                      "geometry min")
                                close(float(np.max(geometry)), row["geometry_max"],
                                      "geometry max")
                                matrix = matrices[law]
                                normalized = matrix / scale
                                for label, actual in (
                                        ("raw", metrics(matrix)),
                                        ("normalized", metrics(normalized))):
                                    target = row[label]
                                    for field in (
                                            "schur", "frobenius", "spectral",
                                            "minimum_eigenvalue",
                                            "maximum_eigenvalue",
                                            "spectral_over_schur",
                                            "spectral_over_frobenius"):
                                        close(actual[field], target[field],
                                              label + " " + field)
                                    need(actual["schur_row_index"] ==
                                         target["schur_row_index"],
                                         label + " row index")
                                if float(row["normalized"]["spectral"]) > \
                                        SPECTRAL_CAP:
                                    violations[beta] += 1
                                if float(row["normalized"]["schur"]) > SCHUR_CAP:
                                    schur_violations[beta] += 1
                                checked += 1
        need(checked == 480 and violations == {0: 60, 2: 0} and
             schur_violations == {0: 60, 2: 0}, "phase census")
        print("TPC366_INDEPENDENT_CHECK=PASS rows=480 beta2_rows=240 "
              "beta2_violations=0 baseline_beta0_violations=60")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC366_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
