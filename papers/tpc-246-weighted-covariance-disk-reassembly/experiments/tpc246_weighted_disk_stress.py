#!/usr/bin/env python3
"""Exact forward/reverse stress suite for TPC-246 weighted disks."""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction


class CheckFailure(RuntimeError):
    """Fail-closed stress error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


Gaussian = tuple[Fraction, Fraction]


def g(re: Fraction | int, im: Fraction | int = 0) -> Gaussian:
    return Fraction(re), Fraction(im)


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def conj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def scale(factor: Fraction, value: Gaussian) -> Gaussian:
    return factor * value[0], factor * value[1]


def norm2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def local_grid(radius: Fraction) -> list[Gaussian]:
    return [g(0), g(radius), g(-radius), g(0, radius), g(0, -radius)]


def weighted_sum(weights: list[Gaussian], values: list[Gaussian]) -> Gaussian:
    total = g(0)
    for weight, value in zip(weights, values):
        total = add(total, mul(weight, value))
    return total


def reverse(weights: list[Gaussian], moduli: list[Fraction],
            radii: list[Fraction], radius: Fraction,
            deviation: Gaussian) -> list[Gaussian]:
    require(radius > 0, "positive reverse radius")
    result: list[Gaussian] = []
    for weight, modulus, local_radius in zip(weights, moduli, radii):
        if modulus == 0:
            result.append(g(0))
        else:
            result.append(scale(local_radius / (modulus * radius),
                                mul(conj(weight), deviation)))
    return result


def target_grid(radius: Fraction) -> list[Gaussian]:
    coordinates = [-radius, -radius / 2, Fraction(0), radius / 2, radius]
    return [g(x, y) for x, y in itertools.product(coordinates, repeat=2)
            if x * x + y * y <= radius * radius]


def run() -> None:
    systems = [
        {
            "weights": [g(Fraction(3, 5), Fraction(4, 5)),
                        g(Fraction(-5, 13), Fraction(12, 13)), g(2)],
            "moduli": [Fraction(1), Fraction(1), Fraction(2)],
            "radii": [Fraction(1), Fraction(1, 2), Fraction(1, 4)],
        },
        {
            "weights": [g(0), g(0)],
            "moduli": [Fraction(0), Fraction(0)],
            "radii": [Fraction(2), Fraction(0)],
        },
        {
            "weights": [g(2), g(0, -1)],
            "moduli": [Fraction(2), Fraction(1)],
            "radii": [Fraction(1, 3), Fraction(1, 2)],
        },
    ]

    forward_count = 0
    reverse_count = 0
    degenerate_count = 0
    for index, system in enumerate(systems):
        weights = system["weights"]
        moduli = system["moduli"]
        radii = system["radii"]
        require(len(weights) == len(moduli) == len(radii), "system lengths")
        for weight, modulus in zip(weights, moduli):
            require(norm2(weight) == modulus * modulus, "modulus mismatch")
        radius = sum((modulus * local_radius
                      for modulus, local_radius in zip(moduli, radii)), Fraction(0))

        for local_values in itertools.product(*(local_grid(value) for value in radii)):
            aggregate = weighted_sum(weights, list(local_values))
            require(norm2(aggregate) <= radius * radius,
                    f"forward containment system {index}")
            forward_count += 1

        if radius == 0:
            require(all(weighted_sum(weights, list(values)) == g(0)
                        for values in itertools.product(
                            *(local_grid(value) for value in radii))),
                    "degenerate singleton")
            reverse_count += 1
            degenerate_count += 1
            continue

        targets = target_grid(radius)
        require(len(targets) == 13, "target census")
        for target in targets:
            local_values = reverse(weights, moduli, radii, radius, target)
            for value, local_radius in zip(local_values, radii):
                require(norm2(value) <= local_radius * local_radius,
                        "reverse local containment")
            require(weighted_sum(weights, local_values) == target,
                    "reverse exactness")
            reverse_count += 1

    # Two independent circles of radii 2 and 1 cannot reach the origin.
    # The reverse triangle inequality gives a sharp inner radius of 1.
    circle_samples = [g(2), g(-2), g(0, 2), g(0, -2)]
    small_samples = [g(1), g(-1), g(0, 1), g(0, -1)]
    circle_pairs = 0
    sampled_minimum = None
    for left, right in itertools.product(circle_samples, small_samples):
        value = add(left, right)
        value_norm2 = norm2(value)
        require(value_norm2 >= 1, "circle annulus inner radius")
        sampled_minimum = (value_norm2 if sampled_minimum is None
                           else min(sampled_minimum, value_norm2))
        circle_pairs += 1
    require(sampled_minimum == 1, "circle annulus sharp sample")

    require(forward_count == 175, "forward census")
    require(reverse_count == 27, "reverse census")
    require(degenerate_count == 1 and circle_pairs == 16, "auxiliary census")
    print("TPC246_WEIGHTED_DISK_STRESS=PASS")
    print("systems=3")
    print("forward_product_points=175")
    print("reverse_disk_targets=27")
    print("degenerate_zero_radius_systems=1")
    print("circle_annulus_pairs=16")
    print("circle_to_disk_promotion=REJECTED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC246_WEIGHTED_DISK_STRESS=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC246_WEIGHTED_DISK_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
