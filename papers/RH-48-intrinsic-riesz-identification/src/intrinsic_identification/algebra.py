"""Scalar ledgers for the one-sided Schur identification theorem."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


def _finite_nonnegative(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def self_energy_upper(
    detail_resolvent: float,
    coarse_to_detail: float,
    detail_to_coarse: float,
) -> float:
    r"""Return ``||B (z-D)^(-1) C||`` from three nonnegative uppers."""

    rd = _finite_nonnegative("detail_resolvent", detail_resolvent)
    c = _finite_nonnegative("coarse_to_detail", coarse_to_detail)
    b = _finite_nonnegative("detail_to_coarse", detail_to_coarse)
    return b * rd * c


def detail_resolvent_upper(
    contour_minimum_modulus: float, detail_operator_norm: float
) -> float:
    r"""Bound ``(z-D)^(-1)`` by a Neumann distance from the origin."""

    rho = _finite_nonnegative(
        "contour_minimum_modulus", contour_minimum_modulus
    )
    d = _finite_nonnegative("detail_operator_norm", detail_operator_norm)
    if d >= rho:
        raise ValueError("detail block reaches the contour minimum modulus")
    return 1.0 / (rho - d)


@dataclass(frozen=True)
class DirectionalSchurBound:
    """One Hilbert--Schmidt bound for a weighted top-left Riesz defect."""

    contour_length_over_two_pi: float
    contour_maximum_modulus: float
    detail_resolvent_upper: float
    left_directional_hilbert_schmidt_upper: float
    right_directional_operator_upper: float
    identification_hilbert_schmidt_upper: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def directional_schur_bound(
    *,
    contour_length_over_two_pi: float,
    contour_maximum_modulus: float,
    detail_resolvent: float,
    left_directional_hilbert_schmidt: float,
    right_directional_operator: float,
) -> DirectionalSchurBound:
    r"""Bound the exact integral ``int z S B R_D C R_A dz/(2 pi i)``.

    The two directional arguments are the already-composed quantities
    ``sup ||S(z)B||_S2`` and ``sup ||C R_A(z)||``.  No global norm of either
    coarse resolvent is used.
    """

    length = _finite_nonnegative(
        "contour_length_over_two_pi", contour_length_over_two_pi
    )
    modulus = _finite_nonnegative(
        "contour_maximum_modulus", contour_maximum_modulus
    )
    rd = _finite_nonnegative("detail_resolvent", detail_resolvent)
    left = _finite_nonnegative(
        "left_directional_hilbert_schmidt",
        left_directional_hilbert_schmidt,
    )
    right = _finite_nonnegative(
        "right_directional_operator", right_directional_operator
    )
    upper = length * modulus * rd * left * right
    return DirectionalSchurBound(
        contour_length_over_two_pi=length,
        contour_maximum_modulus=modulus,
        detail_resolvent_upper=rd,
        left_directional_hilbert_schmidt_upper=left,
        right_directional_operator_upper=right,
        identification_hilbert_schmidt_upper=upper,
    )


def dyadic_tail_upper(first_level_upper: float, ratio: float = 0.25) -> float:
    """Sum a geometric dyadic defect tail with successive ratio below one."""

    first = _finite_nonnegative("first_level_upper", first_level_upper)
    q = _finite_nonnegative("ratio", ratio)
    if q >= 1.0:
        raise ValueError("dyadic ratio must be below one")
    return first / (1.0 - q)


@dataclass(frozen=True)
class PowerLawLedger:
    """Exponents for ``n=sigma^-p`` and gain ``L=sigma^-gamma``."""

    mesh_power: float
    directional_gain_power: float
    anchored_hilbert_schmidt_exponent: float
    anchored_trace_norm_exponent: float
    intrinsic_identification_exponent: float
    identification_over_anchored_hilbert_schmidt_exponent: float
    intrinsic_trace_contribution_exponent: float
    intrinsic_trace_over_anchored_trace_exponent: float
    identification_is_lower_order: bool
    trace_contribution_is_lower_order: bool

    def as_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def power_law_ledger(
    mesh_power: float, directional_gain_power: float
) -> PowerLawLedger:
    r"""Return all small-noise powers used in the RH-48 closure theorem.

    The generic quadratic Schur estimate is

    ``I_n,sigma = O(n^-2 sigma^-3 L_sigma)``

    with ``L_sigma = O(sigma^-gamma)``.  Positive exponents below mean
    decay as ``sigma`` tends to zero.
    """

    p = _finite_nonnegative("mesh_power", mesh_power)
    gamma = _finite_nonnegative(
        "directional_gain_power", directional_gain_power
    )
    anchored_hs = p - 1.5
    anchored_trace = p - 2.0
    identification = 2.0 * p - 3.0 - gamma
    relative = p - 1.5 - gamma
    intrinsic_trace = 2.0 * p - 3.5 - gamma
    return PowerLawLedger(
        mesh_power=p,
        directional_gain_power=gamma,
        anchored_hilbert_schmidt_exponent=anchored_hs,
        anchored_trace_norm_exponent=anchored_trace,
        intrinsic_identification_exponent=identification,
        identification_over_anchored_hilbert_schmidt_exponent=relative,
        intrinsic_trace_contribution_exponent=intrinsic_trace,
        intrinsic_trace_over_anchored_trace_exponent=relative,
        identification_is_lower_order=relative > 0.0,
        trace_contribution_is_lower_order=relative > 0.0,
    )
