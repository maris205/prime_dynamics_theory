"""Finite exact reproduction for the RH-394 odd-parity compiler.

The certificate records finite algebra, table censuses, and typed theorem
interfaces.  It is deliberately not a replacement for the analytic
Tao--Teravainen or RH-393 inputs.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import math
from typing import Any


TITLE = "Odd-Parity Terminal-Log Möbius Compiler and the Complete Three-Shift Table Law"
EPISTEMIC_ROLE = "finite_exact_algebra_not_analytic_proof"
SCHEMA_VERSION = 1
TERNARY = (-1, 0, 1)
ROW_PARTITION = (81, 17, 512, 8, 8, 8, 8, 8, 8)
ROW_COUNT = sum(ROW_PARTITION)

FIREWALL_NAMES = (
    "even_odd_support_at_least_four",
    "unrestricted_m_at_least_four_tables",
    "growing_m_q_shifts_masks_or_coefficients",
    "effective_uniform_rate",
    "ordinary_cesaro",
    "maximum_before_limit",
    "generic_graph_coupled_capacity",
    "operator_trace_zero_or_gate",
)

MUTATION_NAMES = (
    "title",
    "role",
    "schema_version_float",
    "row_partition_float",
    "row_count",
    "monomial_alpha",
    "monomial_odd_count",
    "monomial_admitted",
    "monomial_channel",
    "histogram_numerator",
    "histogram_count",
    "histogram_eligible",
    "current_table_id",
    "current_corner_alt",
    "current_eligible",
    "dimension_admitted",
    "dimension_total",
    "stratum_count",
    "current_count",
    "phase_pi",
    "phase_theta",
    "phase_recovered",
    "analytic_clock",
    "analytic_source",
    "analytic_phase_bridge",
    "analytic_support_rule",
    "analytic_limit",
    "firewall_true",
    "summary_m3",
    "summary_m4",
    "summary_table_count",
    "summary_phase_mass",
)

BUILDER_NAMES = (
    "build_certificate",
    "build_monomial_rows",
    "build_signed_cube_histogram",
    "build_current_rows",
    "build_dimension_rows",
    "build_stratum_rows",
    "build_current_count_rows",
    "build_phase_rows",
    "build_analytic_rows",
    "build_firewall_rows",
)

SEMANTIC_HELPER_NAMES = (
    "admitted_odd_support",
    "admitted_dimension",
    "current_stratum_count",
    "current_table_count",
    "table_values",
    "corner_alternating_numerator",
    "interpolation_profile",
    "brute_stratum_count",
    "product",
    "math",
    "_local_semantic_verify",
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


def _exact_int(value: Any) -> bool:
    return type(value) is int and type(value) is not bool


def admitted_odd_support(k: int) -> bool:
    return _exact_int(k) and k >= 0 and (k == 0 or k == 2 or k % 2 == 1)


def admitted_dimension(m: int) -> int:
    if not _exact_int(m) or m < 1:
        raise ValueError("m must be an exact positive integer")
    two_channel = math.comb(m, 2) * 2 ** (m - 2) if m >= 2 else 0
    return 2**m + two_channel + (3**m - 1) // 2


def current_stratum_count(k: int) -> int:
    if not _exact_int(k) or k < 0:
        raise ValueError("k must be an exact nonnegative integer")
    if k == 0:
        return 2
    value = 2 ** (2 ** (k - 1)) + 2 * k
    if k >= 2:
        value += 4 * math.comb(k, 2) * 2 ** (2 ** (k - 2))
    return value


def current_table_count(d: int) -> int:
    if not _exact_int(d) or d < 0:
        raise ValueError("d must be an exact nonnegative integer")
    value = 1
    for k in range(d + 1):
        value *= current_stratum_count(k) ** math.comb(d, k)
    return value


def table_values(table_id: int) -> dict[tuple[int, int], int]:
    if not _exact_int(table_id) or not 0 <= table_id < 512:
        raise ValueError("table_id must be an exact integer in [0,512)")
    points = tuple(product(TERNARY, repeat=2))
    return {
        point: (1 if (table_id >> index) & 1 else -1)
        for index, point in enumerate(points)
    }


def corner_alternating_numerator(values: dict[tuple[int, int], int]) -> int:
    expected = set(product(TERNARY, repeat=2))
    if type(values) is not dict or set(values) != expected:
        raise ValueError("values must be the exact two-coordinate ternary table")
    if any(not _exact_int(value) or value not in (-1, 1) for value in values.values()):
        raise ValueError("table values must be exact signs")
    return (
        values[(1, 1)]
        - values[(1, -1)]
        - values[(-1, 1)]
        + values[(-1, -1)]
    )


def interpolation_profile(values: dict[tuple[int, int], int]) -> tuple[int, int, int]:
    """Return nonzero count, largest odd support, and disallowed count for z*f."""

    expected = set(product(TERNARY, repeat=2))
    if type(values) is not dict or set(values) != expected:
        raise ValueError("values must be the exact two-coordinate ternary table")
    if any(not _exact_int(value) or value not in (-1, 1) for value in values.values()):
        raise ValueError("table values must be exact signs")
    weights = {
        0: {-1: Fraction(0), 0: Fraction(1), 1: Fraction(0)},
        1: {-1: Fraction(-1, 2), 0: Fraction(0), 1: Fraction(1, 2)},
        2: {-1: Fraction(1, 2), 0: Fraction(-1), 1: Fraction(1, 2)},
    }
    nonzero = 0
    maximum = 0
    disallowed = 0
    for alpha in product((0, 1, 2), repeat=2):
        coefficient = sum(
            Fraction(values[(x, y)]) * weights[alpha[0]][x] * weights[alpha[1]][y]
            for x, y in product(TERNARY, repeat=2)
        )
        if coefficient:
            odd_support = 1 + alpha.count(1)
            nonzero += 1
            maximum = max(maximum, odd_support)
            if not admitted_odd_support(odd_support):
                disallowed += 1
    return nonzero, maximum, disallowed


def brute_stratum_count(k: int) -> int:
    """Brute-force the Boolean odd-Fourier-degree-at-most-one census for k<=4."""

    if not _exact_int(k) or not 0 <= k <= 4:
        raise ValueError("k must be an exact integer in [0,4]")
    point_count = 1 << k
    if k < 3:
        return 1 << point_count
    points = tuple(product((-1, 1), repeat=k))
    negative_masks: list[int] = []
    for support_size in range(3, k + 1, 2):
        for support in product((0, 1), repeat=k):
            if sum(support) != support_size:
                continue
            mask = 0
            for index, point in enumerate(points):
                parity = math.prod(
                    coordinate for coordinate, selected in zip(point, support) if selected
                )
                if parity == -1:
                    mask |= 1 << index
            negative_masks.append(mask)
    return sum(
        all((table_id ^ mask).bit_count() == point_count // 2 for mask in negative_masks)
        for table_id in range(1 << point_count)
    )


def build_monomial_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for alpha in product((0, 1, 2), repeat=4):
        odd_count = alpha.count(1)
        admitted = admitted_odd_support(odd_count)
        if odd_count == 0:
            channel = "squarefree_density"
        elif odd_count == 2:
            channel = "rh393_two_odd"
        elif odd_count % 2 == 1:
            channel = "tao_teravainen_odd_total_power"
        else:
            channel = "outside_even_four_or_more"
        rows.append(
            {
                "alpha": list(alpha),
                "odd_count": odd_count,
                "admitted": admitted,
                "channel": channel,
            }
        )
    return rows


def build_signed_cube_histogram() -> list[dict[str, Any]]:
    return [
        {
            "transformed_plus_count": plus_count,
            "signed_cube_numerator": 2 * plus_count - 16,
            "truth_table_count": math.comb(16, plus_count),
            "eligible": plus_count == 8,
        }
        for plus_count in range(17)
    ]


def build_current_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table_id in range(512):
        values = table_values(table_id)
        nonzero, maximum, disallowed = interpolation_profile(values)
        rows.append(
            {
                "table_id": table_id,
                "corner_alternating_numerator": corner_alternating_numerator(values),
                "nonzero_coefficient_count": nonzero,
                "maximum_odd_support": maximum,
                "disallowed_nonzero_count": disallowed,
                "eligible": disallowed == 0,
                "terminal_limit_numerator": 0,
            }
        )
    return rows


def build_dimension_rows() -> list[dict[str, Any]]:
    return [
        {
            "m": m,
            "all_even": 2**m,
            "two_odd": math.comb(m, 2) * 2 ** (m - 2) if m >= 2 else 0,
            "positive_odd": (3**m - 1) // 2,
            "admitted": admitted_dimension(m),
            "total": 3**m,
        }
        for m in range(1, 9)
    ]


def build_stratum_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in range(8):
        even_functions = 2 if k == 0 else 2 ** (2 ** (k - 1))
        dictators = 0 if k == 0 else 2 * k
        paired_linear = (
            4 * math.comb(k, 2) * 2 ** (2 ** (k - 2)) if k >= 2 else 0
        )
        rows.append(
            {
                "k": k,
                "even_functions": even_functions,
                "signed_dictators": dictators,
                "paired_half_linear": paired_linear,
                "M_k": current_stratum_count(k),
                "brute_checked": k <= 4,
                "brute_M_k": brute_stratum_count(k) if k <= 4 else None,
            }
        )
    return rows


def build_current_count_rows() -> list[dict[str, Any]]:
    return [
        {
            "d": d,
            "stratum_exponents": [math.comb(d, k) for k in range(d + 1)],
            "B_d": current_table_count(d),
        }
        for d in range(8)
    ]


def _synthetic_pi_numerator(mask: int) -> int:
    return mask.bit_count() + 1


def _synthetic_theta_numerator(mask: int) -> int:
    return sum(
        _synthetic_pi_numerator(support)
        for support in range(8)
        if support & mask == mask
    )


def build_phase_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pi = [_synthetic_pi_numerator(mask) for mask in range(8)]
    theta = [_synthetic_theta_numerator(mask) for mask in range(8)]
    recovered_values: list[int] = []
    for support in range(8):
        complement = 7 ^ support
        recovered = sum(
            (-1) ** subset.bit_count() * theta[support | subset]
            for subset in range(8)
            if subset & support == 0
        )
        recovered_values.append(recovered)
    for q in range(1, 9):
        rows.append(
            {
                "fixture_kind": "synthetic_exact_support_density",
                "q": q,
                "r": q - 1,
                "pi_numerators": list(pi),
                "theta_numerators": list(theta),
                "recovered_pi_numerators": list(recovered_values),
                "common_denominator": 20 * q,
                "phase_mass_numerator": sum(pi),
                "phase_mass": "1/q",
                "pass": recovered_values == pi and all(value >= 0 for value in pi),
            }
        )
    return rows


def build_analytic_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "fixed_terminal_quantifiers",
            "m_q": "exact fixed positive integers",
            "shifts": "fixed pairwise-distinct integers",
            "coefficients": "fixed q-periodic coefficients",
            "mobius_extension": "mu_0(t)=mu(t) for integer t>=1 and mu_0(t)=0 for t<=0",
            "coordinates": "z_i(n)=mu_0(n-a_i)",
            "clock": "1<=omega(X)<=X and omega(X)->infinity",
            "terminal_functional": "T_X(P;omega)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) P_(n mod q)(z(n))/n",
        },
        {
            "claim": "odd_total_power_source",
            "source": "Tao-Teravainen Corollary 1.8, PDF page 7",
            "positive_exponents": [1, 2],
            "sum_exponents_odd": True,
            "channel": "every positive odd support",
        },
        {
            "claim": "fixed_affine_phase_bridge",
            "source": "Tao-Teravainen Remark 1.5 and Theorem A.1",
            "appendix_locator": "PDF page 38",
            "substitution": "n=q*t+r",
            "weight": "1/(q*t+r)=1/(q*t)+O(t^-2)",
        },
        {
            "claim": "admitted_supports",
            "alpha_domain": "alpha in {0,1,2}^m",
            "odd_support_definition": "O(alpha)={i:alpha_i=1}",
            "even_support_definition": "E(alpha)={i:alpha_i=2}",
            "rule": "odd_support is 0, 2, or positive odd",
            "first_excluded": 4,
        },
        {
            "claim": "coefficient_limit",
            "survivors": "all-even channels only",
            "formula": "sum_r sum_{alpha in {0,2}^m} c_alpha(r) Theta_{q,r}(E(alpha))",
            "theta_classes": "B_p(E)=distinct {a_i mod p^2:i in E}; nu_p=|B_p(E)|; tau_p(r)=#{b in B_p(E):b mod p=r mod p}",
            "theta_formula": "q^-1 product_(p not|q)(1-nu_p/p^2) product_(p||q)(1-tau_p(r)/p) product_(p^2|q)1_(r mod p^2 notin B_p(E))",
            "theta_mass": "Theta_{q,r}(empty)=1/q and sum_(r mod q)Theta_{q,r}(E)=kappa_E=product_p(1-nu_p/p^2)",
            "odd_zero_source": "local finite-prime CRT and union tail",
            "odd_two_source": "frozen RH393 compiler using RH392 two-form cancellation",
            "cutoff_order": ["P_fixed", "X_to_infinity", "P_to_infinity"],
        },
        {
            "claim": "table_limit",
            "pi_formula": "Pi(U)=sum_{W subset complement(U)}(-1)^|W|Theta(U union W)",
            "formula": "sum_{r,U} Pi_{q,r}(U) average_signs(f_{r,U})",
            "phase_mass": "sum_U Pi_{q,r}(U)=1/q",
            "m3_full_table_families": "2^(27q)",
            "m4_compiler_table_families": "[binom(16,8)*2^65]^q",
        },
        {
            "claim": "intrinsic_full_table_test",
            "criterion": "each support-stratum even part has Fourier degree at most two",
            "m3_all_tables": True,
        },
        {
            "claim": "intrinsic_current_test",
            "criterion": "each support-stratum odd part has Fourier degree at most one",
            "linear_forms": ["0", "+/-x_i", "(+/-x_i+/-x_j)/2"],
            "phase_family_count": "B_d^q",
            "two_input_complete_count": "B_2^q=512^q",
        },
    ]


def build_firewall_rows() -> list[dict[str, Any]]:
    return [{"claim": name, "proved": False} for name in FIREWALL_NAMES]


def build_certificate() -> dict[str, Any]:
    monomial_rows = build_monomial_rows()
    histogram_rows = build_signed_cube_histogram()
    current_rows = build_current_rows()
    dimension_rows = build_dimension_rows()
    stratum_rows = build_stratum_rows()
    current_count_rows = build_current_count_rows()
    phase_rows = build_phase_rows()
    analytic_rows = build_analytic_rows()
    firewall_rows = build_firewall_rows()
    summary = {
        "m3_admitted": admitted_dimension(3),
        "m3_ternary_table_count": 2 ** (3**3),
        "m4_admitted": sum(1 for row in monomial_rows if row["admitted"]),
        "m4_total": len(monomial_rows),
        "m4_boolean_corner_eligible": sum(
            row["truth_table_count"] for row in histogram_rows if row["eligible"]
        ),
        "m4_ternary_table_count": math.comb(16, 8) * 2**65,
        "two_input_current_tables": sum(1 for row in current_rows if row["eligible"]),
        "two_input_disallowed_nonzero": sum(
            row["disallowed_nonzero_count"] for row in current_rows
        ),
        "B_2": current_table_count(2),
        "B_3": current_table_count(3),
        "phase_pi_mass_numerator": phase_rows[0]["phase_mass_numerator"],
        "phase_fixture_pass_count": sum(1 for row in phase_rows if row["pass"]),
    }
    all_pass = (
        sum(
            len(rows)
            for rows in (
                monomial_rows,
                histogram_rows,
                current_rows,
                dimension_rows,
                stratum_rows,
                current_count_rows,
                phase_rows,
                analytic_rows,
                firewall_rows,
            )
        ) == ROW_COUNT
        and summary["m3_admitted"] == 27
        and summary["m3_ternary_table_count"] == 2**27
        and summary["m4_admitted"] == 80
        and summary["m4_boolean_corner_eligible"] == math.comb(16, 8)
        and summary["two_input_current_tables"] == 512
        and summary["two_input_disallowed_nonzero"] == 0
        and summary["B_2"] == 512
        and summary["B_3"] == 36_700_160
        and all(
            row["pi_numerators"] == row["recovered_pi_numerators"]
            and row["phase_mass_numerator"] * row["q"] == row["common_denominator"]
            and row["pass"] is True
            for row in phase_rows
        )
        and summary["phase_pi_mass_numerator"] == 20
        and summary["phase_fixture_pass_count"] == 8
        and all(
            row["brute_M_k"] == row["M_k"]
            for row in stratum_rows
            if row["brute_checked"]
        )
        and all(row["proved"] is False for row in firewall_rows)
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "title": TITLE,
        "epistemic_role": EPISTEMIC_ROLE,
        "row_partition": list(ROW_PARTITION),
        "row_count": ROW_COUNT,
        "monomial_rows": monomial_rows,
        "signed_cube_histogram": histogram_rows,
        "current_table_rows": current_rows,
        "dimension_rows": dimension_rows,
        "stratum_rows": stratum_rows,
        "current_count_rows": current_count_rows,
        "phase_rows": phase_rows,
        "analytic_rows": analytic_rows,
        "firewall_rows": firewall_rows,
        "mutation_names": list(MUTATION_NAMES),
        "summary": summary,
        "all_pass": all_pass,
    }


def _local_semantic_verify(value: Any) -> bool:
    """Independent verifier used by the builder-free validation path."""

    from fractions import Fraction as local_fraction
    from itertools import product as local_product
    from math import comb as local_comb

    def is_int(item: Any) -> bool:
        return type(item) is int and type(item) is not bool

    def same(left: Any, right: Any) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(same(left[key], right[key]) for key in left)
        if type(left) is list:
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        return left == right

    def keys(item: Any, expected: tuple[str, ...]) -> bool:
        return type(item) is dict and tuple(item) == expected

    top_keys = (
        "schema_version",
        "title",
        "epistemic_role",
        "row_partition",
        "row_count",
        "monomial_rows",
        "signed_cube_histogram",
        "current_table_rows",
        "dimension_rows",
        "stratum_rows",
        "current_count_rows",
        "phase_rows",
        "analytic_rows",
        "firewall_rows",
        "mutation_names",
        "summary",
        "all_pass",
    )
    if not keys(value, top_keys):
        return False
    if not (
        is_int(value["schema_version"])
        and value["schema_version"] == 1
        and type(value["title"]) is str
        and value["title"] == "Odd-Parity Terminal-Log Möbius Compiler and the Complete Three-Shift Table Law"
        and type(value["epistemic_role"]) is str
        and value["epistemic_role"] == "finite_exact_algebra_not_analytic_proof"
        and type(value["row_partition"]) is list
        and all(is_int(item) for item in value["row_partition"])
        and value["row_partition"] == [81, 17, 512, 8, 8, 8, 8, 8, 8]
        and is_int(value["row_count"])
        and value["row_count"] == 658
        and type(value["all_pass"]) is bool
        and value["all_pass"] is True
    ):
        return False

    monomials = value["monomial_rows"]
    expected_alphas = list(local_product((0, 1, 2), repeat=4))
    if type(monomials) is not list or len(monomials) != 81:
        return False
    for row, alpha in zip(monomials, expected_alphas):
        if not keys(row, ("alpha", "odd_count", "admitted", "channel")):
            return False
        odd_count = alpha.count(1)
        admitted = odd_count == 0 or odd_count == 2 or odd_count % 2 == 1
        channel = (
            "squarefree_density" if odd_count == 0 else
            "rh393_two_odd" if odd_count == 2 else
            "tao_teravainen_odd_total_power" if odd_count % 2 == 1 else
            "outside_even_four_or_more"
        )
        if not (
            same(row["alpha"], list(alpha))
            and is_int(row["odd_count"])
            and row["odd_count"] == odd_count
            and type(row["admitted"]) is bool
            and row["admitted"] is admitted
            and type(row["channel"]) is str
            and row["channel"] == channel
        ):
            return False

    histogram = value["signed_cube_histogram"]
    if type(histogram) is not list or len(histogram) != 17:
        return False
    scanned = [0] * 17
    negative_parity_mask = 0
    for index, epsilon in enumerate(local_product((-1, 1), repeat=4)):
        parity = epsilon[0] * epsilon[1] * epsilon[2] * epsilon[3]
        if parity == -1:
            negative_parity_mask |= 1 << index
    for table_id in range(1 << 16):
        scanned[(table_id ^ negative_parity_mask).bit_count()] += 1
    for plus_count, row in enumerate(histogram):
        if not keys(row, ("transformed_plus_count", "signed_cube_numerator", "truth_table_count", "eligible")):
            return False
        if not (
            is_int(row["transformed_plus_count"])
            and row["transformed_plus_count"] == plus_count
            and is_int(row["signed_cube_numerator"])
            and row["signed_cube_numerator"] == 2 * plus_count - 16
            and is_int(row["truth_table_count"])
            and row["truth_table_count"] == scanned[plus_count]
            and type(row["eligible"]) is bool
            and row["eligible"] is (plus_count == 8)
        ):
            return False

    current_rows = value["current_table_rows"]
    if type(current_rows) is not list or len(current_rows) != 512:
        return False
    points = list(local_product((-1, 0, 1), repeat=2))
    point_index = {point: index for index, point in enumerate(points)}
    local_weights = {
        0: {-1: local_fraction(0), 0: local_fraction(1), 1: local_fraction(0)},
        1: {-1: local_fraction(-1, 2), 0: local_fraction(0), 1: local_fraction(1, 2)},
        2: {-1: local_fraction(1, 2), 0: local_fraction(-1), 1: local_fraction(1, 2)},
    }
    for table_id, row in enumerate(current_rows):
        if not keys(
            row,
            (
                "table_id",
                "corner_alternating_numerator",
                "nonzero_coefficient_count",
                "maximum_odd_support",
                "disallowed_nonzero_count",
                "eligible",
                "terminal_limit_numerator",
            ),
        ):
            return False

        def sign(point: tuple[int, int]) -> int:
            return 1 if (table_id >> point_index[point]) & 1 else -1

        alternating = sign((1, 1)) - sign((1, -1)) - sign((-1, 1)) + sign((-1, -1))
        nonzero = 0
        maximum = 0
        disallowed = 0
        for alpha in local_product((0, 1, 2), repeat=2):
            coefficient = sum(
                local_fraction(sign((x, y)))
                * local_weights[alpha[0]][x]
                * local_weights[alpha[1]][y]
                for x, y in points
            )
            if coefficient:
                odd_support = 1 + alpha.count(1)
                nonzero += 1
                maximum = max(maximum, odd_support)
                if not (odd_support == 2 or odd_support % 2 == 1):
                    disallowed += 1
        if not (
            is_int(row["table_id"])
            and row["table_id"] == table_id
            and is_int(row["corner_alternating_numerator"])
            and row["corner_alternating_numerator"] == alternating
            and is_int(row["nonzero_coefficient_count"])
            and row["nonzero_coefficient_count"] == nonzero
            and is_int(row["maximum_odd_support"])
            and row["maximum_odd_support"] == maximum
            and is_int(row["disallowed_nonzero_count"])
            and row["disallowed_nonzero_count"] == disallowed == 0
            and type(row["eligible"]) is bool
            and row["eligible"] is (disallowed == 0)
            and is_int(row["terminal_limit_numerator"])
            and row["terminal_limit_numerator"] == 0
        ):
            return False

    dimensions = value["dimension_rows"]
    if type(dimensions) is not list or len(dimensions) != 8:
        return False
    for m, row in enumerate(dimensions, 1):
        expected = {
            "m": m,
            "all_even": 2**m,
            "two_odd": local_comb(m, 2) * 2 ** (m - 2) if m >= 2 else 0,
            "positive_odd": (3**m - 1) // 2,
        }
        expected["admitted"] = expected["all_even"] + expected["two_odd"] + expected["positive_odd"]
        expected["total"] = 3**m
        if not keys(row, ("m", "all_even", "two_odd", "positive_odd", "admitted", "total")) or not same(row, expected):
            return False

    strata = value["stratum_rows"]
    if type(strata) is not list or len(strata) != 8:
        return False
    local_M: list[int] = []
    for k, row in enumerate(strata):
        even = 2 if k == 0 else 2 ** (2 ** (k - 1))
        dictators = 0 if k == 0 else 2 * k
        paired = 4 * local_comb(k, 2) * 2 ** (2 ** (k - 2)) if k >= 2 else 0
        formula_count = even + dictators + paired
        brute_count: int | None = None
        if k <= 4:
            point_count = 1 << k
            if k < 3:
                brute_count = 1 << point_count
            else:
                cube = tuple(local_product((-1, 1), repeat=k))
                masks: list[int] = []
                for support_size in range(3, k + 1, 2):
                    for support in local_product((0, 1), repeat=k):
                        if sum(support) != support_size:
                            continue
                        mask = 0
                        for index, point in enumerate(cube):
                            parity = 1
                            for coordinate, selected in zip(point, support):
                                if selected:
                                    parity *= coordinate
                            if parity == -1:
                                mask |= 1 << index
                        masks.append(mask)
                brute_count = sum(
                    all(
                        (table_id ^ mask).bit_count() == point_count // 2
                        for mask in masks
                    )
                    for table_id in range(1 << point_count)
                )
        expected = {
            "k": k,
            "even_functions": even,
            "signed_dictators": dictators,
            "paired_half_linear": paired,
            "M_k": formula_count,
            "brute_checked": k <= 4,
            "brute_M_k": brute_count,
        }
        if not keys(
            row,
            (
                "k",
                "even_functions",
                "signed_dictators",
                "paired_half_linear",
                "M_k",
                "brute_checked",
                "brute_M_k",
            ),
        ) or not same(row, expected):
            return False
        if k <= 4 and brute_count != formula_count:
            return False
        local_M.append(formula_count)

    counts = value["current_count_rows"]
    if type(counts) is not list or len(counts) != 8:
        return False
    local_B: list[int] = []
    for d, row in enumerate(counts):
        exponents = [local_comb(d, k) for k in range(d + 1)]
        total = 1
        for k, exponent in enumerate(exponents):
            total *= local_M[k] ** exponent
        expected = {"d": d, "stratum_exponents": exponents, "B_d": total}
        if not keys(row, ("d", "stratum_exponents", "B_d")) or not same(row, expected):
            return False
        local_B.append(total)

    phases = value["phase_rows"]
    if type(phases) is not list or len(phases) != 8:
        return False
    pi = [mask.bit_count() + 1 for mask in range(8)]
    theta = [sum(pi[support] for support in range(8) if support & mask == mask) for mask in range(8)]
    recovered_values = []
    for support in range(8):
        recovered_values.append(
            sum(
                (-1) ** subset.bit_count() * theta[support | subset]
                for subset in range(8)
                if subset & support == 0
            )
        )
    for q, row in enumerate(phases, 1):
        expected = {
            "fixture_kind": "synthetic_exact_support_density",
            "q": q,
            "r": q - 1,
            "pi_numerators": list(pi),
            "theta_numerators": list(theta),
            "recovered_pi_numerators": list(recovered_values),
            "common_denominator": 20 * q,
            "phase_mass_numerator": 20,
            "phase_mass": "1/q",
            "pass": True,
        }
        if not keys(
            row,
            (
                "fixture_kind",
                "q",
                "r",
                "pi_numerators",
                "theta_numerators",
                "recovered_pi_numerators",
                "common_denominator",
                "phase_mass_numerator",
                "phase_mass",
                "pass",
            ),
        ) or not same(row, expected):
            return False
        if recovered_values != pi or sum(pi) * q != expected["common_denominator"]:
            return False

    analytic_expected = [
        {
            "claim": "fixed_terminal_quantifiers",
            "m_q": "exact fixed positive integers",
            "shifts": "fixed pairwise-distinct integers",
            "coefficients": "fixed q-periodic coefficients",
            "mobius_extension": "mu_0(t)=mu(t) for integer t>=1 and mu_0(t)=0 for t<=0",
            "coordinates": "z_i(n)=mu_0(n-a_i)",
            "clock": "1<=omega(X)<=X and omega(X)->infinity",
            "terminal_functional": "T_X(P;omega)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) P_(n mod q)(z(n))/n",
        },
        {
            "claim": "odd_total_power_source",
            "source": "Tao-Teravainen Corollary 1.8, PDF page 7",
            "positive_exponents": [1, 2],
            "sum_exponents_odd": True,
            "channel": "every positive odd support",
        },
        {
            "claim": "fixed_affine_phase_bridge",
            "source": "Tao-Teravainen Remark 1.5 and Theorem A.1",
            "appendix_locator": "PDF page 38",
            "substitution": "n=q*t+r",
            "weight": "1/(q*t+r)=1/(q*t)+O(t^-2)",
        },
        {
            "claim": "admitted_supports",
            "alpha_domain": "alpha in {0,1,2}^m",
            "odd_support_definition": "O(alpha)={i:alpha_i=1}",
            "even_support_definition": "E(alpha)={i:alpha_i=2}",
            "rule": "odd_support is 0, 2, or positive odd",
            "first_excluded": 4,
        },
        {
            "claim": "coefficient_limit",
            "survivors": "all-even channels only",
            "formula": "sum_r sum_{alpha in {0,2}^m} c_alpha(r) Theta_{q,r}(E(alpha))",
            "theta_classes": "B_p(E)=distinct {a_i mod p^2:i in E}; nu_p=|B_p(E)|; tau_p(r)=#{b in B_p(E):b mod p=r mod p}",
            "theta_formula": "q^-1 product_(p not|q)(1-nu_p/p^2) product_(p||q)(1-tau_p(r)/p) product_(p^2|q)1_(r mod p^2 notin B_p(E))",
            "theta_mass": "Theta_{q,r}(empty)=1/q and sum_(r mod q)Theta_{q,r}(E)=kappa_E=product_p(1-nu_p/p^2)",
            "odd_zero_source": "local finite-prime CRT and union tail",
            "odd_two_source": "frozen RH393 compiler using RH392 two-form cancellation",
            "cutoff_order": ["P_fixed", "X_to_infinity", "P_to_infinity"],
        },
        {
            "claim": "table_limit",
            "pi_formula": "Pi(U)=sum_{W subset complement(U)}(-1)^|W|Theta(U union W)",
            "formula": "sum_{r,U} Pi_{q,r}(U) average_signs(f_{r,U})",
            "phase_mass": "sum_U Pi_{q,r}(U)=1/q",
            "m3_full_table_families": "2^(27q)",
            "m4_compiler_table_families": "[binom(16,8)*2^65]^q",
        },
        {"claim": "intrinsic_full_table_test", "criterion": "each support-stratum even part has Fourier degree at most two", "m3_all_tables": True},
        {
            "claim": "intrinsic_current_test",
            "criterion": "each support-stratum odd part has Fourier degree at most one",
            "linear_forms": ["0", "+/-x_i", "(+/-x_i+/-x_j)/2"],
            "phase_family_count": "B_d^q",
            "two_input_complete_count": "B_2^q=512^q",
        },
    ]
    if not same(value["analytic_rows"], analytic_expected):
        return False
    firewall_names = [
        "even_odd_support_at_least_four",
        "unrestricted_m_at_least_four_tables",
        "growing_m_q_shifts_masks_or_coefficients",
        "effective_uniform_rate",
        "ordinary_cesaro",
        "maximum_before_limit",
        "generic_graph_coupled_capacity",
        "operator_trace_zero_or_gate",
    ]
    firewall_expected = [{"claim": name, "proved": False} for name in firewall_names]
    if not same(value["firewall_rows"], firewall_expected):
        return False
    mutation_expected = [
        "title", "role", "schema_version_float", "row_partition_float", "row_count",
        "monomial_alpha", "monomial_odd_count", "monomial_admitted", "monomial_channel",
        "histogram_numerator", "histogram_count", "histogram_eligible", "current_table_id",
        "current_corner_alt", "current_eligible", "dimension_admitted", "dimension_total",
        "stratum_count", "current_count", "phase_pi", "phase_theta", "phase_recovered",
        "analytic_clock", "analytic_source", "analytic_phase_bridge", "analytic_support_rule",
        "analytic_limit", "firewall_true", "summary_m3", "summary_m4",
        "summary_table_count", "summary_phase_mass",
    ]
    if not same(value["mutation_names"], mutation_expected):
        return False
    expected_summary = {
        "m3_admitted": 27,
        "m3_ternary_table_count": 2**27,
        "m4_admitted": 80,
        "m4_total": 81,
        "m4_boolean_corner_eligible": 12870,
        "m4_ternary_table_count": 12870 * 2**65,
        "two_input_current_tables": 512,
        "two_input_disallowed_nonzero": 0,
        "B_2": 512,
        "B_3": 36_700_160,
        "phase_pi_mass_numerator": 20,
        "phase_fixture_pass_count": 8,
    }
    if not keys(value["summary"], tuple(expected_summary)) or not same(value["summary"], expected_summary):
        return False
    return (
        sum(1 for row in monomials if row["admitted"]) == 80
        and sum(row["truth_table_count"] for row in histogram if row["eligible"]) == 12870
        and all(row["pass"] is True for row in phases)
        and all(row["phase_mass_numerator"] * row["q"] == row["common_denominator"] for row in phases)
        and all(row["disallowed_nonzero_count"] == 0 for row in current_rows)
        and local_B[2] == 512
        and local_B[3] == 36_700_160
    )


def _make_certificate_verifier():
    independent_semantic_verify = _local_semantic_verify

    def verifier(value: Any, *, compare_fresh: bool = True) -> bool:
        if type(compare_fresh) is not bool:
            return False
        if not independent_semantic_verify(value):
            return False
        if compare_fresh:
            return exact_equal(value, build_certificate())
        return True

    return verifier


verify_certificate = _make_certificate_verifier()
del _make_certificate_verifier


def mutate_certificate(value: dict[str, Any], name: str) -> dict[str, Any]:
    if type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    changed = deepcopy(value)
    actions = {
        "title": lambda: changed.__setitem__("title", "wrong"),
        "role": lambda: changed.__setitem__("epistemic_role", "analytic_proof"),
        "schema_version_float": lambda: changed.__setitem__("schema_version", 1.0),
        "row_partition_float": lambda: changed["row_partition"].__setitem__(0, 81.0),
        "row_count": lambda: changed.__setitem__("row_count", 657),
        "monomial_alpha": lambda: changed["monomial_rows"][0]["alpha"].__setitem__(0, 1),
        "monomial_odd_count": lambda: changed["monomial_rows"][0].__setitem__("odd_count", 1),
        "monomial_admitted": lambda: changed["monomial_rows"][40].__setitem__("admitted", True),
        "monomial_channel": lambda: changed["monomial_rows"][-1].__setitem__("channel", "rh393_two_odd"),
        "histogram_numerator": lambda: changed["signed_cube_histogram"][8].__setitem__("signed_cube_numerator", 2),
        "histogram_count": lambda: changed["signed_cube_histogram"][8].__setitem__("truth_table_count", 12869),
        "histogram_eligible": lambda: changed["signed_cube_histogram"][7].__setitem__("eligible", True),
        "current_table_id": lambda: changed["current_table_rows"][0].__setitem__("table_id", 1),
        "current_corner_alt": lambda: changed["current_table_rows"][0].__setitem__("corner_alternating_numerator", 2),
        "current_eligible": lambda: changed["current_table_rows"][0].__setitem__("eligible", False),
        "dimension_admitted": lambda: changed["dimension_rows"][3].__setitem__("admitted", 81),
        "dimension_total": lambda: changed["dimension_rows"][2].__setitem__("total", 26),
        "stratum_count": lambda: changed["stratum_rows"][4].__setitem__("M_k", 647),
        "current_count": lambda: changed["current_count_rows"][3].__setitem__("B_d", 36_700_159),
        "phase_pi": lambda: changed["phase_rows"][0]["pi_numerators"].__setitem__(0, 2),
        "phase_theta": lambda: changed["phase_rows"][0]["theta_numerators"].__setitem__(0, 19),
        "phase_recovered": lambda: changed["phase_rows"][0]["recovered_pi_numerators"].__setitem__(0, 2),
        "analytic_clock": lambda: changed["analytic_rows"][0].__setitem__("clock", "omega=X"),
        "analytic_source": lambda: changed["analytic_rows"][1].__setitem__("source", "unlocked"),
        "analytic_phase_bridge": lambda: changed["analytic_rows"][2].__setitem__("substitution", "n=t+r"),
        "analytic_support_rule": lambda: changed["analytic_rows"][3].__setitem__("first_excluded", 6),
        "analytic_limit": lambda: changed["analytic_rows"][4].__setitem__("survivors", "all channels"),
        "firewall_true": lambda: changed["firewall_rows"][0].__setitem__("proved", True),
        "summary_m3": lambda: changed["summary"].__setitem__("m3_admitted", 26),
        "summary_m4": lambda: changed["summary"].__setitem__("m4_admitted", 81),
        "summary_table_count": lambda: changed["summary"].__setitem__("m4_boolean_corner_eligible", 12871),
        "summary_phase_mass": lambda: changed["summary"].__setitem__("phase_pi_mass_numerator", 19),
    }
    actions[name]()
    return changed


def certificate_bytes() -> bytes:
    return canonical_json_bytes(build_certificate())
