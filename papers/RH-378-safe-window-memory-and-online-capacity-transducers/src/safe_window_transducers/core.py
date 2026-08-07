"""Exact finite certificates for RH-378.

The routines below certify finite identities and automata statements.  They do
not prove any unproved Mobius correlation limit, a capacity limit, or RH.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


TERNARY = (-1, 0, 1)
SIGNS = (-1, 1)
ENDPOINT = 1 << 20
ROW_LIMITS = (1 << 10, 1 << 16, 1 << 20)
COEFFICIENT_LABELS = ("c01", "c02", "c11", "c12", "c21", "c22")


def mobius_prefix(limit: int) -> list[int]:
    """Return ``mu(0),...,mu(limit)`` by an exact linear sieve."""

    if type(limit) is not int or limit < 1:
        raise ValueError("limit must be a positive integer")
    mu = [0] * (limit + 1)
    composite = bytearray(limit + 1)
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
            composite[multiple] = 1
            if value % prime == 0:
                mu[multiple] = 0
                break
            mu[multiple] = -mu[value]
    return mu


def _fraction_rank(matrix: list[list[Fraction]]) -> int:
    """Exact row rank over the rationals."""

    work = [row[:] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [entry / divisor for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def fraction_text(value: Fraction) -> str:
    """Stable text for an exact rational."""

    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def one_variable_coefficients(values: dict[int, Fraction]) -> tuple[Fraction, ...]:
    """Interpolate a degree-at-most-two function on ``{-1,0,1}``."""

    minus, zero, plus = (values[value] for value in TERNARY)
    return zero, (plus - minus) / 2, (plus + minus) / 2 - zero


def score_coefficients(plus_edges: frozenset[tuple[int, int]]) -> tuple[Fraction, ...]:
    """Interpolate ``z*f(x,z)`` in the frozen six-monomial order."""

    by_x: dict[int, tuple[Fraction, ...]] = {}
    for x in TERNARY:
        by_x[x] = one_variable_coefficients(
            {
                z: Fraction(z * (1 if (x, z) in plus_edges else -1))
                for z in TERNARY
            }
        )
    tensor: dict[tuple[int, int], Fraction] = {}
    for z_degree in range(3):
        x_coefficients = one_variable_coefficients(
            {x: by_x[x][z_degree] for x in TERNARY}
        )
        for x_degree, coefficient in enumerate(x_coefficients):
            tensor[(x_degree, z_degree)] = coefficient
    assert all(tensor[(degree, 0)] == 0 for degree in range(3))
    return tuple(
        tensor[index] for index in ((0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2))
    )


def lag_rule_is_safe(plus_edges: frozenset[tuple[int, int]]) -> bool:
    """No two plus edges may be composable."""

    return not any(
        (x, z) in plus_edges and (z, w) in plus_edges
        for x, z, w in product(TERNARY, repeat=3)
    )


def edge_text(edges: frozenset[tuple[int, int]]) -> list[list[int]]:
    return [list(edge) for edge in sorted(edges)]


@lru_cache(maxsize=1)
def lag_table_certificate() -> dict[str, object]:
    """Enumerate all lag-two tables and certify the 13 safe tables."""

    edges = tuple(product(TERNARY, repeat=2))
    safe_tables: list[frozenset[tuple[int, int]]] = []
    for mask in range(1 << len(edges)):
        plus = frozenset(edge for index, edge in enumerate(edges) if mask >> index & 1)
        if lag_rule_is_safe(plus):
            safe_tables.append(plus)

    size_histogram = Counter(len(table) for table in safe_tables)
    in_stars = 0
    out_stars = 0
    for table in safe_tables:
        if len(table) == 2:
            if len({right for _, right in table}) == 1:
                in_stars += 1
            if len({left for left, _ in table}) == 1:
                out_stars += 1

    coefficient_rows = [score_coefficients(table) for table in safe_tables]
    rank = _fraction_rank([list(row) for row in coefficient_rows])
    relation_pass = all(row[5] == -row[1] - row[2] for row in coefficient_rows)
    coefficient_histogram = Counter(coefficient_rows)
    multiplicities = sorted(coefficient_histogram.values())
    ab_histogram = Counter((row[1], row[2]) for row in coefficient_rows)

    unconditional_witness = frozenset({(0, 1)})
    conditional_witness = frozenset({(-1, 1), (0, 1)})
    table_rows = [
        {
            "plus_edges": edge_text(table),
            "coefficients": [fraction_text(value) for value in row],
            "c02": fraction_text(row[1]),
            "c11": fraction_text(row[2]),
        }
        for table, row in zip(safe_tables, coefficient_rows)
    ]
    expected_ab = {
        (Fraction(0), Fraction(0)): 5,
        (Fraction(0), Fraction(-1, 2)): 2,
        (Fraction(0), Fraction(1, 2)): 2,
        (Fraction(-1), Fraction(0)): 1,
        (Fraction(1), Fraction(0)): 1,
        (Fraction(1), Fraction(-1, 2)): 1,
        (Fraction(-1), Fraction(1, 2)): 1,
    }
    return {
        "total_table_count": 512,
        "safe_table_count": len(safe_tables),
        "safe_size_histogram": {str(key): size_histogram[key] for key in sorted(size_histogram)},
        "two_edge_in_star_count": in_stars,
        "two_edge_out_star_count": out_stars,
        "coefficient_order": list(COEFFICIENT_LABELS),
        "coefficient_rank": rank,
        "unique_linear_relation": "c22=-c02-c11",
        "relation_pass": relation_pass,
        "distinct_coefficient_vector_count": len(coefficient_histogram),
        "coefficient_vector_multiplicities": multiplicities,
        "coefficient_multiplicity_histogram": {
            str(key): Counter(multiplicities)[key] for key in sorted(set(multiplicities))
        },
        "ab_multiplicities": [
            {"c02": fraction_text(pair[0]), "c11": fraction_text(pair[1]), "count": count}
            for pair, count in sorted(ab_histogram.items())
        ],
        "c11_zero_count": sum(row[2] == 0 for row in coefficient_rows),
        "c11_nonzero_count": sum(row[2] != 0 for row in coefficient_rows),
        "unconditional_witness": edge_text(unconditional_witness),
        "unconditional_witness_coefficients": [
            fraction_text(value) for value in score_coefficients(unconditional_witness)
        ],
        "conditional_witness": edge_text(conditional_witness),
        "conditional_witness_coefficients": [
            fraction_text(value) for value in score_coefficients(conditional_witness)
        ],
        "tables": table_rows,
        "all_pass": (
            len(safe_tables) == 13
            and size_histogram == Counter({1: 6, 2: 6, 0: 1})
            and in_stars == 3
            and out_stars == 3
            and rank == 5
            and relation_pass
            and multiplicities == [1, 1, 1, 1, 1, 2, 2, 4]
            and ab_histogram == expected_ab
            and score_coefficients(unconditional_witness) == (0, 1, 0, 0, -1, -1)
            and score_coefficients(conditional_witness)
            == (0, 1, Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2))
        ),
    }


def window_safety_cases(
    table: dict[tuple[int, tuple[int, ...]], int], q: int, ell: int
) -> tuple[bool, int]:
    """Check all compatible length-``ell+2`` blocks for a periodic table."""

    if type(q) is not int or q < 1 or type(ell) is not int or ell < 1:
        raise ValueError("q and ell must be positive integers")
    expected_keys = {
        (phase, window)
        for phase in range(q)
        for window in product(TERNARY, repeat=ell)
    }
    if set(table) != expected_keys or any(value not in SIGNS for value in table.values()):
        raise ValueError("table must be a complete {-1,+1}-valued q-periodic ell-window table")
    checked = 0
    safe = True
    for phase in range(q):
        for block in product(TERNARY, repeat=ell + 2):
            checked += 1
            first = table[(phase, tuple(block[:ell]))]
            second = table[((phase + 2) % q, tuple(block[2:]))]
            safe = safe and not (first == second == 1)
    return safe, checked


def lag_graph_lift_table(plus_edges: frozenset[tuple[int, int]]) -> dict[tuple[int, tuple[int, ...]], int]:
    """Represent a lag-two rule as an ell=3 window table ignoring the middle."""

    return {
        (0, tuple(window)): 1 if (window[0], window[2]) in plus_edges else -1
        for window in product(TERNARY, repeat=3)
    }


@lru_cache(maxsize=1)
def graph_lift_certificate() -> dict[str, object]:
    witnesses = (
        ("unconditional", frozenset({(0, 1)})),
        ("conditional", frozenset({(-1, 1), (0, 1)})),
    )
    rows = []
    for name, edges in witnesses:
        safe, cases = window_safety_cases(lag_graph_lift_table(edges), q=1, ell=3)
        rows.append({"name": name, "plus_edges": edge_text(edges), "cases": cases, "safe": safe})
    return {
        "witness_count": len(rows),
        "cases_per_witness": 243,
        "total_cases": sum(row["cases"] for row in rows),
        "rows": rows,
        "all_pass": all(row["safe"] and row["cases"] == 243 for row in rows),
    }


def current_zero_basis_dimension(q: int, ell: int) -> int:
    """Dimension of current-zero score functions on a q-periodic ell-window."""

    if type(q) is not int or q < 1 or type(ell) is not int or ell < 1:
        raise ValueError("q and ell must be positive integers")
    return 2 * q * 3 ** (ell - 1)


def greedy_step(state: tuple[int, int], symbol: int, sigma: int) -> tuple[int, tuple[int, int]]:
    """One step of the frozen orientation transducer."""

    if state not in tuple(product(SIGNS, repeat=2)) or symbol not in TERNARY or sigma not in SIGNS:
        raise ValueError("invalid transducer argument")
    previous_one, previous_two = state
    output = 1 if symbol == sigma and previous_two == -1 else -1
    return output, (output, previous_one)


def greedy_outputs(values: tuple[int, ...] | list[int], sigma: int) -> tuple[list[int], int]:
    state = (-1, -1)
    outputs: list[int] = []
    score = 0
    for symbol in values:
        output, state = greedy_step(state, symbol, sigma)
        outputs.append(output)
        score += symbol * output
    return outputs, score


def independent_extrema(values: tuple[int, ...] | list[int]) -> tuple[int, int]:
    """Independent four-state DP for distance-two safe signs."""

    states = {(-1, -1): (0, 0)}
    for symbol in values:
        updated: dict[tuple[int, int], tuple[int, int]] = {}
        for (previous_one, previous_two), (maximum, minimum) in states.items():
            for output in SIGNS:
                if previous_two == output == 1:
                    continue
                state = (output, previous_one)
                candidate_max = maximum + symbol * output
                candidate_min = minimum + symbol * output
                if state not in updated:
                    updated[state] = (candidate_max, candidate_min)
                else:
                    old_max, old_min = updated[state]
                    updated[state] = (max(old_max, candidate_max), min(old_min, candidate_min))
        states = updated
    return max(pair[0] for pair in states.values()), min(pair[1] for pair in states.values())


@lru_cache(maxsize=1)
def mealy_certificate() -> dict[str, object]:
    safety_cases = 0
    safety_pass = True
    for sigma, state, first_symbol, second_symbol in product(
        SIGNS, product(SIGNS, repeat=2), TERNARY, TERNARY
    ):
        first, state_one = greedy_step(state, first_symbol, sigma)
        second, _ = greedy_step(state_one, second_symbol, sigma)
        safety_cases += 1
        safety_pass = safety_pass and not (state[0] == second == 1)
        safety_pass = safety_pass and not (state[1] == first == 1)

    reachability: dict[str, list[list[int]]] = {}
    distinguishable_count = 0
    for sigma in SIGNS:
        reachable = {(-1, -1)}
        frontier = {(-1, -1)}
        while frontier:
            new_frontier = set()
            for state in frontier:
                for symbol in TERNARY:
                    _, target = greedy_step(state, symbol, sigma)
                    if target not in reachable:
                        reachable.add(target)
                        new_frontier.add(target)
            frontier = new_frontier
        reachability[str(sigma)] = [list(state) for state in sorted(reachable)]
        for left, right in combinations(sorted(reachable), 2):
            separated = False
            for length in (1, 2):
                for suffix in product(TERNARY, repeat=length):
                    left_state, right_state = left, right
                    left_word: list[int] = []
                    right_word: list[int] = []
                    for symbol in suffix:
                        out_left, left_state = greedy_step(left_state, symbol, sigma)
                        out_right, right_state = greedy_step(right_state, symbol, sigma)
                        left_word.append(out_left)
                        right_word.append(out_right)
                    if left_word != right_word:
                        separated = True
                        break
                if separated:
                    break
            distinguishable_count += int(separated)
            safety_pass = safety_pass and separated

    return {
        "safety_case_count": safety_cases,
        "safety_pass": safety_pass,
        "reachable_states": reachability,
        "reachable_state_count_per_orientation": [len(reachability[str(sigma)]) for sigma in SIGNS],
        "pairwise_distinguishability_cases": distinguishable_count,
        "exact_output_state_minimum": 4,
        "minimality_scope": "exact output realization of one frozen orientation transducer",
        "all_pass": safety_cases == 72 and safety_pass and distinguishable_count == 12,
    }


@lru_cache(maxsize=1)
def exhaustive_extrema_certificate() -> dict[str, object]:
    word_count = 0
    equality_count = 0
    all_pass = True
    by_length = []
    for length in range(1, 11):
        count = 0
        for word in product(TERNARY, repeat=length):
            count += 1
            word_count += 1
            maximum, minimum = independent_extrema(word)
            plus_score = greedy_outputs(word, 1)[1]
            minus_score = greedy_outputs(word, -1)[1]
            equality_count += 2
            all_pass = all_pass and plus_score == maximum and minus_score == minimum
        by_length.append({"length": length, "word_count": count})
    return {
        "maximum_length": 10,
        "word_count": word_count,
        "extrema_equality_count": equality_count,
        "by_length": by_length,
        "all_pass": all_pass and word_count == 88_572 and equality_count == 177_144,
    }


@lru_cache(maxsize=None)
def _word_capacity(word: tuple[int, ...]) -> int:
    maximum, minimum = independent_extrema(word)
    return max(abs(maximum), abs(minimum))


def causal_policy_count(horizon: int) -> int:
    """Count safe deterministic causal policy trees attaining K at every node."""

    if type(horizon) is not int or horizon < 0:
        raise ValueError("horizon must be a nonnegative integer")

    @lru_cache(maxsize=None)
    def recurse(word: tuple[int, ...], state: tuple[int, int], score: int) -> int:
        if len(word) == horizon:
            return 1
        branch_product = 1
        for symbol in TERNARY:
            next_word = word + (symbol,)
            branch_sum = 0
            for output in SIGNS:
                if state[1] == output == 1:
                    continue
                next_score = score + symbol * output
                if abs(next_score) != _word_capacity(next_word):
                    continue
                branch_sum += recurse(next_word, (output, state[0]), next_score)
            branch_product *= branch_sum
        return branch_product

    return recurse((), (-1, -1), 0)


@lru_cache(maxsize=1)
def online_obstruction_certificate() -> dict[str, object]:
    counts = [causal_policy_count(horizon) for horizon in range(1, 5)]
    plus_branch = (1, -1, 1)
    minus_branch = (1, -1, -1, -1)
    plus_capacities = [_word_capacity(plus_branch[:length]) for length in range(1, 4)]
    minus_capacities = [_word_capacity(minus_branch[:length]) for length in range(1, 5)]
    plus_outputs = (1, -1, -1)
    minus_outputs = (-1, 1, 1, -1)

    def forced_choice_rows(
        word: tuple[int, ...], first_output: int
    ) -> list[dict[str, object]]:
        score = word[0] * first_output
        state = (first_output, -1)
        rows: list[dict[str, object]] = []
        for index in range(1, len(word)):
            symbol = word[index]
            choices = [
                output
                for output in SIGNS
                if not (state[1] == output == 1)
                and abs(score + symbol * output) == _word_capacity(word[: index + 1])
            ]
            rows.append(
                {
                    "prefix_length": index + 1,
                    "safe_prefix_optimal_choices": choices,
                }
            )
            if not choices:
                break
            if len(choices) != 1:
                raise AssertionError("adversarial branch did not force a unique continuation")
            output = choices[0]
            score += symbol * output
            state = (output, state[0])
        return rows

    def prefix_scores(word: tuple[int, ...], outputs: tuple[int, ...]) -> list[int]:
        score = 0
        scores: list[int] = []
        for symbol, output in zip(word, outputs):
            score += symbol * output
            scores.append(score)
        return scores

    def outputs_are_safe(outputs: tuple[int, ...]) -> bool:
        return all(
            not (outputs[index] == outputs[index + 2] == 1)
            for index in range(len(outputs) - 2)
        )

    plus_scores = prefix_scores(plus_branch, plus_outputs)
    minus_scores = prefix_scores(minus_branch, minus_outputs)
    plus_choice_rows = forced_choice_rows(plus_branch, 1)
    minus_choice_rows = forced_choice_rows(minus_branch, -1)
    branch_pass = (
        outputs_are_safe(plus_outputs)
        and outputs_are_safe(minus_outputs)
        and plus_scores == [1, 2, 1]
        and plus_capacities == [1, 2, 3]
        and minus_scores == [-1, -2, -3, -2]
        and minus_capacities == [1, 2, 3, 4]
        and plus_choice_rows
        == [
            {"prefix_length": 2, "safe_prefix_optimal_choices": [-1]},
            {"prefix_length": 3, "safe_prefix_optimal_choices": []},
        ]
        and minus_choice_rows
        == [
            {"prefix_length": 2, "safe_prefix_optimal_choices": [1]},
            {"prefix_length": 3, "safe_prefix_optimal_choices": [1]},
            {"prefix_length": 4, "safe_prefix_optimal_choices": []},
        ]
    )
    return {
        "policy_tree_counts": [
            {"horizon": horizon, "count": count}
            for horizon, count in enumerate(counts, start=1)
        ],
        "maximum_universal_horizon": 3,
        "first_zero_horizon": 4,
        "adversarial_first_symbol": 1,
        "if_first_output_plus_extension": list(plus_branch[1:]),
        "if_first_output_plus_forced_outputs": list(plus_outputs),
        "if_first_output_plus_scores": plus_scores,
        "if_first_output_plus_prefix_capacities": plus_capacities,
        "if_first_output_plus_choice_rows": plus_choice_rows,
        "if_first_output_minus_extension": list(minus_branch[1:]),
        "if_first_output_minus_forced_outputs": list(minus_outputs),
        "if_first_output_minus_scores": minus_scores,
        "if_first_output_minus_prefix_capacities": minus_capacities,
        "if_first_output_minus_choice_rows": minus_choice_rows,
        "adversarial_branch_replay_pass": branch_pass,
        "scope": "single deterministic causal universally safe policy attaining absolute K on every input prefix",
        "all_pass": counts == [8, 256, 65_536, 0] and branch_pass,
    }


def truncated_output(values: tuple[int, ...] | list[int], index: int, sigma: int) -> int:
    """The ell=15 alternating-product output at one zero-based index."""

    if sigma not in SIGNS or index < 0 or index >= len(values):
        raise ValueError("invalid truncated-output argument")
    alternating_sum = 0
    product_indicator = 1
    for k in range(1, 9):
        position = index - 2 * (k - 1)
        product_indicator *= int(position >= 0 and values[position] == sigma)
        alternating_sum += (1 if k % 2 else -1) * product_indicator
    if alternating_sum not in (0, 1):
        raise AssertionError("alternating indicator left {0,1}")
    return 2 * alternating_sum - 1


def truncated_outputs(values: tuple[int, ...] | list[int], sigma: int) -> list[int]:
    return [truncated_output(values, index, sigma) for index in range(len(values))]


@lru_cache(maxsize=1)
def truncated_window_certificate() -> dict[str, object]:
    binary_cases = 0
    binary_safety_pass = True
    run_behavior_pass = True
    for parity_word in product((0, 1), repeat=9):
        binary_cases += 1
        embedded = tuple(
            parity_word[index // 2] if index % 2 == 0 else 0
            for index in range(17)
        )
        output_at_fifteen = truncated_output(embedded, 14, 1)
        output_at_seventeen = truncated_output(embedded, 16, 1)
        binary_safety_pass = binary_safety_pass and not (
            output_at_fifteen == output_at_seventeen == 1
        )
    for run_length in range(10):
        word = [0] * 17
        for index in range(16, max(-1, 16 - 2 * run_length), -2):
            word[index] = 1
        observed = truncated_output(word, 16, 1)
        expected = 1 if run_length in (1, 3, 5, 7) else -1
        run_behavior_pass = run_behavior_pass and observed == expected

    counterexample = tuple(1 if index % 2 == 0 else 0 for index in range(17))
    recursive = greedy_outputs(counterexample, 1)[0]
    truncated = truncated_outputs(counterexample, 1)
    same_parity_recursive = recursive[::2]
    same_parity_truncated = truncated[::2]
    first_difference = next(
        index for index, (left, right) in enumerate(zip(recursive, truncated), start=1) if left != right
    )
    run_seven_word = tuple(1 if index in range(2, 15, 2) else 0 for index in range(15))
    run_eight_word = (1,) + run_seven_word[1:]
    narrow_windows_equal = run_seven_word[-14:] == run_eight_word[-14:]
    narrow_outputs = [
        greedy_outputs(word, 1)[0][-1] for word in (run_seven_word, run_eight_word)
    ]
    return {
        "window_length": 15,
        "alternating_product_depth": 8,
        "binary_same_parity_case_count": binary_cases,
        "binary_safety_pass": binary_safety_pass,
        "run_behavior_pass": run_behavior_pass,
        "synthetic_prefix_length": len(counterexample),
        "same_parity_sigma_site_count": sum(counterexample),
        "first_integer_index_of_divergence": first_difference,
        "same_parity_recursive_outputs": same_parity_recursive,
        "same_parity_window_outputs": same_parity_truncated,
        "not_nine_consecutive_integers": True,
        "narrow_stateless_minimality": {
            "input_class": "all same-parity sigma-runs have length at most eight",
            "run_lengths": [7, 8],
            "last_fourteen_symbols_equal": narrow_windows_equal,
            "greedy_current_outputs": narrow_outputs,
            "minimum_contiguous_window_length": 15,
            "scope": "q=1 causal contiguous stateless exact-stream realization",
        },
        "all_pass": (
            binary_cases == 512
            and binary_safety_pass
            and run_behavior_pass
            and same_parity_recursive == [1, -1, 1, -1, 1, -1, 1, -1, 1]
            and same_parity_truncated == [1, -1, 1, -1, 1, -1, 1, -1, -1]
            and first_difference == 17
            and narrow_windows_equal
            and narrow_outputs == [1, -1]
        ),
    }


def _lag_score(value: int, lag: int, edges: frozenset[tuple[int, int]]) -> int:
    return value * (1 if (lag, value) in edges else -1)


@lru_cache(maxsize=1)
def mobius_certificate() -> dict[str, object]:
    """Stream every prefix through both machines and the two lag witnesses."""

    mu = mobius_prefix(ENDPOINT)
    states = {sigma: (-1, -1) for sigma in SIGNS}
    scores = {sigma: 0 for sigma in SIGNS}
    dp_states = {(-1, -1): (0, 0)}
    prefix_equalities = 0
    recursive_window_equalities = 0
    no_nine_run = {sigma: True for sigma in SIGNS}
    parity_runs = {(sigma, parity): 0 for sigma in SIGNS for parity in (0, 1)}

    M = Q1 = D2 = U2 = V2 = Q2 = S0 = Sh = 0
    lag_ledger_prefix_count = 0
    lag_ledger_pass = True
    unconditional = frozenset({(0, 1)})
    conditional = frozenset({(-1, 1), (0, 1)})
    rows = []

    for n in range(1, ENDPOINT + 1):
        value = mu[n]
        M += value
        Q1 += value * value
        if n >= 3:
            left = mu[n - 2]
            D2 += left * value
            U2 += left * value * value
            V2 += left * left * value
            Q2 += left * left * value * value
        lag = mu[n - 2] if n >= 3 else 0
        S0 += _lag_score(value, lag, unconditional)
        Sh += _lag_score(value, lag, conditional)
        lag_ledger_prefix_count += 1
        lag_ledger_pass = lag_ledger_pass and (
            S0 == Q1 - V2 - Q2
            and 2 * Sh == 2 * Q1 - D2 - U2 - V2 - Q2
        )

        updated_dp: dict[tuple[int, int], tuple[int, int]] = {}
        for (previous_one, previous_two), (maximum, minimum) in dp_states.items():
            for output in SIGNS:
                if previous_two == output == 1:
                    continue
                target = (output, previous_one)
                candidate = (maximum + value * output, minimum + value * output)
                if target not in updated_dp:
                    updated_dp[target] = candidate
                else:
                    old_maximum, old_minimum = updated_dp[target]
                    updated_dp[target] = (
                        max(old_maximum, candidate[0]),
                        min(old_minimum, candidate[1]),
                    )
        dp_states = updated_dp
        maximum = max(pair[0] for pair in dp_states.values())
        minimum = min(pair[1] for pair in dp_states.values())

        for sigma in SIGNS:
            output, states[sigma] = greedy_step(states[sigma], value, sigma)
            scores[sigma] += value * output
            target = minimum if sigma == -1 else maximum
            if scores[sigma] != target:
                raise AssertionError(f"prefix extremum mismatch at n={n}, sigma={sigma}")
            prefix_equalities += 1

            parity = n % 2
            if value == sigma:
                parity_runs[(sigma, parity)] += 1
            else:
                parity_runs[(sigma, parity)] = 0
            no_nine_run[sigma] = no_nine_run[sigma] and parity_runs[(sigma, parity)] <= 8
            # ``mu`` is one-indexed; construct the same formula directly.
            alternating_sum = 0
            indicator = 1
            for k in range(1, 9):
                position = n - 2 * (k - 1)
                indicator *= int(position >= 1 and mu[position] == sigma)
                alternating_sum += (1 if k % 2 else -1) * indicator
            window_output = 2 * alternating_sum - 1
            if window_output != output:
                raise AssertionError(f"Mobius ell=15 mismatch at n={n}, sigma={sigma}")
            recursive_window_equalities += 1

        if n in ROW_LIMITS:
            rows.append(
                {
                    "N": n,
                    "M": M,
                    "Q1": Q1,
                    "D2": D2,
                    "U2": U2,
                    "V2": V2,
                    "Q2": Q2,
                    "S0": S0,
                    "Sh": Sh,
                    "Smax": scores[1],
                    "Smin": scores[-1],
                    "K": max(abs(scores[1]), abs(scores[-1])),
                }
            )

    expected_rows = [
        {"N": 1024, "M": -4, "Q1": 624, "D2": -34, "U2": -18, "V2": -14, "Q2": 330, "S0": 308, "Sh": 492, "Smax": 530, "Smin": -504, "K": 530},
        {"N": 65536, "M": 14, "Q1": 39844, "D2": 33, "U2": -51, "V2": 35, "Q2": 21155, "S0": 18654, "Sh": 29258, "Smax": 32320, "Smin": -32222, "K": 32320},
        {"N": 1048576, "M": 257, "Q1": 637461, "D2": -382, "U2": 130, "V2": 438, "Q2": 338334, "S0": 298689, "Sh": 468201, "Smax": 515983, "Smin": -516163, "K": 516163},
    ]
    ledger_pass = all(
        row["S0"] == row["Q1"] - row["V2"] - row["Q2"]
        and 2 * row["Sh"]
        == 2 * row["Q1"] - row["D2"] - row["U2"] - row["V2"] - row["Q2"]
        for row in rows
    )
    return {
        "endpoint": ENDPOINT,
        "prefix_extrema_equality_count": prefix_equalities,
        "recursive_window_equality_count": recursive_window_equalities,
        "lag_ledger_prefix_count": lag_ledger_prefix_count,
        "lag_ledger_all_prefixes_pass": lag_ledger_pass,
        "no_same_parity_sigma_run_of_length_nine": no_nine_run,
        "rows": rows,
        "finite_ledger_pass": ledger_pass,
        "finite_not_asymptotic": True,
        "all_pass": (
            prefix_equalities == 2 * ENDPOINT
            and recursive_window_equalities == 2 * ENDPOINT
            and lag_ledger_prefix_count == ENDPOINT
            and lag_ledger_pass
            and all(no_nine_run.values())
            and ledger_pass
            and rows == expected_rows
        ),
    }


@lru_cache(maxsize=1)
def verify_certificate() -> dict[str, object]:
    lag = lag_table_certificate()
    graph = graph_lift_certificate()
    mealy = mealy_certificate()
    exhaustive = exhaustive_extrema_certificate()
    online = online_obstruction_certificate()
    truncated = truncated_window_certificate()
    mobius = mobius_certificate()
    basis = {
        "basis": "prod_(j<ell) x_j^alpha_j * x_ell^e, alpha_j in {0,1,2}, e in {1,2}",
        "dimension_formula": "2*q*3^(ell-1)",
        "sample_dimensions": [
            {"q": q, "ell": ell, "dimension": current_zero_basis_dimension(q, ell)}
            for q, ell in ((1, 1), (1, 2), (2, 3), (1, 15))
        ],
        "formal_not_arithmetic_minimal": True,
        "all_pass": current_zero_basis_dimension(1, 15) == 2 * 3**14,
    }
    sections = (basis, lag, graph, mealy, exhaustive, online, truncated, mobius)
    return {
        "window_basis": basis,
        "lag_two_census": lag,
        "graph_lift_safety": graph,
        "orientation_mealy": mealy,
        "exhaustive_prefix_extrema": exhaustive,
        "online_single_policy_obstruction": online,
        "ell15_truncation": truncated,
        "mobius_finite_reproduction": mobius,
        "all_pass": all(section["all_pass"] for section in sections),
    }
