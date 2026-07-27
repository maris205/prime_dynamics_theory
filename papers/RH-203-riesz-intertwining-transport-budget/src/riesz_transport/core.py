"""Exact finite-dimensional identities behind Riesz packet transport."""

from __future__ import annotations

import math

import numpy as np


def resolvent_intertwining(
    fine_operator: np.ndarray,
    coarse_operator: np.ndarray,
    embedding: np.ndarray,
    spectral_parameter: complex,
) -> dict[str, np.ndarray | float]:
    """Evaluate R_f J-J R_c=R_f(A_fJ-JA_c)R_c."""

    fine = np.asarray(fine_operator, dtype=complex)
    coarse = np.asarray(coarse_operator, dtype=complex)
    lift = np.asarray(embedding, dtype=complex)
    z = complex(spectral_parameter)
    fine_resolvent = np.linalg.inv(z * np.eye(fine.shape[0]) - fine)
    coarse_resolvent = np.linalg.inv(z * np.eye(coarse.shape[0]) - coarse)
    defect = fine @ lift - lift @ coarse
    left = fine_resolvent @ lift - lift @ coarse_resolvent
    right = fine_resolvent @ defect @ coarse_resolvent
    return {
        "left": left,
        "right": right,
        "defect": defect,
        "absolute_identity_residual": float(np.linalg.norm(left - right, 2)),
    }


def contour_projector_bound(
    contour_length: float,
    fine_resolvent_upper: float,
    coarse_resolvent_upper: float,
    intertwining_defect_upper: float,
) -> float:
    """Return the standard integrated resolvent transport upper bound."""

    values = tuple(float(value) for value in (
        contour_length,
        fine_resolvent_upper,
        coarse_resolvent_upper,
        intertwining_defect_upper,
    ))
    if any(not math.isfinite(value) or value < 0.0 for value in values):
        raise ValueError("transport bounds must be finite and nonnegative")
    length, fine, coarse, defect = values
    return length * fine * coarse * defect / (2.0 * math.pi)


def channel_transport_decomposition(
    fine_projector: np.ndarray,
    coarse_projector: np.ndarray,
    fine_source: np.ndarray,
    coarse_source: np.ndarray,
    row_embedding: np.ndarray,
    column_embedding: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """Split channel-state transport into source and projector defects."""

    pf = np.asarray(fine_projector, dtype=complex)
    pc = np.asarray(coarse_projector, dtype=complex)
    sf = np.asarray(fine_source, dtype=complex)
    sc = np.asarray(coarse_source, dtype=complex)
    row = np.asarray(row_embedding, dtype=complex)
    column = np.asarray(column_embedding, dtype=complex)
    lifted_source = row @ sc @ column.conj().T
    source_defect = sf - lifted_source
    projector_defect = pf @ row - row @ pc
    left = pf @ sf - row @ pc @ sc @ column.conj().T
    source_term = pf @ source_defect
    projector_term = projector_defect @ sc @ column.conj().T
    right = source_term + projector_term
    upper = (
        np.linalg.norm(pf, 2) * np.linalg.norm(source_defect, "fro")
        + np.linalg.norm(projector_defect, 2) * np.linalg.norm(sc, "fro")
    )
    return {
        "left": left,
        "right": right,
        "source_term": source_term,
        "projector_term": projector_term,
        "absolute_identity_residual": float(np.linalg.norm(left - right, "fro")),
        "triangle_upper_bound": float(upper),
    }
