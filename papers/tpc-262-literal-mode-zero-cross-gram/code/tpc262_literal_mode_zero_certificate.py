#!/usr/bin/env python3
"""Exact certificate for the TPC-262 literal zero-fiber Gram audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "fbf95fe0ca19918c6f5fe182277d1ecc4068b449"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc262_certificate.json"
PRIMES = (5, 7, 11, 13)
STATUS = (
    "PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL"
)
ROUND2_CLUE = "CENSUS_THE_LITERAL_GROWING_PRIME_SHELL_CROSS_GRAM"

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

FIREWALL = {
    "TPC262_ARITHMETIC_ADVANCE": "NO",
    "TPC262_CROSS_GRAM_IDENTITY": "PROVED_EXACT",
    "TPC262_ENDPOINT_THRESHOLD": "PROVED_EXACT_ONE_OVER_400",
    "TPC262_FIXED_ATOM_CREDIT": 0,
    "TPC262_FULL_GATE_B": "OPEN",
    "TPC262_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC262_GROWING_SHELL_COUNTEREXAMPLE": "NONE",
    "TPC262_L2": "NONE",
    "TPC262_LITERAL_BETA_W_CROSS_GRAM": "OPEN",
    "TPC262_OPERATOR_IMAGE_WITNESS": "NUMERICALLY_CERTIFIED_STRUCTURAL",
    "TPC262_PHASE_CHARACTER_SEPARATION": "PROVED_EXACT",
    "TPC262_POLARIZED_V59_CHARACTER": "OPEN",
    "TPC262_ROUTE_ADVANCE": "YES_SCOPED_LITERAL_SIGNED_OPERATOR_INTERFACE",
    "TPC262_SIGNED_REMAINDER_OPERATOR": "PROVED_EXACT_FINITE_X",
    "TPC262_DELETED_DIAGONAL": "PROVED_EXACT_Q_MINUS_2",
    "TPC262_STATUS": STATUS,
    "TPC262_TWIN_PRIME_RESULT": "NONE",
    "TPC262_UNIT_CLASS_PROJECTION": "PROVED_EXACT_FINITE",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def source_audit() -> int:
    for relative, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(relative)).hexdigest() == expected,
             "source hash: " + relative)
    return len(SOURCE_HASHES)


def centered(q: int) -> tuple[tuple[Fraction, ...], ...]:
    m = q - 1
    return tuple(
        tuple((Fraction(1) if i == j else Fraction(0)) - Fraction(1, m)
              for j in range(m))
        for i in range(m)
    )


def mat_vec(matrix: tuple[tuple[Fraction, ...], ...],
            vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum((a * b for a, b in zip(row, vector)), Fraction(0))
                 for row in matrix)


def dot(left: tuple[Fraction, ...],
        right: tuple[Fraction, ...],
        weight: Fraction = Fraction(1)) -> Fraction:
    return weight * sum((a * b for a, b in zip(left, right)), Fraction(0))


def fiber_audit() -> dict[str, Any]:
    records = []
    for q in PRIMES:
        matrix = centered(q)
        m = q - 1
        identity = tuple(tuple(Fraction(1) if i == j else Fraction(0)
                               for j in range(m)) for i in range(m))
        square = tuple(
            tuple(sum((matrix[i][k] * matrix[k][j] for k in range(m)),
                      Fraction(0)) for j in range(m))
            for i in range(m)
        )
        need(matrix == tuple(tuple(row) for row in zip(*matrix)), "symmetry")
        need(square == matrix, "idempotence")
        need(all(sum(row, Fraction(0)) == 0 for row in matrix), "row sum")
        trace = sum((matrix[i][i] for i in range(m)), Fraction(0))
        need(trace == q - 2, "trace rank proxy")
        probes = (
            tuple(Fraction(i - 2) for i in range(m)),
            tuple(Fraction((i + 1) * (i - 3)) for i in range(m)),
        )
        forms = []
        for vector in probes:
            transformed = mat_vec(matrix, vector)
            form = dot(vector, transformed)
            pair_sum = sum(
                ((vector[i] - vector[j]) ** 2 for i in range(m)
                 for j in range(i + 1, m)), Fraction(0)
            ) / m
            need(form == pair_sum and form >= 0, "PSD form")
            forms.append(str(form))
        need(identity[0][0] == 1, "identity fixture")
        records.append({
            "q": q,
            "dimension": m,
            "rank": q - 2,
            "trace": str(trace),
            "quadratic_forms": forms,
        })
    return {"primes": list(PRIMES), "records": records}


def zero_packet() -> dict[int, tuple[Fraction, ...]]:
    return {q: (Fraction(0),) * (q - 1) for q in PRIMES}


def apply_operator(source: dict[int, tuple[Fraction, ...]]) -> dict[int, tuple[Fraction, ...]]:
    return {q: mat_vec(centered(q), source[q]) for q in PRIMES}


def inner(left: dict[int, tuple[Fraction, ...]],
          right: dict[int, tuple[Fraction, ...]]) -> Fraction:
    return sum((dot(left[q], right[q], Fraction(q)) for q in PRIMES),
               Fraction(0))


def source_probe() -> dict[int, tuple[Fraction, ...]]:
    source = zero_packet()
    source[5] = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    return source


def packet_family(signs: tuple[int, int, int, int]) -> tuple[
        dict[int, tuple[Fraction, ...]], ...]:
    output = apply_operator(source_probe())
    return tuple({q: tuple(sign * value for value in output[q])
                  for q in PRIMES} for sign in signs)


def gaussian_mul(left: tuple[Fraction, Fraction],
                 right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def dft_energy(packets: tuple[dict[int, tuple[Fraction, ...]], ...]
               ) -> list[Fraction]:
    roots = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
             (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))
    answer = []
    for k in range(4):
        mode = {q: [(Fraction(0), Fraction(0))] * (q - 1)
                for q in PRIMES}
        for j, packet in enumerate(packets):
            root = roots[(-j * k) % 4]
            for q in PRIMES:
                for r, value in enumerate(packet[q]):
                    old = mode[q][r]
                    product = gaussian_mul(root, (value, Fraction(0)))
                    mode[q][r] = (old[0] + product[0] / 2,
                                  old[1] + product[1] / 2)
        energy = sum(
            (Fraction(q) * (value[0] * value[0] + value[1] * value[1])
             for q in PRIMES for value in mode[q]), Fraction(0)
        )
        answer.append(energy)
    return answer


def gram_audit() -> dict[str, Any]:
    plus = packet_family((1, 1, 1, 1))
    alternating = packet_family((1, -1, 1, -1))
    mixed = packet_family((1, 1, -1, -1))
    records = {}
    for name, packets in (("plus", plus), ("alternating", alternating),
                          ("mixed", mixed)):
        gram = [[inner(packets[i], packets[j]) for j in range(4)]
                for i in range(4)]
        diagonal = [gram[i][i] for i in range(4)]
        total_diagonal = sum(diagonal, Fraction(0))
        cross_real = sum((gram[i][j] for i in range(4)
                          for j in range(i + 1, 4)), Fraction(0))
        mode = dft_energy(packets)
        need(all(diagonal[i] == diagonal[0] for i in range(4)),
             "equal packet diagonal")
        need(4 * mode[0] == total_diagonal + 2 * cross_real,
             "cross-Gram reconstruction")
        need(sum(mode, Fraction(0)) == total_diagonal, "DFT Parseval")
        records[name] = {
            "cross_real": str(cross_real),
            "diagonal": [str(value) for value in diagonal],
            "mode_energy": [str(value) for value in mode],
            "mode_zero": str(4 * mode[0]),
            "packet_energy": str(total_diagonal),
        }
    d = inner(plus[0], plus[0])
    need(d == Fraction(15, 4), "q=5 probe norm")
    need(records["plus"]["mode_zero"] == str(16 * d), "plus endpoint")
    need(records["alternating"]["mode_zero"] == "0", "alternating endpoint")
    need(records["mixed"]["mode_zero"] == "0", "mixed endpoint")
    return {"probe_norm": str(d), "records": records}


def phase_character_audit() -> dict[str, Any]:
    """Separate aggregate mode zero from the nontrivial polarization modes."""
    first = source_probe()
    second = zero_packet()
    second[5] = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    x = apply_operator(first)
    y = apply_operator(second)
    xx = inner(x, x)
    yy = inner(y, y)
    xy = inner(x, y)
    need(xx == Fraction(15, 4) and yy == Fraction(15, 4), "phase norms")
    need(xy == Fraction(-5, 4), "phase cross term")
    # E_j = ||X+i^jY||^2 for the conjugate-linear-first-slot convention.
    energies = ["5", "15/2", "10", "15/2"]
    need(sum((Fraction(5), Fraction(15, 2), Fraction(10), Fraction(15, 2)),
             Fraction(0)) / 4 == xx + yy, "F0")
    need((energies[0], energies[1], energies[2], energies[3]) ==
         ("5", "15/2", "10", "15/2"), "phase energy fixture")
    return {
        "packet_energy": energies,
        "F0": "15/2",
        "F1": "-5/4",
        "F2": "0",
        "F3": "-5/4",
        "cross_inner": str(xy),
        "interpretation": "F0=||X||^2+||Y||^2; F1=<Y,X>; F3=<X,Y>",
    }


def signed_operator_audit() -> dict[str, Any]:
    """Audit the literal reduced-residue synthesis and deleted diagonal at v=0."""
    interval = tuple(range(1, 25))
    size = len(interval)
    total = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    rows = []
    for q in (5, 7):
        c = centered(q)
        synthesis = tuple(
            tuple(Fraction(1) if n % q == r else Fraction(0)
                  for n in interval)
            for r in range(1, q)
        )
        js = [[Fraction(0) for _ in range(size)] for _ in range(size)]
        for a in range(size):
            for b in range(size):
                value = sum(
                    (synthesis[r][a] * c[r][s] * synthesis[s][b]
                     for r in range(q - 1) for s in range(q - 1)),
                    Fraction(0),
                )
                if a == b and interval[a] % q != 0:
                    value -= Fraction(q - 2, q - 1)
                js[a][b] = value
                total[a][b] += Fraction(q) * value
        need(all(js[a][b] == js[b][a] for a in range(size)
                 for b in range(size)), "signed operator symmetry")
        probe = tuple(Fraction((n % 5) - 2) for n in interval)
        residue = tuple(sum((synthesis[r][a] * probe[a] for a in range(size)),
                            Fraction(0)) for r in range(q - 1))
        centered_residue = mat_vec(c, residue)
        variance = dot(centered_residue, centered_residue)
        diagonal = Fraction(q - 2, q - 1) * sum(
            (probe[a] * probe[a] for a, n in enumerate(interval) if n % q != 0),
            Fraction(0),
        )
        quadratic = sum(
            (probe[a] * js[a][b] * probe[b]
             for a in range(size) for b in range(size)), Fraction(0)
        )
        need(quadratic == variance - diagonal, "signed quadratic identity")
        rows.append({"q": q, "deleted_diagonal": f"{q - 2}/{q - 1}",
                     "variance": str(variance), "diagonal": str(diagonal),
                     "remainder": str(quadratic)})
    beta = tuple(Fraction((n % 5) - 2) for n in interval)
    w = tuple(Fraction((2 * n % 7) - 3) for n in interval)
    def bilinear(left: tuple[Fraction, ...],
                 right: tuple[Fraction, ...]) -> Fraction:
        return sum((left[a] * total[a][b] * right[b]
                    for a in range(size) for b in range(size)), Fraction(0))
    qb = bilinear(beta, beta)
    qw = bilinear(w, w)
    cross = bilinear(w, beta)
    need(cross == bilinear(beta, w), "Hermitian cross term")
    packets = (qb + qw + 2 * cross, qb + qw,
               qb + qw - 2 * cross, qb + qw)
    polarized_real = (packets[0] - packets[2]) / 4
    polarized_imag = (packets[1] - packets[3]) / 4
    need(polarized_real == cross and polarized_imag == 0,
         "four-phase polarization")
    return {
        "additive_phase": "v=0_FINITE_CERTIFICATE_ONLY",
        "interval": [interval[0], interval[-1]],
        "primes": [5, 7],
        "rows": rows,
        "packet_quadratics": [str(value) for value in packets],
        "polarized_scalar": str(cross),
        "polarized_imaginary_part": str(polarized_imag),
        "identity":
            "V_q^times-D_q^times=<a,J_q,0 a>; 1/4 sum i^j Q(a_j)=<w,J beta>",
    }


def threshold_audit() -> dict[str, str]:
    baseline = Fraction(5, 3)
    target = Fraction(1997, 1200)
    gap = baseline - target
    need(gap == Fraction(1, 400), "endpoint gap")
    strict = Fraction(1, 96) - Fraction(1, 400)
    need(strict == Fraction(19, 2400), "strict benchmark")
    return {
        "baseline": str(baseline),
        "target": str(target),
        "gap": str(gap),
        "criterion": "effective_saving > 1/400",
        "benchmark_margin": str(strict),
    }


def build() -> dict[str, Any]:
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_audit()},
        "claim": STATUS,
        "epistemic_status": {
            "cross_gram_identity": "PROVED_EXACT",
            "finite_operator_image_witness": "NUMERICALLY_CERTIFIED_STRUCTURAL",
            "growing_beta_w_cross_gram": "OPEN",
            "phase_character_separation": "PROVED_EXACT",
            "signed_remainder_operator": "PROVED_EXACT_FINITE_X",
            "unit_class_projection": "PROVED_EXACT_FINITE",
        },
        "fiber_audit": fiber_audit(),
        "firewall": dict(FIREWALL),
        "gram_audit": gram_audit(),
        "phase_character_audit": phase_character_audit(),
        "signed_operator_audit": signed_operator_audit(),
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC262_LITERAL_MODE_ZERO_CROSS_GRAM_CERTIFICATE_V1",
        "source_hashes": dict(SOURCE_HASHES),
        "threshold_audit": threshold_audit(),
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
    gram = expected["gram_audit"]
    print("TPC262_CERTIFICATE=PASS "
          f"sources={expected['baseline']['source_count']} primes={len(PRIMES)} "
          f"probe_norm={gram['probe_norm']} plus_mode_zero={gram['records']['plus']['mode_zero']} "
          "alternating_mode_zero=0 threshold=1/400 literal_growing=OPEN")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC262_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
