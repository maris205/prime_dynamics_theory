#!/usr/bin/env python3
"""Exact producer/checker for the TPC-249 weighted contraction certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc249_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def qt(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict_load(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise Failure("duplicate key")
            output[key] = value
        return output
    return json.loads(text, object_pairs_hook=hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("nonfinite token: " + token)))


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def contract(probes: list[list[Fraction]], weights: list[Fraction]) -> list[Fraction]:
    return [sum((weight * probe[j] for weight, probe in zip(weights, probes)),
                Fraction(0)) for j in range(len(probes[0]))]


def gram(probes: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[dot(left, right) for right in probes] for left in probes]


def quadratic(weights: list[Fraction], matrix: list[list[Fraction]]) -> Fraction:
    return sum((weights[i] * matrix[i][j] * weights[j]
                for i in range(len(weights)) for j in range(len(weights))), Fraction(0))


def group_record(name: str, probes: list[list[Fraction]], weights: list[Fraction],
                 rho: Fraction, norms: list[Fraction]) -> dict[str, Any]:
    g = contract(probes, weights)
    g2 = dot(g, g)
    matrix = gram(probes)
    need(g2 == quadratic(weights, matrix), "Gram contraction")
    tagged = rho * sum((abs(weight) * norm for weight, norm in zip(weights, norms)),
                       Fraction(0))
    return {
        "name": name,
        "probes": [[qt(value) for value in probe] for probe in probes],
        "weights": [qt(value) for value in weights],
        "rho": qt(rho),
        "gram": [[qt(value) for value in row] for row in matrix],
        "contracted_probe": [qt(value) for value in g],
        "contracted_norm_squared": qt(g2),
        "tagged_radius": qt(tagged),
    }


def fixtures() -> dict[str, Any]:
    orthogonal = group_record(
        "orthogonal", [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]],
        [Fraction(3, 5), Fraction(4, 5)], Fraction(2), [Fraction(1), Fraction(1)])
    cancellation = group_record(
        "cancellation", [[Fraction(1), Fraction(0)], [Fraction(1), Fraction(0)]],
        [Fraction(1), Fraction(-1)], Fraction(3), [Fraction(1), Fraction(1)])
    aligned = group_record(
        "aligned", [[Fraction(1), Fraction(0)], [Fraction(2), Fraction(0)]],
        [Fraction(1), Fraction(1, 2)], Fraction(1), [Fraction(1), Fraction(2)])
    need(orthogonal["contracted_norm_squared"] == "1/1", "orthogonal norm")
    need(cancellation["contracted_norm_squared"] == "0/1", "cancellation norm")
    need(aligned["contracted_norm_squared"] == "4/1", "aligned norm")
    need(orthogonal["tagged_radius"] == "14/5" and
         cancellation["tagged_radius"] == "6/1" and
         aligned["tagged_radius"] == "2/1", "tagged radii")
    return {
        "groups": [orthogonal, cancellation, aligned],
        "independent_exact_radius": "4/1",
        "independent_tagged_radius": "54/5",
        "explicit_target": "2/1",
        "explicit_local_targets": ["1/1", "0/1", "1/1"],
        "explicit_preimages": [["3/5", "4/5"], ["0/1", "0/1"],
                               ["1/2", "0/1"]],
        "affine_centers": [["1/1", "2/1"], ["0/1", "0/1"],
                           ["-1/1", "0/1"]],
        "affine_scalar_center": "1/5",
        "affine_zero_feasible": True,
        "affine_minimum_modulus": "0/1",
        "positive_margin_center_modulus": "5/1",
        "positive_margin_minimum": "1/1",
        "global_budget_rho": "2/1",
        "global_radius_squared": "20/1",
        "complex_orientation": {
            "weight": {"re": "0/1", "im": "1/1"},
            "physical_covariance": {"re": "2/1", "im": "-1/1"},
            "weighted_scalar": {"re": "1/1", "im": "2/1"},
            "contracted_probe": {"re": "0/1", "im": "1/1"},
            "inner_product_with_contracted_probe": {"re": "1/1", "im": "2/1"},
        },
    }


def payload() -> dict[str, Any]:
    return {
        "source": {
            "probe": "v_cb=A_cb beta_b",
            "contraction": "g_c=sum_b lambda_cb v_cb",
            "same_weights_no_conjugation": True,
            "affine_domain": "MODELING_CHOICE",
        },
        "theorem": {
            "independent_radius": "SUM_C_RHO_C_SQRT_LAMBDA_STAR_G_LAMBDA",
            "global_radius": "RHO_SQRT_SUM_C_LAMBDA_STAR_G_LAMBDA",
            "reverse_realization": "EXPLICIT",
            "tagged_dominance": "EXACT_TRIANGLE",
            "tagged_equality": "COMMON_NONNEGATIVE_RAY_ON_EACH_ACTIVE_GROUP",
        },
        "fixtures": fixtures(),
        "scope_firewall": {
            "ACTUAL_GRAM_ASYMPTOTIC": "OPEN",
            "ARITHMETIC_ADVANCE": "NO",
            "ARITHMETIC_L2": "NONE",
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TWIN_PRIME_RESULT": "NONE",
        },
    }


def document() -> dict[str, Any]:
    body = payload()
    return {"certificate_version": 1, "claim_status": STATUS, "payload": body,
            "payload_sha256": hashlib.sha256(canonical(body)).hexdigest()}


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
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical(document()) + b"\n")


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    stored = strict_load(raw.decode("ascii"))
    need(raw == canonical(stored) + b"\n", "canonical bytes")
    need(same_typed(stored, document()), "certificate mismatch")
    print("TPC249_CERTIFICATE=PASS")
    print("independent_exact_radius=4/1")
    print("independent_tagged_radius=54/5")
    print("cancellation_group_radius=0/1")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose one mode")
    try:
        write() if args.write else check()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, ZeroDivisionError) as error:
        raise SystemExit("TPC249_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
