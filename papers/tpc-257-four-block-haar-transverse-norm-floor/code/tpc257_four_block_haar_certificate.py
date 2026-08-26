#!/usr/bin/env python3
"""Deterministic certificate for the TPC-257 four-block Haar floor.

The executable checks exact finite geometry and provenance.  Its finite beta
values are diagnostic observations; the asymptotic theorem is not inferred
from those samples.
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


BASELINE_HEAD = "e593b6f85ff16c0c8fc99474ba50e74af4a93b51"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results" / "tpc257_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "2d71869341393ad78c627cb84e306f0bfeca730f471f7e37dc4cb2f482dff5f0",
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md":
        "ccb87a64ddb36ed35af415dde2d9fcf0a3ed7f443934edf0a24c98f7bd3ab4da",
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md":
        "cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97",
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md":
        "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16",
    "papers/tpc-256-literal-beta-haar-adjoint-asymptotic/PROOF_PACKAGE.md":
        "cd6c0aecf0f88b3ad1988793998b98e883473b3c25af47244bebf97614e90f4f",
    "papers/tpc-256-literal-beta-haar-adjoint-asymptotic/notes/source_lock.md":
        "d195a076158087d7626e0f1ff1976009ed9c84610160b6d109547689aa1b3dc7",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md":
        "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
    "papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md":
        "a61a7a8f43ef4cbf46a69443b01bd2d4d41cc31a418612ad7a66fd5d54af6446",
}

SOURCE_MARKERS = {
    "AGENTS.md": ("The primary agent owns repository synchronization.",
                   "The primary agent alone stages, commits, rebases, and pushes."),
    "TPC_HANDOFF.md": ("TPC256_MAXIMUM_CLAIM", "TPC256_FULL_GATE_B"),
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md": (
        "TPC-256 estimates", "1/48", "B_Q=sum_",
    ),
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md": (
        "H>2Q", "B_Q=sum_", "child-jump leakage",
    ),
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md": (
        "Coefficient-independent", "rho=sqrt(ell r/N)", "ordered rank",
    ),
    "papers/tpc-256-literal-beta-haar-adjoint-asymptotic/PROOF_PACKAGE.md": (
        "TPC-256 proof package", "Boundary exponents", "Complex phase",
    ),
    "papers/tpc-256-literal-beta-haar-adjoint-asymptotic/notes/source_lock.md": (
        "Frozen release", "Frozen source matrix",
    ),
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md": (
        "(3/2+o(1)) Q^2/log Q", "Weighted-prime aggregation",
    ),
    "papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md": (
        "de la Vallee Poussin", "pi(x) = Li(x)",
    ),
}

FIREWALL = {
    "TPC257_ARITHMETIC_ADVANCE": "YES_SCOPED_TRANSVERSE_LOWER_FLOOR",
    "TPC257_BETA_CONTRASTS": "PROVED_SOURCE_BACKED",
    "TPC257_BOUNDED_VARIATION_ADJOINT": "PROVED_SOURCE_BACKED",
    "TPC257_FIXED_ATOM_CREDIT": 0,
    "TPC257_FULL_GATE_B": "OPEN",
    "TPC257_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC257_FULL_OUTPUT_NORM_FLOOR": "PROVED_SOURCE_BACKED",
    "TPC257_L2": "NONE",
    "TPC257_MAXIMUM_CLAIM":
        "PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT",
    "TPC257_ROUTE_ADVANCE": "YES_SCOPED_TRANSVERSE_HAAR",
    "TPC257_STATUS": "PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR",
    "TPC257_THREE_MODE_HAAR_ORTHOGONALITY": "PROVED_EXACT",
    "TPC257_TRANSVERSE_OUTPUT_FLOOR": "PROVED_SOURCE_BACKED",
    "TPC257_TWIN_PRIME_RESULT": "NONE",
}

ROUND2_CLUE = (
    "USE_THE_EXPLICIT_TWO_DIMENSIONAL_TRANSVERSE_HAAR_FLOOR_TO_SEARCH_FOR_A_"
    "SOURCE_FROZEN_DIAGONAL_NULL_DIRECTION_BEFORE_ATTEMPTING_ANY_FULL_GATE_B_UPPER_BOUND"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"


def frozen_blob(relative_path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{BASELINE_HEAD}:{relative_path}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(proc.returncode == 0 and proc.stderr == b"", f"cannot read frozen source {relative_path}")
    return proc.stdout


def verify_sources() -> int:
    marker_count = 0
    for relative_path, expected_hash in SOURCE_HASHES.items():
        blob = frozen_blob(relative_path)
        require(hashlib.sha256(blob).hexdigest() == expected_hash,
                f"source hash mismatch: {relative_path}")
        text = blob.decode("utf-8")
        for marker in SOURCE_MARKERS[relative_path]:
            require(marker in text, f"source marker missing: {relative_path}: {marker}")
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
    require(ell > 1 and right > 1, "rank clock too short")
    return a, b, n, ell, right, midpoint


def block_data(clock: Fraction) -> dict[str, Any]:
    a, b, n, ell, right, midpoint = rank_data(clock)
    sizes = [ell // 2, ell - ell // 2, right // 2, right - right // 2]
    require(all(size > 0 for size in sizes), "empty four-block child")
    intervals: list[tuple[int, int]] = []
    cursor = a + 1
    for size in sizes:
        intervals.append((cursor, cursor + size - 1))
        cursor += size
    require(cursor == b + 1, "four blocks do not cover the clock")
    return {
        "a": a,
        "b": b,
        "n": n,
        "ell": ell,
        "right": right,
        "midpoint": midpoint,
        "sizes": sizes,
        "intervals": intervals,
    }


def frame_specs(data: dict[str, Any]) -> list[dict[str, Any]]:
    ell = data["ell"]
    right = data["right"]
    s1, s2, s3, s4 = data["sizes"]
    return [
        {
            "rho2": Fraction(ell * right, ell + right),
            "coeff": [Fraction(1, ell), Fraction(1, ell),
                      Fraction(-1, right), Fraction(-1, right)],
            "pair": [0, 1, 2, 3],
        },
        {
            "rho2": Fraction(s1 * s2, s1 + s2),
            "coeff": [Fraction(1, s1), Fraction(-1, s2), Fraction(0), Fraction(0)],
            "pair": [0, 1],
        },
        {
            "rho2": Fraction(s3 * s4, s3 + s4),
            "coeff": [Fraction(0), Fraction(0), Fraction(1, s3), Fraction(-1, s4)],
            "pair": [2, 3],
        },
    ]


def exact_frame_checks(clock: Fraction) -> tuple[int, int, int]:
    data = block_data(clock)
    sizes = data["sizes"]
    specs = frame_specs(data)
    norm_checks = 0
    dot_checks = 0
    variation_checks = 0
    for spec in specs:
        rho2 = spec["rho2"]
        coeff = spec["coeff"]
        norm2 = rho2 * sum((size * value * value for size, value in zip(sizes, coeff)), Fraction(0))
        require(norm2 == 1, "Haar norm identity failed")
        variation_base = sum(
            (abs(left - right) for left, right in zip([Fraction(0)] + coeff, coeff + [Fraction(0)])),
            Fraction(0),
        )
        require(rho2 * variation_base * variation_base == Fraction(4, 1) / rho2,
                "zero-extension variation identity failed")
        for value in coeff:
            require(rho2 * value * value <= Fraction(1, 1) / rho2,
                    "Haar height bound failed")
        norm_checks += 1
        variation_checks += 1

    for left_index in range(3):
        for right_index in range(left_index + 1, 3):
            dot_base = sum(
                (size * left * right for size, left, right in
                 zip(sizes, specs[left_index]["coeff"], specs[right_index]["coeff"])),
                Fraction(0),
            )
            require(dot_base == 0, "Haar orthogonality failed")
            dot_checks += 1
    return norm_checks, dot_checks, variation_checks


def count_multiples(lo: int, hi: int, divisor: int) -> int:
    if lo > hi:
        return 0
    return hi // divisor - (lo - 1) // divisor


def exact_log_vector(value: Fraction) -> dict[int, Fraction]:
    require(value > 0, "log argument must be positive")
    numerator = value.numerator
    denominator = value.denominator
    vector: dict[int, Fraction] = {}

    def factor(number: int, sign: int) -> None:
        divisor = 2
        while divisor * divisor <= number:
            exponent = 0
            while number % divisor == 0:
                number //= divisor
                exponent += 1
            if exponent:
                vector[divisor] = vector.get(divisor, Fraction(0)) + sign * exponent
            divisor += 1
        if number > 1:
            vector[number] = vector.get(number, Fraction(0)) + sign

    factor(numerator, 1)
    factor(denominator, -1)
    return {prime: exponent for prime, exponent in vector.items() if exponent}


def add_log_term(vector: dict[int, Fraction], value: Fraction, coefficient: Fraction) -> None:
    for prime, exponent in exact_log_vector(value).items():
        vector[prime] = vector.get(prime, Fraction(0)) + coefficient * exponent


def interval_log_vector(interval: tuple[Fraction, Fraction]) -> dict[int, Fraction]:
    lo, hi = interval
    vector: dict[int, Fraction] = {}
    add_log_term(vector, hi, hi)
    add_log_term(vector, lo, -lo)
    return vector


def curvature_log_vector(left: tuple[Fraction, Fraction],
                         right: tuple[Fraction, Fraction]) -> dict[int, Fraction]:
    width = left[1] - left[0]
    require(width == right[1] - right[0], "limiting widths differ")
    vector: dict[int, Fraction] = {}
    for prime, value in interval_log_vector(right).items():
        vector[prime] = vector.get(prime, Fraction(0)) + value / width
    for prime, value in interval_log_vector(left).items():
        vector[prime] = vector.get(prime, Fraction(0)) - value / width
    return {prime: value for prime, value in vector.items() if value}


def check_curvature_table() -> int:
    pairs = [
        ((Fraction(1, 2), Fraction(3, 4)), (Fraction(3, 4), Fraction(1)), Fraction(32, 27)),
        ((Fraction(1, 2), Fraction(5, 8)), (Fraction(5, 8), Fraction(3, 4)), Fraction(3456, 3125)),
        ((Fraction(3, 4), Fraction(7, 8)), (Fraction(7, 8), Fraction(1)), Fraction(884736, 823543)),
    ]
    for left, right, ratio in pairs:
        observed = curvature_log_vector(left, right)
        expected = {prime: 2 * value for prime, value in exact_log_vector(ratio).items()}
        require(observed == expected, "curvature logarithm vector failed")
        require(ratio > 1, "curvature constant is not positive")
    return len(pairs)


def finite_exact_checks() -> dict[str, int]:
    clocks = [Fraction(80 + 3 * index, 1) for index in range(32)]
    clocks += [Fraction(323 + 12 * index + (2 * (index % 5) + 1), 4)
               for index in range(32)]
    rank_checks = 0
    frame_norm_checks = 0
    orthogonality_checks = 0
    variation_checks = 0
    divisor_layers = 0
    boundary_checks = 0
    for clock in clocks:
        data = block_data(clock)
        require(data["ell"] + data["right"] == data["n"], "rank sum failed")
        norms, dots, variations = exact_frame_checks(clock)
        rank_checks += 1
        frame_norm_checks += norms
        orthogonality_checks += dots
        variation_checks += variations
        for lo, hi in data["intervals"]:
            length = hi - lo + 1
            for divisor in range(1, 25):
                discrepancy = abs(Fraction(count_multiples(lo, hi, divisor), 1)
                                  - Fraction(length, divisor))
                require(discrepancy <= 1, "divisor endpoint discrepancy failed")
                divisor_layers += 1
        lo, hi = data["a"] + 1, data["b"]
        boundaries = [data["a"], data["midpoint"], data["b"]]
        for shift in range(-96, 97):
            for boundary in boundaries:
                crossing = sum(
                    1 for source in range(lo, hi + 1)
                    if (source <= boundary) != (source + shift <= boundary)
                )
                require(crossing <= abs(shift), "step crossing bound failed")
                boundary_checks += 1
    curvature_pairs = check_curvature_table()
    require(len(clocks) == 64, "clock count failed")
    return {
        "boundary_checks": boundary_checks,
        "clock_count": len(clocks),
        "curvature_pairs": curvature_pairs,
        "divisor_layers": divisor_layers,
        "frame_norm_checks": frame_norm_checks,
        "orthogonality_checks": orthogonality_checks,
        "rank_checks": rank_checks,
        "variation_checks": variation_checks,
    }


def prime_sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for value in range(2, math.isqrt(limit) + 1):
        if flags[value]:
            first = value * value
            count = (limit - first) // value + 1
            flags[first : limit + 1 : value] = b"\x00" * count
    return [value for value in range(2, limit + 1) if flags[value]]


def mobius_value(value: int) -> int:
    remaining = value
    parity = 0
    divisor = 2
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent >= 2:
            return 0
        parity += exponent
        divisor += 1
    if remaining > 1:
        parity += 1
    return -1 if parity % 2 else 1


def block_index(intervals: list[tuple[int, int]], value: int) -> int | None:
    for index, (lo, hi) in enumerate(intervals):
        if lo <= value <= hi:
            return index
    return None


def beta_frame_observation(clock: int) -> dict[str, Any]:
    data = block_data(Fraction(clock, 1))
    intervals = data["intervals"]
    beta_sums = [0.0, 0.0, 0.0, 0.0]
    for prime in prime_sieve(data["b"]):
        power = prime
        exponent = 1
        while power <= data["b"]:
            index = block_index(intervals, power)
            if index is not None:
                beta_sums[index] += 1.0 / exponent
            if power > data["b"] // prime:
                break
            power *= prime
            exponent += 1

    cutoff = int(math.floor(clock ** (133.0 / 400.0)))
    for divisor in range(1, cutoff + 1):
        value = mobius_value(divisor)
        if value == 0:
            continue
        for index, (lo, hi) in enumerate(intervals):
            beta_sums[index] -= value * count_multiples(lo, hi, divisor)

    s1, s2, s3, s4 = data["sizes"]
    means = [total / size for total, size in zip(beta_sums, (s1, s2, s3, s4))]
    pairs = [
        (s1 + s2, s3 + s4, (s1 * means[0] + s2 * means[1]) / (s1 + s2),
         (s3 * means[2] + s4 * means[3]) / (s3 + s4),
         data["ell"] * data["right"] / data["n"]),
        (s1, s2, means[0], means[1], s1 * s2 / (s1 + s2)),
        (s3, s4, means[2], means[3], s3 * s4 / (s3 + s4)),
    ]
    scaled: list[str] = []
    for _, _, left_mean, right_mean, rho2 in pairs:
        moment = math.sqrt(rho2) * (left_mean - right_mean)
        scaled.append(format(moment * math.log(clock) ** 2 / math.sqrt(clock), ".15f"))
    return {
        "cutoff_U_floor": cutoff,
        "scaled_beta_haar": scaled,
        "x": clock,
    }


def exponent_ledger() -> dict[str, str]:
    divisor = Fraction(133, 400) - Fraction(1, 2)
    boundary = Fraction(1, 3) + 2 * Fraction(21, 32) - Fraction(1, 2)
    main = Fraction(2, 3) + Fraction(1, 2)
    unit = Fraction(1, 1) + Fraction(1, 3) - Fraction(1, 2)
    require(divisor == Fraction(-67, 400), "divisor exponent failed")
    require(boundary == Fraction(55, 48), "boundary exponent failed")
    require(main == Fraction(7, 6), "main exponent failed")
    require(unit == Fraction(5, 6), "unit exponent failed")
    require(main - boundary == Fraction(1, 48), "boundary gap failed")
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
    observations = [beta_frame_observation(100000), beta_frame_observation(1000000)]
    kappas = [
        math.log(32.0 / 27.0) / math.sqrt(2.0),
        math.log(3456.0 / 3125.0) / 2.0,
        math.log(884736.0 / 823543.0) / 2.0,
    ]
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": len(SOURCE_HASHES)},
        "claim": FIREWALL["TPC257_MAXIMUM_CLAIM"],
        "constants": {
            "kappa0": "log(32/27)/sqrt(2)",
            "kappa1": "log(3456/3125)/2",
            "kappa2": "log(884736/823543)/2",
            "three_mode_factor": "sqrt(kappa0^2+kappa1^2+kappa2^2)",
            "transverse_factor": "sqrt(kappa1^2+kappa2^2)",
            "kappa_decimals": [format(value, ".15f") for value in kappas],
            "three_mode_factor_decimal": format(math.sqrt(sum(value * value for value in kappas)), ".15f"),
            "transverse_factor_decimal": format(math.sqrt(sum(value * value for value in kappas[1:])), ".15f"),
            "weighted_prime_BQ": "9/2",
        },
        "epistemic_status": {
            "finite_exact_checks": "PROVED_EXACT_FINITE_REPRODUCTION",
            "finite_beta_samples": "NUMERICAL_OBSERVATION",
            "theorem": "PROVED_SOURCE_BACKED",
        },
        "exponents": exponent_ledger(),
        "finite_exact_checks": exact_checks,
        "firewall": deepcopy(FIREWALL),
        "numerical_observation": {
            "proof_credit": "NONE",
            "samples": observations,
            "status": "NUMERICAL_OBSERVATION",
        },
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC257_CERTIFICATE_V1",
        "source_claim_markers": marker_count,
        "source_hashes": deepcopy(SOURCE_HASHES),
    }


def check_result(expected: dict[str, Any]) -> None:
    require(RESULT.is_file(), "certificate JSON is missing")
    raw = RESULT.read_text(encoding="utf-8")
    require(raw == canonical_json(expected), "certificate JSON is not canonical expected object")
    require(json.loads(raw) == expected, "certificate JSON semantic mismatch")


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
        "TPC257_CERTIFICATE=PASS "
        f"clocks={counts['clock_count']} "
        f"frame_norms={counts['frame_norm_checks']} "
        f"orthogonality={counts['orthogonality_checks']} "
        f"divisor_layers={counts['divisor_layers']} "
        "numerical_samples=2 asymptotic_proof=SOURCE_BACKED"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TPC257_CERTIFICATE=FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
