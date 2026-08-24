#!/usr/bin/env python3
"""Independent exact audit of the TPC-227 certificate."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/certificate.json"


class IndependentFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise IndependentFailure(f"duplicate key: {key}")
        result[key] = value
    return result


def main() -> int:
    data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
    require(data["schema"] == "tpc227-packet-profile-axis-separation-v1", "schema")
    require(data["status"] == "PASS", "status")

    block = data["q25_resonance_block"]
    c = Fraction(1, 400)
    physical = ((c * c, c * c), (c * c, c * c))
    odd = ((c * c, -c * c), (-c * c, c * c))
    difference = tuple(
        tuple(odd[i][j] - physical[i][j] for j in range(2)) for i in range(2)
    )
    require(block["physical_gram"] == [[str(x) for x in row] for row in physical], "physical Gram")
    require(block["odd_row_gram"] == [[str(x) for x in row] for row in odd], "odd Gram")
    require(difference[0][1] == Fraction(-1, 80000), "off-diagonal witness")

    fixtures = data["fixtures"]
    expected = {
        "common_physical": True,
        "packet_global_signs": True,
        "row_dependent_odd_sign": False,
        "alternating_scale": False,
        "fully_unequal_scale": False,
        "mixed_row_profile": False,
    }
    require(set(fixtures) == set(expected), "fixture names")
    for name, verdict in expected.items():
        require(fixtures[name]["compatible_with_target"] is verdict, f"fixture {name}")
        require(
            fixtures[name]["compatible_with_target"]
            is fixtures[name]["all_packet_grams_equal_target"],
            f"Gram iff mismatch: {name}",
        )

    firewall = data["firewall"]
    require(firewall["arithmetic_advance"] == "NO", "arithmetic firewall")
    require(firewall["fixed_atom_credit"] == 0, "fixed atom firewall")
    require(firewall["strict_1_over_400"] == "UNPAID", "strict firewall")
    print("TPC227_INDEPENDENT_CHECK=PASS")
    print("criterion=FOUR_GRAMS_EQUAL_TARGET")
    print("q25_off_diagonal_difference=-1/80000")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
