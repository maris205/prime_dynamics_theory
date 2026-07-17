"""Outward Schur-similarity and exact dyadic circle certificates."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import math

from flint import arb, ctx
import numpy as np


def _upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _lower_float(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def _upward_add(left: float, right: float) -> float:
    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or math.isnan(first + second):
        raise ValueError("outward bounds must be nonnegative")
    return math.nextafter(first + second, math.inf)


def _upward_multiply(left: float, right: float) -> float:
    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or math.isnan(first + second):
        raise ValueError("outward bounds must be nonnegative")
    return math.nextafter(first * second, math.inf)


def combine_frobenius_bounds(bounds) -> float:
    """Combine block Frobenius upper bounds by an outward Euclidean sum."""

    total = 0.0
    count = 0
    for value in bounds:
        item = float(value)
        total = _upward_add(total, _upward_multiply(item, item))
        count += 1
    if count == 0:
        return 0.0
    return math.nextafter(math.sqrt(total), math.inf)


def sha256_array(values: np.ndarray) -> str:
    """Hash an array together with its exact dtype and shape metadata."""

    array = np.ascontiguousarray(values)
    digest = hashlib.sha256()
    digest.update(array.dtype.str.encode("ascii"))
    digest.update(repr(tuple(array.shape)).encode("ascii"))
    digest.update(array.view(np.uint8))
    return digest.hexdigest()


@dataclass(frozen=True)
class SimilarityCertificate:
    """Bounds for the exact similarity and the boundary homotopy."""

    unitarity_defect_upper: float
    schur_residual_frobenius_upper: float
    complement_resolvent_upper: float
    z_two_norm_upper: float
    z_inverse_two_norm_upper: float
    similarity_condition_upper: float
    transformed_residual_upper: float
    transformed_resolvent_upper: float
    homotopy_neumann_product_upper: float
    homotopy_denominator_lower: float
    invertibility_certified: bool
    homotopy_certified: bool


def similarity_certificate(
    unitarity_defect_upper: float,
    schur_residual_frobenius_upper: float,
    complement_resolvent_upper: float,
    *,
    precision: int = 256,
) -> SimilarityCertificate:
    r"""Certify the Schur comparison from ``BZ-ZT=R``.

    If ``eta >= ||Z*Z-I||_2`` is below one, then

    ``||Z|| <= sqrt(1+eta)`` and ``||Z^-1|| <= 1/sqrt(1-eta)``.

    For ``C=Z^-1 B Z`` this gives

    ``||C-T|| <= ||Z^-1|| ||R||``

    and transports a complement resolvent bound to ``C``.  A Neumann
    product below one keeps the complete segment from ``C`` to ``T``
    invertible on the relevant boundary set.
    """

    eta_value = float(unitarity_defect_upper)
    residual_value = float(schur_residual_frobenius_upper)
    resolvent_value = float(complement_resolvent_upper)
    if any(
        value < 0.0 or math.isnan(value)
        for value in (eta_value, residual_value, resolvent_value)
    ):
        raise ValueError("certificate inputs must be nonnegative")

    previous_precision = ctx.prec
    try:
        ctx.prec = int(precision)
        eta = arb(eta_value).upper()
        residual = arb(residual_value).upper()
        resolvent = arb(resolvent_value).upper()
        invertible = bool(eta < 1)
        if not invertible:
            infinity = float("inf")
            return SimilarityCertificate(
                unitarity_defect_upper=eta_value,
                schur_residual_frobenius_upper=residual_value,
                complement_resolvent_upper=resolvent_value,
                z_two_norm_upper=infinity,
                z_inverse_two_norm_upper=infinity,
                similarity_condition_upper=infinity,
                transformed_residual_upper=infinity,
                transformed_resolvent_upper=infinity,
                homotopy_neumann_product_upper=infinity,
                homotopy_denominator_lower=0.0,
                invertibility_certified=False,
                homotopy_certified=False,
            )
        z_norm = (1 + eta).sqrt().upper()
        z_inverse = (1 / (1 - eta).sqrt()).upper()
        condition = (z_norm * z_inverse).upper()
        transformed_residual = (z_inverse * residual).upper()
        transformed_resolvent = (
            z_inverse * z_norm * resolvent
        ).upper()
        product = (
            transformed_resolvent * transformed_residual
        ).upper()
        homotopy = bool(product < 1)
        denominator = (1 - product).lower() if homotopy else arb(0)
        return SimilarityCertificate(
            unitarity_defect_upper=eta_value,
            schur_residual_frobenius_upper=residual_value,
            complement_resolvent_upper=resolvent_value,
            z_two_norm_upper=_upper_float(z_norm),
            z_inverse_two_norm_upper=_upper_float(z_inverse),
            similarity_condition_upper=_upper_float(condition),
            transformed_residual_upper=_upper_float(transformed_residual),
            transformed_resolvent_upper=_upper_float(transformed_resolvent),
            homotopy_neumann_product_upper=_upper_float(product),
            homotopy_denominator_lower=(
                max(0.0, _lower_float(denominator)) if homotopy else 0.0
            ),
            invertibility_certified=True,
            homotopy_certified=homotopy,
        )
    finally:
        ctx.prec = previous_precision


@dataclass(frozen=True)
class CircleClassification:
    """Exact dyadic classification of a stored complex diagonal."""

    inside_count: int
    outside_count: int
    boundary_count: int
    nearest_index: int
    nearest_value: complex
    minimum_floating_boundary_distance: float
    nearest_squared_margin_numerator: int
    nearest_squared_margin_denominator: int
    records: tuple[dict[str, object], ...]


def _fraction(value: float) -> Fraction:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("circle classification requires finite binary64 data")
    return Fraction.from_float(number)


def classify_binary64_diagonal(
    diagonal: np.ndarray,
    center: complex,
    radius: float,
) -> CircleClassification:
    """Classify exact stored binary64 points relative to an exact stored circle."""

    values = np.asarray(diagonal, dtype=np.complex128).reshape(-1)
    point = complex(center)
    radius_value = float(radius)
    if radius_value <= 0.0:
        raise ValueError("circle radius must be positive")
    center_real = _fraction(point.real)
    center_imag = _fraction(point.imag)
    radius_fraction = _fraction(radius_value)
    radius_square = radius_fraction * radius_fraction
    records: list[dict[str, object]] = []
    margins: list[Fraction] = []
    floating_distances: list[float] = []
    inside = outside = boundary = 0
    for index, value in enumerate(values):
        real = float(value.real)
        imag = float(value.imag)
        delta_real = _fraction(real) - center_real
        delta_imag = _fraction(imag) - center_imag
        margin = delta_real * delta_real + delta_imag * delta_imag - radius_square
        sign = (margin > 0) - (margin < 0)
        if sign < 0:
            inside += 1
            location = "inside"
        elif sign > 0:
            outside += 1
            location = "outside"
        else:
            boundary += 1
            location = "boundary"
        floating_distance = abs(value - point) - radius_value
        margins.append(margin)
        floating_distances.append(float(floating_distance))
        records.append(
            {
                "index": index,
                "diagonal_real": real,
                "diagonal_imag": imag,
                "diagonal_real_hex": real.hex(),
                "diagonal_imag_hex": imag.hex(),
                "exact_squared_margin_sign": sign,
                "classification": location,
                "floating_signed_boundary_distance": float(floating_distance),
            }
        )
    if not records:
        raise ValueError("at least one diagonal value is required")
    nearest = min(range(len(records)), key=lambda index: abs(floating_distances[index]))
    nearest_margin = margins[nearest]
    return CircleClassification(
        inside_count=inside,
        outside_count=outside,
        boundary_count=boundary,
        nearest_index=nearest,
        nearest_value=complex(values[nearest]),
        minimum_floating_boundary_distance=abs(floating_distances[nearest]),
        nearest_squared_margin_numerator=nearest_margin.numerator,
        nearest_squared_margin_denominator=nearest_margin.denominator,
        records=tuple(records),
    )
