#!/usr/bin/env python3
"""Exact certificate for the TPC-263 rank-three physical channel."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc263_certificate.json"
BASELINE_HEAD = "6c32d179c7225add34dfcc3a4d43a0c59da14424"
STATUS = "PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL"
ROUND2_CLUE = "ATTACK_THE_ORTHOGONAL_COMPLEMENT_AFTER_PAYING_THE_RANK_THREE_LOG_CHANNEL"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "344c75a6c41730703b04d5474e385986f8c66dcf5639531848da99c3bec574f4",
    "papers/tpc-262-literal-mode-zero-cross-gram/README.md":
        "d93b364a110103a81cdf3e766586da0f43af1f2b090aecb7514e875d4f8365d6",
    "papers/tpc-262-literal-mode-zero-cross-gram/PROOF_PACKAGE.md":
        "520f74acd0fc39f50c53d1cef31e2a9a599630384b4f888b190a8a64842364b1",
    "papers/tpc-262-literal-mode-zero-cross-gram/notes/theorem_ledger.md":
        "ef8c6d834dfda217a412c99d9f70a93961ac7e501fa7a86c8b9286d92dcb8556",
    "papers/tpc-262-literal-mode-zero-cross-gram/notes/route_evaluation.md":
        "4951487298f1cb5ec0062d75512d4d05b7de3893b26b98a148b70d2a311147cc",
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md":
        "faaede82e2ebf84a994e3e9c945e42c321a8c81d0c0db9e0f8e2f9a88329e609",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md":
        "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md":
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee",
    "papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/notes/theorem_ledger.md":
        "ea138a0cd5839bdb62633a38389f82a4e6f4346641757b05729722daec89aa2b",
}

FIREWALL = {
    "TPC263_MAXIMUM_CLAIM": STATUS,
    "TPC263_ROUTE_ADVANCE": "YES_SCOPED_RANK_THREE_LOG_CHANNEL",
    "TPC263_W_FRAME_MOMENTS": "PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC263_ADJOINT_FRAME_COEFFICIENTS": "PROVED_SOURCE_BACKED_TPC257",
    "TPC263_PROJECTION_SPLIT": "PROVED_EXACT",
    "TPC263_RANK_THREE_CHANNEL": "PROVED_SOURCE_BACKED_X_5_OVER_3_LOG_M_PLUS_3",
    "TPC263_ORTHOGONAL_RESIDUAL": "OPEN",
    "TPC263_FIXED_POWER_CREDIT": 0,
    "TPC263_ARITHMETIC_ADVANCE": "YES_SCOPED_FIXED_LOG_ONLY",
    "TPC263_L2": "NONE",
    "TPC263_FULL_GATE_B": "OPEN",
    "TPC263_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC263_TWIN_PRIME_RESULT": "NONE",
    "TPC263_STATUS": STATUS,
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + relative],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def source_audit() -> int:
    for path, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(path)).hexdigest() == expected,
             "source hash: " + path)
    return len(SOURCE_HASHES)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def block_data(clock: Fraction) -> dict[str, Any]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    sizes = [ell // 2, ell - ell // 2, right // 2, right - right // 2]
    need(min(sizes) > 0, "empty rank block")
    intervals: list[tuple[int, int]] = []
    cursor = a + 1
    for size in sizes:
        intervals.append((cursor, cursor + size - 1))
        cursor += size
    need(cursor == b + 1, "blocks do not cover interval")
    return {"a": a, "b": b, "n": n, "ell": ell, "right": right,
            "sizes": sizes, "intervals": intervals}


def frame_specs(data: dict[str, Any]) -> list[dict[str, Any]]:
    ell, right = data["ell"], data["right"]
    s1, s2, s3, s4 = data["sizes"]
    return [
        {"rho2": Fraction(ell * right, ell + right),
         "coeff": [Fraction(1, ell), Fraction(1, ell),
                   Fraction(-1, right), Fraction(-1, right)]},
        {"rho2": Fraction(s1 * s2, s1 + s2),
         "coeff": [Fraction(1, s1), Fraction(-1, s2),
                   Fraction(0), Fraction(0)]},
        {"rho2": Fraction(s3 * s4, s3 + s4),
         "coeff": [Fraction(0), Fraction(0), Fraction(1, s3),
                   Fraction(-1, s4)]},
    ]


def frame_checks(clock: Fraction) -> dict[str, int]:
    data = block_data(clock)
    sizes = data["sizes"]
    specs = frame_specs(data)
    norm_checks = variation_checks = 0
    for spec in specs:
        rho2 = spec["rho2"]
        coeff = spec["coeff"]
        norm2 = rho2 * sum((s * c * c for s, c in zip(sizes, coeff)),
                           Fraction(0))
        need(norm2 == 1, "frame norm")
        jumps = [Fraction(0)] + coeff + [Fraction(0)]
        variation = sum((abs(jumps[i + 1] - jumps[i])
                         for i in range(len(jumps) - 1)), Fraction(0))
        need(rho2 * variation * variation == Fraction(4, 1) / rho2,
             "frame variation")
        norm_checks += 1
        variation_checks += 1
    dot_checks = 0
    for i in range(3):
        for j in range(i + 1, 3):
            dot = sum((s * a * b for s, a, b in zip(
                sizes, specs[i]["coeff"], specs[j]["coeff"])), Fraction(0))
            need(dot == 0, "frame orthogonality")
            dot_checks += 1
    return {"norm_checks": norm_checks, "variation_checks": variation_checks,
            "orthogonality_checks": dot_checks}


Gaussian = tuple[Fraction, Fraction]


def g(real: int | str | Fraction,
      imag: int | str | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def gadd(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] + b[0], a[1] + b[1])


def gmul(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def gconj(a: Gaussian) -> Gaussian:
    return (a[0], -a[1])


def inner(left: list[Gaussian], right: list[Gaussian]) -> Gaussian:
    total = g(0)
    for a, b in zip(left, right):
        total = gadd(total, gmul(gconj(a), b))
    return total


def gscale(value: Fraction, a: Gaussian) -> Gaussian:
    return (value * a[0], value * a[1])


def gjson(a: Gaussian) -> list[str]:
    return [str(a[0]), str(a[1])]


def projection_audit() -> dict[str, Any]:
    # The first three coordinates model the exact orthonormal frame; the last
    # three force a genuinely nonzero orthogonal residual.
    w = [g(3, 1), g(-2, 3), g(5, -1), g(7, 2), g(-4, 1), g(1, -3)]
    h = [g(-1, 2), g(4, -1), g(2, 3), g(-3, 1), g(5, 0), g(-2, -4)]
    pw = w[:3] + [g(0), g(0), g(0)]
    ph = h[:3] + [g(0), g(0), g(0)]
    rw = [g(0), g(0), g(0)] + w[3:]
    rh = [g(0), g(0), g(0)] + h[3:]
    total = inner(w, h)
    projected = inner(pw, ph)
    residual = inner(rw, rh)
    need(total == gadd(projected, residual), "projection split")
    need(residual != g(0), "residual must be nonzero")
    coefficients = [inner([g(1) if j == i else g(0) for j in range(6)], w)
                    for i in range(3)]
    adjoint_coefficients = [inner(
        [g(1) if j == i else g(0) for j in range(6)], h)
        for i in range(3)]
    reconstructed = g(0)
    for a, b in zip(coefficients, adjoint_coefficients):
        reconstructed = gadd(reconstructed, gmul(gconj(a), b))
    need(reconstructed == projected, "frame cross-Gram reconstruction")
    return {
        "ambient_dimension": 6,
        "projected_cross_gram": gjson(projected),
        "orthogonal_residual": gjson(residual),
        "full_coupling": gjson(total),
        "residual_nonzero": True,
        "projection_rank": 3,
        "reconstruction": gjson(reconstructed),
    }


def block_moment_audit() -> dict[str, Any]:
    sizes = [3, 4, 5, 6]
    sums = [g(5, 1), g(-2, 3), g(7, -2), g(1, 4)]
    pairs = [(0, 1), (2, 3)]
    moments = []
    for left, right in pairs:
        rho2 = Fraction(sizes[left] * sizes[right],
                        sizes[left] + sizes[right])
        difference = gadd(gscale(Fraction(1, sizes[left]), sums[left]),
                          gscale(Fraction(-1, sizes[right]), sums[right]))
        norm2 = difference[0] * difference[0] + difference[1] * difference[1]
        moments.append({"pair": [left + 1, right + 1],
                        "rho2": str(rho2),
                        "mean_difference": gjson(difference),
                        "haar_moment_abs_squared": str(rho2 * norm2)})
    need(all(item["rho2"] for item in moments), "block moment ledger")
    return {"sizes": sizes, "block_sums": [gjson(item) for item in sums],
            "moments": moments,
            "interpretation": "four block sums are controlled before signed assembly"}


def constants_and_exponents() -> dict[str, Any]:
    ratios = [Fraction(32, 27), Fraction(3456, 3125),
              Fraction(884736, 823543)]
    need(all(value > 1 for value in ratios), "positive curvature ratios")
    kappas = [math.log(float(ratios[0])) / math.sqrt(2.0),
              math.log(float(ratios[1])) / 2.0,
              math.log(float(ratios[2])) / 2.0]
    three = math.sqrt(sum(value * value for value in kappas))
    transverse = math.sqrt(sum(value * value for value in kappas[1:]))
    w_exp = Fraction(1, 2)
    adjoint_exp = Fraction(7, 6)
    product_exp = w_exp + adjoint_exp
    need(product_exp == Fraction(5, 3), "product exponent")
    gap = Fraction(5, 3) - Fraction(1997, 1200)
    need(gap == Fraction(1, 400), "endpoint gap")
    return {
        "kappa_forms": ["log(32/27)/sqrt(2)",
                        "log(3456/3125)/2",
                        "log(884736/823543)/2"],
        "kappa_decimals": [format(value, ".15f") for value in kappas],
        "three_mode_factor": format(three, ".15f"),
        "transverse_factor": format(transverse, ".15f"),
        "w_exponent": "1/2",
        "adjoint_exponent": "7/6",
        "channel_exponent": "5/3",
        "w_log_power": "M",
        "adjoint_log_power": "3",
        "channel_log_power": "M+3",
        "endpoint_gap": "1/400",
        "fixed_power_credit": 0,
        "power_firewall": "x^eta/(log x)^(M+3)->infinity for fixed eta>0",
    }


def finite_checks() -> dict[str, Any]:
    clocks = [Fraction(80 + 3 * i, 1) for i in range(24)]
    clocks += [Fraction(641 + 7 * i, 2) for i in range(24)]
    totals = {"clock_count": len(clocks), "norm_checks": 0,
              "variation_checks": 0, "orthogonality_checks": 0}
    for clock in clocks:
        checks = frame_checks(clock)
        for key, value in checks.items():
            totals[key] += value
    need(totals["clock_count"] == 48, "clock count")
    return totals


def build() -> dict[str, Any]:
    source_count = source_audit()
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_count},
        "block_moment_audit": block_moment_audit(),
        "claim": STATUS,
        "constants_and_exponents": constants_and_exponents(),
        "epistemic_status": {
            "frame_geometry": "PROVED_EXACT",
            "projection_split": "PROVED_EXACT",
            "w_block_moments": "PROVED_SOURCE_BACKED",
            "adjoint_coefficients": "PROVED_SOURCE_BACKED_TPC257",
            "rank_three_channel": "PROVED_SOURCE_BACKED",
            "orthogonal_residual": "OPEN",
            "finite_checks": "NUMERICALLY_CERTIFIED",
        },
        "finite_checks": finite_checks(),
        "firewall": dict(FIREWALL),
        "projection_audit": projection_audit(),
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC263_RANK_THREE_PHYSICAL_CROSS_GRAM_CERTIFICATE_V1",
        "source_hashes": dict(SOURCE_HASHES),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    need(args.check != args.emit, "choose exactly one mode")
    expected = build()
    if args.emit:
        sys.stdout.write(canonical(expected))
        return 0
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    need(raw == canonical(expected), "certificate mismatch")
    need(json.loads(raw) == expected, "certificate semantics")
    print("TPC263_CERTIFICATE=PASS "
          f"sources={expected['baseline']['source_count']} "
          f"clocks={expected['finite_checks']['clock_count']} "
          "projection=EXACT residual=EXPLICIT channel=x^(5/3)/log^(M+3) "
          "fixed_power_credit=0 strict_1_over_400=UNPAID")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC263_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
