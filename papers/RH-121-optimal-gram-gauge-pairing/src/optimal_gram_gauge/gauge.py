"""Eigenframe solution of the exact-Gram gauge minimax problem."""

from __future__ import annotations

import math
import numpy as np


def _symmetric(matrix: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or np.any(~np.isfinite(value)):
        raise ValueError(f"{name} must be a finite square matrix")
    return (value + value.T) / 2.0


def _root_pair(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(matrix)
    if values[0] <= 0.0:
        raise ValueError("Gram matrices must be positive definite")
    root = (vectors * values**0.5) @ vectors.T
    inverse = (vectors * values**-0.5) @ vectors.T
    return root, inverse


def normalized_tail_spectrum(gram: np.ndarray, tail: np.ndarray) -> np.ndarray:
    """Return the ascending generalized spectrum of ``(tail, gram)``."""
    g = _symmetric(gram, "gram")
    d = _symmetric(tail, "tail")
    if np.linalg.eigvalsh(d)[0] <= 0.0:
        raise ValueError("the optimal finite theorem requires a positive definite tail")
    _, inverse = _root_pair(g)
    relative = inverse @ d @ inverse
    return np.linalg.eigvalsh((relative + relative.T) / 2.0)


def optimal_exact_gram_gauge(
    source_gram: np.ndarray,
    source_tail: np.ndarray,
    target_gram: np.ndarray,
    target_tail: np.ndarray,
) -> dict[str, object]:
    """Return the exact-Gram gauge minimizing target tail inflation.

    Among all ``S`` with ``S.T G S = G'``, this minimizes the least ``b``
    satisfying ``D' <= b S.T D S``.
    """
    g = _symmetric(source_gram, "source gram")
    d = _symmetric(source_tail, "source tail")
    gp = _symmetric(target_gram, "target gram")
    dp = _symmetric(target_tail, "target tail")
    source_root, source_inverse = _root_pair(g)
    target_root, target_inverse = _root_pair(gp)
    source_relative = source_inverse @ d @ source_inverse
    target_relative = target_inverse @ dp @ target_inverse
    alpha, source_vectors = np.linalg.eigh((source_relative + source_relative.T) / 2.0)
    beta, target_vectors = np.linalg.eigh((target_relative + target_relative.T) / 2.0)
    if alpha[0] <= 0.0 or beta[0] <= 0.0:
        raise ValueError("both tail matrices must be positive definite")
    orthogonal = source_vectors @ target_vectors.T
    gauge = source_inverse @ orthogonal @ target_root
    transported = gauge.T @ d @ gauge
    ratios = beta / alpha
    factor = float(np.max(ratios))
    gram_error = float(np.linalg.norm(gauge.T @ g @ gauge - gp, 2))
    tail_slack = float(np.linalg.eigvalsh(factor * transported - dp)[0])
    source_gamma = math.sqrt(float(alpha[-1]))
    target_gamma = math.sqrt(float(beta[-1]))
    gamma_upper = math.sqrt(factor) * source_gamma
    return {
        "gauge": gauge,
        "orthogonal_alignment": orthogonal,
        "source_spectrum": alpha,
        "target_spectrum": beta,
        "matched_ratios": ratios,
        "optimal_tail_factor": factor,
        "source_gamma": source_gamma,
        "target_gamma": target_gamma,
        "gamma_upper": gamma_upper,
        "gram_alignment_error": gram_error,
        "tail_minimum_slack": tail_slack,
        "gauge_determinant": float(np.linalg.det(gauge)),
        "source_root_trace": float(np.trace(source_root)),
    }

