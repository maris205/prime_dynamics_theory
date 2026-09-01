#!/usr/bin/env python3
"""TPC-322: an operator-level signed projector/reassembly audit.

The preceding projects formed a direct-sum operator
    A_direct beta = (B_p beta)_p,
whose Gram matrix forgets cross-prime signs.  This release defines the
normalized coherent projector onto a sign-labelled diagonal subspace and
audits its finite Hilbert--Schmidt energy.  Everything is kept on the same
literal deleted-diagonal prime-shell operator as TPC-321.

The result is deliberately an operator-image audit.  It is not a signed
prime-sum estimate and does not claim arithmetic cancellation or a power
saving.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
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

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC322 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc322_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-321-cross-shell-profile-stability/results/"
    "tpc321_certificate.json")
PARENT_CERT_SHA256 = (
    "f7048edce7260bceb14acc674311ce0268fb5ae4fdb9914edc0138a5cb7cc6be")

SCHEMA = "TPC322_SIGNED_PROJECTOR_REASSEMBLY_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_"
    "REASSEMBLY_ATLAS")
ROUND2_CLUE = (
    "TEST_CANONICAL_SIGN_LAWS_AGAINST_OPERATOR_SPECTRAL_PROFILES_"
    "AND_SOURCE_NATIVE_ARITHMETIC_L2")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
NUMERICAL_GUARD = 1.0e-12
PATH_TOL = 2.0e-9
SMALL_INTERVAL = (17, 32)
SMALL_Q = 4
SMALL_EXPONENT = 1


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


def display(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(160)


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def source_interval(scale: int) -> tuple[int, int, int]:
    lo, hi = scale // 2 + 1, scale
    count = hi - lo + 1
    need(scale % 2 == 0 and count == scale // 2,
         "dyadic source interval")
    return lo, hi, count


def block_matrix(scale: int, q0: int, exponent: int,
                 reverse_shell: bool = False) -> tuple[list[int], list[np.ndarray]]:
    """Return the literal p-blocks B_p in the requested accumulation order."""
    lo, hi, _ = source_interval(scale)
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    height = float(HEIGHT)
    kernel = (height ** (2 * exponent) /
              (height * height + dd * dd) ** exponent)
    shell = shell_for(q0)
    if reverse_shell:
        shell = list(reversed(shell))
    blocks: list[np.ndarray] = []
    for prime in shell:
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        blocks.append(prime * kernel * centered * valid)
    return shell, blocks


def block_gram(blocks: list[np.ndarray], reverse: bool = False) -> np.ndarray:
    """Frobenius Gram of the p-blocks, with an explicit order choice."""
    order = range(len(blocks) - 1, -1, -1) if reverse else range(len(blocks))
    ordered = list(order)
    result = np.zeros((len(blocks), len(blocks)), dtype=np.float64)
    for i in ordered:
        for j in ordered:
            result[i, j] = float(np.sum(blocks[i] * blocks[j],
                                        dtype=np.float64))
    return (result + result.T) / 2.0


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    m = len(primes)
    return {
        "all_plus": np.ones(m, dtype=np.float64),
        "alternating_index": np.asarray(
            [1 if i % 2 == 0 else -1 for i in range(m)], dtype=np.float64),
        "mod4_character": np.asarray(
            [1 if prime % 4 == 1 else -1 for prime in primes],
            dtype=np.float64),
        "half_split": np.asarray(
            [1 if i < m / 2 else -1 for i in range(m)], dtype=np.float64),
    }


def ratio(gram: np.ndarray, signs: np.ndarray) -> float:
    diagonal = float(np.trace(gram))
    need(diagonal > 0 and math.isfinite(diagonal), "positive direct energy")
    value = float(signs @ gram @ signs)
    need(value >= -1.0e-8 and math.isfinite(value), "nonnegative signed energy")
    return max(0.0, value / diagonal)


def exhaustive_extrema(gram: np.ndarray) -> dict[str, Any]:
    """Enumerate sign vectors with the first sign fixed to remove global sign."""
    m = len(gram)
    best_min: tuple[float, tuple[int, ...]] | None = None
    best_max: tuple[float, tuple[int, ...]] | None = None
    diagonal = float(np.trace(gram))
    need(m > 0 and diagonal > 0, "extrema domain")
    for tail in itertools.product((1, -1), repeat=m - 1):
        signs = np.asarray((1,) + tail, dtype=np.float64)
        value = ratio(gram, signs)
        label = tuple(int(x) for x in signs)
        candidate = (value, label)
        if best_min is None or candidate < best_min:
            best_min = candidate
        if best_max is None or candidate > best_max:
            best_max = candidate
    need(best_min is not None and best_max is not None, "signed extrema")
    return {
        "minimum_ratio": display(best_min[0]),
        "minimum_signs": list(best_min[1]),
        "maximum_ratio": display(best_max[0]),
        "maximum_signs": list(best_max[1]),
        "sign_search_size_mod_global": 1 << (m - 1),
    }


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
    centered -= Fraction(1, prime - 1)
    kernel = Fraction(HEIGHT ** (2 * exponent),
                      (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
    return prime * kernel * centered


def exact_small_audit() -> dict[str, Any]:
    values = list(range(SMALL_INTERVAL[0], SMALL_INTERVAL[1] + 1))
    primes = shell_for(SMALL_Q)
    blocks = [[[exact_entry(p, u, t, SMALL_EXPONENT)
                for t in values] for u in values] for p in primes]
    gram = [[sum((blocks[i][u][t] * blocks[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signs = (1, -1) if len(primes) == 2 else tuple(
        1 if i % 2 == 0 else -1 for i in range(len(primes)))
    signed = sum((signs[i] * signs[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))
    need(direct > 0 and signed >= 0, "exact signed anchor")
    def frac_digest(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()
    return {
        "interval": list(SMALL_INTERVAL),
        "Q": SMALL_Q,
        "shell": primes,
        "exponent": SMALL_EXPONENT,
        "direct_energy_digest": frac_digest(direct),
        "signed_energy_digest": frac_digest(signed),
        "direct_energy_decimal": display(float(direct), 16),
        "signed_energy_decimal": display(float(signed), 16),
        "signed_over_direct_decimal": display(float(signed / direct), 16),
        "identity_exact": True,
    }


def interval(values: list[float]) -> list[str]:
    low = max(0.0, min(values) - NUMERICAL_GUARD)
    high = max(values) + NUMERICAL_GUARD
    need(low <= min(values) <= max(values) <= high,
         "outward ratio interval")
    return [display(low), display(high)]


def row_record(scale: int, q0: int, exponent: int) -> dict[str, Any]:
    primes, forward_blocks = block_matrix(scale, q0, exponent, False)
    reverse_primes, reverse_blocks = block_matrix(scale, q0, exponent, True)
    need(primes == list(reversed(reverse_primes)), "shell order")
    # Put the reverse path back in canonical prime order before comparing it.
    reverse_blocks = list(reversed(reverse_blocks))
    forward_gram = block_gram(forward_blocks, False)
    reverse_gram = block_gram(reverse_blocks, True)
    need(bool(np.all(np.isfinite(forward_gram))) and
         bool(np.all(np.isfinite(reverse_gram))), "finite block Gram")
    patterns = sign_patterns(primes)
    pattern_records: dict[str, dict[str, Any]] = {}
    for name, signs in patterns.items():
        forward_value = ratio(forward_gram, signs)
        reverse_value = ratio(reverse_gram, signs)
        need(abs(forward_value - reverse_value) < PATH_TOL,
             "signed path agreement")
        values = [forward_value, reverse_value]
        pattern_records[name] = {
            "signs": [int(value) for value in signs],
            "ratio_interval": interval(values),
            "ratio_estimate": display(forward_value),
            "projected_fraction_interval": interval(
                [value / len(primes) for value in values]),
            "projected_fraction_estimate": display(
                forward_value / len(primes)),
            "path_abs_difference": display(abs(forward_value - reverse_value)),
        }
    forward_extrema = exhaustive_extrema(forward_gram)
    reverse_extrema = exhaustive_extrema(reverse_gram)
    min_values = [float(forward_extrema["minimum_ratio"]),
                  float(reverse_extrema["minimum_ratio"])]
    max_values = [float(forward_extrema["maximum_ratio"]),
                  float(reverse_extrema["maximum_ratio"])]
    need(max(min_values) < 1.0 and min(max_values) > 1.0,
         "finite sign flexibility")
    # The two paths can choose different tied labels; only the values are
    # claim-bearing, while the forward labels are retained as witnesses.
    return {
        "scale": scale,
        "source_interval": [scale // 2 + 1, scale],
        "source_count": scale // 2,
        "Q": q0,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "shell": primes,
        "shell_cardinality": len(primes),
        "operator_rows": (scale // 2) * len(primes),
        "operator_columns": scale // 2,
        "direct_hilbert_schmidt_energy": display(float(np.trace(forward_gram))),
        "path_direct_energy_abs_difference": display(
            abs(float(np.trace(forward_gram)) -
                float(np.trace(reverse_gram)))),
        "pattern_records": pattern_records,
        "minimum": {
            "ratio_interval": interval(min_values),
            "ratio_estimate": display(min_values[0]),
            "projected_fraction_interval": interval(
                [value / len(primes) for value in min_values]),
            "signs": forward_extrema["minimum_signs"],
            "search_size_mod_global": forward_extrema["sign_search_size_mod_global"],
        },
        "maximum": {
            "ratio_interval": interval(max_values),
            "ratio_estimate": display(max_values[0]),
            "projected_fraction_interval": interval(
                [value / len(primes) for value in max_values]),
            "signs": forward_extrema["maximum_signs"],
            "search_size_mod_global": forward_extrema["sign_search_size_mod_global"],
        },
        "projector_definition": (
            "E_e v=m^(-1/2)(e_p v)_p; P_e=E_e E_e^*; "
            "||P_e A_direct||_HS^2=(1/m)||sum_p e_p B_p||_F^2"),
        "finite_numerical_guard": display(NUMERICAL_GUARD),
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC321 parent certificate lock")
    rows = [row_record(scale, q0, exponent)
            for scale in SCALES for q0 in Q_ANCHORS
            for exponent in EXPONENTS]
    need(len(rows) == 24, "row census")
    pattern_names = ("all_plus", "alternating_index", "mod4_character",
                     "half_split")
    counts: dict[str, dict[str, int]] = {
        name: {"below_one": 0, "above_one": 0} for name in pattern_names}
    for row in rows:
        for name in pattern_names:
            value = float(row["pattern_records"][name]["ratio_estimate"])
            counts[name]["below_one" if value < 1.0 else "above_one"] += 1
    min_values = [float(row["minimum"]["ratio_estimate"]) for row in rows]
    max_values = [float(row["maximum"]["ratio_estimate"]) for row in rows]
    need(all(value < 1.0 for value in min_values) and
         all(value > 1.0 for value in max_values), "extreme sign census")
    need(counts["all_plus"] == {"below_one": 3, "above_one": 21},
         "all-plus census")
    need(counts["alternating_index"] == {"below_one": 21, "above_one": 3},
         "alternating census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-321 cross-shell spectral-profile stability",
            "certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "source_scales": list(SCALES),
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "domain": "ell^2(I_X)",
            "direct_codomain": "direct_sum_p ell^2(I_X)",
            "shell_rule": "S_Q={p prime: Q<p<=2Q}",
            "block": (
                "B_p[u,t]=1_{u!=t,p not|ut} p H^(2s)/(H^2+(u-t)^2)^s "
                "(1_{u==t mod p}-1/(p-1))"),
            "projector": (
                "E_e v=m^(-1/2)(e_p v)_p; P_e=E_e E_e^*"),
            "reassembled_operator": "C_e=sum_p e_p B_p",
            "ratio": "rho_e=||C_e||_F^2/sum_p||B_p||_F^2",
            "projected_fraction": "phi_e=rho_e/m",
            "canonical_sign_laws": ["all_plus", "alternating_index",
                                     "mod4_character", "half_split"],
            "global_sign_gauge": "first sign fixed to +1 in exhaustive search",
            "paths": ["forward prime order", "reverse prime order"],
            "numerical_guard": NUMERICAL_GUARD,
        },
        "exact_theorem": {
            "direct_sum_identity": (
                "||A_direct beta||^2=sum_p||B_p beta||^2"),
            "signed_expansion": (
                "C_e^T C_e=sum_{p,q}e_p e_q B_p^T B_q"),
            "projector_identity": (
                "||P_e A_direct||_HS^2=(1/m)||C_e||_F^2"),
            "global_sign_invariance": "rho_e=rho_{-e}",
            "projector_contraction": "0<=phi_e<=1",
            "scope": "finite matrices on the declared panel",
        },
        "finite_audit": {
            "rows": len(rows),
            "minimum_sign_below_one": sum(value < 1.0 for value in min_values),
            "maximum_sign_above_one": sum(value > 1.0 for value in max_values),
            "minimum_ratio_range": [display(min(min_values)),
                                    display(max(min_values))],
            "maximum_ratio_range": [display(min(max_values)),
                                    display(max(max_values))],
            "pattern_counts": counts,
            "all_plus_law": "REFUTED_FINITE_PANEL",
            "alternating_law": "REFUTED_FINITE_PANEL",
            "finite_sign_flexibility": "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC322_SIGNED_PROJECTOR_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC322_OPERATOR_REASSEMBLY_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_24_ROWS",
            "TPC322_MIN_SIGN_EXISTS": "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC322_MAX_SIGN_EXISTS": "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC322_ALL_PLUS_LAW": "REFUTED_FINITE_PANEL",
            "TPC322_ALTERNATING_LAW": "REFUTED_FINITE_PANEL",
            "TPC322_ARITHMETIC_ADVANCE": "NO",
            "TPC322_FIXED_POWER_CREDIT": 0,
            "TPC322_FULL_GATE_B": "OPEN",
            "TPC322_TWIN_PRIME_RESULT": "NONE",
        },
        "exact_small_audit": exact_small_audit(),
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored == build_document(), "certificate does not replay")
    print("TPC322_CERTIFICATE=PASS rows=24 min_sign=24/24 max_sign=24/24 "
          "all_plus=3/21 alternating=21/3")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            write_certificate()
            print("TPC322_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC322_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
