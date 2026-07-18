"""One-center rank-one Grushin contour inequalities."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

from .bounds import _down, upper_add, upper_divide, upper_multiply


@dataclass(frozen=True)
class ContourGrushinLedger:
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


def grushin_contour_ledger(
    *,
    radius: float,
    center_reduced_inverse_upper: float,
    right_mode_infinity_upper: float,
    left_mode_one_upper: float,
    right_residual_infinity_upper: float,
    left_residual_one_upper: float,
    gram_lower: float,
    gram_upper: float,
    border_scale: float,
) -> ContourGrushinLedger:
    r"""Close a simple-root circle from one reduced inverse certificate.

    With ``R_- = s r`` and ``R_+ = l^T/s``, let ``E_0`` be the leading block
    of the bordered inverse at the approximate eigenvalue.  The exact
    Woodbury identity gives

    ``E(z)=E_0(I+(z-z_0)E_0)^-1``.

    Right and left eigen-residual identities keep the channel blocks close to
    ``s r/g`` and ``l^T/(s g)``.  The effective scalar is consequently close
    to ``-(z-z_0)/g`` on the whole circle.
    """

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
        raise ValueError("invalid Grushin contour inputs")
    transport_product = upper_multiply(contour_radius, e0)
    disk_invertible = bool(transport_product < 1.0)
    if not disk_invertible:
        infinity = math.inf
        return ContourGrushinLedger(
            radius=contour_radius,
            center_reduced_inverse_upper=e0,
            center_transport_product_upper=transport_product,
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
    denominator = _down(1.0 - transport_product)
    contour_e = upper_divide(e0, denominator)
    right_base = upper_divide(
        upper_multiply(scale, right_mode_infinity_upper), g_lower
    )
    right_correction = upper_divide(
        upper_multiply(
            contour_e, scale, right_residual_infinity_upper
        ),
        g_lower,
    )
    right_channel = upper_add(right_base, right_correction)
    left_base = upper_divide(
        left_mode_one_upper, upper_multiply(scale, g_lower)
    )
    left_correction = upper_divide(
        upper_multiply(left_residual_one_upper, contour_e),
        upper_multiply(scale, g_lower),
    )
    left_channel = upper_add(left_base, left_correction)
    affine_lower = _down(contour_radius / g_upper)
    scalar_error = upper_divide(
        upper_multiply(
            left_channel, scale, right_residual_infinity_upper
        ),
        g_lower,
    )
    scalar_lower = _down(affine_lower - scalar_error)
    count_one = bool(scalar_lower > 0.0 and scalar_error < affine_lower)
    resolvent = (
        upper_add(
            contour_e,
            upper_divide(
                upper_multiply(right_channel, left_channel), scalar_lower
            ),
        )
        if count_one
        else math.inf
    )
    return ContourGrushinLedger(
        radius=contour_radius,
        center_reduced_inverse_upper=e0,
        center_transport_product_upper=transport_product,
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
