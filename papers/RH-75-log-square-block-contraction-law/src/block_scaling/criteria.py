"""Sufficient scalar laws for a polylogarithmic dyadic Hardy family."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


def dyadic_horizon(level: int, offset: float = 2.0) -> int:
    k = int(level)
    shift = float(offset)
    if k < 0 or shift <= 0.0:
        raise ValueError("invalid dyadic horizon inputs")
    return int(math.ceil((k + shift) ** 2))


@dataclass(frozen=True)
class DyadicHardyEnvelope:
    level: int
    horizon: int
    tail_energy_squared_upper: float
    finite_energy_squared_upper: float
    full_energy_squared_upper: float
    hardy_energy_upper: float
    block_contraction_upper: float
    block_contraction_certified: bool

    def as_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def uniform_hardy_envelope(
    *,
    level: int,
    sigma: float,
    sigma_zero: float,
    q_constant: float,
    observation_density_constant: float,
    source_constant: float,
    source_log_power: float,
    finite_constant: float,
    finite_log_power: float,
    horizon_offset: float = 2.0,
) -> DyadicHardyEnvelope:
    """Evaluate the square-root block law and its Hardy consequence."""

    k = int(level)
    noise = float(sigma)
    sigma0 = float(sigma_zero)
    cq = float(q_constant)
    cy = float(observation_density_constant)
    cs = float(source_constant)
    source_power = float(source_log_power)
    cf = float(finite_constant)
    finite_power = float(finite_log_power)
    if (
        k < 0
        or noise <= 0.0
        or sigma0 <= 0.0
        or noise > sigma0
        or min(cq, cy, cs, cf) < 0.0
    ):
        raise ValueError("invalid Hardy envelope inputs")
    contraction = math.nextafter(cq * math.sqrt(noise), math.inf)
    denominator = 1.0 - cq * cq * sigma0
    if denominator <= 0.0:
        raise ValueError("block-contraction denominator is nonpositive")
    logarithmic_scale = k + horizon_offset
    tail = math.nextafter(
        cy
        * cq
        * cq
        * cs
        * logarithmic_scale**source_power
        / denominator,
        math.inf,
    )
    finite = math.nextafter(
        cf * logarithmic_scale**finite_power, math.inf
    )
    full = math.nextafter(finite + tail, math.inf)
    return DyadicHardyEnvelope(
        level=k,
        horizon=dyadic_horizon(k, horizon_offset),
        tail_energy_squared_upper=tail,
        finite_energy_squared_upper=finite,
        full_energy_squared_upper=full,
        hardy_energy_upper=math.nextafter(math.sqrt(full), math.inf),
        block_contraction_upper=contraction,
        block_contraction_certified=contraction < 1.0,
    )
