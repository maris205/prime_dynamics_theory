#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V43 Poisson transference artifact."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import partial
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_PROPER_FACTOR_POISSON_TRANSFERENCE_DELETES_ALL_SMALL_D_"
    "NONZERO_ALIASES_AND_IDENTIFIES_THE_D_GT_H_OVER_4Q_INVERSE_"
    "RESIDUE_GATE_A_FRONTIER_WITH_ZERO_AXIS_RETURN"
)


CONTRACT_ITEMS = (
    ("schema_version", "V43_PROPER_FACTOR_POISSON_TRANSFERENCE_V1"),
    ("artifact_name", "bridge_b_proper_factor_poisson_transference.md"),
    ("baseline_commit", "1f17878cfa62c40afab9620ee73536c7b5c9ea1e"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "POISSON_TRANSFERENCE_THEN_TRANSITION_TYPE_II_REVERSE_TYPE_I_ALIAS_WITH_V42_MPD_PARALLEL"),
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
    ("small_d_cutoff", "H/(4Q)=x^(31/96+o(1))"),
    ("transition_dual_length", "x^(23/2400+o(1))"),
    ("centered_vector", "unit_u1_row_with_zero_mean"),
    ("poisson_prefactor", "H/(dq)"),
    ("poisson_spike_phase", "e_d(m*u*inverse(q))"),
    ("poisson_background_phase", "e_(dq)(m*u)/(q-1)"),
    ("row_identity", "s_q=alias_q-cprime_q(0)*unit_diagonal+error"),
    ("core_identity", "C_x=A_x-L_pr*S_physical+paid_errors"),
    ("direct_identity", "D_x=A_x-L_pr*S_physical+paid_errors"),
    ("J_identity", "J(r_x)=A_x/L_pr+paid_errors"),
    ("shell_freeze_error", "x^(79/48+epsilon+o(1))"),
    ("shell_freeze_margin", "11/600-epsilon"),
    ("principal_nonunit_error", "x^(53/32+o(1))"),
    ("square_energy", "x^(95/48+o(1))"),
    ("square_scalar", "x^(143/96+o(1))"),
    ("first_fatal", "NO_LITERAL_THEOREM_BOUNDS_THE_FULL_CENTERED_TRANSITION_OR_LONG_MOBIUS_REVERSE_TYPE_I_AND_BALANCED_FOUR_VARIABLE_INVERSE_RESIDUE_ALIAS_WITH_PHYSICAL_W_AT_THE_STRICT_NUMERATOR_POWER"),
)


REGISTRY_ITEMS = (
    ("V43_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V43_ROUTE_ADVANCE", "YES"),
    ("V43_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V43_ARITHMETIC_ADVANCE", "NO"),
    ("V43_FIXED_ATOM_CREDIT", "0"),
    ("V43_STRICT_1_OVER_400", "UNPAID"),
    ("V43_L2", "NONE"),
    ("V43_TPC_207_TRIGGER", "false"),
    ("V43_NUMBERED_RELEASE", "NO"),
    ("V43_DERIVATION_STATUS", "COHERENT_AFTER_ORDERED_WEIGHT_FREEZE_CENTERED_POISSON_HARD_SHELL_DIAGONAL_AND_SCALAR_REASSEMBLY"),
    ("V43_ASSUMPTION_POLICY", "GATE_A_ALIAS_AND_GATE_B_NUMERATOR_REMAIN_TWO_EXPLICIT_OPEN_THEOREMS"),
    ("V43_SELECTED_RESEARCH_ROUTE", "PROPER_FACTOR_POISSON_TRANSFERENCE_FIRST__TRANSITION_TYPE_II_REVERSE_TYPE_I_ALIAS_SECOND__V42_MPD_PARALLEL__A_AND_B_JOIN__C_RESERVE"),
    ("V43_V35_PROPER_FACTOR_IDENTITY", "RETAINED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA"),
    ("V43_ORDERED_WEIGHT_FREEZE", "PROVED_UNIFORM_ERROR_ABS_U_MINUS_DK_OVER_X_LOG_X"),
    ("V43_WEIGHT_FREEZE_DIAGONAL", "PROVED_EXACT_SUM_D_DIVIDES_U_THETA_FROZEN_EQUALS_BETA_U"),
    ("V43_FOLDED_NONSQUARE_IDENTITY", "PROVED_EXACT_TWO_ORIENTATION_FORM"),
    ("V43_FOLDED_SQUARE_IDENTITY", "PROVED_EXACT_MU_S_OVER_2"),
    ("V43_SEMIPRIME_ORIENTATION_CANCELLATION", "PROVED_EXACT_ZERO_WHEN_BOTH_MU_EQUAL_MINUS_1_IN_SHORT_FACTOR_BRANCH"),
    ("V43_CENTERED_UNIT_VECTOR", "PROVED_EXACT_Q_PERIODIC_PHYSICAL_U1_ROW"),
    ("V43_CENTERED_UNIT_VECTOR_MEAN", "PROVED_EXACT_ZERO"),
    ("V43_CENTERED_UNIT_VECTOR_DFT", "PROVED_EXACT_NONZERO_FREQUENCY_E_MINUS_AR_PLUS_ONE_OVER_Q_MINUS_1_OVER_Q"),
    ("V43_COMPLETE_POISSON_ALIAS", "PROVED_EXACT_H_OVER_DQ_TIMES_INVERSE_RESIDUE_PLUS_BACKGROUND_SUM"),
    ("V43_POISSON_PHASE_RECIPROCITY", "PROVED_EXACT_E_Q_MINUS_MU_DBAR_TIMES_E_DQ_MU_EQUALS_E_D_MU_QBAR"),
    ("V43_SMALL_D_CUTOFF", "H_OVER_4Q_EQUALS_X_POWER_31_OVER_96_PLUS_O1"),
    ("V43_SMALL_D_NONZERO_ALIAS", "PROVED_EXACT_ZERO_BY_PSI_SUPPORT"),
    ("V43_OFFZERO_DELETION_EFFECT", "PROVED_EXACT_NEGATIVE_PHYSICAL_DIAGONAL_RETURN"),
    ("V43_ROW_TRANSFERENCE", "PROVED_S_Q_EQUALS_ALIAS_Q_MINUS_CENTERED_UNIT_DIAGONAL_PLUS_ERROR"),
    ("V43_ROW_TRANSFERENCE_ERROR", "X_POWER_H_SQUARED_OVER_Q_TIMES_X_EPSILON_PLUS_O1"),
    ("V43_SCALAR_ALIAS", "PROVED_EXACT_ONE_OUTER_SIGNED_SUM_Q_Q_ALIAS_Q"),
    ("V43_DIAGONAL_SHELL_COEFFICIENT", "Q_TIMES_Q_MINUS_2_OVER_Q_MINUS_1"),
    ("V43_DIAGONAL_SHELL_COEFFICIENT_SUM", "L_PR_PLUS_X_O1"),
    ("V43_UNIT_OMISSION_CORRECTION", "PROVED_ABSOLUTE_X_POWER_4_OVER_3_PLUS_O1"),
    ("V43_CORE_SCALAR_TRANSFERENCE", "PROVED_C_EQUALS_ALIAS_MINUS_L_PR_S_PHYSICAL_PLUS_PAID_ERRORS"),
    ("V43_SHELL_FREEZE_ERROR_NUMERATOR", "X_POWER_79_OVER_48_PLUS_EPSILON_PLUS_O1"),
    ("V43_SHELL_FREEZE_ERROR_MARGIN", "11_OVER_600_MINUS_EPSILON"),
    ("V43_V35_PRINCIPAL_NONUNIT_REMAINDERS", "RETAINED_PAID_X_POWER_53_OVER_32_PLUS_O1"),
    ("V43_DIRECT_NUMERATOR_TRANSFERENCE", "PROVED_D_EQUALS_ALIAS_MINUS_L_PR_S_PHYSICAL_PLUS_PAID_ERRORS"),
    ("V43_J_MAJOR_ALIAS", "PROVED_J_R_EQUALS_ALIAS_OVER_L_PR_PLUS_X_95_OVER_96_AND_X_47_OVER_48_ERRORS"),
    ("V43_GATE_B_TO_GATE_A_ZERO_AXIS_TRANSFER", "PROVED_EXACT_UP_TO_PAID_ERRORS"),
    ("V43_SMALL_FACTOR_TYPE_I_ALIAS", "DELETED_EXACT_NONZERO_FREQUENCIES_BUT_ZERO_AXIS_NOT_PAID"),
    ("V43_TRANSITION_RANGE", "H_OVER_4Q_LT_D_LE_X_POWER_133_OVER_400"),
    ("V43_TRANSITION_DUAL_LENGTH", "X_POWER_23_OVER_2400_PLUS_O1"),
    ("V43_TYPE_II_RANGE", "D_GT_U_AND_K_GT_U"),
    ("V43_REVERSE_TYPE_I_RANGE", "D_GT_U_AND_K_LE_U_WITH_MOBIUS_ON_LONG_D"),
    ("V43_SQUARE_ROW_ENERGY", "PROVED_ABSOLUTE_X_POWER_95_OVER_48_PLUS_O1"),
    ("V43_SQUARE_ROW_ENERGY_MARGIN", "1_OVER_3"),
    ("V43_SQUARE_SCALAR_OUTPUT", "PROVED_ABSOLUTE_X_POWER_143_OVER_96_PLUS_O1"),
    ("V43_CONDITIONAL_TWO_GATE_COMPILER", "PROVED_H_A_AND_H_B_IMPLY_PHYSICAL_X_POWER_399_OVER_400_MINUS_ETA"),
    ("V43_CONDITIONAL_TWO_GATE_MARGIN", "MIN_ETA_A_ETA_B_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON"),
    ("V43_V42_MPD_GATE", "RETAINED_PARALLEL_SUFFICIENT_IMPLEMENTATION_OF_GATE_B"),
    ("V43_BETTIN_CHANDEE_DIRECT_ATTACHMENT", "STOP_SCOPED_PHYSICAL_U_COUPLED_TO_NUMERATOR_DENOMINATOR_AND_MOVING_DUAL_CUTOFF"),
    ("V43_BLOMER_PASCADI_DIRECT_ATTACHMENT", "STOP_SCOPED_FIXED_MODULUS_LOCAL_CELL_NO_VARYING_D_Q_U_AGGREGATE"),
    ("V43_PASCADI_HORIZONTAL_KUZNETSOV", "OPEN_STRONGEST_ALTERNATIVE_COMPILER_CANDIDATE_AFTER_EXACT_ALIAS_EMITTER"),
    ("V43_RUNBO_LI_FIRST_SIZE_CONDITIONS", "PASS_599_OVER_600_AND_1199_OVER_1200"),
    ("V43_RUNBO_LI_SECOND_SIZE_CONDITIONS", "FAIL_2531_OVER_400_AND_1897_OVER_300_GREATER_THAN_4"),
    ("V43_RUNBO_LI_DIRECT_ATTACHMENT", "STOP_SCOPED_MODULUS_FACTORS_FIXED_RESIDUE_AND_NO_PHYSICAL_W_ALIAS"),
    ("V43_BAZIN_DIRECT_ATTACHMENT", "STOP_SCOPED_COLLAPSED_BETA_MARGINAL_NOT_JOINT_PROPER_FACTOR_POISSON_ALIAS"),
    ("V43_DIRECT_PRIMARY_SOURCE_FOR_HARD_ALIAS", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10"),
    ("V43_FIRST_FATAL", "NO_LITERAL_THEOREM_BOUNDS_THE_FULL_CENTERED_TRANSITION_OR_LONG_MOBIUS_REVERSE_TYPE_I_AND_BALANCED_FOUR_VARIABLE_INVERSE_RESIDUE_ALIAS_WITH_PHYSICAL_W_AT_THE_STRICT_NUMERATOR_POWER"),
    ("V43_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B_SMALL_FACTOR_ALIAS_REMOVED_ZERO_AXIS_RETURNED_LONG_MOBIUS_SPAN_OPEN"),
    ("V43_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V43_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B"),
)


EXPECTED_REGISTRY_SHA256 = "6cc36d9d2acfaeebfbdda5e09410e6c0dd77732831f80042f4a56a473ca10715"


SOURCE_ITEMS = (
    ("BETTIN_CHANDEE", "arXiv:1502.00769v1_Theorem_1"),
    ("PASCADI_HORIZONTAL", "arXiv:2404.04239v3_Corollaries_17_18"),
    ("BLOMER_PASCADI", "arXiv:2607.24311v1_Theorem_1_1"),
    ("RUNBO_LI", "arXiv:2602.20917v6_Theorem_1_1"),
    ("BAZIN", "arXiv:2607.15137v1_Theorem_8"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md", "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a"),
    ("research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md", "705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1"),
    ("research/tpc-big-road/tpc_bridge_b_proper_factor_unit_ratio_checker.py", "8c5e3dcc03b6ac132baae8a0c0c1949fddc24a6f114fd61de416cf4a7b02bd51"),
    ("research/tpc-big-road/bridge_b_paid_local_carrier_and_compensated_prime_frame.md", "e1816cdac10715bd982ef14960346f17968ac1ea96a3cdbf0b740d3f473ebca8"),
    ("research/tpc-big-road/tpc_bridge_b_paid_local_carrier_prime_frame_checker.py", "d1ac9b35ac3c164cdf5931f5b01fa4021db233263c537c0602c73796632a151a"),
    ("research/tpc-big-road/bridge_b_mobius_directional_dispersion_compiler.md", "7888146d36445289520b7f20b9fc99f5ccf39c41d9ed5aec7da47b9e25cb859f"),
    ("research/tpc-big-road/tpc_bridge_b_mobius_directional_dispersion_checker.py", "0bb4bd2133851060737060ebd958fc0cd3caa99ed4da130d1463cf29af369c5b"),
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
        values = dict_type(candidate)
        if values.get("maximum_claim") != literal_maximum_claim:
            raise failure_type("maximum claim contract seed changed")

    def validate_registry(candidate: object) -> None:
        require_rows(candidate, literal_registry, "registry", True)
        values = dict_type(candidate)
        if values.get("V43_MAXIMUM_CLAIM") != literal_maximum_claim:
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

    def centered_vector(q: int, d: int, u: int) -> tuple[Fraction, ...]:
        inverse_d = pow_fn(d, -1, q)
        residue = u * inverse_d % q
        return tuple_type(
            fraction_type(0) if k == 0 else (
                fraction_type(q - 2, q - 1) if k == residue else fraction_type(-1, q - 1)
            )
            for k in range_fn(q)
        )

    def cyclotomic_reduce(coefficients: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        last = coefficients[-1]
        return tuple_type(coefficients[j] - last for j in range_fn(len_fn(coefficients) - 1))

    def dft_fixture() -> bool:
        q, d, u = 5, 2, 3
        values = centered_vector(q, d, u)
        residue = u * pow_fn(d, -1, q) % q
        for a in range_fn(1, q):
            actual = [fraction_type(0) for _ in range_fn(q)]
            for k, value in enumerate_fn(values):
                actual[(-a * k) % q] += value / q
            expected = [fraction_type(0) for _ in range_fn(q)]
            expected[(-a * residue) % q] += fraction_type(1, q)
            expected[0] += fraction_type(1, q * (q - 1))
            if cyclotomic_reduce(tuple_type(actual)) != cyclotomic_reduce(tuple_type(expected)):
                return False
        return True

    def active_frequencies(q: int, d: int, h_scale: int) -> tuple[int, ...]:
        bound = 4 * q * d
        return tuple_type(
            m for m in range_fn(-bound, bound + 1)
            if m != 0 and m % q != 0 and abs_fn(fraction_type(h_scale * m, d * q)) <= 1
        )

    def fraction_mod_one(value: Fraction) -> Fraction:
        return value - (value.numerator // value.denominator)

    def finite_items() -> tuple[tuple[str, object], ...]:
        q, d, u = 5, 2, 3
        vector = centered_vector(q, d, u)
        if vector != (
            fraction_type(0), fraction_type(-1, 4), fraction_type(-1, 4),
            fraction_type(-1, 4), fraction_type(3, 4),
        ):
            raise failure_type("centered vector changed")
        if sum_fn(vector, fraction_type(0)) != 0:
            raise failure_type("centered mean changed")
        if not dft_fixture():
            raise failure_type("centered DFT changed")

        zero_support = active_frequencies(5, 2, 11)
        active_support = active_frequencies(5, 2, 9)
        if zero_support != tuple_type() or active_support != (-1, 1):
            raise failure_type("Poisson support gap changed")

        q2, d2, u2, m2 = 5, 3, 2, 1
        left = fraction_type(-m2 * u2 * pow_fn(d2, -1, q2), q2) + fraction_type(m2 * u2, d2 * q2)
        right = fraction_type(m2 * u2 * pow_fn(q2, -1, d2), d2)
        phase_difference = left - right
        if phase_difference.denominator != 1:
            raise failure_type("reciprocity phase changed")

        deletion_vector = centered_vector(5, 2, 4)
        deleted_diagonal = sum_fn(deletion_vector, fraction_type(0)) - deletion_vector[2]
        if deleted_diagonal != fraction_type(-3, 4):
            raise failure_type("zero-axis deletion changed")

        semiprime_fold = mobius(5) - mobius(3)
        nonzero_fold = mobius(6) - mobius(2)
        square_fold = fraction_type(mobius(6), 2)
        if (semiprime_fold, nonzero_fold, square_fold) != (0, 2, fraction_type(1, 2)):
            raise failure_type("folded factor fixtures changed")

        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        u_exp = fraction_type(133, 400)
        y_exp = h_exp - q_exp
        transition_exp = u_exp + q_exp - h_exp
        row_error_exp = 2 * h_exp + q_exp
        target_exp = fraction_type(1997, 1200)
        row_error_margin = target_exp - row_error_exp
        paid_remainder_exp = fraction_type(53, 32)
        paid_remainder_margin = target_exp - paid_remainder_exp
        square_energy_exp = 1 + 2 * h_exp - q_exp
        square_energy_margin = fraction_type(37, 16) - square_energy_exp
        square_scalar_exp = fraction_type(1, 2) + h_exp + q_exp
        runbo_first = (2 * u_exp + q_exp, 2 * q_exp + u_exp)
        runbo_second = (7 * u_exp + 12 * q_exp, 7 * q_exp + 12 * u_exp)
        pascadi_optimistic_exp = fraction_type(2399, 1200)
        pascadi_deficit = pascadi_optimistic_exp - target_exp
        background_absolute_exp = fraction_type(1999, 1200)
        background_deficit = background_absolute_exp - target_exp

        expected = (
            fraction_type(31, 96), fraction_type(23, 2400),
            fraction_type(79, 48), fraction_type(11, 600),
            fraction_type(19, 2400), fraction_type(95, 48),
            fraction_type(1, 3), fraction_type(143, 96),
            (fraction_type(599, 600), fraction_type(1199, 1200)),
            (fraction_type(2531, 400), fraction_type(1897, 300)),
            fraction_type(2399, 1200), fraction_type(67, 200),
            fraction_type(1999, 1200), fraction_type(1, 600),
        )
        actual = (
            y_exp, transition_exp, row_error_exp, row_error_margin,
            paid_remainder_margin, square_energy_exp, square_energy_margin,
            square_scalar_exp, runbo_first, runbo_second,
            pascadi_optimistic_exp, pascadi_deficit,
            background_absolute_exp, background_deficit,
        )
        if actual != expected:
            raise failure_type("rational exponent ledger changed")

        b_q = fraction_type(5 * 3, 4)
        if b_q != fraction_type(5 - 1) - fraction_type(1, 5 - 1):
            raise failure_type("diagonal shell coefficient changed")

        return (
            ("fold_semiprime", semiprime_fold),
            ("fold_nonzero", nonzero_fold),
            ("fold_square", str_type(square_fold)),
            ("center_vector", tuple_type(str_type(value) for value in vector)),
            ("center_mean", str_type(sum_fn(vector, fraction_type(0)))),
            ("dft_exact", True),
            ("support_gap", zero_support),
            ("support_active", active_support),
            ("phase_difference", str_type(phase_difference)),
            ("deleted_diagonal", str_type(deleted_diagonal)),
            ("small_d_exponent", str_type(y_exp)),
            ("transition_exponent", str_type(transition_exp)),
            ("row_error_exponent", str_type(row_error_exp)),
            ("row_error_margin", str_type(row_error_margin)),
            ("paid_remainder_exponent", str_type(paid_remainder_exp)),
            ("paid_remainder_margin", str_type(paid_remainder_margin)),
            ("square_energy_exponent", str_type(square_energy_exp)),
            ("square_energy_margin", str_type(square_energy_margin)),
            ("square_scalar_exponent", str_type(square_scalar_exp)),
            ("runbo_first", tuple_type(str_type(value) for value in runbo_first)),
            ("runbo_second", tuple_type(str_type(value) for value in runbo_second)),
            ("pascadi_optimistic_exponent", str_type(pascadi_optimistic_exp)),
            ("pascadi_deficit", str_type(pascadi_deficit)),
            ("background_absolute_exponent", str_type(background_absolute_exp)),
            ("background_deficit", str_type(background_deficit)),
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
