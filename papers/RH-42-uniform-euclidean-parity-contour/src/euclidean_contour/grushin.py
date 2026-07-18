"""Rank-one Grushin contour inequalities in Hilbert norm."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


def _up(value: float) -> float:
    number = float(value)
    if number < 0.0 or math.isnan(number):
        raise ValueError("an outward upper must be nonnegative")
    return math.nextafter(number, math.inf)


def _down(value: float) -> float:
    number = float(value)
    if number <= 0.0:
        return 0.0
    return math.nextafter(number, 0.0)


def upper_add(*values: float) -> float:
    total = 0.0
    for value in values:
        total = _up(total + float(value))
    return total


def upper_multiply(*values: float) -> float:
    total = 1.0
    for value in values:
        if float(value) < 0.0:
            raise ValueError("upper products require nonnegative factors")
        total = _up(total * float(value))
    return total


def upper_divide(numerator: float, denominator: float) -> float:
    bottom = _down(denominator)
    if bottom <= 0.0:
        return math.inf
    return _up(float(numerator) / bottom)


@dataclass(frozen=True)
class EuclideanGrushinLedger:
    radius: float
    center_reduced_inverse_upper: float
    center_transport_product_upper: float
    contour_reduced_inverse_upper: float
    contour_right_channel_upper: float
    contour_left_channel_upper: float
    affine_scalar_boundary_lower: float
    scalar_error_upper: float
    effective_scalar_boundary_lower: float
    contour_resolvent_upper: float
    bordered_disk_invertible: bool
    rouche_count_one: bool

    def as_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def euclidean_grushin_ledger(
    *,
    radius: float,
    center_reduced_inverse_upper: float,
    right_mode_two_upper: float,
    left_mode_two_upper: float,
    right_residual_two_upper: float,
    left_residual_two_upper: float,
    gram_lower: float,
    gram_upper: float,
    border_scale: float,
) -> EuclideanGrushinLedger:
    """Close one eigenvalue circle using subordinate Euclidean norms."""

    contour_radius = float(radius)
    e0 = float(center_reduced_inverse_upper)
    scale = float(border_scale)
    g_lower = float(gram_lower)
    g_upper = float(gram_upper)
    if (
        contour_radius <= 0.0
        or e0 <= 0.0
        or scale <= 0.0
        or g_lower <= 0.0
        or g_upper < g_lower
    ):
        raise ValueError("invalid Euclidean Grushin inputs")
    transport = upper_multiply(contour_radius, e0)
    invertible = bool(transport < 1.0)
    if not invertible:
        infinity = math.inf
        return EuclideanGrushinLedger(
            radius=contour_radius,
            center_reduced_inverse_upper=e0,
            center_transport_product_upper=transport,
            contour_reduced_inverse_upper=infinity,
            contour_right_channel_upper=infinity,
            contour_left_channel_upper=infinity,
            affine_scalar_boundary_lower=0.0,
            scalar_error_upper=infinity,
            effective_scalar_boundary_lower=0.0,
            contour_resolvent_upper=infinity,
            bordered_disk_invertible=False,
            rouche_count_one=False,
        )
    contour_e = upper_divide(e0, _down(1.0 - transport))
    right_channel = upper_add(
        upper_divide(
            upper_multiply(scale, right_mode_two_upper), g_lower
        ),
        upper_divide(
            upper_multiply(
                contour_e, scale, right_residual_two_upper
            ),
            g_lower,
        ),
    )
    left_channel = upper_add(
        upper_divide(
            left_mode_two_upper, upper_multiply(scale, g_lower)
        ),
        upper_divide(
            upper_multiply(left_residual_two_upper, contour_e),
            upper_multiply(scale, g_lower),
        ),
    )
    affine_lower = _down(contour_radius / g_upper)
    scalar_error = upper_divide(
        upper_multiply(
            left_channel, scale, right_residual_two_upper
        ),
        g_lower,
    )
    scalar_lower = _down(affine_lower - scalar_error)
    count_one = bool(
        scalar_lower > 0.0 and scalar_error < affine_lower
    )
    resolvent = (
        upper_add(
            contour_e,
            upper_divide(
                upper_multiply(right_channel, left_channel),
                scalar_lower,
            ),
        )
        if count_one
        else math.inf
    )
    return EuclideanGrushinLedger(
        radius=contour_radius,
        center_reduced_inverse_upper=e0,
        center_transport_product_upper=transport,
        contour_reduced_inverse_upper=contour_e,
        contour_right_channel_upper=right_channel,
        contour_left_channel_upper=left_channel,
        affine_scalar_boundary_lower=affine_lower,
        scalar_error_upper=scalar_error,
        effective_scalar_boundary_lower=scalar_lower,
        contour_resolvent_upper=resolvent,
        bordered_disk_invertible=True,
        rouche_count_one=count_one,
    )
