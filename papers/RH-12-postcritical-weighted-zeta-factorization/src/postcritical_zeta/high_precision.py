"""Independent multiprecision checks of the algebraic constants and traces."""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


@dataclass(frozen=True)
class MultiprecisionConstants:
    u: mp.mpf
    r: mp.mpf
    lam: mp.mpf


def multiprecision_constants(decimal_places: int = 80) -> MultiprecisionConstants:
    """Solve the band-merging cubic independently at arbitrary precision."""

    if decimal_places < 30:
        raise ValueError("decimal_places must be at least 30")
    with mp.workdps(decimal_places):
        u = mp.findroot(
            lambda value: value**3 - 2 * value**2 + 2 * value - 2,
            mp.mpf("1.54"),
        )
        u = +u
        r = +(u - 1)
        lam = +(2 * u * r)
    return MultiprecisionConstants(u=u, r=r, lam=lam)


def component_weighted_trace_mp_range(
    two_step_length: int,
    start_code: int,
    stop_code: int,
    *,
    decimal_places: int = 80,
    maximum_iterations: int = 240,
) -> mp.mpf:
    """Compute a contiguous range of inverse-word contributions."""

    if two_step_length < 1:
        raise ValueError("two_step_length must be positive")
    if decimal_places < 30:
        raise ValueError("decimal_places must be at least 30")
    count = 1 << two_step_length
    if start_code < 0 or stop_code <= start_code or stop_code > count:
        raise ValueError("invalid inverse-word range")

    with mp.workdps(decimal_places):
        constants = multiprecision_constants(decimal_places)
        u, r = constants.u, constants.r
        tolerance = mp.power(10, -(decimal_places - 15))

        def positive_inverse(value: mp.mpf) -> mp.mpf:
            inner = max(mp.mpf("0"), (1 - value) / u)
            numerator = max(mp.mpf("0"), value + r)
            denominator = u**2 * (1 + mp.sqrt(inner))
            return mp.sqrt(numerator / denominator)

        def inverse_word(value: mp.mpf, code: int) -> mp.mpf:
            result = value
            for shift in range(two_step_length - 1, -1, -1):
                positive = positive_inverse(result)
                result = positive if (code >> shift) & 1 else -positive
            return result

        total = mp.mpf("0")
        for code in range(start_code, stop_code):
            value = mp.mpf("0")
            for _ in range(maximum_iterations):
                updated = inverse_word(value, code)
                if abs(updated - value) <= tolerance:
                    value = updated
                    break
                value = updated
            else:
                raise RuntimeError(
                    f"multiprecision inverse word {code} did not converge"
                )

            weight = mp.mpf("1")
            orbit_value = value
            for shift in range(two_step_length - 1, -1, -1):
                positive = positive_inverse(orbit_value)
                weight /= 4 * u**2 * positive * (1 - u * positive**2)
                orbit_value = positive if (code >> shift) & 1 else -positive
            if abs(orbit_value - value) > mp.sqrt(tolerance):
                raise RuntimeError("multiprecision fixed-point residual is too large")
            total += weight
        return +total


def component_weighted_trace_mp(
    two_step_length: int,
    *,
    decimal_places: int = 80,
    maximum_iterations: int = 240,
) -> mp.mpf:
    """Exhaustively compute one component trace using ``mpmath`` only."""

    return component_weighted_trace_mp_range(
        two_step_length,
        0,
        1 << two_step_length,
        decimal_places=decimal_places,
        maximum_iterations=maximum_iterations,
    )
