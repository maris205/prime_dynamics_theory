"""Analytic folded-Gaussian, Galerkin, and Schur resolvent bounds."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

import numpy as np


def _up(value: float) -> float:
    number = float(value)
    if number < 0.0 or math.isnan(number):
        raise ValueError("an outward upper bound must be nonnegative")
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
        number = float(value)
        if number < 0.0:
            raise ValueError("upper products require nonnegative factors")
        total = _up(total * number)
    return total


def upper_divide(numerator: float, denominator: float) -> float:
    bottom = _down(float(denominator))
    if bottom <= 0.0:
        return math.inf
    return _up(float(numerator) / bottom)


@dataclass(frozen=True)
class DerivativeEnvelope:
    """Uniform row-L1 derivative bounds for the normalized folded kernel."""

    u_upper: float
    sigma: float
    parameter_first: float
    target_first: float
    parameter_second: float
    parameter_target: float
    target_second: float
    source_first: float
    source_second: float
    source_target: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def derivative_envelope(u_upper: float, sigma: float) -> DerivativeEnvelope:
    r"""Return moment-based folded-Gaussian derivative bounds.

    For a Gaussian conditioned to ``[-1,1]`` with its unconditioned mean in
    that interval, standardization gives a normal variable conditioned to
    ``[a,b]`` with ``a<=0<=b``.  Integration by parts yields

    ``E(T-m)^2 <= sigma^2`` and hence ``Var(T) <= sigma^2``.

    Folding cannot increase the L1 norm of a parameter derivative.  Hence

    ``||q_m||_1, ||q_y||_1 <= 1/sigma``,
    ``||q_mm||_1 <= 2/sigma^2``, and
    ``||q_my||_1, ||q_yy||_1 <= 2/sigma^2``.
    """

    u = float(u_upper)
    width = float(sigma)
    if not (1.0 < u < 2.0) or not (0.0 < width <= 1.0):
        raise ValueError("the folded-Gaussian envelope requires 1<u<2 and 0<sigma<=1")
    parameter_first = _up(1.0 / width)
    target_first = _up(1.0 / width)
    parameter_second = _up(2.0 / (width * width))
    parameter_target = _up(2.0 / (width * width))
    target_second = _up(2.0 / (width * width))
    source_first = upper_multiply(2.0, u, parameter_first)
    source_second = upper_add(
        upper_multiply(4.0, u, u, parameter_second),
        upper_multiply(2.0, u, parameter_first),
    )
    source_target = upper_multiply(2.0, u, parameter_target)
    return DerivativeEnvelope(
        u_upper=u,
        sigma=width,
        parameter_first=parameter_first,
        target_first=target_first,
        parameter_second=parameter_second,
        parameter_target=parameter_target,
        target_second=target_second,
        source_first=source_first,
        source_second=source_second,
        source_target=source_target,
    )


def midpoint_galerkin_defect(
    dimension: int, envelope: DerivativeEnvelope
) -> float:
    r"""Bound midpoint-matrix versus cell-average Galerkin row norm.

    The one-cell midpoint remainder in integrated absolute second derivative
    form gives

    ``||M_n-A_n||_inf <= h^2 (L_xx+L_yy)/8``.
    """

    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    h = 1.0 / n
    return upper_multiply(
        h * h / 8.0,
        upper_add(envelope.source_second, envelope.target_second),
    )


def continuum_galerkin_defect(
    dimension: int, envelope: DerivativeEnvelope
) -> float:
    r"""Bound ``||K-P_n K P_n||`` on ``L^infinity``.

    Cell averaging costs at most ``h L_x/2`` on the output and
    ``h L_y/2`` on the input.
    """

    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    h = 1.0 / n
    return upper_multiply(
        h / 2.0,
        upper_add(envelope.source_first, envelope.target_first),
    )


@dataclass(frozen=True)
class GalerkinHaarBounds:
    coarse_dimension: int
    coarse_consistency: float
    coarse_to_detail: float
    detail_to_coarse: float
    detail_block: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def galerkin_haar_bounds(
    coarse_dimension: int, envelope: DerivativeEnvelope
) -> GalerkinHaarBounds:
    r"""Return exact-consistency dyadic Galerkin Haar bounds.

    Nested conditional expectations make the coarse-consistency block zero.
    Half-cell cancellation gives

    ``C <= h L_x/4``, ``B <= h L_y/2``, and
    ``D <= h^2 L_xy/8`` in the induced infinity norm.
    """

    n = int(coarse_dimension)
    if n < 2:
        raise ValueError("coarse dimension must be at least two")
    h = 1.0 / n
    return GalerkinHaarBounds(
        coarse_dimension=n,
        coarse_consistency=0.0,
        coarse_to_detail=upper_multiply(h / 4.0, envelope.source_first),
        detail_to_coarse=upper_multiply(h / 2.0, envelope.target_first),
        detail_block=upper_multiply(h * h / 8.0, envelope.source_target),
    )


@dataclass(frozen=True)
class NeumannTransfer:
    base_resolvent_upper: float
    perturbation_upper: float
    neumann_product_upper: float
    transferred_resolvent_upper: float
    admissible: bool

    def as_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def neumann_transfer(
    base_resolvent_upper: float, perturbation_upper: float
) -> NeumannTransfer:
    base = float(base_resolvent_upper)
    defect = float(perturbation_upper)
    if base < 0.0 or defect < 0.0:
        raise ValueError("Neumann inputs must be nonnegative")
    product = upper_multiply(base, defect)
    admissible = bool(math.isfinite(product) and product < 1.0)
    transferred = (
        upper_divide(base, _down(1.0 - product)) if admissible else math.inf
    )
    return NeumannTransfer(
        base_resolvent_upper=base,
        perturbation_upper=defect,
        neumann_product_upper=product,
        transferred_resolvent_upper=transferred,
        admissible=admissible,
    )


@dataclass(frozen=True)
class SchurStep:
    coarse_dimension: int
    coarse_resolvent_upper: float
    minimum_boundary_modulus: float
    detail_resolvent_upper: float
    self_energy_upper: float
    schur_neumann_product_upper: float
    schur_inverse_upper: float
    top_right_upper: float
    bottom_left_upper: float
    bottom_right_upper: float
    fine_resolvent_upper: float
    count_transfers: bool

    def as_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def schur_resolvent_step(
    coarse_resolvent_upper: float,
    minimum_boundary_modulus: float,
    blocks: GalerkinHaarBounds,
) -> SchurStep:
    r"""Propagate a contour resolvent through one exact dyadic split.

    In Haar coordinates the Galerkin fine matrix is

    ``[[A_n, B], [C, D]]``.

    The returned original-coordinate infinity bound uses the explicit sum of
    the four inverse-block bounds rather than the crude condition number of
    the Haar transform.
    """

    coarse = float(coarse_resolvent_upper)
    modulus = float(minimum_boundary_modulus)
    if coarse <= 0.0 or modulus <= 0.0:
        raise ValueError("resolvent and boundary modulus must be positive")
    if blocks.detail_block >= modulus:
        detail = math.inf
    else:
        detail = upper_divide(1.0, _down(modulus - blocks.detail_block))
    self_energy = upper_add(
        blocks.coarse_consistency,
        upper_multiply(
            blocks.detail_to_coarse,
            detail,
            blocks.coarse_to_detail,
        ),
    )
    product = upper_multiply(coarse, self_energy)
    admissible = bool(math.isfinite(product) and product < 1.0)
    if not admissible:
        infinity = math.inf
        return SchurStep(
            coarse_dimension=blocks.coarse_dimension,
            coarse_resolvent_upper=coarse,
            minimum_boundary_modulus=modulus,
            detail_resolvent_upper=detail,
            self_energy_upper=self_energy,
            schur_neumann_product_upper=product,
            schur_inverse_upper=infinity,
            top_right_upper=infinity,
            bottom_left_upper=infinity,
            bottom_right_upper=infinity,
            fine_resolvent_upper=infinity,
            count_transfers=False,
        )
    schur = upper_divide(coarse, _down(1.0 - product))
    top_right = upper_multiply(
        schur, blocks.detail_to_coarse, detail
    )
    bottom_left = upper_multiply(
        detail, blocks.coarse_to_detail, schur
    )
    bottom_right = upper_add(
        detail,
        upper_multiply(
            detail,
            blocks.coarse_to_detail,
            schur,
            blocks.detail_to_coarse,
            detail,
        ),
    )
    fine = upper_add(schur, top_right, bottom_left, bottom_right)
    return SchurStep(
        coarse_dimension=blocks.coarse_dimension,
        coarse_resolvent_upper=coarse,
        minimum_boundary_modulus=modulus,
        detail_resolvent_upper=detail,
        self_energy_upper=self_energy,
        schur_neumann_product_upper=product,
        schur_inverse_upper=schur,
        top_right_upper=top_right,
        bottom_left_upper=bottom_left,
        bottom_right_upper=bottom_right,
        fine_resolvent_upper=fine,
        count_transfers=True,
    )
