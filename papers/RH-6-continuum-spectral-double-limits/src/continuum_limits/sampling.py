"""Conditional multinomial diagnostics for a discretized Gaussian row."""

from __future__ import annotations

import numpy as np


def representative_gaussian_row(
    d: int,
    *,
    sigma: float,
    u: float,
    source: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return grid centers and one normalized point-Nystrom Gaussian row."""
    if d < 2 or sigma <= 0.0 or not -1.0 <= source <= 1.0:
        raise ValueError("invalid row parameters")
    h = 2.0 / d
    centers = -1.0 + h * (np.arange(d, dtype=np.float64) + 0.5)
    mean = 1.0 - float(u) * float(source) ** 2
    log_weights = -((centers - mean) ** 2) / (2.0 * sigma * sigma)
    log_weights -= np.max(log_weights)
    weights = np.exp(log_weights)
    return centers, weights / np.sum(weights)


def sampling_diagnostics(
    probabilities: np.ndarray,
    observable: np.ndarray,
    source_count: int,
    repetitions: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    """Measure strong row-L1 and weak observable multinomial errors."""
    probabilities = np.asarray(probabilities, dtype=np.float64)
    observable = np.asarray(observable, dtype=np.float64)
    if probabilities.ndim != 1 or observable.shape != probabilities.shape:
        raise ValueError("probability and observable arrays are incompatible")
    if source_count < 1 or repetitions < 2:
        raise ValueError("source_count and repetitions are too small")
    if not np.isclose(np.sum(probabilities), 1.0, rtol=0.0, atol=2.0e-14):
        raise ValueError("probabilities must sum to one")

    counts = rng.multinomial(source_count, probabilities, size=repetitions)
    estimates = counts / float(source_count)
    differences = estimates - probabilities
    l1 = np.sum(np.abs(differences), axis=1)
    observable_errors = differences @ observable

    mean_observable = float(np.dot(probabilities, observable))
    variance_observable = float(
        np.dot(probabilities, observable * observable) - mean_observable**2
    )
    l1_upper_bound = float(
        np.sum(np.sqrt(probabilities * (1.0 - probabilities) / source_count))
    )
    exact_observable_rms = float(np.sqrt(max(variance_observable, 0.0) / source_count))
    return {
        "mean_l1_error": float(np.mean(l1)),
        "std_l1_error": float(np.std(l1, ddof=1)),
        "l1_upper_bound": l1_upper_bound,
        "observable_rms_error": float(np.sqrt(np.mean(observable_errors**2))),
        "observable_exact_rms": exact_observable_rms,
    }
