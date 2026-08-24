#!/usr/bin/env python3
"""Independent TPC-238 checker; intentionally imports no producer module."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc238_certificate.json"


class IndependentFailure(RuntimeError):
    pass


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise IndependentFailure(message)


def normalized_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("ascii")


def circle_gap(left: Fraction, right: Fraction) -> Fraction:
    raw = abs(left - right)
    return min(raw, 1 - raw)


def independently_enumerate(height: int) -> list[tuple[int, int]]:
    output: list[tuple[int, int]] = []
    for denominator in range(1, height + 1):
        for numerator in range(denominator):
            if gcd(numerator, denominator) == 1:
                output.append((numerator, denominator))
    return sorted(output, key=lambda pair: Fraction(pair[0], pair[1]))


def independently_admit(
    entries: list[tuple[int, int]], height: int
) -> list[Fraction]:
    admitted: list[Fraction] = []
    for numerator, denominator in entries:
        ensure(type(numerator) is int, "noninteger numerator")
        ensure(type(denominator) is int, "noninteger denominator")
        ensure(1 <= denominator <= height, "height firewall")
        ensure(0 <= numerator < denominator, "mod-one firewall")
        ensure(gcd(numerator, denominator) == 1, "primitive firewall")
        candidate = Fraction(numerator, denominator)
        ensure(candidate not in admitted, "duplicate firewall")
        admitted.append(candidate)
    return admitted


def independently_weight(start: int, length: int) -> list[Fraction]:
    order = (length + 1) // 2
    center = start + order - 1
    return [
        max(Fraction(0, 1), Fraction(order - abs(n - center), order))
        for n in range(start, start + length)
    ]


def independently_gram(
    frequencies: list[Fraction],
    start: int,
    length: int,
    weights: list[Fraction] | None,
) -> np.ndarray:
    size = len(frequencies)
    matrix = np.zeros((size, size), dtype=np.complex128)
    for row, alpha in enumerate(frequencies):
        for column, beta in enumerate(frequencies):
            total = 0.0j
            for offset in range(length):
                multiplier = 1.0 if weights is None else float(weights[offset])
                phase = float(beta - alpha) * (start + offset)
                total += multiplier * complex(
                    math.cos(2.0 * math.pi * phase),
                    math.sin(2.0 * math.pi * phase),
                )
            matrix[row, column] = total
    return (matrix + matrix.conj().T) / 2.0


def close(left: float, right: float, tolerance: float = 2.0e-9) -> bool:
    return abs(left - right) <= tolerance


def verify_complex_phase_direction() -> None:
    """Exact-shape regression distinguishing beta-alpha from alpha-beta."""
    frequencies = [Fraction(0, 1), Fraction(1, 3)]
    weights = independently_weight(0, 3)
    gram = independently_gram(frequencies, 0, 3, weights)
    coefficients = np.asarray([1.0 + 0.0j, 0.0 + 1.0j], dtype=np.complex128)
    matrix_energy = float(np.vdot(coefficients, gram @ coefficients).real)
    direct_energy = 0.0
    for n, weight in enumerate(weights):
        value = sum(
            coefficients[index]
            * complex(
                math.cos(2.0 * math.pi * float(frequency) * n),
                math.sin(2.0 * math.pi * float(frequency) * n),
            )
            for index, frequency in enumerate(frequencies)
        )
        direct_energy += float(weight) * abs(value) ** 2
    correct = 4.0 - math.sqrt(3.0) / 2.0
    reversed_phase = 4.0 + math.sqrt(3.0) / 2.0
    ensure(close(direct_energy, correct), "direct complex phase fixture")
    ensure(close(matrix_energy, correct), "beta-minus-alpha Gram direction")
    ensure(not close(matrix_energy, reversed_phase), "reversed phase was accepted")


def verify() -> dict[str, Any]:
    ensure(CERTIFICATE.is_file(), "missing certificate")
    document = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    supplied_digest = document.get("payload_sha256")
    payload = dict(document)
    payload.pop("payload_sha256", None)
    computed_digest = hashlib.sha256(normalized_json(payload)).hexdigest()
    ensure(supplied_digest == computed_digest, "payload digest mismatch")

    markers = document["markers"]
    expected_markers = {
        "TPC238_ROUTE_ADVANCE": "YES",
        "TPC238_TRIANGULAR_WINDOW_LOWER_FRAME": "PROVED_EXACT",
        "TPC238_PRIMITIVE_FAREY_SPACING": "PROVED_U_TO_MINUS_2",
        "TPC238_FEJER_OFFDIAGONAL": (
            "PROVED_LE_1_OVER_4L_DISTANCE_SQUARED"
        ),
        "TPC238_CIRCULAR_PACKING_ROW_SUM": (
            "PROVED_LE_PI_SQUARED_U_FOUR_OVER_3"
        ),
        "TPC238_LOWER_FRAME": (
            "PROVED_L_MINUS_PI_SQUARED_U_FOUR_OVER_12L_POSITIVE_PART"
        ),
        "TPC238_NORMALIZED_LOWER_FRAME": (
            "PROVED_HALF_MINUS_PI_SQUARED_U_FOUR_OVER_6N_SQUARED_POSITIVE_PART"
        ),
        "TPC238_V59_FRAME_DEFECT": "PROVED_X_MINUS_67_OVER_100",
        "TPC238_CROSS_REDUCED_FREQUENCY_FIXED_POWER_SAVING": (
            "REFUTED_SCOPED_AFTER_Q_COLLAPSE"
        ),
        "TPC238_WITHIN_Q_BUCKET_CANCELLATION": "OPEN",
        "TPC238_STATUS": "PROVED_STRUCTURAL_OBSTRUCTION_L1",
        "TPC238_ROUND2_CLUE": (
            "MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS"
        ),
    }
    ensure(markers == expected_markers, "status marker mismatch")

    firewall = document["scope_firewall"]
    ensure(firewall["ARITHMETIC_ADVANCE"] == "NO", "arithmetic overclaim")
    ensure(firewall["C_H_SIGNED_CANCELLATION"] == "NONE", "C_h overclaim")
    ensure(firewall["FULL_GATE_B"] == "OPEN", "Gate-B overclaim")
    ensure(firewall["STRICT_1_OVER_400"] == "UNPAID_GLOBAL", "saving overclaim")
    ensure(not any(firewall["ROUTE_A"].values()), "Route-A overclaim")
    ensure(firewall["SHARPNESS"] == "NOT_CLAIMED", "sharpness overclaim")

    fixture = document["fixture"]
    height = fixture["U"]
    length = fixture["N"]
    order = (length + 1) // 2
    ensure(order == fixture["L"], "triangular order mismatch")
    pairs = independently_enumerate(height)
    encoded_pairs = [(item["a"], item["h"]) for item in fixture["fractions"]]
    ensure(pairs == encoded_pairs, "primitive enumeration mismatch")
    frequencies = independently_admit(pairs, height)

    minimum = min(
        circle_gap(frequencies[i], frequencies[j])
        for i in range(len(frequencies))
        for j in range(i + 1, len(frequencies))
    )
    ensure(str(minimum) == fixture["minimum_circular_spacing_exact"], "spacing")
    ensure(minimum >= Fraction(1, height**2), "Farey floor")

    first_weights = independently_weight(fixture["window_starts"][0], length)
    ensure(sum(first_weights, Fraction(0, 1)) == order, "weight sum")
    ensure(
        sum(weight > 0 for weight in first_weights) == 2 * order - 1,
        "support size",
    )

    exact = document["exact_theorem_ledger"]
    ensure(exact["classification"] == "EXACT_THEOREM_LEDGER", "ledger class")
    ensure(
        exact["v59_exponent_identity"] == "4*(133/400)-2=-67/100",
        "V59 exponent",
    )
    ensure(Fraction(4 * 133, 400) - 2 == Fraction(-67, 100), "exponent math")

    theorem_bound = max(
        0.0, order - math.pi * math.pi * height**4 / (12.0 * order)
    )
    normalized_bound = max(
        0.0, 0.5 - math.pi * math.pi * height**4 / (6.0 * length**2)
    )
    numerical = document["numerical_checks"]
    ensure(
        numerical["classification"] == "NUMERICALLY_CERTIFIED_FINITE_CHECK",
        "numerical class",
    )
    ensure(
        close(numerical["analytic_lower_bound_approx"], theorem_bound),
        "analytic bound encoding",
    )
    ensure(
        close(
            numerical["normalized_theorem_lower_bound_approx"],
            normalized_bound,
        ),
        "normalized bound encoding",
    )

    reference_hard: np.ndarray | None = None
    reference_weighted: np.ndarray | None = None
    rows = numerical["windows"]
    ensure(len(rows) == len(fixture["window_starts"]), "window count")
    for row, start in zip(rows, fixture["window_starts"]):
        weights = independently_weight(start, length)
        weighted = independently_gram(frequencies, start, length, weights)
        hard = independently_gram(frequencies, start, length, None)
        weighted_eigenvalues = np.linalg.eigvalsh(weighted)
        hard_eigenvalues = np.linalg.eigvalsh(hard)
        weighted_minimum = float(weighted_eigenvalues[0])
        hard_minimum = float(hard_eigenvalues[0])
        ensure(weighted_minimum + 2.0e-9 >= theorem_bound, "lower frame")
        ensure(hard_minimum + 2.0e-9 >= weighted_minimum, "minorant direction")
        ensure(
            close(row["triangular_gram_min_eigenvalue"], weighted_minimum),
            "weighted eigenvalue encoding",
        )
        ensure(
            close(row["hard_gram_min_eigenvalue"], hard_minimum),
            "hard eigenvalue encoding",
        )
        if reference_hard is None:
            reference_hard = hard_eigenvalues
            reference_weighted = weighted_eigenvalues
        else:
            ensure(
                float(np.max(np.abs(hard_eigenvalues - reference_hard))) < 2.0e-9,
                "hard translation spectrum",
            )
            ensure(
                float(
                    np.max(np.abs(weighted_eigenvalues - reference_weighted))
                )
                < 2.0e-9,
                "weighted translation spectrum",
            )

    mutation_inputs = {
        "denominator_above_U": [(0, 1), (1, height + 1)],
        "duplicate_frequency": [(0, 1), (1, 2), (1, 2)],
        "nonprimitive_fraction": [(0, 1), (2, 4)],
    }
    rejected: list[str] = []
    for name, mutation in mutation_inputs.items():
        try:
            independently_admit(mutation, height)
        except IndependentFailure:
            rejected.append(name)
        else:
            raise IndependentFailure(f"accepted mutation: {name}")
    ensure(
        sorted(rejected) == document["mutation_firewalls"]["rejected"],
        "mutation ledger",
    )

    source = Path(__file__).read_text(encoding="utf-8")
    forbidden_import = "import " + "tpc238_lower_frame_certificate"
    ensure(forbidden_import not in source, "independent checker imports producer")
    verify_complex_phase_direction()

    return {
        "TPC238_INDEPENDENT_CHECK": "PASS",
        "complex_phase_direction": "BETA_MINUS_ALPHA_PASS",
        "digest": supplied_digest,
        "fractions": len(frequencies),
        "mutations_rejected": len(rejected),
        "producer_imports": 0,
        "windows": len(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(verify(), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IndependentFailure as error:
        raise SystemExit(f"TPC238_INDEPENDENT_CHECK=FAIL: {error}")
