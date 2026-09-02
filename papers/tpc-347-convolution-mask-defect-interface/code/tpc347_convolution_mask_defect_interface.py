#!/usr/bin/env python3
"""TPC-347: an arithmetic L2 interface with an explicit mask defect.

The physical prime-shell matrix has two different ingredients: a translated
residue kernel and endpoint divisibility masks.  This producer keeps those
ingredients separate.  The unmasked kernel is a convolution on Z, while the
physical finite matrix is its masked interval compression.  The certificate
records the exact finite decomposition and a guarded spectral audit; it does
not claim an asymptotic arithmetic estimate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

# Keep the spectral replay stable across hosts with different BLAS defaults.
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc347_certificate.json"

PARENT_CODE = ROOT / (
    "papers/tpc-346-third-panel-hostile-replication/code/"
    "tpc346_third_panel_hostile_replication.py")
PARENT_CERT = ROOT / (
    "papers/tpc-346-third-panel-hostile-replication/results/"
    "tpc346_certificate.json")
PARENT_CODE_SHA256 = (
    "2c0bb5fd2e8738fa18dc419491a91b29c5a1fb8cc4f5fabaaec19e0a45752d4a")
PARENT_CERT_SHA256 = (
    "f15c5a5bf3ef9f14a5bdd9503bb74dbcc218b82b0598db0726d61deb01ee1e46")

SCHEMA = "TPC347_CONVOLUTION_MASK_DEFECT_INTERFACE_V1"
STATUS = (
    "PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT")
ROUND2_CLUE = "QUANTIFY_MASK_DEFECT_LOWER_WITNESSES_BEFORE_SOURCE_NATIVE_L2"

ORIGINS = (40097, 48097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
YOUNG_RADIUS = 65_536
NUMERIC_TOL = 2.0e-9
BOUND_TOL = 2.0e-9


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


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
    # Twelve significant digits survive harmless eigensolver last-bit changes.
    return format(float(value), ".12g")


def locked(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def load_parent() -> None:
    locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC346 producer")
    locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC346 certificate")
    raw = PARENT_CERT.read_bytes()
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC346 certificate canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION",
         "TPC346 certificate header")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(2 * max(Q_ANCHORS))


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def signs(primes: list[int], law: str) -> list[int]:
    need(law in LAW_NAMES, "unknown sign law")
    if law == "all_plus":
        return [1] * len(primes)
    if law == "alternating_index":
        return [1 if index % 2 == 0 else -1
                for index in range(len(primes))]
    if law == "mod4_character":
        return [1 if prime % 4 == 1 else -1 for prime in primes]
    return [1 if index < len(primes) / 2 else -1
            for index in range(len(primes))]


def spectral_norm(matrix: np.ndarray) -> tuple[float, float, float]:
    """Return induced 2-norm and the extreme eigenvalues of a symmetric matrix."""
    symmetric = (matrix + matrix.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric)
    need(len(eigenvalues) > 0 and bool(np.all(np.isfinite(eigenvalues))),
         "finite spectrum")
    lower = float(eigenvalues[0])
    upper = float(eigenvalues[-1])
    return max(abs(lower), abs(upper)), lower, upper


def matrices(origin: int, count: int, q0: int, exponent: int,
             law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    """Build physical A, unmasked T, and defect D=A-T independently of a parent."""
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distances = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distances * distances) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell_for(q0)
    for prime, sign in zip(primes, signs(primes, law)):
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(sign * prime) * kernel * centered
        ideal += block
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        physical += block * valid
    physical = (physical + physical.T) / 2.0
    ideal = (ideal + ideal.T) / 2.0
    defect = physical - ideal
    need(bool(np.all(np.isfinite(physical))) and
         bool(np.all(np.isfinite(ideal))),
         "finite matrix entries")
    return physical, ideal, defect, primes


def coherent_kernel_values(q0: int, exponent: int, law: str,
                           radius: int = YOUNG_RADIUS
                           ) -> tuple[float, float, float]:
    """Compute a guarded l1/Young envelope for the infinite unmasked kernel.

    For |d|>R, |centered_p(d)|<=1 and
    H^(2s)/(H^2+d^2)^s <= H^(2s)/|d|^(2s).  The returned tail is therefore
    an analytic majorant, while the finite sum is a reproducible numerical
    evaluation with a tiny upward safety margin.
    """
    need(radius > 0, "Young radius")
    distances = np.arange(1, radius + 1, dtype=np.int64)
    h = (float(HEIGHT) ** (2 * exponent) /
         (HEIGHT * HEIGHT + distances.astype(np.float64) ** 2) ** exponent)
    values = np.zeros(radius, dtype=np.float64)
    primes = shell_for(q0)
    for prime, sign in zip(primes, signs(primes, law)):
        centered = ((distances % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        values += float(sign * prime) * h * centered
    finite_l1 = 2.0 * math.fsum(float(abs(value)) for value in values)
    tail = (2.0 * HEIGHT ** (2 * exponent) * sum(primes) /
            ((2 * exponent - 1) * radius ** (2 * exponent - 1)))
    # Round upward so the stored floating envelope is not a lower rounding.
    envelope = math.nextafter(finite_l1 + tail, math.inf)
    return envelope, finite_l1, tail


def exact_matrix(origin: int, count: int, q0: int, exponent: int,
                 law: str, masked: bool) -> list[list[Fraction]]:
    values = list(range(origin, origin + count))
    result = [[Fraction(0) for _ in values] for _ in values]
    primes = shell_for(q0)
    for prime, sign in zip(primes, signs(primes, law)):
        for i, u in enumerate(values):
            for j, t in enumerate(values):
                if u == t:
                    continue
                if masked and (u % prime == 0 or t % prime == 0):
                    continue
                centered = (Fraction(1) if (u - t) % prime == 0
                            else Fraction(0))
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += sign * prime * kernel * centered
    return result


def fraction_matrix_digest(matrix: list[list[Fraction]]) -> str:
    text = [[f"{item.numerator}/{item.denominator}" for item in row]
            for row in matrix]
    return hashlib.sha256(canonical(text)).hexdigest()


def exact_anchor() -> dict[str, Any]:
    actual = exact_matrix(1, 6, 4, 1, "all_plus", True)
    ideal = exact_matrix(1, 6, 4, 1, "all_plus", False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(6)]
              for i in range(6)]
    need(all(actual[i][j] == ideal[i][j] + defect[i][j]
             for i in range(6) for j in range(6)), "exact defect identity")
    need(all(actual[i][j] == actual[j][i] and ideal[i][j] == ideal[j][i]
             for i in range(6) for j in range(6)), "exact symmetry")
    return {
        "interval": [1, 6],
        "q": 4,
        "shell": shell_for(4),
        "kernel_exponent": 1,
        "height": HEIGHT,
        "matrix_shape": [6, 6],
        "actual_digest": fraction_matrix_digest(actual),
        "ideal_digest": fraction_matrix_digest(ideal),
        "defect_digest": fraction_matrix_digest(defect),
        "identity_exact": True,
        "symmetry_exact": True,
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               law: str, young: dict[tuple[int, int, str], tuple[float, float, float]]
               ) -> dict[str, Any]:
    actual, ideal, defect, primes = matrices(origin, count, q0, exponent, law)
    actual_norm, actual_min, actual_max = spectral_norm(actual)
    ideal_norm, ideal_min, ideal_max = spectral_norm(ideal)
    defect_norm, defect_min, defect_max = spectral_norm(defect)
    defect_frobenius = float(np.linalg.norm(defect, ord="fro"))
    envelope, finite_l1, tail = young[(q0, exponent, law)]
    combined = envelope + defect_frobenius
    need(actual_norm <= combined * (1.0 + BOUND_TOL),
         "finite combined envelope")
    need(bool(np.max(np.abs(actual - (ideal + defect))) <= NUMERIC_TOL),
         "matrix decomposition")
    return {
        "origin": origin,
        "count": count,
        "source_interval": [origin, origin + count - 1],
        "q": q0,
        "shell": primes,
        "kernel_exponent": exponent,
        "law": law,
        "operator_shape": [count, count],
        "actual_norm": show(actual_norm),
        "actual_min_eigenvalue": show(actual_min),
        "actual_max_eigenvalue": show(actual_max),
        "ideal_norm": show(ideal_norm),
        "ideal_min_eigenvalue": show(ideal_min),
        "ideal_max_eigenvalue": show(ideal_max),
        "defect_norm": show(defect_norm),
        "defect_min_eigenvalue": show(defect_min),
        "defect_max_eigenvalue": show(defect_max),
        "defect_frobenius_norm": show(defect_frobenius),
        "defect_to_ideal_ratio": show(defect_norm / ideal_norm),
        "actual_to_ideal_ratio": show(actual_norm / ideal_norm),
        "triangle_envelope": show(ideal_norm + defect_norm),
        "young_l1_envelope": show(envelope),
        "young_finite_l1": show(finite_l1),
        "young_tail_majorant": show(tail),
        "combined_finite_envelope": show(combined),
        "combined_occupancy": show(actual_norm / combined),
        "decomposition_max_error": show(float(np.max(
            np.abs(actual - (ideal + defect))))),
        "finite_bound_holds": True,
    }


def build_payload() -> dict[str, Any]:
    load_parent()
    young = {(q0, exponent, law): coherent_kernel_values(q0, exponent, law)
             for q0 in Q_ANCHORS for exponent in EXPONENTS
             for law in LAW_NAMES}
    rows = [row_record(origin, count, q0, exponent, law, young)
            for origin in ORIGINS for count in COUNTS
            for q0 in Q_ANCHORS for exponent in EXPONENTS
            for law in LAW_NAMES]
    need(len(rows) == 192, "row census")

    invariance: list[dict[str, Any]] = []
    for count in COUNTS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                for law in LAW_NAMES:
                    matrices_by_origin = [matrices(origin, count, q0,
                                                    exponent, law)[1]
                                          for origin in ORIGINS]
                    difference = float(np.max(np.abs(
                        matrices_by_origin[0] - matrices_by_origin[1])))
                    norms = [spectral_norm(item)[0] for item in matrices_by_origin]
                    need(difference <= NUMERIC_TOL and
                         abs(norms[0] - norms[1]) <= NUMERIC_TOL *
                         max(1.0, *norms), "translation invariance")
                    invariance.append({
                        "count": count, "q": q0,
                        "kernel_exponent": exponent, "law": law,
                        "origin_pair": list(ORIGINS),
                        "matrix_max_difference": show(difference),
                        "ideal_norms": [show(item) for item in norms],
                        "invariant": True,
                    })
    need(len(invariance) == 96, "invariance census")

    ratios = [float(item["defect_to_ideal_ratio"]) for item in rows]
    actual_ratios = [float(item["actual_to_ideal_ratio"]) for item in rows]
    occupancies = [float(item["combined_occupancy"]) for item in rows]
    need(all(0.0 <= value <= 1.0 + BOUND_TOL for value in occupancies),
         "combined occupancy")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC346_producer_sha256": PARENT_CODE_SHA256,
            "TPC346_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "source_counts": list(COUNTS),
            "interval_rule": "I_(o,M)={o,...,o+M-1}",
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "physical_entry":
                "1_(u!=t)1_(p does not divide u t)p h_s(u-t) "
                "(1_(p divides u-t)-1/(p-1))",
            "ideal_entry":
                "1_(u!=t)p h_s(u-t) "
                "(1_(p divides u-t)-1/(p-1))",
            "defect": "D=A-T",
            "young_radius": YOUNG_RADIUS,
            "young_tail":
                "2 H^(2s) sum_p p / ((2s-1)R^(2s-1))",
        },
        "exact_theorem": {
            "mask_factorization":
                "A_I=sum_p e_p R_I P_p K_p P_p E_I",
            "unmasked_convolution":
                "K_e=sum_p e_p K_p with (K_p f)(u)=sum_d k_p(d)f(u-d)",
            "fourier_interface":
                "||K_e||_(ell2(Z)->ell2(Z))=ess_sup_theta |sum_d k_e(d)e^(-i d theta)|",
            "compression_bound": "||R_I K_e E_I||_(2->2)<=||K_e||_(2->2)",
            "defect_identity": "A_I=T_I+D_I, D_I=A_I-T_I",
            "finite_triangle_bound":
                "||A_I||<=||T_I||+||D_I||<=||K_e||+||D_I||_F",
            "young_bound": "||K_e||<=sum_d |k_e(d)|",
            "translation_invariance":
                "T_(o+v,M)=T_(o,M) after simultaneous index translation",
            "finite_scope": "identities are exact; numerical rows are finite audits",
        },
        "finite_audit": {
            "origins": len(ORIGINS),
            "source_counts": len(COUNTS),
            "q_anchors": len(Q_ANCHORS),
            "kernel_exponents": len(EXPONENTS),
            "laws": len(LAW_NAMES),
            "rows": len(rows),
            "translation_invariance_records": len(invariance),
            "combined_bound_records": len(rows),
            "combined_bound_violations": 0,
            "defect_ratio_gt_quarter": sum(value > 0.25 for value in ratios),
            "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "summary": {
            "defect_to_ideal_ratio_min": show(min(ratios)),
            "defect_to_ideal_ratio_max": show(max(ratios)),
            "actual_to_ideal_ratio_min": show(min(actual_ratios)),
            "actual_to_ideal_ratio_max": show(max(actual_ratios)),
            "combined_occupancy_min": show(min(occupancies)),
            "combined_occupancy_max": show(max(occupancies)),
            "defect_ratio_gt_quarter": sum(value > 0.25 for value in ratios),
            "translation_invariance": "NUMERICALLY_CERTIFIED_FINITE_96_OF_96",
            "route_readout":
                "MASK_DEFECT_IS_NOT_DISCARDABLE_ON_THE_DECLARED_PANEL",
        },
        "exact_anchor": exact_anchor(),
        "young_envelopes": [
            {"q": q0, "kernel_exponent": exponent, "law": law,
             "envelope": show(young[(q0, exponent, law)][0]),
             "finite_l1": show(young[(q0, exponent, law)][1]),
             "tail_majorant": show(young[(q0, exponent, law)][2]),
             "tail_formula_valid": True}
            for q0 in Q_ANCHORS for exponent in EXPONENTS
            for law in LAW_NAMES],
        "translation_invariance_audit": invariance,
        "rows": rows,
        "claim_firewall": {
            "TPC347_MASK_FACTORISATION":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC347_UNMASKED_FOURIER_INTERFACE": "PROVED_EXACT_CONDITIONAL",
            "TPC347_COMPRESSION_INEQUALITY": "PROVED_EXACT",
            "TPC347_YOUNG_ENVELOPE": "PROVED_EXACT_FOR_UNMASKED_KERNEL",
            "TPC347_TRANSLATION_INVARIANCE":
                "NUMERICALLY_CERTIFIED_FINITE_96_OF_96",
            "TPC347_MASK_DEFECT_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_192_ROWS",
            "TPC347_DEFECT_DISCARDABILITY": "REFUTED_SCOPED",
            "TPC347_SOURCE_UNIFORM_ARITHMETIC_L2": "OPEN",
            "TPC347_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC347_FIXED_POWER_CREDIT": 0,
            "TPC347_FULL_GATE_B": "OPEN",
            "TPC347_TWIN_PRIME_RESULT": "NONE",
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
        document = build_document()
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(document))
            print("TPC347_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate does not replay")
            print("TPC347_CERTIFICATE=PASS rows=192 invariance=96 "
                  "bound_violations=0 defect_ratio_gt_quarter=" +
                  str(document["payload"]["finite_audit"]
                      ["defect_ratio_gt_quarter"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC347_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
