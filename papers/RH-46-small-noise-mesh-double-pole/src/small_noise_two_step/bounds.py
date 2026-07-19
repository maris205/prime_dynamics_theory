"""Explicit small-noise Gaussian mesh and geometric determinant bounds."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

import numpy as np


CRITICAL_U = 1.54368901269207636157085597180174798652520329765098
DETERMINISTIC_LAMBDA = 1.6785735104283222651037051293065732008483574921952


def _up(value: float) -> float:
    number = float(value)
    if math.isnan(number):
        raise ValueError("outward upper cannot be NaN")
    return math.nextafter(number, math.inf)


def upper_add(*values: float) -> float:
    total = 0.0
    for value in values:
        if value < 0.0:
            raise ValueError("upper sums require nonnegative values")
        total = _up(total + float(value))
    return total


def upper_multiply(*values: float) -> float:
    total = 1.0
    for value in values:
        if value < 0.0:
            raise ValueError("upper products require nonnegative values")
        total = _up(total * float(value))
    return total


def normalizer_linear_lower(sigma_maximum: float = 0.03) -> float:
    r"""Return ``c_0`` such that ``Z_sigma(x) >= c_0 sigma``.

    The folded normalizer is the Gaussian mass of ``[-1,1]`` with center
    ``m(x) in [1-u_c,1]``.  Its minimum is attained at center one.
    """

    maximum = float(sigma_maximum)
    if not 0.0 < maximum <= 0.25:
        raise ValueError("sigma maximum must lie in (0,1/4]")
    return math.nextafter(
        math.sqrt(math.pi / 2.0)
        * math.erf(math.sqrt(2.0) / maximum),
        0.0,
    )


@dataclass(frozen=True)
class FoldedGaussianEnvelope:
    sigma: float
    sigma_maximum: float
    normalizer_linear_lower: float
    kernel_hilbert_schmidt_upper: float
    raw_parameter_first_row_L2_upper: float
    normalized_parameter_first_row_L2_upper: float
    source_first_hilbert_schmidt_upper: float
    target_first_hilbert_schmidt_upper: float
    combined_first_hilbert_schmidt_upper: float
    kernel_scaled_constant: float
    combined_first_scaled_constant: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def folded_gaussian_envelope(
    sigma: float,
    *,
    sigma_maximum: float = 0.03,
    critical_u: float = CRITICAL_U,
) -> FoldedGaussianEnvelope:
    r"""Coarse explicit Hilbert--Schmidt bounds for the normalized kernel.

    The bounds use only full-line Gaussian moments, ``|Z_m| <= 1``, and
    ``Z >= c_0 sigma``.  They are deliberately uniform rather than sharp.
    """

    width = float(sigma)
    maximum = float(sigma_maximum)
    if not 0.0 < width <= maximum:
        raise ValueError("sigma must lie in (0,sigma_maximum]")
    c0 = normalizer_linear_lower(maximum)
    pi_quarter = math.pi ** 0.25
    kernel_constant = _up(2.0 * pi_quarter / c0)
    raw_parameter_constant = _up(math.sqrt(2.0) * pi_quarter)
    normalized_parameter_constant = _up(
        pi_quarter * (math.sqrt(2.0) / c0 + 2.0 / (c0 * c0))
    )
    target_constant = _up(math.sqrt(2.0) * pi_quarter / c0)
    source_constant = _up(
        2.0 * float(critical_u) * normalized_parameter_constant
    )
    combined_constant = upper_add(source_constant, target_constant)
    return FoldedGaussianEnvelope(
        sigma=width,
        sigma_maximum=maximum,
        normalizer_linear_lower=c0,
        kernel_hilbert_schmidt_upper=upper_multiply(
            kernel_constant, width ** -0.5
        ),
        raw_parameter_first_row_L2_upper=upper_multiply(
            raw_parameter_constant, width ** -0.5
        ),
        normalized_parameter_first_row_L2_upper=upper_multiply(
            normalized_parameter_constant, width ** -1.5
        ),
        source_first_hilbert_schmidt_upper=upper_multiply(
            source_constant, width ** -1.5
        ),
        target_first_hilbert_schmidt_upper=upper_multiply(
            target_constant, width ** -1.5
        ),
        combined_first_hilbert_schmidt_upper=upper_multiply(
            combined_constant, width ** -1.5
        ),
        kernel_scaled_constant=kernel_constant,
        combined_first_scaled_constant=combined_constant,
    )


@dataclass(frozen=True)
class GalerkinResolutionLedger:
    sigma: float
    dimension: int
    determinant_disk_radius: float
    kernel_hilbert_schmidt_upper: float
    galerkin_hilbert_schmidt_error_upper: float
    approximate_hilbert_schmidt_upper: float
    continuum_square_trace_norm_upper: float
    approximate_square_trace_norm_upper: float
    square_trace_norm_error_upper: float
    determinant_log_error_upper: float
    determinant_log10_error_upper: float
    one_step_scaled_resolution: float
    two_step_scaled_resolution: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def galerkin_resolution_ledger(
    sigma: float,
    dimension: int,
    *,
    determinant_disk_radius: float,
    sigma_maximum: float = 0.03,
) -> GalerkinResolutionLedger:
    r"""Compose cell-average HS, square trace norm, and determinant bounds."""

    width = float(sigma)
    n = int(dimension)
    radius = float(determinant_disk_radius)
    if n < 2 or radius <= 0.0:
        raise ValueError("dimension and determinant radius must be positive")
    envelope = folded_gaussian_envelope(
        width, sigma_maximum=sigma_maximum
    )
    error = upper_multiply(
        1.0 / (math.pi * n),
        envelope.combined_first_hilbert_schmidt_upper,
    )
    continuum = envelope.kernel_hilbert_schmidt_upper
    approximate = upper_add(continuum, error)
    continuum_square = upper_multiply(continuum, continuum)
    approximate_square = upper_multiply(approximate, approximate)
    trace_error = upper_multiply(
        error, upper_add(continuum, approximate)
    )
    log_error = (
        math.log(radius)
        + math.log(trace_error)
        + 1.0
        + radius * continuum_square
        + radius * approximate_square
    )
    return GalerkinResolutionLedger(
        sigma=width,
        dimension=n,
        determinant_disk_radius=radius,
        kernel_hilbert_schmidt_upper=continuum,
        galerkin_hilbert_schmidt_error_upper=error,
        approximate_hilbert_schmidt_upper=approximate,
        continuum_square_trace_norm_upper=continuum_square,
        approximate_square_trace_norm_upper=approximate_square,
        square_trace_norm_error_upper=trace_error,
        determinant_log_error_upper=_up(log_error),
        determinant_log10_error_upper=_up(log_error / math.log(10.0)),
        one_step_scaled_resolution=_up(n * width**1.5),
        two_step_scaled_resolution=_up(n * width**2.0),
    )


def power_schedule_dimension(
    sigma: float,
    power: float,
    *,
    reference_sigma: float = 0.01,
    reference_dimension: int = 65536,
) -> int:
    width = float(sigma)
    exponent = float(power)
    if width <= 0.0 or exponent <= 0.0:
        raise ValueError("sigma and power must be positive")
    value = float(reference_dimension) * (
        float(reference_sigma) / width
    ) ** exponent
    return max(2, int(math.ceil(value)))


def bulk_square_mesh_power(
    peripheral_size_power: float,
    peripheral_error_power: float,
) -> float:
    r"""Return the sufficient power in ``n sigma^p -> infinity``.

    If ``||Q_sigma||_2=O(sigma^-q)`` and its HS discretization error is
    ``O(n^-1 sigma^-r)``, then the bulk size exponent is ``max(1/2,q)``
    and the bulk error exponent is ``max(3/2,r)``.
    """

    q = float(peripheral_size_power)
    r = float(peripheral_error_power)
    if q < 0.0 or r < 0.0:
        raise ValueError("peripheral powers must be nonnegative")
    return max(0.5, q) + max(1.5, r)


def geometric_section(degree: int, q: complex) -> complex:
    n = int(degree)
    value = complex(q)
    if n < 0:
        raise ValueError("degree must be nonnegative")
    if abs(value - 1.0) < 1.0e-12:
        return complex(n + 1)
    return complex((1.0 - value ** (n + 1)) / (1.0 - value))


def ideal_cloud(
    degree: int, *, determinant_lambda: float = DETERMINISTIC_LAMBDA
) -> np.ndarray:
    n = int(degree)
    if n < 1:
        raise ValueError("degree must be positive")
    angles = np.arange(1, n + 1, dtype=np.float64) * math.pi / (n + 1)
    positive = float(determinant_lambda) ** -0.5 * np.exp(1j * angles)
    return np.concatenate((positive, np.conjugate(positive)))


def square_cloud_determinant(values: np.ndarray, w: complex) -> complex:
    cloud = np.asarray(values, dtype=np.complex128)
    return complex(np.prod(1.0 - complex(w) * cloud * cloud))


def ideal_square_section(
    degree: int,
    w: complex,
    *,
    determinant_lambda: float = DETERMINISTIC_LAMBDA,
) -> complex:
    q = complex(w) / float(determinant_lambda)
    return geometric_section(int(degree), q) ** 2


def universal_squared_profile(s: complex) -> complex:
    value = complex(s)
    if abs(value) < 1.0e-10:
        base = 1.0 + value / 2.0 + value * value / 6.0
    else:
        base = complex(np.expm1(value) / value)
    return base * base


def edge_scaled_square_section(
    degree: int,
    s: complex,
    *,
    determinant_lambda: float = DETERMINISTIC_LAMBDA,
) -> complex:
    n = int(degree)
    if n < 1:
        raise ValueError("degree must be positive")
    q = np.exp(complex(s) / (n + 1))
    return (geometric_section(n, q) / (n + 1)) ** 2


def gaussian_row_asymptotic_constant() -> float:
    r"""Constant in ``||f_sigma-E_h f_sigma|| ~ C h sigma^-3/2``."""

    return 1.0 / (math.sqrt(48.0) * math.pi ** 0.25)
