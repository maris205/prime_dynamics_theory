"""Scalar composition of directional Hardy and intrinsic-identification bounds."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


def rank_corridor_upper(prefix_energy: float, reduced_future: float, truncation_error: float) -> float:
    values = [float(prefix_energy), float(reduced_future), float(truncation_error)]
    if any(value < 0.0 for value in values):
        raise ValueError("energy bounds must be nonnegative")
    return math.nextafter(sum(values), math.inf)


@dataclass(frozen=True)
class IdentificationEnvelope:
    sigma: float
    mesh: float
    left_hardy_upper: float
    right_hardy_upper: float
    hardy_product_upper: float
    identification_upper: float
    hardy_sigma_power: float
    quarter_power_gate: bool

    def as_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def identification_envelope(
    *,
    sigma: float,
    mesh: float,
    left_hardy_upper: float,
    right_hardy_upper: float,
    left_sigma_power: float = 0.0,
    right_sigma_power: float = 0.0,
) -> IdentificationEnvelope:
    noise = float(sigma)
    n = float(mesh)
    left = float(left_hardy_upper)
    right = float(right_hardy_upper)
    alpha_left = float(left_sigma_power)
    alpha_right = float(right_sigma_power)
    if noise <= 0.0 or n <= 0.0 or min(left, right, alpha_left, alpha_right) < 0.0:
        raise ValueError("invalid identification inputs")
    product = math.nextafter(left * right, math.inf)
    identification = math.nextafter(n ** -2 * noise ** (-13.0 / 4.0) * product, math.inf)
    exponent = alpha_left + alpha_right
    return IdentificationEnvelope(
        sigma=noise,
        mesh=n,
        left_hardy_upper=left,
        right_hardy_upper=right,
        hardy_product_upper=product,
        identification_upper=identification,
        hardy_sigma_power=exponent,
        quarter_power_gate=exponent <= 0.25,
    )
