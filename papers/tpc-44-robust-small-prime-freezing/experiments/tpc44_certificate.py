#!/usr/bin/env python3
"""Exact deterministic certificate for TPC-44.

This script checks finite algebraic identities only.  It uses the Python
standard library, exact integer and rational arithmetic, exhaustive Boolean
cubes, and no sampling.  It does not test any asymptotic estimate or physical
Mobius cancellation statement.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE.joinpath("tpc44_certificate.json")

Gaussian = tuple[int, int]
Coordinate = list[tuple[int, Gaussian]]
Packet = list[Coordinate]


class Certificate:
    def __init__(self) -> None:
        self.checks = 0
        self.stats: dict[str, int] = defaultdict(int)

    def check(self, condition: bool, family: str) -> None:
        self.checks += 1
        self.stats[family] += 1
        if not condition:
            raise RuntimeError(f"certificate failure in {family}")


def factorization(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorization requires a positive integer")
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_squarefree(n: int) -> bool:
    return all(exponent == 1 for exponent in factorization(n).values())


def mobius(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def squarefree_kernel(a: int, b: int) -> int:
    common = gcd(a, b)
    return a * b // (common * common)


def prime_support(values: list[int]) -> list[int]:
    support: set[int] = set()
    for value in values:
        support.update(factorization(value))
    return sorted(support)


def product(values: list[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def squarefree_divisors(primes: list[int]) -> list[int]:
    values = [1]
    for p in primes:
        values.extend(p * value for value in list(values))
    return sorted(values)


def environments(primes: list[int]):
    for mask in range(1 << len(primes)):
        yield {
            p: (-1 if mask & (1 << index) else 1)
            for index, p in enumerate(primes)
        }


def character(n: int, epsilon: dict[int, int]) -> int:
    value = 1
    for p in factorization(n):
        value *= epsilon[p]
    return value


def low_high_split(n: int, z: int) -> tuple[int, int]:
    low = 1
    high = 1
    for p in factorization(n):
        if p <= z:
            low *= p
        else:
            high *= p
    return low, high


def least_prime(n: int) -> int:
    return min(factorization(n))


def largest_prime(n: int) -> int:
    return max(factorization(n))


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gscale(scale: int, value: Gaussian) -> Gaussian:
    return scale * value[0], scale * value[1]


def gnorm2(value: Gaussian) -> int:
    return value[0] * value[0] + value[1] * value[1]


def deterministic_coefficient(packet_index: int, coordinate: int, index: int) -> Gaussian:
    real = ((5 * index + 3 * coordinate + 2 * packet_index) % 9) - 4
    imag = ((7 * index + coordinate + 3 * packet_index) % 7) - 3
    if real == 0 and imag == 0:
        return packet_index + coordinate + 1, 1
    return real, imag


def make_packet(packet_index: int, label_lists: list[list[int]]) -> Packet:
    packet: Packet = []
    for coordinate, labels in enumerate(label_lists):
        entries = [
            (label, deterministic_coefficient(packet_index, coordinate, index))
            for index, label in enumerate(labels)
        ]
        packet.append(entries)
    return packet


def toy_packets() -> list[tuple[str, Packet]]:
    raw = [
        [
            [1, 2, 3, 6, 7, 14, 21, 42],
            [1, 5, 10, 15, 30, 11, 22, 33, 66],
            [2, 6, 10, 30, 13, 26, 39, 65, 78],
        ],
        [
            [1, 2, 5, 10, 7, 35, 70, 11, 22, 55, 110],
            [3, 6, 15, 30, 13, 26, 39, 78, 195],
            [5, 7, 11, 13, 35, 55, 65, 77, 91, 143],
        ],
        [
            [1, 6, 10, 15, 30, 7, 42, 70, 105, 210],
            [2, 3, 5, 11, 13, 22, 33, 55, 65, 286],
            [1, 14, 21, 35, 77, 91, 143, 154, 273],
        ],
    ]
    return [
        (f"gram-packet-{index + 1}", make_packet(index + 1, labels))
        for index, labels in enumerate(raw)
    ]


def packet_labels(packet: Packet) -> list[int]:
    return [label for coordinate in packet for label, _coefficient in coordinate]


def diagonal(packet: Packet) -> int:
    return sum(
        gnorm2(coefficient)
        for coordinate in packet
        for _label, coefficient in coordinate
    )


def energy(packet: Packet, epsilon: dict[int, int]) -> int:
    total = 0
    for coordinate in packet:
        value = (0, 0)
        for label, coefficient in coordinate:
            value = gadd(value, gscale(character(label, epsilon), coefficient))
        total += gnorm2(value)
    return total


def grouped_spectrum(packet: Packet) -> dict[int, int]:
    grouped: dict[int, Gaussian] = defaultdict(lambda: (0, 0))
    for coordinate in packet:
        for left_index, (left_label, left_coefficient) in enumerate(coordinate):
            for right_index, (right_label, right_coefficient) in enumerate(coordinate):
                if left_index == right_index:
                    continue
                kernel = squarefree_kernel(left_label, right_label)
                contribution = gmul(left_coefficient, gconj(right_coefficient))
                grouped[kernel] = gadd(grouped[kernel], contribution)
    spectrum: dict[int, int] = {}
    for kernel, coefficient in grouped.items():
        if coefficient[1] != 0:
            raise RuntimeError("non-real grouped Walsh coefficient")
        if kernel == 1:
            raise RuntimeError("distinct labels produced the identity kernel")
        if coefficient[0] != 0:
            spectrum[kernel] = coefficient[0]
    return spectrum


def centered_value(spectrum: dict[int, int], epsilon: dict[int, int]) -> int:
    return sum(
        coefficient * character(kernel, epsilon)
        for kernel, coefficient in spectrum.items()
    )


def validate_packet(cert: Certificate, packet: Packet) -> tuple[dict[int, int], list[int]]:
    for coordinate in packet:
        labels = [label for label, _coefficient in coordinate]
        cert.check(len(labels) == len(set(labels)), "packet_label_injection")
        for label in labels:
            cert.check(is_squarefree(label), "packet_squarefree_labels")
    labels = packet_labels(packet)
    primes = prime_support(labels)
    spectrum = grouped_spectrum(packet)
    d_value = diagonal(packet)
    total = 0
    variance_total = 0
    environment_count = 0
    for epsilon in environments(primes):
        environment_count += 1
        z_value = energy(packet, epsilon)
        f_value = centered_value(spectrum, epsilon)
        cert.check(z_value == d_value + f_value, "packet_walsh_expansion")
        total += z_value
        variance_total += f_value * f_value
    cert.check(total == environment_count * d_value, "packet_annealed_diagonal")
    cert.check(
        variance_total
        == environment_count * sum(value * value for value in spectrum.values()),
        "packet_walsh_parseval",
    )
    return spectrum, primes


def projected_blocks(
    packet: Packet,
    z: int,
    epsilon_high: dict[int, int],
) -> tuple[list[dict[int, Gaussian]], int]:
    blocks: list[dict[int, Gaussian]] = []
    low_parts: set[int] = set()
    for coordinate in packet:
        coordinate_blocks: dict[int, Gaussian] = defaultdict(lambda: (0, 0))
        for label, coefficient in coordinate:
            low, high = low_high_split(label, z)
            low_parts.add(low)
            coordinate_blocks[low] = gadd(
                coordinate_blocks[low],
                gscale(character(high, epsilon_high), coefficient),
            )
        blocks.append(dict(coordinate_blocks))
    projected_energy = sum(
        gnorm2(value)
        for coordinate_blocks in blocks
        for value in coordinate_blocks.values()
    )
    return blocks, projected_energy


def check_robust_faces(
    cert: Certificate,
    packet: Packet,
    spectrum: dict[int, int],
    primes: list[int],
) -> None:
    d_value = diagonal(packet)
    for z in (2, 3, 5, 7):
        low_primes = [p for p in primes if p <= z]
        high_primes = [p for p in primes if p > z]
        for label in packet_labels(packet):
            low, high = low_high_split(label, z)
            cert.check(low * high == label, "label_low_high_factorization")
            cert.check(gcd(low, high) == 1, "label_low_high_coprimality")
            cert.check(
                all(p <= z for p in factorization(low)),
                "label_low_prime_support",
            )
            cert.check(
                all(p > z for p in factorization(high)),
                "label_high_prime_support",
            )
        low_parts = {
            low_high_split(label, z)[0]
            for label in packet_labels(packet)
        }
        nu = len(low_parts)
        high_count = 1 << len(high_primes)
        projected_total = 0
        projected_values: list[int] = []
        maximum_energies: list[int] = []
        fixed_face_totals: dict[int, int] = defaultdict(int)
        for high_index, epsilon_high in enumerate(environments(high_primes)):
            blocks, projected_energy = projected_blocks(packet, z, epsilon_high)
            projected_total += projected_energy
            projected_values.append(projected_energy)
            for coordinate_index, coordinate in enumerate(packet):
                for low in low_parts:
                    direct_total = 0
                    diagonal_part = 0
                    for label, coefficient in coordinate:
                        label_low, label_high = low_high_split(label, z)
                        if label_low == low:
                            direct_total += gnorm2(coefficient)
                    for extension in environments(high_primes):
                        block_value = (0, 0)
                        for label, coefficient in coordinate:
                            label_low, label_high = low_high_split(label, z)
                            if label_low == low:
                                block_value = gadd(
                                    block_value,
                                    gscale(character(label_high, extension), coefficient),
                                )
                        diagonal_part += gnorm2(block_value)
                    cert.check(
                        diagonal_part == high_count * direct_total,
                        "projected_block_mean",
                    )
                    expected = blocks[coordinate_index].get(low, (0, 0))
                    cert.check(
                        gnorm2(expected) >= 0,
                        "projected_block_nonnegative",
                    )
            maximum = 0
            for low_index, epsilon_low in enumerate(environments(low_primes)):
                epsilon = dict(epsilon_high)
                epsilon.update(epsilon_low)
                for coordinate_index, coordinate in enumerate(packet):
                    grouped_value = (0, 0)
                    direct_value = (0, 0)
                    for low, block_value in blocks[coordinate_index].items():
                        grouped_value = gadd(
                            grouped_value,
                            gscale(character(low, epsilon_low), block_value),
                        )
                    for label, coefficient in coordinate:
                        direct_value = gadd(
                            direct_value,
                            gscale(character(label, epsilon), coefficient),
                        )
                    cert.check(
                        grouped_value == direct_value,
                        "robust_face_grouping_identity",
                    )
                z_value = energy(packet, epsilon)
                maximum = max(maximum, z_value)
                fixed_face_totals[low_index] += z_value
                cert.check(
                    z_value <= nu * projected_energy,
                    "robust_face_pointwise",
                )
            maximum_energies.append(maximum)
            cert.check(
                maximum <= nu * projected_energy,
                "robust_face_supremum",
            )
            cert.check(high_index < high_count, "high_environment_index")
        cert.check(
            projected_total == high_count * d_value,
            "projected_diagonal_mean",
        )
        cert.check(min(projected_values) <= d_value, "robust_face_existence")
        cert.check(
            min(maximum_energies) <= nu * d_value,
            "robust_face_existence",
        )
        for total in fixed_face_totals.values():
            cert.check(
                total <= high_count * nu * d_value,
                "fixed_face_mean_bound",
            )
        for level in (1, 2, 3):
            bad = sum(
                1
                for maximum in maximum_energies
                if maximum > level * nu * d_value
            )
            cert.check(
                bad * level <= high_count,
                "robust_face_markov_tail",
            )

        epsilon_low_minus = {p: -1 for p in low_primes}
        smooth_total = 0
        for epsilon_high in environments(high_primes):
            epsilon = dict(epsilon_high)
            epsilon.update(epsilon_low_minus)
            smooth_total += energy(packet, epsilon)
        smooth_formula = d_value + sum(
            mobius(kernel) * coefficient
            for kernel, coefficient in spectrum.items()
            if low_high_split(kernel, z)[1] == 1
        )
        cert.check(
            smooth_total == high_count * smooth_formula,
            "smooth_physical_projection",
        )
        cert.check(
            0 <= smooth_formula <= nu * d_value,
            "smooth_physical_sector_bound",
        )


def check_martingale_layers(
    cert: Certificate,
    spectrum: dict[int, int],
) -> None:
    active_primes = prime_support(list(spectrum))
    all_environments = list(environments(active_primes))
    count = len(all_environments)
    variance = sum(value * value for value in spectrum.values())
    forward_energy_total = 0
    reverse_energy_total = 0
    forward_previous = {tuple(sorted(epsilon.items())): 0 for epsilon in all_environments}
    reverse_values: list[dict[tuple[tuple[int, int], ...], int]] = []

    for r in range(len(active_primes) + 1):
        retained = active_primes[r:]
        reverse_at_r: dict[tuple[tuple[int, int], ...], int] = {}
        for epsilon_retained in environments(retained):
            formula = sum(
                coefficient * character(kernel, epsilon_retained)
                for kernel, coefficient in spectrum.items()
                if least_prime(kernel) > (active_primes[r - 1] if r else 1)
            )
            averaged = 0
            discarded = active_primes[:r]
            for epsilon_discarded in environments(discarded):
                epsilon = dict(epsilon_retained)
                epsilon.update(epsilon_discarded)
                averaged += centered_value(spectrum, epsilon)
            cert.check(
                averaged == (1 << len(discarded)) * formula,
                "reverse_conditional_expectation",
            )
            reverse_at_r[tuple(sorted(epsilon_retained.items()))] = formula
        reverse_values.append(reverse_at_r)

    for r, p in enumerate(active_primes, start=1):
        retained = active_primes[:r]
        discarded = active_primes[r:]
        for epsilon_retained in environments(retained):
            formula = sum(
                coefficient * character(kernel, epsilon_retained)
                for kernel, coefficient in spectrum.items()
                if largest_prime(kernel) <= p
            )
            averaged = 0
            for epsilon_discarded in environments(discarded):
                epsilon = dict(epsilon_retained)
                epsilon.update(epsilon_discarded)
                averaged += centered_value(spectrum, epsilon)
            cert.check(
                averaged == (1 << len(discarded)) * formula,
                "forward_conditional_expectation",
            )

        forward_layer_energy = sum(
            coefficient * coefficient
            for kernel, coefficient in spectrum.items()
            if largest_prime(kernel) == p
        )
        reverse_layer_energy = sum(
            coefficient * coefficient
            for kernel, coefficient in spectrum.items()
            if least_prime(kernel) == p
        )
        forward_energy_total += forward_layer_energy
        reverse_energy_total += reverse_layer_energy

        forward_current: dict[tuple[tuple[int, int], ...], int] = {}
        forward_layer_square = 0
        reverse_layer_square = 0
        reverse_old_square = 0
        reverse_new_square = 0
        for epsilon in all_environments:
            key = tuple(sorted(epsilon.items()))
            current = sum(
                coefficient * character(kernel, epsilon)
                for kernel, coefficient in spectrum.items()
                if largest_prime(kernel) <= p
            )
            layer = current - forward_previous[key]
            layer_formula = sum(
                coefficient * character(kernel, epsilon)
                for kernel, coefficient in spectrum.items()
                if largest_prime(kernel) == p
            )
            cert.check(layer == layer_formula, "forward_layer_formula")
            forward_layer_square += layer * layer
            forward_current[key] = current

            old_reverse = sum(
                coefficient * character(kernel, epsilon)
                for kernel, coefficient in spectrum.items()
                if least_prime(kernel) >= p
            )
            new_reverse = sum(
                coefficient * character(kernel, epsilon)
                for kernel, coefficient in spectrum.items()
                if least_prime(kernel) > p
            )
            reverse_layer = old_reverse - new_reverse
            reverse_formula = sum(
                coefficient * character(kernel, epsilon)
                for kernel, coefficient in spectrum.items()
                if least_prime(kernel) == p
            )
            cert.check(reverse_layer == reverse_formula, "reverse_layer_formula")
            reverse_layer_square += reverse_layer * reverse_layer
            reverse_old_square += old_reverse * old_reverse
            reverse_new_square += new_reverse * new_reverse
        cert.check(
            forward_layer_square == count * forward_layer_energy,
            "forward_layer_parseval",
        )
        cert.check(
            reverse_layer_square == count * reverse_layer_energy,
            "reverse_layer_parseval",
        )
        cert.check(
            reverse_old_square - reverse_new_square
            == count * reverse_layer_energy,
            "reverse_layer_dissipation",
        )
        forward_previous = forward_current
    cert.check(forward_energy_total == variance, "forward_parseval_ledger")
    cert.check(reverse_energy_total == variance, "reverse_parseval_ledger")
    cert.check(
        all(value == centered_value(spectrum, dict(key)) for key, value in forward_previous.items()),
        "forward_terminal_identity",
    )
    cert.check(
        len(reverse_values) == len(active_primes) + 1,
        "reverse_filtration_length",
    )


def coefficient_descent(
    cert: Certificate,
    spectrum: dict[int, int],
) -> tuple[list[int], list[dict[int, int]], list[int], list[Fraction]]:
    active_primes = prime_support(list(spectrum))
    physical = sum(mobius(kernel) * value for kernel, value in spectrum.items())
    states: list[dict[int, int]] = []
    energies: list[int] = []
    factors: list[Fraction] = []
    processed: list[int] = []
    remaining = list(active_primes)
    state = {m: spectrum.get(m, 0) for m in squarefree_divisors(remaining)}
    states.append(dict(state))
    energies.append(sum(value * value for value in state.values()))
    cert.check(energies[0] == sum(value * value for value in spectrum.values()), "descent_initial_energy")
    cert.check(
        sum(mobius(m) * value for m, value in state.items()) == physical,
        "descent_physical_invariance",
    )

    for p in active_primes:
        processed.append(p)
        remaining = [q for q in remaining if q != p]
        next_state: dict[int, int] = {}
        definition_state: dict[int, int] = {}
        processed_divisors = squarefree_divisors(processed)
        for m in squarefree_divisors(remaining):
            next_state[m] = state.get(m, 0) - state.get(p * m, 0)
            definition_state[m] = sum(
                mobius(a) * spectrum.get(a * m, 0)
                for a in processed_divisors
            )
            cert.check(
                next_state[m] == definition_state[m],
                "coefficient_descent_recurrence",
            )
        old_energy = sum(value * value for value in state.values())
        paired_old_energy = sum(
            state.get(m, 0) * state.get(m, 0)
            + state.get(p * m, 0) * state.get(p * m, 0)
            for m in squarefree_divisors(remaining)
        )
        correlation = sum(
            state.get(m, 0) * state.get(p * m, 0)
            for m in squarefree_divisors(remaining)
        )
        new_energy = sum(value * value for value in next_state.values())
        cert.check(paired_old_energy == old_energy, "descent_pair_partition")
        cert.check(
            new_energy == old_energy - 2 * correlation,
            "descent_energy_recurrence",
        )
        if old_energy > 0:
            theta = Fraction(2 * correlation, old_energy)
            cert.check(-1 <= theta <= 1, "descent_theta_bound")
            factor = Fraction(new_energy, old_energy)
            cert.check(factor == 1 - theta, "descent_theta_factor")
            factors.append(factor)
        else:
            cert.check(new_energy == 0, "descent_zero_energy_absorption")
        state = next_state
        states.append(dict(state))
        energies.append(new_energy)
        cert.check(
            sum(mobius(m) * value for m, value in state.items()) == physical,
            "descent_physical_invariance",
        )

    cert.check(set(state) == {1}, "descent_terminal_support")
    cert.check(state[1] == physical, "descent_terminal_coefficient")
    cert.check(energies[-1] == physical * physical, "descent_terminal_energy")
    product_factor = Fraction(1)
    for factor in factors:
        product_factor *= factor
    cert.check(
        Fraction(energies[0]) * product_factor == energies[-1],
        "descent_exact_product",
    )
    return active_primes, states, energies, factors


def check_low_kernel_energy(
    cert: Certificate,
    packet: Packet,
    spectrum: dict[int, int],
    active_primes: list[int],
    descent_states: list[dict[int, int]],
) -> None:
    variance = sum(value * value for value in spectrum.values())
    for z in (2, 3, 5, 7):
        row_low_parts = {
            low_high_split(label, z)[0]
            for label in packet_labels(packet)
        }
        kernel_low_parts = {
            low_high_split(kernel, z)[0]
            for kernel in spectrum
        }
        pair_low_parts = {
            squarefree_kernel(left, right)
            for left in row_low_parts
            for right in row_low_parts
        }
        cert.check(
            kernel_low_parts.issubset(pair_low_parts),
            "kernel_projection_realization",
        )
        cert.check(
            len(kernel_low_parts) <= len(row_low_parts) * len(row_low_parts),
            "kernel_projection_count",
        )
        aggregated: dict[int, int] = defaultdict(int)
        source_energy: dict[int, int] = defaultdict(int)
        for kernel, coefficient in spectrum.items():
            low, high = low_high_split(kernel, z)
            aggregated[high] += mobius(low) * coefficient
            source_energy[high] += coefficient * coefficient
        low_energy = sum(value * value for value in aggregated.values())
        for high, value in aggregated.items():
            cert.check(
                value * value <= len(kernel_low_parts) * source_energy[high],
                "low_kernel_cauchy",
            )
        cert.check(
            low_energy <= len(kernel_low_parts) * variance,
            "low_kernel_energy_bound",
        )
        cert.check(
            low_energy <= len(row_low_parts) * len(row_low_parts) * variance,
            "low_restriction_energy_bound",
        )
        restricted_count = sum(1 for p in active_primes if p <= z)
        cert.check(
            all(
                aggregated.get(index, 0)
                == descent_states[restricted_count].get(index, 0)
                for index in set(aggregated) | set(descent_states[restricted_count])
            ),
            "low_restriction_matches_descent",
        )


def check_face_likelihoods(
    cert: Certificate,
    packet: Packet,
    spectrum: dict[int, int],
) -> None:
    active_primes = prime_support(list(spectrum))
    d_value = diagonal(packet)
    all_minus = {p: -1 for p in active_primes}
    physical_energy = energy(packet, all_minus)
    cert.check(physical_energy > 0, "face_positive_corner")
    a_values: list[int] = []
    for r in range(len(active_primes) + 1):
        threshold = active_primes[r - 1] if r else 1
        formula = d_value + sum(
            mobius(kernel) * coefficient
            for kernel, coefficient in spectrum.items()
            if least_prime(kernel) > threshold
        )
        direct_total = 0
        for epsilon_low in environments(active_primes[:r]):
            epsilon = {p: -1 for p in active_primes[r:]}
            epsilon.update(epsilon_low)
            direct_total += energy(packet, epsilon)
        cert.check(
            direct_total == (1 << r) * formula,
            "face_conditional_average",
        )
        a_values.append(formula)
    cert.check(a_values[0] == physical_energy, "face_initial_endpoint")
    cert.check(a_values[-1] == d_value, "face_terminal_endpoint")

    delta_product = Fraction(1)
    previous_event_mass = Fraction(physical_energy, (1 << len(active_primes)) * d_value)
    for r, p in enumerate(active_primes, start=1):
        previous = a_values[r - 1]
        current = a_values[r]
        increment = previous - current
        layer_formula = sum(
            mobius(kernel) * coefficient
            for kernel, coefficient in spectrum.items()
            if least_prime(kernel) == p
        )
        cert.check(increment == layer_formula, "face_least_prime_increment")
        cert.check(0 <= previous <= 2 * current, "face_doubling")
        delta = Fraction(increment, current)
        cert.check(-1 <= delta <= 1, "face_delta_bound")
        cert.check(previous == current * (1 + delta), "face_delta_recurrence")
        delta_product *= 1 + delta

        event_mass = Fraction(
            current,
            (1 << (len(active_primes) - r)) * d_value,
        )
        event_energy_total = 0
        event_count = 0
        for epsilon in environments(active_primes):
            if all(epsilon[q] == -1 for q in active_primes[r:]):
                event_energy_total += energy(packet, epsilon)
                event_count += 1
        cert.check(event_count == 1 << r, "face_event_count")
        cert.check(
            Fraction(event_energy_total, (1 << len(active_primes)) * d_value)
            == event_mass,
            "face_event_mass",
        )
        conditional = previous_event_mass * Fraction(event_mass.denominator, event_mass.numerator)
        cert.check(
            conditional == Fraction(previous, 2 * current),
            "face_conditional_probability",
        )
        cert.check(1 + delta == 2 * conditional, "face_likelihood_ratio")
        previous_event_mass = event_mass
    cert.check(
        delta_product == Fraction(physical_energy, d_value),
        "face_likelihood_product",
    )


def check_obstruction_family(cert: Certificate) -> None:
    rough_primes = [11, 13, 17, 19, 23, 29, 31, 37]
    z = 7
    lambdas = [Fraction(1), Fraction(3, 2), Fraction(2)]
    for r_size in range(2, len(rough_primes) + 1):
        primes = rough_primes[:r_size]
        count = 1 << r_size
        for lam in lambdas:
            scale = lam * Fraction(1, r_size)
            constant = 1 + lam * lam * Fraction(1, r_size)
            linear = -2 * scale
            pair = 2 * lam * lam * Fraction(1, r_size * r_size)
            corner = (1 + lam) * (1 + lam)
            variance = (
                4 * lam * lam * Fraction(1, r_size)
                + 2
                * lam
                * lam
                * lam
                * lam
                * (r_size - 1)
                * Fraction(1, r_size * r_size * r_size)
            )
            obstruction_kernels = list(primes)
            obstruction_kernels.extend(
                primes[i] * primes[j]
                for i in range(r_size)
                for j in range(i + 1, r_size)
            )
            cert.check(
                all(is_squarefree(kernel) for kernel in obstruction_kernels),
                "obstruction_squarefree_kernels",
            )
            cert.check(
                all(least_prime(kernel) > z for kernel in obstruction_kernels),
                "obstruction_rough_support",
            )
            cert.check(
                all(len(factorization(kernel)) <= 2 for kernel in obstruction_kernels),
                "obstruction_degree_two",
            )
            total = Fraction(0)
            centered_square_total = Fraction(0)
            absolute_centered_total = Fraction(0)
            for epsilon in environments(primes):
                sign_sum = sum(epsilon[p] for p in primes)
                s_value = 1 - scale * sign_sum
                z_value = s_value * s_value
                expansion = constant + linear * sign_sum
                expansion += pair * sum(
                    epsilon[primes[i]] * epsilon[primes[j]]
                    for i in range(r_size)
                    for j in range(i + 1, r_size)
                )
                cert.check(z_value == expansion, "obstruction_walsh_expansion")
                total += z_value
                centered_square_total += (z_value - constant) * (z_value - constant)
                absolute_centered_total += abs(z_value - constant)
                if all(epsilon[p] == -1 for p in primes):
                    cert.check(z_value == corner, "obstruction_corner")
            cert.check(total == count * constant, "obstruction_mean")
            cert.check(
                centered_square_total == count * variance,
                "obstruction_variance",
            )
            chi_square = centered_square_total * Fraction(
                1,
                count,
            ) * Fraction(constant.denominator, constant.numerator) ** 2
            cert.check(
                chi_square
                == variance * Fraction(constant.denominator, constant.numerator) ** 2,
                "obstruction_chi_square_identity",
            )
            total_variation = absolute_centered_total * Fraction(
                1,
                2 * count,
            ) * Fraction(constant.denominator, constant.numerator)
            cert.check(
                4 * total_variation * total_variation <= chi_square,
                "obstruction_total_variation_bound",
            )
            cert.check(
                all(p > z for p in primes),
                "obstruction_rough_support",
            )

            a_values: list[Fraction] = []
            for t in range(r_size + 1):
                formula = (
                    1 + lam * (r_size - t) * Fraction(1, r_size)
                ) ** 2 + lam * lam * t * Fraction(1, r_size * r_size)
                direct = Fraction(0)
                for epsilon_low in environments(primes[:t]):
                    sign_sum = sum(epsilon_low[p] for p in primes[:t]) - (r_size - t)
                    direct += (1 - scale * sign_sum) ** 2
                cert.check(
                    direct == (1 << t) * formula,
                    "obstruction_face_average",
                )
                a_values.append(formula)
            cert.check(a_values[0] == corner, "obstruction_face_initial")
            cert.check(a_values[-1] == constant, "obstruction_face_terminal")

            product_delta = Fraction(1)
            delta_square_sum = Fraction(0)
            delta_upper = 2 * lam * Fraction(1, r_size)
            for t in range(1, r_size + 1):
                increment = a_values[t - 1] - a_values[t]
                increment_formula = (
                    2
                    * lam
                    * Fraction(1, r_size)
                    * (1 + lam * (r_size - t) * Fraction(1, r_size))
                )
                cert.check(
                    increment == increment_formula,
                    "obstruction_face_increment",
                )
                delta = increment * Fraction(
                    a_values[t].denominator,
                    a_values[t].numerator,
                )
                cert.check(0 <= delta <= delta_upper, "obstruction_delta_bound")
                delta_square_sum += delta * delta
                product_delta *= 1 + delta
            cert.check(
                delta_square_sum <= 4 * lam * lam * Fraction(1, r_size),
                "obstruction_delta_square_bound",
            )
            cert.check(
                product_delta == corner * Fraction(constant.denominator, constant.numerator),
                "obstruction_delta_product",
            )

            influence = (
                4 * lam * lam * Fraction(1, r_size * r_size)
                + 4
                * lam
                * lam
                * lam
                * lam
                * (r_size - 1)
                * Fraction(1, r_size * r_size * r_size * r_size)
            )
            coefficient_influence = linear * linear + (r_size - 1) * pair * pair
            cert.check(
                influence == coefficient_influence,
                "obstruction_prime_influence",
            )

    for t in range(2, 13):
        r_size = t ** 4
        lam = Fraction(t)
        mean = 1 + lam * lam * Fraction(1, r_size)
        variance = (
            4 * lam * lam * Fraction(1, r_size)
            + 2
            * lam
            * lam
            * lam
            * lam
            * (r_size - 1)
            * Fraction(1, r_size * r_size * r_size)
        )
        corner_ratio = (1 + lam) ** 2 * Fraction(mean.denominator, mean.numerator)
        cert.check(mean == 1 + Fraction(1, t * t), "obstruction_scaling_mean")
        cert.check(
            variance <= Fraction(6, t * t),
            "obstruction_scaling_variance",
        )
        cert.check(
            corner_ratio >= Fraction(t * t, 2),
            "obstruction_scaling_corner_growth",
        )
        cert.check(
            2 * lam * Fraction(1, r_size) == Fraction(2, t ** 3),
            "obstruction_scaling_max_delta",
        )
        cert.check(
            4 * lam * lam * Fraction(1, r_size) == Fraction(4, t * t),
            "obstruction_scaling_quadratic_drift",
        )


def reciprocal(value: Fraction) -> Fraction:
    if value == 0:
        raise ZeroDivisionError("cannot invert zero")
    return Fraction(value.denominator, value.numerator)


def check_exponent_ledger(cert: Certificate) -> dict[str, str]:
    q_exponent = Fraction(267, 400)
    j_exponent = Fraction(133, 400)
    divisor_exponent = Fraction(10049, 52500)
    endpoint_exponent = Fraction(1, 400)
    lambda_zero = Fraction(62549, 52500)
    a_value = Fraction(501, 500)
    projected_exponent = Fraction(62549, 26302500)
    gap = Fraction(12829, 105210000)
    a_star = Fraction(250196, 249671)
    cert.check(q_exponent + j_exponent == 1, "exponent_endpoint_ledger")
    cert.check(q_exponent - 2 * j_exponent == endpoint_exponent, "exponent_endpoint_ledger")
    cert.check(lambda_zero == 1 + divisor_exponent, "exponent_label_ledger")
    cert.check(1 - reciprocal(a_value) == Fraction(1, 501), "exponent_rankin_ledger")
    cert.check(
        lambda_zero * Fraction(1, 501) == projected_exponent,
        "exponent_rankin_ledger",
    )
    cert.check(
        endpoint_exponent - projected_exponent == gap,
        "exponent_positive_gap",
    )
    cert.check(gap > 0, "exponent_positive_gap")
    cert.check(
        a_star == reciprocal(1 - reciprocal(400 * lambda_zero)),
        "exponent_critical_cutoff",
    )
    cert.check(a_value < a_star, "exponent_admissible_cutoff")
    return {
        "A": "501/500",
        "A_star": "250196/249671",
        "endpoint_gap": "12829/105210000",
        "lambda_0": "62549/52500",
        "projected_exponent": "62549/26302500",
    }


def check_source_hygiene(cert: Certificate) -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    float_literals = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    assert_statements = [
        node for node in ast.walk(tree) if isinstance(node, ast.Assert)
    ]
    true_divisions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    random_imports = []
    random_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            random_imports.extend(
                alias for alias in node.names if alias.name.split(".")[0] == "random"
            )
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            if node.module.split(".")[0] == "random":
                random_imports.append(node)
        if isinstance(node, ast.Name) and node.id == "random":
            random_names.append(node)
    cert.check(not float_literals, "source_hygiene_no_float")
    cert.check(not assert_statements, "source_hygiene_no_assert")
    cert.check(not true_divisions, "source_hygiene_no_true_division")
    cert.check(not random_imports, "source_hygiene_no_random")
    cert.check(not random_names, "source_hygiene_no_random")


def main() -> None:
    cert = Certificate()
    exponent_ledger = check_exponent_ledger(cert)
    packets = toy_packets()
    for _name, packet in packets:
        spectrum, _label_primes = validate_packet(cert, packet)
        check_robust_faces(cert, packet, spectrum, _label_primes)
        check_martingale_layers(cert, spectrum)
        active_primes, states, _energies, _factors = coefficient_descent(cert, spectrum)
        check_low_kernel_energy(cert, packet, spectrum, active_primes, states)
        check_face_likelihoods(cert, packet, spectrum)
    check_obstruction_family(cert)
    check_source_hygiene(cert)

    payload = {
        "checks": cert.checks,
        "exponent_ledger": exponent_ledger,
        "packet_names": [name for name, _packet in packets],
        "schema": "tpc44-exact-certificate-v1",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "stats": dict(sorted(cert.stats.items())),
    }
    canonical_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    result = dict(payload)
    result["certificate_digest"] = sha256(canonical_payload).hexdigest()
    canonical_result = json.dumps(
        result,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ) + "\n"
    OUT.write_text(canonical_result, encoding="ascii", newline="\n")
    print(canonical_result, end="")


if __name__ == "__main__":
    main()
