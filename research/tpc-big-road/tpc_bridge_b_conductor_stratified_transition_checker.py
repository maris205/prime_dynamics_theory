#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V45 conductor-spectrum artifact."""

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
    "EXACT_CONDUCTOR_STRATIFICATION_REPLACES_THE_V44_CENTERED_VARIANCE_"
    "GATE_BY_A_SOURCE_BACKED_HIGH_CONDUCTOR_PAYMENT_AND_ONE_STRUCTURED_"
    "LOW_CONDUCTOR_MAJOR_SPECTRUM_GATE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V45_CONDUCTOR_STRATIFIED_TRANSITION_V1"),
    ("artifact_name", "bridge_b_conductor_stratified_transition_spectrum.md"),
    ("baseline_commit", "1e19b2d4c8a27db94a9f3798e123017e9df37d28"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "LOW_CONDUCTOR_MAJOR_THEN_LONG_MOBIUS_WITH_V42_GATE_B_PARALLEL"),
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
    ("P", "Q^2/H=x^(1/96)"),
    ("D0", "P^(1/2)=x^(1/192)"),
    ("conductor_split", "principal_plus_low_structured_and_high_variance"),
    ("high_variance", "P^(3/2)*x^o=x^(1/64+o(1))"),
    ("high_output", "x^(213/128+o(1))"),
    ("high_margin", "1/9600"),
    ("low_gate", "x^(1997/1200-eta_low+o(1))_eta_low>0"),
    ("transition_corrections", "x^(319/192+o(1))_and_x^(7171/4800+o(1))"),
    ("first_fatal", "NO_LITERAL_THEOREM_BOUNDS_THE_PRINCIPAL_PLUS_LOW_CONDUCTOR_INDUCED_CHARACTER_GAUSS_RAMANUJAN_SPECTRUM_WITH_PHYSICAL_LAMBDA_MINUS_B_AT_THE_STRICT_TRANSITION_POWER"),
)


REGISTRY_ITEMS = (
    ("V45_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V45_ROUTE_ADVANCE", "YES"),
    ("V45_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V45_ARITHMETIC_ADVANCE", "NO"),
    ("V45_FIXED_ATOM_CREDIT", "0"),
    ("V45_STRICT_1_OVER_400", "UNPAID"),
    ("V45_L2", "NONE"),
    ("V45_TPC_207_TRIGGER", "false"),
    ("V45_NUMBERED_RELEASE", "NO"),
    ("V45_DERIVATION_STATUS", "COHERENT_AFTER_EXACT_CONDUCTOR_SPLIT_GAUSS_RAMANUJAN_RETYPE_AND_HIGH_CONDUCTOR_PAYMENT"),
    ("V45_ASSUMPTION_POLICY", "ONLY_THE_PRINCIPAL_PLUS_LOW_CONDUCTOR_STRUCTURED_MAJOR_SPECTRUM_REMAINS_OPEN_IN_THE_TRANSITION_WINDOW"),
    ("V45_SELECTED_RESEARCH_ROUTE", "LOW_CONDUCTOR_STRUCTURED_MAJOR_FIRST__BALANCED_AND_REVERSE_TYPE_I_SECOND__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE"),
    ("V45_V44_COMMON_TRANSITION", "RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE"),
    ("V45_V44_IMPRIMITIVE_X_O1_SHORTCUT", "RETYPED_AS_FALSE_UNIFORM_LEDGER_FOR_LOW_CONDUCTORS"),
    ("V45_SQUAREFREE_REDUCED_MODULUS", "PROVED_EXACT_FROM_LAMBDA_S_SUPPORT"),
    ("V45_CHARACTER_INVERSION", "PROVED_EXACT_ALL_CHARACTERS_BEFORE_OUTER_ABSOLUTE"),
    ("V45_CONDUCTOR_SPLIT", "PROVED_EXACT_AT_D0_EQUALS_P_POWER_1_OVER_2"),
    ("V45_CONDUCTOR_THRESHOLD", "D0_EQUALS_P_POWER_1_OVER_2_EQUALS_X_POWER_1_OVER_192"),
    ("V45_PRINCIPAL_MODE_LOCATION", "PROVED_EXACT_INSIDE_LOW_CONDUCTOR_SPECTRUM_D_EQUALS_1"),
    ("V45_LOW_NONPRINCIPAL_TOWER", "PROVED_EXACT_INDUCED_PRIMITIVE_CONDUCTORS_1_LT_D_LT_D0"),
    ("V45_HIGH_SPECTRUM", "PROVED_EXACT_PRIMITIVE_CONDUCTORS_D_GE_D0"),
    ("V45_GAUSS_RAMANUJAN_TRANSFORM", "PROVED_EXACT_TAU_CHI_TIMES_CHI_E_TIMES_PHYSICAL_CHIBAR_U_C_E_U"),
    ("V45_GAUSS_RAMANUJAN_PHASE", "PROVED_CHI_STAR_E_NOT_ITS_CONJUGATE"),
    ("V45_RAMANUJAN_LOCAL_DENSITY", "PROVED_MU_E_C_E_U_EQUALS_MU_GCD_TIMES_PHI_GCD"),
    ("V45_RECIPROCAL_COLLISION", "PROVED_N1_Q2_MINUS_N2_Q1_EQUALS_ELL_S_WITH_ABS_ELL_LE_P_X_O1"),
    ("V45_DYADIC_SHORT_LENGTH", "N_ASYMPTOTIC_S_Q_OVER_H"),
    ("V45_INDUCED_EXTENSION_WEIGHT", "PROVED_X_O1_OVER_D_S_SQUARED"),
    ("V45_PRIMITIVE_SECOND_MOMENT", "SOURCE_BACKED_P_SQUARED_TIMES_D_OVER_Q_PLUS_1_OVER_D"),
    ("V45_PRIMITIVE_FOURTH_MOMENT_D_GT_N", "SOURCE_BACKED_P_SQUARED_OVER_N"),
    ("V45_PRIMITIVE_FOURTH_MOMENT_D_LE_N", "SOURCE_BACKED_P_SQUARED_OVER_D"),
    ("V45_HIGH_CONDUCTOR_LOW_D_REGION", "PROVED_SECOND_MOMENT_LE_P_POWER_3_OVER_2"),
    ("V45_HIGH_CONDUCTOR_HIGH_D_REGION", "PROVED_FOURTH_MOMENT_LE_P_POWER_3_OVER_2"),
    ("V45_HIGH_CONDUCTOR_VARIANCE", "PROVED_SOURCE_BACKED_P_POWER_3_OVER_2_X_O1"),
    ("V45_HIGH_CONDUCTOR_VARIANCE_EXPONENT", "1_OVER_64"),
    ("V45_HIGH_CONDUCTOR_OUTPUT", "PROVED_X_POWER_213_OVER_128_PLUS_O1"),
    ("V45_HIGH_CONDUCTOR_ENDPOINT_MARGIN", "1_OVER_9600"),
    ("V45_LOW_STRUCTURED_ABSOLUTE_CEILING", "X_POWER_5_OVER_3_PLUS_O1"),
    ("V45_LOW_STRUCTURED_MAJOR_GATE", "OPEN_X_POWER_1997_OVER_1200_MINUS_ETA_LOW_WITH_ETA_LOW_POSITIVE"),
    ("V45_TRANSITION_CONDITIONAL_COMPILER", "PROVED_LOW_STRUCTURED_GATE_PAYS_FULL_TRANSITION_WITH_HIGH_SPECTRUM_AND_CORRECTIONS"),
    ("V45_TRANSITION_CONDITIONAL_MARGIN", "MIN_ETA_LOW_1_OVER_9600_13_OVER_4800_817_OVER_4800"),
    ("V45_PHYSICAL_Q_DIVIDES_U_CORRECTION", "RETAINED_PAID_X_POWER_319_OVER_192_PLUS_O1"),
    ("V45_BACKGROUND_OUTPUT", "RETAINED_PAID_X_POWER_7171_OVER_4800_PLUS_O1"),
    ("V45_LONG_BALANCED_WINDOW", "OPEN_D_GT_U_AND_K_GT_U"),
    ("V45_LONG_REVERSE_TYPE_I_WINDOW", "OPEN_D_GT_U_AND_K_LE_U"),
    ("V45_V42_GATE_B", "RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE"),
    ("V45_BFI_PRIMITIVE_LARGE_SIEVE", "SOURCE_BACKED_HIGH_CONDUCTOR_SECOND_AND_FOURTH_MOMENTS"),
    ("V45_BFI_INDUCED_CHARACTER_SPLIT", "SOURCE_BACKED_ARCHITECTURE_LOW_SIEGEL_WALFISZ_HIGH_LARGE_SIEVE"),
    ("V45_BFI_LOW_CONDUCTOR_TO_FIXED_POWER", "STOP_SCOPED_LOG_SAVING_DOES_NOT_PAY_1_OVER_400"),
    ("V45_CIS_ASYMPTOTIC_LARGE_SIEVE_DIRECT_ATTACHMENT", "STOP_SCOPED_PRIMITIVE_ASYMPTOTIC_FORM_DOES_NOT_IDENTIFY_LITERAL_PHYSICAL_LOW_SPECTRUM"),
    ("V45_PRODUCTS_OF_PRIMES_DENSE_MODEL_DIRECT_ATTACHMENT", "STOP_SCOPED_TERNARY_PRODUCT_AND_BURGESS_LENGTH_WRONG_PHYSICAL_OBJECT"),
    ("V45_LOW_EXCEPTIONAL_CHARACTER_FIREWALL", "RETAIN_STRUCTURED_MODE_NO_UNIFORM_POWER_BORROWED"),
    ("V45_DIRECT_PRIMARY_SOURCE_FOR_LOW_STRUCTURED_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10"),
    ("V45_FIRST_FATAL", "NO_LITERAL_THEOREM_BOUNDS_THE_PRINCIPAL_PLUS_LOW_CONDUCTOR_INDUCED_CHARACTER_GAUSS_RAMANUJAN_SPECTRUM_WITH_PHYSICAL_LAMBDA_MINUS_B_AT_THE_STRICT_TRANSITION_POWER"),
    ("V45_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TRANSITION_HIGH_CONDUCTOR_PAID_LOW_STRUCTURED_MAJOR_OPEN_LONG_MOBIUS_SPAN_OPEN"),
    ("V45_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V45_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B"),
)


EXPECTED_REGISTRY_SHA256 = "04b9d12a0ddc549da1ecb9cfa1598de1c16a0fffc56d0fbc7e6229ca0d9ada28"


SOURCE_ITEMS = (
    ("BFI", "Acta_Mathematica_156_1986_equation_1_6_Theorem_0_and_proof"),
    ("CIS", "arXiv:1105.1176v1_primitive_character_asymptotic_large_sieve"),
    ("MATOMAKI_TERAVAINEN", "arXiv:2301.07679v1_prime_character_dense_model_and_quadratic_obstruction"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_conductor_stratified_transition_spectrum.md", "0a797eb4e3791319624fb5dd7a597d6d6bb217b46759739a51854312df6f4ec9"),
    ("research/tpc-big-road/bridge_b_transition_reciprocal_variance_and_ramanujan_mean.md", "053ae6a18740a2e81d754c4ecce7af1a00ecfe331f7d5d4991945889f14c9920"),
    ("research/tpc-big-road/tpc_bridge_b_transition_reciprocal_variance_checker.py", "8c928b26ecfd904069366bbfbf003367f3adae7638f0de0c669000da820b0af1"),
    ("research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md", "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a"),
    ("research/tpc-big-road/tpc_bridge_b_proper_factor_poisson_transference_checker.py", "ff48df45275588f6f27572962dd565db1d8e4475daa6d52c2b382ad068d1ab76"),
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
        for index, row in enumerate_fn(candidate):
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type(label + " row shape changed")
            key, value = row
            if not exact_str(key):
                raise failure_type(label + " key type changed")
            if string_values and not exact_str(value):
                raise failure_type(label + " value type changed")
            if not string_values and type_fn(value) is not type_fn(expected[index][1]):
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
        if dict_type(candidate).get("V45_MAXIMUM_CLAIM") != literal_maximum_claim:
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

    def euler_phi(n: int) -> int:
        result = n
        for p, _ in factorization(n):
            result = result // p * (p - 1)
        return result

    def divisors(n: int) -> tuple[int, ...]:
        return tuple_type(d for d in range_fn(1, n + 1) if n % d == 0)

    def ramanujan_sum(s: int, u: int) -> int:
        common = gcd_fn(s, u)
        return sum_fn((d * mobius(s // d) for d in divisors(common)), 0)

    def zeta6_power(k: int) -> tuple[int, int]:
        powers = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
        return powers[k % 6]

    def pair_sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
        return (a[0] - b[0], a[1] - b[1])

    def finite_items() -> tuple[tuple[str, object], ...]:
        s, q1, q2, n1, n2 = 5, 7, 11, 1, 3
        residue1 = n1 * pow_fn(q1, -1, s) % s
        residue2 = n2 * pow_fn(q2, -1, s) % s
        determinant = n1 * q2 - n2 * q1
        ell = determinant // s
        if (residue1, residue2, determinant, ell) != (3, 3, -10, -2):
            raise failure_type("reciprocal collision changed")

        gauss_lhs = pair_sub(zeta6_power(1), zeta6_power(5))
        gauss_rhs = pair_sub(zeta6_power(2), zeta6_power(4))
        if gauss_lhs != (-1, 2) or gauss_rhs != gauss_lhs:
            raise failure_type("induced Gauss Ramanujan phase changed")

        occupancy = (0, 1)
        occupancy_mean = fraction_type(sum_fn(occupancy), 2)
        centered = tuple_type(fraction_type(value) - occupancy_mean for value in occupancy)
        conductor3_character = (1, -1)
        low_fourier = sum_fn(
            (centered[index] * conductor3_character[index] for index in range_fn(2)),
            fraction_type(0),
        )
        if centered != (fraction_type(-1, 2), fraction_type(1, 2)) or low_fourier != -1:
            raise failure_type("low conductor survived-centering fixture changed")

        density_rows = list_type()
        for e in (1, 2, 3, 5, 6, 10, 15, 30):
            if mobius(e) == 0:
                raise failure_type("density fixture lost squarefreeness")
            for u in range_fn(0, 2 * e + 1):
                common = gcd_fn(e, u)
                left = mobius(e) * ramanujan_sum(e, u)
                right = mobius(common) * euler_phi(common)
                if left != right:
                    raise failure_type("Ramanujan local density changed")
                density_rows.append((e, u, left))

        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        p_exp = 2 * q_exp - h_exp
        d0_exp = p_exp / 2
        high_variance_exp = 3 * p_exp / 2
        high_output_exp = h_exp + 1 + 3 * p_exp / 4
        target_exp = fraction_type(1997, 1200)
        high_margin = target_exp - high_output_exp
        unit_output = fraction_type(319, 192)
        unit_margin = target_exp - unit_output
        background_output = fraction_type(7171, 4800)
        background_margin = target_exp - background_output
        split_exp = q_exp - d0_exp

        if (
            p_exp, d0_exp, high_variance_exp, high_output_exp, high_margin,
            unit_margin, background_margin,
        ) != (
            fraction_type(1, 96), fraction_type(1, 192), fraction_type(1, 64),
            fraction_type(213, 128), fraction_type(1, 9600),
            fraction_type(13, 4800), fraction_type(817, 4800),
        ):
            raise failure_type("rational exponent ledger changed")

        low_region_samples = (d0_exp, fraction_type(1, 100), split_exp)
        low_region_bounds = tuple_type(
            max_fn(2 * p_exp + d - q_exp, 2 * p_exp - d)
            for d in low_region_samples
        )
        if not all_fn(value <= high_variance_exp for value in low_region_bounds):
            raise failure_type("second moment interpolation changed")

        d_high = split_exp + fraction_type(1, 10000)
        n_lower = d_high + p_exp - q_exp
        fourth_high = max_fn(2 * p_exp - n_lower, 2 * p_exp - d_high)
        if not (n_lower > d0_exp and fourth_high < high_variance_exp):
            raise failure_type("fourth moment interpolation changed")

        return (
            ("collision_residues", (residue1, residue2)),
            ("collision_determinant", determinant),
            ("collision_ell", ell),
            ("gauss_lhs_zeta6", gauss_lhs),
            ("gauss_rhs_zeta6", gauss_rhs),
            ("centered_s6", tuple_type(str_type(value) for value in centered)),
            ("conductor3_fourier", str_type(low_fourier)),
            ("density_fixture_rows", len_fn(density_rows)),
            ("P_exponent", str_type(p_exp)),
            ("D0_exponent", str_type(d0_exp)),
            ("high_variance_exponent", str_type(high_variance_exp)),
            ("high_output_exponent", str_type(high_output_exp)),
            ("high_margin", str_type(high_margin)),
            ("unit_margin", str_type(unit_margin)),
            ("background_margin", str_type(background_margin)),
            ("conductor_split_exponent", str_type(split_exp)),
            ("second_moment_sample_exponents", tuple_type(str_type(value) for value in low_region_bounds)),
            ("high_region_N_lower", str_type(n_lower)),
            ("high_region_fourth_bound", str_type(fourth_high)),
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
            must_reject(
                lambda index=index, key=key, value=value: validator(
                    replace_row(expected, index, (key, wrong_type(value)))
                ),
                label + "_type_" + str_type(index), labels,
            )
        must_reject(lambda: validator(expected[:-1]), label + "_missing", labels)
        must_reject(lambda: validator(list_type(expected)), label + "_outer_type", labels)
        must_reject(
            lambda: validator((list_type(expected[0]),) + expected[1:]),
            label + "_row_type", labels,
        )
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
