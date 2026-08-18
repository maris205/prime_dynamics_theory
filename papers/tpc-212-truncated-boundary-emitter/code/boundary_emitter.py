"""Exact finite algebra for the TPC-212 boundary/emitter interface.

The module separates two finite mechanisms in the V46 transition:

* a divisor band cut on the squarefree Boolean lattice;
* the reciprocal occupancy map (q,m) -> m*q^{-1} mod d.

It intentionally uses unit reciprocal weights and exact rational arithmetic.
The unit-weight emitter is a finite algebraic fixture, not an asymptotic
replacement for the smooth function psi in the physical transition.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, prod


Vector = tuple[Fraction, ...]
LogVectorFamily = tuple[Vector, ...]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def validate_primes(primes: tuple[int, ...]) -> None:
    require(len(primes) >= 1, "at least one active prime")
    require(all(type(p) is int and p > 2 for p in primes), "odd primes")
    require(tuple(sorted(set(primes))) == primes, "strictly increasing primes")


def masks(primes: tuple[int, ...]) -> tuple[int, ...]:
    validate_primes(primes)
    return tuple(range(1, 1 << len(primes)))


def divisor(primes: tuple[int, ...], mask: int) -> int:
    validate_primes(primes)
    require(mask in masks(primes), "nonempty divisor mask")
    return prod(
        prime for index, prime in enumerate(primes) if (mask >> index) & 1
    )


def mobius_mask(mask: int) -> int:
    require(mask > 0, "nonempty mask")
    return -1 if mask.bit_count() % 2 else 1


def mobius_integer(value: int) -> int:
    require(value >= 1, "positive integer")
    remaining = value
    parity = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            parity ^= 1
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        parity ^= 1
    return -1 if parity else 1


def all_divisor_masks(primes: tuple[int, ...]) -> tuple[int, ...]:
    return masks(primes)


def band_masks(primes: tuple[int, ...], lower: int, upper: int) -> tuple[int, ...]:
    require(type(lower) is int and type(upper) is int, "integer cut")
    require(lower >= 0 and lower < upper, "ordered cut")
    return tuple(
        mask
        for mask in masks(primes)
        if lower < divisor(primes, mask) <= upper
    )


def missing_masks(
    primes: tuple[int, ...], selected: tuple[int, ...]
) -> tuple[int, ...]:
    selected_set = set(selected)
    require(selected_set.issubset(set(masks(primes))), "selected masks")
    return tuple(mask for mask in masks(primes) if mask not in selected_set)


def endpoint_incidence(
    primes: tuple[int, ...], selected: tuple[int, ...]
) -> tuple[int, ...]:
    """Return eta_p=sum_{S in selected,p in S} (-1)^|S|."""

    return tuple(
        sum(
            mobius_mask(mask)
            for mask in selected
            if (mask >> index) & 1
        )
        for index in range(len(primes))
    )


def log_coefficient_vector(primes: tuple[int, ...], mask: int) -> tuple[int, ...]:
    """Coefficients of mu(d_S) log(d_S) in the basis (log p)_p."""

    return tuple(
        mobius_mask(mask) if (mask >> index) & 1 else 0
        for index in range(len(primes))
    )


def scalar_profile(primes: tuple[int, ...], mask: int, length: int) -> Vector:
    """Deterministic rational profile used only for identity QA."""

    require(length >= 1, "profile length")
    seed = divisor(primes, mask)
    return tuple(Fraction((seed + 1) * (index + 2), seed) for index in range(length))


def endpoint_profile(length: int) -> Vector:
    require(length >= 1, "endpoint length")
    return tuple(Fraction(index + 1, 3) for index in range(length))


def zero_vector(length: int) -> Vector:
    return tuple(Fraction(0, 1) for _ in range(length))


def add_vectors(left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "vector shape")
    return tuple(a + b for a, b in zip(left, right))


def scale_vector(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def coefficientwise_log_packet(
    primes: tuple[int, ...],
    selected: tuple[int, ...],
    profiles: dict[int, Vector],
    endpoint: Vector,
) -> LogVectorFamily:
    """Return the packet sum in the independent log-prime basis."""

    require(all(mask in profiles for mask in selected), "profile coverage")
    length = len(endpoint)
    require(all(len(profiles[mask]) == length for mask in selected), "profile lengths")
    output = [zero_vector(length) for _ in primes]
    for mask in selected:
        residual = add_vectors(endpoint, scale_vector(Fraction(-1), profiles[mask]))
        for index, coefficient in enumerate(log_coefficient_vector(primes, mask)):
            if coefficient:
                output[index] = add_vectors(
                    output[index], scale_vector(Fraction(coefficient), residual)
                )
    return tuple(output)


def subtract_families(left: LogVectorFamily, right: LogVectorFamily) -> LogVectorFamily:
    require(len(left) == len(right), "family shape")
    return tuple(
        add_vectors(first, scale_vector(Fraction(-1), second))
        for first, second in zip(left, right)
    )


def boundary_identity_case(
    primes: tuple[int, ...], lower: int, upper: int
) -> dict[str, object]:
    selected = band_masks(primes, lower, upper)
    missing = missing_masks(primes, selected)
    length = prod(primes)
    profiles = {
        mask: scalar_profile(primes, mask, length) for mask in masks(primes)
    }
    endpoint = endpoint_profile(length)
    selected_sum = coefficientwise_log_packet(primes, selected, profiles, endpoint)
    full_sum = coefficientwise_log_packet(primes, masks(primes), profiles, endpoint)
    missing_sum = coefficientwise_log_packet(primes, missing, profiles, endpoint)
    recovered = subtract_families(full_sum, missing_sum)
    require(selected_sum == recovered, "cut/full/missing decomposition")
    full_incidence = endpoint_incidence(primes, masks(primes))
    selected_incidence = endpoint_incidence(primes, selected)
    missing_incidence = endpoint_incidence(primes, missing)
    require(
        tuple(a + b for a, b in zip(selected_incidence, missing_incidence))
        == full_incidence,
        "incidence decomposition",
    )
    return {
        "primes": list(primes),
        "lower": lower,
        "upper": upper,
        "active_masks": list(selected),
        "active_divisors": [divisor(primes, mask) for mask in selected],
        "missing_masks": list(missing),
        "missing_divisors": [divisor(primes, mask) for mask in missing],
        "active_endpoint_incidence": list(selected_incidence),
        "missing_endpoint_incidence": list(missing_incidence),
        "full_endpoint_incidence": list(full_incidence),
        "boundary_identity": True,
        "profile_coordinate_count": length,
    }


def reciprocal_pairs(d: int, q_values: tuple[int, ...], H: int) -> tuple[tuple[int, int], ...]:
    require(d >= 2, "positive divisor")
    require(H >= 1, "positive H")
    pairs: list[tuple[int, int]] = []
    for q in q_values:
        require(gcd(q, d) == 1, f"q={q} not invertible modulo d={d}")
        limit = d * q // H
        for m in range(-limit, limit + 1):
            if m != 0:
                pairs.append((q, m))
    return tuple(pairs)


def emitter_counts(d: int, q_values: tuple[int, ...], H: int) -> tuple[int, ...]:
    counts = [0 for _ in range(d)]
    for q, m in reciprocal_pairs(d, q_values, H):
        counts[(m * pow(q, -1, d)) % d] += 1
    return tuple(counts)


def emitter_norm_squared(d: int, q_values: tuple[int, ...], H: int) -> int:
    counts = emitter_counts(d, q_values, H)
    return sum(value * value for value in counts)


def emitter_collision_count(d: int, q_values: tuple[int, ...], H: int) -> int:
    pairs = reciprocal_pairs(d, q_values, H)
    return sum(
        1
        for q1, m1 in pairs
        for q2, m2 in pairs
        if (m1 * q2 - m2 * q1) % d == 0
    )


def emitter_case(
    divisors: tuple[int, ...], q_values: tuple[int, ...], H: int
) -> dict[str, object]:
    norms = [emitter_norm_squared(d, q_values, H) for d in divisors]
    collisions = [emitter_collision_count(d, q_values, H) for d in divisors]
    counts = [list(emitter_counts(d, q_values, H)) for d in divisors]
    require(norms == collisions, "reciprocal collision identity")
    require(all(value > 0 for value in norms), "nonzero emitter row")

    # The natural residual space is a direct sum over divisors.  Its emitter
    # Gram matrix is diagonal, positive, and therefore full rank.
    gram_rank = sum(value > 0 for value in norms)
    coefficient_signs = [mobius_integer(value) for value in divisors]
    aligned_contributions = [1 for _ in divisors]
    coherent_energy = len(divisors) ** 2
    diagonal_energy = len(divisors)
    return {
        "divisors": list(divisors),
        "q_values": list(q_values),
        "H": H,
        "occupancy_rows": counts,
        "emitter_norm_squared": norms,
        "collision_counts": collisions,
        "direct_sum_gram_diagonal": norms,
        "direct_sum_gram_rank": gram_rank,
        "coefficient_signs_fixture": coefficient_signs,
        "aligned_contributions": aligned_contributions,
        "coherent_energy": coherent_energy,
        "diagonal_energy": diagonal_energy,
        "coherent_to_diagonal_ratio": Fraction(coherent_energy, diagonal_energy).__str__(),
        "unit_weight_alignment": True,
    }


def build_certificate() -> dict[str, object]:
    boundary_cases = (
        boundary_identity_case((5, 7), 5, 35),
        boundary_identity_case((5, 7, 11), 5, 35),
        boundary_identity_case((5, 7, 11), 10, 77),
        boundary_identity_case((5, 7, 11, 13), 30, 100),
    )
    emitter_cases = (
        emitter_case((7, 35), (2, 3, 13), 10),
        emitter_case((7, 11, 35, 55), (2, 3, 13), 10),
        emitter_case((35, 55, 77), (2, 3, 13), 10),
    )
    return {
        "schema": "TPC212_TRUNCATED_BOUNDARY_EMITTER_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_STOP_SCOPED_BOUNDARY_EMITTER",
        "modeling_choice": "UNIT_RECIPROCAL_WEIGHTS_PSI_EQUALS_ONE_FINITE_FIXTURE",
        "theorem_contract": {
            "cut_endpoint_leakage": "PROVED_EXACT_SIGNED_BOOLEAN_INCIDENCE",
            "full_minus_missing_boundary_decomposition": "PROVED_EXACT",
            "reciprocal_collision_identity": "PROVED_EXACT_FINITE",
            "direct_sum_emitter_gram": "PROVED_EXACT_BLOCK_DIAGONAL",
            "emitter_only_universal_saving": "REFUTED_SCOPED",
            "literal_physical_boundary_bound": "OPEN",
            "prime_shell_reassembly": "OPEN",
        },
        "boundary_cases": boundary_cases,
        "emitter_cases": emitter_cases,
        "claim_firewall": {
            "route_advance": "YES",
            "structural_threshold_a": "PASS",
            "cut_endpoint_leakage": "PROVED_EXACT",
            "boundary_decomposition": "PROVED_EXACT",
            "reciprocal_collision": "PROVED_EXACT_FINITE",
            "emitter_gram": "PROVED_EXACT_BLOCK_DIAGONAL",
            "emitter_only_universal_saving": "REFUTED_SCOPED",
            "literal_physical_boundary_bound": "OPEN",
            "physical_cross_divisor_gram_bound": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        },
        "audit_counts": {
            "boundary_cases": len(boundary_cases),
            "emitter_cases": len(emitter_cases),
            "boundary_profile_coordinate_rows": sum(
                int(record["profile_coordinate_count"]) for record in boundary_cases
            ),
            "emitter_divisor_rows": sum(
                len(record["divisors"]) for record in emitter_cases
            ),
        },
        "open_theorem": (
            "CONTROL_THE_LITERAL_PHYSICAL_BOUNDARY_AFTER_A_D_R_WITHOUT_"
            "REPLACING_THE_COUPLED_RESIDUAL_FAMILY_BY_AN_INDEPENDENT_DIRECT_SUM"
        ),
    }
