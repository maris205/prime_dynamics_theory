"""Exterior-power fourth-cross bounds and a sharp scalar-volume barrier."""

from __future__ import annotations

from itertools import combinations
import math

import numpy as np


def _spectrum(values: list[float] | tuple[float, ...] | np.ndarray) -> np.ndarray:
    singular = np.asarray(values, dtype=float)
    if singular.ndim != 1 or singular.size < 4:
        raise ValueError("at least four singular values are required")
    if np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("singular values must be finite and nonnegative")
    return np.sort(singular)[::-1]


def _delta(value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError("the perturbation radius must be finite and nonnegative")
    return number


def _positive_threshold(value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError("the threshold must be finite and positive")
    return number


def exterior_dimension(rank: int) -> int:
    width = int(rank)
    if width < 4:
        raise ValueError("the packet rank must be at least four")
    return math.comb(width, 4)


def spectral_four_volume(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return ||wedge^4 K||_2 from the singular values of K."""
    singular = _spectrum(values)
    return float(np.prod(singular[:4], dtype=float))


def normalized_spectral_four_volume(
    values: list[float] | tuple[float, ...] | np.ndarray,
) -> float:
    """Return (s1 s2 s3 s4) / s1^4."""
    singular = _spectrum(values)
    leading = float(singular[0])
    if leading == 0.0:
        return 0.0
    return spectral_four_volume(singular) / leading**4


def elementary_symmetric_four(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return e_4(values), using a finite positive summation."""
    numbers = np.asarray(values, dtype=float)
    if numbers.ndim != 1 or numbers.size < 4:
        raise ValueError("at least four values are required")
    if np.any(~np.isfinite(numbers)) or np.any(numbers < 0.0):
        raise ValueError("values must be finite and nonnegative")
    terms = (float(np.prod(numbers[list(index)], dtype=float)) for index in combinations(range(numbers.size), 4))
    return float(math.fsum(terms))


def trace_four_volume(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return ||wedge^4 K||_F from singular values of K."""
    singular = _spectrum(values)
    return math.sqrt(elementary_symmetric_four(singular**2))


def normalized_trace_four_volume(
    values: list[float] | tuple[float, ...] | np.ndarray,
) -> float:
    singular = _spectrum(values)
    leading = float(singular[0])
    if leading == 0.0:
        return 0.0
    return trace_four_volume(singular) / leading**4


def volume_loss_factor(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return nu_4 / (s_4/s_1) = (s_2/s_1)(s_3/s_1)."""
    singular = _spectrum(values)
    leading = float(singular[0])
    if leading == 0.0:
        return 0.0
    return float((singular[1] / leading) * (singular[2] / leading))


def exterior_volume_certificate(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
) -> dict[str, float | int | bool]:
    """Build spectral and trace exterior-volume lower bounds after a tail."""
    singular = _spectrum(recent_singular_values)
    delta = _delta(tail_operator_bound)
    lower = np.maximum(singular - delta, 0.0)
    upper_leading = float(singular[0] + delta)
    exterior_count = exterior_dimension(singular.size)
    if upper_leading == 0.0:
        spectral_lower = 0.0
        trace_lower = 0.0
    else:
        spectral_lower = float(np.prod(lower[:4], dtype=float) / upper_leading**4)
        trace_lower = math.sqrt(elementary_symmetric_four(lower**2) / exterior_count) / upper_leading**4
    return {
        "packet_rank": int(singular.size),
        "exterior_dimension": int(exterior_count),
        "tail_operator_bound": delta,
        "recent_leading_singular_value": float(singular[0]),
        "recent_fourth_singular_value": float(singular[3]),
        "spectral_volume_lower_bound": spectral_lower,
        "trace_volume_lower_bound": float(trace_lower),
        "spectral_support_certified": False,
        "trace_support_certified": False,
    }


def finite_memory_exterior_certificate(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
    threshold: float,
) -> dict[str, float | int | bool]:
    """Add threshold decisions to :func:`exterior_volume_certificate`."""
    cutoff = _positive_threshold(threshold)
    result = exterior_volume_certificate(recent_singular_values, tail_operator_bound)
    result["threshold"] = cutoff
    result["spectral_support_certified"] = bool(result["spectral_volume_lower_bound"] >= cutoff)
    result["trace_support_certified"] = bool(result["trace_volume_lower_bound"] >= cutoff)
    return result


def scalar_volume_interval(normalized_volume: float) -> tuple[float, float]:
    """Sharp universal interval for q=s4/s1 given spectral volume nu_4."""
    volume = float(normalized_volume)
    if not math.isfinite(volume) or volume < 0.0 or volume > 1.0:
        raise ValueError("normalized spectral volume must lie in [0, 1]")
    return volume, volume ** (1.0 / 3.0)


def _barrier_row(directions: np.ndarray, eta: float) -> dict[str, object]:
    identity = np.eye(4)
    block = np.block([[identity, directions], [directions, identity]]) / 8.0
    source = np.diag([2.0] * 4 + [1.0] * 4) / 12.0
    memory = block + eta * source
    packet = np.eye(8, 4)
    projector = packet @ packet.T
    cross = (np.eye(8) - projector) @ memory @ packet
    singular = np.linalg.svd(cross, compute_uv=False)
    return {
        "directions": np.diag(directions).tolist(),
        "snapshot": block,
        "memory": memory,
        "singular_values": singular,
        "ratio": float(singular[3] / singular[0]) if singular[0] else 0.0,
        "normalized_volume": normalized_spectral_four_volume(singular),
        "trace_clock": float(np.trace(memory)),
        "packet_block": packet.T @ memory @ packet,
        "complement_block": memory[4:, 4:],
        "operator_norm": float(np.linalg.norm(memory, 2)),
    }


def sharp_scalar_volume_barrier(normalized_volume: float, eta: float = 1.0 / 512.0) -> dict[str, object]:
    """Construct two admissible memories with the same volume and sharp q endpoints."""
    volume = float(normalized_volume)
    if not math.isfinite(volume) or volume < 0.0 or volume > 1.0:
        raise ValueError("normalized spectral volume must lie in [0, 1]")
    decay = float(eta)
    if not math.isfinite(decay) or decay < 0.0 or decay >= 1.0:
        raise ValueError("eta must lie in [0, 1)")
    cube_root = volume ** (1.0 / 3.0)
    linear = _barrier_row(np.diag([1.0, 1.0, 1.0, volume]), decay)
    cubic = _barrier_row(np.diag([1.0, cube_root, cube_root, cube_root]), decay)
    return {
        "eta": decay,
        "normalized_volume": volume,
        "linear": linear,
        "cubic": cubic,
        "trace_clock_constant": abs(linear["trace_clock"] - cubic["trace_clock"]) < 1e-14,
        "diagonal_blocks_constant": (
            np.linalg.norm(linear["packet_block"] - cubic["packet_block"], 2) < 1e-14
            and np.linalg.norm(linear["complement_block"] - cubic["complement_block"], 2) < 1e-14
        ),
    }
