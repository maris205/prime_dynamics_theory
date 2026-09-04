#!/usr/bin/env python3
"""Independent reverse-shell replay for the TPC-379 law-control panel.

The checker deliberately does not import the TPC-379 producer.  It rebuilds
the prime shell, four sign vectors, common geometry, normalized matrices, and
the c=1 band directly from integer coordinates before comparing the sealed
certificate.
"""

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
PROJECT = ROOT / "papers/tpc-379-c1-crossholdout-law-control"
CERTIFICATE = PROJECT / "results/tpc379_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-378-c1-scale-origin-crossholdout/code/"
    "tpc378_c1_scale_origin_crossholdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-378-c1-scale-origin-crossholdout/results/"
    "tpc378_certificate.json")

PARENT_CODE_SHA256 = (
    "dd9289a390a1c52b9d22cd19766e4b2c5def87b6fa3c6eda530e4a81081997fa")
PARENT_CERT_SHA256 = (
    "4846b4cfd0bfb75b9eebb95fcdfb33dc0365c3aba0b7080278be2be96df540d1")

SCHEMA = "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL"
ORIGINS = (1200001, 1208021, 1216041)
WINDOW_COUNT = 1024
BLOCK_LENGTH = 256
BLOCK_COUNT = 4
BAND_CUTOFF = 1
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1200001, 1200014)
EXACT_Q = 8


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


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and finite_tree(item)
                   for key, item in value.items())
    if isinstance(value, list):
        return all(finite_tree(item) for item in value)
    return True


def parse_no_duplicates(raw: bytes) -> dict[str, Any]:
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise Failure("duplicate JSON key")
            result[key] = value
        return result
    value = json.loads(raw, object_pairs_hook=hook)
    need(isinstance(value, dict), "document object")
    return value


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 4.0e-9) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(target) and math.isfinite(actual) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual),
                                                  abs(target)),
         label + " mismatch")


def sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = b"\x00" * (
                ((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


PRIMES = sieve(20000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0
             for i in range(len(primes))], dtype=np.float64),
        "mod4_character": np.asarray(
            [1.0 if p % 4 == 1 else -1.0 for p in primes],
            dtype=np.float64),
        "half_split": np.asarray(
             [1.0 if i < len(primes) / 2 else -1.0
             for i in range(len(primes))], dtype=np.float64),
    }


def metric(matrix: np.ndarray, eigenvalues: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 2.0e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 3.0e-8 and
         spectral <= frobenius + 3.0e-8, "metric envelope")
    return {"schur": schur, "frobenius": frobenius,
            "spectral": spectral, "minimum_eigenvalue": lo,
            "maximum_eigenvalue": hi, "symmetry_error": symmetry,
            "spectral_over_schur": spectral / schur,
            "spectral_over_frobenius": spectral / frobenius,
            "schur_row_index": int(np.argmax(mass))}


def replay(origin: int, q0: int) -> list[dict[str, Any]]:
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    kernel = float(HEIGHT * HEIGHT) / (
        HEIGHT * HEIGHT + difference.astype(np.float64) ** 2)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    signs = sign_patterns(primes)
    matrices = {law: np.zeros((WINDOW_COUNT, WINDOW_COUNT), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(WINDOW_COUNT, dtype=np.float64)
    weights: list[float] = []
    # Reverse shell order is intentional: it is independent of the producer's
    # ascending accumulation order while representing the same finite sum.
    for prime in reversed(primes):
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
        for law in LAWS:
            matrices[law] += signs[law][primes.index(prime)] * block
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry")
    blocks = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_LENGTH
    mask = np.abs(blocks[:, None] - blocks[None, :]) <= BAND_CUTOFF
    output = []
    for law in LAWS:
        full = matrices[law] / np.sqrt(geometry[:, None] * geometry[None, :])
        values_full, vectors = np.linalg.eigh(full)
        full_data = metric(full, values_full)
        index = 0 if abs(values_full[0]) >= abs(values_full[-1]) else -1
        vector = np.asarray(vectors[:, index], dtype=np.float64)
        selected = float(values_full[index])
        band = np.where(mask, full, 0.0)
        tail = full - band
        band_values = np.linalg.eigvalsh(band)
        band_data = metric(band, band_values)
        residual = float(np.max(np.abs(full @ vector - selected * vector)))
        norm_error = abs(float(np.dot(vector, vector)) - 1.0)
        band_rayleigh = float(vector @ (band @ vector))
        tail_rayleigh = float(vector @ (tail @ vector))
        rayleigh_error = abs(band_rayleigh + tail_rayleigh - selected)
        need(residual <= 2.0e-8 and norm_error <= 2.0e-10 and
             rayleigh_error <= 4.0e-10 and
             float(np.max(np.abs(tail - tail.T))) <= 3.0e-12,
             "eigen/rayleigh")
        output.append({
            "origin": origin, "Q": q0, "law": law,
            "full": full_data, "band": band_data,
            "tail": {"frobenius": float(np.sqrt(np.sum(tail * tail))),
                     "schur": float(np.max(np.sum(np.abs(tail), axis=1))),
                     "symmetry_error": float(np.max(np.abs(tail - tail.T)))},
            "geometry_min": float(np.min(geometry)),
            "geometry_max": float(np.max(geometry)),
            "geometry_spread": float(np.max(geometry) / np.min(geometry)),
            "weight_min": min(weights), "weight_max": max(weights),
            "selected_mode": "minimum_eigenvalue" if index == 0
            else "maximum_eigenvalue",
            "selected_eigenvalue": selected,
            "selected_eigenvalue_abs": abs(selected),
            "residual": residual, "norm_error": norm_error,
            "band_rayleigh": band_rayleigh,
            "tail_rayleigh": tail_rayleigh,
            "rayleigh_error": rayleigh_error,
            "band_signed_retention": band_rayleigh / selected,
            "band_retention": abs(band_rayleigh) / abs(selected),
            "tail_signed_fraction": tail_rayleigh / selected,
            "tail_fraction": abs(tail_rayleigh) / abs(selected),
            "full_failure": full_data["spectral"] > SPECTRAL_CAP,
            "band_failure": band_data["spectral"] > SPECTRAL_CAP,
            "schur_failure": band_data["schur"] > SCHUR_CAP,
        })
    return output


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell(EXACT_Q)
    signs = sign_patterns(primes)

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    matrices = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        rows = {law: [] for law in LAWS}
        grow = Fraction(0)
        for t in values:
            components = []
            for prime in primes:
                if u == t or u % prime == 0 or t % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(prime, EXACT_Q) ** BETA *
                            Fraction(HEIGHT * HEIGHT,
                                     HEIGHT * HEIGHT + (u - t) ** 2) *
                            centered)
                components.append(base)
            grow += sum(value * value for value in components)
            for index, law in enumerate(LAWS):
                rows[law].append(sum(
                    Fraction(int(signs[law][j])) * value
                    for j, value in enumerate(components)))
        geometry.append(grow)
        for law in LAWS:
            matrices[law].append(rows[law])
    need(all(value > 0 for value in geometry), "anchor positivity")
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "shell": primes, "laws": list(LAWS),
        "matrix_symmetric_by_law": {law: True for law in LAWS},
        "law_matrix_digests": {
            law: hashlib.sha256(canonical([
                [text(value) for value in row] for row in matrices[law]
            ])).hexdigest() for law in LAWS},
        "geometry_positive": True,
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    need(finite_tree(document), "nonfinite JSON value")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code lock")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate lock")
    need(payload.get("parent_lock") == {
        "parent_code_sha256": PARENT_CODE_SHA256,
        "parent_certificate_sha256": PARENT_CERT_SHA256,
        "parent_schema": "TPC378_C1_SCALE_ORIGIN_CROSSHOLDOUT_V1",
        "parent_round2_clue": "TEST_C1_CROSSHOLDOUT_LAW_CONTROL",
        "parent_profile": [0, 3, 3],
    }, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1200001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1200001 + 401 * i for i in range(41)] and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == list(ORIGINS) and
         selection.get("window_count") == WINDOW_COUNT and
         selection.get("block_length") == BLOCK_LENGTH and
         selection.get("block_count") == BLOCK_COUNT and
         selection.get("q_anchors") == list(Q_ANCHORS) and
         selection.get("laws") == list(LAWS) and
         selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("window_count") == WINDOW_COUNT and
         protocol.get("block_length") == BLOCK_LENGTH and
         protocol.get("block_count") == BLOCK_COUNT and
         protocol.get("band_cutoff") == BAND_CUTOFF and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == [EXPONENT] and
         protocol.get("laws") == list(LAWS) and
         protocol.get("betas") == [BETA] and protocol.get("height") == HEIGHT
         and protocol.get("common_geometry") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("law_selection_used") is False and
         protocol.get("row_selection_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    expected_profile = {
        "all_plus": [0, 3, 3], "alternating_index": [0, 0, 0],
        "mod4_character": [0, 0, 0], "half_split": [0, 0, 0]}
    need(audit.get("rows") == 36 and audit.get("origin_count") == 3 and
         audit.get("q_count") == 3 and audit.get("law_count") == 4 and
         audit.get("spectral_rows") == 36 and
         audit.get("spectral_cap_violations") == 6 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_law_Q") == expected_profile and
         audit.get("all_plus_failure_profile") == [0, 3, 3] and
         audit.get("signed_control_failure_profiles") == {
             law: [0, 0, 0] for law in LAWS if law != "all_plus"} and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("law_control_complete") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 36 and phase.get("laws") == list(LAWS) and
         phase.get("law_count") == 4 and
         phase.get("band_cutoff") == 1 and
         phase.get("failure_profile_by_law_Q") == expected_profile and
         phase.get("spectral_cap_violations") == 6 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("signed_controls_all_below_spectral_cap") is True,
         "phase")
    rows = payload.get("rows", [])
    need(isinstance(rows, list) and len(rows) == 36, "rows")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    expected_keys = {(origin, q0, law) for origin in ORIGINS
                     for q0 in Q_ANCHORS for law in LAWS}
    need({(row.get("origin"), row.get("Q"), row.get("law"))
          for row in rows} == expected_keys, "row keys")
    for row in rows:
        need(row.get("count") == WINDOW_COUNT and
             row.get("block_length") == BLOCK_LENGTH and
             row.get("block_count") == BLOCK_COUNT and
             row.get("kernel_exponent") == EXPONENT and
             row.get("beta") == BETA and row.get("height") == HEIGHT and
             row.get("law") in LAWS and
             row.get("band_failure") in (True, False) and
             row.get("schur_failure") in (True, False), "row header")
    anchor = exact_anchor()
    need(payload.get("exact_anchor") == anchor, "exact anchor")


def compare(document: dict[str, Any]) -> None:
    rows = {(row["origin"], row["Q"], row["law"]): row
            for row in document["payload"]["rows"]}
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for result in replay(origin, q0):
                key = (origin, q0, result["law"])
                row = rows[key]
                for part in ("full", "band"):
                    for field in ("schur", "frobenius", "spectral",
                                  "minimum_eigenvalue",
                                  "maximum_eigenvalue", "symmetry_error",
                                  "spectral_over_schur",
                                  "spectral_over_frobenius"):
                        close(result[part][field], row[part][field],
                              f"{key} {part}.{field}")
                for field in ("geometry_min", "geometry_max",
                              "geometry_spread", "weight_min", "weight_max"):
                    close(result[field], row[field], f"{key} {field}")
                close(result["tail"]["frobenius"], row["tail"]["frobenius"],
                      f"{key} tail.frobenius")
                close(result["tail"]["schur"], row["tail"]["schur"],
                      f"{key} tail.schur")
                close(result["tail"]["symmetry_error"],
                      row["tail"]["symmetry_error"],
                      f"{key} tail.symmetry_error")
                mode = row["mode"]
                for field in ("selected_eigenvalue", "selected_eigenvalue_abs",
                              "eigen_residual_inf", "full_mode_norm_error",
                              "band_rayleigh", "tail_rayleigh",
                              "rayleigh_sum_error", "band_signed_retention",
                              "band_rayleigh_abs_retention",
                              "tail_signed_fraction",
                              "tail_rayleigh_abs_fraction"):
                    close(result[{
                        "eigen_residual_inf": "residual",
                        "full_mode_norm_error": "norm_error",
                        "rayleigh_sum_error": "rayleigh_error",
                        "band_rayleigh_abs_retention": "band_retention",
                        "tail_rayleigh_abs_fraction": "tail_fraction",
                    }.get(field, field)], mode[field], f"{key} mode.{field}")
                need(result["selected_mode"] == mode["selected_mode"],
                     f"{key} mode choice")
                need(result["full_failure"] == row["full_failure"] and
                     result["band_failure"] == row["band_failure"] and
                     result["schur_failure"] == row["schur_failure"],
                     f"{key} flags")


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        raw = CERTIFICATE.read_bytes()
        document = parse_no_duplicates(raw)
        need(raw == canonical(document), "certificate canonicality")
        validate(document)
        compare(document)
        profile = document["payload"]["finite_audit"][
            "failure_profile_by_law_Q"]
        compact = ";".join(
            law + ":" + ",".join(str(x) for x in profile[law])
            for law in LAWS)
        print("TPC379_INDEPENDENT_CHECK=PASS rows=36 failures=6 "
              "profiles=" + compact)
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC379_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
