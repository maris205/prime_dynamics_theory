#!/usr/bin/env python3
"""Deterministic exact certificate for TPC-50.

The certificate checks finite algebraic models of weighted mask survival,
three-channel concentration, degree--flatness, energy selection, phase and
scale invariance, the three static-mask obstructions, and the endpoint
exponent ledger.  It uses integers and fractions only.  It is a regression
certificate for the displayed finite identities, not a proof of any
asymptotic row-count theorem and not a search for physical TPC coefficients
or prime pairs.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import itertools
import json
from math import gcd
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def nonzero_integer_vectors(n: int, maximum: int = 2):
    for vector in itertools.product(range(maximum + 1), repeat=n):
        if any(vector):
            yield vector


def binary_matrices(rows: int, columns: int):
    for bits in itertools.product((0, 1), repeat=rows * columns):
        yield tuple(
            tuple(bits[i * columns + j] for j in range(columns))
            for i in range(rows)
        )


def energy(vector: tuple[int, ...]) -> int:
    return sum(value * value for value in vector)


def weighted_survival(
    mask: tuple[tuple[int, ...], ...],
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> Fraction:
    numerator = sum(
        left[i] * left[i] * mask[i][j] * right[j] * right[j]
        for i in range(len(mask))
        for j in range(len(mask[0]))
    )
    return Fraction(numerator, energy(left) * energy(right))


def forbidden_concentration(
    mask: tuple[tuple[int, ...], ...], right: tuple[int, ...]
) -> Fraction:
    total = energy(right)
    return max(
        Fraction(
            sum(right[j] * right[j] for j, value in enumerate(row) if not value),
            total,
        )
        for row in mask
    )


def row_survival(
    mask: tuple[tuple[int, ...], ...], row: int, right: tuple[int, ...]
) -> Fraction:
    return Fraction(
        sum(
            mask[row][j] * right[j] * right[j]
            for j in range(len(right))
        ),
        energy(right),
    )


def check_exact_infimum() -> dict:
    """Enumerate masks and weights and certify inf_a delta = 1 - eta."""
    start = CHECKS
    cases = 0
    basis_attainments = 0
    for row_count in range(1, 4):
        for column_count in range(1, 4):
            left_vectors = tuple(nonzero_integer_vectors(row_count))
            right_vectors = tuple(nonzero_integer_vectors(column_count))
            for mask in binary_matrices(row_count, column_count):
                for right in right_vectors:
                    eta = forbidden_concentration(mask, right)
                    expected = 1 - eta
                    row_values = tuple(
                        row_survival(mask, i, right) for i in range(row_count)
                    )
                    require(min(row_values) == expected, "row minimum equals 1-eta")
                    minimizing_row = row_values.index(expected)
                    basis = tuple(
                        int(i == minimizing_row) for i in range(row_count)
                    )
                    require(
                        weighted_survival(mask, basis, right) == expected,
                        "a basis vector attains the exact infimum",
                    )
                    basis_attainments += 1
                    for left in left_vectors:
                        delta = weighted_survival(mask, left, right)
                        convex = sum(
                            Fraction(left[i] * left[i], energy(left))
                            * row_values[i]
                            for i in range(row_count)
                        )
                        require(delta == convex, "survival is a row convex combination")
                        require(delta >= expected, "integer left weights obey exact infimum")
                    cases += 1
    return {
        "checks": CHECKS - start,
        "mask_right_weight_cases": cases,
        "basis_attainments": basis_attainments,
        "largest_enumerated_mask": "3x3",
        "integer_weight_alphabet": [0, 1, 2],
    }


def channel_union_mask(
    source_forbidden: tuple[tuple[int, ...], ...],
    near_forbidden: tuple[tuple[int, ...], ...],
    gcd_forbidden: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            int(
                not source_forbidden[i][j]
                and not near_forbidden[i][j]
                and not gcd_forbidden[i][j]
            )
            for j in range(len(source_forbidden[0]))
        )
        for i in range(len(source_forbidden))
    )


def channel_concentration(
    forbidden: tuple[tuple[int, ...], ...], right: tuple[int, ...]
) -> Fraction:
    total = energy(right)
    return max(
        Fraction(
            sum(right[j] * right[j] * row[j] for j in range(len(right))),
            total,
        )
        for row in forbidden
    )


def check_three_channel_union() -> dict:
    start = CHECKS
    cases = 0
    rows = columns = 2
    forbidden_matrices = tuple(binary_matrices(rows, columns))
    right_vectors = tuple(nonzero_integer_vectors(columns))
    left_vectors = tuple(nonzero_integer_vectors(rows))
    for source in forbidden_matrices:
        for near in forbidden_matrices:
            for gcd_channel in forbidden_matrices:
                mask = channel_union_mask(source, near, gcd_channel)
                for right in right_vectors:
                    eta = forbidden_concentration(mask, right)
                    eta_source = channel_concentration(source, right)
                    eta_near = channel_concentration(near, right)
                    eta_gcd = channel_concentration(gcd_channel, right)
                    channel_sum = eta_source + eta_near + eta_gcd
                    require(eta <= channel_sum, "three-channel forbidden union bound")
                    for left in left_vectors:
                        require(
                            weighted_survival(mask, left, right)
                            >= 1 - channel_sum,
                            "three-channel survival lower bound",
                        )
                    cases += 1
    return {
        "checks": CHECKS - start,
        "exact_channel_weight_cases": cases,
        "channel_count": 3,
        "mask_size": "2x2",
    }


def maximum_forbidden_degree(mask: tuple[tuple[int, ...], ...]) -> int:
    return max(sum(1 - value for value in row) for row in mask)


def check_degree_flatness_and_energy_selection() -> dict:
    start = CHECKS
    degree_cases = 0
    selection_cases = 0
    tau_values = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))

    for row_count, column_count in ((2, 2), (2, 3)):
        left_vectors = tuple(nonzero_integer_vectors(row_count))
        right_vectors = tuple(nonzero_integer_vectors(column_count))
        for mask in binary_matrices(row_count, column_count):
            defect = maximum_forbidden_degree(mask)
            epsilon = Fraction(defect, column_count)
            for right in right_vectors:
                flatness = Fraction(
                    column_count * max(value * value for value in right),
                    energy(right),
                )
                lower = 1 - epsilon * flatness
                for left in left_vectors:
                    require(
                        weighted_survival(mask, left, right) >= lower,
                        "degree-flatness inequality",
                    )
                degree_cases += 1

            # Exact two-cell energy-selection models.
            for first in right_vectors:
                for second in right_vectors:
                    family = (first, second)
                    bound = max(max(first), max(second))
                    require(bound > 0, "family supremum bound is nonzero")
                    bound_squared = bound * bound
                    total_energy = sum(energy(vector) for vector in family)
                    A = Fraction(total_energy, column_count * bound_squared)
                    S = len(family)
                    for tau in tau_values:
                        low_energy = 0
                        for vector in family:
                            if energy(vector) >= tau * column_count * bound_squared:
                                survival_infimum = 1 - forbidden_concentration(mask, vector)
                                require(
                                    survival_infimum >= 1 - epsilon / tau,
                                    "energetic-cell survival",
                                )
                            else:
                                low_energy += energy(vector)
                        require(
                            Fraction(low_energy, total_energy)
                            <= Fraction(S) * tau / A,
                            "nonenergetic aggregate-energy bound",
                        )
                        selection_cases += 1

    return {
        "checks": CHECKS - start,
        "degree_flatness_cases": degree_cases,
        "energy_selection_cases": selection_cases,
        "tau_values": ["1/4", "1/2", "3/4"],
    }


GAUSSIAN_UNIT_PHASES = ((1, 0), (-1, 0), (0, 1), (0, -1))


def phase_norm_squared(phase: tuple[int, int]) -> int:
    return phase[0] * phase[0] + phase[1] * phase[1]


def check_phase_and_scale_invariance() -> dict:
    start = CHECKS
    cases = 0
    masks = tuple(binary_matrices(2, 2))
    vectors = tuple(nonzero_integer_vectors(2))
    for phase in GAUSSIAN_UNIT_PHASES:
        require(phase_norm_squared(phase) == 1, "Gaussian phase has unit modulus")
    for mask in masks:
        for left in vectors:
            for right in vectors:
                base = weighted_survival(mask, left, right)
                for left_scale in (1, 2, 3):
                    for right_scale in (1, 2, 3):
                        scaled_left = tuple(left_scale * value for value in left)
                        scaled_right = tuple(right_scale * value for value in right)
                        require(
                            weighted_survival(mask, scaled_left, scaled_right) == base,
                            "independent nonzero scale invariance",
                        )
                for row_phase in GAUSSIAN_UNIT_PHASES:
                    for column_phase in GAUSSIAN_UNIT_PHASES:
                        for kernel_phase in GAUSSIAN_UNIT_PHASES:
                            phase_factor = (
                                phase_norm_squared(row_phase)
                                * phase_norm_squared(column_phase)
                                * phase_norm_squared(kernel_phase)
                            )
                            transformed_numerator = sum(
                                left[i] * left[i]
                                * mask[i][j]
                                * right[j] * right[j]
                                * phase_factor
                                for i in range(2)
                                for j in range(2)
                            )
                            require(
                                Fraction(
                                    transformed_numerator,
                                    energy(left) * energy(right),
                                )
                                == base,
                                "row, column, and supported-kernel unit phases preserve survival",
                            )
                cases += 1
    return {
        "checks": CHECKS - start,
        "weighted_mask_cases": cases,
        "unit_phase_group": ["1", "-1", "i", "-i"],
        "tested_scales": [1, 2, 3],
    }


def literal_static_mask(
    rows: tuple[tuple[int, int], ...], delta: int, G: int
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            int(
                ell != ell2
                and abs(ell * d - ell2 * d2) > delta
                and gcd(d, d2) <= G
            )
            for ell2, d2 in rows
        )
        for ell, d in rows
    )


def indicator(size: int, support: tuple[int, ...]) -> tuple[int, ...]:
    chosen = set(support)
    return tuple(int(index in chosen) for index in range(size))


def check_three_obstruction_models() -> dict:
    start = CHECKS
    rows = (
        (11, 1),   # 0: same-source block
        (11, 2),   # 1: same-source block
        (13, 2),   # 2: near block, product 26
        (5, 5),    # 3: near block, product 25
        (7, 3),    # 4: gcd block
        (17, 6),   # 5: gcd block
        (19, 7),   # 6: admitted neighbor for each selected first row
    )
    delta = 1
    G = 2
    mask = literal_static_mask(rows, delta, G)
    blocks = {
        "same_source": (0, 1),
        "near_row": (2, 3),
        "large_gcd": (4, 5),
    }
    records = []
    for name, support in blocks.items():
        for i in support:
            for j in support:
                require(mask[i][j] == 0, f"{name} block is completely forbidden")
        alpha = support[0]
        neighbor = 6
        require(mask[alpha][neighbor] == 1, f"{name} row has admitted neighbor")
        left = indicator(len(rows), (alpha,))
        zero_right = indicator(len(rows), support)
        require(
            weighted_survival(mask, left, zero_right) == 0,
            f"{name} zero-survival packet",
        )
        positive_right = indicator(len(rows), support + (neighbor,))
        expected = Fraction(1, len(support) + 1)
        require(
            weighted_survival(mask, left, positive_right) == expected,
            f"{name} one-neighbor exact survival",
        )
        records.append(
            {
                "channel": name,
                "block_size": len(support),
                "zero_survival": "0",
                "one_neighbor_survival": f"{expected.numerator}/{expected.denominator}",
            }
        )
    return {
        "checks": CHECKS - start,
        "rows": [list(row) for row in rows],
        "delta": delta,
        "G": G,
        "records": records,
    }


def check_endpoint_ledger() -> dict:
    start = CHECKS
    mu = Fraction(267, 400)
    nu = Fraction(133, 400)
    kappa = Fraction(1, 400)
    lambda_L = Fraction(99979, 210000)
    lambda_D = Fraction(10049, 52500)
    lambda_V = Fraction(23, 120)

    require(mu + nu == 1, "source and orbit endpoint exponents sum to one")
    require(lambda_L + lambda_D == mu, "row-factor exponents sum to mu")
    require(mu - kappa == Fraction(133, 200), "near/gcd block exponent")
    require(
        lambda_D - kappa == Fraction(39671, 210000),
        "source survival deficit",
    )
    require(mu - 2 * kappa == Fraction(133, 200) - kappa, "budget comparison identity")
    require(lambda_D > kappa, "same-source survival is below target")
    require(mu - kappa > kappa, "near/gcd survival is below target")
    require(min(kappa, lambda_D) == kappa, "canonical degree defect exponent")
    require(2 * 0 + 0 <= kappa, "zero-cost canonical face fits isolated budget")
    require(
        lambda_V - lambda_D == Fraction(9, 35000),
        "opened-divisor cutoff has the claimed fixed-power interior margin",
    )
    require(lambda_V > lambda_D, "the endpoint dyadic divisor cell lies below V")

    return {
        "checks": CHECKS - start,
        "mu": "267/400",
        "nu": "133/400",
        "kappa": "1/400",
        "lambda_L": "99979/210000",
        "lambda_D": "10049/52500",
        "lambda_V": "23/120",
        "V_minus_D_margin": "9/35000",
        "near_gcd_block_exponent": "133/200",
        "same_source_survival_exponent": "10049/52500",
        "canonical_degree_defect_exponent_when_kappa0_is_kappa": "1/400",
        "isolated_budget_identity": "2*0+0 <= 1/400",
    }


def normalized_source_hash() -> str:
    source = Path(__file__).read_text(encoding="utf-8")
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in source.split("\n"))
    if not normalized.endswith("\n"):
        normalized += "\n"
    return sha256(normalized.encode("utf-8")).hexdigest()


def main() -> None:
    result = {
        "certificate": "TPC-50 fixed-complexity cell survival",
        "arithmetic": "integers and exact rational numbers",
        "scope": (
            "finite deterministic regression certificate; not an asymptotic "
            "proof and not a certificate for literal physical TPC coefficients"
        ),
        "exact_infimum": check_exact_infimum(),
        "three_channel_union": check_three_channel_union(),
        "degree_flatness_and_energy_selection": (
            check_degree_flatness_and_energy_selection()
        ),
        "phase_and_scale_invariance": check_phase_and_scale_invariance(),
        "three_obstruction_models": check_three_obstruction_models(),
        "endpoint_ledger": check_endpoint_ledger(),
    }
    result["total_checks"] = CHECKS
    semantic_payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["semantic_sha256"] = sha256(
        semantic_payload.encode("utf-8")
    ).hexdigest()
    result["normalized_source_sha256"] = normalized_source_hash()

    output = Path(__file__).with_name("tpc50_certificate.json")
    output.write_bytes(
        (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    output_hash = sha256(output.read_bytes()).hexdigest()
    print(f"TPC-50 certificate: {CHECKS} exact checks passed")
    print(f"semantic sha256: {result['semantic_sha256']}")
    print(f"normalized source sha256: {result['normalized_source_sha256']}")
    print(f"json sha256: {output_hash}")


if __name__ == "__main__":
    main()
