#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-388.

This file intentionally does not import the TPC-388 producer.  It rebuilds
the finite c=1 matrices in descending prime-shell order and checks the
cross-family forecast against the sealed certificate.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-388-c1-cross-family-slope-transfer"
CERTIFICATE = PROJECT / "results/tpc388_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-387-c1-count-ladder-renormalization/results/"
    "tpc387_certificate.json")
PARENT_CERT_SHA256 = (
    "337aa65feedd4c729cd34c7d6de8865baeb96c4888ab44fbdf00f840d079e344")

SCHEMA = "TPC388_C1_CROSS_FAMILY_SLOPE_TRANSFER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_CROSS_FAMILY_SLOPE_TRANSFER"
ORIGINS = (2600001, 2604011, 2608021, 2612031, 2616041)
CALIBRATION_ORIGINS = ORIGINS[:3]
HOLDOUT_ORIGINS = ORIGINS[3:]
CALIBRATION_COUNTS = (512, 768)
HOLDOUT_COUNT = 1024
BLOCK_LENGTH = 128
BAND_MODES = ("fixed_c3", "full_relative")
Q_ANCHORS = (2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMALIZATIONS = ("local_diagonal", "pooled_train_scalar")
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
TRANSFER_ERROR_CAP = 0.03


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


def parse_no_duplicates(raw: bytes) -> dict[str, Any]:
    def hook(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise Failure("duplicate JSON key")
            out[key] = value
        return out
    value = json.loads(raw, object_pairs_hook=hook)
    need(isinstance(value, dict), "document object")
    return value


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 5.0e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
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


def signs(primes: list[int]) -> dict[str, np.ndarray]:
    result = {}
    for law in LAWS:
        result[law] = np.asarray([
            1.0 if (law == "all_plus" or
                    (law == "alternating_index" and i % 2 == 0) or
                    (law == "mod4_character" and p % 4 == 1) or
                    (law == "half_split" and i < len(primes) / 2)) else -1.0
            for i, p in enumerate(primes)], dtype=np.float64)
    return result


def weighted_components(values: np.ndarray, q0: int) -> tuple[Any, ...]:
    difference = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + difference.astype(np.float64) ** 2) ** EXPONENT)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    sign_vectors = signs(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(len(values), dtype=np.float64)
    weights = []
    # Descending shell order is the deliberate independent replay choice.
    for index, prime in reversed(tuple(enumerate(primes))):
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
            matrices[law] += sign_vectors[law][index] * block
    for law in LAWS:
        matrices[law][:] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return primes, matrices, geometry, weights


def metric(matrix: np.ndarray) -> tuple[float, float, float, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    eigenvalues = np.linalg.eigvalsh(matrix)
    spectral = max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 2e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frobenius + 1e-8, "metric envelope")
    return spectral, schur, frobenius, symmetry


def mask_for(mode: str, count: int) -> tuple[np.ndarray, int]:
    blocks = count // BLOCK_LENGTH
    cutoff = 3 if mode == "fixed_c3" else blocks - 1
    ids = np.arange(count) // BLOCK_LENGTH
    return np.abs(ids[:, None] - ids[None, :]) <= cutoff, cutoff


def make_row(origin: int, count: int, q0: int, law: str, norm: str,
             mode: str, matrix: np.ndarray, geometry: np.ndarray,
             denominator: float, denominator_role: str,
             primes: list[int], weights: list[float], mask: np.ndarray,
             cutoff: int) -> dict[str, Any]:
    if norm == "local_diagonal":
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
    else:
        normalized = matrix / denominator
    spectral, schur, frobenius, symmetry = metric(np.where(mask, normalized, 0.0))
    return {
        "origin": origin, "origin_role":
            f"calibration_{count}" if origin in CALIBRATION_ORIGINS else "holdout_1024",
        "Q": q0, "law": law, "normalization": norm, "band_mode": mode,
        "effective_cutoff": cutoff, "count": count,
        "interval": [origin, origin + count], "block_length": BLOCK_LENGTH,
        "block_count": count // BLOCK_LENGTH, "kernel_exponent": EXPONENT,
        "beta": BETA, "height": HEIGHT, "shell_cardinality": len(primes),
        "weight_min": min(weights), "weight_max": max(weights),
        "geometry_min": float(np.min(geometry)),
        "geometry_max": float(np.max(geometry)),
        "geometry_mean": float(np.mean(geometry)),
        "pooled_scalar_used": denominator, "pooled_scalar_role": denominator_role,
        "band_spectral": spectral, "band_schur": schur,
        "band_frobenius": frobenius, "symmetry_error": symmetry,
        "spectral_failure": bool(spectral > SPECTRAL_CAP),
        "schur_failure": bool(schur > SCHUR_CAP),
    }


def replay_rows() -> list[dict[str, Any]]:
    rows = []
    for q0 in Q_ANCHORS:
        packs = {}
        for origin in CALIBRATION_ORIGINS:
            for count in CALIBRATION_COUNTS:
                packs[origin, count] = weighted_components(
                    np.arange(origin, origin + count, dtype=np.int64), q0)
        for origin in HOLDOUT_ORIGINS:
            packs[origin, HOLDOUT_COUNT] = weighted_components(
                np.arange(origin, origin + HOLDOUT_COUNT, dtype=np.int64), q0)
        train = {count: float(np.mean([packs[o, count][2].mean()
                                       for o in CALIBRATION_ORIGINS])
                              ) for count in CALIBRATION_COUNTS}
        gamma = math.log(train[768] / train[512]) / math.log(1.5)
        extrapolated = train[768] * (4.0 / 3.0) ** gamma
        for (origin, count), (primes, matrices, geometry, weights) in packs.items():
            for mode in BAND_MODES:
                mask, cutoff = mask_for(mode, count)
                for norm in NORMALIZATIONS:
                    if norm == "local_diagonal":
                        denominator, role = 1.0, "local_diagonal"
                    elif count == 512:
                        denominator, role = train[512], "calibration_512"
                    elif count == 768:
                        denominator, role = train[768], "calibration_768"
                    else:
                        denominator, role = extrapolated, "calibration_extrapolated_1024"
                    for law in LAWS:
                        rows.append(make_row(origin, count, q0, law, norm, mode,
                                             matrices[law], geometry, denominator,
                                             role, primes, weights, mask, cutoff))
    need(len(rows) == 256, "replayed row census")
    return rows


def parent_cells() -> dict[tuple[str, str, str, int], dict[str, Any]]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent hash")
    doc = parse_no_duplicates(raw)
    cells = doc.get("payload", {}).get("ladder_summary", {}).get("cells", [])
    result = {}
    for cell in cells:
        result[(cell["band_mode"], cell["normalization"], cell["law"],
               cell["Q"])] = cell
    need(len(result) == 32, "parent cells")
    return result


def check_document(document: dict[str, Any], recompute: bool = True) -> dict[str, Any]:
    need(finite_tree(document), "non-finite document")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         parent.get("parent_slopes_frozen") is True and
         parent.get("parent_slopes_refit_on_current_family") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
         selection.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
         selection.get("calibration_counts") == [512, 768] and
         selection.get("holdout_count") == 1024 and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_slope_refit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "certificate rows")
    expected = {(o, n, q, law, norm, mode)
                for o in CALIBRATION_ORIGINS for n in (512, 768)
                for q in Q_ANCHORS for law in LAWS for norm in NORMALIZATIONS
                for mode in BAND_MODES}
    expected |= {(o, 1024, q, law, norm, mode)
                 for o in HOLDOUT_ORIGINS for q in Q_ANCHORS for law in LAWS
                 for norm in NORMALIZATIONS for mode in BAND_MODES}
    observed = {(r.get("origin"), r.get("count"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_mode")) for r in rows}
    need(observed == expected, "row keys")
    row_map = {(
        r["origin"], r["count"], r["Q"], r["law"], r["normalization"],
        r["band_mode"]): r for r in rows}
    for key, row in row_map.items():
        origin, count, q0, law, norm, mode = key
        role = f"calibration_{count}" if origin in CALIBRATION_ORIGINS else "holdout_1024"
        need(row.get("origin_role") == role and
             isinstance(row.get("spectral_failure"), bool) and
             isinstance(row.get("schur_failure"), bool), "row role")
    if recompute:
        replayed = replay_rows()
        for fresh in replayed:
            key = (fresh["origin"], fresh["count"], fresh["Q"], fresh["law"],
                   fresh["normalization"], fresh["band_mode"])
            recorded = row_map[key]
            for field in ("origin", "count", "Q", "law", "normalization",
                          "band_mode", "effective_cutoff", "block_length",
                          "block_count", "kernel_exponent", "beta", "height",
                          "shell_cardinality", "pooled_scalar_role"):
                need(recorded.get(field) == fresh[field], field + " mismatch")
            for field in ("weight_min", "weight_max", "geometry_min",
                          "geometry_max", "geometry_mean", "pooled_scalar_used",
                          "band_spectral", "band_schur", "band_frobenius",
                          "symmetry_error"):
                close(fresh[field], recorded.get(field), field)
            need(recorded.get("spectral_failure") == fresh["spectral_failure"] and
                 recorded.get("schur_failure") == fresh["schur_failure"],
                 "failure flags")
    summary = payload.get("transfer_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("parent_transfer_pass_count") == 32 and
         summary.get("local_control_pass_count") == 32 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32,
         "summary census")
    failures = summary.get("failure_counts_by_mode_normalization", {})
    need(sum(int(v.get("spectral", -1)) for v in failures.values()) == 40 and
         sum(int(v.get("schur", -1)) for v in failures.values()) == 0,
         "failure census")
    need(summary.get("stable_cells", {}).get("1024_holdout") == 28,
         "holdout stability")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC388_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC388_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC388_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC388_TWIN_PRIME_RESULT") == "NONE", "firewall")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [2600001, 2600014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "anchor")
    return summary


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        raw = CERTIFICATE.read_bytes()
        document = parse_no_duplicates(raw)
        need(raw == canonical(document), "noncanonical certificate")
        summary = check_document(document)
        print("TPC388_INDEPENDENT_CHECK=PASS rows=256 cells=32 "
              f"parent_pass={summary['parent_transfer_pass_count']}/32 "
              f"local_pass={summary['local_control_pass_count']}/32 "
              f"spectral_failures={sum(v['spectral'] for v in summary['failure_counts_by_mode_normalization'].values())} "
              f"stable_holdout={summary['stable_cells']['1024_holdout']}/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC388_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
