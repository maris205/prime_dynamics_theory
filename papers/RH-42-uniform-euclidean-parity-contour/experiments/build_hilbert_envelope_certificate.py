"""Validate continuum Hilbert--Schmidt derivative norms by one-dimensional Arb integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "hilbert_schmidt_envelope_certificate.json"
PRECISION = 160
CRITICAL_U_MIDPOINT = (
    "1.543689012692076361570855971801747986525203297650983935240804"
)
CRITICAL_U_RADIUS = "1e-60"
SIGMA = arb(1) / 100
NAMES = (
    "kernel",
    "source_first",
    "target_first",
    "source_second",
    "source_target",
    "target_second",
    "source_second_target_second",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def poly_add(
    left: list[acb], right: list[acb]
) -> list[acb]:
    size = max(len(left), len(right))
    result = [acb(0) for _ in range(size)]
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return result


def poly_scale(values: list[acb], scalar: acb) -> list[acb]:
    return [scalar * value for value in values]


def poly_multiply(
    left: list[acb], right: list[acb]
) -> list[acb]:
    result = [acb(0) for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += (
                left_value * right_value
            )
    return result


def poly_derivative(values: list[acb]) -> list[acb]:
    if len(values) <= 1:
        return [acb(0)]
    return [
        arb(index) * values[index]
        for index in range(1, len(values))
    ]


def gaussian_target_derivative(
    polynomial: list[acb], offset: list[acb]
) -> list[acb]:
    return poly_add(
        poly_derivative(polynomial),
        poly_scale(
            poly_multiply(offset, polynomial),
            -1 / (SIGMA * SIGMA),
        ),
    )


def gaussian_target_second(
    polynomial: list[acb], offset: list[acb]
) -> list[acb]:
    return gaussian_target_derivative(
        gaussian_target_derivative(polynomial, offset),
        offset,
    )


def gaussian_power_integrals(
    center: acb, degree: int
) -> list[acb]:
    lower = -center / SIGMA
    upper = (1 - center) / SIGMA
    exp_lower = (-(lower * lower)).exp()
    exp_upper = (-(upper * upper)).exp()
    standardized = [
        acb.pi().sqrt() * (upper.erf() - lower.erf()) / 2,
        (exp_lower - exp_upper) / 2,
    ]
    for power in range(2, degree + 1):
        standardized.append(
            (
                lower ** (power - 1) * exp_lower
                - upper ** (power - 1) * exp_upper
            )
            / 2
            + arb(power - 1) * standardized[power - 2] / 2
        )
    moments = []
    for power in range(degree + 1):
        value = acb(0)
        for shifted_power in range(power + 1):
            value += (
                math.comb(power, shifted_power)
                * center ** (power - shifted_power)
                * SIGMA**shifted_power
                * standardized[shifted_power]
            )
        moments.append(SIGMA * value)
    return moments


def integrate_polynomial_gaussian(
    coefficients: list[acb], center: acb
) -> acb:
    moments = gaussian_power_integrals(
        center, len(coefficients) - 1
    )
    return sum(
        (
            coefficient * moments[index]
            for index, coefficient in enumerate(coefficients)
        ),
        acb(0),
    )


def normalizer(mean: acb) -> tuple[acb, acb, acb]:
    root_two = acb(2).sqrt()
    prefactor = SIGMA * (acb.pi() / 2).sqrt()
    left = (-((1 + mean) / SIGMA) ** 2 / 2).exp()
    right = (-((1 - mean) / SIGMA) ** 2 / 2).exp()
    value = prefactor * (
        ((1 - mean) / (root_two * SIGMA)).erf()
        + ((1 + mean) / (root_two * SIGMA)).erf()
    )
    first = left - right
    second = (
        -(1 + mean) * left - (1 - mean) * right
    ) / (SIGMA * SIGMA)
    return value, first, second


def quantity_polynomials(
    source: acb, name: str
) -> tuple[list[acb], list[acb], acb, acb]:
    critical_u = acb(
        arb(f"{CRITICAL_U_MIDPOINT} +/- {CRITICAL_U_RADIUS}")
    )
    mean = 1 - critical_u * source * source
    mean_first = -2 * critical_u * source
    mean_second = -2 * critical_u
    z, zm, zmm = normalizer(mean)
    ratio = zm / z
    second_ratio = 2 * ratio * ratio - zmm / z
    inv_sigma_square = 1 / (SIGMA * SIGMA)
    inv_sigma_four = inv_sigma_square * inv_sigma_square
    minus_offset = [-mean, acb(1)]
    plus_offset = [mean, acb(1)]
    minus_square = poly_multiply(minus_offset, minus_offset)
    plus_square = poly_multiply(plus_offset, plus_offset)
    constant_one = [acb(1)]

    kernel_plus = constant_one
    kernel_minus = constant_one
    target_first_plus = poly_scale(
        minus_offset, -inv_sigma_square
    )
    target_first_minus = poly_scale(
        plus_offset, -inv_sigma_square
    )
    target_second_plus = poly_add(
        poly_scale(minus_square, inv_sigma_four),
        [-inv_sigma_square],
    )
    target_second_minus = poly_add(
        poly_scale(plus_square, inv_sigma_four),
        [-inv_sigma_square],
    )
    parameter_first_plus = poly_add(
        poly_scale(minus_offset, inv_sigma_square),
        [-ratio],
    )
    parameter_first_minus = poly_add(
        poly_scale(plus_offset, -inv_sigma_square),
        [-ratio],
    )
    parameter_second_plus = poly_add(
        poly_add(
            target_second_plus,
            poly_scale(
                minus_offset, -2 * ratio * inv_sigma_square
            ),
        ),
        [second_ratio],
    )
    parameter_second_minus = poly_add(
        poly_add(
            target_second_minus,
            poly_scale(
                plus_offset, 2 * ratio * inv_sigma_square
            ),
        ),
        [second_ratio],
    )
    parameter_target_plus = poly_add(
        poly_add(
            [inv_sigma_square],
            poly_scale(minus_square, -inv_sigma_four),
        ),
        poly_scale(
            minus_offset, ratio * inv_sigma_square
        ),
    )
    parameter_target_minus = poly_add(
        poly_add(
            [-inv_sigma_square],
            poly_scale(plus_square, inv_sigma_four),
        ),
        poly_scale(
            plus_offset, ratio * inv_sigma_square
        ),
    )

    pairs = {
        "kernel": (kernel_plus, kernel_minus),
        "source_first": (
            poly_scale(parameter_first_plus, mean_first),
            poly_scale(parameter_first_minus, mean_first),
        ),
        "target_first": (
            target_first_plus,
            target_first_minus,
        ),
        "source_second": (
            poly_add(
                poly_scale(
                    parameter_second_plus, mean_first * mean_first
                ),
                poly_scale(parameter_first_plus, mean_second),
            ),
            poly_add(
                poly_scale(
                    parameter_second_minus,
                    mean_first * mean_first,
                ),
                poly_scale(parameter_first_minus, mean_second),
            ),
        ),
        "source_target": (
            poly_scale(parameter_target_plus, mean_first),
            poly_scale(parameter_target_minus, mean_first),
        ),
        "target_second": (
            target_second_plus,
            target_second_minus,
        ),
        "source_second_target_second": (
            poly_add(
                poly_scale(
                    gaussian_target_second(
                        parameter_second_plus, minus_offset
                    ),
                    mean_first * mean_first,
                ),
                poly_scale(
                    gaussian_target_second(
                        parameter_first_plus, minus_offset
                    ),
                    mean_second,
                ),
            ),
            poly_add(
                poly_scale(
                    gaussian_target_second(
                        parameter_second_minus, plus_offset
                    ),
                    mean_first * mean_first,
                ),
                poly_scale(
                    gaussian_target_second(
                        parameter_first_minus, plus_offset
                    ),
                    mean_second,
                ),
            ),
        ),
    }
    plus, minus = pairs[name]
    return plus, minus, mean, z


def row_square(source: acb, name: str) -> acb:
    plus, minus, mean, z = quantity_polynomials(source, name)
    plus_square = poly_multiply(plus, plus)
    minus_square = poly_multiply(minus, minus)
    cross = poly_scale(poly_multiply(plus, minus), acb(2))
    value = integrate_polynomial_gaussian(plus_square, mean)
    value += integrate_polynomial_gaussian(minus_square, -mean)
    value += (
        (-(mean / SIGMA) ** 2).exp()
        * integrate_polynomial_gaussian(cross, acb(0))
    )
    return value / (z * z)


def upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def integrate_quantity(
    name: str, tolerance: arb, eval_limit: int
) -> dict[str, object]:
    result = acb.integral(
        lambda source, analytic: row_square(source, name),
        0,
        1,
        rel_tol=tolerance,
        abs_tol=tolerance,
        eval_limit=eval_limit,
        depth_limit=30,
        use_heap=True,
    )
    norm = result.sqrt()
    if not result.is_finite() or not norm.is_finite():
        raise RuntimeError(f"non-finite Arb integral for {name}")
    square_upper = upper_float(result.real)
    if not result.imag.contains(0) or square_upper < 0.0:
        raise RuntimeError(f"invalid real integral enclosure for {name}")
    norm_upper = math.nextafter(
        math.sqrt(max(0.0, square_upper)), math.inf
    )
    return {
        "square_ball": str(result),
        "square_upper": square_upper,
        "norm_ball": str(norm),
        "norm_upper": norm_upper,
        "imaginary_part_ball": str(result.imag),
        "imaginary_part_contains_zero": bool(result.imag.contains(0)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=PRECISION)
    parser.add_argument("--tolerance", default="1e-18")
    parser.add_argument("--eval-limit", type=int, default=1000000)
    parser.add_argument("--name", choices=NAMES)
    arguments = parser.parse_args()
    previous = ctx.prec
    ctx.prec = int(arguments.precision)
    try:
        tolerance = arb(arguments.tolerance)
        names = (arguments.name,) if arguments.name else NAMES
        quantities = {}
        for name in names:
            print(f"integrating {name}", flush=True)
            quantities[name] = integrate_quantity(
                name, tolerance, int(arguments.eval_limit)
            )
            print(
                f"{name}: {quantities[name]['norm_upper']:.12g}",
                flush=True,
            )
        payload = {
            "status": (
                "rigorous_arb_hilbert_schmidt_derivative_envelope"
            ),
            "evidence_level": (
                f"{int(arguments.precision)}_bit_arb_closed_target_integrals_"
                "plus_validated_source_integration"
            ),
            "arb_precision_bits": int(arguments.precision),
            "integration_tolerance": arguments.tolerance,
            "critical_u_ball": (
                f"{CRITICAL_U_MIDPOINT} +/- {CRITICAL_U_RADIUS}"
            ),
            "sigma_exact": "1/100",
            "quantities": quantities,
            "source_sha256": sha256_file(Path(__file__)),
        }
    finally:
        ctx.prec = previous
    if arguments.name:
        print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
