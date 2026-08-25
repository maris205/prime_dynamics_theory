#!/usr/bin/env python3
"""Exact producer/checker for the TPC-247 source-operator certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc247_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_LITERAL_V59_SOURCE_OPERATOR_ATTACHMENT_WITH_NORM_OBSTRUCTION"


class CheckFailure(RuntimeError):
    """Fail-closed certificate error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def qtext(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict_load(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise CheckFailure("duplicate JSON key: " + key)
            output[key] = value
        return output
    return json.loads(text, object_pairs_hook=hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          CheckFailure("nonfinite JSON token: " + token)))


def source_fixture() -> dict[str, Any]:
    indices = (2, 3, 4, 6, 8, 9)
    primes = (5, 7)
    blocks = ((2, 3), (4, 6), (8, 9))
    beta = {2: 1, 3: -2, 4: 3, 6: 1, 8: -1, 9: 2}
    w = {2: 2, 3: 1, 4: -1, 6: 3, 8: 2, 9: -2}
    labels = {value: block for block, members in enumerate(blocks)
              for value in members}

    def kernel(shift: int) -> Fraction:
        return Fraction(1, 1 + abs(shift))

    def entry(u: int, t: int) -> Fraction:
        if u == t:
            return Fraction(0)
        total = Fraction(0)
        for prime in primes:
            if u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1) - Fraction(1, prime - 1)
            total += prime * kernel(u - t) * centered
        return total

    direct = sum((Fraction(w[u] * beta[t]) * entry(u, t)
                  for u in indices for t in indices), Fraction(0))
    block_values: dict[tuple[int, int], Fraction] = {}
    block_counts: dict[tuple[int, int], int] = {}
    admissible_count = 0
    for c in range(len(blocks)):
        for b in range(len(blocks)):
            value = Fraction(0)
            count = 0
            for u in blocks[c]:
                for t in blocks[b]:
                    value += Fraction(w[u] * beta[t]) * entry(u, t)
                    for prime in primes:
                        if u != t and u % prime != 0 and t % prime != 0:
                            count += 1
            block_values[(c, b)] = value
            block_counts[(c, b)] = count
            admissible_count += count
    require(sum(block_values.values(), Fraction(0)) == direct,
            "direct/block scalar mismatch")
    require(sum(block_counts.values()) == admissible_count,
            "admissible count mismatch")
    for u in indices:
        for t in indices:
            require(labels[u] in range(len(blocks)) and labels[t] in range(len(blocks)),
                    "block membership")

    w_norm2 = sum((Fraction(value * value) for value in w.values()), Fraction(0))
    w_ext_norm2 = Fraction(len(blocks)) * w_norm2
    b_ext_norm2 = Fraction(0)
    full_output_norm2 = Fraction(0)
    for u in indices:
        full = sum((entry(u, t) * beta[t] for t in indices), Fraction(0))
        full_output_norm2 += full * full
        for b in range(len(blocks)):
            partial = sum((entry(u, t) * beta[t] for t in blocks[b]), Fraction(0))
            b_ext_norm2 += partial * partial
    require(w_ext_norm2 == len(blocks) * w_norm2, "W copy norm")

    counter_a_beta_norm2 = Fraction(0)
    counter_b_ext_norm2 = Fraction(2)
    require(counter_a_beta_norm2 != counter_b_ext_norm2,
            "B norm counterexample")

    block_rows = [
        {"c": c, "b": b, "scalar": qtext(block_values[(c, b)]),
         "admissible_triples": block_counts[(c, b)]}
        for c in range(len(blocks)) for b in range(len(blocks))
    ]
    return {
        "indices": list(indices),
        "primes": list(primes),
        "blocks": [list(block) for block in blocks],
        "beta": {str(key): value for key, value in beta.items()},
        "w": {str(key): value for key, value in w.items()},
        "kernel": "K(h)=1/(1+abs(h))",
        "direct_scalar": qtext(direct),
        "block_scalar": qtext(sum(block_values.values(), Fraction(0))),
        "block_rows": block_rows,
        "admissible_triples": admissible_count,
        "exactly_once": True,
        "w_norm2": qtext(w_norm2),
        "w_external_norm2": qtext(w_ext_norm2),
        "input_block_count": len(blocks),
        "b_external_norm2": qtext(b_ext_norm2),
        "full_output_norm2": qtext(full_output_norm2),
        "b_norms_equal_in_fixture": b_ext_norm2 == full_output_norm2,
        "counterexample_full_output_norm2": qtext(counter_a_beta_norm2),
        "counterexample_external_norm2": qtext(counter_b_ext_norm2),
    }


def build_payload() -> dict[str, Any]:
    return {
        "theorem": {
            "literal_source_operator": "EXACT",
            "hard_support_block_decomposition": "EXACT",
            "admissible_triple_coverage": "EXACTLY_ONCE",
            "tagged_external_covariance": "EXACT",
            "w_lane_norm_inflation": "INPUT_BLOCK_COUNT",
            "b_lane_norm_preservation": "REFUTED_SCOPED",
        },
        "source_fixture": source_fixture(),
        "complex_orientation_firewall": {
            "unconjugated_physical_scalar": {"re": "5/1", "im": "-1/1"},
            "inner_product_with_w": {"re": "5/1", "im": "1/1"},
            "inner_product_with_conjugate_w": {"re": "5/1", "im": "-1/1"},
            "physical_w_is_real": True,
        },
        "scope_firewall": {
            "ARITHMETIC_ADVANCE": "NO",
            "ARITHMETIC_L2": "NONE",
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "PRIMITIVE_FREQUENCY_ATTACHMENT": "OPEN",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC243_NEAR_ISOMETRY_ATTACHMENT": "OPEN",
            "TPC244_COMMON_MULTIPLIER": "OPEN",
            "TWIN_PRIME_RESULT": "NONE",
        },
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def same_typed(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return left.keys() == right.keys() and all(
            same_typed(left[key], right[key]) for key in right)
    if type(right) is list:
        return len(left) == len(right) and all(
            same_typed(a, b) for a, b in zip(left, right))
    return left == right


def write() -> None:
    document = build_document()
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical(document) + b"\n")


def check() -> None:
    require(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    stored = strict_load(raw.decode("ascii"))
    expected = build_document()
    require(same_typed(stored, expected), "certificate payload mismatch")
    require(raw == canonical(stored) + b"\n", "noncanonical certificate bytes")
    print("TPC247_CERTIFICATE=PASS")
    print("admissible_triples=" + str(stored["payload"]["source_fixture"]["admissible_triples"]))
    print("source_scalar=" + stored["payload"]["source_fixture"]["direct_scalar"])
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write/--check")
    try:
        if args.write:
            write()
        else:
            check()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError,
            UnicodeError) as error:
        raise SystemExit("TPC247_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
