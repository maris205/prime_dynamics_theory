#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V44 transition artifact."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from functools import partial
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_TRANSITION_GCD_REDUCTION_SPLITS_THE_PRIMARY_ALIAS_INTO_"
    "PRINCIPAL_RAMANUJAN_MEAN_CENTERED_RECIPROCAL_VARIANCE_PAID_"
    "UNIT_CORRECTION_AND_PAID_BACKGROUND_WITH_THE_STRICT_ENDPOINT_CLOCK"
)


CONTRACT_ITEMS = (
    ("schema_version", "V44_TRANSITION_RECIPROCAL_VARIANCE_V1"),
    ("artifact_name", "bridge_b_transition_reciprocal_variance_and_ramanujan_mean.md"),
    ("baseline_commit", "be9d783536eeec36ab1c5a95525523f762c1d4d3"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "TRANSITION_MEAN_VARIANCE_THEN_LONG_MOBIUS_WITH_V42_GATE_B_PARALLEL"),
    ("route_position", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B"),
    ("route_advance", "YES"),
    ("conditional_bridge_advance", "YES"),
    ("arithmetic_advance", False),
    ("fixed_atom_credit", 0),
    ("strict_1_over_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", False),
    ("numbered_release", "NO"),
    ("H", "x^(21/32)"),
    ("Q", "x^(1/3)"),
    ("U", "x^(133/400)"),
    ("Y0", "H/(4Q)=x^(31/96+o(1))"),
    ("P", "Q^2/H=x^(1/96)"),
    ("reduced_modulus_range", "Q^(31/32+o(1))_to_Q^(399/400+o(1))"),
    ("transition_dual_length", "x^(23/2400+o(1))"),
    ("transition_split", "principal_Ramanujan_mean_plus_centered_reciprocal_variance"),
    ("generic_variance", "P^2*x^o=x^(1/48+o(1))"),
    ("generic_output", "x^(5/3+o(1))"),
    ("variance_gate", "P^2*x^(-kappa+o(1))_with_kappa>1/200"),
    ("mean_gate", "x^(5/3-delta_M+o(1))_with_delta_M>1/400"),
    ("unit_correction", "x^(319/192+o(1))"),
    ("background_output", "x^(7171/4800+o(1))"),
    ("first_fatal", "NO_LITERAL_THEOREM_GIVES_FIXED_POWER_FOR_THE_PRINCIPAL_RAMANUJAN_MEAN_OR_CENTERED_PRIME_SHORT_INTEGER_RECIPROCAL_VARIANCE_AT_REDUCED_MODULI_Q_POWER_31_OVER_32_TO_Q_POWER_399_OVER_400"),
)


REGISTRY_ITEMS = (
    ("V44_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V44_ROUTE_ADVANCE", "YES"),
    ("V44_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V44_ARITHMETIC_ADVANCE", "NO"),
    ("V44_FIXED_ATOM_CREDIT", "0"),
    ("V44_STRICT_1_OVER_400", "UNPAID"),
    ("V44_L2", "NONE"),
    ("V44_TPC_207_TRIGGER", "false"),
    ("V44_NUMBERED_RELEASE", "NO"),
    ("V44_DERIVATION_STATUS", "COHERENT_AFTER_TRANSITION_EXTRACTION_GCD_REDUCTION_MEAN_VARIANCE_SPLIT_AND_TWO_CORRECTION_PAYMENTS"),
    ("V44_ASSUMPTION_POLICY", "PRINCIPAL_MEAN_AND_RECIPROCAL_VARIANCE_REMAIN_TWO_EXPLICIT_OPEN_ENDPOINT_THEOREMS"),
    ("V44_SELECTED_RESEARCH_ROUTE", "TRANSITION_MEAN_AND_VARIANCE_FIRST__BALANCED_AND_REVERSE_TYPE_I_SECOND__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE"),
    ("V44_V43_TRANSITION_ALIAS", "RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE"),
    ("V44_Q_NONUNIT_IN_D", "ABSENT_EXACT_BECAUSE_D_LE_U_LT_Q"),
    ("V44_Q_NONUNIT_IN_M", "ABSENT_EXACT_BECAUSE_ABS_M_LE_2UQ_OVER_H_LT_Q"),
    ("V44_GCD_REDUCTION", "PROVED_EXACT_D_EQUALS_GS_M_EQUALS_GN"),
    ("V44_GCD_PHASE_CANCELLATION", "PROVED_E_D_MU_QBAR_EQUALS_E_S_NU_QBAR"),
    ("V44_GCD_CUTOFF_CANCELLATION", "PROVED_PSI_HM_OVER_DQ_EQUALS_PSI_HN_OVER_SQ"),
    ("V44_REDUCED_MODULUS_RANGE", "Q_POWER_31_OVER_32_TO_Q_POWER_399_OVER_400"),
    ("V44_REDUCED_DUAL_LENGTH", "X_POWER_23_OVER_2400_PLUS_O1"),
    ("V44_LAMBDA_S_ENVELOPE", "X_O1_OVER_S"),
    ("V44_RECIPROCAL_OCCUPANCY", "PROVED_EXACT_R_EQUALS_N_Q_INVERSE_MOD_S"),
    ("V44_MEAN_CENTERED_SPLIT", "PROVED_EXACT_BEFORE_OUTER_ABSOLUTE"),
    ("V44_PRINCIPAL_TERM", "PROVED_EXACT_RAMANUJAN_SUM_PAIRING"),
    ("V44_CENTERED_CHARACTER_PARSEVAL", "PROVED_EXACT_NONPRINCIPAL_CHARACTER_ENERGY"),
    ("V44_RECIPROCAL_VARIANCE_GENERIC", "PROVED_LARGE_SIEVE_P_SQUARED_X_O1"),
    ("V44_RECIPROCAL_VARIANCE_GENERIC_EXPONENT", "1_OVER_48"),
    ("V44_CENTERED_GENERIC_OUTPUT", "X_POWER_5_OVER_3_PLUS_O1"),
    ("V44_CENTERED_GENERIC_ENDPOINT_DEFICIT", "1_OVER_400"),
    ("V44_RECIPROCAL_VARIANCE_GATE", "OPEN_P_SQUARED_X_MINUS_KAPPA_WITH_KAPPA_GREATER_THAN_1_OVER_200"),
    ("V44_RECIPROCAL_VARIANCE_IDEAL", "P_X_O1"),
    ("V44_RECIPROCAL_VARIANCE_IDEAL_OUTPUT", "X_POWER_319_OVER_192_PLUS_O1"),
    ("V44_RECIPROCAL_VARIANCE_IDEAL_MARGIN", "13_OVER_4800"),
    ("V44_PHYSICAL_Q_DIVIDES_U_CORRECTION", "PROVED_ADDITIVE_LARGE_SIEVE_X_POWER_319_OVER_192_PLUS_O1"),
    ("V44_BACKGROUND_Q_RETENTION", "PROVED_EXACT_REDUCED_DENOMINATOR_STILL_CONTAINS_Q"),
    ("V44_BACKGROUND_COEFFICIENT_ENERGY", "H_INVERSE_X_O1"),
    ("V44_BACKGROUND_OUTPUT", "PROVED_X_POWER_7171_OVER_4800_PLUS_O1"),
    ("V44_BACKGROUND_MARGIN", "817_OVER_4800"),
    ("V44_PRINCIPAL_MEAN_AP_FORM", "PROVED_EXACT_C_S_DIVISOR_EXPANSION"),
    ("V44_PRINCIPAL_MEAN_ABSOLUTE_CEILING", "X_POWER_5_OVER_3_PLUS_O1"),
    ("V44_PRINCIPAL_MEAN_ENDPOINT_DEFICIT", "1_OVER_400"),
    ("V44_PRINCIPAL_MEAN_GATE", "OPEN_X_POWER_5_OVER_3_MINUS_DELTA_M_WITH_DELTA_M_GREATER_THAN_1_OVER_400"),
    ("V44_TRANSITION_CONDITIONAL_COMPILER", "PROVED_MEAN_AND_VARIANCE_GATES_PAY_FULL_TRANSITION"),
    ("V44_LONG_BALANCED_WINDOW", "OPEN_D_GT_U_AND_K_GT_U"),
    ("V44_LONG_REVERSE_TYPE_I_WINDOW", "OPEN_D_GT_U_AND_K_LE_U"),
    ("V44_V42_GATE_B", "RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE"),
    ("V44_BFI_GENERIC_LARGE_SIEVE", "SOURCE_BACKED_GENERIC_P_SQUARED_CEILING_ONLY"),
    ("V44_BFI_BDH_TO_FIXED_POWER", "STOP_SCOPED_LOG_SAVING_DOES_NOT_PAY_1_OVER_400"),
    ("V44_MAYNARD_LARGE_MODULI_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_RESIDUE_FACTORIZED_MODULI_MAX_RELATIVE_EXPONENT_11_OVER_21_NOT_ALL_RESIDUE_VARIANCE_AT_31_OVER_32_TO_399_OVER_400"),
    ("V44_DONG_ROBLES_ZEINDLER_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_A_B_TWO_ARRAY_FORM_NOT_MOVING_NU_OR_RECIPROCAL_FOURTH_MOMENT"),
    ("V44_PASCADI_HORIZONTAL_DIRECT_ATTACHMENT", "STOP_SCOPED_POST_EMITTER_LOCAL_FORM_NOT_TRANSITION_MEAN_OR_VARIANCE_COMPILER"),
    ("V44_DIRECT_PRIMARY_SOURCE_FOR_TWO_TRANSITION_GATES", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10"),
    ("V44_FIRST_FATAL", "NO_LITERAL_THEOREM_GIVES_FIXED_POWER_FOR_THE_PRINCIPAL_RAMANUJAN_MEAN_OR_CENTERED_PRIME_SHORT_INTEGER_RECIPROCAL_VARIANCE_AT_REDUCED_MODULI_Q_POWER_31_OVER_32_TO_Q_POWER_399_OVER_400"),
    ("V44_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B_TRANSITION_SPLIT_INTO_TWO_ENDPOINT_GATES_LONG_MOBIUS_SPAN_OPEN"),
    ("V44_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V44_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B"),
)


EXPECTED_REGISTRY_SHA256 = "d6330cda90981b374d594c0d4b1dc209a5599b7d4cbf5caac6ec753c5adbe503"


SOURCE_ITEMS = (
    ("BFI", "Acta_Mathematica_156_1986_Theorem_0_and_equation_1_6"),
    ("MAYNARD_FIXED", "arXiv:2006.06572v2_Theorem_1_1"),
    ("DONG_ROBLES_ZEINDLER", "arXiv:2601.00292v1_main_bilinear_theorem"),
    ("PASCADI_HORIZONTAL", "arXiv:2404.04239v3_Corollaries_17_18"),
    ("VAUGHAN_MAXIMAL_BV", "Corollary_1_1_1_maximal_Bombieri_Vinogradov"),
    ("IWANIEC_ROSSER", "Acta_Arithmetica_36_1980_Theorem_1"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_transition_reciprocal_variance_and_ramanujan_mean.md", "053ae6a18740a2e81d754c4ecce7af1a00ecfe331f7d5d4991945889f14c9920"),
    ("research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md", "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a"),
    ("research/tpc-big-road/tpc_bridge_b_proper_factor_poisson_transference_checker.py", "ff48df45275588f6f27572962dd565db1d8e4475daa6d52c2b382ad068d1ab76"),
    ("research/tpc-big-road/bridge_b_mesoscopic_covariance.md", "e9838ebee8aa027421dad9bc2d05cb7b3655d2de413da0aa11aa143095636c37"),
    ("research/tpc-big-road/tpc_bridge_b_mesoscopic_covariance_checker.py", "b6350ce0f7ed38dd7671f5076a0c26bf82bb57850ec35505c4cfec3239ad336e"),
)


def _make_trusted_runner(
    maximum_claim_seed=MAXIMUM_CLAIM,
    contract_seed=CONTRACT_ITEMS,
    registry_seed=REGISTRY_ITEMS,
    registry_digest_seed=EXPECTED_REGISTRY_SHA256,
    source_seed=SOURCE_ITEMS,
    dependency_seed=DEPENDENCIES,
    root_seed=str(Path(__file__).resolve().parents[2]),
    failure_type=CheckFailure,
    fraction_type=Fraction,
    path_type=Path,
    path_is_file=Path.is_file,
    path_read_bytes=Path.read_bytes,
    sha256_fn=hashlib.sha256,
    gcd_fn=math.gcd,
    dict_type=dict,
    list_type=list,
    tuple_type=tuple,
    set_type=set,
    str_type=str,
    int_type=int,
    bool_type=bool,
    type_fn=type,
    len_fn=len,
    range_fn=range,
    sum_fn=sum,
    abs_fn=abs,
    min_fn=min,
    max_fn=max,
    all_fn=all,
    enumerate_fn=enumerate,
    sorted_fn=sorted,
    pow_fn=pow,
):
    literal_maximum_claim = maximum_claim_seed
    literal_contract = tuple_type(contract_seed)
    literal_registry = tuple_type(registry_seed)
    literal_registry_digest = registry_digest_seed
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(root_seed)

    def exact_str(value: object) -> bool:
        return type_fn(value) is str_type

    def canonical_bytes(raw: bytes) -> bytes:
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    def digest_bytes(raw: bytes) -> str:
        return sha256_fn(raw).hexdigest()

    def registry_bytes(candidate: tuple[tuple[str, str], ...]) -> bytes:
        return b"".join((key + "=" + value + "\n").encode("utf-8") for key, value in candidate)

    def registry_digest(candidate: tuple[tuple[str, str], ...]) -> str:
        return digest_bytes(registry_bytes(candidate))

    def require_rows(candidate: object, expected: tuple, label: str, string_values: bool) -> None:
        if type_fn(candidate) is not tuple_type or len_fn(candidate) != len_fn(expected):
            raise failure_type(label + " shape changed")
        keys = list_type()
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type(label + " row shape changed")
            key, value = row
            if not exact_str(key):
                raise failure_type(label + " key type changed")
            if string_values and not exact_str(value):
                raise failure_type(label + " value type changed")
            keys.append(key)
        if len_fn(set_type(keys)) != len_fn(keys):
            raise failure_type(label + " keys not unique")
        if candidate != expected:
            raise failure_type(label + " changed")

    def validate_contract(candidate: object) -> None:
        require_rows(candidate, literal_contract, "contract", False)
        if dict_type(candidate).get("maximum_claim") != literal_maximum_claim:
            raise failure_type("maximum claim contract seed changed")

    def validate_registry(candidate: object) -> None:
        require_rows(candidate, literal_registry, "registry", True)
        if dict_type(candidate).get("V44_MAXIMUM_CLAIM") != literal_maximum_claim:
            raise failure_type("maximum claim registry seed changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry literal digest changed")

    def validate_sources(candidate: object) -> None:
        require_rows(candidate, literal_sources, "source", True)

    def validate_dependencies(candidate: object) -> None:
        require_rows(candidate, literal_dependencies, "dependency", True)
        for relative, expected_hash in candidate:
            path = repo_root / relative
            if not path_is_file(path):
                raise failure_type("dependency missing: " + relative)
            actual = digest_bytes(canonical_bytes(path_read_bytes(path)))
            if actual != expected_hash:
                raise failure_type("dependency hash changed: " + relative)

    def factorization(n: int) -> tuple[tuple[int, int], ...]:
        if type_fn(n) is not int_type or n < 1:
            raise failure_type("factorization input changed")
        value = n
        rows = list_type()
        p = 2
        while p * p <= value:
            exponent = 0
            while value % p == 0:
                value //= p
                exponent += 1
            if exponent:
                rows.append((p, exponent))
            p += 1
        if value > 1:
            rows.append((value, 1))
        return tuple_type(rows)

    def mobius(n: int) -> int:
        rows = factorization(n)
        if not all_fn(exponent == 1 for _, exponent in rows):
            return 0
        return -1 if len_fn(rows) % 2 else 1

    def divisors(n: int) -> tuple[int, ...]:
        return tuple_type(d for d in range_fn(1, n + 1) if n % d == 0)

    def ramanujan_sum(s: int, u: int) -> int:
        common = gcd_fn(s, u)
        return sum_fn((d * mobius(s // d) for d in divisors(common)), 0)

    def reciprocal_occupancy(s: int, primes: tuple[int, ...], numerators: tuple[int, ...]) -> tuple[int, ...]:
        counts = [0 for _ in range_fn(s)]
        for q in primes:
            inverse_q = pow_fn(q, -1, s)
            for n in numerators:
                residue = n * inverse_q % s
                counts[residue] += 1
        return tuple_type(counts[r] for r in range_fn(1, s))

    def finite_items() -> tuple[tuple[str, object], ...]:
        q, d, m, u = 7, 10, 2, 1
        g = gcd_fn(d, abs_fn(m))
        s = d // g
        n = m // g
        phase_full = fraction_type(m * u * pow_fn(q, -1, d), d)
        phase_reduced = fraction_type(n * u * pow_fn(q, -1, s), s)
        phase_wrong_g = fraction_type(g * n * u * pow_fn(q, -1, s), s)
        if (g, s, n) != (2, 5, 1):
            raise failure_type("gcd reduction changed")
        if (phase_full - phase_reduced).denominator != 1:
            raise failure_type("gcd phase cancellation changed")
        if (phase_wrong_g - phase_reduced).denominator == 1:
            raise failure_type("false g phase was not rejected")

        occupancy = reciprocal_occupancy(5, (7, 11), (1, 2))
        if occupancy != (2, 1, 1, 0):
            raise failure_type("reciprocal occupancy changed")
        mean = fraction_type(sum_fn(occupancy), len_fn(occupancy))
        uncentered = sum_fn((value * value for value in occupancy), 0)
        variance = sum_fn(((fraction_type(value) - mean) ** 2 for value in occupancy), fraction_type(0))
        if (mean, uncentered, variance) != (1, 6, 2):
            raise failure_type("mean variance split changed")

        ramanujan = tuple_type(ramanujan_sum(6, value) for value in range_fn(6))
        if ramanujan != (2, 1, -1, -2, -1, 1):
            raise failure_type("Ramanujan divisor expansion changed")

        background = fraction_type(4, 6 * 11)
        if background != fraction_type(2, 33) or background.denominator % 11 != 0:
            raise failure_type("background q retention changed")

        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        u_exp = fraction_type(133, 400)
        y_exp = h_exp - q_exp
        relative_low = y_exp / q_exp
        relative_high = u_exp / q_exp
        dual_exp = u_exp + q_exp - h_exp
        p_exp = 2 * q_exp - h_exp
        p_square_exp = 2 * p_exp
        generic_output = h_exp + 1 + p_exp
        target_exp = fraction_type(1997, 1200)
        endpoint_deficit = generic_output - target_exp
        kappa_threshold = 2 * endpoint_deficit
        ideal_output = h_exp + 1 + p_exp / 2
        ideal_margin = target_exp - ideal_output
        background_output = h_exp / 2 + fraction_type(1, 2) + q_exp + u_exp
        background_margin = target_exp - background_output
        sparse_background = 1 + h_exp / 2
        lower_fourth_moment = 4 * q_exp - 2 * h_exp

        actual = (
            y_exp, relative_low, relative_high, dual_exp,
            p_exp, p_square_exp, lower_fourth_moment,
            generic_output, endpoint_deficit, kappa_threshold,
            ideal_output, ideal_margin, background_output,
            background_margin, sparse_background,
        )
        expected = (
            fraction_type(31, 96), fraction_type(31, 32), fraction_type(399, 400),
            fraction_type(23, 2400), fraction_type(1, 96), fraction_type(1, 48),
            fraction_type(1, 48), fraction_type(5, 3), fraction_type(1, 400),
            fraction_type(1, 200), fraction_type(319, 192), fraction_type(13, 4800),
            fraction_type(7171, 4800), fraction_type(817, 4800), fraction_type(85, 64),
        )
        if actual != expected:
            raise failure_type("rational exponent ledger changed")

        constant_occupancy = (3, 3, 3, 3)
        constant_mean = fraction_type(sum_fn(constant_occupancy), 4)
        constant_variance = sum_fn(
            ((fraction_type(value) - constant_mean) ** 2 for value in constant_occupancy),
            fraction_type(0),
        )
        if constant_variance != 0 or constant_mean != 3:
            raise failure_type("principal fluctuation independence changed")

        return (
            ("gcd_g_s_n", (g, s, n)),
            ("phase_full", str_type(phase_full)),
            ("phase_reduced", str_type(phase_reduced)),
            ("phase_wrong_g", str_type(phase_wrong_g)),
            ("reciprocal_occupancy", occupancy),
            ("occupancy_mean", str_type(mean)),
            ("occupancy_uncentered_energy", uncentered),
            ("occupancy_centered_variance", str_type(variance)),
            ("ramanujan_s6", ramanujan),
            ("background_fraction", str_type(background)),
            ("reduced_lower_exponent", str_type(y_exp)),
            ("relative_lower_exponent", str_type(relative_low)),
            ("relative_upper_exponent", str_type(relative_high)),
            ("dual_exponent", str_type(dual_exp)),
            ("P_exponent", str_type(p_exp)),
            ("P_squared_exponent", str_type(p_square_exp)),
            ("generic_output_exponent", str_type(generic_output)),
            ("endpoint_deficit", str_type(endpoint_deficit)),
            ("kappa_threshold", str_type(kappa_threshold)),
            ("ideal_output_exponent", str_type(ideal_output)),
            ("ideal_margin", str_type(ideal_margin)),
            ("background_output_exponent", str_type(background_output)),
            ("background_margin", str_type(background_margin)),
            ("sparse_background_exponent", str_type(sparse_background)),
            ("constant_mean", str_type(constant_mean)),
            ("constant_variance", str_type(constant_variance)),
        )

    def mutated_value(value: object) -> object:
        if type_fn(value) is bool_type:
            return not value
        if type_fn(value) is int_type:
            return value + 1
        if type_fn(value) is str_type:
            return value + "__MUTATED"
        if type_fn(value) is tuple_type:
            return value + ("__MUTATED",)
        raise failure_type("unsupported mutation value")

    def wrong_type(value: object) -> object:
        if type_fn(value) is bool_type:
            return 1
        if type_fn(value) is int_type:
            return True
        if type_fn(value) is str_type:
            return (value,)
        if type_fn(value) is tuple_type:
            return list_type(value)
        raise failure_type("unsupported wrong type")

    def replace_row(rows: tuple, index: int, row: tuple) -> tuple:
        mutable = list_type(rows)
        mutable[index] = row
        return tuple_type(mutable)

    def must_reject(action, label: str, labels: list[str]) -> None:
        rejected = False
        try:
            action()
        except failure_type:
            rejected = True
        if not rejected:
            raise failure_type("mutation accepted: " + label)
        labels.append(label)

    def run_pair_mutations(expected: tuple, validator, label: str, labels: list[str]) -> int:
        before = len_fn(labels)
        for index, (key, value) in enumerate_fn(expected):
            must_reject(
                lambda index=index, key=key, value=value: validator(
                    replace_row(expected, index, (key, mutated_value(value)))
                ),
                label + "_value_" + str_type(index), labels,
            )
            must_reject(
                lambda index=index, key=key, value=value: validator(
                    replace_row(expected, index, (key + "__KEY", value))
                ),
                label + "_key_" + str_type(index), labels,
            )
        must_reject(lambda: validator(expected[:-1]), label + "_missing", labels)
        return len_fn(labels) - before

    def validate_result(candidate: object, expected_items: tuple) -> None:
        if type_fn(candidate) is not dict_type:
            raise failure_type("result outer type changed")
        if not all_fn(exact_str(key) for key in candidate):
            raise failure_type("result key type changed")
        if len_fn(candidate) != len_fn(expected_items):
            raise failure_type("result key count changed")
        expected = dict_type(expected_items)
        if set_type(candidate) != set_type(expected):
            raise failure_type("result key set changed")
        for key, value in expected_items:
            if type_fn(candidate[key]) is not type_fn(value):
                raise failure_type("result value type changed: " + key)
            if candidate[key] != value:
                raise failure_type("result value changed: " + key)

    def run() -> dict[str, object]:
        validate_contract(literal_contract)
        validate_registry(literal_registry)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)
        finite = finite_items()

        labels = list_type()
        contract_mutations = run_pair_mutations(literal_contract, validate_contract, "contract", labels)
        registry_mutations = run_pair_mutations(literal_registry, validate_registry, "registry", labels)
        source_mutations = run_pair_mutations(literal_sources, validate_sources, "source", labels)
        dependency_mutations = run_pair_mutations(literal_dependencies, validate_dependencies, "dependency", labels)

        prefix = (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("conditional_bridge_advance", "YES"),
            ("arithmetic_advance", False),
            ("fixed_atom_credit", 0),
            ("strict_1_over_400", "UNPAID"),
            ("L2", "NONE"),
            ("TPC_207_TRIGGER", False),
            ("numbered_release", "NO"),
            ("contract_fields", len_fn(literal_contract)),
            ("registry_rows", len_fn(literal_registry)),
            ("source_locks", len_fn(literal_sources)),
            ("dependency_locks", len_fn(literal_dependencies)),
            ("registry_sha256", literal_registry_digest),
        ) + finite + (
            ("first_fatal", dict_type(literal_contract)["first_fatal"]),
            ("contract_mutations", contract_mutations),
            ("registry_mutations", registry_mutations),
            ("source_mutations", source_mutations),
            ("dependency_mutations", dependency_mutations),
        )
        full_field_count = len_fn(prefix) + 2
        semantic_mutations = 3 * full_field_count + 1
        mutation_actions = contract_mutations + registry_mutations + source_mutations + dependency_mutations + semantic_mutations
        expected_items = prefix + (
            ("semantic_mutations", semantic_mutations),
            ("mutation_actions", mutation_actions),
        )
        expected_result = dict_type(expected_items)
        validate_result(expected_result, expected_items)

        semantic_before = len_fn(labels)
        for index, (key, value) in enumerate_fn(expected_items):
            missing = dict_type(expected_result)
            del missing[key]
            must_reject(lambda missing=missing: validate_result(missing, expected_items), "result_missing_" + str_type(index), labels)
            bad_type = dict_type(expected_result)
            bad_type[key] = wrong_type(value)
            must_reject(lambda bad_type=bad_type: validate_result(bad_type, expected_items), "result_type_" + str_type(index), labels)
            bad_value = dict_type(expected_result)
            bad_value[key] = mutated_value(value)
            must_reject(lambda bad_value=bad_value: validate_result(bad_value, expected_items), "result_value_" + str_type(index), labels)
        extra = dict_type(expected_result)
        extra["__EXTRA"] = "forbidden"
        must_reject(lambda: validate_result(extra, expected_items), "result_extra", labels)
        if len_fn(labels) - semantic_before != semantic_mutations:
            raise failure_type("semantic mutation count changed")
        if len_fn(labels) != mutation_actions or len_fn(set_type(labels)) != len_fn(labels):
            raise failure_type("mutation trace changed")

        result = dict_type(expected_result)
        validate_result(result, expected_items)
        return result

    return run


_TRUSTED_RUN = _make_trusted_runner()


def _sealed_main_call(
    runner,
    baseline_items,
    frozen_text,
    print_fn,
    tuple_type,
    str_type,
    type_fn,
    len_fn,
    sorted_fn,
    all_fn,
    failure_type,
    *argv_objects,
) -> int:
    if len_fn(argv_objects) != 1:
        raise failure_type("explicit --check is required")
    args = argv_objects[0]
    if type_fn(args) is not tuple_type or not all_fn(type_fn(arg) is str_type for arg in args):
        raise failure_type("explicit --check is required")
    if args != ("--check",):
        raise failure_type("explicit --check is required")
    current_items = tuple_type(sorted_fn(runner().items()))
    if current_items != baseline_items:
        raise failure_type("sealed result changed")
    print_fn(frozen_text)
    return 0


def _seal_main(
    runner=_TRUSTED_RUN,
    dumps_fn=json.dumps,
    print_fn=print,
    partial_fn=partial,
    tuple_type=tuple,
    dict_type=dict,
    str_type=str,
    type_fn=type,
    len_fn=len,
    sorted_fn=sorted,
    all_fn=all,
    failure_type=CheckFailure,
):
    baseline_items = tuple_type(sorted_fn(runner().items()))
    frozen_text = dumps_fn(dict_type(baseline_items), sort_keys=True, separators=(",", ":"))
    return partial_fn(
        _sealed_main_call,
        runner,
        baseline_items,
        frozen_text,
        print_fn,
        tuple_type,
        str_type,
        type_fn,
        len_fn,
        sorted_fn,
        all_fn,
        failure_type,
    )


main = _seal_main()


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        print("CheckFailure: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
