#!/usr/bin/env python3
"""Deterministic producer for the TPC-238 finite-window certificate."""

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


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = PROJECT_ROOT / "results" / "tpc238_certificate.json"

MARKERS = {
    "TPC238_ROUTE_ADVANCE": "YES",
    "TPC238_TRIANGULAR_WINDOW_LOWER_FRAME": "PROVED_EXACT",
    "TPC238_PRIMITIVE_FAREY_SPACING": "PROVED_U_TO_MINUS_2",
    "TPC238_FEJER_OFFDIAGONAL": "PROVED_LE_1_OVER_4L_DISTANCE_SQUARED",
    "TPC238_CIRCULAR_PACKING_ROW_SUM": "PROVED_LE_PI_SQUARED_U_FOUR_OVER_3",
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

FIREWALL = {
    "ARITHMETIC_ADVANCE": "NO",
    "C_H_SIGNED_CANCELLATION": "NONE",
    "FIXED_ATOM": 0,
    "FULL_GATE_B": "OPEN",
    "L2": "NONE",
    "ROUTE_A": {
        "A0": False,
        "A1": False,
        "A2": False,
        "A3": False,
        "A4": False,
    },
    "SHARPNESS": "NOT_CLAIMED",
    "SIGNED_FOUR_PACKET_PROJECTION": "OPEN",
    "STRICT_1_OVER_400": "UNPAID_GLOBAL",
}


class CertificateFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateFailure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("ascii")


def payload_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def primitive_fractions(height: int) -> list[tuple[int, int]]:
    require(height >= 1, "height must be positive")
    entries = [(0, 1)]
    for denominator in range(2, height + 1):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) == 1:
                entries.append((numerator, denominator))
    entries.sort(key=lambda pair: Fraction(pair[0], pair[1]))
    return entries


def validate_fractions(
    entries: list[tuple[int, int]], height: int
) -> list[Fraction]:
    values: list[Fraction] = []
    seen: set[Fraction] = set()
    for numerator, denominator in entries:
        require(isinstance(numerator, int), "numerator must be an integer")
        require(isinstance(denominator, int), "denominator must be an integer")
        require(denominator >= 1, "denominator must be positive")
        require(denominator <= height, "denominator exceeds U")
        require(0 <= numerator < denominator, "fraction is not reduced modulo one")
        require(gcd(numerator, denominator) == 1, "fraction is not primitive")
        value = Fraction(numerator, denominator)
        require(value not in seen, "duplicate frequency")
        seen.add(value)
        values.append(value)
    return values


def circular_distance(left: Fraction, right: Fraction) -> Fraction:
    gap = abs(left - right)
    return min(gap, 1 - gap)


def minimum_spacing(values: list[Fraction]) -> Fraction:
    require(len(values) >= 2, "spacing fixture needs at least two frequencies")
    return min(
        circular_distance(values[i], values[j])
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )


def triangular_weights(start: int, length: int) -> dict[int, Fraction]:
    require(length >= 1, "interval length must be positive")
    order = (length + 1) // 2
    center = start + order - 1
    return {
        center + offset: Fraction(order - abs(offset), order)
        for offset in range(-(order - 1), order)
    }


def frequency_vector(values: list[Fraction]) -> np.ndarray:
    return np.asarray([float(value) for value in values], dtype=np.float64)


def gram_matrix(
    values: list[Fraction],
    start: int,
    length: int,
    triangular: bool,
) -> np.ndarray:
    frequencies = frequency_vector(values)
    integers = np.arange(start, start + length, dtype=np.float64)
    vandermonde = np.exp(
        2j * math.pi * np.outer(integers, frequencies)
    )
    if triangular:
        exact_weights = triangular_weights(start, length)
        weights = np.asarray(
            [float(exact_weights.get(int(n), Fraction(0, 1))) for n in integers],
            dtype=np.float64,
        )
        return vandermonde.conj().T @ (weights[:, None] * vandermonde)
    return vandermonde.conj().T @ vandermonde


def rounded(value: float) -> float:
    return float(f"{value:.12f}")


def fejer(order: int, theta: float) -> float:
    distance = abs(theta - round(theta))
    if distance < 1.0e-15:
        return float(order)
    numerator = math.sin(math.pi * order * theta)
    denominator = math.sin(math.pi * theta)
    return (numerator / denominator) ** 2 / order


def finite_matrix_checks(
    values: list[Fraction], height: int, length: int, starts: list[int]
) -> dict[str, Any]:
    order = (length + 1) // 2
    analytic_lower = max(
        0.0, order - math.pi * math.pi * height**4 / (12.0 * order)
    )
    normalized_lower = max(
        0.0, 0.5 - math.pi * math.pi * height**4 / (6.0 * length**2)
    )
    window_rows: list[dict[str, Any]] = []
    weighted_minima: list[float] = []
    hard_minima: list[float] = []
    for start in starts:
        weighted = gram_matrix(values, start, length, triangular=True)
        hard = gram_matrix(values, start, length, triangular=False)
        hermitian_weighted = (weighted + weighted.conj().T) / 2.0
        hermitian_hard = (hard + hard.conj().T) / 2.0
        weighted_eigenvalues = np.linalg.eigvalsh(hermitian_weighted)
        hard_eigenvalues = np.linalg.eigvalsh(hermitian_hard)
        weighted_min = float(weighted_eigenvalues[0])
        hard_min = float(hard_eigenvalues[0])
        require(
            weighted_min + 1.0e-9 >= analytic_lower,
            "weighted Gram matrix violates theorem lower bound",
        )
        require(
            hard_min + 1.0e-9 >= weighted_min,
            "hard-window Gram matrix is below triangular Gram matrix",
        )
        weighted_minima.append(weighted_min)
        hard_minima.append(hard_min)
        window_rows.append(
            {
                "hard_gram_min_eigenvalue": rounded(hard_min),
                "hard_normalized_min_eigenvalue": rounded(hard_min / length),
                "start": start,
                "triangular_gram_min_eigenvalue": rounded(weighted_min),
                "triangular_normalized_min_eigenvalue": rounded(
                    weighted_min / length
                ),
            }
        )

    reference_weighted = weighted_minima[0]
    reference_hard = hard_minima[0]
    require(
        max(abs(value - reference_weighted) for value in weighted_minima)
        < 1.0e-9,
        "translated triangular Gram spectra are not invariant",
    )
    require(
        max(abs(value - reference_hard) for value in hard_minima) < 1.0e-9,
        "translated hard-window Gram spectra are not invariant",
    )

    packing_sums: list[float] = []
    fejer_ratios: list[float] = []
    for index, left in enumerate(values):
        inverse_square_sum = 0.0
        for other_index, right in enumerate(values):
            if index == other_index:
                continue
            distance = float(circular_distance(left, right))
            inverse_square_sum += 1.0 / (distance * distance)
            ratio = 4.0 * order * distance * distance * fejer(
                order, float(left - right)
            )
            fejer_ratios.append(ratio)
        packing_sums.append(inverse_square_sum)
    require(max(fejer_ratios) <= 1.0 + 1.0e-12, "Fejer mutation detected")
    packing_cap = math.pi * math.pi * height**4 / 3.0
    require(max(packing_sums) <= packing_cap, "packing cap violated")

    coefficients = np.asarray(
        [
            complex((index + 1) / 7.0, ((-1) ** index) * (index + 2) / 11.0)
            for index in range(len(values))
        ],
        dtype=np.complex128,
    )
    coefficient_energy = float(np.vdot(coefficients, coefficients).real)
    direct_ratios: list[float] = []
    for start in starts:
        hard = gram_matrix(values, start, length, triangular=False)
        energy = float(np.vdot(coefficients, hard @ coefficients).real)
        ratio = energy / coefficient_energy
        require(ratio + 1.0e-9 >= analytic_lower, "direct energy check failed")
        direct_ratios.append(ratio)

    return {
        "classification": "NUMERICALLY_CERTIFIED_FINITE_CHECK",
        "analytic_lower_bound_approx": rounded(analytic_lower),
        "direct_test_vector_min_energy_ratio": rounded(min(direct_ratios)),
        "fejer_offdiagonal_max_bound_ratio": rounded(max(fejer_ratios)),
        "max_inverse_square_row_sum": rounded(max(packing_sums)),
        "normalized_theorem_lower_bound_approx": rounded(normalized_lower),
        "packing_row_sum_cap_approx": rounded(packing_cap),
        "translation_spectrum_tolerance": 1.0e-9,
        "windows": window_rows,
    }


def mutation_checks(height: int) -> dict[str, Any]:
    cases = {
        "denominator_above_U": [(0, 1), (1, height + 1)],
        "duplicate_frequency": [(0, 1), (1, 2), (1, 2)],
        "nonprimitive_fraction": [(0, 1), (2, 4)],
    }
    rejected: list[str] = []
    for name, entries in cases.items():
        try:
            validate_fractions(entries, height)
        except CertificateFailure:
            rejected.append(name)
        else:
            raise CertificateFailure(f"mutation was accepted: {name}")
    return {
        "classification": "NUMERICALLY_CERTIFIED_FINITE_CHECK",
        "rejected": sorted(rejected),
        "rejected_count": len(rejected),
    }


def build_payload() -> dict[str, Any]:
    height = 4
    length = 41
    order = (length + 1) // 2
    starts = [-20, 0, 17, 103]
    entries = primitive_fractions(height)
    values = validate_fractions(entries, height)
    spacing = minimum_spacing(values)
    weights = triangular_weights(starts[0], length)
    require(sum(weights.values(), Fraction(0, 1)) == order, "weight sum mismatch")
    require(len(weights) == 2 * order - 1, "triangular support mismatch")
    require(spacing >= Fraction(1, height**2), "Farey spacing mismatch")

    exact_ledger = {
        "classification": "EXACT_THEOREM_LEDGER",
        "fejer_offdiagonal": "F_L(theta) <= 1/(4*L*||theta||^2)",
        "lower_frame": (
            "E_I(z) >= [L - pi^2*U^4/(12*L)]_+ * sum_alpha |z_alpha|^2"
        ),
        "normalized_lower_frame": (
            "E_I(z)/N >= [1/2 - pi^2*U^4/(6*N^2)]_+"
            " * sum_alpha |z_alpha|^2"
        ),
        "packing_row_sum": (
            "sum_{beta!=alpha} ||alpha-beta||^-2 <= pi^2/(3*delta^2)"
        ),
        "primitive_spacing": "delta >= U^-2",
        "triangular_order": "L=floor((N+1)/2)",
        "v59_exponent_identity": "4*(133/400)-2=-67/100",
    }
    fixture = {
        "classification": "MODELING_CHOICE",
        "L": order,
        "N": length,
        "U": height,
        "fractions": [
            {"a": numerator, "h": denominator}
            for numerator, denominator in entries
        ],
        "minimum_circular_spacing_exact": str(spacing),
        "normalized_lower_bound_symbolic": "1/2 - 128*pi^2/5043",
        "theorem_lower_bound_symbolic": "21 - 64*pi^2/63",
        "theorem_spacing_floor_exact": str(Fraction(1, height**2)),
        "triangular_support_size": len(weights),
        "triangular_weight_sum_exact": str(sum(weights.values(), Fraction(0, 1))),
        "window_starts": starts,
    }
    numerical_checks = finite_matrix_checks(values, height, length, starts)
    mutations = mutation_checks(height)
    observation = {
        "classification": "NUMERICAL_OBSERVATION",
        "statement": (
            "For the finite fixture, the actual Gram minima exceed the"
            " universal theorem constants; no sharpness inference is made."
        ),
    }
    return {
        "artifact": "TPC-238 finite-window lower-frame certificate",
        "date": "2026-08-24",
        "exact_theorem_ledger": exact_ledger,
        "fixture": fixture,
        "markers": MARKERS,
        "mutation_firewalls": mutations,
        "numerical_checks": numerical_checks,
        "numerical_observation": observation,
        "scope_firewall": FIREWALL,
        "schema_version": 1,
    }


def build_certificate() -> dict[str, Any]:
    payload = build_payload()
    return {**payload, "payload_sha256": payload_digest(payload)}


def write_certificate() -> dict[str, Any]:
    certificate = build_certificate()
    CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE_PATH.write_text(
        json.dumps(certificate, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return certificate


def check_certificate() -> dict[str, Any]:
    require(CERTIFICATE_PATH.is_file(), "certificate is missing")
    loaded = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    expected = build_certificate()
    require(loaded == expected, "certificate bytes do not encode expected payload")
    digest = loaded.get("payload_sha256")
    payload = dict(loaded)
    payload.pop("payload_sha256", None)
    require(digest == payload_digest(payload), "certificate digest mismatch")
    return loaded


def summary(certificate: dict[str, Any], action: str) -> dict[str, Any]:
    checks = certificate["numerical_checks"]
    return {
        "TPC238_CERTIFICATE": "PASS",
        "action": action,
        "digest": certificate["payload_sha256"],
        "fractions": len(certificate["fixture"]["fractions"]),
        "mutations_rejected": certificate["mutation_firewalls"]["rejected_count"],
        "status": certificate["markers"]["TPC238_STATUS"],
        "windows": len(checks["windows"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = write_certificate() if args.write else check_certificate()
    action = "write" if args.write else "check"
    print(json.dumps(summary(certificate, action), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateFailure as error:
        raise SystemExit(f"TPC238_CERTIFICATE=FAIL: {error}")
