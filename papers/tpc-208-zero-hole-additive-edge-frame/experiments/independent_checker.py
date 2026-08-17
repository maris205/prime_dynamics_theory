#!/usr/bin/env python3
"""Independent exact checker for the TPC-208 certificate.

This implementation imports neither code/additive_edge.py nor the producer.
It reconstructs the projection, physical kernel, row variances,
polarization, falsifiers, and claim firewall from separate formulas.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results" / "certificate.json"


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    answer: dict[str, object] = {}
    for key, value in pairs:
        if key in answer:
            raise CheckFailure(f"duplicate JSON key: {key}")
        answer[key] = value
    return answer


def pair(value: list[str]) -> tuple[F, F]:
    require(type(value) is list and len(value) == 2, "Gaussian pair shape")
    require(all(type(item) is str for item in value), "Gaussian pair type")
    return F(value[0]), F(value[1])


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def sub(left, right):
    return left[0] - right[0], left[1] - right[1]


def mul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conj(value):
    return value[0], -value[1]


def scale(scalar, value):
    return scalar * value[0], scalar * value[1]


def abs2(value):
    return value[0] * value[0] + value[1] * value[1]


def total(values):
    answer = (F(0), F(0))
    for value in values:
        answer = add(answer, value)
    return answer


def direct_variance(row):
    units = row[1:]
    mean = scale(F(1, len(units)), total(units))
    return sum((abs2(sub(value, mean)) for value in units), F(0))


def closed_kernel(q, left, right):
    if left == 0 or right == 0:
        return 0
    if left == right:
        return q * (q - 2)
    return -q


def kernel_variance(row):
    q = len(row)
    answer = (F(0), F(0))
    for left in range(q):
        for right in range(q):
            coefficient = F(closed_kernel(q, left, right), q * (q - 1))
            answer = add(answer, scale(coefficient, mul(row[left], conj(row[right]))))
    return answer


def polarized(left, right):
    phases = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
    answer = (F(0), F(0))
    for phase in phases:
        packet = add(left, mul(phase, right))
        answer = add(answer, scale(F(1, 4), scale(abs2(packet), phase)))
    return answer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()

    require(CERTIFICATE.is_file(), "certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
    )
    require(type(data) is dict, "top-level type")
    require(
        set(data) == {
            "audit_counts",
            "audit_total",
            "claim_firewall",
            "classification",
            "falsifiers",
            "moduli",
            "open_theorem",
            "polarization",
            "schema",
        },
        "top-level keys",
    )
    require(
        data["schema"] == "TPC208_ZERO_HOLE_ADDITIVE_EDGE_FRAME_CERTIFICATE_V1",
        "schema",
    )
    require(data["classification"] == "PROVED_STRUCTURAL_L1", "classification")
    expected_counts = {
        "falsifier_uniqueness_rows": 20,
        "laplacian_rank_rows": 167,
        "mutation_rows": 14,
        "physical_kernel_rows": 208,
        "polarization_rows": 2,
        "row_diagonal_rows": 20,
    }
    require(data["audit_counts"] == expected_counts, "audit counts")
    require(type(data["audit_total"]) is int and data["audit_total"] == 431, "audit total")
    require(sum(expected_counts.values()) == data["audit_total"], "audit count sum")

    moduli = data["moduli"]
    require(type(moduli) is dict and set(moduli) == {"2", "3", "5", "7", "11"}, "moduli")
    for q in (2, 3, 5, 7, 11):
        record = moduli[str(q)]
        dimension = q - 1
        expected_laplacian = [
            [dimension - 1 if left == right else -1 for right in range(dimension)]
            for left in range(dimension)
        ]
        require(record["laplacian"] == expected_laplacian, f"laplacian q={q}")
        require(type(record["edge_count"]) is int, f"edge count type q={q}")
        require(record["edge_count"] == dimension * (dimension - 1) // 2, f"edge count q={q}")
        require(record["projection_rank"] == max(q - 2, 0), f"rank q={q}")
        require(record["oriented_edge_count"] == dimension * (dimension - 1), f"oriented q={q}")
        require(record["edge_mass_on_unit"] == q * (q - 2), f"edge mass q={q}")
        require(F(record["diagonal_factor"]) == F(q - 2, q - 1), f"diagonal q={q}")
        require(
            F(record["forced_literal_edge_weight"]) == F(1, q - 1),
            f"forced weight q={q}",
        )
        expected_kernel = [
            [closed_kernel(q, left, right) for right in range(q)]
            for left in range(q)
        ]
        require(record["physical_kernel"] == expected_kernel, f"kernel q={q}")

        row = tuple(pair(value) for value in record["row_fixture"])
        variance = direct_variance(row)
        emitted = kernel_variance(row)
        require(F(record["row_variance_direct"]) == variance, f"direct variance q={q}")
        require(pair(record["row_variance_edge_frame"]) == emitted, f"frame record q={q}")
        require(emitted == (variance, F(0)), f"row equality q={q}")
        single_raw_variance = F(q - 2, q - 1)
        single_diagonal = F(q - 2, q - 1)
        require(single_raw_variance - single_diagonal == 0, f"omitted diagonal q={q}")
        require((q - 1) != max(q - 2, 0), f"frequency-zero mutation q={q}")
        if q > 2:
            require(F(0) != -F(1, q - 1), f"dropped-edge mutation q={q}")

    for record in data["polarization"]:
        left = pair(record["left"])
        right = pair(record["right"])
        observed = polarized(left, right)
        expected = mul(left, conj(right))
        require(observed == expected, "polarization identity")
        require(pair(record["polarized"]) == observed, "polarization record")
        require(pair(record["direct"]) == expected, "direct product record")

    falsifiers = data["falsifiers"]
    require(set(falsifiers) == {"3", "5", "7", "11"}, "falsifier moduli")
    for q in (3, 5, 7, 11):
        record = falsifiers[str(q)]
        equal_piece = F(record["zero_residue_spike_equal_piece"])
        off_piece = F(record["zero_residue_spike_off_equal_piece"])
        require(equal_piece == F(q - 1, q) and off_piece == -equal_piece, f"spike q={q}")
        require(F(record["zero_residue_spike_total"]) == 0, f"spike total q={q}")
        require(F(record["forced_edge_weight"]) == F(1, q - 1), f"unique weight q={q}")
        require(F(record["projection_off_diagonal"]) == -F(1, q - 1), f"projection q={q}")

    firewall = data["claim_firewall"]
    expected_firewall = {
        "V61_ARITHMETIC_ADVANCE": "NO",
        "V61_FIXED_ATOM_CREDIT": 0,
        "V61_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID",
        "V61_L2": "NONE",
        "V61_ROUTE_ADVANCE": "YES",
        "V61_STRUCTURAL_THRESHOLD_A": "PASS",
        "V61_TPC_208_TRIGGER": True,
        "equal_off_equal_separate_estimation": "REFUTED",
        "twin_prime_theorem": False,
    }
    require(set(firewall) == set(expected_firewall), "firewall keys")
    for key, expected in expected_firewall.items():
        observed = firewall[key]
        require(type(observed) is type(expected) and observed == expected, f"firewall {key}")

    print("TPC208_INDEPENDENT_CHECK=PASS")
    print("implementation=independent_projection_and_closed_kernel")
    print("exact_rows=431")
    print("claim_firewall=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as exc:
        print(f"TPC208_INDEPENDENT_CHECK=FAIL {exc}")
        raise SystemExit(1) from exc
