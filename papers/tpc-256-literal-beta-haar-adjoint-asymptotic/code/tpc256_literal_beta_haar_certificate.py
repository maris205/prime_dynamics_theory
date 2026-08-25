#!/usr/bin/env python3
"""Deterministic certificate for the TPC-256 literal beta Haar theorem.

The finite computations reproduce exact rank, divisor-density, unit-mask, and
boundary bookkeeping.  The two finite beta samples are explicitly labelled
NUMERICAL_OBSERVATION and are not used to prove an asymptotic statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "4695df00b1c6962bc94e21474e101c698f39f4bd"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results" / "tpc256_certificate.json"

SOURCE_HASHES = {
    "TPC_HANDOFF.md": "1da1d8a74c5fd85a2401a389762966aaa0cb0405e2df16465edae09ead47600e",
    "papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md": "a61a7a8f43ef4cbf46a69443b01bd2d4d41cc31a418612ad7a66fd5d54af6446",
    "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md": "b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e",
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md": "cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97",
    "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md": "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a",
    "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md": "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1",
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md": "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md": "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
}

SOURCE_MARKERS = {
    "TPC_HANDOFF.md": ("TPC-255", "V108"),
    "papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md": (
        "pi(x) = Li(x) + O(x exp(-c sqrt(log x))).",
        "de la Vallee Poussin",
    ),
    "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md": (
        "H=x^{21/32}",
        "U=x^{133/400}",
        "\\beta(t)=\\frac{\\Lambda(t)}{\\log t}",
    ),
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md": (
        "B_Q=sum_(q in Q_x) q(q-2)/(q-1).",
        "hard-window leakage",
        "child-jump leakage",
    ),
    "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md": (
        "\\frac{H^2}{q}",
        "Complete centered Poisson identity",
    ),
    "research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md": (
        "\\beta_x^{\\rm raw}(t)=",
        "d^{400}\\leq x^{133}",
        "proper-factor identity",
    ),
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md": (
        "rho=sqrt(ell r/N)",
        "Coefficient-independent rank midpoint",
    ),
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md": (
        "(3/2+o(1)) Q^2/log Q",
        "Weighted-prime aggregation",
    ),
}

FIREWALL = {
    "TPC256_ADJOINT_NORMALIZED_COMPLEX_ASYMPTOTIC": "PROVED_SOURCE_BACKED",
    "TPC256_ARITHMETIC_ADVANCE": "YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE",
    "TPC256_FIXED_ATOM_CREDIT": 0,
    "TPC256_FULL_GATE_B": "OPEN",
    "TPC256_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC256_L2": "NONE",
    "TPC256_LITERAL_BETA_HAAR_ASYMPTOTIC": "PROVED_SOURCE_BACKED",
    "TPC256_NORMALIZED_PHASE_TO_MINUS_ONE": "PROVED",
    "TPC256_REAL_PART_EVENTUALLY_NEGATIVE": "PROVED",
    "TPC256_ROUTE_ADVANCE": "YES_LITERAL_ARITHMETIC",
    "TPC256_SCALAR_EVENTUALLY_NONZERO": "PROVED",
    "TPC256_SCALAR_IS_REAL": "NOT_CLAIMED",
    "TPC256_TWIN_PRIME_RESULT": "NONE",
    "TPC256_UNQUALIFIED_PRINCIPAL_ARGUMENT_TO_PLUS_PI": "NOT_CLAIMED",
}

ROUND2_CLUE = (
    "EXPLOIT_EXACT_DIVISOR_DENSITY_CANCELLATION_BEFORE_ANY_TRIANGLE__"
    "THEN_USE_THE_BQ_DIAGONAL_MAIN_AND_H2_OVER_Q_BOUNDARY_MOMENT_TO_"
    "ISOLATE_THE_TRANSVERSE_FULL_GATE_B_REMAINDER"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"


def git_blob(relative_path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{BASELINE_HEAD}:{relative_path}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(proc.returncode == 0, f"cannot read frozen source {relative_path}")
    return proc.stdout


def verify_sources() -> int:
    marker_count = 0
    for relative_path, expected_hash in SOURCE_HASHES.items():
        blob = git_blob(relative_path)
        observed_hash = hashlib.sha256(blob).hexdigest()
        require(observed_hash == expected_hash, f"source hash mismatch: {relative_path}")
        text = blob.decode("utf-8")
        for marker in SOURCE_MARKERS[relative_path]:
            require(marker in text, f"source claim marker missing: {relative_path}: {marker}")
            marker_count += 1
    return marker_count


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def rank_data(clock: Fraction) -> tuple[int, int, int, int, int, int]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    midpoint = a + ell
    require(ell > 0 and right > 0, "rank clock too short")
    return a, b, n, ell, right, midpoint


def count_multiples(lo: int, hi: int, divisor: int) -> int:
    if lo > hi:
        return 0
    return hi // divisor - (lo - 1) // divisor


def finite_exact_checks() -> dict[str, int]:
    clocks = [Fraction(80 + 3 * index, 1) for index in range(32)]
    clocks += [Fraction(323 + 12 * index + (2 * (index % 5) + 1), 4) for index in range(32)]
    rank_identities = 0
    divisor_layers = 0
    for clock in clocks:
        a, b, n, ell, right, midpoint = rank_data(clock)
        rho_squared = Fraction(ell * right, n)
        normalization = rho_squared * (Fraction(1, ell) + Fraction(1, right))
        require(normalization == 1, "rank normalization failed")
        require((midpoint - a) == ell and (b - midpoint) == right, "rank endpoint failed")
        rank_identities += 1
        for divisor in range(1, 25):
            left_count = count_multiples(a + 1, midpoint, divisor)
            right_count = count_multiples(midpoint + 1, b, divisor)
            left_error = abs(Fraction(left_count, 1) - Fraction(ell, divisor))
            right_error = abs(Fraction(right_count, 1) - Fraction(right, divisor))
            require(left_error <= 1 and right_error <= 1, "divisor density error exceeded one")
            divisor_layers += 1

    unit_mask_terms = 0
    unit_periods = 0
    for prime in (3, 5, 7, 11, 13, 17, 19, 23):
        for residue in range(1, prime):
            period_sum = Fraction(0, 1)
            for u in range(prime):
                value = Fraction(0, 1)
                if u % prime != 0:
                    value = Fraction(int(u % prime == residue), 1) - Fraction(1, prime - 1)
                period_sum += value
            require(period_sum == 0, "combined output-unit row is not centered")
            unit_periods += 1
            t = residue
            for h in range(-3 * prime, 3 * prime + 1):
                u = t + h
                value = Fraction(0, 1)
                if u % prime != 0:
                    value = Fraction(int(u % prime == t % prime), 1) - Fraction(1, prime - 1)
                bound = Fraction(int(h % prime == 0), 1) + Fraction(2, prime)
                require(abs(value) <= bound, "full unit-mask pointwise bound failed")
                unit_mask_terms += 1

    hard_boundary_checks = 0
    child_boundary_checks = 0
    lo, hi, midpoint = 33, 96, 64
    points = range(lo, hi + 1)
    for h in range(-96, 97):
        hard_count = sum(1 for t in points if not (lo <= t + h <= hi))
        child_count = sum(
            1
            for t in points
            if lo <= t + h <= hi and ((t <= midpoint) != (t + h <= midpoint))
        )
        require(hard_count <= abs(h), "hard-boundary crossing count failed")
        require(child_count <= abs(h), "child-boundary crossing count failed")
        hard_boundary_checks += 1
        child_boundary_checks += 1

    return {
        "boundary_hard_checks": hard_boundary_checks,
        "boundary_jump_checks": child_boundary_checks,
        "divisor_layers": divisor_layers,
        "rank_clocks": len(clocks),
        "rank_identities": rank_identities,
        "unit_mask_periods": unit_periods,
        "unit_mask_terms": unit_mask_terms,
    }


def prime_sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    stop = math.isqrt(limit)
    for value in range(2, stop + 1):
        if flags[value]:
            start = value * value
            count = (limit - start) // value + 1
            flags[start : limit + 1 : value] = b"\x00" * count
    return [value for value in range(2, limit + 1) if flags[value]]


def mobius_value(value: int) -> int:
    remaining = value
    sign = 1
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            if remaining % prime == 0:
                return 0
            sign = -sign
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        sign = -sign
    return sign


def beta_haar_observation(clock: int) -> dict[str, str | int]:
    x = int(clock)
    a = x // 2
    b = x
    n = b - a
    ell = n // 2
    right = n - ell
    midpoint = a + ell
    rho = math.sqrt(ell * right / n)

    prime_left = 0.0
    prime_right = 0.0
    for prime in prime_sieve(b):
        power = prime
        exponent = 1
        while power <= b:
            weight = 1.0 / exponent
            if a < power <= midpoint:
                prime_left += weight
            elif midpoint < power <= b:
                prime_right += weight
            if power > b // prime:
                break
            power *= prime
            exponent += 1

    cutoff = int(math.floor(x ** (133.0 / 400.0)))
    divisor_left = 0
    divisor_right = 0
    for divisor in range(1, cutoff + 1):
        mu = mobius_value(divisor)
        if mu != 0:
            divisor_left += mu * count_multiples(a + 1, midpoint, divisor)
            divisor_right += mu * count_multiples(midpoint + 1, b, divisor)

    left_mean = (prime_left - divisor_left) / ell
    right_mean = (prime_right - divisor_right) / right
    moment = rho * (left_mean - right_mean)
    scaled = moment * math.log(x) ** 2 / math.sqrt(x)
    return {
        "cutoff_U_floor": cutoff,
        "scaled_beta_haar": format(scaled, ".15f"),
        "x": x,
    }


def exponent_ledger() -> dict[str, str]:
    u_exponent = Fraction(133, 400)
    rho_exponent = Fraction(1, 2)
    hard_exponent = Fraction(1, 3) + 2 * Fraction(21, 32) - rho_exponent
    main_exponent = Fraction(2, 3) + rho_exponent
    unit_exponent = Fraction(1, 1) + Fraction(1, 3) - rho_exponent
    require(u_exponent - rho_exponent == Fraction(-67, 400), "divisor exponent failed")
    require(hard_exponent == Fraction(55, 48), "boundary exponent failed")
    require(main_exponent == Fraction(7, 6), "main exponent failed")
    require(main_exponent - hard_exponent == Fraction(1, 48), "boundary gap failed")
    require(unit_exponent == Fraction(5, 6), "unit exponent failed")
    return {
        "adjoint_main": "7/6=56/48",
        "boundary_gap": "1/48",
        "divisor_density_remainder": "-67/400",
        "hard_and_jump": "55/48",
        "input_unit": "5/6",
    }


def build_certificate() -> dict[str, Any]:
    marker_count = verify_sources()
    exact_checks = finite_exact_checks()
    observations = [beta_haar_observation(100000), beta_haar_observation(1000000)]
    return {
        "baseline": {
            "head": BASELINE_HEAD,
            "handoff_sha256": SOURCE_HASHES["TPC_HANDOFF.md"],
        },
        "claim": "PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC",
        "constants": {
            "adjoint_main": "9*log(32/27)/(2*sqrt(2))",
            "beta_haar_main": "log(32/27)/sqrt(2)",
            "beta_haar_main_decimal": format(math.log(32.0 / 27.0) / math.sqrt(2.0), ".15f"),
            "weighted_prime_BQ": "9/2",
        },
        "epistemic_status": {
            "finite_exact_checks": "PROVED_EXACT_FINITE_REPRODUCTION",
            "finite_prime_samples": "NUMERICAL_OBSERVATION",
            "theorem": "PROVED_SOURCE_BACKED",
        },
        "exponents": exponent_ledger(),
        "finite_exact_checks": exact_checks,
        "firewall": deepcopy(FIREWALL),
        "numerical_observation": {
            "proof_credit": "NONE",
            "samples": observations,
            "status": "NUMERICAL_OBSERVATION",
            "target_scaled_constant": format(math.log(32.0 / 27.0) / math.sqrt(2.0), ".15f"),
        },
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC256_CERTIFICATE_V1",
        "source_claim_markers": marker_count,
        "source_hashes": deepcopy(SOURCE_HASHES),
    }


def check_result(expected: dict[str, Any]) -> None:
    require(RESULT.is_file(), "certificate JSON is missing")
    raw = RESULT.read_text(encoding="utf-8")
    require(raw == canonical_json(expected), "certificate JSON is not the canonical expected object")
    parsed = json.loads(raw)
    require(parsed == expected, "certificate JSON semantic mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    require(args.check != args.emit, "choose exactly one of --check or --emit")
    expected = build_certificate()
    if args.emit:
        sys.stdout.write(canonical_json(expected))
        return 0
    check_result(expected)
    counts = expected["finite_exact_checks"]
    print(
        "TPC256_CERTIFICATE=PASS "
        f"rank_clocks={counts['rank_clocks']} "
        f"divisor_layers={counts['divisor_layers']} "
        f"unit_mask_terms={counts['unit_mask_terms']} "
        "numerical_samples=2 asymptotic_proof=SOURCE_BACKED"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TPC256_CERTIFICATE=FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
