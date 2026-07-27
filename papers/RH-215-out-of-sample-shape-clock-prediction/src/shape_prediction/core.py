"""Predeclared low-complexity models for the finite axial clock."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


MODEL_NAMES = ("affine_log", "logistic_log", "power_gap")


@dataclass(frozen=True)
class ClockFit:
    model: str
    slope: float
    intercept: float

    def predict(self, sigma: np.ndarray | float) -> np.ndarray:
        scale = np.asarray(sigma, dtype=float)
        t = np.log(1.0 / scale)
        linear = self.slope * t + self.intercept
        if self.model == "affine_log":
            return linear
        if self.model == "logistic_log":
            return 1.0 / (1.0 + np.exp(-linear))
        if self.model == "power_gap":
            return 1.0 - np.exp(linear)
        raise ValueError(f"unknown model {self.model}")


def transformed_response(model: str, u: np.ndarray) -> np.ndarray:
    values = np.asarray(u, dtype=float)
    if np.any((values <= 0.0) | (values >= 1.0)):
        raise ValueError("clock coordinates must lie strictly between zero and one")
    if model == "affine_log":
        return values
    if model == "logistic_log":
        return np.log(values / (1.0 - values))
    if model == "power_gap":
        return np.log(1.0 - values)
    raise ValueError(f"unknown model {model}")


def fit_clock(model: str, sigmas: np.ndarray, u: np.ndarray) -> ClockFit:
    scales = np.asarray(sigmas, dtype=float).reshape(-1)
    values = np.asarray(u, dtype=float).reshape(-1)
    if scales.shape != values.shape or scales.size < 3:
        raise ValueError("at least three paired training points are required")
    t = np.log(1.0 / scales)
    response = transformed_response(model, values)
    slope, intercept = np.polyfit(t, response, 1)
    return ClockFit(model=model, slope=float(slope), intercept=float(intercept))


def prediction_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    truth = np.asarray(actual, dtype=float).reshape(-1)
    forecast = np.asarray(predicted, dtype=float).reshape(-1)
    if truth.shape != forecast.shape or not truth.size:
        raise ValueError("paired nonempty arrays are required")
    residual = forecast - truth
    denominator = float(np.sum((truth - np.mean(truth)) ** 2))
    r_squared = 1.0 - float(np.sum(residual**2)) / denominator if denominator > 0.0 else float("nan")
    return {
        "r_squared": r_squared,
        "maximum_absolute_error": float(np.max(np.abs(residual))),
        "mean_absolute_error": float(np.mean(np.abs(residual))),
        "root_mean_square_error": float(np.sqrt(np.mean(residual**2))),
    }


def constant_prediction(values: np.ndarray) -> float:
    sample = np.asarray(values, dtype=float).reshape(-1)
    if not sample.size:
        raise ValueError("a nonempty sample is required")
    return float(np.mean(sample))
