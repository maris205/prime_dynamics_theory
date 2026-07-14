"""Arb-certified operator-norm bounds for the two reduced sectors."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

from flint import arb, arb_mat, arb_series, ctx, fmpz_poly


@dataclass(frozen=True)
class CertifiedBounds:
    decimal_precision: int
    dimension: int
    tail_degree: int
    disk_radius: arb
    cauchy_radius: arb
    u: arb
    r: arb
    lam: arb
    t_norm: arb
    t_cauchy_bound: arb
    tau: arb
    sigma: arb
    beta_one_cauchy_supremum: arb
    beta_two_cauchy_supremum: arb
    beta_one_weight_norm: arb
    beta_one_weight_tail: arb
    beta_two_weight_norm: arb
    beta_two_weight_tail: arb
    beta_one_matrix_norm: arb
    beta_one_matrix_square_norm: arb
    beta_one_matrix_cube_norm: arb
    beta_one_output_tail: arb
    beta_one_high_column_bound: arb
    beta_one_truncation_error: arb
    beta_one_cube_bound: arb
    beta_one_threshold: arb
    beta_one_radius_bound: arb
    beta_two_matrix_norm: arb
    beta_two_matrix_square_norm: arb
    beta_two_output_tail: arb
    beta_two_high_column_bound: arb
    beta_two_truncation_error: arb
    beta_two_square_bound: arb
    beta_two_threshold: arb
    beta_two_radius_bound: arb
    target_radius: arb

    @property
    def beta_one_certified(self) -> bool:
        return self.beta_one_cube_bound < self.beta_one_threshold

    @property
    def beta_two_certified(self) -> bool:
        return self.beta_two_square_bound < self.beta_two_threshold


def algebraic_parameter() -> arb:
    roots = fmpz_poly([-2, 2, -2, 1]).complex_roots()
    real_roots = [root.real for root, multiplicity in roots if root.imag.contains(0)]
    if len(real_roots) != 1:
        raise RuntimeError("failed to isolate the real cubic root")
    u = real_roots[0]
    if not (u > arb(1) and u < arb(2)):
        raise RuntimeError("isolated cubic root is outside (1,2)")
    return u


def _ingredients(cap: int, radius: arb, u: arb) -> tuple[arb_series, ...]:
    ctx.cap = cap
    z = arb_series([arb(0), radius])
    s = ((1 - z) / u).sqrt()
    t = (1 - s) / u
    a = ((1 + s) * (u - 1 + s)).sqrt() / (4 * s)
    b = a / (2 * u**2 * s)
    return s, t, a, b


def _scalar_t(value: arb, u: arb) -> arb:
    return (1 - ((1 - value) / u).sqrt()) / u


def _absolute_upper(value: arb) -> arb:
    return value.abs_upper()


def _matrix_one_norm(matrix: arb_mat) -> arb:
    result = arb(0)
    for column in range(matrix.ncols()):
        column_sum = arb(0)
        for row in range(matrix.nrows()):
            column_sum += _absolute_upper(matrix[row, column])
        result = result.max(column_sum)
    return result.upper()


def _wiener_norm_bound(
    series: arb_series,
    coefficient_count: int,
    cauchy_supremum: arb,
    radius_ratio: arb,
) -> tuple[arb, arb]:
    partial = arb(0)
    for index in range(coefficient_count):
        partial += _absolute_upper(series[index])
    tail = (
        cauchy_supremum
        * radius_ratio**coefficient_count
        / (1 - radius_ratio)
    )
    return (partial + tail).upper(), tail.upper()


def _mean_moment(index: int, r: arb, radius: arb) -> arb:
    if index % 2:
        return arb(0)
    k = index // 2
    return comb(2 * k, k) * (r / (2 * radius)) ** (2 * k)


def _finite_matrices(
    dimension: int,
    cap: int,
    radius: arb,
    u: arb,
) -> tuple[arb_mat, arb_mat]:
    _, t, a, b = _ingredients(cap, radius, u)

    beta_one_rows = [
        [arb(0) for _ in range(dimension)] for _ in range(dimension)
    ]
    beta_two_rows = [
        [arb(0) for _ in range(dimension)] for _ in range(dimension)
    ]

    # Reduced beta=1 coordinates are the scaled Taylor coefficients j=1,...,N.
    # The constant coefficient is eliminated by the exact circle-mean functional.
    for column, input_index in enumerate(range(1, dimension + 1)):
        if input_index % 2:
            continue
        k = input_index // 2
        column_series = 2 * a * (
            t**k / radius**input_index
            - _mean_moment(input_index, u - 1, radius)
        )
        for row, output_index in enumerate(range(1, dimension + 1)):
            beta_one_rows[row][column] = column_series[output_index]

    # Odd beta=2 coordinates use all scaled Taylor coefficients j=0,...,N-1;
    # even input columns vanish under odd branch extraction.
    for input_index in range(dimension):
        if input_index % 2 == 0:
            continue
        k = (input_index - 1) // 2
        column_series = b * t**k / radius**input_index
        for output_index in range(dimension):
            beta_two_rows[output_index][input_index] = column_series[output_index]

    return arb_mat(beta_one_rows), arb_mat(beta_two_rows)


def certify_reduced_gap(
    *,
    decimal_precision: int = 100,
    dimension: int = 50,
    tail_degree: int = 100,
) -> CertifiedBounds:
    if dimension < 10 or dimension % 2:
        raise ValueError("dimension must be an even integer at least ten")
    if tail_degree < dimension + 2:
        raise ValueError("tail_degree must exceed the finite dimension")
    ctx.dps = decimal_precision
    ctx.cap = tail_degree

    radius = arb(7) / 10
    cauchy_radius = arb(9) / 10
    radius_ratio = radius / cauchy_radius
    u = algebraic_parameter()
    r = u - 1
    lam = 2 * u * r

    _, t_series, a_series, b_series = _ingredients(tail_degree, radius, u)
    t_norm = _scalar_t(radius, u).upper()
    t_cauchy = _scalar_t(cauchy_radius, u).upper()
    tau = (t_norm / radius**2).upper()
    sigma = (t_cauchy / radius**2).upper()
    if not tau < 1 or not sigma < 1:
        raise RuntimeError("chosen radii do not give geometric column decay")

    u_lower = u.lower()
    u_upper = u.upper()
    s_min = (((1 - cauchy_radius) / u_upper).sqrt()).lower()
    s_max = (((1 + cauchy_radius) / u_lower).sqrt()).upper()
    a_cauchy = (
        ((u_upper * (1 + s_max) * (1 + t_cauchy)).sqrt())
        / (4 * s_min)
    ).upper()
    b_cauchy = (a_cauchy / (2 * u_lower**2 * s_min)).upper()

    a_norm, a_weight_tail = _wiener_norm_bound(
        a_series, tail_degree, a_cauchy, radius_ratio
    )
    b_norm, b_weight_tail = _wiener_norm_bound(
        b_series, tail_degree, b_cauchy, radius_ratio
    )

    beta_one_matrix, beta_two_matrix = _finite_matrices(
        dimension, tail_degree, radius, u
    )
    beta_one_square = beta_one_matrix * beta_one_matrix
    beta_one_cube = beta_one_square * beta_one_matrix
    beta_two_square = beta_two_matrix * beta_two_matrix

    a_norm_matrix = _matrix_one_norm(beta_one_matrix)
    a_square_norm = _matrix_one_norm(beta_one_square)
    a_cube_norm = _matrix_one_norm(beta_one_cube)
    b_norm_matrix = _matrix_one_norm(beta_two_matrix)
    b_square_norm = _matrix_one_norm(beta_two_square)

    # Finite-rank error: low columns lose only their Cauchy output tail;
    # high columns are bounded by geometric decimation in the Wiener norm.
    cauchy_tail_a = (
        2
        * a_cauchy
        * (sigma + _mean_moment(2, r, radius))
        * radius_ratio ** (dimension + 1)
        / (1 - radius_ratio)
    ).upper()
    first_high_even = dimension + 2
    high_k_a = first_high_even // 2
    high_column_a = (
        2
        * a_norm
        * (
            tau**high_k_a
            + _mean_moment(first_high_even, r, radius)
        )
    ).upper()
    epsilon_a = cauchy_tail_a.max(high_column_a).upper()

    cauchy_tail_b = (
        b_cauchy
        / radius
        * radius_ratio**dimension
        / (1 - radius_ratio)
    ).upper()
    first_high_odd = dimension + 1
    high_k_b = (first_high_odd - 1) // 2
    high_column_b = (
        b_norm / radius * tau**high_k_b
    ).upper()
    epsilon_b = cauchy_tail_b.max(high_column_b).upper()

    beta_one_bound = (
        a_cube_norm
        + epsilon_a * (2 * a_square_norm + a_norm_matrix**2)
        + 3 * a_norm_matrix * epsilon_a**2
        + epsilon_a**3
    ).upper()
    beta_two_bound = (
        b_square_norm
        + 2 * b_norm_matrix * epsilon_b
        + epsilon_b**2
    ).upper()

    result = CertifiedBounds(
        decimal_precision=decimal_precision,
        dimension=dimension,
        tail_degree=tail_degree,
        disk_radius=radius,
        cauchy_radius=cauchy_radius,
        u=u,
        r=r,
        lam=lam,
        t_norm=t_norm,
        t_cauchy_bound=t_cauchy,
        tau=tau,
        sigma=sigma,
        beta_one_cauchy_supremum=a_cauchy,
        beta_two_cauchy_supremum=b_cauchy,
        beta_one_weight_norm=a_norm,
        beta_one_weight_tail=a_weight_tail,
        beta_two_weight_norm=b_norm,
        beta_two_weight_tail=b_weight_tail,
        beta_one_matrix_norm=a_norm_matrix,
        beta_one_matrix_square_norm=a_square_norm,
        beta_one_matrix_cube_norm=a_cube_norm,
        beta_one_output_tail=cauchy_tail_a,
        beta_one_high_column_bound=high_column_a,
        beta_one_truncation_error=epsilon_a,
        beta_one_cube_bound=beta_one_bound,
        beta_one_threshold=(lam ** -6).lower(),
        beta_one_radius_bound=beta_one_bound.root(3).upper(),
        beta_two_matrix_norm=b_norm_matrix,
        beta_two_matrix_square_norm=b_square_norm,
        beta_two_output_tail=cauchy_tail_b,
        beta_two_high_column_bound=high_column_b,
        beta_two_truncation_error=epsilon_b,
        beta_two_square_bound=beta_two_bound,
        beta_two_threshold=(lam ** -4).lower(),
        beta_two_radius_bound=beta_two_bound.sqrt().upper(),
        target_radius=(lam ** -2).lower(),
    )
    if not result.beta_one_certified or not result.beta_two_certified:
        raise RuntimeError("validated bounds did not clear the target thresholds")
    return result
