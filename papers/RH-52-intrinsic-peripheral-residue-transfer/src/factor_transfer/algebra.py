"""Exact finite-factor norm identities used by RH-52."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _vector(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128).reshape(-1)
    if result.size < 1 or np.any(~np.isfinite(result)):
        raise ValueError(f"{name} must be a nonempty finite vector")
    return result


def _positive(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


@dataclass(frozen=True)
class FactorNorms:
    """Physical norms of a cell-mass or cell-value eigenfactor."""

    l1_or_linf: float
    l2: float


def left_mass_norms(left_mass: np.ndarray) -> FactorNorms:
    """Return physical L1/L2 norms from equal-cell left masses."""

    mass = _vector(left_mass, "left_mass")
    return FactorNorms(
        l1_or_linf=float(np.sum(np.abs(mass))),
        l2=float(math.sqrt(mass.size) * np.linalg.norm(mass)),
    )


def right_value_norms(right_values: np.ndarray) -> FactorNorms:
    """Return physical Linfinity/L2 norms from equal-cell values."""

    values = _vector(right_values, "right_values")
    return FactorNorms(
        l1_or_linf=float(np.max(np.abs(values))),
        l2=float(np.linalg.norm(values) / math.sqrt(values.size)),
    )


def normalize_l1(values: np.ndarray) -> np.ndarray:
    """Normalize a vector by its discrete total variation."""

    vector = _vector(values, "values")
    norm = float(np.sum(np.abs(vector)))
    if norm == 0.0:
        raise ValueError("cannot normalize a zero vector")
    return vector / norm


def normalize_linf(values: np.ndarray) -> np.ndarray:
    """Normalize a vector by its maximum modulus."""

    vector = _vector(values, "values")
    norm = float(np.max(np.abs(vector)))
    if norm == 0.0:
        raise ValueError("cannot normalize a zero vector")
    return vector / norm


def aggregate_left_masses(fine_mass: np.ndarray) -> np.ndarray:
    """Push adjacent fine cell masses to the coarse partition."""

    mass = _vector(fine_mass, "fine_mass")
    if mass.size % 2:
        raise ValueError("fine_mass must have even length")
    return mass[0::2] + mass[1::2]


def average_right_values(fine_values: np.ndarray) -> np.ndarray:
    """Orthogonally compress fine cell values to coarse cell values."""

    values = _vector(fine_values, "fine_values")
    if values.size % 2:
        raise ValueError("fine_values must have even length")
    return 0.5 * (values[0::2] + values[1::2])


def left_haar_detail_l2(left_mass: np.ndarray) -> float:
    """Return the physical L2 norm of the adjacent Haar detail."""

    mass = _vector(left_mass, "left_mass")
    if mass.size % 2:
        raise ValueError("left_mass must have even length")
    detail_mass = (mass[0::2] - mass[1::2]) / math.sqrt(2.0)
    return float(math.sqrt(mass.size) * np.linalg.norm(detail_mass))


def rank_one_frobenius(right: np.ndarray, left: np.ndarray) -> float:
    """Return the Frobenius norm of a rank-one outer product."""

    r = _vector(right, "right")
    ell = _vector(left, "left")
    return float(np.linalg.norm(r) * np.linalg.norm(ell))


def rank_one_difference_frobenius(
    right_a: np.ndarray,
    left_a: np.ndarray,
    right_b: np.ndarray,
    left_b: np.ndarray,
) -> float:
    """Return the Frobenius norm of a rank-one difference."""

    ra = _vector(right_a, "right_a")
    la = _vector(left_a, "left_a")
    rb = _vector(right_b, "right_b")
    lb = _vector(left_b, "left_b")
    if ra.size != rb.size or la.size != lb.size:
        raise ValueError("rank-one factors have incompatible shapes")
    square = (
        np.vdot(ra, ra).real * np.vdot(la, la).real
        + np.vdot(rb, rb).real * np.vdot(lb, lb).real
        - 2.0
        * np.real(np.vdot(ra, rb) * np.vdot(lb, la))
    )
    return float(math.sqrt(max(float(square), 0.0)))


def weak_to_l2_factor_upper(
    *,
    kernel_l1_to_l2: float,
    weak_factor_error: float,
    eigenvalue_modulus_lower: float,
    eigenvalue_error: float = 0.0,
    continuum_factor_l2: float = 0.0,
) -> float:
    """Lift weak factor error to L2 using the exact eigenrelations."""

    smoothing = _positive(kernel_l1_to_l2, "kernel_l1_to_l2")
    weak = max(float(weak_factor_error), 0.0)
    lower = _positive(eigenvalue_modulus_lower, "eigenvalue_modulus_lower")
    eigen_error = max(float(eigenvalue_error), 0.0)
    continuum = max(float(continuum_factor_l2), 0.0)
    return float(
        smoothing * weak / lower
        + eigen_error * continuum / (lower * lower)
    )


@dataclass(frozen=True)
class WeakResidueBudget:
    """Scale ledger for direct left and right peripheral residue bounds."""

    fine_left_detail_upper: float
    fine_residue_ratio_upper: float
    right_image_upper: float
    right_left_l2_upper: float
    right_residue_ratio_upper: float


def weak_residue_budget(
    *,
    cell_width: float,
    sigma: float,
    eigenvalue_modulus_lower: float,
    right_l2_upper: float,
    right_linf_upper: float,
    left_l1_upper: float,
    target_detail_constant: float,
    source_detail_constant: float,
    kernel_l1_to_l2_constant: float,
    detail_block_plus_eigenvalue_upper: float,
    outgoing_hs_lower_constant: float,
    incoming_hs_lower_constant: float,
) -> WeakResidueBudget:
    """Compose direct weak-factor residue estimates."""

    h = _positive(cell_width, "cell_width")
    width = _positive(sigma, "sigma")
    lower = _positive(eigenvalue_modulus_lower, "eigenvalue_modulus_lower")
    r2 = _positive(right_l2_upper, "right_l2_upper")
    rinf = _positive(right_linf_upper, "right_linf_upper")
    ell1 = _positive(left_l1_upper, "left_l1_upper")
    cy = _positive(target_detail_constant, "target_detail_constant")
    cx = _positive(source_detail_constant, "source_detail_constant")
    c0 = _positive(kernel_l1_to_l2_constant, "kernel_l1_to_l2_constant")
    block = _positive(
        detail_block_plus_eigenvalue_upper,
        "detail_block_plus_eigenvalue_upper",
    )
    b_lower = _positive(
        outgoing_hs_lower_constant, "outgoing_hs_lower_constant"
    )
    c_lower = _positive(
        incoming_hs_lower_constant, "incoming_hs_lower_constant"
    )
    detail = cy * h * width ** -1.5 * ell1 / lower
    fine_ratio = r2 * block * detail / (
        b_lower * h * width ** -1.5
    )
    right_image = cx * h * width ** -1.0 * rinf
    left_l2 = c0 * width ** -0.5 * ell1 / lower
    right_ratio = right_image * left_l2 / (
        c_lower * h * width ** -1.5
    )
    return WeakResidueBudget(
        fine_left_detail_upper=float(detail),
        fine_residue_ratio_upper=float(fine_ratio),
        right_image_upper=float(right_image),
        right_left_l2_upper=float(left_l2),
        right_residue_ratio_upper=float(right_ratio),
    )
