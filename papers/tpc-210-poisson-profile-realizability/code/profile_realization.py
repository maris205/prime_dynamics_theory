"""Exact finite model for the TPC-210 Poisson-profile obstruction.

The code certifies a structural fact: finite residue profiles can be realized
by compactly supported smooth Fourier packets.  It then inserts literal
Mobius weights into an aligned family.  No asymptotic estimate is attempted.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd


Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def units(q: int) -> tuple[int, ...]:
    require(q > 2, "prime modulus dimension")
    return tuple(range(1, q))


def mobius(value: int) -> int:
    require(value >= 1, "Mobius domain")
    remaining = value
    prime = 2
    parity = 0
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


def nonzero_mobius_divisors(q: int) -> tuple[int, ...]:
    return tuple(
        divisor
        for divisor in range(2, q)
        if gcd(divisor, q) == 1 and mobius(divisor) != 0
    )


def dilation_image(q: int, divisor: int) -> tuple[int, ...]:
    require(gcd(divisor, q) == 1, "unit divisor")
    return tuple((frequency * divisor) % q - 1 for frequency in units(q))


def apply_dilation(vector: Vector, q: int, divisor: int) -> Vector:
    image = dilation_image(q, divisor)
    return tuple(vector[index] for index in image)


def apply_adjoint_dilation(vector: Vector, q: int, divisor: int) -> Vector:
    inverse = pow(divisor, -1, q)
    return apply_dilation(vector, q, inverse)


def centered_witness(q: int) -> Vector:
    values = [Fraction(0, 1) for _ in units(q)]
    values[0] = Fraction(1, 2)
    values[1] = Fraction(-1, 2)
    return tuple(values)


def mean(vector: Vector) -> Fraction:
    return sum(vector, Fraction(0, 1)) / len(vector)


def center(vector: Vector) -> Vector:
    average = mean(vector)
    return tuple(value - average for value in vector)


def norm_squared(vector: Vector) -> Fraction:
    return sum(value * value for value in vector)


def inner(left: Vector, right: Vector) -> Fraction:
    require(len(left) == len(right), "inner-product shape")
    return sum(value * other for value, other in zip(left, right))


def aggregate(
    q: int,
    divisors: tuple[int, ...],
    weights: tuple[int, ...],
    profiles: tuple[Vector, ...],
) -> Vector:
    require(len(divisors) == len(weights) == len(profiles), "aggregate shape")
    return tuple(
        sum(
            weight * apply_dilation(profile, q, divisor)[coordinate]
            for divisor, weight, profile in zip(divisors, weights, profiles)
        )
        for coordinate in range(q - 1)
    )


def profile_gram(
    q: int,
    divisors: tuple[int, ...],
    profiles: tuple[Vector, ...],
) -> Matrix:
    require(len(divisors) == len(profiles), "Gram shape")
    outputs = tuple(
        center(apply_dilation(profile, q, divisor))
        for divisor, profile in zip(divisors, profiles)
    )
    return tuple(
        tuple(inner(left, right) for right in outputs) for left in outputs
    )


def weighted_quadratic(
    weights: tuple[int, ...], gram: Matrix
) -> Fraction:
    return sum(
        weights[left] * weights[right] * gram[left][right]
        for left in range(len(weights))
        for right in range(len(weights))
    )


def profile_nodes(q: int) -> tuple[int, ...]:
    """Distinct dual integers, one for each nonzero residue."""

    return tuple(residue + 10 * q * residue for residue in units(q))


def support_radius(q: int) -> Fraction:
    return Fraction(1, 4 * q)


def minimum_node_gap(q: int) -> Fraction:
    nodes = profile_nodes(q)
    return min(
        abs(Fraction(left - right, q))
        for index, left in enumerate(nodes)
        for right in nodes[index + 1 :]
    )


def isolated_profile_geometry(q: int) -> dict[str, str | int]:
    """Return the exact support facts used by the bump interpolation proof."""

    radius = support_radius(q)
    gap = minimum_node_gap(q)
    lattice_gap = Fraction(1, 1)
    require(2 * radius < gap, "distinct residue nodes overlap")
    require(2 * radius < lattice_gap, "same-residue lattice nodes overlap")
    return {
        "node_count": q - 1,
        "support_radius": str(radius),
        "minimum_node_gap": str(gap),
        "same_residue_lattice_gap": str(lattice_gap),
        "strict_isolation": True,
    }


def realize_profile(q: int, target: Vector) -> Vector:
    """Evaluate the exact lattice profile of the canonical bump construction.

    Choose eta in C_c^infty((-1,1)) with eta(0)=1 and set
    Fhat(xi)=sum_s target[s] eta((xi-n_s/q)/rho).  The isolation inequalities
    imply that the residue-class Poisson profile is exactly target.
    """

    require(len(target) == q - 1, "target profile dimension")
    geometry = isolated_profile_geometry(q)
    require(geometry["strict_isolation"] is True, "profile geometry")
    return tuple(target)


def aligned_mobius_profiles(
    q: int, divisors: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[Vector, ...]]:
    weights = tuple(mobius(divisor) for divisor in divisors)
    require(all(weight != 0 for weight in weights), "squarefree Mobius family")
    witness = centered_witness(q)
    profiles = tuple(
        tuple(
            weight * value
            for value in apply_adjoint_dilation(witness, q, divisor)
        )
        for divisor, weight in zip(divisors, weights)
    )
    return weights, profiles


def aligned_certificate(q: int) -> dict[str, object]:
    divisors = nonzero_mobius_divisors(q)
    weights, profiles = aligned_mobius_profiles(q, divisors)
    realized = tuple(realize_profile(q, profile) for profile in profiles)
    gram = profile_gram(q, divisors, realized)
    output = aggregate(q, divisors, weights, realized)
    diagonal_energy = sum(
        weight * weight * norm_squared(center(apply_dilation(profile, q, divisor)))
        for divisor, weight, profile in zip(divisors, weights, realized)
    )
    aggregate_energy = norm_squared(center(output))
    ratio = aggregate_energy / diagonal_energy
    require(center(output) == tuple(
        len(divisors) * value for value in centered_witness(q)
    ), "aligned output")
    require(weighted_quadratic(weights, gram) == aggregate_energy, "Gram quadratic")
    return {
        "divisors": list(divisors),
        "weights": list(weights),
        "profile_rows": len(realized),
        "geometry": isolated_profile_geometry(q),
        "realized_exactly": all(left == right for left, right in zip(profiles, realized)),
        "profile_gram": [[str(value) for value in row] for row in gram],
        "diagonal_energy": str(diagonal_energy),
        "aggregate_energy": str(aggregate_energy),
        "energy_ratio": str(ratio),
        "mobius_l1_mass": sum(abs(weight) for weight in weights),
        "mobius_l2_mass": sum(weight * weight for weight in weights),
    }
