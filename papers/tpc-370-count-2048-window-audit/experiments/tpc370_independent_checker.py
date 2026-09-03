#!/usr/bin/env python3
"""Independent reverse-shell replay for the TPC-370 count-2048 audit."""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-370-count-2048-window-audit"
CERTIFICATE = PROJECT / "results/tpc370_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE = ROOT / (
    "papers/tpc-369-third-origin-family-audit/code/"
    "tpc369_third_origin_family_audit.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-369-third-origin-family-audit/results/"
    "tpc369_certificate.json")
PARENT_CODE_SHA256 = (
    "45d8895b3a5db445d6464b6d5a728373c3dc4b8a247161315b54dad7b9ae21b9")
PARENT_CERTIFICATE_SHA256 = (
    "ea6d3f8916b8ae099bfe8831f6feb765aede68b24a7df5f229226b6c931a69b6")

SCHEMA = "TPC370_COUNT_2048_WINDOW_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_COUNT_2048_WINDOW_AUDIT"
CANDIDATE_ORIGINS = tuple(1010001 + 401 * j for j in range(41))
ORIGIN_INDICES = (0, 20, 40)
ORIGINS = tuple(CANDIDATE_ORIGINS[index] for index in ORIGIN_INDICES)
COUNTS = (2048,)
Q_ANCHORS = (512, 2048, 8192)
EXPONENTS = (1,)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
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


def parent_failure_snapshot() -> tuple[list[list[Any]], list[list[Any]]]:
    raw = PARENT_CERTIFICATE.read_bytes()
    need(digest(raw) == PARENT_CERTIFICATE_SHA256,
         "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload", {})
    need(payload.get("schema") == "TPC369_THIRD_ORIGIN_FAMILY_AUDIT_V1",
         "parent schema")
    keys = payload.get("finite_audit", {}).get("replicated_failure_keys")
    need(isinstance(keys, list) and all(isinstance(key, list) and len(key) == 5
                                         for key in keys),
         "parent failure keys")
    signature = sorted([[key[0], key[2], key[3], key[4]] for key in keys])
    return keys, signature


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
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0 for i in range(len(primes))],
            dtype=np.float64),
        "mod4_character": np.asarray(
            [1.0 if p % 4 == 1 else -1.0 for p in primes],
            dtype=np.float64),
        "half_split": np.asarray(
            [1.0 if i < len(primes) / 2 else -1.0
             for i in range(len(primes))], dtype=np.float64),
    }


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
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrices, geometry, weights


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
         spectral <= schur + 3.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 3.0e-9 * max(1.0, frobenius),
         "spectral envelopes")
    return {"schur": schur, "frobenius": frobenius, "spectral": spectral,
            "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
            "symmetry_error": symmetry,
            "spectral_over_schur": spectral / schur,
            "spectral_over_frobenius": spectral / frobenius,
            "schur_row_index": int(np.argmax(row_mass))}


def close(actual: float, recorded: Any, label: str) -> None:
    target = float(recorded)
    need(abs(actual - target) <= 4.0e-6 *
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
                [text(value) for value in geometry])).hexdigest(),
        })
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
    parent_failure_keys, parent_signature = parent_failure_snapshot()
    lock = payload.get("parent_lock", {})
    need(lock.get("base_code_sha256") == BASE_SHA256 and
         lock.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         lock.get("parent_certificate_sha256") == PARENT_CERTIFICATE_SHA256 and
         lock.get("parent_schema") ==
         "TPC369_THIRD_ORIGIN_FAMILY_AUDIT_V1", "parent lock")
    origin = payload.get("origin_protocol", {})
    need(origin.get("candidate_origins") == list(CANDIDATE_ORIGINS) and
         origin.get("candidate_count") == 41 and origin.get("grid_start") == 1010001 and
         origin.get("grid_step") == 401 and
         origin.get("grid_indices") == list(ORIGIN_INDICES) and
         origin.get("selected_origins") == list(ORIGINS) and
         origin.get("response_used") is False and
         origin.get("geometry_used_for_selection") is False and
         origin.get("source_used") is False, "origin protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == list(LAWS) and protocol.get("betas") == list(BETAS) and
         protocol.get("height") == HEIGHT and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False, "protocol")
    rows = payload.get("rows")
    expected_keys = {(o, n, q, e, b, law)
                     for b in BETAS for o in ORIGINS for n in COUNTS
                     for q in Q_ANCHORS for e in EXPONENTS for law in LAWS}
    need(isinstance(rows, list) and len(rows) == 72, "row census")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows}
    need(keys == expected_keys, "row keys")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("cap_repair_betas") == [], "phase caps")
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        spectra = [float(row["normalized"]["spectral"]) for row in selected]
        schurs = [float(row["normalized"]["schur"]) for row in selected]
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 36 and
             item.get("spectral_cap_violations") == sum(
                 value > SPECTRAL_CAP for value in spectra) and
             item.get("schur_cap_violations") == sum(
                 value > SCHUR_CAP for value in schurs),
             "phase beta " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 72 and audit.get("settings_per_beta") == 36 and
         audit.get("beta_count") == 2 and audit.get("spectral_rows") == 72 and
         audit.get("beta2_rows") == 36 and
         audit.get("beta2_spectral_cap_violations") ==
         phase["by_beta"]["2"]["spectral_cap_violations"] and
         audit.get("beta2_schur_cap_violations") ==
         phase["by_beta"]["2"]["schur_cap_violations"] and
         audit.get("baseline_beta0_spectral_cap_violations") ==
         phase["by_beta"]["0"]["spectral_cap_violations"] and
         audit.get("baseline_beta0_schur_cap_violations") ==
         phase["by_beta"]["0"]["schur_cap_violations"] and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("count_min") == 2048 and audit.get("count_max") == 2048 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    actual_failure_keys = [
        [row["origin"], row["count"], row["Q"], row["kernel_exponent"],
         row["law"]]
        for row in rows if row["beta"] == 2 and
        float(row["normalized"]["spectral"]) > SPECTRAL_CAP
    ]
    actual_signature = sorted([[key[0], key[2], key[3], key[4]]
                                for key in actual_failure_keys])
    audit_parent_keys = audit.get("parent_failure_keys")
    need(audit_parent_keys == parent_failure_keys and
         audit.get("parent_failure_signature") == parent_signature and
         audit.get("replicated_failure_keys") == actual_failure_keys and
         audit.get("replicated_failure_signature") == actual_signature and
         audit.get("failure_signature_matches_parent") ==
         (actual_signature == parent_signature),
         "failure signature comparison")
    inheritance = payload.get("exact_theorem", {}).get("anchor_inheritance", {})
    need(inheritance == {
        "interval": [1010346, 1010359], "Q": 4,
        "kernel_exponent": 1,
        "source_project": "TPC-369 third predeclared origin-family audit",
    }, "anchor inheritance")
    expected_firewall = {
        "TPC370_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC370_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC370_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
        "TPC370_COUNT_2048_WINDOW": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_BETA2_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_BETA2_PARENT_SIGNATURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_ORIGIN_UNIFORMITY": "OPEN",
        "TPC370_WINDOW_UNIFORMITY": "OPEN",
        "TPC370_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC370_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC370_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC370_SOURCE_UNIFORM_L2": "OPEN",
        "TPC370_ARITHMETIC_ADVANCE": "NO",
        "TPC370_FIXED_POWER_CREDIT": 0,
        "TPC370_FULL_GATE_B": "OPEN",
        "TPC370_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall " + key)
    need(payload.get("round2_clue") ==
         "TEST_COUNT_2048_PHASE_LOCALIZATION", "clue")
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
        for beta in reversed(BETAS):
            for origin in reversed(ORIGINS):
                for count in reversed(COUNTS):
                    values = np.arange(origin, origin + count, dtype=np.int64)
                    for q0 in reversed(Q_ANCHORS):
                        for exponent in reversed(EXPONENTS):
                            primes, matrices, geometry, weights = \
                                reverse_components(values, q0, exponent, beta)
                            scale = np.sqrt(geometry[:, None] * geometry[None, :])
                            effective = (sum(x * x for x in weights) ** 2 /
                                         sum(x ** 4 for x in weights))
                            for law in reversed(LAWS):
                                key = (origin, count, q0, exponent, beta, law)
                                row = recorded[key]
                                need(row["shell"] == primes and
                                     row["shell_cardinality"] == len(primes),
                                     "shell")
                                close(min(weights), row["weight_min"], "weight min")
                                close(max(weights), row["weight_max"], "weight max")
                                close(effective, row["weight_effective_count"],
                                      "effective count")
                                close(float(effective / len(weights)),
                                      row["weight_effective_fraction"],
                                      "effective fraction")
                                close(float(np.min(geometry)), row["geometry_min"],
                                      "geometry min")
                                close(float(np.max(geometry)), row["geometry_max"],
                                      "geometry max")
                                close(float(np.max(geometry) / np.min(geometry)),
                                      row["geometry_spread"], "geometry spread")
                                for label, matrix in (
                                        ("raw", matrices[law]),
                                        ("normalized", matrices[law] / scale)):
                                    actual = metrics(matrix)
                                    target = row[label]
                                    for field in (
                                            "schur", "frobenius", "spectral",
                                            "minimum_eigenvalue",
                                            "maximum_eigenvalue", "symmetry_error",
                                            "spectral_over_schur",
                                            "spectral_over_frobenius"):
                                        close(actual[field], target[field],
                                              label + " " + field)
                                    need(actual["schur_row_index"] ==
                                         target["schur_row_index"],
                                         label + " row index")
                                if float(row["normalized"]["spectral"]) > SPECTRAL_CAP:
                                    violations[beta] += 1
                                if float(row["normalized"]["schur"]) > SCHUR_CAP:
                                    schur_violations[beta] += 1
                                checked += 1
        phase = payload["phase_summary"]["by_beta"]
        need(checked == 72 and violations == {
            beta: phase[str(beta)]["spectral_cap_violations"] for beta in BETAS
        } and schur_violations == {
            beta: phase[str(beta)]["schur_cap_violations"] for beta in BETAS
        }, "phase census")
        print("TPC370_INDEPENDENT_CHECK=PASS rows=" + str(checked) +
              " beta2_rows=" + str(sum(row["beta"] == 2
                                         for row in payload["rows"])) +
              " beta2_violations=" + str(violations[2]) +
              " baseline_beta0_violations=" + str(violations[0]))
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC370_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
