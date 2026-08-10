"""Finite exact reproduction for the RH-393 two-odd-factor compiler."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
import json
import math
from typing import Any


TERNARY = (-1, 0, 1)
ROW_PARTITION = (512, 27, 8, 12, 9, 8)
ROW_COUNT = sum(ROW_PARTITION)
EPISTEMIC_ROLE = "finite_reproduction_not_analytic_proof"
TITLE = (
    "Two-Odd-Factor Terminal-Log Möbius Compiler and the Multi-Shift "
    "Squarefree Landscape"
)


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads_strict(text: str) -> Any:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(
        text,
        object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def exact_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    if type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and left == right
    return left == right


def odd_support(alpha: tuple[int, ...]) -> tuple[int, ...]:
    _validate_alpha(alpha)
    return tuple(index for index, exponent in enumerate(alpha) if exponent == 1)


def even_support(alpha: tuple[int, ...]) -> tuple[int, ...]:
    _validate_alpha(alpha)
    return tuple(index for index, exponent in enumerate(alpha) if exponent == 2)


def _validate_alpha(alpha: tuple[int, ...]) -> None:
    if type(alpha) is not tuple or not alpha:
        raise TypeError("alpha must be a nonempty exact tuple")
    if any(type(exponent) is not int or exponent not in (0, 1, 2) for exponent in alpha):
        raise ValueError("coordinate exponents must be 0, 1, or 2")


def allowed_dimension(m: int) -> int:
    if type(m) is not int or type(m) is bool or m < 1:
        raise ValueError("m must be an exact positive integer")
    return sum(
        math.comb(m, odd_count) * 2 ** (m - odd_count)
        for odd_count in range(min(2, m) + 1)
    )


def table_values(table_id: int) -> dict[tuple[int, int], int]:
    if type(table_id) is not int or type(table_id) is bool or not 0 <= table_id < 512:
        raise ValueError("table id must be an exact integer in [0,512)")
    points = tuple(product(TERNARY, repeat=2))
    return {point: (1 if (table_id >> index) & 1 else -1) for index, point in enumerate(points)}


def interpolation_c11(values: dict[tuple[int, int], int]) -> Fraction:
    required = set(product(TERNARY, repeat=2))
    if type(values) is not dict or set(values) != required:
        raise ValueError("truth table must contain all nine ternary inputs")
    if any(type(value) is not int or type(value) is bool or value not in (-1, 1) for value in values.values()):
        raise ValueError("truth table outputs must be exact signs")
    return Fraction(
        values[(1, 1)] - values[(1, -1)] - values[(-1, 1)] + values[(-1, -1)],
        4,
    )


def distinct_residues(shifts: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    if type(shifts) is not tuple or any(type(item) is not int or type(item) is bool for item in shifts):
        raise TypeError("shifts must be exact integers")
    if type(modulus) is not int or type(modulus) is bool or modulus < 1:
        raise ValueError("modulus must be a positive exact integer")
    return tuple(sorted({item % modulus for item in shifts}))


def local_theta_data(
    shifts: tuple[int, ...], p: int, q_exponent: int, phase: int
) -> dict[str, int | bool | list[int]]:
    if (
        type(p) is not int or type(p) is bool or p < 2
        or any(p % divisor == 0 for divisor in range(2, math.isqrt(p) + 1))
    ):
        raise ValueError("p must be an exact prime")
    if type(q_exponent) is not int or type(q_exponent) is bool or q_exponent < 0:
        raise ValueError("q exponent must be an exact nonnegative integer")
    residues = distinct_residues(shifts, p * p)
    nu = len(residues)
    tau = sum(1 for residue in residues if residue % p == phase % p)
    forced = q_exponent >= 2 and phase % (p * p) in residues
    if q_exponent == 0:
        numerator, denominator = p * p - nu, p * p
    elif q_exponent == 1:
        numerator, denominator = p - tau, p
    else:
        numerator, denominator = (0, 1) if forced else (1, 1)
    factor = Fraction(numerator, denominator)
    return {
        "residues": list(residues),
        "nu": nu,
        "tau": tau,
        "forced_zero": forced,
        "factor_numerator": factor.numerator,
        "factor_denominator": factor.denominator,
    }


def build_truth_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table_id in range(512):
        values = table_values(table_id)
        coefficient = interpolation_c11(values)
        alternating_sum = (
            values[(1, 1)] - values[(1, -1)]
            - values[(-1, 1)] + values[(-1, -1)]
        )
        rows.append(
            {
                "table_id": table_id,
                "corner_values": [
                    values[(1, 1)], values[(1, -1)],
                    values[(-1, 1)], values[(-1, -1)],
                ],
                "alternating_corner_sum": alternating_sum,
                "c11_numerator": coefficient.numerator,
                "c11_denominator": coefficient.denominator,
                "eligible": coefficient == 0,
                "distinguished_current_cancellation": coefficient == 0,
                "outside_theorem": coefficient != 0,
            }
        )
    return rows


def build_monomial_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for alpha in product((0, 1, 2), repeat=3):
        odd = odd_support(alpha)
        even = even_support(alpha)
        rows.append(
            {
                "alpha": list(alpha),
                "odd_support": list(odd),
                "even_support": list(even),
                "odd_count": len(odd),
                "allowed": len(odd) <= 2,
                "survives": len(odd) == 0,
            }
        )
    return rows


def build_dimension_rows() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for m in range(1, 9):
        by_odd_count = [
            math.comb(m, odd_count) * 2 ** (m - odd_count)
            if odd_count <= m else 0
            for odd_count in range(3)
        ]
        rows.append(
            {
                "m": m,
                "odd_count_0": by_odd_count[0],
                "odd_count_1": by_odd_count[1],
                "odd_count_2": by_odd_count[2],
                "allowed_dimension": sum(by_odd_count),
                "full_dimension": 3**m,
                "missing_dimension": 3**m - sum(by_odd_count),
            }
        )
    return rows


THETA_CASES = (
    ((), (2, 3), 1, 0),
    ((0,), (2, 3, 5), 1, 0),
    ((0, 2), (2, 3), 1, 0),
    ((0, 2), (2, 3), 2, 0),
    ((0, 4), (2, 3), 2, 0),
    ((0, 2), (2, 3), 4, 0),
    ((0, 1, 2), (2, 3), 2, 0),
    ((0, 1, 2), (2, 3), 3, 0),
    ((0, 3, 6), (2, 3), 3, 0),
    ((0, 9), (2, 3), 3, 0),
    ((0, 1, 2, 3), (2, 3), 4, 0),
    ((-2, 0, 3), (2, 3, 5), 12, 0),
)


def _valuation(number: int, prime: int) -> int:
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def _theta_fixture(
    shifts: tuple[int, ...], primes: tuple[int, ...], q: int, phase: int
) -> dict[str, Any]:
    local_factors: list[dict[str, Any]] = []
    predicted = Fraction(1, q)
    global_density = Fraction(1, 1)
    modulus = q
    for p in primes:
        exponent = _valuation(q, p)
        local = local_theta_data(shifts, p, exponent, phase)
        local_factors.append({"p": p, "q_exponent": exponent, **local})
        predicted *= Fraction(local["factor_numerator"], local["factor_denominator"])
        global_density *= Fraction(p * p - local["nu"], p * p)
        modulus = math.lcm(modulus, p * p)
    allowed_by_residue = [
        all(
            all((residue - shift) % (p * p) != 0 for shift in shifts)
            for p in primes
        )
        for residue in range(modulus)
    ]
    direct_counts = [
        sum(allowed_by_residue[residue] and residue % q == r for residue in range(modulus))
        for r in range(q)
    ]
    direct_count = direct_counts[phase % q]
    direct_density = Fraction(direct_count, modulus)
    phase_densities = [Fraction(count, modulus) for count in direct_counts]
    predicted_phase_densities: list[Fraction] = []
    for r in range(q):
        value = Fraction(1, q)
        for p in primes:
            exponent = _valuation(q, p)
            local = local_theta_data(shifts, p, exponent, r)
            value *= Fraction(local["factor_numerator"], local["factor_denominator"])
        predicted_phase_densities.append(value)
    phase_mass = sum(phase_densities, Fraction(0, 1))
    return {
        "shifts": list(shifts),
        "primes": list(primes),
        "q": q,
        "phase": phase,
        "local_factors": local_factors,
        "crt_modulus": modulus,
        "direct_counts": direct_counts,
        "phase_densities": [[value.numerator, value.denominator] for value in phase_densities],
        "predicted_phase_densities": [
            [value.numerator, value.denominator] for value in predicted_phase_densities
        ],
        "direct_count": direct_count,
        "direct_density_numerator": direct_density.numerator,
        "direct_density_denominator": direct_density.denominator,
        "predicted_density_numerator": predicted.numerator,
        "predicted_density_denominator": predicted.denominator,
        "phase_mass_numerator": phase_mass.numerator,
        "phase_mass_denominator": phase_mass.denominator,
        "global_density_numerator": global_density.numerator,
        "global_density_denominator": global_density.denominator,
    }


def _build_landscape_contracts() -> list[dict[str, Any]]:
    return [
        {
            "claim": "positive_lower", "m": 1,
            "lower_product": "product_p(1-1/p^2)",
            "equality_condition": "automatic", "witness": [0],
            "oracle_shift_box": [-3, 3], "oracle_primes": [2, 3, 5],
            "oracle_checks": 21, "oracle_failures": 0,
            "local_lower_gap": "(m-nu_p)/p^2",
            "positivity_reason": "nu_p_at_most_m_and_p^2_greater_than_m",
        },
        {
            "claim": "positive_lower", "m": 2,
            "lower_product": "product_p(1-2/p^2)",
            "equality_condition": "all_pairwise_differences_squarefree",
            "witness": [0, 1], "oracle_shift_box": [-3, 3],
            "oracle_primes": [2, 3, 5], "oracle_checks": 63,
            "oracle_failures": 0,
            "local_lower_gap": "(m-nu_p)/p^2",
            "positivity_reason": "nu_p_at_most_m_and_p^2_greater_than_m",
        },
        {
            "claim": "positive_lower", "m": 3,
            "lower_product": "product_p(1-3/p^2)",
            "equality_condition": "all_pairwise_differences_squarefree",
            "witness": [0, 1, 2], "oracle_shift_box": [-3, 3],
            "oracle_primes": [2, 3, 5], "oracle_checks": 105,
            "oracle_failures": 0,
            "local_lower_gap": "(m-nu_p)/p^2",
            "positivity_reason": "nu_p_at_most_m_and_p^2_greater_than_m",
        },
        {
            "claim": "zero_attained", "m": 4, "prime": 2,
            "witness": [0, 1, 2, 3], "covered_residues": [0, 1, 2, 3],
            "local_factor_numerator": 0,
            "all_m_at_least_4": True,
            "extension_rule": "adjoin_arbitrary_distinct_shifts_to_mod4_cover",
            "extension_preserves_zero_factor": True,
        },
        {
            "claim": "zero_iff_prime_square_cover", "m_min": 4,
            "condition": "exists_p_with_nu_p_equals_p_squared",
            "oracle_shift_box": [0, 7], "oracle_m_values": [4, 5],
            "oracle_primes": [2, 3], "oracle_checks": 126, "oracle_failures": 0,
            "finite_scan_reason": "only_primes_with_p^2_at_most_m_can_cover",
            "positive_tail_reason": "no_zero_factor_and_sum_p(nu_p/p^2)_converges",
        },
        {
            "claim": "upper_bound", "m_min": 2,
            "value": "product_p(1-1/p^2)=6/pi^2",
            "local_reason": "nu_p_at_least_1",
            "local_upper_gap": "(nu_p-1)/p^2",
        },
        {
            "claim": "upper_not_attained", "m_min": 2,
            "reason": "a_nonzero_pair_difference_has_a_prime_square_escape",
            "sample_pair": [0, 1], "sample_escape_prime": 2,
            "general_escape_rule": (
                "choose_nonzero_difference_d_and_prime_p_not_dividing_d_then_nu_p_at_least_2"
            ),
        },
        {
            "claim": "primorial_square_approach", "m_min": 2,
            "Q_y_definition": "Q_y=product_(p<=y)p^2",
            "configuration_definition": "A_(m,y)={jQ_y:0<=j<m}",
            "general_small_prime_nu": "nu_p(A_(m,y))=1_for_p<=y",
            "sample_primes": [2, 3, 5], "sample_Q": 900,
            "sample_m": 4, "sample_configuration": [0, 900, 1800, 2700],
            "small_prime_nu": [1, 1, 1], "sample_tail_prime": 7,
            "sample_tail_nu": 4, "finite_left_factor": [16, 25],
            "fixed_m_condition": "y_squared_greater_than_m",
            "lower_sandwich": (
                "product_(p<=y)(1-1/p^2)product_(p>y)(1-m/p^2)"
            ),
            "upper_sandwich": "6/pi^2",
            "tail_reason": "sum_(p>y)(m-1)/p^2_to_0",
            "limit": "6/pi^2_not_attained_for_m_at_least_2",
        },
        {
            "claim": "phase_global_distinction",
            "sample_shifts": [0, 2], "sample_q": 2,
            "sample_primes": [2, 3],
            "sample_phase_vector": [[0, 1], [7, 18]],
            "sample_global_kappa": [7, 18], "phase_may_be_zero": True,
            "positive_lower_applies_only_to_global_kappa": True,
        },
    ]


def _build_analytic_contracts() -> list[dict[str, Any]]:
    return [
        {
            "claim": "terminal_score_definition",
            "functional": (
                "T_X=(log(omega(X)))^-1 sum_(X/omega(X)<n<=X) "
                "sum_alpha c_alpha(n mod q) prod_i mu_0(n-a_i)^alpha_i / n"
            ),
            "clock": "1<=omega(X)<=X_and_omega(X)->infinity",
        },
        {
            "claim": "fixed_quantifiers", "m_integer_min": 1,
            "q_integer_min": 1, "shifts": "fixed_finite_distinct_integers",
            "coefficients": "fixed_q_periodic_before_X_limit",
            "coordinate_exponents": [0, 1, 2],
            "admissible_alpha": "odd_support_size_at_most_2",
            "dimension_formula": (
                "D_m=2^m+m*2^(m-1)+binom(m,2)*2^(m-2)_with_absent_terms_zero"
            ),
            "for_every_admissible_omega": True,
            "source_roles": {
                "RH392_equation_19": "frozen_one_form_input",
                "RH392_theorem_2_2": "frozen_two_form_input",
                "Tao": "inherited_remote_analytic_provenance",
                "JY_and_Maynard": "closure_only",
                "Mirsky": "historical_only_local_CRT_proof",
            },
        },
        {
            "claim": "odd_zero_crt_density",
            "E_alpha_definition": "E(alpha)={i:alpha_i=2}",
            "B_p_definition": "B_p(E)=distinct_set_{i in E}(a_i mod p^2)",
            "nu_definition": "nu_p(E)=cardinality(B_p(E))",
            "tau_definition": (
                "tau_(p,E)(r)=number_of_distinct_b_in_B_p(E)_with_b_mod_p=r_mod_p"
            ),
            "kappa_definition": "kappa_E=product_p(1-nu_p(E)/p^2)",
            "limit_formula": (
                "sum_(r mod q) sum_(alpha in {0,2}^m) "
                "c_alpha(r) Theta_(q,r)(E(alpha))"
            ),
            "theta_formula": (
                "q^-1 product_(p not_dividing q)(1-nu_p/p^2) "
                "product_(p exactly_divides q)(1-tau_p(r)/p) "
                "product_(p^2 divides q)1_(r mod p^2 notin B_p)"
            ),
            "phase_sum": "sum_(r mod q)Theta_(q,r)(E)=kappa_E",
            "empty_even_support": "Theta_(q,r)(empty)=1/q",
        },
        {
            "claim": "odd_one_masked_davenport", "odd_support": 1,
            "source": "RH392_equation_19", "limit": 0,
            "extra_even_coordinates": "fixed_Boolean_periodic_square_masks",
        },
        {
            "claim": "odd_two_masked_arbitrary_determinant", "odd_support": 2,
            "source": "RH392_theorem_2_2", "limit": 0,
            "distinct_shifts_imply_nonzero_determinant": True,
            "extra_even_coordinates": "fixed_Boolean_periodic_square_masks",
        },
        {
            "claim": "boolean_tail_and_limit_order",
            "tail": "O_m(log(omega(X))/P+1)",
            "normalized_tail": "O_m(1/P+1/log(omega(X)))",
            "order": ["P_fixed", "X_to_infinity", "P_to_infinity"],
        },
        {
            "claim": "distinguished_current_truth_census", "eligible": 192,
            "total": 512, "corner_patterns": 6, "free_noncorner_bits": 5,
            "score": "mu_0(n-a_3)*f(mu_0(n-a_1),mu_0(n-a_2))",
            "fixed_distinct_triple_shifts": True,
            "fixed_q_periodic_phase_tables_from_eligible_class": True,
            "eligible_limit": 0, "outside_count": 320,
            "outside_means_nonconvergence": False,
            "c11_formula": (
                "[f(1,1)-f(1,-1)-f(-1,1)+f(-1,-1)]/4"
            ),
            "m3_unique_excluded_monomial": [1, 1, 1],
            "m3_general_interpolant_criterion": (
                "c111=2^-3_sum_(epsilon_in_{-1,1}^3)"
                "epsilon_1_epsilon_2_epsilon_3_f(epsilon)=0"
            ),
        },
        {
            "claim": "firewalls", "max_odd_support": 2,
            "generic_safe_table_capacity": "STOP_SCOPED",
            "forbidden": [
                "odd_support_at_least_3", "growing_m_q_shifts_or_masks",
                "growing_or_X_dependent_coefficients", "rate",
                "ordinary_Cesaro", "max_before_limit", "adaptive_capacity",
                "operator_trace_RH_or_Gates",
            ],
        },
    ]


def build_theta_rows() -> list[dict[str, Any]]:
    return [_theta_fixture(shifts, primes, q, phase) for shifts, primes, q, phase in THETA_CASES]


def build_landscape_rows() -> list[dict[str, Any]]:
    return _build_landscape_contracts()


def build_analytic_rows() -> list[dict[str, Any]]:
    return _build_analytic_contracts()


def build_certificate() -> dict[str, Any]:
    groups = {
        "truth_rows": build_truth_rows(),
        "monomial_rows": build_monomial_rows(),
        "dimension_rows": build_dimension_rows(),
        "theta_rows": build_theta_rows(),
        "landscape_rows": build_landscape_rows(),
        "analytic_rows": build_analytic_rows(),
    }
    sizes = [len(rows) for rows in groups.values()]
    eligible = sum(row["eligible"] for row in groups["truth_rows"])
    eligible_corner_counts: dict[tuple[int, ...], int] = {}
    for row in groups["truth_rows"]:
        if row["eligible"]:
            corner = tuple(row["corner_values"])
            eligible_corner_counts[corner] = eligible_corner_counts.get(corner, 0) + 1
    all_pass = (
        sizes == list(ROW_PARTITION)
        and eligible == 192
        and len(eligible_corner_counts) == 6
        and set(eligible_corner_counts.values()) == {32}
        and sum(row["allowed"] for row in groups["monomial_rows"]) == 26
        and allowed_dimension(3) == 26
        and all(
            row["phase_densities"] == row["predicted_phase_densities"]
            and [row["phase_mass_numerator"], row["phase_mass_denominator"]]
            == [row["global_density_numerator"], row["global_density_denominator"]]
            for row in groups["theta_rows"]
        )
        and groups["theta_rows"][0]["phase_densities"] == [[1, 1]]
        and groups["theta_rows"][3]["local_factors"][0]["tau"] == 2
        and groups["theta_rows"][4]["local_factors"][0]["nu"] == 1
        and groups["theta_rows"][10]["phase_mass_numerator"] == 0
        and all(row.get("oracle_failures", 0) == 0 for row in groups["landscape_rows"])
        and groups["landscape_rows"][3]["local_factor_numerator"] == 0
        and groups["landscape_rows"][3]["all_m_at_least_4"] is True
        and groups["landscape_rows"][7]["small_prime_nu"] == [1, 1, 1]
        and groups["landscape_rows"][7]["fixed_m_condition"]
        == "y_squared_greater_than_m"
        and groups["landscape_rows"][7]["Q_y_definition"]
        == "Q_y=product_(p<=y)p^2"
        and groups["landscape_rows"][8]["sample_phase_vector"] == [[0, 1], [7, 18]]
        and groups["analytic_rows"][1]["for_every_admissible_omega"] is True
        and groups["analytic_rows"][2]["E_alpha_definition"] == "E(alpha)={i:alpha_i=2}"
        and groups["analytic_rows"][5]["order"]
        == ["P_fixed", "X_to_infinity", "P_to_infinity"]
        and groups["analytic_rows"][6]["eligible"] == 192
        and groups["analytic_rows"][6]["m3_unique_excluded_monomial"] == [1, 1, 1]
        and groups["analytic_rows"][7]["max_odd_support"] == 2
    )
    return {
        "title": TITLE,
        "epistemic_role": EPISTEMIC_ROLE,
        "row_partition": sizes,
        "row_count": sum(sizes),
        **groups,
        "all_pass": all_pass,
    }


BUILDER_NAMES = (
    "build_certificate", "build_truth_rows", "build_monomial_rows",
    "build_dimension_rows", "build_theta_rows", "build_landscape_rows",
    "build_analytic_rows", "_theta_fixture", "_build_landscape_contracts",
    "_build_analytic_contracts",
)

SEMANTIC_HELPER_NAMES = (
    "table_values", "interpolation_c11", "odd_support", "even_support",
    "allowed_dimension", "local_theta_data", "distinct_residues", "_valuation",
    "exact_equal", "canonical_json_bytes",
)


def verify_certificate(candidate: dict[str, Any], *, compare_fresh: bool = False) -> bool:
    from fractions import Fraction as _Fraction
    from itertools import combinations as _combinations, product as _product
    import math as _math

    def same(left: Any, right: Any) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(same(left[key], right[key]) for key in left)
        if type(left) in (list, tuple):
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        if type(left) is float:
            return _math.isfinite(left) and _math.isfinite(right) and left == right
        return left == right

    def valuation(number: int, prime: int) -> int:
        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        return exponent

    def is_prime(number: int) -> bool:
        return (
            type(number) is int and type(number) is not bool and number >= 2
            and not any(number % divisor == 0 for divisor in range(2, _math.isqrt(number) + 1))
        )

    def is_squarefree(number: int) -> bool:
        number = abs(number)
        return number > 0 and not any(
            number % (divisor * divisor) == 0
            for divisor in range(2, _math.isqrt(number) + 1)
        )

    if type(candidate) is not dict:
        return False
    required = {
        "title", "epistemic_role", "row_partition", "row_count",
        "truth_rows", "monomial_rows", "dimension_rows", "theta_rows",
        "landscape_rows", "analytic_rows", "all_pass",
    }
    if set(candidate) != required or candidate.get("all_pass") is not True:
        return False
    if candidate.get("title") != (
        "Two-Odd-Factor Terminal-Log Möbius Compiler and the Multi-Shift "
        "Squarefree Landscape"
    ):
        return False
    if candidate.get("epistemic_role") != "finite_reproduction_not_analytic_proof":
        return False
    partition = candidate.get("row_partition")
    if type(partition) is not list or not same(partition, [512, 27, 8, 12, 9, 8]):
        return False
    if any(type(value) is not int or type(value) is bool for value in partition):
        return False
    if type(candidate.get("row_count")) is not int or type(candidate.get("row_count")) is bool:
        return False
    if candidate.get("row_count") != 576:
        return False
    truth = candidate.get("truth_rows")
    monomials = candidate.get("monomial_rows")
    dimensions = candidate.get("dimension_rows")
    theta = candidate.get("theta_rows")
    if not all(type(rows) is list for rows in (truth, monomials, dimensions, theta)):
        return False
    if len(truth) != 512 or len(monomials) != 27 or len(dimensions) != 8 or len(theta) != 12:
        return False
    corner_counts: dict[tuple[int, ...], int] = {}
    for table_id, row in enumerate(truth):
        if type(row) is not dict or set(row) != {
            "table_id", "corner_values", "alternating_corner_sum",
            "c11_numerator", "c11_denominator", "eligible",
            "distinguished_current_cancellation", "outside_theorem",
        } or row.get("table_id") != table_id:
            return False
        values = [1 if (table_id >> index) & 1 else -1 for index in range(9)]
        corners = [values[8], values[6], values[2], values[0]]
        alternating_sum = corners[0] - corners[1] - corners[2] + corners[3]
        coefficient = _Fraction(alternating_sum, 4)
        expected = {
            "table_id": table_id,
            "corner_values": corners,
            "alternating_corner_sum": alternating_sum,
            "c11_numerator": coefficient.numerator,
            "c11_denominator": coefficient.denominator,
            "eligible": coefficient == 0,
            "distinguished_current_cancellation": coefficient == 0,
            "outside_theorem": coefficient != 0,
        }
        if not same(row, expected):
            return False
        if row["eligible"]:
            key = tuple(corners)
            corner_counts[key] = corner_counts.get(key, 0) + 1
    if sum(row["eligible"] for row in truth) != 192:
        return False
    if len(corner_counts) != 6 or set(corner_counts.values()) != {32}:
        return False
    expected_alphas = tuple(
        (a, b, c) for a in (0, 1, 2) for b in (0, 1, 2) for c in (0, 1, 2)
    )
    for alpha, row in zip(expected_alphas, monomials):
        if type(row) is not dict or set(row) != {
            "alpha", "odd_support", "even_support", "odd_count", "allowed", "survives"
        }:
            return False
        odd = tuple(index for index, exponent in enumerate(alpha) if exponent == 1)
        even = tuple(index for index, exponent in enumerate(alpha) if exponent == 2)
        expected = {
            "alpha": list(alpha), "odd_support": list(odd),
            "even_support": list(even), "odd_count": len(odd),
            "allowed": len(odd) <= 2, "survives": len(odd) == 0,
        }
        if not same(row, expected):
            return False
    for m, row in enumerate(dimensions, 1):
        if type(row) is not dict or set(row) != {
            "m", "odd_count_0", "odd_count_1", "odd_count_2",
            "allowed_dimension", "full_dimension", "missing_dimension",
        }:
            return False
        counts = [0, 0, 0]
        brute_allowed = 0
        for alpha in _product((0, 1, 2), repeat=m):
            odd_count = sum(exponent == 1 for exponent in alpha)
            if odd_count <= 2:
                counts[odd_count] += 1
                brute_allowed += 1
        expected = {
            "m": m, "odd_count_0": counts[0], "odd_count_1": counts[1],
            "odd_count_2": counts[2], "allowed_dimension": brute_allowed,
            "full_dimension": 3**m,
            "missing_dimension": 3**m - brute_allowed,
        }
        if not same(row, expected):
            return False

    theta_cases = (
        ((), (2, 3), 1, 0), ((0,), (2, 3, 5), 1, 0),
        ((0, 2), (2, 3), 1, 0), ((0, 2), (2, 3), 2, 0),
        ((0, 4), (2, 3), 2, 0), ((0, 2), (2, 3), 4, 0),
        ((0, 1, 2), (2, 3), 2, 0), ((0, 1, 2), (2, 3), 3, 0),
        ((0, 3, 6), (2, 3), 3, 0), ((0, 9), (2, 3), 3, 0),
        ((0, 1, 2, 3), (2, 3), 4, 0), ((-2, 0, 3), (2, 3, 5), 12, 0),
    )
    theta_keys = {
        "shifts", "primes", "q", "phase", "local_factors", "crt_modulus",
        "direct_counts", "phase_densities", "predicted_phase_densities",
        "direct_count", "direct_density_numerator", "direct_density_denominator",
        "predicted_density_numerator", "predicted_density_denominator",
        "phase_mass_numerator", "phase_mass_denominator",
        "global_density_numerator", "global_density_denominator",
    }
    local_keys = {
        "p", "q_exponent", "residues", "nu", "tau", "forced_zero",
        "factor_numerator", "factor_denominator",
    }
    for case, row in zip(theta_cases, theta):
        shifts, primes, q, phase = case
        if type(row) is not dict or set(row) != theta_keys:
            return False
        if type(q) is not int or q < 1 or phase not in range(q):
            return False
        if len(set(primes)) != len(primes) or not all(is_prime(p) for p in primes):
            return False
        remaining = q
        for p in primes:
            while remaining % p == 0:
                remaining //= p
        if remaining != 1:
            return False
        modulus = q
        for p in primes:
            modulus = _math.lcm(modulus, p * p)
        allowed = [
            all(
                all((residue - shift) % (p * p) != 0 for shift in shifts)
                for p in primes
            )
            for residue in range(modulus)
        ]
        direct_counts = [
            sum(allowed[residue] and residue % q == r for residue in range(modulus))
            for r in range(q)
        ]
        direct_densities = [_Fraction(count, modulus) for count in direct_counts]
        predicted_densities: list[_Fraction] = []
        for r in range(q):
            predicted = _Fraction(1, q)
            for p in primes:
                exponent = valuation(q, p)
                residues = sorted({shift % (p * p) for shift in shifts})
                nu = len(residues)
                tau = sum(residue % p == r % p for residue in residues)
                if sum(
                    sum(residue % p == s for residue in residues) for s in range(p)
                ) != nu:
                    return False
                forced = exponent >= 2 and r % (p * p) in residues
                if exponent == 0:
                    factor = _Fraction(p * p - nu, p * p)
                elif exponent == 1:
                    factor = _Fraction(p - tau, p)
                else:
                    factor = _Fraction(0 if forced else 1, 1)
                predicted *= factor
            predicted_densities.append(predicted)
        local_factors: list[dict[str, Any]] = []
        global_density = _Fraction(1, 1)
        for p in primes:
            exponent = valuation(q, p)
            residues = sorted({shift % (p * p) for shift in shifts})
            nu = len(residues)
            tau = sum(residue % p == phase % p for residue in residues)
            forced = exponent >= 2 and phase % (p * p) in residues
            if exponent == 0:
                factor = _Fraction(p * p - nu, p * p)
            elif exponent == 1:
                factor = _Fraction(p - tau, p)
            else:
                factor = _Fraction(0 if forced else 1, 1)
            local = {
                "p": p, "q_exponent": exponent, "residues": residues,
                "nu": nu, "tau": tau, "forced_zero": forced,
                "factor_numerator": factor.numerator,
                "factor_denominator": factor.denominator,
            }
            if set(local) != local_keys:
                return False
            local_factors.append(local)
            global_density *= _Fraction(p * p - nu, p * p)
        phase_mass = sum(direct_densities, _Fraction(0, 1))
        highlighted = direct_densities[phase]
        predicted_highlighted = predicted_densities[phase]
        expected = {
            "shifts": list(shifts), "primes": list(primes), "q": q,
            "phase": phase, "local_factors": local_factors,
            "crt_modulus": modulus, "direct_counts": direct_counts,
            "phase_densities": [
                [value.numerator, value.denominator] for value in direct_densities
            ],
            "predicted_phase_densities": [
                [value.numerator, value.denominator] for value in predicted_densities
            ],
            "direct_count": direct_counts[phase],
            "direct_density_numerator": highlighted.numerator,
            "direct_density_denominator": highlighted.denominator,
            "predicted_density_numerator": predicted_highlighted.numerator,
            "predicted_density_denominator": predicted_highlighted.denominator,
            "phase_mass_numerator": phase_mass.numerator,
            "phase_mass_denominator": phase_mass.denominator,
            "global_density_numerator": global_density.numerator,
            "global_density_denominator": global_density.denominator,
        }
        if not same(row, expected):
            return False
        if direct_densities != predicted_densities or phase_mass != global_density:
            return False

    landscape = candidate.get("landscape_rows")
    analytic = candidate.get("analytic_rows")
    if type(landscape) is not list or len(landscape) != 9:
        return False
    if type(analytic) is not list or len(analytic) != 8:
        return False

    expected_landscape = [
        {
            "claim": "positive_lower", "m": 1,
            "lower_product": "product_p(1-1/p^2)",
            "equality_condition": "automatic", "witness": [0],
            "oracle_shift_box": [-3, 3], "oracle_primes": [2, 3, 5],
            "oracle_checks": 21, "oracle_failures": 0,
            "local_lower_gap": "(m-nu_p)/p^2",
            "positivity_reason": "nu_p_at_most_m_and_p^2_greater_than_m",
        },
        {
            "claim": "positive_lower", "m": 2,
            "lower_product": "product_p(1-2/p^2)",
            "equality_condition": "all_pairwise_differences_squarefree",
            "witness": [0, 1], "oracle_shift_box": [-3, 3],
            "oracle_primes": [2, 3, 5], "oracle_checks": 63,
            "oracle_failures": 0,
            "local_lower_gap": "(m-nu_p)/p^2",
            "positivity_reason": "nu_p_at_most_m_and_p^2_greater_than_m",
        },
        {
            "claim": "positive_lower", "m": 3,
            "lower_product": "product_p(1-3/p^2)",
            "equality_condition": "all_pairwise_differences_squarefree",
            "witness": [0, 1, 2], "oracle_shift_box": [-3, 3],
            "oracle_primes": [2, 3, 5], "oracle_checks": 105,
            "oracle_failures": 0,
            "local_lower_gap": "(m-nu_p)/p^2",
            "positivity_reason": "nu_p_at_most_m_and_p^2_greater_than_m",
        },
        {
            "claim": "zero_attained", "m": 4, "prime": 2,
            "witness": [0, 1, 2, 3], "covered_residues": [0, 1, 2, 3],
            "local_factor_numerator": 0,
            "all_m_at_least_4": True,
            "extension_rule": "adjoin_arbitrary_distinct_shifts_to_mod4_cover",
            "extension_preserves_zero_factor": True,
        },
        {
            "claim": "zero_iff_prime_square_cover", "m_min": 4,
            "condition": "exists_p_with_nu_p_equals_p_squared",
            "oracle_shift_box": [0, 7], "oracle_m_values": [4, 5],
            "oracle_primes": [2, 3], "oracle_checks": 126, "oracle_failures": 0,
            "finite_scan_reason": "only_primes_with_p^2_at_most_m_can_cover",
            "positive_tail_reason": "no_zero_factor_and_sum_p(nu_p/p^2)_converges",
        },
        {
            "claim": "upper_bound", "m_min": 2,
            "value": "product_p(1-1/p^2)=6/pi^2",
            "local_reason": "nu_p_at_least_1",
            "local_upper_gap": "(nu_p-1)/p^2",
        },
        {
            "claim": "upper_not_attained", "m_min": 2,
            "reason": "a_nonzero_pair_difference_has_a_prime_square_escape",
            "sample_pair": [0, 1], "sample_escape_prime": 2,
            "general_escape_rule": (
                "choose_nonzero_difference_d_and_prime_p_not_dividing_d_then_nu_p_at_least_2"
            ),
        },
        {
            "claim": "primorial_square_approach", "m_min": 2,
            "Q_y_definition": "Q_y=product_(p<=y)p^2",
            "configuration_definition": "A_(m,y)={jQ_y:0<=j<m}",
            "general_small_prime_nu": "nu_p(A_(m,y))=1_for_p<=y",
            "sample_primes": [2, 3, 5], "sample_Q": 900,
            "sample_m": 4, "sample_configuration": [0, 900, 1800, 2700],
            "small_prime_nu": [1, 1, 1], "sample_tail_prime": 7,
            "sample_tail_nu": 4, "finite_left_factor": [16, 25],
            "fixed_m_condition": "y_squared_greater_than_m",
            "lower_sandwich": (
                "product_(p<=y)(1-1/p^2)product_(p>y)(1-m/p^2)"
            ),
            "upper_sandwich": "6/pi^2",
            "tail_reason": "sum_(p>y)(m-1)/p^2_to_0",
            "limit": "6/pi^2_not_attained_for_m_at_least_2",
        },
        {
            "claim": "phase_global_distinction", "sample_shifts": [0, 2],
            "sample_q": 2, "sample_primes": [2, 3],
            "sample_phase_vector": [[0, 1], [7, 18]],
            "sample_global_kappa": [7, 18], "phase_may_be_zero": True,
            "positive_lower_applies_only_to_global_kappa": True,
        },
    ]
    if not same(landscape, expected_landscape):
        return False
    for row in landscape[:3]:
        checks = 0
        failures = 0
        lower, upper = row["oracle_shift_box"]
        for configuration in _combinations(range(lower, upper + 1), row["m"]):
            for p in row["oracle_primes"]:
                nu = len({item % (p * p) for item in configuration})
                collision_free = all(
                    (right - left) % (p * p) != 0
                    for left, right in _combinations(configuration, 2)
                )
                failures += (nu == row["m"]) != collision_free
                failures += nu > row["m"]
                checks += 1
        if checks != row["oracle_checks"] or failures != row["oracle_failures"]:
            return False
        witness = row["witness"]
        if len(witness) != row["m"] or len(set(witness)) != row["m"]:
            return False
        if not all(is_squarefree(right - left) for left, right in _combinations(witness, 2)):
            return False
    if sorted({item % 4 for item in landscape[3]["witness"]}) != [0, 1, 2, 3]:
        return False
    for m in range(4, 9):
        extension = list(range(m))
        if len(extension) != m or len(set(extension)) != m:
            return False
        if len({item % 4 for item in extension}) != 4:
            return False
    zero_checks = 0
    zero_failures = 0
    for m in landscape[4]["oracle_m_values"]:
        for configuration in _combinations(range(0, 8), m):
            truncated_product = _Fraction(1, 1)
            has_cover = False
            for p in landscape[4]["oracle_primes"]:
                nu = len({item % (p * p) for item in configuration})
                truncated_product *= _Fraction(p * p - nu, p * p)
                has_cover = has_cover or nu == p * p
            zero_failures += (truncated_product == 0) != has_cover
            zero_checks += 1
    if zero_checks != 126 or zero_failures != 0:
        return False
    for m in (2, 3):
        for configuration in _combinations(range(-3, 4), m):
            for p in (2, 3, 5):
                nu = len({item % (p * p) for item in configuration})
                if nu < 1 or nu - 1 < 0:
                    return False
            difference = abs(configuration[1] - configuration[0])
            escape = next(p for p in (2, 3, 5, 7) if difference % p != 0)
            if len({item % (escape * escape) for item in configuration}) < 2:
                return False
    pair = landscape[6]["sample_pair"]
    escape = landscape[6]["sample_escape_prime"]
    if pair[0] == pair[1] or (pair[1] - pair[0]) % (escape * escape) == 0:
        return False
    primorial = landscape[7]
    q_value = _math.prod(p * p for p in primorial["sample_primes"])
    if q_value != primorial["sample_Q"]:
        return False
    configuration = primorial["sample_configuration"]
    if configuration != [index * q_value for index in range(primorial["sample_m"])]:
        return False
    if max(primorial["sample_primes"]) ** 2 <= primorial["sample_m"]:
        return False
    small_nu = [len({item % (p * p) for item in configuration}) for p in primorial["sample_primes"]]
    if small_nu != primorial["small_prime_nu"]:
        return False
    tail_p = primorial["sample_tail_prime"]
    if len({item % (tail_p * tail_p) for item in configuration}) != primorial["sample_tail_nu"]:
        return False
    finite_factor = _Fraction(1, 1)
    for p in primorial["sample_primes"]:
        finite_factor *= _Fraction(p * p - 1, p * p)
    if [finite_factor.numerator, finite_factor.denominator] != primorial["finite_left_factor"]:
        return False
    if landscape[8]["sample_phase_vector"] != theta[3]["phase_densities"]:
        return False
    if landscape[8]["sample_global_kappa"] != [
        theta[3]["phase_mass_numerator"], theta[3]["phase_mass_denominator"]
    ]:
        return False

    expected_analytic = [
        {
            "claim": "terminal_score_definition",
            "functional": (
                "T_X=(log(omega(X)))^-1 sum_(X/omega(X)<n<=X) "
                "sum_alpha c_alpha(n mod q) prod_i mu_0(n-a_i)^alpha_i / n"
            ),
            "clock": "1<=omega(X)<=X_and_omega(X)->infinity",
        },
        {
            "claim": "fixed_quantifiers", "m_integer_min": 1,
            "q_integer_min": 1, "shifts": "fixed_finite_distinct_integers",
            "coefficients": "fixed_q_periodic_before_X_limit",
            "coordinate_exponents": [0, 1, 2],
            "admissible_alpha": "odd_support_size_at_most_2",
            "dimension_formula": (
                "D_m=2^m+m*2^(m-1)+binom(m,2)*2^(m-2)_with_absent_terms_zero"
            ),
            "for_every_admissible_omega": True,
            "source_roles": {
                "RH392_equation_19": "frozen_one_form_input",
                "RH392_theorem_2_2": "frozen_two_form_input",
                "Tao": "inherited_remote_analytic_provenance",
                "JY_and_Maynard": "closure_only",
                "Mirsky": "historical_only_local_CRT_proof",
            },
        },
        {
            "claim": "odd_zero_crt_density",
            "E_alpha_definition": "E(alpha)={i:alpha_i=2}",
            "B_p_definition": "B_p(E)=distinct_set_{i in E}(a_i mod p^2)",
            "nu_definition": "nu_p(E)=cardinality(B_p(E))",
            "tau_definition": (
                "tau_(p,E)(r)=number_of_distinct_b_in_B_p(E)_with_b_mod_p=r_mod_p"
            ),
            "kappa_definition": "kappa_E=product_p(1-nu_p(E)/p^2)",
            "limit_formula": (
                "sum_(r mod q) sum_(alpha in {0,2}^m) "
                "c_alpha(r) Theta_(q,r)(E(alpha))"
            ),
            "theta_formula": (
                "q^-1 product_(p not_dividing q)(1-nu_p/p^2) "
                "product_(p exactly_divides q)(1-tau_p(r)/p) "
                "product_(p^2 divides q)1_(r mod p^2 notin B_p)"
            ),
            "phase_sum": "sum_(r mod q)Theta_(q,r)(E)=kappa_E",
            "empty_even_support": "Theta_(q,r)(empty)=1/q",
        },
        {
            "claim": "odd_one_masked_davenport", "odd_support": 1,
            "source": "RH392_equation_19", "limit": 0,
            "extra_even_coordinates": "fixed_Boolean_periodic_square_masks",
        },
        {
            "claim": "odd_two_masked_arbitrary_determinant", "odd_support": 2,
            "source": "RH392_theorem_2_2", "limit": 0,
            "distinct_shifts_imply_nonzero_determinant": True,
            "extra_even_coordinates": "fixed_Boolean_periodic_square_masks",
        },
        {
            "claim": "boolean_tail_and_limit_order",
            "tail": "O_m(log(omega(X))/P+1)",
            "normalized_tail": "O_m(1/P+1/log(omega(X)))",
            "order": ["P_fixed", "X_to_infinity", "P_to_infinity"],
        },
        {
            "claim": "distinguished_current_truth_census", "eligible": 192,
            "total": 512, "corner_patterns": 6, "free_noncorner_bits": 5,
            "score": "mu_0(n-a_3)*f(mu_0(n-a_1),mu_0(n-a_2))",
            "fixed_distinct_triple_shifts": True,
            "fixed_q_periodic_phase_tables_from_eligible_class": True,
            "eligible_limit": 0, "outside_count": 320,
            "outside_means_nonconvergence": False,
            "c11_formula": (
                "[f(1,1)-f(1,-1)-f(-1,1)+f(-1,-1)]/4"
            ),
            "m3_unique_excluded_monomial": [1, 1, 1],
            "m3_general_interpolant_criterion": (
                "c111=2^-3_sum_(epsilon_in_{-1,1}^3)"
                "epsilon_1_epsilon_2_epsilon_3_f(epsilon)=0"
            ),
        },
        {
            "claim": "firewalls", "max_odd_support": 2,
            "generic_safe_table_capacity": "STOP_SCOPED",
            "forbidden": [
                "odd_support_at_least_3", "growing_m_q_shifts_or_masks",
                "growing_or_X_dependent_coefficients", "rate",
                "ordinary_Cesaro", "max_before_limit", "adaptive_capacity",
                "operator_trace_RH_or_Gates",
            ],
        },
    ]
    if not same(analytic, expected_analytic):
        return False
    census = analytic[6]
    if census["eligible"] != 6 * 2**5 or census["outside_count"] != 512 - census["eligible"]:
        return False
    if census["outside_means_nonconvergence"] is not False:
        return False
    if sum(row["distinguished_current_cancellation"] for row in truth) != census["eligible"]:
        return False
    if monomials[13]["alpha"] != census["m3_unique_excluded_monomial"]:
        return False
    if monomials[13]["allowed"] is not False or monomials[13]["odd_count"] != 3:
        return False
    for row in truth:
        corners = row["corner_values"]
        signed_cube_sum = 2 * (corners[0] - corners[1] - corners[2] + corners[3])
        cube_coefficient = _Fraction(signed_cube_sum, 8)
        if cube_coefficient != _Fraction(row["c11_numerator"], row["c11_denominator"]):
            return False
    if compare_fresh:
        return same(candidate, build_certificate())
    return True


MUTATION_NAMES = (
    "title", "role", "partition_float", "row_count_float",
    "truth_c11", "truth_eligible", "truth_outside", "truth_corner_sum",
    "monomial_allowed", "monomial_odd_count", "monomial_odd_support",
    "monomial_even_support", "monomial_survives", "dimension_odd_zero",
    "dimension_allowed", "dimension_missing", "theta_local_tau",
    "theta_collision_nu", "theta_forced", "theta_direct_count",
    "theta_formula_vector", "theta_phase_mass", "theta_global_density",
    "theta_composite_prime", "landscape_lower", "landscape_cover",
    "landscape_nonattainment", "landscape_primorial", "analytic_source",
    "analytic_limit_order", "analytic_census", "analytic_firewall",
)


def mutate_certificate(candidate: dict[str, Any], mutation: str) -> dict[str, Any]:
    if type(candidate) is not dict:
        raise TypeError("candidate must be an exact dictionary")
    if type(mutation) is not str or mutation not in MUTATION_NAMES:
        raise ValueError("unknown semantic mutation")
    changed = deepcopy(candidate)
    if mutation == "title":
        changed["title"] += "!"
    elif mutation == "role":
        changed["epistemic_role"] = "analytic_proof"
    elif mutation == "partition_float":
        changed["row_partition"][2] = 8.0
    elif mutation == "row_count_float":
        changed["row_count"] = 576.0
    elif mutation == "truth_c11":
        changed["truth_rows"][0]["c11_numerator"] = 1
    elif mutation == "truth_eligible":
        changed["truth_rows"][257]["eligible"] = True
    elif mutation == "truth_outside":
        changed["truth_rows"][257]["outside_theorem"] = False
    elif mutation == "truth_corner_sum":
        changed["truth_rows"][257]["alternating_corner_sum"] = 0
    elif mutation == "monomial_allowed":
        changed["monomial_rows"][13]["allowed"] = True
    elif mutation == "monomial_odd_count":
        changed["monomial_rows"][13]["odd_count"] = 2
    elif mutation == "monomial_odd_support":
        changed["monomial_rows"][13]["odd_support"] = [0, 1]
    elif mutation == "monomial_even_support":
        changed["monomial_rows"][2]["even_support"] = []
    elif mutation == "monomial_survives":
        changed["monomial_rows"][0]["survives"] = False
    elif mutation == "dimension_odd_zero":
        changed["dimension_rows"][0]["odd_count_0"] = 1
    elif mutation == "dimension_allowed":
        changed["dimension_rows"][0]["allowed_dimension"] = 4
    elif mutation == "dimension_missing":
        changed["dimension_rows"][2]["missing_dimension"] = 0
    elif mutation == "theta_local_tau":
        changed["theta_rows"][3]["local_factors"][0]["tau"] = 1
    elif mutation == "theta_collision_nu":
        changed["theta_rows"][4]["local_factors"][0]["nu"] = 2
    elif mutation == "theta_forced":
        changed["theta_rows"][5]["local_factors"][0]["forced_zero"] = False
    elif mutation == "theta_direct_count":
        changed["theta_rows"][11]["direct_counts"][1] += 1
    elif mutation == "theta_formula_vector":
        changed["theta_rows"][3]["predicted_phase_densities"][1] = [1, 2]
    elif mutation == "theta_phase_mass":
        changed["theta_rows"][8]["phase_mass_numerator"] = 2
    elif mutation == "theta_global_density":
        changed["theta_rows"][9]["global_density_denominator"] = 10
    elif mutation == "theta_composite_prime":
        changed["theta_rows"][2]["primes"][0] = 4
    elif mutation == "landscape_lower":
        changed["landscape_rows"][1]["equality_condition"] = "shifts_squarefree"
    elif mutation == "landscape_cover":
        changed["landscape_rows"][3]["covered_residues"] = [0, 1, 2]
    elif mutation == "landscape_nonattainment":
        changed["landscape_rows"][6]["reason"] = "supremum_attained"
    elif mutation == "landscape_primorial":
        changed["landscape_rows"][7]["sample_Q"] = 30
    elif mutation == "analytic_source":
        changed["analytic_rows"][4]["source"] = "RH392_equation_19"
    elif mutation == "analytic_limit_order":
        changed["analytic_rows"][5]["order"] = [
            "X_to_infinity", "P_fixed", "P_to_infinity"
        ]
    elif mutation == "analytic_census":
        changed["analytic_rows"][6]["eligible"] = 191
    elif mutation == "analytic_firewall":
        changed["analytic_rows"][7]["max_odd_support"] = 3
    return changed
