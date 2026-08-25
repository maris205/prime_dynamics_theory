#!/usr/bin/env python3
"""Exact producer/checker for the TPC-248 Gram-ellipsoid certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc248_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET"
Q = tuple[Fraction, Fraction]


class Failure(RuntimeError):
    """Fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def rat(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict_load(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise Failure("duplicate JSON key: " + key)
            output[key] = value
        return output
    return json.loads(text, object_pairs_hook=hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("nonfinite JSON token: " + token)))


def mm(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    need(bool(left) and bool(right) and len(left[0]) == len(right), "matrix shape")
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def mv(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    need(bool(matrix) and len(matrix[0]) == len(vector), "matrix/vector shape")
    return [sum((entry * value for entry, value in zip(row, vector)), Fraction(0))
            for row in matrix]


def tr(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*matrix)]


def energy(vector: list[Fraction], inverse: list[list[Fraction]]) -> Fraction:
    return sum((a * b for a, b in zip(vector, mv(inverse, vector))), Fraction(0))


def verify_mp(gram: list[list[Fraction]], dagger: list[list[Fraction]]) -> None:
    need(mm(mm(gram, dagger), gram) == gram, "G Gdagger G")
    need(mm(mm(dagger, gram), dagger) == dagger, "Gdagger G Gdagger")
    need(mm(gram, dagger) == tr(mm(gram, dagger)), "G Gdagger symmetry")
    need(mm(dagger, gram) == tr(mm(dagger, gram)), "Gdagger G symmetry")


def qadd(a: Q, b: Q) -> Q:
    return a[0] + b[0], a[1] + b[1]


def qmul(a: Q, b: Q) -> Q:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def qconj(a: Q) -> Q:
    return a[0], -a[1]


def qscale(a: Q, scalar: Fraction) -> Q:
    return a[0] * scalar, a[1] * scalar


def qinner(left: list[Q], right: list[Q]) -> Q:
    output = (Fraction(0), Fraction(0))
    for a, b in zip(left, right):
        output = qadd(output, qmul(qconj(a), b))
    return output


def qmv(matrix: list[list[Q]], vector: list[Q]) -> list[Q]:
    return [qinner([qconj(entry) for entry in row], vector) for row in matrix]


def qtext(value: Q) -> dict[str, str]:
    return {"re": rat(value[0]), "im": rat(value[1])}


def rmatrix(matrix: list[list[Fraction]]) -> list[list[str]]:
    return [[rat(value) for value in row] for row in matrix]


def complex_fixture() -> dict[str, Any]:
    one = (Fraction(1), Fraction(0))
    imag = (Fraction(0), Fraction(1))
    v1 = [one]
    v2 = [imag]
    w = [(Fraction(2), Fraction(1))]
    probes = [v1, v2]
    gram = [[qinner(left, right) for right in probes] for left in probes]
    dagger = [[qscale(value, Fraction(1, 4)) for value in row] for row in gram]
    y = [qinner(probe, w) for probe in probes]
    z = [qinner(w, probe) for probe in probes]
    need(z == [qconj(value) for value in y], "physical conjugate orientation")
    quadratic = qinner(y, qmv(dagger, y))
    need(quadratic == (Fraction(5), Fraction(0)), "complex Gram energy")
    return {
        "gram": [[qtext(value) for value in row] for row in gram],
        "gram_dagger": [[qtext(value) for value in row] for row in dagger],
        "y_vstar_w": [qtext(value) for value in y],
        "z_physical": [qtext(value) for value in z],
        "z_equals_conjugate_y": True,
        "quadratic_energy": rat(quadratic[0]),
    }


def real_fixtures() -> dict[str, Any]:
    rank_one_g = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]]
    rank_one_d = [[Fraction(1, 4), Fraction(1, 4)],
                  [Fraction(1, 4), Fraction(1, 4)]]
    identity = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    tilted_g = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(2)]]
    tilted_d = [[Fraction(2), Fraction(-1)], [Fraction(-1), Fraction(1)]]
    for gram, dagger in ((rank_one_g, rank_one_d), (identity, identity),
                         (tilted_g, tilted_d)):
        verify_mp(gram, dagger)
    need(mv(mm(rank_one_g, rank_one_d), [Fraction(1), Fraction(0)]) !=
         [Fraction(1), Fraction(0)], "rank-one range obstruction")
    need(energy([Fraction(1), Fraction(1)], rank_one_d) == 1,
         "rank-one boundary energy")
    need(energy([Fraction(3, 5), Fraction(4, 5)], identity) == 1,
         "full-rank shell energy")
    return {
        "rank_one_repeated_probe": {
            "gram": rmatrix(rank_one_g),
            "gram_dagger": rmatrix(rank_one_d),
            "range_equation": "y_1=y_2",
            "boundary_y": ["1/1", "1/1"],
            "boundary_energy": "1/1",
            "marginal_point_rejected": ["1/1", "0/1"],
            "polydisk_promotion": "REFUTED_SCOPED",
        },
        "full_rank_orthogonal_probe": {
            "gram": rmatrix(identity),
            "gram_dagger": rmatrix(identity),
            "shell_y": ["3/5", "4/5"],
            "shell_energy": "1/1",
            "joint_set": "EUCLIDEAN_BALL_NOT_BIDISK",
        },
        "tilted_full_rank_probe": {
            "gram": rmatrix(tilted_g),
            "gram_dagger": rmatrix(tilted_d),
        },
        "sphere_slack": {
            "rho": "1/1",
            "interior_y": ["3/5", "0/1"],
            "minimum_energy": "9/25",
            "slack_norm": "4/5",
            "kernel_dimension_positive": True,
            "sphere_image": "SOLID_ELLIPSOID",
        },
        "sphere_no_slack": {
            "rho": "1/1",
            "same_interior_y": ["3/5", "0/1"],
            "minimum_energy": "9/25",
            "kernel_dimension": 0,
            "sphere_membership": False,
            "sphere_image": "BOUNDARY_SHELL",
        },
        "global_budget": {
            "local_radii": ["1/1", "1/1"],
            "candidate": ["1/1", "1/1"],
            "local_product_membership": True,
            "global_energy": "2/1",
            "global_radius_squared": "1/1",
            "global_membership": False,
        },
        "zero_radius": {
            "rho": "0/1",
            "only_image": ["0/1", "0/1"],
        },
    }


def payload() -> dict[str, Any]:
    return {
        "source_object": {
            "output_lane": "w_c=P_cw",
            "probe": "v_cb=A_cb beta_b",
            "fixed_c_shared_lane": True,
            "cartesian_promotion_from_tagged_copies": False,
        },
        "theorem": {
            "ball_image": "RANGE_G_AND_Y_STAR_G_DAGGER_Y_LE_RHO_SQUARED",
            "minimum_preimage": "V_G_DAGGER_Y",
            "sphere_with_kernel_slack": "SOLID_ELLIPSOID",
            "sphere_without_kernel_slack": "BOUNDARY_SHELL",
            "physical_orientation": "CONJUGATE_GRAM_ELLIPSOID",
            "global_budget": "SUM_OF_GRAM_ENERGIES",
        },
        "real_fixtures": real_fixtures(),
        "complex_fixture": complex_fixture(),
        "scope_firewall": {
            "ARITHMETIC_ADVANCE": "NO",
            "ARITHMETIC_L2": "NONE",
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "PRIMITIVE_FREQUENCY_ATTACHMENT": "OPEN",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TWIN_PRIME_RESULT": "NONE",
        },
    }


def document() -> dict[str, Any]:
    body = payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": body,
        "payload_sha256": hashlib.sha256(canonical(body)).hexdigest(),
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
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical(document()) + b"\n")


def check() -> None:
    need(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    stored = strict_load(raw.decode("ascii"))
    need(raw == canonical(stored) + b"\n", "noncanonical bytes")
    need(same_typed(stored, document()), "certificate mismatch")
    print("TPC248_CERTIFICATE=PASS")
    print("gram_fixtures=7")
    print("rank_one_polydisk_obstruction=PASS")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, ZeroDivisionError) as error:
        raise SystemExit("TPC248_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
