#!/usr/bin/env python3
"""Independent semantic checker for the TPC-256 certificate.

This module deliberately duplicates the defining computations and never
imports the producer.  It also performs deterministic mutation rejection.
"""

from __future__ import annotations

import argparse
import ast
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

SEMANTIC_MANIFEST = {
    ".gitignore",
    "DERIVATION_PACKAGE.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "README.md",
    "code/tpc256_literal_beta_haar_certificate.py",
    "experiments/tpc256_beta_haar_asymptotic_stress.py",
    "experiments/tpc256_independent_checker.py",
    "notes/citation_verification.md",
    "notes/claim_firewall.md",
    "notes/computational_protocol.md",
    "notes/route_evaluation.md",
    "notes/source_lock.md",
    "notes/theorem_ledger.md",
    "paper/main.tex",
    "paper/paper.pdf",
    "paper/references.bib",
    "results/tpc256_certificate.json",
}

LATEX_INTERMEDIATES = {
    "paper/paper.aux",
    "paper/paper.bbl",
    "paper/paper.blg",
    "paper/paper.log",
    "paper/paper.out",
}

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


def frozen_blob(relative_path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{BASELINE_HEAD}:{relative_path}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(proc.returncode == 0, f"frozen source unreadable: {relative_path}")
    return proc.stdout


def verify_source_hashes() -> None:
    for relative_path, expected_hash in SOURCE_HASHES.items():
        digest = hashlib.sha256(frozen_blob(relative_path)).hexdigest()
        require(digest == expected_hash, f"frozen source mismatch: {relative_path}")


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def rank_data(clock: Fraction) -> tuple[int, int, int, int, int, int]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    midpoint = a + ell
    require(ell > 0 and right > 0, "short rank clock")
    return a, b, n, ell, right, midpoint


def multiples(lo: int, hi: int, divisor: int) -> int:
    return hi // divisor - (lo - 1) // divisor


def independently_count_exact_fixtures() -> dict[str, int]:
    clocks = [Fraction(80 + 3 * index, 1) for index in range(32)]
    clocks.extend(Fraction(323 + 12 * index + (2 * (index % 5) + 1), 4) for index in range(32))
    ranks = 0
    layers = 0
    for clock in clocks:
        a, b, n, ell, right, midpoint = rank_data(clock)
        require(Fraction(ell * right, n) * (Fraction(1, ell) + Fraction(1, right)) == 1, "rank identity")
        require(midpoint == a + ell and b - midpoint == right, "rank endpoints")
        ranks += 1
        for divisor in range(1, 25):
            left_error = abs(Fraction(multiples(a + 1, midpoint, divisor), 1) - Fraction(ell, divisor))
            right_error = abs(Fraction(multiples(midpoint + 1, b, divisor), 1) - Fraction(right, divisor))
            require(left_error <= 1 and right_error <= 1, "density discrepancy")
            layers += 1

    mask_terms = 0
    periods = 0
    for prime in (3, 5, 7, 11, 13, 17, 19, 23):
        for residue in range(1, prime):
            values = []
            for u in range(prime):
                if u % prime == 0:
                    values.append(Fraction(0, 1))
                else:
                    values.append(Fraction(int(u % prime == residue), 1) - Fraction(1, prime - 1))
            require(sum(values, Fraction(0, 1)) == 0, "mask period")
            periods += 1
            for h in range(-3 * prime, 3 * prime + 1):
                u = residue + h
                value = Fraction(0, 1)
                if u % prime != 0:
                    value = Fraction(int(u % prime == residue), 1) - Fraction(1, prime - 1)
                require(abs(value) <= int(h % prime == 0) + Fraction(2, prime), "mask bound")
                mask_terms += 1

    hard = 0
    jump = 0
    for h in range(-96, 97):
        hard_count = 0
        jump_count = 0
        for t in range(33, 97):
            shifted = t + h
            hard_count += int(not (33 <= shifted <= 96))
            jump_count += int(33 <= shifted <= 96 and ((t <= 64) != (shifted <= 64)))
        require(hard_count <= abs(h), "hard crossing")
        require(jump_count <= abs(h), "jump crossing")
        hard += 1
        jump += 1

    return {
        "boundary_hard_checks": hard,
        "boundary_jump_checks": jump,
        "divisor_layers": layers,
        "rank_clocks": len(clocks),
        "rank_identities": ranks,
        "unit_mask_periods": periods,
        "unit_mask_terms": mask_terms,
    }


def primes_up_to(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if flags[value]:
            first = value * value
            size = (limit - first) // value + 1
            flags[first : limit + 1 : value] = b"\x00" * size
    return [value for value in range(2, limit + 1) if flags[value]]


def mu(value: int) -> int:
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
        if exponent == 1:
            parity += 1
        divisor += 1
    if remaining > 1:
        parity += 1
    return -1 if parity % 2 else 1


def independent_observation(x: int) -> dict[str, str | int]:
    a, b = x // 2, x
    n = b - a
    ell = n // 2
    right = n - ell
    midpoint = a + ell
    prime_sums = [0.0, 0.0]
    for prime in primes_up_to(b):
        exponent = 1
        power = prime
        while power <= b:
            if a < power <= midpoint:
                prime_sums[0] += 1.0 / exponent
            elif midpoint < power <= b:
                prime_sums[1] += 1.0 / exponent
            if power > b // prime:
                break
            power *= prime
            exponent += 1
    cutoff = int(math.floor(x ** (133.0 / 400.0)))
    divisor_sums = [0, 0]
    for divisor in range(1, cutoff + 1):
        value = mu(divisor)
        divisor_sums[0] += value * multiples(a + 1, midpoint, divisor)
        divisor_sums[1] += value * multiples(midpoint + 1, b, divisor)
    rho = math.sqrt(ell * right / n)
    moment = rho * (
        (prime_sums[0] - divisor_sums[0]) / ell
        - (prime_sums[1] - divisor_sums[1]) / right
    )
    scaled = moment * math.log(x) ** 2 / math.sqrt(x)
    return {"cutoff_U_floor": cutoff, "scaled_beta_haar": format(scaled, ".15f"), "x": x}


def independent_expected() -> dict[str, Any]:
    main_decimal = format(math.log(Fraction(32, 27)) / math.sqrt(2.0), ".15f")
    return {
        "baseline": {"handoff_sha256": SOURCE_HASHES["TPC_HANDOFF.md"], "head": BASELINE_HEAD},
        "claim": "PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC",
        "constants": {
            "adjoint_main": "9*log(32/27)/(2*sqrt(2))",
            "beta_haar_main": "log(32/27)/sqrt(2)",
            "beta_haar_main_decimal": main_decimal,
            "weighted_prime_BQ": "9/2",
        },
        "epistemic_status": {
            "finite_exact_checks": "PROVED_EXACT_FINITE_REPRODUCTION",
            "finite_prime_samples": "NUMERICAL_OBSERVATION",
            "theorem": "PROVED_SOURCE_BACKED",
        },
        "exponents": {
            "adjoint_main": "7/6=56/48",
            "boundary_gap": "1/48",
            "divisor_density_remainder": "-67/400",
            "hard_and_jump": "55/48",
            "input_unit": "5/6",
        },
        "finite_exact_checks": independently_count_exact_fixtures(),
        "firewall": deepcopy(FIREWALL),
        "numerical_observation": {
            "proof_credit": "NONE",
            "samples": [independent_observation(100000), independent_observation(1000000)],
            "status": "NUMERICAL_OBSERVATION",
            "target_scaled_constant": main_decimal,
        },
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC256_CERTIFICATE_V1",
        "source_claim_markers": 19,
        "source_hashes": deepcopy(SOURCE_HASHES),
    }


def semantic_check(candidate: Any, expected: dict[str, Any]) -> bool:
    if not isinstance(candidate, dict):
        return False
    if candidate != expected:
        return False
    if not isinstance(candidate["firewall"]["TPC256_FIXED_ATOM_CREDIT"], int):
        return False
    if candidate["numerical_observation"]["status"] != "NUMERICAL_OBSERVATION":
        return False
    if candidate["numerical_observation"]["proof_credit"] != "NONE":
        return False
    return True


def mutate(candidate: dict[str, Any], class_index: int, offset: int) -> dict[str, Any]:
    changed = deepcopy(candidate)
    suffix = f"_M{offset}"
    if class_index == 0:
        changed["schema"] += suffix
    elif class_index == 1:
        changed["claim"] = "CONJECTURE" + suffix
    elif class_index == 2:
        changed["baseline"]["head"] = ("0" if offset % 2 == 0 else "f") * 40
    elif class_index == 3:
        key = sorted(SOURCE_HASHES)[offset % len(SOURCE_HASHES)]
        changed["source_hashes"][key] = ("a" if offset % 2 == 0 else "b") * 64
    elif class_index == 4:
        changed["source_claim_markers"] += offset + 1
    elif class_index == 5:
        key = sorted(changed["exponents"])[offset % len(changed["exponents"])]
        changed["exponents"][key] += suffix
    elif class_index == 6:
        key = sorted(changed["constants"])[offset % len(changed["constants"])]
        changed["constants"][key] += suffix
    elif class_index == 7:
        key = sorted(changed["firewall"])[offset % len(changed["firewall"])]
        changed["firewall"][key] = "PROMOTED_WITHOUT_PROOF" + suffix
    elif class_index == 8:
        changed["firewall"]["TPC256_FIXED_ATOM_CREDIT"] = str(offset + 1)
    elif class_index == 9:
        key = sorted(changed["finite_exact_checks"])[offset % len(changed["finite_exact_checks"])]
        changed["finite_exact_checks"][key] += offset + 1
    elif class_index == 10:
        key = sorted(changed["epistemic_status"])[offset % 3]
        changed["epistemic_status"][key] = "HEURISTIC" + suffix
    elif class_index == 11:
        changed["numerical_observation"]["status"] = "PROVED" + suffix
    elif class_index == 12:
        sample = changed["numerical_observation"]["samples"][offset % 2]
        sample["scaled_beta_haar"] = format(float(sample["scaled_beta_haar"]) + offset + 1, ".15f")
    else:
        changed["round2_clue"] += suffix
    return changed


def check_manifest() -> None:
    actual = {
        str(path.relative_to(PROJECT))
        for path in PROJECT.rglob("*")
        if path.is_file()
    }
    require(actual == SEMANTIC_MANIFEST | LATEX_INTERMEDIATES, "project manifest mismatch")


def check_no_language_assertions() -> None:
    python_files = [
        PROJECT / "code" / "tpc256_literal_beta_haar_certificate.py",
        PROJECT / "experiments" / "tpc256_independent_checker.py",
        PROJECT / "experiments" / "tpc256_beta_haar_asymptotic_stress.py",
    ]
    for path in python_files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        forbidden = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        require(not forbidden, f"language assertion found in {path.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.check, "--check is required")
    verify_source_hashes()
    expected = independent_expected()
    raw = RESULT.read_text(encoding="utf-8")
    require(raw == canonical_json(json.loads(raw)), "certificate is not canonical JSON")
    candidate = json.loads(raw)
    require(semantic_check(candidate, expected), "independent semantic reconstruction failed")
    rejected = 0
    classes = 14
    for class_index in range(classes):
        for offset in range(8):
            if not semantic_check(mutate(candidate, class_index, offset), expected):
                rejected += 1
    require(rejected == 112, "mutation rejection count failed")
    check_manifest()
    check_no_language_assertions()
    print(
        "TPC256_INDEPENDENT_CHECK=PASS mutations_rejected=112 classes=14 "
        "source_hashes=8 producer_imported=NO"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TPC256_INDEPENDENT_CHECK=FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
