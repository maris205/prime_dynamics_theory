from __future__ import annotations

import numpy as np
import pytest

from reduced_cross_factorization import (
    cross_moment_matrices,
    cutoff_projector_bound,
    projected_cross,
    reconstruction_error_bound,
    reduced_cross_factorization,
)


def test_moment_identities() -> None:
    gram = np.diag([5.0, 3.0, 2.0, 1.0])
    packet, _ = np.linalg.qr(np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.0, 1.0]]))
    cross = projected_cross(gram, packet)
    _, _, _, cross_gram, cross_cubic = cross_moment_matrices(gram, packet)
    assert np.linalg.norm(cross_gram - cross.T @ cross) < 1e-12
    assert np.linalg.norm(cross_cubic - cross.T @ gram @ cross) < 1e-11


def test_reduced_factorization() -> None:
    gram = np.diag([6.0, 4.0, 2.0, 1.0])
    packet, _ = np.linalg.qr(np.array([[1.0], [1.0], [1.0], [1.0]]))
    factor = reduced_cross_factorization(gram, packet, 1)
    direction = factor["directions"]
    assert abs(float((direction.T @ direction).item()) - 1.0) < 1e-12
    assert abs(float((packet.T @ direction).item())) < 1e-12
    enriched = np.column_stack([packet, direction])
    assert np.linalg.norm(factor["compressed_moment"] - enriched.T @ gram @ enriched) < 1e-11


def test_stability_bounds() -> None:
    assert reconstruction_error_bound(1e-8, 1e-4) >= 1e-4
    assert cutoff_projector_bound(1e-6, 1e-3) >= 2e-3
    with pytest.raises(ValueError):
        cutoff_projector_bound(1.0, 1.0)
