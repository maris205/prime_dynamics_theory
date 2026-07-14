#!/usr/bin/env python3
"""Deterministic finite checks for the factor-ray identities in TPC-11.

The certificate checks finite algebra, frequency spacing, kernel identities,
determinant-layer counts, and endpoint geometry.  It does not test or estimate
any fixed-shift prime-pair asymptotic.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


def prime_power_base(n: int) -> int | None:
    """Return p if n is a positive power of the prime p, otherwise None."""
    if n < 2:
        return None
    p = 2
    while p * p <= n and n % p:
        p = 3 if p == 2 else p + 2
    if p * p > n:
        return n
    remainder = n
    while remainder % p == 0:
        remainder //= p
    return p if remainder == 1 else None


def von_mangoldt(n: int) -> float:
    p = prime_power_base(n)
    return 0.0 if p is None else math.log(p)


def bump_weight(v: float, alpha: float, beta: float) -> float:
    """A compactly supported C1 polynomial bump normalized to height one."""
    if not alpha < v < beta:
        return 0.0
    half_width = 0.5 * (beta - alpha)
    z = ((v - alpha) * (beta - v)) / (half_width * half_width)
    return z * z


def supported_pairs(
    X: int, D: int, h: int, alpha: float, beta: float
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    product_max = math.floor(beta * X)
    for n in range(D + 1, product_max + 1):
        for m in range(1, product_max // n + 1):
            v = n * m / X
            w = bump_weight(v, alpha, beta)
            if w == 0.0:
                continue
            ray = Fraction(n, m)
            coefficient = (
                (von_mangoldt(n) - 1.0)
                * (von_mangoldt(n * m + h) - 1.0)
                * w
            )
            rows.append(
                {
                    "n": n,
                    "m": m,
                    "ray": ray,
                    "coefficient": coefficient,
                    "coordinate": math.log(n / m),
                }
            )
    return rows


def compress_rays(rows: Sequence[dict[str, object]]) -> dict[Fraction, float]:
    buckets: dict[Fraction, list[float]] = defaultdict(list)
    for row in rows:
        buckets[row["ray"]].append(float(row["coefficient"]))
    return {ray: math.fsum(values) for ray, values in buckets.items()}


def stable_complex_sum(values: Iterable[complex]) -> complex:
    values = list(values)
    return complex(
        math.fsum(value.real for value in values),
        math.fsum(value.imag for value in values),
    )


def direct_transform(rows: Sequence[dict[str, object]], t: float) -> complex:
    return stable_complex_sum(
        float(row["coefficient"])
        * cmath.exp(1j * t * float(row["coordinate"]))
        for row in rows
    )


def ray_transform(rays: dict[Fraction, float], t: float) -> complex:
    return stable_complex_sum(
        coefficient * cmath.exp(1j * t * math.log(ray.numerator / ray.denominator))
        for ray, coefficient in rays.items()
    )


def hard_kernel(x: float, T: float) -> float:
    return 2.0 * T if x == 0.0 else 2.0 * math.sin(T * x) / x


def hard_form_from_pairs(rows: Sequence[dict[str, object]], T: float) -> float:
    return math.fsum(
        float(left["coefficient"])
        * float(right["coefficient"])
        * hard_kernel(
            float(left["coordinate"]) - float(right["coordinate"]), T
        )
        for left in rows
        for right in rows
    )


def hard_form_from_rays(rays: dict[Fraction, float], T: float) -> float:
    items = [
        (math.log(ray.numerator / ray.denominator), coefficient)
        for ray, coefficient in rays.items()
    ]
    return math.fsum(
        left_coefficient
        * right_coefficient
        * hard_kernel(left_frequency - right_frequency, T)
        for left_frequency, left_coefficient in items
        for right_frequency, right_coefficient in items
    )


def ray_spacing(
    rays: Iterable[Fraction], beta: float, X: int
) -> dict[str, object]:
    ordered = sorted(rays, key=lambda ray: ray.numerator / ray.denominator)
    best_gap = math.inf
    best_pair: tuple[Fraction, Fraction] | None = None
    for left, right in zip(ordered, ordered[1:]):
        gap = math.log(right.numerator / right.denominator) - math.log(
            left.numerator / left.denominator
        )
        if gap < best_gap:
            best_gap = gap
            best_pair = (left, right)
    theoretical = 2.0 * math.asinh(1.0 / (2.0 * beta * X))
    assert best_pair is not None
    return {
        "observed_min_gap": best_gap,
        "theoretical_delta_X": theoretical,
        "ratio": best_gap / theoretical,
        "minimizing_rays": [str(best_pair[0]), str(best_pair[1])],
        "bound_verified": best_gap + 1e-14 >= theoretical,
    }


def fejer_form(rays: dict[Fraction, float], T: float) -> tuple[float, float, int]:
    items = [
        (math.log(ray.numerator / ray.denominator), coefficient)
        for ray, coefficient in rays.items()
    ]
    surviving_off_diagonal = 0
    full = 0.0
    for i, (left_frequency, left_coefficient) in enumerate(items):
        for j, (right_frequency, right_coefficient) in enumerate(items):
            scaled_gap = T * abs(left_frequency - right_frequency)
            multiplier = max(1.0 - scaled_gap, 0.0)
            if i != j and multiplier > 1e-13:
                surviving_off_diagonal += 1
            full += T * multiplier * left_coefficient * right_coefficient
    diagonal = T * math.fsum(value * value for _, value in items)
    return full, diagonal, surviving_off_diagonal


def determinant_layers(
    rays: Iterable[Fraction],
    T_values: Sequence[float],
    X: int,
    beta: float,
    L: float = 1.0,
) -> list[dict[str, object]]:
    rays = list(rays)
    output: list[dict[str, object]] = []
    for T in T_values:
        layers: Counter[int] = Counter()
        allowed_ordered_pairs = 0
        for left in rays:
            for right in rays:
                if left == right:
                    continue
                log_gap = abs(
                    math.log(
                        (left.numerator * right.denominator)
                        / (left.denominator * right.numerator)
                    )
                )
                if T * log_gap <= L + 1e-14:
                    determinant = abs(
                        left.numerator * right.denominator
                        - left.denominator * right.numerator
                    )
                    layers[determinant] += 1
                    allowed_ordered_pairs += 1
        determinant_bound = 2.0 * beta * X * math.sinh(L / (2.0 * T))
        largest_determinant = max(layers, default=0)
        output.append(
            {
                "T": T,
                "support_allowed_ordered_off_diagonal_pairs": allowed_ordered_pairs,
                "distinct_nonzero_determinants": len(layers),
                "largest_allowed_determinant": largest_determinant,
                "theoretical_determinant_bound": determinant_bound,
                "determinant_bound_verified": (
                    largest_determinant <= determinant_bound + 1e-10
                ),
                "layer_counts": {str(key): layers[key] for key in sorted(layers)},
            }
        )
    return output


def endpoint_geometry(
    rows: Sequence[dict[str, object]], X: int, D: int, alpha: float, beta: float
) -> dict[str, object]:
    selected_violations = 0
    rejected_violations = 0
    selected_count = 0
    rejected_count = 0
    lower = math.log(alpha)
    upper = math.log(beta)
    rejection_boundary = math.log(beta / 4.0)
    for row in rows:
        n = int(row["n"])
        m = int(row["m"])
        coordinate = math.log(n / m) - math.log(X)
        if m == 1:
            selected_count += 1
            if not lower - 1e-14 <= coordinate <= upper + 1e-14 or n <= D:
                selected_violations += 1
        else:
            rejected_count += 1
            if coordinate > rejection_boundary + 1e-14:
                rejected_violations += 1
    return {
        "beta_less_than_4alpha": beta < 4.0 * alpha,
        "D_less_than_alpha_X": D < alpha * X,
        "m_equals_1_rows": selected_count,
        "m_at_least_2_rows": rejected_count,
        "selected_window_violations": selected_violations,
        "rejection_boundary_violations": rejected_violations,
        "selector_verified": selected_violations == 0 and rejected_violations == 0,
    }


def relative_error(left: float | complex, right: float | complex) -> float:
    return abs(left - right) / max(1.0, abs(left), abs(right))


def build_certificate(
    X: int = 72,
    D: int = 4,
    h: int = 2,
    alpha: float = 0.75,
    beta: float = 2.25,
) -> dict[str, object]:
    if not (0.0 < alpha < beta < 4.0 * alpha):
        raise ValueError("Require 0 < alpha < beta < 4 alpha")
    if not D < alpha * X:
        raise ValueError("Require D < alpha X for endpoint certification")

    rows = supported_pairs(X, D, h, alpha, beta)
    rays = compress_rays(rows)
    sample_frequencies = [0.0, 0.375, 1.25, 4.5]
    transform_checks = []
    for t in sample_frequencies:
        direct = direct_transform(rows, t)
        compressed = ray_transform(rays, t)
        transform_checks.append(
            {
                "t": t,
                "direct": [direct.real, direct.imag],
                "compressed": [compressed.real, compressed.imag],
                "relative_error": relative_error(direct, compressed),
            }
        )

    spacing = ray_spacing(rays, beta, X)
    hard_T = 7.25
    hard_direct = hard_form_from_pairs(rows, hard_T)
    hard_compressed = hard_form_from_rays(rays, hard_T)

    fejer_T = 1.05 / float(spacing["observed_min_gap"])
    fejer_full, fejer_diagonal, surviving = fejer_form(rays, fejer_T)

    layer_T_values = [math.sqrt(X), X / 2.0, X, 2.0 * X]
    layers = determinant_layers(rays, layer_T_values, X=X, beta=beta)
    endpoint = endpoint_geometry(rows, X, D, alpha, beta)

    checks = {
        "ray_compression": max(
            float(item["relative_error"]) for item in transform_checks
        )
        < 5e-12,
        "hyperbolic_spacing": bool(spacing["bound_verified"]),
        "hard_kernel_compression": relative_error(hard_direct, hard_compressed)
        < 5e-11,
        "fejer_exact_diagonal": relative_error(fejer_full, fejer_diagonal)
        < 5e-12
        and surviving == 0,
        "endpoint_selector_geometry": bool(endpoint["selector_verified"]),
        "determinant_counts_monotone": all(
            int(left["support_allowed_ordered_off_diagonal_pairs"])
            >= int(right["support_allowed_ordered_off_diagonal_pairs"])
            for left, right in zip(layers, layers[1:])
        ),
        "determinant_layer_bound": all(
            bool(layer["determinant_bound_verified"]) for layer in layers
        ),
    }

    certificate: dict[str, object] = {
        "scope": (
            "Finite algebraic regression certificate only; no prime-pair "
            "asymptotic or twin-prime inference."
        ),
        "parameters": {
            "X": X,
            "D": D,
            "h": h,
            "alpha": alpha,
            "beta": beta,
            "weight": "squared polynomial bump on (alpha,beta)",
        },
        "counts": {"factor_pairs": len(rows), "primitive_rays": len(rays)},
        "transform_checks": transform_checks,
        "spacing": spacing,
        "hard_band": {
            "T": hard_T,
            "pair_form": hard_direct,
            "ray_form": hard_compressed,
            "relative_error": relative_error(hard_direct, hard_compressed),
        },
        "fejer_band": {
            "T": fejer_T,
            "full_form": fejer_full,
            "diagonal_form": fejer_diagonal,
            "relative_error": relative_error(fejer_full, fejer_diagonal),
            "surviving_ordered_off_diagonal_pairs": surviving,
        },
        "determinant_layers": layers,
        "endpoint_geometry": endpoint,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate["payload_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("data") / "factor-ray-certificate.json",
    )
    args = parser.parse_args()
    certificate = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(certificate["checks"], indent=2, sort_keys=True))
    print(f"all_checks_passed={certificate['all_checks_passed']}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
