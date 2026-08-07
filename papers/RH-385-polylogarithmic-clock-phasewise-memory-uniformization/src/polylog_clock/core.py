"""Exact finite reproduction for RH-385.

The certificate checks the finite interpolation, period, Fourier, padding,
and max-plus interfaces used by the paper.  It is deliberately not evidence
for the analytic Davenport estimate or for an asymptotic limit.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import isfinite, isqrt, lcm
from typing import Iterable


TERNARY = (-1, 0, 1)
POINTS = tuple(product(TERNARY, repeat=2))
NONZERO_POINTS = tuple((x, z) for x, z in POINTS if z)
COEFFICIENT_NAMES = ("c01", "c02", "c11", "c12", "c21", "c22")
EXPECTED_C11_HISTOGRAM = {
    "-1": 32,
    "-1/2": 128,
    "0": 192,
    "1/2": 128,
    "1": 32,
}
EXPECTED_CUTOFF_PERIODS = ((2, 4), (3, 36), (5, 900), (7, 44100))
EXPECTED_LEDGER = {
    "fourier_multiplier": 4,
    "tail_multiplier": 13,
    "period_multiplier": 6,
    "padding_multiplier": 4,
}
REPRODUCTION_LABEL = "reproduction_not_analytic_proof"


def _require_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an exact integer")
    return value


def fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    if type(value) is not str:
        raise TypeError("fraction must be serialized as text")
    return Fraction(value)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def payload_sha256(value: object) -> str:
    return sha256(canonical_json(value).encode()).hexdigest()


def exact_equal(left: object, right: object) -> bool:
    """Compare JSON-shaped values without Python's bool/int aliasing."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def truth_values(table_id: int) -> tuple[int, ...]:
    table_id = _require_int(table_id, "table_id")
    if not 0 <= table_id < 512:
        raise ValueError("table_id must lie in [0,512)")
    return tuple(1 if (table_id >> index) & 1 else -1 for index in range(9))


def plus_edges(table_id: int) -> frozenset[tuple[int, int]]:
    values = truth_values(table_id)
    return frozenset(point for point, value in zip(POINTS, values) if value == 1)


def _basis(x: int, z: int) -> tuple[int, ...]:
    return (z, z * z, x * z, x * z * z, x * x * z, x * x * z * z)


def _solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> tuple[Fraction, ...]:
    size = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column]), None)
        if pivot is None:
            raise ArithmeticError("singular interpolation matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return tuple(augmented[row][-1] for row in range(size))


@lru_cache(maxsize=512)
def coefficient_vector(table_id: int) -> tuple[Fraction, ...]:
    values = truth_values(table_id)
    lookup = dict(zip(POINTS, values))
    matrix = [[Fraction(value) for value in _basis(x, z)] for x, z in NONZERO_POINTS]
    rhs = [Fraction(z * lookup[(x, z)]) for x, z in NONZERO_POINTS]
    return _solve(matrix, rhs)


def evaluate_coefficients(coefficients: Iterable[Fraction], x: int, z: int) -> Fraction:
    coeffs = tuple(Fraction(value) for value in coefficients)
    if len(coeffs) != 6:
        raise ValueError("six interpolation coefficients are required")
    return sum((coefficient * basis for coefficient, basis in zip(coeffs, _basis(x, z))), Fraction())


def compatible(left_id: int, right_id: int) -> bool:
    left = plus_edges(left_id)
    right = plus_edges(right_id)
    return not any((z, w) in right for x, z in left for w in TERNARY)


def primorial_square(cutoff: int) -> int:
    cutoff = _require_int(cutoff, "cutoff")
    if cutoff < 2:
        raise ValueError("cutoff must be at least two")
    product_value = 1
    for prime in primes_up_to(cutoff):
        product_value *= prime
    return product_value * product_value


def primes_up_to(limit: int) -> tuple[int, ...]:
    limit = _require_int(limit, "limit")
    if limit < 2:
        return ()
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for candidate in range(2, isqrt(limit) + 1):
        if sieve[candidate]:
            sieve[candidate * candidate : limit + 1 : candidate] = b"\x00" * (
                (limit - candidate * candidate) // candidate + 1
            )
    return tuple(index for index, flag in enumerate(sieve) if flag)


def cutoff_mask(value: int, cutoff: int) -> int:
    value = _require_int(value, "value")
    cutoff = _require_int(cutoff, "cutoff")
    if cutoff < 2:
        raise ValueError("cutoff must be at least two")
    return int(all(value % (prime * prime) for prime in primes_up_to(cutoff)))


def mobius_values(limit: int) -> tuple[int, ...]:
    limit = _require_int(limit, "limit")
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    mu = [1] * (limit + 1)
    prime = [True] * (limit + 1)
    if limit >= 0:
        mu[0] = 0
    if limit >= 1:
        prime[0] = prime[1] = False
    for p in range(2, limit + 1):
        if not prime[p]:
            continue
        for multiple in range(p, limit + 1, p):
            prime[multiple] = False if multiple != p else prime[multiple]
            mu[multiple] *= -1
        square = p * p
        for multiple in range(square, limit + 1, square):
            mu[multiple] = 0
    return tuple(mu)


def _cycle_components(q: int) -> tuple[tuple[int, ...], ...]:
    unseen = set(range(q))
    output: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        cycle: list[int] = []
        phase = start
        while phase not in cycle:
            cycle.append(phase)
            unseen.discard(phase)
            phase = (phase + 2) % q
        output.append(tuple(cycle))
    return tuple(output)


@lru_cache(maxsize=1)
def zero_table_ids() -> tuple[int, ...]:
    return tuple(table_id for table_id in range(512) if coefficient_vector(table_id)[2] == 0)


@lru_cache(maxsize=1)
def _predecessors() -> tuple[tuple[int, ...], ...]:
    states = zero_table_ids()
    return tuple(
        tuple(index for index, left in enumerate(states) if compatible(left, right))
        for right in states
    )


def _component_extreme(
    phases: tuple[int, ...], weights: tuple[tuple[int, ...], ...], maximize: bool
) -> int:
    states = zero_table_ids()
    if len(phases) == 1:
        values = [
            weights[phases[0]][index]
            for index, table_id in enumerate(states)
            if compatible(table_id, table_id)
        ]
        return (max if maximize else min)(values)
    predecessors = _predecessors()
    best_total: int | None = None
    for start_index, start_id in enumerate(states):
        current: dict[int, int] = {start_index: weights[phases[0]][start_index]}
        for phase in phases[1:]:
            next_values: dict[int, int] = {}
            for right_index, possible in enumerate(predecessors):
                candidates = [current[left] for left in possible if left in current]
                if candidates:
                    extreme = (max if maximize else min)(candidates)
                    next_values[right_index] = extreme + weights[phase][right_index]
            current = next_values
        closed = [
            value
            for index, value in current.items()
            if compatible(states[index], start_id)
        ]
        if not closed:
            continue
        candidate = (max if maximize else min)(closed)
        if best_total is None or (candidate > best_total if maximize else candidate < best_total):
            best_total = candidate
    if best_total is None:
        raise RuntimeError("cyclic phase optimizer has no feasible family")
    return best_total


def finite_clock_extrema(limit: int, q: int) -> tuple[int, int]:
    limit = _require_int(limit, "limit")
    q = _require_int(q, "q")
    if limit < 1 or q < 1:
        raise ValueError("positive limit and clock required")
    mu = mobius_values(limit)
    states = zero_table_ids()
    weights = [[0 for _ in states] for _ in range(q)]
    truth = [truth_values(table_id) for table_id in states]
    point_index = {point: index for index, point in enumerate(POINTS)}
    for n in range(1, limit + 1):
        x = mu[n - 2] if n >= 3 else 0
        z = mu[n]
        index = point_index[(x, z)]
        phase = n % q
        for state_index, values in enumerate(truth):
            weights[phase][state_index] += z * values[index]
    frozen = tuple(tuple(row) for row in weights)
    maximum = sum(_component_extreme(component, frozen, True) for component in _cycle_components(q))
    minimum = sum(_component_extreme(component, frozen, False) for component in _cycle_components(q))
    return minimum, maximum


def _complex_dft_q4(values: tuple[int, int, int, int]) -> tuple[tuple[Fraction, Fraction], ...]:
    roots = ((1, 0), (0, -1), (-1, 0), (0, 1))
    output = []
    for frequency in range(4):
        real = 0
        imag = 0
        for residue, value in enumerate(values):
            root_real, root_imag = roots[(frequency * residue) % 4]
            real += value * root_real
            imag += value * root_imag
        output.append((Fraction(real, 4), Fraction(imag, 4)))
    return tuple(output)


def _pure_axis_magnitude(value: tuple[Fraction, Fraction]) -> Fraction:
    real, imag = value
    if real and imag:
        raise ValueError("fixture magnitude is not rational")
    return abs(real or imag)


def _table_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    tables: list[dict[str, object]] = []
    evaluations: list[dict[str, object]] = []
    for table_id in range(512):
        truth = truth_values(table_id)
        coefficients = coefficient_vector(table_id)
        tables.append({
            "table_id": table_id,
            "truth": list(truth),
            "coefficients": [fraction_text(value) for value in coefficients],
            "c11_zero": coefficients[2] == 0,
            "self_compatible": compatible(table_id, table_id),
        })
        for point_index, ((x, z), truth_value) in enumerate(zip(POINTS, truth)):
            expected = Fraction(z * truth_value)
            actual = evaluate_coefficients(coefficients, x, z)
            evaluations.append({
                "table_id": table_id,
                "point_index": point_index,
                "x": x,
                "z": z,
                "expected": fraction_text(expected),
                "actual": fraction_text(actual),
                "pass": actual == expected,
            })
    return tables, evaluations


def _square_mean_rows() -> list[dict[str, object]]:
    rows = []
    for cutoff, period in EXPECTED_CUTOFF_PERIODS:
        one_count = sum(cutoff_mask(residue, cutoff) for residue in range(period))
        pair_count = sum(
            cutoff_mask(residue - 2, cutoff) * cutoff_mask(residue, cutoff)
            for residue in range(period)
        )
        one_formula = Fraction(1)
        pair_formula = Fraction(1)
        for prime in primes_up_to(cutoff):
            one_formula *= Fraction(prime * prime - 1, prime * prime)
            pair_formula *= Fraction(prime * prime - 2, prime * prime)
        rows.append({
            "cutoff": cutoff,
            "period": period,
            "one_count": one_count,
            "one_mean": fraction_text(Fraction(one_count, period)),
            "one_formula": fraction_text(one_formula),
            "pair_count": pair_count,
            "pair_mean": fraction_text(Fraction(pair_count, period)),
            "pair_formula": fraction_text(pair_formula),
            "pass": Fraction(one_count, period) == one_formula
            and Fraction(pair_count, period) == pair_formula,
        })
    return rows


def _tail_fixture(cutoff: int, limit: int) -> dict[str, object]:
    mu = mobius_values(limit)
    differences = [
        index
        for index in range(1, limit + 1)
        if cutoff_mask(index, cutoff) - mu[index] * mu[index] == 1
    ]
    return {
        "cutoff": cutoff,
        "limit": limit,
        "difference_count": len(differences),
        "difference_is_nonnegative": all(
            0 <= cutoff_mask(index, cutoff) - mu[index] * mu[index] <= 1
            for index in range(1, limit + 1)
        ),
        "floor_union_bound_form": "sum_(p>P) floor(X/p^2) <= X*tau_P",
        "finite_tail_coefficients": [1, 1, 2, 4],
        "finite_tail_total": 8,
        "limit_tail_coefficients": [1, 4],
        "limit_tail_total": 5,
        "combined_tail_total": 13,
    }


def build_certificate() -> dict[str, object]:
    tables, evaluations = _table_rows()
    zero_rows = [row for row in tables if row["c11_zero"]]
    histogram = Counter(row["coefficients"][2] for row in tables)
    vector_histogram = Counter(tuple(row["coefficients"]) for row in zero_rows)
    witness = next(
        row
        for row in zero_rows
        if row["coefficients"] == ["1", "0", "0", "0", "-2", "0"]
        and row["self_compatible"]
    )
    dft_values = (-2, -2, 0, -2)
    dft = _complex_dft_q4(dft_values)
    dft_magnitudes = tuple(_pure_axis_magnitude(value) for value in dft)
    triangular_rows = []
    prefix_max = Fraction()
    for q in (1, 2, 3):
        minimum, maximum = finite_clock_extrema(96, q)
        absolute = max(abs(minimum), abs(maximum))
        value = Fraction(absolute, 96)
        prefix_max = max(prefix_max, value)
        triangular_rows.append({
            "N": 96,
            "q": q,
            "minimum_sum": minimum,
            "maximum_sum": maximum,
            "G_N": fraction_text(value),
            "max_over_clocks_up_to_q": fraction_text(prefix_max),
            "state_count": len(zero_rows),
            "diagnostic_only": True,
        })
    certificate = {
        "status": "RH-385_exact_finite_certificate",
        "epistemic_role": REPRODUCTION_LABEL,
        "counts": {
            "truth_tables": len(tables),
            "interpolation_evaluations": len(evaluations),
            "phasewise_c11_zero_tables": len(zero_rows),
            "distinct_zero_score_vectors": len(vector_histogram),
            "cutoff_period_rows": len(EXPECTED_CUTOFF_PERIODS),
            "dft_channels": 3,
            "triangular_clock_rows": len(triangular_rows),
            "mutation_rows": 24,
        },
        "coefficient_contract": {
            "names": list(COEFFICIENT_NAMES),
            "c01_alphabet": [-1, 0, 1],
            "c02_alphabet": [-1, 0, 1],
            "c11_required": 0,
            "c12_alphabet": [-1, 0, 1],
            "c21_alphabet": [-2, -1, 0, 1, 2],
            "c22_alphabet": [-2, -1, 0, 1, 2],
            "c11_histogram": dict(sorted(histogram.items(), key=lambda item: Fraction(item[0]))),
            "zero_vector_multiplicities": [
                {"vector": list(vector), "multiplicity": multiplicity}
                for vector, multiplicity in sorted(vector_histogram.items())
            ],
            "max_zero_vector_l1": 3,
            "max_zero_vector_l2_squared": 5,
            "c21_minus_two_self_compatible_witness": witness["table_id"],
            "witness_plus_edges": [list(edge) for edge in sorted(plus_edges(witness["table_id"]))],
        },
        "truth_tables": tables,
        "interpolation_evaluations": evaluations,
        "period_contract": {
            "periods_are_not_asserted_minimal": True,
            "cutoff_periods": [
                {"P": cutoff, "M_P": period, "pass": primorial_square(cutoff) == period}
                for cutoff, period in EXPECTED_CUTOFF_PERIODS
            ],
            "lcm_fixtures": [
                {"kind": "coprime", "q": 5, "P": 2, "M_P": 4, "Q": 20},
                {"kind": "noncoprime", "q": 6, "P": 3, "M_P": 36, "Q": 36},
                {
                    "kind": "valid_not_minimal",
                    "q": 5,
                    "P": 3,
                    "M_P": 36,
                    "Q": 180,
                    "relevant_mask_minimal_period": 36,
                },
            ],
        },
        "dft_contract": {
            "normalization": "hat_w(a)=Q^-1 sum_r w(r) exp(-2*pi*i*a*r/Q)",
            "parseval": "sum_a |hat_w(a)|^2=Q^-1 sum_r |w(r)|^2",
            "l1_bound": "sum_a |hat_w(a)|<=sqrt(Q)*||w||_infinity",
            "channel_sup_norms": [1, 1, 2],
            "channel_total": 4,
            "c21_factor_two_fixture": {
                "P": 2,
                "q": 1,
                "Q": 4,
                "period_values": list(dft_values),
                "normalized_dft": [
                    {"real": fraction_text(real), "imag": fraction_text(imag)} for real, imag in dft
                ],
                "magnitudes": [fraction_text(value) for value in dft_magnitudes],
                "l1": fraction_text(sum(dft_magnitudes, Fraction())),
                "sqrt_Q": 2,
                "exceeds_sqrt_Q_without_sup_norm": sum(dft_magnitudes, Fraction()) > 2,
                "within_factor_two_bound": sum(dft_magnitudes, Fraction()) <= 4,
            },
        },
        "square_means": _square_mean_rows(),
        "tail_and_padding": {
            "tail_fixture": _tail_fixture(3, 2000),
            "ledger": dict(EXPECTED_LEDGER),
            "ledger_formula": "4*sqrt(Q)*D_*(N)/N+13*tau_P+6*Q/N+4/N",
            "padding_rows": [
                {"channel": "c21", "site": 1, "cost": 2, "reason": "eta_P(-1)=1 but mu_0(-1)=0"},
                {"channel": "c22", "site": 1, "cost": 2, "reason": "eta_P(-1)=1 but mu_0(-1)=0"},
            ],
            "eta_zero": 0,
            "eta_minus_one": 1,
        },
        "small_clock_triangular_dp": triangular_rows,
        "diagonal_sentinel": {
            "first_square_clock": 36,
            "below_36": "no_square_clock_available",
            "never_substitute_q1": True,
        },
        "analytic_firewall": {
            "fixed_B_positive": True,
            "clock_budget": "floor((log N)^B)",
            "davenport_exponent": "choose fixed A>B/2",
            "active_c11": False,
            "polynomial_clock": False,
            "B_may_depend_on_N": False,
            "effective_threshold_claimed": False,
            "adaptive_capacity_limit_claimed": False,
            "projective_selector_claimed": False,
        },
        "all_pass": True,
    }
    verify_certificate(certificate, compare_fresh=False)
    return certificate


def _check_finite(value: object) -> None:
    if type(value) is dict:
        for child in value.values():
            _check_finite(child)
    elif type(value) is list:
        for child in value:
            _check_finite(child)
    elif type(value) is float and not isfinite(value):
        raise ValueError("nonfinite certificate number")


def verify_certificate(certificate: object | None = None, *, compare_fresh: bool = True) -> dict[str, object]:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact Boolean")
    if certificate is None:
        certificate = build_certificate()
        compare_fresh = False
    if type(certificate) is not dict:
        raise TypeError("certificate root must be an object")
    _check_finite(certificate)
    expected_top_level = {
        "status", "epistemic_role", "counts", "coefficient_contract", "truth_tables",
        "interpolation_evaluations", "period_contract", "dft_contract", "square_means",
        "tail_and_padding", "small_clock_triangular_dp", "diagonal_sentinel",
        "analytic_firewall", "all_pass",
    }
    if set(certificate) != expected_top_level:
        raise ValueError("certificate top-level membership failed")
    if certificate.get("status") != "RH-385_exact_finite_certificate":
        raise ValueError("certificate status failed")
    counts = certificate.get("counts")
    expected_counts = {
        "truth_tables": 512,
        "interpolation_evaluations": 4608,
        "phasewise_c11_zero_tables": 192,
        "distinct_zero_score_vectors": 24,
        "cutoff_period_rows": 4,
        "dft_channels": 3,
        "triangular_clock_rows": 3,
        "mutation_rows": 24,
    }
    if not exact_equal(counts, expected_counts):
        raise ValueError("certificate count contract failed")
    if certificate.get("epistemic_role") != REPRODUCTION_LABEL:
        raise ValueError("finite artifact was promoted to analytic proof")
    tables = certificate.get("truth_tables")
    if type(tables) is not list or len(tables) != 512:
        raise ValueError("truth-table rows failed")
    derived_histogram: Counter[str] = Counter()
    derived_vectors: Counter[tuple[str, ...]] = Counter()
    zero_coefficients: list[tuple[Fraction, ...]] = []
    for table_id, row in enumerate(tables):
        coefficients = coefficient_vector(table_id)
        expected = {
            "table_id": table_id,
            "truth": list(truth_values(table_id)),
            "coefficients": [fraction_text(value) for value in coefficients],
            "c11_zero": coefficients[2] == 0,
            "self_compatible": compatible(table_id, table_id),
        }
        if type(row) is not dict or not exact_equal(row, expected):
            raise ValueError("truth-table semantic recomputation failed")
        derived_histogram[fraction_text(coefficients[2])] += 1
        if coefficients[2] == 0:
            derived_vectors[tuple(expected["coefficients"])] += 1
            zero_coefficients.append(coefficients)
    evaluations = certificate.get("interpolation_evaluations")
    if type(evaluations) is not list or len(evaluations) != 4608:
        raise ValueError("interpolation evaluation rows failed")
    evaluation_index = 0
    for table_id in range(512):
        coefficients = coefficient_vector(table_id)
        truth = truth_values(table_id)
        for point_index, ((x, z), truth_value) in enumerate(zip(POINTS, truth)):
            expected_value = Fraction(z * truth_value)
            actual_value = evaluate_coefficients(coefficients, x, z)
            expected_row = {
                "table_id": table_id,
                "point_index": point_index,
                "x": x,
                "z": z,
                "expected": fraction_text(expected_value),
                "actual": fraction_text(actual_value),
                "pass": actual_value == expected_value,
            }
            if not exact_equal(evaluations[evaluation_index], expected_row):
                raise ValueError("interpolation semantic recomputation failed")
            evaluation_index += 1
    contract = certificate.get("coefficient_contract")
    expected_contract_keys = {
        "names", "c01_alphabet", "c02_alphabet", "c11_required", "c12_alphabet",
        "c21_alphabet", "c22_alphabet", "c11_histogram", "zero_vector_multiplicities",
        "max_zero_vector_l1", "max_zero_vector_l2_squared",
        "c21_minus_two_self_compatible_witness", "witness_plus_edges",
    }
    if (
        type(contract) is not dict
        or set(contract) != expected_contract_keys
        or not exact_equal(contract.get("names"), list(COEFFICIENT_NAMES))
        or not exact_equal(contract.get("c11_histogram"), EXPECTED_C11_HISTOGRAM)
        or dict(sorted(derived_histogram.items(), key=lambda item: Fraction(item[0])))
        != EXPECTED_C11_HISTOGRAM
    ):
        raise ValueError("c11 histogram contract failed")
    multiplicities = contract.get("zero_vector_multiplicities")
    if type(multiplicities) is not list or len(multiplicities) != 24:
        raise ValueError("zero vector census failed")
    if any(type(row) is not dict or row.get("multiplicity") != 8 for row in multiplicities):
        raise ValueError("zero vector multiplicity failed")
    expected_multiplicities = [
        {"vector": list(vector), "multiplicity": count}
        for vector, count in sorted(derived_vectors.items())
    ]
    if not exact_equal(multiplicities, expected_multiplicities):
        raise ValueError("zero vector rows differ from exact enumeration")
    alphabets = [sorted({coefficient[index] for coefficient in zero_coefficients}) for index in range(6)]
    expected_alphabets = [
        [Fraction(-1), Fraction(0), Fraction(1)],
        [Fraction(-1), Fraction(0), Fraction(1)],
        [Fraction(0)],
        [Fraction(-1), Fraction(0), Fraction(1)],
        [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)],
        [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)],
    ]
    if alphabets != expected_alphabets:
        raise ValueError("derived coefficient alphabets failed")
    serialized_alphabets = (
        contract.get("c01_alphabet"), contract.get("c02_alphabet"), [contract.get("c11_required")],
        contract.get("c12_alphabet"), contract.get("c21_alphabet"), contract.get("c22_alphabet"),
    )
    if not exact_equal(list(serialized_alphabets), [
        [-1, 0, 1], [-1, 0, 1], [0], [-1, 0, 1],
        [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2],
    ]):
        raise ValueError("serialized coefficient alphabets failed")
    derived_l1 = max(sum(map(abs, vector), Fraction()) for vector in zero_coefficients)
    derived_l2 = max(sum(value * value for value in vector) for vector in zero_coefficients)
    if (
        not exact_equal([
            contract.get("max_zero_vector_l1"), contract.get("max_zero_vector_l2_squared")
        ], [3, 5])
        or derived_l1 != 3
        or derived_l2 != 5
    ):
        raise ValueError("coefficient norm contract failed")
    witness_id = contract.get("c21_minus_two_self_compatible_witness")
    if type(witness_id) is not int or coefficient_vector(witness_id) != (
        Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(-2), Fraction(0)
    ) or not compatible(witness_id, witness_id) or not exact_equal(
        contract.get("witness_plus_edges"), [[0, -1], [0, 1]]
    ):
        raise ValueError("legal c21=-2 witness failed")
    period = certificate.get("period_contract")
    expected_period_rows = [
        {"P": cutoff, "M_P": expected_period, "pass": True}
        for cutoff, expected_period in EXPECTED_CUTOFF_PERIODS
    ]
    expected_lcm_rows = [
        {"kind": "coprime", "q": 5, "P": 2, "M_P": 4, "Q": 20},
        {"kind": "noncoprime", "q": 6, "P": 3, "M_P": 36, "Q": 36},
        {
            "kind": "valid_not_minimal", "q": 5, "P": 3, "M_P": 36, "Q": 180,
            "relevant_mask_minimal_period": 36,
        },
    ]
    expected_period = {
        "periods_are_not_asserted_minimal": True,
        "cutoff_periods": expected_period_rows,
        "lcm_fixtures": expected_lcm_rows,
    }
    if not exact_equal(period, expected_period):
        raise ValueError("period contract semantic recomputation failed")
    lcm_rows = period["lcm_fixtures"]
    for row in lcm_rows:
        if row["Q"] != lcm(row["q"], row["M_P"]):
            raise ValueError("lcm fixture failed")
    dft = certificate.get("dft_contract")
    expected_dft = _complex_dft_q4((-2, -2, 0, -2))
    expected_magnitudes = [_pure_axis_magnitude(value) for value in expected_dft]
    expected_dft_contract = {
        "normalization": "hat_w(a)=Q^-1 sum_r w(r) exp(-2*pi*i*a*r/Q)",
        "parseval": "sum_a |hat_w(a)|^2=Q^-1 sum_r |w(r)|^2",
        "l1_bound": "sum_a |hat_w(a)|<=sqrt(Q)*||w||_infinity",
        "channel_sup_norms": [1, 1, 2],
        "channel_total": 4,
        "c21_factor_two_fixture": {
            "P": 2,
            "q": 1,
            "Q": 4,
            "period_values": [-2, -2, 0, -2],
            "normalized_dft": [
            {"real": fraction_text(real), "imag": fraction_text(imag)}
            for real, imag in expected_dft
            ],
            "magnitudes": [fraction_text(value) for value in expected_magnitudes],
            "l1": fraction_text(sum(expected_magnitudes, Fraction())),
            "sqrt_Q": 2,
            "exceeds_sqrt_Q_without_sup_norm": True,
            "within_factor_two_bound": True,
        },
    }
    if not exact_equal(dft, expected_dft_contract):
        raise ValueError("DFT factor-two fixture failed")
    if not exact_equal(certificate.get("square_means"), _square_mean_rows()):
        raise ValueError("square mean contract failed")
    tail = certificate.get("tail_and_padding")
    expected_tail = {
        "tail_fixture": _tail_fixture(3, 2000),
        "ledger": dict(EXPECTED_LEDGER),
        "ledger_formula": "4*sqrt(Q)*D_*(N)/N+13*tau_P+6*Q/N+4/N",
        "padding_rows": [
            {"channel": "c21", "site": 1, "cost": 2, "reason": "eta_P(-1)=1 but mu_0(-1)=0"},
            {"channel": "c22", "site": 1, "cost": 2, "reason": "eta_P(-1)=1 but mu_0(-1)=0"},
        ],
        "eta_zero": cutoff_mask(0, 2),
        "eta_minus_one": cutoff_mask(-1, 2),
    }
    if not exact_equal(tail, expected_tail):
        raise ValueError("tail and padding semantic recomputation failed")
    triangular = certificate.get("small_clock_triangular_dp")
    if type(triangular) is not list or len(triangular) != 3:
        raise ValueError("triangular DP membership failed")
    prefix_max = Fraction()
    for q, row in enumerate(triangular, start=1):
        minimum, maximum = finite_clock_extrema(96, q)
        value = Fraction(max(abs(minimum), abs(maximum)), 96)
        prefix_max = max(prefix_max, value)
        expected_row = {
            "N": 96,
            "q": q,
            "minimum_sum": minimum,
            "maximum_sum": maximum,
            "G_N": fraction_text(value),
            "max_over_clocks_up_to_q": fraction_text(prefix_max),
            "state_count": 192,
            "diagnostic_only": True,
        }
        if not exact_equal(row, expected_row):
            raise ValueError("triangular DP semantic recomputation failed")
    sentinel = certificate.get("diagonal_sentinel")
    if not exact_equal(sentinel, {
        "first_square_clock": 36,
        "below_36": "no_square_clock_available",
        "never_substitute_q1": True,
    }):
        raise ValueError("empty square-clock sentinel failed")
    firewall = certificate.get("analytic_firewall")
    expected_firewall = {
        "fixed_B_positive": True,
        "clock_budget": "floor((log N)^B)",
        "davenport_exponent": "choose fixed A>B/2",
        "active_c11": False,
        "polynomial_clock": False,
        "B_may_depend_on_N": False,
        "effective_threshold_claimed": False,
        "adaptive_capacity_limit_claimed": False,
        "projective_selector_claimed": False,
    }
    if not exact_equal(firewall, expected_firewall):
        raise ValueError("fixed-B contract failed")
    if certificate.get("all_pass") is not True:
        raise ValueError("certificate pass flag failed")
    if compare_fresh and canonical_json(certificate) != canonical_json(build_certificate()):
        raise ValueError("certificate differs from fresh exact regeneration")
    return certificate


MUTATION_NAMES = (
    "truth_bit", "interpolation_value", "c11_count", "vector_multiplicity",
    "coefficient_norm", "c21_factor_two", "dft_normalization", "wrong_shift",
    "cutoff_period", "lcm_product", "minimal_period_claim", "square_mean",
    "finite_tail", "limit_tail", "padding", "active_c11", "missing_absolute_value",
    "unrestricted_clock", "varying_B", "polynomial_clock", "empty_square_sentinel",
    "effective_threshold", "adaptive_capacity", "artifact_promotion",
)


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if name not in MUTATION_NAMES:
        raise ValueError(f"unknown mutation: {name}")
    value = json.loads(json.dumps(certificate, allow_nan=False))
    if name == "truth_bit":
        value["truth_tables"][0]["truth"][0] *= -1
    elif name == "interpolation_value":
        value["interpolation_evaluations"][0]["actual"] = "0"
    elif name == "c11_count":
        value["counts"]["phasewise_c11_zero_tables"] = 191
    elif name == "vector_multiplicity":
        value["coefficient_contract"]["zero_vector_multiplicities"][0]["multiplicity"] = 7
    elif name == "coefficient_norm":
        value["coefficient_contract"]["max_zero_vector_l2_squared"] = 4
    elif name == "c21_factor_two":
        value["dft_contract"]["channel_sup_norms"][2] = 1
    elif name == "dft_normalization":
        value["dft_contract"]["c21_factor_two_fixture"]["l1"] = "3/4"
    elif name == "wrong_shift":
        value["tail_and_padding"]["eta_minus_one"] = 0
    elif name == "cutoff_period":
        value["period_contract"]["cutoff_periods"][1]["M_P"] = 18
    elif name == "lcm_product":
        value["period_contract"]["lcm_fixtures"][1]["Q"] = 216
    elif name == "minimal_period_claim":
        value["period_contract"]["periods_are_not_asserted_minimal"] = False
    elif name == "square_mean":
        value["square_means"][0]["pass"] = False
    elif name == "finite_tail":
        value["tail_and_padding"]["ledger"]["tail_multiplier"] = 8
    elif name == "limit_tail":
        value["tail_and_padding"]["tail_fixture"]["limit_tail_total"] = 4
    elif name == "padding":
        value["tail_and_padding"]["padding_rows"][0]["cost"] = 0
    elif name == "active_c11":
        value["analytic_firewall"]["active_c11"] = True
    elif name == "missing_absolute_value":
        value["small_clock_triangular_dp"][0]["G_N"] = "0"
    elif name == "unrestricted_clock":
        value["analytic_firewall"]["clock_budget"] = "all q"
    elif name == "varying_B":
        value["analytic_firewall"]["B_may_depend_on_N"] = True
    elif name == "polynomial_clock":
        value["analytic_firewall"]["polynomial_clock"] = True
    elif name == "empty_square_sentinel":
        value["diagonal_sentinel"]["below_36"] = "q_1"
    elif name == "effective_threshold":
        value["analytic_firewall"]["effective_threshold_claimed"] = True
    elif name == "adaptive_capacity":
        value["analytic_firewall"]["adaptive_capacity_limit_claimed"] = True
    elif name == "artifact_promotion":
        value["epistemic_role"] = "analytic_proof"
    return value
