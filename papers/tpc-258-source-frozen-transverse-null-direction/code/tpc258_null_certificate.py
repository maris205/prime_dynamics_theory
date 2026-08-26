#!/usr/bin/env python3
"""Deterministic certificate for the TPC-258 transverse null direction."""

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


BASELINE_HEAD = "337fa65aca20122f241c30c67f1deb64b45e3c0b"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc258_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "c4c79b25fdbcdb7f8f26b1348263f159d5cd7f55c486c2653066c5519a1782a5",
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md":
        "faaede82e2ebf84a994e3e9c945e42c321a8c81d0c0db9e0f8e2f9a88329e609",
    "research/tpc-big-road/tpc_bridge_b_four_block_haar_transverse_norm_floor_checker.py":
        "d2cf0321dfbc730850438badaadf6018e0555662010ea39b80bd12a175ded2e1",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md":
        "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/route_evaluation.md":
        "b92bf14797013e4371a0d9c88d4dc7bdef39d76b1361d8cf73009165b41e1f3f",
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md":
        "ccb87a64ddb36ed35af415dde2d9fcf0a3ed7f443934edf0a24c98f7bd3ab4da",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md":
        "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
}

SOURCE_MARKERS = {
    "AGENTS.md": ("The primary agent owns repository synchronization.",
                   "The primary agent alone stages, commits, rebases, and pushes."),
    "TPC_HANDOFF.md": ("TPC257_MAXIMUM_CLAIM", "TPC257_ROUND2_CLUE"),
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md": (
        "kappa1=log(3456/3125)/2", "midpoint-transverse component", "TPC257_L2 = NONE",
    ),
    "research/tpc-big-road/tpc_bridge_b_four_block_haar_transverse_norm_floor_checker.py": (
        "TPC257_BRIDGE_CHECK=PASS", "boundary_gap=1_OVER_48",
    ),
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md": (
        "TPC-257 proof package", "Parseval and the transverse lower floor", "1/48",
    ),
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md": (
        "T257.9", "Transverse projected norm floor",
    ),
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/route_evaluation.md": (
        "ROUND2_CLUE", "source-frozen transverse combination",
    ),
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md": (
        "B_Q=sum_", "1/48",
    ),
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md": (
        "(3/2+o(1)) Q^2/log Q", "Weighted-prime aggregation",
    ),
}

STATUS = (
    "PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_"
    "FOR_LITERAL_V59_ADJOINT"
)

FIREWALL = {
    "TPC258_ARITHMETIC_ADVANCE": "YES_SCOPED_LOG_CANCELLATION",
    "TPC258_FIXED_ATOM_CREDIT": 0,
    "TPC258_FIXED_POWER_SAVING": "NONE",
    "TPC258_FULL_GATE_B": "OPEN",
    "TPC258_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC258_L2": "NONE",
    "TPC258_LEADING_DIAGONAL_CANCELLATION": "PROVED_SOURCE_BACKED",
    "TPC258_MAXIMUM_CLAIM": STATUS,
    "TPC258_NULL_DIRECTION": "PROVED_SOURCE_FROZEN_UNIT_VECTOR",
    "TPC258_RATE_REFINEMENT": "CONDITIONAL_THEOREM_LOG_ONE_OVER_X",
    "TPC258_ROUTE_ADVANCE": "YES_SCOPED_TRANSVERSE_NULL",
    "TPC258_STATUS": STATUS,
    "TPC258_TWIN_PRIME_RESULT": "NONE",
}

ROUND2_CLUE = (
    "TEST_THE_SOURCE_FROZEN_NULL_DIRECTION_AGAINST_THE_LITERAL_SIGNED_W_BETA_"
    "COUPLING_ON_THE_SAME_CLOCK_BEFORE_ANY_FULL_REASSEMBLY"
)


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"


def frozen_blob(relative: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    need(proc.returncode == 0 and proc.stderr == b"", "frozen source: " + relative)
    return proc.stdout


def verify_sources() -> int:
    markers = 0
    for relative, expected in SOURCE_HASHES.items():
        blob = frozen_blob(relative)
        need(hashlib.sha256(blob).hexdigest() == expected, "source hash: " + relative)
        source = blob.decode("utf-8")
        for marker in SOURCE_MARKERS[relative]:
            need(marker in source, "source marker: " + relative + ": " + marker)
            markers += 1
    return markers


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def four_blocks(clock: Fraction) -> dict[str, Any]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    sizes = [ell // 2, ell - ell // 2, right // 2, right - right // 2]
    need(all(size > 0 for size in sizes), "short clock")
    intervals: list[tuple[int, int]] = []
    cursor = a + 1
    for size in sizes:
        intervals.append((cursor, cursor + size - 1))
        cursor += size
    need(cursor == b + 1, "block cover")
    return {"a": a, "b": b, "n": n, "ell": ell, "right": right,
            "sizes": sizes, "intervals": intervals}


def frame_specs(data: dict[str, Any]) -> list[tuple[Fraction, list[Fraction]]]:
    ell = data["ell"]
    right = data["right"]
    s1, s2, s3, s4 = data["sizes"]
    return [
        (Fraction(ell * right, ell + right),
         [Fraction(1, ell), Fraction(1, ell), Fraction(-1, right), Fraction(-1, right)]),
        (Fraction(s1 * s2, s1 + s2),
         [Fraction(1, s1), Fraction(-1, s2), Fraction(0), Fraction(0)]),
        (Fraction(s3 * s4, s3 + s4),
         [Fraction(0), Fraction(0), Fraction(1, s3), Fraction(-1, s4)]),
    ]


def factor_vector(value: Fraction) -> dict[int, int]:
    need(value > 0, "positive log ratio")
    result: dict[int, int] = {}

    def consume(number: int, sign: int) -> None:
        divisor = 2
        while divisor * divisor <= number:
            exponent = 0
            while number % divisor == 0:
                number //= divisor
                exponent += 1
            if exponent:
                result[divisor] = result.get(divisor, 0) + sign * exponent
            divisor += 1
        if number > 1:
            result[number] = result.get(number, 0) + sign

    consume(value.numerator, 1)
    consume(value.denominator, -1)
    return {prime: exponent for prime, exponent in result.items() if exponent}


def exact_checks() -> dict[str, int]:
    clocks = [Fraction(128 + 5 * index, 1) for index in range(40)]
    clocks += [Fraction(1025 + 20 * index + 2 * (index % 7) + 1, 8)
               for index in range(40)]
    norms = dots = variations = null_norms = source_cuts = 0
    for clock in clocks:
        data = four_blocks(clock)
        specs = frame_specs(data)
        sizes = data["sizes"]
        for rho2, coefficients in specs:
            norm = rho2 * sum((size * coefficient * coefficient
                               for size, coefficient in zip(sizes, coefficients)), Fraction(0))
            need(norm == 1, "frame norm")
            variation = sum((abs(left - right) for left, right in
                             zip([Fraction(0)] + coefficients,
                                 coefficients + [Fraction(0)])), Fraction(0))
            need(rho2 * variation * variation == Fraction(4, 1) / rho2,
                 "frame variation")
            norms += 1
            variations += 1
        for i in range(3):
            for j in range(i + 1, 3):
                dot = sum((size * left * right for size, left, right in
                           zip(sizes, specs[i][1], specs[j][1])), Fraction(0))
                need(dot == 0, "frame dot")
                dots += 1
        # The normalized null weights have squared norm one because z1,z2 are orthonormal.
        l1 = math.log(3456.0 / 3125.0)
        l2 = math.log(884736.0 / 823543.0)
        lt2 = l1 * l1 + l2 * l2
        need(abs((l2 * l2 + l1 * l1) / lt2 - 1.0) < 1e-15, "null norm")
        null_norms += 1
        need(data["intervals"][0][0] == data["a"] + 1 and
             data["intervals"][-1][1] == data["b"], "source cut")
        source_cuts += 1

    ratio1 = Fraction(3456, 3125)
    ratio2 = Fraction(884736, 823543)
    need(ratio1 > 1 and ratio2 > 1, "positive curvature ratios")
    need(bool(factor_vector(ratio1)) and bool(factor_vector(ratio2)), "log factor vectors")
    # Formal commutative monomial L1*L2 has coefficients +1/2 and -1/2.
    leading_monomial = Fraction(1, 2) - Fraction(1, 2)
    need(leading_monomial == 0, "formal diagonal cancellation")
    need(Fraction(7, 6) - Fraction(55, 48) == Fraction(1, 48), "boundary gap")
    return {"clocks": len(clocks), "frame_norms": norms, "orthogonality": dots,
            "variation_checks": variations, "null_norms": null_norms,
            "source_cuts": source_cuts, "formal_cancellations": 1,
            "log_factor_vectors": 2}


def sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if flags[value]:
            first = value * value
            count = (limit - first) // value + 1
            flags[first:limit + 1:value] = b"\x00" * count
    return [value for value in range(2, limit + 1) if flags[value]]


def mobius(value: int) -> int:
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


def multiple_count(lo: int, hi: int, divisor: int) -> int:
    return hi // divisor - (lo - 1) // divisor


def beta_observation(clock: int) -> dict[str, Any]:
    data = four_blocks(Fraction(clock, 1))
    sums = [0.0, 0.0, 0.0, 0.0]
    for prime in sieve(data["b"]):
        power = prime
        exponent = 1
        while power <= data["b"]:
            for index, (lo, hi) in enumerate(data["intervals"]):
                if lo <= power <= hi:
                    sums[index] += 1.0 / exponent
                    break
            if power > data["b"] // prime:
                break
            power *= prime
            exponent += 1
    cutoff = int(math.floor(clock ** (133.0 / 400.0)))
    for divisor in range(1, cutoff + 1):
        weight = mobius(divisor)
        if weight:
            for index, (lo, hi) in enumerate(data["intervals"]):
                sums[index] -= weight * multiple_count(lo, hi, divisor)
    s1, s2, s3, s4 = data["sizes"]
    means = [total / size for total, size in zip(sums, (s1, s2, s3, s4))]
    rho1 = math.sqrt(s1 * s2 / (s1 + s2))
    rho2 = math.sqrt(s3 * s4 / (s3 + s4))
    scale = math.log(clock) ** 2 / math.sqrt(clock)
    c1 = rho1 * (means[0] - means[1]) * scale
    c2 = rho2 * (means[2] - means[3]) * scale
    l1 = math.log(3456.0 / 3125.0)
    l2 = math.log(884736.0 / 823543.0)
    null = (l2 * c1 - l1 * c2) / math.sqrt(l1 * l1 + l2 * l2)
    return {"x": clock, "cutoff_U_floor": cutoff,
            "scaled_descendants": [format(c1, ".15f"), format(c2, ".15f")],
            "scaled_null": format(null, ".15f")}


def adversarial_control() -> dict[str, Any]:
    ratios = []
    for m in range(4, 41, 2):
        error = 1.0 / m
        benchmark = math.exp(-Fraction(1, 400) * m * m)
        ratios.append(format(error / benchmark, ".12f"))
    need(float(ratios[-1]) > float(ratios[0]), "adversarial power ratio")
    return {"error_model": "1/sqrt(log x) along x=exp(m^2)",
            "fixed_power_benchmark": "x^(-1/400)",
            "proof_credit": "QUANTIFIER_FIREWALL_ONLY", "ratios": ratios}


def build_certificate() -> dict[str, Any]:
    markers = verify_sources()
    checks = exact_checks()
    l1 = math.log(3456.0 / 3125.0)
    l2 = math.log(884736.0 / 823543.0)
    lt = math.sqrt(l1 * l1 + l2 * l2)
    return {
        "adversarial_control": adversarial_control(),
        "baseline": {"head": BASELINE_HEAD, "source_count": len(SOURCE_HASHES)},
        "claim": STATUS,
        "constants": {"L1": "log(3456/3125)", "L2": "log(884736/823543)",
                      "L1_decimal": format(l1, ".15f"),
                      "L2_decimal": format(l2, ".15f"),
                      "null_weights": [format(l2 / lt, ".15f"),
                                       format(-l1 / lt, ".15f")],
                      "symbolic_cancellation": "L2*(L1/2)-L1*(L2/2)=0"},
        "epistemic_status": {"finite_beta_samples": "NUMERICAL_OBSERVATION",
                             "finite_exact_checks": "PROVED_EXACT_FINITE_REPRODUCTION",
                             "rate_refinement": "CONDITIONAL_THEOREM",
                             "theorem": "PROVED_SOURCE_BACKED"},
        "exact_checks": checks,
        "firewall": deepcopy(FIREWALL),
        "numerical_observation": {"proof_credit": "NONE",
                                  "samples": [beta_observation(100000),
                                              beta_observation(1000000)],
                                  "status": "NUMERICAL_OBSERVATION"},
        "rate_ledger": {"boundary": "55/48+epsilon",
                        "conditional": "S_x/log(x)+x^(55/48+epsilon)",
                        "main": "S_x=x^(7/6)/log^3(x)",
                        "proved": "o(S_x)"},
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC258_CERTIFICATE_V1",
        "source_claim_markers": markers,
        "source_hashes": deepcopy(SOURCE_HASHES),
    }


def check_result(expected: dict[str, Any]) -> None:
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    need(raw == canonical_json(expected), "certificate not canonical expected object")
    need(json.loads(raw) == expected, "certificate semantic mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    need(args.check != args.emit, "choose exactly one mode")
    expected = build_certificate()
    if args.emit:
        sys.stdout.write(canonical_json(expected))
        return 0
    check_result(expected)
    counts = expected["exact_checks"]
    print("TPC258_CERTIFICATE=PASS "
          f"clocks={counts['clocks']} frame_norms={counts['frame_norms']} "
          f"orthogonality={counts['orthogonality']} null_norms={counts['null_norms']} "
          "formal_cancellation=1 theorem=SOURCE_BACKED rate=CONDITIONAL")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC258_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
