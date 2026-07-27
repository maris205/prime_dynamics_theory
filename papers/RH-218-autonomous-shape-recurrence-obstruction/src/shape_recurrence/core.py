"""Low-complexity recurrences and finite-orbit non-identifiability."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


SCALAR_MODELS = ("affine", "logistic", "power_gap")


def transform(model: str, values: np.ndarray) -> np.ndarray:
    data = np.asarray(values, dtype=float)
    if model == "affine":
        return data
    if np.any((data <= 0.0) | (data >= 1.0)):
        raise ValueError("transformed recurrences require values in (0,1)")
    if model == "logistic":
        return np.log(data / (1.0 - data))
    if model == "power_gap":
        return np.log(1.0 - data)
    raise ValueError(f"unknown recurrence model {model}")


def inverse_transform(model: str, values: np.ndarray) -> np.ndarray:
    data = np.asarray(values, dtype=float)
    if model == "affine":
        return data
    if model == "logistic":
        return 1.0 / (1.0 + np.exp(-data))
    if model == "power_gap":
        return 1.0 - np.exp(data)
    raise ValueError(f"unknown recurrence model {model}")


@dataclass(frozen=True)
class ScalarRecurrence:
    model: str
    slope: float
    intercept: float

    def __call__(self, values: np.ndarray | float) -> np.ndarray:
        transformed = transform(self.model, np.asarray(values, dtype=float))
        return inverse_transform(self.model, self.slope * transformed + self.intercept)


def fit_scalar_recurrence(model: str, current: np.ndarray, following: np.ndarray) -> ScalarRecurrence:
    first = transform(model, np.asarray(current, dtype=float).reshape(-1))
    second = transform(model, np.asarray(following, dtype=float).reshape(-1))
    if first.shape != second.shape or first.size < 2:
        raise ValueError("at least two paired transitions are required")
    slope, intercept = np.polyfit(first, second, 1)
    return ScalarRecurrence(model, float(slope), float(intercept))


@dataclass(frozen=True)
class AffineShapeMap:
    matrix: np.ndarray
    offset: np.ndarray

    def __call__(self, states: np.ndarray) -> np.ndarray:
        values = np.asarray(states, dtype=float)
        return values @ self.matrix.T + self.offset


def fit_affine_shape_map(current: np.ndarray, following: np.ndarray) -> AffineShapeMap:
    first = np.asarray(current, dtype=float)
    second = np.asarray(following, dtype=float)
    if first.ndim != 2 or first.shape != second.shape or first.shape[1] != 2:
        raise ValueError("paired two-dimensional states are required")
    design = np.column_stack((first, np.ones(first.shape[0])))
    coefficients, *_ = np.linalg.lstsq(design, second, rcond=None)
    return AffineShapeMap(coefficients[:2, :].T, coefficients[2, :])


def lagrange_autonomous_map(states: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Interpolate any finite distinct-u orbit by F(u,eta)=(P(u),Q(u))."""

    points = np.asarray(states, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or points.shape[0] < 2:
        raise ValueError("a finite two-dimensional orbit is required")
    current_u = points[:-1, 0]
    if np.min(np.abs(current_u[:, None] - current_u[None, :] + np.eye(current_u.size)), initial=1.0) == 0.0:
        raise ValueError("current u coordinates must be distinct")
    degree = current_u.size - 1
    p = np.polyfit(current_u, points[1:, 0], degree)
    q = np.polyfit(current_u, points[1:, 1], degree)
    return p, q


def evaluate_polynomial_shape_map(coefficients: tuple[np.ndarray, np.ndarray], states: np.ndarray) -> np.ndarray:
    points = np.asarray(states, dtype=float)
    return np.column_stack((np.polyval(coefficients[0], points[:, 0]), np.polyval(coefficients[1], points[:, 0])))


def error_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    truth = np.asarray(actual, dtype=float)
    forecast = np.asarray(predicted, dtype=float)
    residual = forecast - truth
    row_norms = np.linalg.norm(residual, axis=1) if residual.ndim == 2 else np.abs(residual)
    return {
        "maximum_error": float(np.max(row_norms)),
        "mean_error": float(np.mean(row_norms)),
        "rms_error": float(np.sqrt(np.mean(row_norms**2))),
    }
