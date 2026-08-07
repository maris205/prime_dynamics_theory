"""Exact finite certificates for the RH-377 mixed-exponent hierarchy.

The calculations in this module reproduce finite algebraic identities.  They
do not supply any asymptotic Mobius correlation theorem.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from itertools import product


MAX_RUN = 8
ENDPOINT = 1 << 18
ROW_LIMITS = (1 << 10, 1 << 16, 1 << 18)
EULER_PRIME_LIMIT = 1 << 20
CHAIN_EPSILON = Fraction(1, 1)
TERNARY = (-1, 0, 1)


def mobius_prefix(limit: int) -> list[int]:
    """Return ``mu(0),...,mu(limit)`` using an exact linear sieve."""

    if type(limit) is not int or limit < 1:
        raise ValueError("limit must be a positive integer")
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
    mu[1] = 1
    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            multiple = value * prime
            if multiple > limit:
                break
            composite[multiple] = True
            if value % prime == 0:
                mu[multiple] = 0
                break
            mu[multiple] = -mu[value]
    return mu


def prime_list(limit: int) -> list[int]:
    """Return all primes at most ``limit`` by a bytearray sieve."""

    if type(limit) is not int or limit < 2:
        raise ValueError("limit must be an integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def mixed_layers(values: tuple[int, ...] | list[int]) -> list[int]:
    """Coefficients of ``prod_j (x_j^2+t*x_j)`` in ascending degree."""

    if not values or len(values) > MAX_RUN:
        raise ValueError("need between one and eight ternary values")
    if any(value not in TERNARY for value in values):
        raise ValueError("values must lie in {-1,0,1}")
    coefficients = [1]
    for value in values:
        updated = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            updated[degree] += coefficient * value * value
            updated[degree + 1] += coefficient * value
        coefficients = updated
    return coefficients


def aggregate_layers(layers: list[int]) -> tuple[int, int]:
    """Return the high even and high odd block sums ``(A_k,B_k)``."""

    k = len(layers) - 1
    if k < 1 or k > MAX_RUN:
        raise ValueError("layers must have degrees zero through k, 1<=k<=8")
    even = sum(layers[degree] for degree in range(2, k + 1, 2))
    odd = sum(layers[degree] for degree in range(3, k + 1, 2))
    return even, odd


def signed_run_indicator(values: tuple[int, ...] | list[int], sigma: int) -> int:
    """Indicator that every value in a window equals ``sigma``."""

    if sigma not in (-1, 1):
        raise ValueError("sigma must be -1 or +1")
    return int(all(value == sigma for value in values))


@lru_cache(maxsize=1)
def boolean_rank_certificate() -> dict[str, object]:
    """Exhaust the ternary identity and compute the formal block-map rank."""

    identity_count = 0
    identity_pass = True
    for k in range(1, MAX_RUN + 1):
        for values in product(TERNARY, repeat=k):
            layers = mixed_layers(values)
            even, odd = aggregate_layers(layers)
            for sigma in (-1, 1):
                identity_count += 1
                right = layers[0] + even + sigma * (layers[1] + odd)
                left = (1 << k) * signed_run_indicator(values, sigma)
                identity_pass = identity_pass and left == right

    coordinates = [
        (k, mask)
        for k in range(2, MAX_RUN + 1)
        for mask in range(1 << k)
        if mask.bit_count() >= 2
    ]
    row_labels = [
        *(f"A_{k}" for k in range(2, MAX_RUN + 1)),
        *(f"B_{k}" for k in range(3, MAX_RUN + 1)),
    ]
    matrix: list[list[Fraction]] = []
    row_supports: list[int] = []
    for label in row_labels:
        parity = 0 if label.startswith("A") else 1
        block_k = int(label.split("_")[1])
        row = [
            Fraction(int(k == block_k and mask.bit_count() % 2 == parity))
            for k, mask in coordinates
        ]
        matrix.append(row)
        row_supports.append(sum(int(value) for value in row))

    rank = _fraction_rank(matrix)
    expected_a_supports = [1, 3, 7, 15, 31, 63, 127]
    expected_b_supports = [1, 4, 11, 26, 57, 120]
    return {
        "boolean_case_count": identity_count,
        "boolean_identity_pass": identity_pass,
        "formal_coordinate_count": len(coordinates),
        "formal_block_count": len(row_labels),
        "formal_rank": rank,
        "formal_kernel_dimension": len(coordinates) - rank,
        "formal_rank_not_arithmetic_minimal": True,
        "row_labels": row_labels,
        "a_row_supports": row_supports[:7],
        "b_row_supports": row_supports[7:],
        "support_counts_pass": (
            row_supports[:7] == expected_a_supports
            and row_supports[7:] == expected_b_supports
        ),
        "all_pass": (
            identity_pass
            and identity_count == 19_680
            and len(coordinates) == 466
            and rank == 13
            and len(coordinates) - rank == 453
            and row_supports[:7] == expected_a_supports
            and row_supports[7:] == expected_b_supports
        ),
    }


def _fraction_rank(matrix: list[list[Fraction]]) -> int:
    """Compute rational rank by exact row reduction."""

    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [value / divisor for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


@lru_cache(maxsize=None)
def transition_probability(
    left: int, middle: int, right: int, epsilon: Fraction = CHAIN_EPSILON
) -> Fraction:
    """Second-order ternary transition from the RH-377 synthetic witness."""

    if any(value not in TERNARY for value in (left, middle, right)):
        raise ValueError("states must lie in {-1,0,1}")
    if not Fraction(0) < abs(epsilon) < Fraction(3, 2):
        raise ValueError("epsilon must satisfy 0<|epsilon|<3/2")
    return Fraction(1, 3) * (
        1 + epsilon * left * middle * (right * right - Fraction(2, 3))
    )


def sequence_probability(
    values: tuple[int, ...], epsilon: Fraction = CHAIN_EPSILON
) -> Fraction:
    """Stationary probability of one finite word under the uniform-pair chain."""

    if not values or any(value not in TERNARY for value in values):
        raise ValueError("need a nonempty ternary word")
    if len(values) == 1:
        return Fraction(1, 3)
    probability = Fraction(1, 9)
    for index in range(2, len(values)):
        probability *= transition_probability(
            values[index - 2], values[index - 1], values[index], epsilon
        )
    return probability


@lru_cache(maxsize=None)
def stationary_moment(
    exponents: tuple[int, ...], epsilon: Fraction = CHAIN_EPSILON
) -> Fraction:
    """Return an exact stationary monomial moment for a consecutive window."""

    if not exponents or any(exponent not in (0, 1, 2) for exponent in exponents):
        raise ValueError("exponents must lie in {0,1,2}")
    if len(exponents) == 1:
        return sum(Fraction(value ** exponents[0], 3) for value in TERNARY)

    pair_weights = {
        (left, middle): Fraction(
            left ** exponents[0] * middle ** exponents[1], 9
        )
        for left, middle in product(TERNARY, repeat=2)
    }
    for exponent in exponents[2:]:
        updated = {(middle, right): Fraction(0) for middle, right in product(TERNARY, repeat=2)}
        for (left, middle), weight in pair_weights.items():
            for right in TERNARY:
                updated[(middle, right)] += (
                    weight
                    * transition_probability(left, middle, right, epsilon)
                    * right**exponent
                )
        pair_weights = updated
    return sum(pair_weights.values())


@lru_cache(maxsize=1)
def countermodel_certificate() -> dict[str, object]:
    """Audit the exact rational stationary-chain countermodel at epsilon=1."""

    epsilon = CHAIN_EPSILON
    transition_count = 0
    transition_rows_pass = True
    for left, middle in product(TERNARY, repeat=2):
        probabilities = [
            transition_probability(left, middle, right, epsilon)
            for right in TERNARY
        ]
        transition_count += len(probabilities)
        transition_rows_pass = transition_rows_pass and (
            sum(probabilities) == 1 and all(value > 0 for value in probabilities)
        )

    stationarity_cells = 0
    stationarity_pass = True
    for middle, right in product(TERNARY, repeat=2):
        incoming = sum(
            Fraction(1, 9)
            * transition_probability(left, middle, right, epsilon)
            for left in TERNARY
        )
        stationarity_cells += 1
        stationarity_pass = stationarity_pass and incoming == Fraction(1, 9)

    raw_cases = 0
    square_cases = 0
    one_sign_cases = 0
    raw_pass = True
    square_pass = True
    one_sign_pass = True
    for k in range(1, MAX_RUN + 1):
        for mask in range(1, 1 << k):
            raw_cases += 1
            raw_exponents = tuple(int(mask >> index & 1) for index in range(k))
            raw_pass = raw_pass and stationary_moment(raw_exponents, epsilon) == 0

            square_cases += 1
            square_exponents = tuple(2 * int(mask >> index & 1) for index in range(k))
            square_pass = square_pass and stationary_moment(
                square_exponents, epsilon
            ) == Fraction(2, 3) ** mask.bit_count()

        for sign_site in range(k):
            other_sites = [index for index in range(k) if index != sign_site]
            for mask in range(1 << len(other_sites)):
                exponents = [0] * k
                exponents[sign_site] = 1
                for bit, site in enumerate(other_sites):
                    if mask >> bit & 1:
                        exponents[site] = 2
                one_sign_cases += 1
                one_sign_pass = one_sign_pass and stationary_moment(
                    tuple(exponents), epsilon
                ) == 0

    directional = {
        "E_A_B_C2": stationary_moment((1, 1, 2), epsilon),
        "E_A_B2_C": stationary_moment((1, 2, 1), epsilon),
        "E_A2_B_C": stationary_moment((2, 1, 1), epsilon),
    }
    triple_probabilities = {
        "plus_plus_plus": sequence_probability((1, 1, 1), epsilon),
        "minus_minus_minus": sequence_probability((-1, -1, -1), epsilon),
    }
    directional_pass = directional == {
        "E_A_B_C2": Fraction(8, 81),
        "E_A_B2_C": Fraction(0),
        "E_A2_B_C": Fraction(0),
    }
    triple_pass = triple_probabilities == {
        "plus_plus_plus": Fraction(4, 81),
        "minus_minus_minus": Fraction(4, 81),
    }
    all_pass = all(
        (
            transition_rows_pass,
            stationarity_pass,
            raw_pass,
            square_pass,
            one_sign_pass,
            directional_pass,
            triple_pass,
            transition_count == 27,
            stationarity_cells == 9,
            raw_cases == 502,
            square_cases == 502,
            one_sign_cases == 1_793,
        )
    )
    return {
        "epsilon": _fraction_json(epsilon),
        "transition_cells": transition_count,
        "transition_rows_pass": transition_rows_pass,
        "stationarity_pair_cells": stationarity_cells,
        "uniform_pair_stationarity_pass": stationarity_pass,
        "distinct_raw_moment_cases": raw_cases,
        "distinct_raw_moments_pass": raw_pass,
        "square_only_moment_cases": square_cases,
        "square_only_iid_moments_pass": square_pass,
        "one_sign_masked_moment_cases": one_sign_cases,
        "one_sign_masked_moments_pass": one_sign_pass,
        "directional_moments": {
            key: _fraction_json(value) for key, value in directional.items()
        },
        "directional_moments_pass": directional_pass,
        "triple_probabilities": {
            key: _fraction_json(value) for key, value in triple_probabilities.items()
        },
        "triple_probabilities_pass": triple_pass,
        "synthetic_not_mobius": True,
        "does_not_match_mobius_squarefree": True,
        "all_pass": all_pass,
    }


def _fraction_json(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def _path_update(state: tuple[int, int], weight: int) -> tuple[int, int]:
    previous_two, previous = state
    return previous, max(previous, previous_two + weight)


def _scaled_channels(
    even_plus: int,
    even_minus: int,
    layers: list[list[int]],
) -> tuple[int, int, int, int]:
    """Return ``256*(P_N,Q_N,U_N,V_N)`` as exact integers."""

    p_scaled = 128 * (even_plus + even_minus)
    q_scaled = 128 * (even_plus - even_minus)
    u_scaled = 0
    v_scaled = 0
    for k in range(1, MAX_RUN + 1):
        sign = 1 if k % 2 else -1
        coefficient = 1 << (MAX_RUN - k)
        even, odd = aggregate_layers(layers[k])
        p_scaled += sign * coefficient * layers[k][0]
        q_scaled += sign * coefficient * layers[k][1]
        u_scaled += sign * coefficient * even
        v_scaled += sign * coefficient * odd
    return p_scaled, q_scaled, u_scaled, v_scaled


@lru_cache(maxsize=1)
def mobius_residual_certificate() -> dict[str, object]:
    """Check every finite hierarchy, path-DP, and two-envelope identity to 2^18."""

    mu = mobius_prefix(ENDPOINT)
    layers = [[0] * (k + 1) for k in range(MAX_RUN + 1)]
    c_plus = [0] * (MAX_RUN + 1)
    c_minus = [0] * (MAX_RUN + 1)
    even_plus = 0
    even_minus = 0
    mobius_sum = 0
    plus_states = {0: (0, 0), 1: (0, 0)}
    minus_states = {0: (0, 0), 1: (0, 0)}
    window_updates = 0
    cumulative_sign_identities = 0
    cumulative_identity_pass = True
    path_capacity_prefixes = 0
    path_capacity_pass = True
    decomposition_pass = True
    envelope_bound_pass = True
    frozen_rows: dict[int, dict[str, object]] = {}

    for limit in range(1, ENDPOINT + 1):
        value = mu[limit]
        mobius_sum += value
        parity = limit % 2
        plus_states[parity] = _path_update(plus_states[parity], value)
        minus_states[parity] = _path_update(minus_states[parity], -value)
        if limit % 4 == 2:
            even_plus += int(value == 1)
            even_minus += int(value == -1)

        for k in range(1, MAX_RUN + 1):
            start = limit - 2 * (k - 1)
            if start >= 1 and start % 2 == 1:
                values = tuple(mu[start : limit + 1 : 2])
                row_layers = mixed_layers(values)
                for degree, coefficient in enumerate(row_layers):
                    layers[k][degree] += coefficient
                c_plus[k] += signed_run_indicator(values, 1)
                c_minus[k] += signed_run_indicator(values, -1)
                window_updates += 1

            even, odd = aggregate_layers(layers[k])
            for sigma, counts in ((1, c_plus), (-1, c_minus)):
                cumulative_sign_identities += 1
                cumulative_identity_pass = cumulative_identity_pass and (
                    (1 << k) * counts[k]
                    == layers[k][0]
                    + even
                    + sigma * (layers[k][1] + odd)
                )

        r_plus = even_plus + sum(
            (1 if k % 2 else -1) * c_plus[k]
            for k in range(1, MAX_RUN + 1)
        )
        r_minus = even_minus + sum(
            (1 if k % 2 else -1) * c_minus[k]
            for k in range(1, MAX_RUN + 1)
        )
        w_plus = plus_states[0][1] + plus_states[1][1]
        w_minus = minus_states[0][1] + minus_states[1][1]
        maximum = -mobius_sum + 2 * w_plus
        minimum = -mobius_sum - 2 * w_minus
        capacity = max(abs(maximum), abs(minimum))
        path_capacity_prefixes += 1
        path_capacity_pass = path_capacity_pass and (
            r_plus == w_plus and r_minus == w_minus
        )

        p_scaled, q_scaled, u_scaled, v_scaled = _scaled_channels(
            even_plus, even_minus, layers
        )
        decomposition_pass = decomposition_pass and (
            256 * r_plus == p_scaled + u_scaled + q_scaled + v_scaled
            and 256 * r_minus == p_scaled + u_scaled - q_scaled - v_scaled
            and 256 * max(r_plus, r_minus)
            == p_scaled + u_scaled + abs(q_scaled + v_scaled)
        )
        residual = abs(
            256 * capacity - 2 * (p_scaled + u_scaled + abs(v_scaled))
        )
        bound = 256 * abs(mobius_sum) + 2 * abs(q_scaled)
        envelope_bound_pass = envelope_bound_pass and residual <= bound

        if limit in ROW_LIMITS:
            frozen_rows[limit] = {
                "P_scaled_256": p_scaled,
                "Q_scaled_256": q_scaled,
                "U_scaled_256": u_scaled,
                "V_scaled_256": v_scaled,
                "M_N": mobius_sum,
                "R_plus": r_plus,
                "R_minus": r_minus,
                "K_N": capacity,
                "capacity_residual_scaled_256": residual,
                "capacity_bound_scaled_256": bound,
                "H0": [layers[k][0] for k in range(1, MAX_RUN + 1)],
                "H1": [layers[k][1] for k in range(1, MAX_RUN + 1)],
                "A": [aggregate_layers(layers[k])[0] for k in range(1, MAX_RUN + 1)],
                "B": [aggregate_layers(layers[k])[1] for k in range(1, MAX_RUN + 1)],
                "C_plus": c_plus[1:],
                "C_minus": c_minus[1:],
            }

    expected_scaled = {
        1024: (64711, 1108, 1465, 44, 3240, 3240),
        65536: (4127474, 3132, 3214, 4932, 2680, 9848),
        262144: (16508741, 4352, 827, 11392, 2560, 14848),
    }
    frozen_rows_pass = all(
        (
            frozen_rows[limit]["P_scaled_256"],
            frozen_rows[limit]["Q_scaled_256"],
            frozen_rows[limit]["U_scaled_256"],
            frozen_rows[limit]["V_scaled_256"],
            frozen_rows[limit]["capacity_residual_scaled_256"],
            frozen_rows[limit]["capacity_bound_scaled_256"],
        )
        == expected
        for limit, expected in expected_scaled.items()
    )
    endpoint_layers_pass = (
        frozen_rows[ENDPOINT]["H0"]
        == [106237, 84569, 65768, 49604, 35783, 24127, 14429, 6449]
        and frozen_rows[ENDPOINT]["H1"]
        == [3, -56, -174, -146, 115, -54, -111, -14]
        and frozen_rows[ENDPOINT]["K_N"] == 129080
    )
    all_pass = all(
        (
            cumulative_identity_pass,
            path_capacity_pass,
            decomposition_pass,
            envelope_bound_pass,
            frozen_rows_pass,
            endpoint_layers_pass,
            window_updates == 1_048_548,
            cumulative_sign_identities == 4_194_304,
            path_capacity_prefixes == ENDPOINT,
        )
    )
    return {
        "label": "finite_exact_reproduction_only_not_asymptotic_evidence",
        "finite_not_asymptotic": True,
        "endpoint": ENDPOINT,
        "odd_start_endpoint": "1<=n<=N-2(k-1), n odd",
        "run_lengths": list(range(1, MAX_RUN + 1)),
        "window_updates": window_updates,
        "cumulative_sign_identity_count": cumulative_sign_identities,
        "cumulative_sign_identities_pass": cumulative_identity_pass,
        "path_capacity_prefix_count": path_capacity_prefixes,
        "path_capacity_pass": path_capacity_pass,
        "exact_channel_decomposition_pass": decomposition_pass,
        "capacity_envelope_bound_pass": envelope_bound_pass,
        "frozen_rows": {str(limit): frozen_rows[limit] for limit in ROW_LIMITS},
        "frozen_rows_pass": frozen_rows_pass,
        "endpoint_layers_pass": endpoint_layers_pass,
        "all_pass": all_pass,
    }


@lru_cache(maxsize=1)
def euler_diagnostic() -> dict[str, object]:
    """Return a deterministic finite Euler-product diagnostic, not a limit proof."""

    primes = prime_list(EULER_PRIME_LIMIT)
    odd_primes = primes[1:]
    with localcontext() as context:
        context.prec = 50
        zeta_partial = Decimal(1)
        for prime in primes:
            square = Decimal(prime * prime)
            zeta_partial *= Decimal(1) - Decimal(1) / square
        e_values: list[Decimal] = []
        for k in range(1, MAX_RUN + 1):
            value = Decimal(1)
            for prime in odd_primes:
                square = Decimal(prime * prime)
                value *= Decimal(1) - Decimal(k) / square
            e_values.append(value)
        conditional = zeta_partial / Decimal(3)
        for k, value in enumerate(e_values, start=1):
            conditional += (Decimal(1) if k % 2 else Decimal(-1)) * value / Decimal(
                1 << k
            )
        conditional_text = f"{conditional:.19f}"
        zeta_text = f"{zeta_partial:.30f}"
        e_text = [f"{value:.30f}" for value in e_values]

    exact_cutoff = 97
    exact_primes = [prime for prime in primes if prime <= exact_cutoff]
    exact_zeta = Fraction(1)
    for prime in exact_primes:
        exact_zeta *= Fraction(prime * prime - 1, prime * prime)
    exact_e: list[Fraction] = []
    for k in range(1, MAX_RUN + 1):
        value = Fraction(1)
        for prime in exact_primes[1:]:
            value *= Fraction(prime * prime - k, prime * prime)
        exact_e.append(value)
    exact_conditional = exact_zeta / 3 + sum(
        (1 if k % 2 else -1) * exact_e[k - 1] / (1 << k)
        for k in range(1, MAX_RUN + 1)
    )

    return {
        "label": "conditional_finite_euler_product_diagnostic_only",
        "prime_cutoff": EULER_PRIME_LIMIT,
        "prime_count": len(primes),
        "odd_prime_count": len(odd_primes),
        "zeta_inverse_partial": zeta_text,
        "odd_prime_e_k_partials": e_text,
        "conditional_capacity_partial": conditional_text,
        "expected_partial": "0.4920202775829839485",
        "decimal_reproduction_pass": conditional_text == "0.4920202775829839485",
        "exact_fraction_checkpoint": {
            "prime_cutoff": exact_cutoff,
            "conditional_numerator": str(exact_conditional.numerator),
            "conditional_denominator": str(exact_conditional.denominator),
        },
        "finite_not_asymptotic": True,
    }


@lru_cache(maxsize=1)
def verify_certificate() -> dict[str, object]:
    """Run every RH-377 exact finite certificate."""

    boolean_rank = boolean_rank_certificate()
    mobius = mobius_residual_certificate()
    countermodel = countermodel_certificate()
    euler = euler_diagnostic()
    all_pass = all(
        (
            boolean_rank["all_pass"],
            mobius["all_pass"],
            countermodel["all_pass"],
            euler["decimal_reproduction_pass"],
        )
    )
    return {
        "boolean_and_formal_rank": boolean_rank,
        "mobius_finite_residual_ledger": mobius,
        "stationary_ternary_countermodel": countermodel,
        "conditional_euler_diagnostic": euler,
        "all_pass": all_pass,
    }
