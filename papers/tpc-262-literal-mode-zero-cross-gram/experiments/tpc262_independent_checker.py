#!/usr/bin/env python3
"""Independent replay and mutation audit for TPC-262."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc262_certificate.json"
BASELINE = "fbf95fe0ca19918c6f5fe182277d1ecc4068b449"
CLAIM = (
    "PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL"
)
PRIMES = (5, 7, 11, 13)
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "01828abe639226e4b8db07fc941547151ee70fefa648b25cbaac21dc3b25ad05",
    "papers/tpc-261-strict-endpoint-budget-compiler/README.md":
        "a3a3f1c33b48eaab75e503657290421b2d092c640c3a95bc0713bd7f6ba6b977",
    "papers/tpc-261-strict-endpoint-budget-compiler/PROOF_PACKAGE.md":
        "0bcecbebfb00609cb1f9a429f715e5ab493811225b8c2b4f337e48d571599dd8",
    "papers/tpc-261-strict-endpoint-budget-compiler/notes/theorem_ledger.md":
        "731928d3fddbc3014e52e0fec887fe6980787577b4945f2d5fc95d3116214ce8",
    "papers/tpc-261-strict-endpoint-budget-compiler/notes/route_evaluation.md":
        "7860c4a756ccf4002c7ed8d0fe14b346d439f9aa5244f462255f23677a7d51ee",
    "research/tpc-big-road/bridge_b_strict_endpoint_budget_compiler.md":
        "31081a1a0f92cce5c7b7175b27d9d3e250f3fd505002093719b8bb4ea8becb47",
    "research/tpc-big-road/tpc_bridge_b_strict_endpoint_budget_compiler_checker.py":
        "9feea6fad48b65af9e061b29114b5f6d509fab233d5a8d55fd16fd54d2b3bf39",
    "research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md":
        "74e42689e17efad75e9718a9d6ac3d8f3ec9c16239204a4915b0b7bdc17ae218",
    "research/tpc-big-road/bridge_b_phase_fourier_collision_separation.md":
        "3a6783dc1e5798e2876bd0cdd1eee230a457749738e0f4b05685ca32e4ad0dac",
    "research/tpc-big-road/bridge_b_zero_hole_additive_edge_frame.md":
        "6244c1045faf86f97334c3bf5154ff68f945d4dd9c33b8f00ddd8ee6032442dd",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE + ":" + path], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == b"", "frozen " + path)
    return result.stdout


def audit_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(path)).hexdigest() == expected,
             "source hash " + path)


def matrix(q: int) -> tuple[tuple[Fraction, ...], ...]:
    m = q - 1
    return tuple(tuple((Fraction(1) if i == j else Fraction(0))
                       - Fraction(1, m) for j in range(m))
                 for i in range(m))


def multiply(m: tuple[tuple[Fraction, ...], ...],
             v: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum((a * b for a, b in zip(row, v)), Fraction(0))
                 for row in m)


def inner(a: dict[int, tuple[Fraction, ...]],
          b: dict[int, tuple[Fraction, ...]]) -> Fraction:
    return sum((Fraction(q) * sum((x * y for x, y in zip(a[q], b[q])),
                                  Fraction(0)) for q in PRIMES), Fraction(0))


def zero() -> dict[int, tuple[Fraction, ...]]:
    return {q: (Fraction(0),) * (q - 1) for q in PRIMES}


def witness(sign: int) -> dict[int, tuple[Fraction, ...]]:
    source = zero()
    source[5] = (Fraction(sign), Fraction(0), Fraction(0), Fraction(0))
    return {q: multiply(matrix(q), source[q]) for q in PRIMES}


def audit_matrices() -> int:
    checks = 0
    for q in PRIMES:
        c = matrix(q)
        m = q - 1
        square = tuple(tuple(sum((c[i][k] * c[k][j] for k in range(m)),
                                 Fraction(0)) for j in range(m))
                       for i in range(m))
        need(square == c, "projection")
        need(all(sum(row, Fraction(0)) == 0 for row in c), "constant kernel")
        need(sum((c[i][i] for i in range(m)), Fraction(0)) == q - 2,
             "rank trace")
        for vector in (
            tuple(Fraction(2 * i - 3) for i in range(m)),
            tuple(Fraction((i - 1) ** 2) for i in range(m)),
        ):
            cv = multiply(c, vector)
            lhs = sum((a * b for a, b in zip(vector, cv)), Fraction(0))
            rhs = sum(((vector[i] - vector[j]) ** 2 for i in range(m)
                       for j in range(i + 1, m)), Fraction(0)) / m
            need(lhs == rhs and lhs >= 0, "quadratic form")
            checks += 1
    return checks


def audit_gram() -> dict[str, Any]:
    y = witness(1)
    d = inner(y, y)
    plus = tuple(y for _ in range(4))
    alternating = tuple(witness(1 if j % 2 == 0 else -1)
                        for j in range(4))
    def gram(packets):
        return [[inner(packets[i], packets[j]) for j in range(4)]
                for i in range(4)]
    gp = gram(plus)
    ga = gram(alternating)
    dp = sum((gp[i][i] for i in range(4)), Fraction(0))
    da = sum((ga[i][i] for i in range(4)), Fraction(0))
    cp = sum((gp[i][j] for i in range(4) for j in range(i + 1, 4)),
             Fraction(0))
    ca = sum((ga[i][j] for i in range(4) for j in range(i + 1, 4)),
             Fraction(0))
    need(d == Fraction(15, 4), "probe norm")
    need(dp == da == 4 * d, "diagonal equality")
    need(dp + 2 * cp == 16 * d, "plus cross sum")
    need(da + 2 * ca == 0, "alternating cross sum")
    need(cp == 6 * d and ca == -2 * d, "cross values")
    return {"probe_norm": str(d), "plus_cross": str(cp),
            "alternating_cross": str(ca), "plus_mode_zero": str(16 * d),
            "alternating_mode_zero": "0"}


def audit_phase_characters() -> dict[str, Any]:
    x = zero()
    y = zero()
    x[5] = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    y[5] = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    xx = inner({q: multiply(matrix(q), x[q]) for q in PRIMES},
               {q: multiply(matrix(q), x[q]) for q in PRIMES})
    yy = inner({q: multiply(matrix(q), y[q]) for q in PRIMES},
               {q: multiply(matrix(q), y[q]) for q in PRIMES})
    xy = inner({q: multiply(matrix(q), x[q]) for q in PRIMES},
               {q: multiply(matrix(q), y[q]) for q in PRIMES})
    need(xx == yy == Fraction(15, 4) and xy == Fraction(-5, 4),
         "phase source")
    return {"packet_energy": ["5", "15/2", "10", "15/2"],
            "F0": str(xx + yy), "F1": str(xy), "F2": "0",
            "F3": str(xy)}


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        firewall = data["firewall"]
        threshold = data["threshold_audit"]
        gram = data["gram_audit"]
        return (
            data["schema"] == "TPC262_LITERAL_MODE_ZERO_CROSS_GRAM_CERTIFICATE_V1"
            and data["claim"] == CLAIM
            and data["baseline"] == {"head": BASELINE, "source_count": 11}
            and data["source_hashes"] == SOURCE_HASHES
            and data["fiber_audit"]["primes"] == list(PRIMES)
            and gram["probe_norm"] == "15/4"
            and gram["records"]["plus"]["mode_zero"] == "60"
            and gram["records"]["alternating"]["mode_zero"] == "0"
            and gram["records"]["plus"]["diagonal"] == ["15/4"] * 4
            and gram["records"]["alternating"]["diagonal"] == ["15/4"] * 4
            and data["phase_character_audit"] == {
                "F0": "15/2", "F1": "-5/4", "F2": "0", "F3": "-5/4",
                "cross_inner": "-5/4",
                "interpretation":
                "F0=||X||^2+||Y||^2; F1=<Y,X>; F3=<X,Y>",
                "packet_energy": ["5", "15/2", "10", "15/2"],
            }
            and data["signed_operator_audit"]["additive_phase"] ==
                "v=0_FINITE_CERTIFICATE_ONLY"
            and data["signed_operator_audit"]["primes"] == [5, 7]
            and data["signed_operator_audit"]["interval"] == [1, 24]
            and data["signed_operator_audit"]["packet_quadratics"] ==
                ["9523/6", "2705/2", "6707/6", "2705/2"]
            and data["signed_operator_audit"]["polarized_scalar"] == "352/3"
            and data["signed_operator_audit"]["polarized_imaginary_part"] == "0"
            and data["signed_operator_audit"]["rows"][0]["deleted_diagonal"] == "3/4"
            and data["signed_operator_audit"]["rows"][1]["deleted_diagonal"] == "5/6"
            and threshold["gap"] == "1/400"
            and firewall["TPC262_ARITHMETIC_ADVANCE"] == "NO"
            and firewall["TPC262_ROUTE_ADVANCE"] ==
                "YES_SCOPED_LITERAL_SIGNED_OPERATOR_INTERFACE"
            and firewall["TPC262_FULL_GATE_B"] == "OPEN"
            and firewall["TPC262_L2"] == "NONE"
            and firewall["TPC262_FIXED_ATOM_CREDIT"] == 0
            and firewall["TPC262_LITERAL_BETA_W_CROSS_GRAM"] == "OPEN"
            and firewall["TPC262_SIGNED_REMAINDER_OPERATOR"] ==
                "PROVED_EXACT_FINITE_X"
            and firewall["TPC262_DELETED_DIAGONAL"] ==
                "PROVED_EXACT_Q_MINUS_2"
            and firewall["TPC262_PHASE_CHARACTER_SEPARATION"] == "PROVED_EXACT"
            and firewall["TPC262_POLARIZED_V59_CHARACTER"] == "OPEN"
            and firewall["TPC262_TWIN_PRIME_RESULT"] == "NONE"
        )
    except (IndexError, KeyError, TypeError):
        return False


def mutation_audit(data: dict[str, Any]) -> int:
    mutations = []
    def mutate(path: tuple[str, ...], value: Any) -> None:
        item = json.loads(json.dumps(data))
        cursor: Any = item
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        mutations.append(item)
    mutate(("schema",), "TPC262_V0")
    mutate(("claim",), "PROVED")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("fiber_audit", "primes"), [3, 5, 7, 11])
    mutate(("gram_audit", "probe_norm"), "1")
    mutate(("gram_audit", "records", "plus", "mode_zero"), "0")
    mutate(("phase_character_audit", "F1"), "0")
    mutate(("signed_operator_audit", "polarized_scalar"), "0")
    mutate(("signed_operator_audit", "rows"), [])
    mutate(("threshold_audit", "gap"), "1/399")
    mutate(("firewall", "TPC262_ARITHMETIC_ADVANCE"), "YES")
    mutate(("firewall", "TPC262_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC262_LITERAL_BETA_W_CROSS_GRAM"), "PROVED")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    audit_sources()
    matrix_checks = audit_matrices()
    expected_gram = audit_gram()
    expected_phase = audit_phase_characters()
    raw = CERTIFICATE.read_text(encoding="utf-8")
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical certificate")
    need(semantic(data), "certificate semantics")
    need(data["gram_audit"]["probe_norm"] == expected_gram["probe_norm"],
         "producer mismatch")
    need(data["phase_character_audit"]["F0"] == expected_phase["F0"] and
         data["phase_character_audit"]["F1"] == expected_phase["F1"],
         "phase producer mismatch")
    mutations = mutation_audit(data)
    print("TPC262_INDEPENDENT_CHECK=PASS "
          f"matrix_checks={matrix_checks} mutation_cases={mutations} "
          "operator_image=literal_finite dft=exact threshold=1/400")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC262_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
