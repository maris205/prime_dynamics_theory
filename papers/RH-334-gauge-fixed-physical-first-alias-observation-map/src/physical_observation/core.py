"""Exact folding, localization, and coefficient ledgers for RH-334."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

import mpmath as mp


EXPECTED_COEFFICIENT_TYPE = "hardy_full_trace_constituent"


@dataclass(frozen=True)
class CriticalData:
    """Algebraic constants for the band-merging quadratic map."""

    u: mp.mpf
    r: mp.mpf
    lambda_fixed: mp.mpf
    fold_cusp: mp.mpf
    decimal_digits: int


@dataclass(frozen=True)
class PeriodTwoWitness:
    """The exact RH-327 period-two localization counterexample."""

    critical: CriticalData
    x_minus: mp.mpf
    x_plus: mp.mpf
    y_minus: mp.mpf
    cycle_multiplier: mp.mpf
    fixed_weight: mp.mpf
    cycle_weight: mp.mpf


@dataclass(frozen=True)
class FrozenWindows:
    """The RH-327 boundary-owned source/basepoint partition after freezing."""

    sigma: mp.mpf
    radius: mp.mpf
    fold_cusp: mp.mpf
    minus_left: mp.mpf
    plus_right: mp.mpf
    decimal_digits: int

    def classify(self, value: mp.mpf | float) -> str:
        """Return ``J_minus``, ``J_plus``, or ``F`` with fixed endpoints."""

        with mp.workdps(self.decimal_digits):
            value = mp.mpf(value)
            if not 0 <= value <= 1:
                raise ValueError("the folded basepoint must belong to [0,1]")
            if self.minus_left <= value < self.fold_cusp:
                return "J_minus"
            if self.fold_cusp <= value <= self.plus_right:
                return "J_plus"
            return "F"


@lru_cache(maxsize=8)
def critical_data(decimal_digits: int = 110) -> CriticalData:
    """Return the algebraic map constants at controlled working precision."""

    decimal_digits = int(decimal_digits)
    if decimal_digits < 50:
        raise ValueError("decimal_digits must be at least fifty")
    with mp.workdps(decimal_digits):
        u = mp.findroot(
            lambda value: value**3 - 2 * value**2 + 2 * value - 2,
            (mp.mpf("1.5"), mp.mpf("1.6")),
        )
        r = u - 1
        return CriticalData(
            u=+u,
            r=+r,
            lambda_fixed=+(2 * u * r),
            fold_cusp=+(1 / mp.sqrt(u)),
            decimal_digits=decimal_digits,
        )


def deterministic_map(
    value: mp.mpf | float, data: CriticalData | None = None
) -> mp.mpf:
    """Evaluate ``f(x)=1-u_c*x**2``."""

    data = critical_data() if data is None else data
    with mp.workdps(data.decimal_digits):
        value = mp.mpf(value)
        return +(1 - data.u * value**2)


def folded_map(
    value: mp.mpf | float, data: CriticalData | None = None
) -> mp.mpf:
    """Evaluate ``T(y)=|f(y)|`` on the folded interval."""

    data = critical_data() if data is None else data
    with mp.workdps(data.decimal_digits):
        return +abs(deterministic_map(value, data))


def signed_derivative(
    value: mp.mpf | float, data: CriticalData | None = None
) -> mp.mpf:
    """Evaluate ``f'(x)``."""

    data = critical_data() if data is None else data
    with mp.workdps(data.decimal_digits):
        return +(-2 * data.u * mp.mpf(value))


def folded_derivative(
    value: mp.mpf | float, data: CriticalData | None = None
) -> mp.mpf:
    """Evaluate ``T'(y)`` away from the nonperiodic folding cusp."""

    data = critical_data() if data is None else data
    with mp.workdps(data.decimal_digits):
        signed_image = deterministic_map(value, data)
        if abs(signed_image) < mp.power(10, -(data.decimal_digits - 20)):
            raise ValueError("the folded derivative is undefined at the cusp")
        return +(mp.sign(signed_image) * signed_derivative(value, data))


@lru_cache(maxsize=8)
def period_two_witness(decimal_digits: int = 110) -> PeriodTwoWitness:
    """Return the exact negative-point witness and its flat-trace weights."""

    data = critical_data(decimal_digits)
    with mp.workdps(decimal_digits):
        discriminant = mp.sqrt(4 * data.u - 3)
        x_minus = (1 - discriminant) / (2 * data.u)
        x_plus = (1 + discriminant) / (2 * data.u)
        multiplier = -4 * data.r
        return PeriodTwoWitness(
            critical=data,
            x_minus=+x_minus,
            x_plus=+x_plus,
            y_minus=+abs(x_minus),
            cycle_multiplier=+multiplier,
            fixed_weight=+(1 / (data.lambda_fixed**2 - 1)),
            cycle_weight=+(1 / (1 + 4 * data.r)),
        )


def _product(values: list[mp.mpf]) -> mp.mpf:
    return +mp.fprod(values)


def period_two_bijection_rows(decimal_digits: int = 110) -> list[dict[str, mp.mpf]]:
    """Return all three marked points in ``Fix(T**2)`` and their signed lifts."""

    witness = period_two_witness(decimal_digits)
    data = witness.critical
    rows = []
    pairs = (
        (data.r, data.r, witness.fixed_weight),
        (witness.x_plus, witness.x_plus, witness.cycle_weight),
        (witness.y_minus, witness.x_minus, witness.cycle_weight),
    )
    with mp.workdps(decimal_digits):
        for folded_point, signed_point, weight in pairs:
            signed_next = deterministic_map(signed_point, data)
            signed_multiplier = _product(
                [
                    signed_derivative(signed_point, data),
                    signed_derivative(signed_next, data),
                ]
            )
            folded_next = folded_map(folded_point, data)
            folded_multiplier = _product(
                [
                    folded_derivative(folded_point, data),
                    folded_derivative(folded_next, data),
                ]
            )
            rows.append(
                {
                    "folded_point": +folded_point,
                    "signed_lift": +signed_point,
                    "signed_fixed_residual": +abs(
                        deterministic_map(signed_next, data) - signed_point
                    ),
                    "folded_fixed_residual": +abs(
                        folded_map(folded_next, data) - folded_point
                    ),
                    "signed_multiplier": +signed_multiplier,
                    "folded_multiplier": +folded_multiplier,
                    "weight": +weight,
                }
            )
    return rows


def frozen_windows(
    sigma: mp.mpf | float | str = "0.25",
    radius: mp.mpf | float | str = "0.25",
    decimal_digits: int = 110,
) -> FrozenWindows:
    """Freeze the RH-327 windows before any trace or fixed-point evaluation."""

    data = critical_data(decimal_digits)
    with mp.workdps(decimal_digits):
        sigma = mp.mpf(sigma)
        radius = mp.mpf(radius)
        if sigma <= 0 or radius <= 0:
            raise ValueError("sigma and radius must be positive")
        half_width = mp.sqrt(sigma) * radius
        return FrozenWindows(
            sigma=+sigma,
            radius=+radius,
            fold_cusp=+data.fold_cusp,
            minus_left=+max(mp.mpf("0"), data.fold_cusp - half_width),
            plus_right=+min(mp.mpf("1"), data.fold_cusp + half_width),
            decimal_digits=decimal_digits,
        )


def period_two_slot_weights(
    *, corrected: bool, decimal_digits: int = 110
) -> dict[str, mp.mpf]:
    """Return corrected or old positive-``x`` localized deterministic weights."""

    windows = frozen_windows(decimal_digits=decimal_digits)
    rows = period_two_bijection_rows(decimal_digits)
    with mp.workdps(decimal_digits):
        slots = {
            "J_minus": mp.mpf("0"),
            "J_plus": mp.mpf("0"),
            "F": mp.mpf("0"),
        }
        for row in rows:
            signed_point = row["signed_lift"]
            if not corrected and signed_point < 0:
                continue
            slot = windows.classify(row["folded_point"])
            slots[slot] += row["weight"]
        return {key: +value for key, value in slots.items()}


def period_two_total_weight(decimal_digits: int = 110) -> mp.mpf:
    """Return the complete signed physical flat trace at order two."""

    witness = period_two_witness(decimal_digits)
    with mp.workdps(decimal_digits):
        return +(witness.fixed_weight + 2 * witness.cycle_weight)


def validate_localized_weight_partition(
    slots: dict[str, mp.mpf],
    total: mp.mpf,
    *,
    tolerance: mp.mpf | str = "1e-90",
) -> None:
    """Fail closed unless three localized slots recover the full physical sum."""

    if set(slots) != {"J_minus", "J_plus", "F"}:
        raise ValueError("the frozen partition requires exactly three slots")
    with mp.workdps(110):
        if abs(mp.fsum(slots.values()) - total) > mp.mpf(tolerance):
            raise ValueError("localized deterministic slots do not recover P_n")


def _fraction_trace_square(
    matrix: tuple[tuple[Fraction, ...], ...], mask: tuple[bool, ...]
) -> Fraction:
    total = Fraction(0)
    for i, selected in enumerate(mask):
        if selected:
            total += sum(matrix[i][j] * matrix[j][i] for j in range(len(matrix)))
    return total


def exact_block_folding_fixture() -> dict[str, object]:
    """Return an exact rational ``EA/AE`` localized trace-square fixture."""

    row_zero = (Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(2, 5))
    row_one = (Fraction(1, 5), Fraction(1, 10), Fraction(1, 4), Fraction(9, 20))
    signed = (row_zero, row_one, row_zero, row_one)
    folded = (
        (row_zero[0] + row_zero[2], row_zero[1] + row_zero[3]),
        (row_one[0] + row_one[2], row_one[1] + row_one[3]),
    )
    signed_traces = (
        _fraction_trace_square(signed, (True, False, True, False)),
        _fraction_trace_square(signed, (False, True, False, True)),
    )
    folded_traces = (
        _fraction_trace_square(folded, (True, False)),
        _fraction_trace_square(folded, (False, True)),
    )
    return {
        "signed_matrix": signed,
        "folded_matrix": folded,
        "signed_localized_traces": signed_traces,
        "folded_localized_traces": folded_traces,
        "identity_holds": signed_traces == folded_traces,
    }


def _legendre_interval(
    order: int, left: mp.mpf, right: mp.mpf
) -> tuple[list[mp.mpf], list[mp.mpf]]:
    nodes, weights = mp.gauss_quadrature(order, "legendre")
    midpoint = (left + right) / 2
    half_length = (right - left) / 2
    return (
        [+(midpoint + half_length * nodes[index]) for index in range(order)],
        [+(half_length * weights[index]) for index in range(order)],
    )


def _normal_cdf(value: mp.mpf) -> mp.mpf:
    return +(mp.mpf("0.5") * (1 + mp.erf(value / mp.sqrt(2))))


def _signed_gaussian_kernel(
    source: mp.mpf, destination: mp.mpf, sigma: mp.mpf, data: CriticalData
) -> mp.mpf:
    mean = deterministic_map(source, data)
    normalizer = _normal_cdf((1 - mean) / sigma) - _normal_cdf((-1 - mean) / sigma)
    density = mp.exp(-((destination - mean) / sigma) ** 2 / 2) / (
        mp.sqrt(2 * mp.pi) * sigma
    )
    return +(density / normalizer)


def _folded_gaussian_kernel(
    source: mp.mpf, destination: mp.mpf, sigma: mp.mpf, data: CriticalData
) -> mp.mpf:
    return +(
        _signed_gaussian_kernel(source, destination, sigma, data)
        + _signed_gaussian_kernel(source, -destination, sigma, data)
    )


def _trace_square(matrix: list[list[mp.mpf]], mask: list[bool]) -> mp.mpf:
    return +mp.fsum(
        matrix[i][j] * matrix[j][i]
        for i, selected in enumerate(mask)
        if selected
        for j in range(len(matrix))
    )


@lru_cache(maxsize=4)
def finite_nystrom_folding_check(
    order: int = 32, decimal_digits: int = 110
) -> dict[str, object]:
    """Check the localized ``n=2`` folding identity on a symmetric grid.

    This is a deterministic finite Nyström reproduction check, not a
    continuum or interval certificate.
    """

    order = int(order)
    decimal_digits = int(decimal_digits)
    if order < 4 or decimal_digits < 50:
        raise ValueError("order and precision are too small")
    with mp.workdps(decimal_digits):
        data = critical_data(decimal_digits)
        sigma = mp.mpf("0.25")
        windows = frozen_windows(sigma, mp.mpf("0.25"), decimal_digits)
        positive_nodes, positive_weights = _legendre_interval(
            order, mp.mpf("0"), mp.mpf("1")
        )
        signed_nodes = positive_nodes + [-value for value in positive_nodes]
        signed_weights = positive_weights + positive_weights
        signed_matrix = [
            [
                _signed_gaussian_kernel(source, destination, sigma, data)
                * signed_weights[j]
                for j, destination in enumerate(signed_nodes)
            ]
            for source in signed_nodes
        ]
        folded_matrix = [
            [
                _folded_gaussian_kernel(source, destination, sigma, data)
                * positive_weights[j]
                for j, destination in enumerate(positive_nodes)
            ]
            for source in positive_nodes
        ]
        rows = []
        for slot in ("J_minus", "J_plus", "F"):
            signed_mask = [windows.classify(abs(value)) == slot for value in signed_nodes]
            folded_mask = [windows.classify(value) == slot for value in positive_nodes]
            signed_trace = _trace_square(signed_matrix, signed_mask)
            folded_trace = _trace_square(folded_matrix, folded_mask)
            rows.append(
                {
                    "slot": slot,
                    "signed_trace": +signed_trace,
                    "folded_trace": +folded_trace,
                    "absolute_error": +abs(signed_trace - folded_trace),
                }
            )
        return {
            "order": order,
            "decimal_digits": decimal_digits,
            "sigma": sigma,
            "rows": rows,
            "maximum_absolute_error": +max(row["absolute_error"] for row in rows),
            "certification_status": "finite_nystrom_distributive_identity_check_only",
        }


@lru_cache(maxsize=4)
def positive_gauge_shift_check(
    order: int = 16, decimal_digits: int = 110
) -> dict[str, object]:
    """Reproduce the strictly positive noisy trace of the frozen gauge set."""

    order = int(order)
    decimal_digits = int(decimal_digits)
    if order < 4 or decimal_digits < 50:
        raise ValueError("order and precision are too small")
    with mp.workdps(decimal_digits):
        data = critical_data(decimal_digits)
        sigma = mp.mpf("0.25")
        left = data.fold_cusp - mp.mpf("0.1")
        right = data.fold_cusp - mp.mpf("0.08")
        windows = frozen_windows(sigma, mp.mpf("0.25"), decimal_digits)
        if not (
            windows.minus_left <= left < right < windows.fold_cusp
        ):
            raise RuntimeError("the gauge fixture is not contained in J_minus")
        contains_period_two_point = any(
            left <= row["folded_point"] < right
            for row in period_two_bijection_rows(decimal_digits)
        )
        if contains_period_two_point:
            raise RuntimeError("the gauge fixture contains a folded period-two point")
        x_nodes, x_weights = _legendre_interval(order, left, right)
        y_nodes, y_weights = _legendre_interval(order, mp.mpf("0"), mp.mpf("1"))
        localized_trace = mp.fsum(
            wx
            * wy
            * _folded_gaussian_kernel(x, y, sigma, data)
            * _folded_gaussian_kernel(y, x, sigma, data)
            for x, wx in zip(x_nodes, x_weights)
            for y, wy in zip(y_nodes, y_weights)
        )
        hardy_delta = (Fraction(20, 17) ** 2) * Fraction(1, 1)
        scaled_delta = mp.mpf(hardy_delta.numerator) / hardy_delta.denominator * localized_trace
        return {
            "order": order,
            "decimal_digits": decimal_digits,
            "sigma": sigma,
            "left": +left,
            "right": +right,
            "length": +(right - left),
            "localized_trace": +localized_trace,
            "hardy_scaled_delta": +scaled_delta,
            "shift_vector": (-scaled_delta, mp.mpf("0"), +scaled_delta),
            "contained_in_J_minus": True,
            "contains_period_two_point": contains_period_two_point,
            "certification_status": "positive_quadrature_reproduction_only",
        }


def exact_fraction_ledger() -> dict[str, object]:
    """Return the exact rational first-alias fixture in the required type."""

    k = 2
    n = 4
    r_h = Fraction(17, 20)
    localized_noisy = (Fraction(3, 2), Fraction(3, 4), Fraction(1, 4))
    localized_flat = (Fraction(11, 10), Fraction(2, 5), Fraction(1, 5))
    parity_eigenvalue = Fraction(-3, 4)
    counterloop = Fraction(3, 2)
    pole = Fraction(-2, 1)
    scale = r_h ** (-n)
    c_h_sigma = scale * (
        sum(localized_noisy) - 1 - parity_eigenvalue**n
    )
    c_h_deterministic = scale * (sum(localized_flat) - 1 - (-1) ** n)
    numerator_anchor = c_h_deterministic - pole
    q_ft = c_h_sigma - counterloop - numerator_anchor
    localized_slots = tuple(
        scale * (noisy - flat)
        for noisy, flat in zip(localized_noisy, localized_flat)
    )
    parity_packet = scale * ((-1) ** n - parity_eigenvalue**n)
    alias_packet = counterloop - pole
    slot_route = sum(localized_slots) + parity_packet - alias_packet
    head_counterloop_discrepancy = Fraction(5, 12)
    noisy_head = counterloop + head_counterloop_discrepancy
    modulus_complement_minus_anchor = c_h_sigma - noisy_head - numerator_anchor
    return {
        "coefficient_type": EXPECTED_COEFFICIENT_TYPE,
        "k": k,
        "n": n,
        "r_H": r_h,
        "localized_noisy": localized_noisy,
        "localized_flat": localized_flat,
        "lambda_minus": parity_eigenvalue,
        "counterloop": counterloop,
        "pole": pole,
        "c_H_sigma": c_h_sigma,
        "c_H_deterministic": c_h_deterministic,
        "a_num": numerator_anchor,
        "slots": localized_slots,
        "parity_packet": parity_packet,
        "alias_packet": alias_packet,
        "q_FT_direct": q_ft,
        "q_FT_slots": slot_route,
        "q_path_error": q_ft - slot_route,
        "head_counterloop_discrepancy_d": head_counterloop_discrepancy,
        "noisy_head": noisy_head,
        "tau_minus_a": modulus_complement_minus_anchor,
        "tau_relation_error": modulus_complement_minus_anchor
        - (q_ft - head_counterloop_discrepancy),
    }


def validate_coefficient_type(value: str) -> None:
    """Reject coefficient-type substitutions before evaluating a ledger."""

    if value != EXPECTED_COEFFICIENT_TYPE:
        raise ValueError(
            f"expected coefficient_type={EXPECTED_COEFFICIENT_TYPE!r}, got {value!r}"
        )


def fraction_text(value: Fraction) -> str:
    """Serialize one exact rational without converting through binary64."""

    return f"{value.numerator}/{value.denominator}"
