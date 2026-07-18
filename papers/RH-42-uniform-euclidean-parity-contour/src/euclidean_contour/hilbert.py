"""Hilbert-space Galerkin, normalization, and cutoff transfers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

from .grushin import (
    _down,
    _up,
    upper_add,
    upper_divide,
    upper_multiply,
)


@dataclass(frozen=True)
class HilbertEnvelope:
    kernel: float
    source_first: float
    target_first: float
    source_second: float
    source_target: float
    target_second: float
    source_second_target_second: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


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
    product = upper_multiply(base, defect)
    admissible = bool(math.isfinite(product) and product < 1.0)
    transferred = (
        upper_divide(base, _down(1.0 - product))
        if admissible
        else math.inf
    )
    return NeumannTransfer(
        base_resolvent_upper=base,
        perturbation_upper=defect,
        neumann_product_upper=product,
        transferred_resolvent_upper=transferred,
        admissible=admissible,
    )


def midpoint_galerkin_defect(
    dimension: int, envelope: HilbertEnvelope
) -> float:
    r"""Bound midpoint versus cell-average Galerkin in Euclidean norm.

    The one-dimensional midpoint-average Peano kernel has L2 norm
    h^(3/2)/sqrt(320). Tensor decomposition gives

    C h^2 (||k_xx||_2+||k_yy||_2)
      + C^2 h^4 ||k_xxyy||_2.
    """

    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    h = 1.0 / n
    constant = _up(1.0 / math.sqrt(320.0))
    second = upper_multiply(
        constant,
        h * h,
        upper_add(envelope.source_second, envelope.target_second),
    )
    fourth = upper_multiply(
        1.0 / 320.0,
        h**4,
        envelope.source_second_target_second,
    )
    return upper_add(second, fourth)


def continuum_galerkin_defect(
    dimension: int, envelope: HilbertEnvelope
) -> float:
    """Bound ||K-P_n K P_n|| on L2 by Poincare--Wirtinger."""

    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    h = 1.0 / n
    return upper_multiply(
        h / math.pi,
        upper_add(envelope.source_first, envelope.target_first),
    )


@dataclass(frozen=True)
class HilbertHaarBounds:
    coarse_dimension: int
    coarse_consistency: float
    coarse_to_detail: float
    detail_to_coarse: float
    detail_block: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def hilbert_haar_bounds(
    coarse_dimension: int, envelope: HilbertEnvelope
) -> HilbertHaarBounds:
    n = int(coarse_dimension)
    if n < 2:
        raise ValueError("coarse dimension must be at least two")
    h = 1.0 / n
    return HilbertHaarBounds(
        coarse_dimension=n,
        coarse_consistency=0.0,
        coarse_to_detail=upper_multiply(
            h / math.pi, envelope.source_first
        ),
        detail_to_coarse=upper_multiply(
            h / math.pi, envelope.target_first
        ),
        detail_block=upper_multiply(
            h * h / (math.pi * math.pi),
            envelope.source_target,
        ),
    )


@dataclass(frozen=True)
class HilbertSchurStep:
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


def hilbert_schur_step(
    coarse_resolvent_upper: float,
    minimum_boundary_modulus: float,
    blocks: HilbertHaarBounds,
) -> HilbertSchurStep:
    coarse = float(coarse_resolvent_upper)
    modulus = float(minimum_boundary_modulus)
    if blocks.detail_block >= modulus:
        detail = math.inf
    else:
        detail = upper_divide(
            1.0, _down(modulus - blocks.detail_block)
        )
    self_energy = upper_multiply(
        blocks.detail_to_coarse,
        detail,
        blocks.coarse_to_detail,
    )
    product = upper_multiply(coarse, self_energy)
    admissible = bool(math.isfinite(product) and product < 1.0)
    if not admissible:
        infinity = math.inf
        return HilbertSchurStep(
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
    frobenius_square = upper_add(
        upper_multiply(schur, schur),
        upper_multiply(top_right, top_right),
        upper_multiply(bottom_left, bottom_left),
        upper_multiply(bottom_right, bottom_right),
    )
    fine = _up(math.sqrt(frobenius_square))
    return HilbertSchurStep(
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


@dataclass(frozen=True)
class NormalizationDefect:
    dimension: int
    normalizer_lower: float
    normalizer_midpoint_error_upper: float
    relative_row_scaling_upper: float
    continuum_midpoint_norm_upper: float
    spectral_norm_defect_upper: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def discrete_normalization_defect(
    dimension: int,
    sigma: float,
    normalizer_lower: float,
    kernel_hilbert_schmidt_upper: float,
    midpoint_defect_upper: float,
) -> NormalizationDefect:
    n = int(dimension)
    h = 1.0 / n
    width = float(sigma)
    z_lower = float(normalizer_lower)
    normalizer_error = upper_multiply(
        math.exp(-0.5) / width, h * h
    )
    denominator = _down(z_lower - normalizer_error)
    scaling = upper_divide(normalizer_error, denominator)
    midpoint_norm = upper_add(
        kernel_hilbert_schmidt_upper, midpoint_defect_upper
    )
    defect = upper_multiply(scaling, midpoint_norm)
    return NormalizationDefect(
        dimension=n,
        normalizer_lower=z_lower,
        normalizer_midpoint_error_upper=normalizer_error,
        relative_row_scaling_upper=scaling,
        continuum_midpoint_norm_upper=midpoint_norm,
        spectral_norm_defect_upper=defect,
    )


@dataclass(frozen=True)
class CutoffDefect:
    dimension: int
    declared_multiple: float
    omitted_mass_upper: float
    infinity_norm_upper: float
    omitted_frobenius_square_upper: float
    renormalization_frobenius_square_upper: float
    spectral_norm_upper: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def relaxed_cutoff_defect(
    dimension: int, sigma: float, declared_multiple: float
) -> CutoffDefect:
    """Evaluate RH-39 using the rigorous relaxation Lambda_h >= L."""

    n = int(dimension)
    h = 1.0 / n
    width = float(sigma)
    multiple = float(declared_multiple)
    if not (0.0 < h < width and multiple > 0.0):
        raise ValueError("invalid cutoff inputs")
    exp_half = _up(math.exp(-0.5 * multiple * multiple))
    omitted = upper_divide(
        upper_multiply(
            2.0,
            math.sqrt(math.e),
            exp_half,
            upper_add(h, width / multiple),
        ),
        _down(width - h),
    )
    alpha = upper_divide(omitted, _down(1.0 - omitted))
    omitted_square = upper_divide(
        upper_multiply(
            4.0,
            math.e,
            exp_half,
            exp_half,
            upper_add(h, width / (2.0 * multiple)),
        ),
        upper_multiply(_down(width - h), _down(width - h)),
    )
    renormalization_square = upper_divide(
        upper_multiply(
            math.e,
            alpha,
            alpha,
            upper_add(
                4.0 * h, 2.0 * math.sqrt(math.pi) * width
            ),
        ),
        upper_multiply(_down(width - h), _down(width - h)),
    )
    total_square = upper_add(
        omitted_square, renormalization_square
    )
    return CutoffDefect(
        dimension=n,
        declared_multiple=multiple,
        omitted_mass_upper=omitted,
        infinity_norm_upper=upper_multiply(2.0, omitted),
        omitted_frobenius_square_upper=omitted_square,
        renormalization_frobenius_square_upper=(
            renormalization_square
        ),
        spectral_norm_upper=_up(math.sqrt(total_square)),
    )


def adaptive_multiple(dimension: int, minimum: float = 8.0) -> float:
    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    return max(float(minimum), 2.0 * math.sqrt(math.log(n)))


def weighted_riesz_perturbation_upper(
    *,
    contour_radius: float,
    contour_maximum_modulus: float,
    first_resolvent_upper: float,
    second_resolvent_upper: float,
    perturbation_upper: float,
) -> float:
    return upper_multiply(
        contour_radius,
        contour_maximum_modulus,
        first_resolvent_upper,
        second_resolvent_upper,
        perturbation_upper,
    )
