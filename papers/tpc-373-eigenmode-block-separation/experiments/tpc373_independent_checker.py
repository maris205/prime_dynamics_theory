#!/usr/bin/env python3
"""Independent reverse-shell replay for the TPC-373 eigenmode audit."""

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
PROJECT = ROOT / "papers/tpc-373-eigenmode-block-separation"
CERTIFICATE = PROJECT / "results/tpc373_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-372-full-window-offblock-decomposition/code/"
    "tpc372_full_window_offblock_decomposition.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-372-full-window-offblock-decomposition/results/"
    "tpc372_certificate.json")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "deff2866697eb308112fe516fe5313bcac766624d13ffdbb2fad534afbdbf563")
PARENT_CERTIFICATE_SHA256 = (
    "ecbaa0f8f1549bcd565135f70f3e36ee0edda36719f69a14d95ca77c1509e257")

SCHEMA = "TPC373_EIGENMODE_BLOCK_SEPARATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_EIGENMODE_BLOCK_SEPARATION"
ORIGINS = (1010001, 1018021, 1026041)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(8))
Q_ANCHORS = (512, 2048, 8192)
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


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 8.0e-6) -> None:
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


def sign_patterns(primes: list[int]) -> np.ndarray:
    return np.ones(len(primes), dtype=np.float64)


def reverse_components(values: np.ndarray, q0: int, beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = float(HEIGHT * HEIGHT) / (HEIGHT * HEIGHT +
                                         distance * distance)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    geometry = np.zeros(len(values), dtype=np.float64)
    weights = [0.0] * len(primes)
    # Descending shell order is deliberately different from the producer.
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


def eigendata(matrix: np.ndarray) -> dict[str, Any]:
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(schur) and schur > 0 and
         math.isfinite(frobenius) and frobenius > 0 and
         math.isfinite(spectral) and spectral > 0 and
         spectral <= schur + 5.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 5.0e-9 * max(1.0, frobenius),
         "spectral envelopes")
    if abs(lo) >= abs(hi):
        index = 0
        mode = "minimum_eigenvalue"
    else:
        index = len(eigenvalues) - 1
        mode = "maximum_eigenvalue"
    vector = np.asarray(eigenvectors[:, index], dtype=np.float64)
    selected = float(eigenvalues[index])
    norm_error = abs(float(np.dot(vector, vector)) - 1.0)
    residual = float(np.max(np.abs(matrix @ vector - selected * vector)))
    need(norm_error <= 3.0e-10 and residual <= 5.0e-8,
         "eigenvector residual")
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    terms: list[float] = []
    layer_sum = np.zeros_like(matrix)
    for distance in BLOCK_INDICES:
        mask = (np.abs(block_ids[:, None] - block_ids[None, :]) == distance)
        layer = np.where(mask, matrix, 0.0)
        layer_sum += layer
        terms.append(float(vector @ (layer @ vector)))
    reconstruction = float(np.max(np.abs(matrix - layer_sum)))
    rayleigh_error = abs(sum(terms) - selected)
    need(reconstruction <= 3.0e-14 and rayleigh_error <= 3.0e-10,
         "layer identities")
    mass = float(sum(abs(term) for term in terms))
    need(math.isfinite(mass) and mass > 0, "layer mass")
    cumulative = 0.0
    layers: list[dict[str, Any]] = []
    for distance, term in zip(BLOCK_INDICES, terms):
        absolute = abs(term)
        cumulative += absolute
        layers.append({
            "block_distance": distance,
            "rayleigh": term,
            "abs_rayleigh": absolute,
            "signed_fraction": term / selected,
            "abs_fraction": absolute / mass,
            "cumulative_abs_fraction": cumulative / mass,
        })
    return {
        "schur": schur, "frobenius": frobenius, "spectral": spectral,
        "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
        "symmetry_error": float(np.max(np.abs(matrix - matrix.T))),
        "spectral_over_schur": spectral / schur,
        "spectral_over_frobenius": spectral / frobenius,
        "schur_row_index": int(np.argmax(row_mass)),
        "mode": mode, "selected": selected,
        "norm_error": norm_error, "residual": residual,
        "terms": terms, "layers": layers,
        "reconstruction": reconstruction, "rayleigh_error": rayleigh_error,
        "mass": mass,
        "same_fraction": terms[0] / selected,
        "cross_fraction": sum(terms[1:]) / selected,
        "cross_abs_fraction": sum(abs(x) for x in terms[1:]) / mass,
        "far_abs_fraction": sum(abs(x) for x in terms[4:]) / mass,
        "dominant_distance": int(
            BLOCK_INDICES[int(np.argmax(np.abs(np.asarray(terms))))]),
    }


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
    parent_payload = parent["payload"]
    lock = payload.get("parent_lock", {})
    need(lock == {
        "base_code_sha256": BASE_SHA256,
        "parent_code_sha256": PARENT_CODE_SHA256,
        "parent_certificate_sha256": PARENT_CERTIFICATE_SHA256,
        "parent_schema": "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1",
        "parent_round2_clue": "TEST_EIGENMODE_BLOCK_SEPARATION",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("window_count") == WINDOW_COUNT and
         protocol.get("block_count") == BLOCK_COUNT and
         protocol.get("block_indices") == list(BLOCK_INDICES) and
         protocol.get("partition") == "fixed eight contiguous 256-point blocks" and
         protocol.get("layer_definition") == "absolute block-index distance 0..7" and
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
         {(row.get("origin"), row.get("Q"), row.get("kernel_exponent"),
           row.get("beta"), row.get("law")) for row in rows} == expected,
         "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    parent_failures = parent_payload["finite_audit"]["full_failure_keys"]
    jobs = [(row["beta"], row["origin"], row["Q"]) for row in rows]

    def replay(job):
        beta, origin, q0 = job
        values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
        primes, matrix, geometry, weights = reverse_components(values, q0, beta)
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
        return job, primes, geometry, weights, normalized, eigendata(normalized)

    with ThreadPoolExecutor(max_workers=4) as pool:
        replays = list(pool.map(replay, jobs))
    by_key = {(job[1], job[2], job[0]): (primes, geometry, weights, matrix, data)
              for job, primes, geometry, weights, matrix, data in replays}
    for row in rows:
        key = (row["origin"], row["Q"], row["beta"])
        primes, geometry, weights, matrix, data = by_key[key]
        need(row["shell"] == primes and
             row["shell_cardinality"] == len(primes), "shell " + str(key))
        close(min(weights), row["weight_min"], "weight min")
        close(max(weights), row["weight_max"], "weight max")
        effective = float(np.sum(np.asarray(weights) ** 2) ** 2 /
                          np.sum(np.asarray(weights) ** 4))
        close(effective, row["weight_effective_count"], "weight effective")
        close(float(np.min(geometry)), row["geometry_min"], "geometry min")
        close(float(np.max(geometry)), row["geometry_max"], "geometry max")
        close(float(np.max(geometry) / np.min(geometry)),
              row["geometry_spread"], "geometry spread")
        metrics = row["full"]
        for name in ("schur", "frobenius", "spectral", "minimum_eigenvalue",
                     "maximum_eigenvalue", "symmetry_error",
                     "spectral_over_schur", "spectral_over_frobenius"):
            close(data[name], metrics[name], "metric " + name)
        need(data["schur_row_index"] == metrics["schur_row_index"],
             "schur index")
        mode = row["eigenmode"]
        for name, actual in (
                ("selected_mode", data["mode"]),
                ("selected_eigenvalue", data["selected"]),
                ("selected_eigenvalue_abs", abs(data["selected"])),
                ("eigenvector_norm_error", data["norm_error"]),
                ("eigen_residual_inf", data["residual"]),
                ("rayleigh_sum_error", data["rayleigh_error"]),
                ("layer_reconstruction_error", data["reconstruction"]),
                ("absolute_rayleigh_mass", data["mass"]),
                ("same_block_signed_fraction", data["same_fraction"]),
                ("cross_block_signed_fraction", data["cross_fraction"]),
                ("cross_block_abs_fraction", data["cross_abs_fraction"]),
                ("far_block_abs_fraction", data["far_abs_fraction"])):
            if isinstance(actual, str):
                need(mode[name] == actual, "mode " + name)
            else:
                close(actual, mode[name], "mode " + name, 1.5e-5)
        need(mode["mode_rule"] ==
             "largest absolute eigenvalue; minimum mode wins ties" and
             mode["layer_count"] == 8 and
             mode["dominant_block_distance"] == data["dominant_distance"],
             "mode header")
        for expected_layer, actual_layer in zip(mode["layers"], data["layers"]):
            need(expected_layer["block_distance"] ==
                 actual_layer["block_distance"], "layer index")
            for name in ("rayleigh", "abs_rayleigh", "signed_fraction",
                         "abs_fraction", "cumulative_abs_fraction"):
                close(actual_layer[name], expected_layer[name],
                      "layer " + name, 2.0e-5)
        expected_parent = [row["origin"], row["count"], row["Q"],
                           row["kernel_exponent"], row["law"]] in parent_failures
        need(row["parent_failure"] is expected_parent, "parent flag")

    phase = payload.get("phase_summary", {})
    need(phase.get("cap") == "0.64000000000000001" and
         phase.get("schur_cap") == "0.82999999999999996" and
         phase.get("mode_selection") ==
         "largest absolute eigenvalue; min wins ties" and
         phase.get("layer_partition") ==
         "absolute block-index distance 0..7" and
         phase.get("cap_repair_betas") == [], "phase header")
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        item = phase.get("by_beta", {}).get(str(beta), {})
        cross = [float(row["eigenmode"]["cross_block_abs_fraction"])
                 for row in selected]
        need(item.get("rows") == 9 and
             item.get("full_spectral_cap_violations") == sum(
                 float(row["full"]["spectral"]) > SPECTRAL_CAP
                 for row in selected) and
             item.get("full_schur_cap_violations") == sum(
                 float(row["full"]["schur"]) > SCHUR_CAP
                 for row in selected) and
             item.get("minimum_mode_rows") + item.get("maximum_mode_rows") == 9,
             "phase beta")
        close(min(cross), item["cross_block_abs_fraction_min"], "phase cross min")
        close(max(cross), item["cross_block_abs_fraction_max"], "phase cross max")
        close(sum(cross) / len(cross), item["cross_block_abs_fraction_mean"],
              "phase cross mean")
        need(sum(item.get("dominant_distance_histogram", {}).values()) == 9,
             "phase histogram")
        for q0 in Q_ANCHORS:
            setting = [row for row in selected if row["Q"] == q0]
            item_q = phase.get("by_beta_q", {}).get(f"{beta}:{q0}", {})
            need(item_q.get("rows") == 3 and
                 item_q.get("full_spectral_cap_violations") == sum(
                     float(row["full"]["spectral"]) > SPECTRAL_CAP
                     for row in setting) and
                 item_q.get("dominant_distances") == [
                     row["eigenmode"]["dominant_block_distance"]
                     for row in setting], "phase q")
    audit = payload.get("finite_audit", {})
    beta2 = [row for row in rows if row["beta"] == 2]
    beta0 = [row for row in rows if row["beta"] == 0]
    actual_failures = [[row["origin"], row["count"], row["Q"],
                        row["kernel_exponent"], row["law"]]
                       for row in beta2
                       if float(row["full"]["spectral"]) > SPECTRAL_CAP]
    expected_failures = [
        [1010001, 2048, 2048, 1, "all_plus"],
        [1010001, 2048, 8192, 1, "all_plus"],
        [1018021, 2048, 2048, 1, "all_plus"],
        [1018021, 2048, 8192, 1, "all_plus"],
        [1026041, 2048, 2048, 1, "all_plus"],
        [1026041, 2048, 8192, 1, "all_plus"],
    ]
    need(audit.get("rows") == 18 and audit.get("beta2_rows") == 9 and
         audit.get("baseline_beta0_rows") == 9 and
         audit.get("origin_count") == 3 and audit.get("q_count") == 3 and
         audit.get("spectral_rows") == 18 and
         audit.get("beta2_full_spectral_cap_violations") == len(actual_failures) and
         audit.get("beta2_full_schur_cap_violations") == sum(
             float(row["full"]["schur"]) > SCHUR_CAP for row in beta2) and
         audit.get("baseline_beta0_full_spectral_cap_violations") == sum(
             float(row["full"]["spectral"]) > SPECTRAL_CAP for row in beta0) and
         audit.get("baseline_beta0_full_schur_cap_violations") == sum(
             float(row["full"]["schur"]) > SCHUR_CAP for row in beta0) and
         audit.get("full_failure_keys") == actual_failures and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    need(actual_failures == expected_failures and all(
         row["eigenmode"]["selected_mode"] == "minimum_eigenvalue" and
         row["eigenmode"]["dominant_block_distance"] == 0
         for row in rows), "finite mode census")
    failure_rows = [row for row in beta2 if row["parent_failure"]]
    need(len(failure_rows) == 6 and all(
         float(layer["rayleigh"]) < 0.0
         for row in failure_rows for layer in row["eigenmode"]["layers"]),
         "failure-mode sign coherence")
    need(max(float(row["eigenmode"]["far_block_abs_fraction"])
             for row in failure_rows) <= 0.008428824 and
         min(sum(float(layer["abs_fraction"])
                 for layer in row["eigenmode"]["layers"][:4])
             for row in failure_rows) >= 0.991571176,
         "near-block mass profile")
    theorem = payload.get("exact_theorem", {})
    need(theorem.get("anchor_inheritance") == {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-372 full-window off-block decomposition",
    }, "anchor theorem")
    need(payload.get("exact_anchor") == expected_anchor(), "exact anchor")
    expected_firewall = {
        "TPC373_FULL_WINDOW_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC373_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC373_BLOCK_DISTANCE_PARTITION": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC373_EIGENMODE_SELECTION_RULE": "PROVED_EXACT_FINITE_DETERMINISTIC",
        "TPC373_EIGENMODE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC373_LAYER_RECONSTRUCTION": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC373_RAYLEIGH_PROFILE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC373_CROSS_BLOCK_DECAY": "OPEN",
        "TPC373_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC373_ORIGIN_UNIFORMITY": "OPEN",
        "TPC373_WINDOW_UNIFORMITY": "OPEN",
        "TPC373_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC373_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC373_SOURCE_UNIFORM_L2": "OPEN",
        "TPC373_ARITHMETIC_ADVANCE": "NO",
        "TPC373_FIXED_POWER_CREDIT": 0,
        "TPC373_FULL_GATE_B": "OPEN",
        "TPC373_TWIN_PRIME_RESULT": "NONE",
    }
    need(payload.get("claim_firewall") == expected_firewall, "firewall")
    need(payload.get("round2_clue") == "TEST_LAYERWISE_CROSS_BLOCK_DECAY",
         "clue")
    return payload


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        payload = validate(document)
        phase = payload["phase_summary"]["by_beta"]["2"]
        print("TPC373_INDEPENDENT_CHECK=PASS rows=18 beta2_rows=9 "
              "beta2_violations=" + str(
                  payload["finite_audit"][
                      "beta2_full_spectral_cap_violations"]) +
              " max_cross_abs=" + phase["cross_block_abs_fraction_max"])
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC373_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
