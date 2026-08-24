#!/usr/bin/env python3
"""Independent arithmetic audit for TPC-228."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CheckFailure(f"duplicate key: {key}")
        result[key] = value
    return result


def main() -> int:
    data = json.loads((PROJECT / "results/certificate.json").read_text(), object_pairs_hook=no_duplicates)
    require(data["schema"] == "tpc228-source-native-polarized-collision-compiler-v1", "schema")
    require(data["q25"] == {"Q": 25, "h": 400, "p": 37, "r": 47, "residues": [119, 281]}, "Q25")
    h2 = 400 * 400
    expected = {
        "positive": Fraction(4, h2),
        "negative": Fraction(-4, h2),
        "row_cancellation": Fraction(0),
        "directed": Fraction(2, h2),
        "one_coordinate": Fraction(1, h2),
    }
    fixtures = data["fixtures"]
    for name, value in expected.items():
        require(Fraction(fixtures[name]["four_phase_value"]) == value, f"polarized {name}")
        require(Fraction(fixtures[name]["direct_collision_value"]) == value, f"direct {name}")
    require(data["no_collision_control"]["four_phase_value"] == "0", "no collision")
    firewall = data["firewall"]
    require(firewall["actual_V59_to_primitive_atom_amplitude_crosswalk"] == "OPEN", "crosswalk")
    require(firewall["arithmetic_advance"] == "NO", "arithmetic")
    require(firewall["fixed_atom_credit"] == 0, "atom")
    print("TPC228_INDEPENDENT_CHECK=PASS")
    print("compiler=POLARIZED_AP_MINUS_DIAGONAL_TO_SOURCE_COLLISIONS")
    print("q25_controls=POSITIVE_NEGATIVE_ZERO_DIRECTED_SINGLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
