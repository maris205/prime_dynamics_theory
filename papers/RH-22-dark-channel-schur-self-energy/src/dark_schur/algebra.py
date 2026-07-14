"""Exact scalar Schur algebra for a two-channel return matrix."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SchurAudit:
    """Diagnostics comparing one 2x2 return with a prescribed target root."""

    target: complex
    direct_bright: complex
    dark_pole: complex
    bright_to_dark: complex
    dark_to_bright: complex
    observed_product: complex
    required_product: complex
    signed_coupling_ratio: complex
    self_energy_at_target: complex
    required_shift: complex
    schur_residual: complex
    determinant_residual: complex
    bright_root: complex
    bright_root_shift: complex
    small_coupling_parameter: float
    small_coupling_bound: float
    target_pole_distance: float
    target_pole_distance_ratio: float


@dataclass(frozen=True)
class NestedSchurData:
    """Effective 2x2 entries after eliminating an external complement."""

    direct_bright: complex
    bright_to_dark: complex
    dark_to_bright: complex
    dark_pole: complex
    external_determinant: complex
    reduced_determinant: complex
    full_determinant: complex
    scalar_schur_function: complex


def _matrix_2x2(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix)
    if values.shape != (2, 2):
        raise ValueError("the return matrix must be 2x2")
    dtype = np.complex128 if np.iscomplexobj(values) else np.float64
    return np.asarray(values, dtype=dtype)


def bright_dark_transform(matrix: np.ndarray) -> np.ndarray:
    r"""Return ``U* M U`` for bright/dark Hadamard coordinates."""

    values = _matrix_2x2(matrix)
    transform = np.asarray(((1.0, 1.0), (1.0, -1.0))) / np.sqrt(2.0)
    return np.real_if_close(transform.conj().T @ values @ transform)


def characteristic(matrix: np.ndarray, spectral_parameter: complex) -> complex:
    r"""Return ``det(z I-M)`` evaluated without an eigensolver."""

    values = _matrix_2x2(matrix)
    zeta = complex(spectral_parameter)
    a, b = values[0]
    c, d = values[1]
    return complex((zeta - a) * (zeta - d) - b * c)


def self_energy(matrix: np.ndarray, spectral_parameter: complex) -> complex:
    r"""Return the local dark-channel self-energy ``bc/(z-d)``."""

    values = _matrix_2x2(matrix)
    zeta = complex(spectral_parameter)
    a, b = values[0]
    c, d = values[1]
    del a
    if zeta == d:
        raise ZeroDivisionError("the Schur self-energy is singular at the dark pole")
    return complex(b * c / (zeta - d))


def schur_function(matrix: np.ndarray, spectral_parameter: complex) -> complex:
    r"""Return ``F_b(z)=z-a-bc/(z-d)`` away from the dark pole."""

    values = _matrix_2x2(matrix)
    zeta = complex(spectral_parameter)
    return complex(zeta - values[0, 0] - self_energy(values, zeta))


def required_coupling(
    direct_bright: complex,
    dark_pole: complex,
    target: complex,
) -> complex:
    r"""Return the unique product ``bc`` making ``target`` an eigenvalue."""

    return complex((target - direct_bright) * (target - dark_pole))


def diagonal_gauge_transform(
    matrix: np.ndarray,
    bright_scale: complex,
    dark_scale: complex,
) -> np.ndarray:
    r"""Return ``D^{-1} M D`` for a nonzero diagonal channel gauge."""

    values = _matrix_2x2(matrix)
    if bright_scale == 0 or dark_scale == 0:
        raise ValueError("diagonal gauge scales must be nonzero")
    gauge = np.diag((complex(bright_scale), complex(dark_scale)))
    return np.linalg.solve(gauge, values @ gauge)


def nested_schur_data(
    matrix: np.ndarray,
    spectral_parameter: complex,
) -> NestedSchurData:
    r"""Eliminate all channels after the leading bright/dark pair.

    For the block ordering ``bright + dark + external``, this returns the
    spectral-parameter-dependent entries of the exact effective 2x2 matrix.
    The external block must be nonempty and ``z I-E`` must be invertible.
    """

    values = np.asarray(matrix)
    if values.ndim != 2 or values.shape[0] != values.shape[1] or values.shape[0] < 3:
        raise ValueError("nested Schur reduction requires a square matrix of size at least three")
    values = np.asarray(values, dtype=np.complex128)
    zeta = complex(spectral_parameter)
    external = values[2:, 2:]
    resolvent_matrix = zeta * np.eye(external.shape[0]) - external
    external_determinant = np.linalg.det(resolvent_matrix)
    if abs(external_determinant) == 0.0:
        raise np.linalg.LinAlgError("the external resolvent is singular")

    bright_external = values[0, 2:]
    dark_external = values[1, 2:]
    external_bright = values[2:, 0]
    external_dark = values[2:, 1]
    solved_bright = np.linalg.solve(resolvent_matrix, external_bright)
    solved_dark = np.linalg.solve(resolvent_matrix, external_dark)
    a_eff = values[0, 0] + bright_external @ solved_bright
    b_eff = values[0, 1] + bright_external @ solved_dark
    c_eff = values[1, 0] + dark_external @ solved_bright
    d_eff = values[1, 1] + dark_external @ solved_dark
    reduced = np.asarray(((a_eff, b_eff), (c_eff, d_eff)))
    reduced_determinant = characteristic(reduced, zeta)
    full_determinant = np.linalg.det(zeta * np.eye(values.shape[0]) - values)
    scalar = schur_function(reduced, zeta)
    return NestedSchurData(
        direct_bright=complex(a_eff),
        bright_to_dark=complex(b_eff),
        dark_to_bright=complex(c_eff),
        dark_pole=complex(d_eff),
        external_determinant=complex(external_determinant),
        reduced_determinant=complex(reduced_determinant),
        full_determinant=complex(full_determinant),
        scalar_schur_function=complex(scalar),
    )


def bright_root(matrix: np.ndarray) -> complex:
    """Return the eigenvalue continuously attached to ``a`` at ``bc=0``.

    The root closest to the direct bright entry is selected.  This convention
    is unambiguous in the small-coupling regime used by the audit.
    """

    values = _matrix_2x2(matrix)
    roots = np.linalg.eigvals(values)
    distances = np.abs(roots - values[0, 0])
    return complex(roots[int(np.argmin(distances))])


def small_coupling_root_bound(matrix: np.ndarray) -> float:
    r"""Return the Rouch\'e bound ``2|bc|/|a-d|`` when applicable.

    If ``|bc|/|a-d|^2 < 1/4``, exactly one eigenvalue lies in the disk
    ``|z-a| < 2|bc|/|a-d|``.  Otherwise this function returns infinity.
    """

    values = _matrix_2x2(matrix)
    a, b = values[0]
    c, d = values[1]
    separation = abs(a - d)
    if separation == 0.0:
        return float("inf")
    product = abs(b * c)
    if product / separation**2 >= 0.25:
        return float("inf")
    return float(2.0 * product / separation)


def audit_matrix(matrix: np.ndarray, target: complex) -> SchurAudit:
    """Compute exact algebraic diagnostics for a target return eigenvalue."""

    values = _matrix_2x2(matrix)
    zeta = complex(target)
    a, b = values[0]
    c, d = values[1]
    if zeta == d:
        raise ZeroDivisionError("the target coincides with the dark pole")
    product = complex(b * c)
    required = required_coupling(a, d, zeta)
    ratio = complex(np.nan) if required == 0 else product / required
    sigma = self_energy(values, zeta)
    shift = complex(zeta - a)
    schur = complex(shift - sigma)
    determinant = characteristic(values, zeta)
    root = bright_root(values)
    separation = abs(a - d)
    epsilon = float("inf") if separation == 0 else float(abs(product) / separation**2)
    pole_distance = float(abs(zeta - d))
    target_scale = abs(zeta)
    pole_ratio = float("inf") if target_scale == 0 else pole_distance / target_scale
    return SchurAudit(
        target=zeta,
        direct_bright=complex(a),
        dark_pole=complex(d),
        bright_to_dark=complex(b),
        dark_to_bright=complex(c),
        observed_product=product,
        required_product=required,
        signed_coupling_ratio=ratio,
        self_energy_at_target=sigma,
        required_shift=shift,
        schur_residual=schur,
        determinant_residual=determinant,
        bright_root=root,
        bright_root_shift=root - a,
        small_coupling_parameter=epsilon,
        small_coupling_bound=small_coupling_root_bound(values),
        target_pole_distance=pole_distance,
        target_pole_distance_ratio=float(pole_ratio),
    )
