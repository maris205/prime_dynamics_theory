"""Exact Feshbach identities for a finite-rank oblique packet projection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


VectorOperator = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class DenseFeshbachData:
    """Exact dense packet/complement Schur data at one spectral parameter."""

    reduced: np.ndarray
    self_energy: np.ndarray
    feshbach: np.ndarray
    external_solutions: np.ndarray
    full_determinant: complex
    external_full_determinant: complex
    feshbach_determinant: complex
    determinant_residual: float


@dataclass(frozen=True)
class EigenmodeClosure:
    """Two exact block equations induced by one physical eigenmode."""

    coordinates: np.ndarray
    packet_component: np.ndarray
    external_component: np.ndarray
    reduced: np.ndarray
    packet_defect: np.ndarray
    external_self_energy_action: np.ndarray
    external_forcing: np.ndarray
    packet_closure_residual: float
    external_equation_residual: float
    packet_component_norm: float
    external_component_norm: float
    coordinate_norm: float
    forcing_norm: float
    resolvent_lower_bound: float


def _pair(
    synthesis: np.ndarray,
    analysis: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    trial = np.asarray(synthesis)
    test = np.asarray(analysis)
    if trial.ndim != 2 or test.ndim != 2:
        raise ValueError("synthesis and analysis must be matrices")
    if test.shape != (trial.shape[1], trial.shape[0]):
        raise ValueError("analysis must have shape (packet rank, ambient rank)")
    residual = np.linalg.norm(test @ trial - np.eye(trial.shape[1]))
    if residual > 2.0e-8:
        raise ValueError("analysis and synthesis are not biorthogonal")
    dtype = np.complex128 if np.iscomplexobj(trial) or np.iscomplexobj(test) else np.float64
    return np.asarray(trial, dtype=dtype), np.asarray(test, dtype=dtype)


def packet_project(
    values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
) -> np.ndarray:
    """Apply the oblique packet projector ``P=VW``."""

    trial, test = _pair(synthesis, analysis)
    source = np.asarray(values)
    if source.shape[0] != trial.shape[0]:
        raise ValueError("values and packet pair have incompatible dimensions")
    return trial @ (test @ source)


def external_project(
    values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
) -> np.ndarray:
    """Apply the complementary projector ``Q=I-VW``."""

    source = np.asarray(values)
    return source - packet_project(source, synthesis, analysis)


def reduced_matrix(
    operator: VectorOperator,
    synthesis: np.ndarray,
    analysis: np.ndarray,
) -> np.ndarray:
    """Return the Petrov--Galerkin matrix ``W A V``."""

    trial, test = _pair(synthesis, analysis)
    applied = np.asarray(operator(trial))
    if applied.shape != trial.shape:
        raise ValueError("operator must preserve the synthesis shape")
    return np.asarray(test @ applied)


def eigenmode_closure(
    operator: VectorOperator,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    eigenvalue: complex,
    eigenvector: np.ndarray,
) -> EigenmodeClosure:
    r"""Evaluate the exact packet and external equations for ``A r=z r``."""

    trial, test = _pair(synthesis, analysis)
    vector = np.asarray(eigenvector, dtype=np.complex128).reshape(-1)
    if vector.size != trial.shape[0]:
        raise ValueError("eigenvector and packet pair have incompatible dimensions")
    zeta = complex(eigenvalue)
    coordinates = test @ vector
    packet = trial @ coordinates
    external = vector - packet
    reduced = reduced_matrix(operator, trial, test)
    applied_external = np.asarray(operator(external), dtype=np.complex128)
    applied_packet = np.asarray(operator(trial @ coordinates), dtype=np.complex128)
    external_self_energy = test @ applied_external
    packet_defect = (zeta * np.eye(trial.shape[1]) - reduced) @ coordinates
    forcing = external_project(applied_packet, trial, test)
    external_left = zeta * external - external_project(
        applied_external, trial, test
    )
    packet_scale = max(
        np.linalg.norm(packet_defect),
        np.linalg.norm(external_self_energy),
        np.finfo(float).tiny,
    )
    external_scale = max(
        np.linalg.norm(forcing),
        np.linalg.norm(external_left),
        np.finfo(float).tiny,
    )
    forcing_norm = float(np.linalg.norm(forcing))
    external_norm = float(np.linalg.norm(external))
    lower_bound = float("inf") if forcing_norm == 0.0 else external_norm / forcing_norm
    return EigenmodeClosure(
        coordinates=np.asarray(coordinates),
        packet_component=np.asarray(packet),
        external_component=np.asarray(external),
        reduced=np.asarray(reduced),
        packet_defect=np.asarray(packet_defect),
        external_self_energy_action=np.asarray(external_self_energy),
        external_forcing=np.asarray(forcing),
        packet_closure_residual=float(
            np.linalg.norm(packet_defect - external_self_energy) / packet_scale
        ),
        external_equation_residual=float(
            np.linalg.norm(external_left - forcing) / external_scale
        ),
        packet_component_norm=float(np.linalg.norm(packet)),
        external_component_norm=external_norm,
        coordinate_norm=float(np.linalg.norm(coordinates)),
        forcing_norm=forcing_norm,
        resolvent_lower_bound=lower_bound,
    )


def dense_feshbach_data(
    matrix: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    spectral_parameter: complex,
) -> DenseFeshbachData:
    r"""Return the exact dense Feshbach matrix and determinant check.

    The solve uses ``z I-Q A Q`` on the full ambient space.  Its restriction
    to the packet range is ``z I``, so the full determinant contains an
    extra factor ``z**m`` relative to the external determinant.
    """

    values = np.asarray(matrix, dtype=np.complex128)
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("matrix must be square")
    trial, test = _pair(synthesis, analysis)
    if trial.shape[0] != values.shape[0]:
        raise ValueError("matrix and packet pair have incompatible dimensions")
    zeta = complex(spectral_parameter)
    if zeta == 0.0:
        raise ValueError("the full-space determinant check requires nonzero z")
    packet = trial @ test
    external = np.eye(values.shape[0]) - packet
    reduced = test @ values @ trial
    coupling_out = test @ values @ external
    coupling_in = external @ values @ trial
    external_operator = zeta * np.eye(values.shape[0]) - external @ values @ external
    solutions = np.linalg.solve(external_operator, coupling_in)
    self_energy = coupling_out @ solutions
    feshbach = zeta * np.eye(trial.shape[1]) - reduced - self_energy
    full_det = np.linalg.det(zeta * np.eye(values.shape[0]) - values)
    external_full_det = np.linalg.det(external_operator)
    feshbach_det = np.linalg.det(feshbach)
    reconstructed = external_full_det * feshbach_det / zeta**trial.shape[1]
    scale = max(abs(full_det), abs(reconstructed), np.finfo(float).tiny)
    return DenseFeshbachData(
        reduced=np.asarray(reduced),
        self_energy=np.asarray(self_energy),
        feshbach=np.asarray(feshbach),
        external_solutions=np.asarray(solutions),
        full_determinant=complex(full_det),
        external_full_determinant=complex(external_full_det),
        feshbach_determinant=complex(feshbach_det),
        determinant_residual=float(abs(full_det - reconstructed) / scale),
    )
