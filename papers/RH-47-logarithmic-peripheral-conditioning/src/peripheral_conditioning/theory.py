"""Analytic clocks for endpoint conditioning and anchored deflation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


U_CRITICAL = 1.54368901269207636157085597180174798652520329765098
ENDPOINT_RHO_C = 0.5626412544865719


def logarithmic_clock(sigma: float) -> float:
    """Return the natural square-root logarithmic peripheral clock."""

    width = float(sigma)
    if not 0.0 < width < 1.0:
        raise ValueError("sigma must lie in (0,1)")
    return math.sqrt(math.log(1.0 / width))


def endpoint_tail_constant(
    rho_c: float = ENDPOINT_RHO_C,
    u: float = U_CRITICAL,
) -> float:
    r"""Return ``c_R`` in ``R(xi) ~ c_R xi^(-1/2)``."""

    density = float(rho_c)
    parameter = float(u)
    if density <= 0.0 or parameter <= 0.0:
        raise ValueError("rho_c and u must be positive")
    return density / (2.0 * math.sqrt(parameter))


def endpoint_log_coefficient(
    rho_c: float = ENDPOINT_RHO_C,
    u: float = U_CRITICAL,
) -> float:
    r"""Return the endpoint coefficient in the squared-density log law."""

    constant = endpoint_tail_constant(rho_c, u)
    return constant * constant


def contour_resolvent_lower(
    projector_norm: float, contour_radius: float
) -> float:
    r"""Use ``||P|| <= r sup_Gamma ||(z-K)^-1||`` on a circle."""

    projection = float(projector_norm)
    radius = float(contour_radius)
    if projection < 0.0 or radius <= 0.0:
        raise ValueError("projector norm must be nonnegative and radius positive")
    return projection / radius


@dataclass(frozen=True)
class AnchoredBulkLedger:
    sigma: float
    dimension: int
    logarithmic_clock: float
    markov_hilbert_schmidt_upper: float
    peripheral_hilbert_schmidt_upper: float
    anchored_bulk_hilbert_schmidt_upper: float
    markov_projection_error_upper: float
    peripheral_projection_error_upper: float
    anchored_bulk_error_upper: float
    anchored_square_trace_norm_error_upper: float
    one_step_scaled_resolution: float
    two_step_scaled_resolution: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def anchored_bulk_ledger(
    sigma: float,
    dimension: int,
    *,
    markov_size_constant: float = 2.124503864054395,
    markov_error_constant: float = 3.620364287707642,
    peripheral_size_constant: float = 1.0,
    peripheral_error_constant: float = 1.0,
) -> AnchoredBulkLedger:
    r"""Compose the spatially anchored small-noise bulk bounds.

    The theorem supplies ``||Q_per,sigma||_2 <= C_Q sqrt(log(1/sigma))``
    and ``||E_n Q_per E_n-Q_per||_2 <= C_E/(n sigma^(3/2))``.
    Constants are left symbolic in the manuscript; this ledger exposes their
    scaling and interaction with the explicit RH-46 Markov constants.
    """

    width = float(sigma)
    n = int(dimension)
    if not 0.0 < width < 1.0 or n < 2:
        raise ValueError("sigma must lie in (0,1) and dimension be at least 2")
    clock = logarithmic_clock(width)
    markov_size = float(markov_size_constant) * width**-0.5
    peripheral_size = float(peripheral_size_constant) * clock
    bulk_size = markov_size + peripheral_size
    markov_error = (
        float(markov_error_constant) / (n * width**1.5)
    )
    peripheral_error = (
        float(peripheral_error_constant) / (n * width**1.5)
    )
    bulk_error = markov_error + peripheral_error
    square_error = bulk_error * (2.0 * bulk_size + bulk_error)
    return AnchoredBulkLedger(
        sigma=width,
        dimension=n,
        logarithmic_clock=clock,
        markov_hilbert_schmidt_upper=markov_size,
        peripheral_hilbert_schmidt_upper=peripheral_size,
        anchored_bulk_hilbert_schmidt_upper=bulk_size,
        markov_projection_error_upper=markov_error,
        peripheral_projection_error_upper=peripheral_error,
        anchored_bulk_error_upper=bulk_error,
        anchored_square_trace_norm_error_upper=square_error,
        one_step_scaled_resolution=n * width**1.5,
        two_step_scaled_resolution=n * width**2.0,
    )


def power_schedule_closes(power: float) -> dict[str, float | bool]:
    """Return the leading anchored-bulk exponents for ``n ~ sigma^-p``."""

    exponent = float(power)
    if exponent <= 0.0:
        raise ValueError("power must be positive")
    return {
        "power": exponent,
        "hilbert_schmidt_error_exponent": exponent - 1.5,
        "square_trace_norm_error_exponent": exponent - 2.0,
        "hilbert_schmidt_converges": exponent > 1.5,
        "square_trace_norm_converges": exponent > 2.0,
    }
