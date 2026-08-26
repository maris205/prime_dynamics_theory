#!/usr/bin/env python3
"""Independent semantic checker for TPC-257.

The producer is intentionally not imported.  The finite frame and sample
calculations are reconstructed here, followed by deterministic mutation tests.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "e593b6f85ff16c0c8fc99474ba50e74af4a93b51"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc257_certificate.json"
BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}
EXPECTED_FILES = {
    ".gitignore", "DERIVATION_PACKAGE.md", "PAPER_PLAN.md", "PROOF_PACKAGE.md",
    "README.md", "code/tpc257_four_block_haar_certificate.py",
    "experiments/tpc257_four_block_haar_stress.py",
    "experiments/tpc257_independent_checker.py",
    "notes/citation_verification.md", "notes/claim_firewall.md",
    "notes/computational_protocol.md", "notes/route_evaluation.md",
    "notes/source_lock.md", "notes/theorem_ledger.md", "paper/main.tex",
    "paper/paper.pdf", "paper/references.bib", "results/tpc257_certificate.json",
}

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


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", f"{BASELINE_HEAD}:{path}"], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", f"frozen source: {path}")
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(path)).hexdigest() == expected, f"source hash: {path}")


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def blocks(clock: Fraction) -> dict[str, Any]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    need(ell > 1 and right > 1, "short clock")
    sizes = [ell // 2, ell - ell // 2, right // 2, right - right // 2]
    need(min(sizes) > 0, "empty block")
    intervals = []
    cursor = a + 1
    for size in sizes:
        intervals.append((cursor, cursor + size - 1))
        cursor += size
    need(cursor == b + 1, "block cover")
    return {"a": a, "b": b, "n": n, "ell": ell, "right": right,
            "midpoint": a + ell, "sizes": sizes, "intervals": intervals}


def specs(data: dict[str, Any]) -> list[tuple[Fraction, list[Fraction]]]:
    ell, right = data["ell"], data["right"]
    s1, s2, s3, s4 = data["sizes"]
    return [
        (Fraction(ell * right, ell + right),
         [Fraction(1, ell), Fraction(1, ell), Fraction(-1, right), Fraction(-1, right)]),
        (Fraction(s1 * s2, s1 + s2),
         [Fraction(1, s1), Fraction(-1, s2), Fraction(0), Fraction(0)]),
        (Fraction(s3 * s4, s3 + s4),
         [Fraction(0), Fraction(0), Fraction(1, s3), Fraction(-1, s4)]),
    ]


def factor(value: int) -> dict[int, int]:
    result: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        exponent = 0
        while value % divisor == 0:
            value //= divisor
            exponent += 1
        if exponent:
            result[divisor] = result.get(divisor, 0) + exponent
        divisor += 1
    if value > 1:
        result[value] = result.get(value, 0) + 1
    return result


def log_vector(value: Fraction) -> dict[int, Fraction]:
    need(value > 0, "nonpositive log")
    result = {prime: Fraction(exponent) for prime, exponent in factor(value.numerator).items()}
    for prime, exponent in factor(value.denominator).items():
        result[prime] = result.get(prime, Fraction(0)) - exponent
    return {prime: exponent for prime, exponent in result.items() if exponent}


def interval_vector(interval: tuple[Fraction, Fraction]) -> dict[int, Fraction]:
    lo, hi = interval
    result: dict[int, Fraction] = {}
    for prime, exponent in log_vector(hi).items():
        result[prime] = result.get(prime, Fraction(0)) + hi * exponent
    for prime, exponent in log_vector(lo).items():
        result[prime] = result.get(prime, Fraction(0)) - lo * exponent
    return result


def curvature(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> dict[int, Fraction]:
    width = left[1] - left[0]
    need(width == right[1] - right[0], "width")
    result: dict[int, Fraction] = {}
    for prime, value in interval_vector(right).items():
        result[prime] = result.get(prime, Fraction(0)) + value / width
    for prime, value in interval_vector(left).items():
        result[prime] = result.get(prime, Fraction(0)) - value / width
    return {prime: value for prime, value in result.items() if value}


def exact_counts() -> dict[str, int]:
    clocks = [Fraction(80 + 3 * i, 1) for i in range(32)]
    clocks += [Fraction(323 + 12 * i + 2 * (i % 5) + 1, 4) for i in range(32)]
    rank = norms = dots = variations = layers = boundary = 0
    for clock in clocks:
        data = blocks(clock)
        sizes = data["sizes"]
        frame = specs(data)
        for rho2, coeff in frame:
            need(rho2 * sum((s * c * c for s, c in zip(sizes, coeff)), Fraction(0)) == 1,
                 "norm")
            base = sum((abs(a - b) for a, b in zip([Fraction(0)] + coeff, coeff + [Fraction(0)])),
                       Fraction(0))
            need(rho2 * base * base == Fraction(4, 1) / rho2, "variation")
            for c in coeff:
                need(rho2 * c * c <= Fraction(1, 1) / rho2, "height")
            norms += 1
            variations += 1
        for i in range(3):
            for j in range(i + 1, 3):
                value = sum((s * a * b for s, a, b in zip(sizes, frame[i][1], frame[j][1])),
                            Fraction(0))
                need(value == 0, "orthogonality")
                dots += 1
        rank += 1
        for lo, hi in data["intervals"]:
            length = hi - lo + 1
            for divisor in range(1, 25):
                count = hi // divisor - (lo - 1) // divisor
                need(abs(Fraction(count) - Fraction(length, divisor)) <= 1, "density")
                layers += 1
        for shift in range(-96, 97):
            for split in (data["a"], data["midpoint"], data["b"]):
                cross = sum(1 for source in range(data["a"] + 1, data["b"] + 1)
                            if (source <= split) != (source + shift <= split))
                need(cross <= abs(shift), "crossing")
                boundary += 1
    pairs = [
        ((Fraction(1, 2), Fraction(3, 4)), (Fraction(3, 4), Fraction(1)), Fraction(32, 27)),
        ((Fraction(1, 2), Fraction(5, 8)), (Fraction(5, 8), Fraction(3, 4)), Fraction(3456, 3125)),
        ((Fraction(3, 4), Fraction(7, 8)), (Fraction(7, 8), Fraction(1)), Fraction(884736, 823543)),
    ]
    for left, right, ratio in pairs:
        expected = {p: 2 * e for p, e in log_vector(ratio).items()}
        need(curvature(left, right) == expected and ratio > 1, "curvature")
    need(len(clocks) == 64, "clock count")
    return {"boundary_checks": boundary, "clock_count": 64, "curvature_pairs": 3,
            "divisor_layers": layers, "frame_norm_checks": norms,
            "orthogonality_checks": dots, "rank_checks": rank,
            "variation_checks": variations}


def sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if flags[value]:
            first = value * value
            count = (limit - first) // value + 1
            flags[first:limit + 1:value] = b"\x00" * count
    return [value for value in range(2, limit + 1) if flags[value]]


def mu(value: int) -> int:
    remaining, parity, divisor = value, 0, 2
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


def multiples(lo: int, hi: int, divisor: int) -> int:
    return hi // divisor - (lo - 1) // divisor


def observation(clock: int) -> dict[str, Any]:
    data = blocks(Fraction(clock, 1))
    intervals = data["intervals"]
    sums = [0.0] * 4
    for prime in sieve(data["b"]):
        power, exponent = prime, 1
        while power <= data["b"]:
            for index, (lo, hi) in enumerate(intervals):
                if lo <= power <= hi:
                    sums[index] += 1.0 / exponent
                    break
            if power > data["b"] // prime:
                break
            power *= prime
            exponent += 1
    cutoff = int(math.floor(clock ** (133.0 / 400.0)))
    for divisor in range(1, cutoff + 1):
        value = mu(divisor)
        if value:
            for index, (lo, hi) in enumerate(intervals):
                sums[index] -= value * multiples(lo, hi, divisor)
    sizes = data["sizes"]
    means = [total / size for total, size in zip(sums, sizes)]
    pairs = [
        (math.sqrt(data["ell"] * data["right"] / data["n"]),
         (sums[0] + sums[1]) / data["ell"], (sums[2] + sums[3]) / data["right"]),
        (math.sqrt(sizes[0] * sizes[1] / (sizes[0] + sizes[1])), means[0], means[1]),
        (math.sqrt(sizes[2] * sizes[3] / (sizes[2] + sizes[3])), means[2], means[3]),
    ]
    scaled = [format(rho * (left - right) * math.log(clock) ** 2 / math.sqrt(clock), ".15f")
              for rho, left, right in pairs]
    return {"cutoff_U_floor": cutoff, "scaled_beta_haar": scaled, "x": clock}


def expected_object() -> dict[str, Any]:
    kappas = [math.log(32.0 / 27.0) / math.sqrt(2.0),
              math.log(3456.0 / 3125.0) / 2.0,
              math.log(884736.0 / 823543.0) / 2.0]
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": 9},
        "claim": FIREWALL["TPC257_MAXIMUM_CLAIM"],
        "constants": {
            "kappa0": "log(32/27)/sqrt(2)", "kappa1": "log(3456/3125)/2",
            "kappa2": "log(884736/823543)/2",
            "three_mode_factor": "sqrt(kappa0^2+kappa1^2+kappa2^2)",
            "transverse_factor": "sqrt(kappa1^2+kappa2^2)",
            "kappa_decimals": [format(value, ".15f") for value in kappas],
            "three_mode_factor_decimal": format(math.sqrt(sum(v * v for v in kappas)), ".15f"),
            "transverse_factor_decimal": format(math.sqrt(sum(v * v for v in kappas[1:])), ".15f"),
            "weighted_prime_BQ": "9/2",
        },
        "epistemic_status": {"finite_beta_samples": "NUMERICAL_OBSERVATION",
                              "finite_exact_checks": "PROVED_EXACT_FINITE_REPRODUCTION",
                              "theorem": "PROVED_SOURCE_BACKED"},
        "exponents": {"adjoint_main": "7/6=56/48", "boundary_gap": "1/48",
                       "divisor_density_remainder": "-67/400", "hard_and_jump": "55/48",
                       "input_unit": "5/6"},
        "finite_exact_checks": exact_counts(),
        "firewall": copy.deepcopy(FIREWALL),
        "numerical_observation": {"proof_credit": "NONE",
                                   "samples": [observation(100000), observation(1000000)],
                                   "status": "NUMERICAL_OBSERVATION"},
        "round2_clue": ROUND2_CLUE, "schema": "TPC257_CERTIFICATE_V1",
        "source_claim_markers": 22, "source_hashes": copy.deepcopy(SOURCE_HASHES),
    }


def semantic(candidate: Any, expected: dict[str, Any]) -> bool:
    if not isinstance(candidate, dict) or candidate != expected:
        return False
    firewall = candidate.get("firewall", {})
    return (type(firewall.get("TPC257_FIXED_ATOM_CREDIT")) is int
            and candidate.get("numerical_observation", {}).get("status") == "NUMERICAL_OBSERVATION"
            and candidate.get("numerical_observation", {}).get("proof_credit") == "NONE")


def mutations(expected: dict[str, Any]) -> tuple[int, int]:
    rejected = 0
    classes = 14
    for index in range(classes):
        candidate = copy.deepcopy(expected)
        if index == 0:
            candidate["schema"] += "_M"
        elif index == 1:
            candidate["claim"] = "CONJECTURE"
        elif index == 2:
            candidate["baseline"]["head"] = "0" * 40
        elif index == 3:
            candidate["source_hashes"][sorted(SOURCE_HASHES)[0]] = "a" * 64
        elif index == 4:
            candidate["source_claim_markers"] += 1
        elif index == 5:
            candidate["constants"]["kappa0"] += "_M"
        elif index == 6:
            candidate["exponents"]["boundary_gap"] = "0"
        elif index == 7:
            candidate["firewall"]["TPC257_FULL_GATE_B"] = "PAID"
        elif index == 8:
            candidate["firewall"]["TPC257_FIXED_ATOM_CREDIT"] = "1"
        elif index == 9:
            candidate["finite_exact_checks"]["clock_count"] += 1
        elif index == 10:
            candidate["epistemic_status"]["theorem"] = "HEURISTIC"
        elif index == 11:
            candidate["numerical_observation"]["status"] = "PROVED"
        elif index == 12:
            candidate["numerical_observation"]["samples"][0]["scaled_beta_haar"][0] = "0"
        else:
            candidate["round2_clue"] += "_M"
        if not semantic(candidate, expected):
            rejected += 1
    return rejected, classes


def check_manifest() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*") if path.is_file()}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    need((actual & BUILD_INTERMEDIATES) in (set(), BUILD_INTERMEDIATES), "partial build manifest")


def run() -> None:
    check_manifest()
    check_sources()
    expected = expected_object()
    raw = RESULT.read_text(encoding="utf-8")
    need(raw == canonical(expected), "certificate canonical mismatch")
    need(json.loads(raw) == expected, "certificate semantic mismatch")
    producer_text = (PROJECT / "code/tpc257_four_block_haar_certificate.py").read_text(encoding="utf-8")
    own_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_import = "from " + "tpc257_four_block_haar_certificate"
    need(forbidden_import not in own_text, "producer import")
    forbidden_keyword = "as" + "sert "
    need(forbidden_keyword not in producer_text and forbidden_keyword not in own_text,
         "syntax guard")
    rejected, classes = mutations(expected)
    need(rejected == classes, "mutation rejection")
    counts = expected["finite_exact_checks"]
    print("TPC257_INDEPENDENT_CHECK=PASS "
          f"mutations_rejected={rejected} classes={classes} "
          f"clocks={counts['clock_count']} source_hashes={len(SOURCE_HASHES)} producer_imported=NO")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check is required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TPC257_INDEPENDENT_CHECK=FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
