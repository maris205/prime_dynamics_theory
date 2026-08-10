#!/usr/bin/env python3
"""Fail-closed checker for the unnumbered V46 Euler--AP/BDH compiler."""

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
    "EXACT_PROPER_FACTOR_LOCAL_PROFILE_SPLIT_PAYS_THE_TRANSITION_NATIVE_"
    "EULER_CARRIER_AND_REPLACES_THE_V45_LOW_CONDUCTOR_MAJOR_BY_ONE_"
    "LITERAL_ALL_RESIDUE_AP_BDH_ENERGY_GATE"
)


CONTRACT_ITEMS = (
    ("schema_version", "V46_TRANSITION_NATIVE_EULER_BDH_V1"),
    ("artifact_name", "bridge_b_transition_native_euler_bdh_compiler.md"),
    ("baseline_commit", "9737b62421770ed5f96c08f197488460833550d3"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "PROPER_FACTOR_EULER_THEN_ALL_RESIDUE_AP_BDH_THEN_LONG_MOBIUS"),
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
    ("local_output", "x^(1057/640+o(1))_numerator"),
    ("occupancy_energy", "P^2*x^o=x^(1/48+o(1))"),
    ("ap_gate", "x*U^2*x^(rho+o(1))_0<=rho<33/100"),
    ("residual_output", "x^(1799/1200+rho/2+o(1))"),
    ("transition_corrections", "x^(319/192+o(1))_and_x^(7171/4800+o(1))"),
    ("first_fatal", "NO_LITERAL_THEOREM_PROVES_THE_NATURAL_SCALE_ALL_RESIDUE_AP_VARIANCE_FOR_LAMBDA_U_PLUS_2_MINUS_B_Z_U_MINUS_THE_PROPER_FACTOR_LOCAL_PROFILE_UNIFORMLY_FOR_X_POWER_31_OVER_96_LT_D_LE_X_POWER_133_OVER_400"),
)


REGISTRY_ITEMS = (
    ("V46_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V46_ROUTE_ADVANCE", "YES"),
    ("V46_CONDITIONAL_BRIDGE_ADVANCE", "YES"),
    ("V46_ARITHMETIC_ADVANCE", "NO"),
    ("V46_FIXED_ATOM_CREDIT", "0"),
    ("V46_STRICT_1_OVER_400", "UNPAID"),
    ("V46_L2", "NONE"),
    ("V46_TPC_207_TRIGGER", "false"),
    ("V46_NUMBERED_RELEASE", "NO"),
    ("V46_DERIVATION_STATUS", "COHERENT_AFTER_EXACT_PROPER_FACTOR_EULER_SPLIT_RECIPROCAL_OCCUPANCY_ENERGY_AND_AP_PARSEVAL_COMPILER"),
    ("V46_ASSUMPTION_POLICY", "ONE_LITERAL_TRANSITION_AP_BDH_ENERGY_REMAINS_OPEN_AND_IS_NOT_CALLED_AN_EQUIVALENT_OR_WEAKEST_REFORMULATION"),
    ("V46_SELECTED_RESEARCH_ROUTE", "TRANSITION_NATIVE_EULER_PAID__ALL_RESIDUE_AP_BDH_NEXT__LONG_MOBIUS_SECOND__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE"),
    ("V46_V43_TRANSITION_ALIAS", "RETAINED_EXACT_PROPER_FACTOR_POISSON_SCALAR_BEFORE_OUTER_ABSOLUTE"),
    ("V46_V44_CORRECTION_LEDGER", "RETAINED_Q_DIVIDES_U_AND_CENTERED_BACKGROUND_PAID"),
    ("V46_V45_HIGH_CONDUCTOR_PAYMENT", "RETAINED_INDEPENDENT_SOURCE_BACKED_X_POWER_213_OVER_128"),
    ("V46_PROPER_FACTOR_SQUAREFREE", "PROVED_EXACT_FROM_MU_D_NONZERO"),
    ("V46_SHIFTED_PRIME_LOCAL_PROFILE", "PROVED_EXACT_PRODUCT_OF_F_P"),
    ("V46_HYBRID_LOCAL_PROFILE", "PROVED_EXACT_PRODUCT_OF_G_P_Z"),
    ("V46_LOCAL_PROFILE_DIFFERENCE", "DELTA_D_Z_EQUALS_P_D_MINUS_B_D_Z"),
    ("V46_LOCAL_PROFILE_ZERO_AXIS", "PROVED_DELTA_D_Z_ZERO_EQUALS_ZERO"),
    ("V46_LOCAL_PROFILE_ZERO_MEAN", "PROVED_SUM_A_MOD_D_DELTA_D_Z_A_EQUALS_ZERO"),
    ("V46_PROPER_FACTOR_CONGRUENCE", "PROVED_D_DIVIDES_T_IMPLIES_DELTA_D_Z_U_MINUS_T_EQUALS_DELTA_D_Z_U"),
    ("V46_COMMON_TRANSITION_SPLIT", "PROVED_EXACT_LOCAL_PLUS_AP_RESIDUAL_BEFORE_OUTER_ABSOLUTE"),
    ("V46_TRANSITION_NATIVE_CARRIER", "PROVED_EXACT_WITH_LOG_T_PLUS_H_DENOMINATOR"),
    ("V46_TRANSITION_NATIVE_CARRIER_ZERO_AXIS", "PROVED_EXACT_ZERO"),
    ("V46_LOCAL_RADICAL_ACTIVE_RANGE", "PROVED_R_GE_H_OVER_Q_EQUALS_X_POWER_31_OVER_96"),
    ("V46_LOCAL_P_BRANCH", "PROVED_EXACT_MU_R_OVER_PHI_R_TIMES_E_R_2_A_QBAR"),
    ("V46_LOCAL_B_BRANCH", "PROVED_EXACT_MU_R0_OVER_PHI_R0_PHI_R1_SQUARED_TIMES_E_R0_2_A_QR1_BAR"),
    ("V46_LOCAL_COEFFICIENT_L2_P_BRANCH", "PROVED_X_OVER_S_POWER_3_OVER_2"),
    ("V46_LOCAL_COEFFICIENT_L2_B_BRANCH", "PROVED_X_OVER_S_POWER_3_OVER_2_R1_CUBED"),
    ("V46_LOCAL_BETTIN_CHANDEE_ATTACHMENT", "SOURCE_BACKED_BY_V29_COMPILER_WITH_PROPER_FACTOR_AS_SELECTED_GROUP"),
    ("V46_LOCAL_NORMALIZED_OUTPUT", "PROVED_X_POWER_1891_OVER_1920_PLUS_O1"),
    ("V46_LOCAL_NUMERATOR_OUTPUT", "PROVED_X_POWER_1057_OVER_640_PLUS_O1"),
    ("V46_LOCAL_ENDPOINT_MARGIN", "121_OVER_9600"),
    ("V46_AP_RESIDUAL", "PROVED_EXACT_W_MINUS_DELTA_D_Z_OVER_LOG_U_IN_EACH_RESIDUE_CLASS"),
    ("V46_AP_PARSEVAL", "PROVED_EXACT_SUM_R_FOURIER_SQUARED_EQUALS_D_SUM_A_RESIDUAL_SQUARED"),
    ("V46_RECIPROCAL_OCCUPANCY", "PROVED_EXACT_A_D_R_WITH_M_QBAR_MOD_D"),
    ("V46_RECIPROCAL_COLLISION", "PROVED_M1_Q2_MINUS_M2_Q1_EQUALS_ELL_D_WITH_ABS_ELL_LE_P_X_O1"),
    ("V46_RECIPROCAL_OCCUPANCY_ENERGY", "PROVED_ELEMENTARY_P_SQUARED_X_O1"),
    ("V46_RECIPROCAL_OCCUPANCY_ENERGY_EXPONENT", "1_OVER_48"),
    ("V46_TRANSITION_AP_BDH_ENERGY", "DEFINED_SUM_D_SUM_A_D_TIMES_ABS_RESIDUAL_SQUARED"),
    ("V46_TRANSITION_AP_BDH_NATURAL_SCALE", "X_TIMES_U_SQUARED_EQUALS_X_POWER_333_OVER_200"),
    ("V46_TRANSITION_AP_BDH_GATE", "OPEN_X_U_SQUARED_X_POWER_RHO_WITH_ZERO_LE_RHO_LT_33_OVER_100"),
    ("V46_AP_RESIDUAL_NUMERATOR_OUTPUT", "CONDITIONAL_X_POWER_1799_OVER_1200_PLUS_RHO_OVER_2_PLUS_O1"),
    ("V46_AP_RESIDUAL_NORMALIZED_OUTPUT", "CONDITIONAL_X_POWER_333_OVER_400_PLUS_RHO_OVER_2_PLUS_O1"),
    ("V46_AP_RESIDUAL_MARGIN", "33_OVER_200_MINUS_RHO_OVER_2"),
    ("V46_TRANSITION_CONDITIONAL_COMPILER", "PROVED_AP_BDH_GATE_PAYS_FULL_TRANSITION_WITH_LOCAL_AND_V44_CORRECTIONS"),
    ("V46_TRANSITION_CONDITIONAL_MARGIN", "MIN_121_OVER_9600_33_OVER_200_MINUS_RHO_OVER_2_13_OVER_4800_817_OVER_4800"),
    ("V46_AP_GATE_STRENGTH", "SUFFICIENT_WHOLE_OBJECT_THEOREM_STRONGER_THAN_ONLY_V45_LOW_CONDUCTOR_GATE"),
    ("V46_LOW_EXCEPTIONAL_CHARACTER_FIREWALL", "RETAINED_INSIDE_AP_RESIDUAL_NO_LANDAU_PAGE_POWER_BORROWED"),
    ("V46_LONG_BALANCED_WINDOW", "OPEN_D_GT_U_AND_K_GT_U"),
    ("V46_LONG_REVERSE_TYPE_I_WINDOW", "OPEN_D_GT_U_AND_K_LE_U"),
    ("V46_V42_GATE_B", "RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE"),
    ("V46_BETTIN_CHANDEE_LOCAL_ATTACHMENT", "SOURCE_BACKED_TRANSITION_NATIVE_EULER_COMPONENT_ONLY"),
    ("V46_CLASSICAL_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_REQUIRES_MODULUS_SCALE_X_LOG_POWER_MINUS_A_NOT_U_X_POWER_133_OVER_400"),
    ("V46_HARPER_GENERAL_SEQUENCE_DIRECT_ATTACHMENT", "STOP_SCOPED_REQUIRES_Q_GREATER_THAN_SQRT_2X_AND_MODULUS_INDEPENDENT_SEQUENCE_HYPOTHESES"),
    ("V46_KMT_MULTIPLICATIVE_AP_DIRECT_ATTACHMENT", "STOP_SCOPED_BOUNDED_MULTIPLICATIVE_ALMOST_ALL_MODULI_NOT_SHIFTED_LAMBDA_MINUS_D_DEPENDENT_HYBRID_PROFILE"),
    ("V46_FIORILLI_HOOLEY_VARIANCE", "HEURISTIC_SUPPORT_ONLY_NO_UNIFORM_LITERAL_THEOREM_BELOW_SQUARE_ROOT"),
    ("V46_DIRECT_PRIMARY_SOURCE_FOR_AP_BDH_GATE", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10"),
    ("V46_FIRST_FATAL", "NO_LITERAL_THEOREM_PROVES_THE_NATURAL_SCALE_ALL_RESIDUE_AP_VARIANCE_FOR_LAMBDA_U_PLUS_2_MINUS_B_Z_U_MINUS_THE_PROPER_FACTOR_LOCAL_PROFILE_UNIFORMLY_FOR_X_POWER_31_OVER_96_LT_D_LE_X_POWER_133_OVER_400"),
    ("V46_ROUTE_POSITION", "ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TRANSITION_LOCAL_EULER_PAID_AP_BDH_RESIDUAL_OPEN_LONG_MOBIUS_SPAN_OPEN"),
    ("V46_SOURCE_LOCK_POLICY", "PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED"),
    ("V46_ROUTE_MAP_REFERENCE", "TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B"),
)


EXPECTED_REGISTRY_SHA256 = "d0948832a3d6e7921b8730f69826fc4499b25caa1e53066a7769d6f62176de99"


SOURCE_ITEMS = (
    ("BETTIN_CHANDEE", "arXiv:1502.00769v1_Theorem_1_trilinear_Kloosterman_fractions"),
    ("LEWKO_LEWKO", "arXiv:1111.6190v2_Theorem_1_classical_BDH_range_x_log_minus_A_to_x"),
    ("HARPER", "arXiv:2412.19644v1_Theorems_1_2_require_sqrt_2x_less_Q"),
    ("FIORILLI", "arXiv:1301.5663_Hooley_variance_below_sqrt_is_conjectural"),
    ("KMT", "arXiv:1909.12280_bounded_multiplicative_almost_all_moduli_wrong_object"),
)


DEPENDENCIES = (
    ("research/tpc-big-road/bridge_b_transition_native_euler_bdh_compiler.md", "f834c13f689b8283c40bd962b0ec4fa5cdcaaee061eca1914a6356a1cfd96011"),
    ("research/tpc-big-road/bridge_b_conductor_stratified_transition_spectrum.md", "0a797eb4e3791319624fb5dd7a597d6d6bb217b46759739a51854312df6f4ec9"),
    ("research/tpc-big-road/tpc_bridge_b_conductor_stratified_transition_checker.py", "6b726a75674587ce9ec8450f4b462b90d685ac267519f68c732b8794962b51b6"),
    ("research/tpc-big-road/bridge_b_transition_reciprocal_variance_and_ramanujan_mean.md", "053ae6a18740a2e81d754c4ecce7af1a00ecfe331f7d5d4991945889f14c9920"),
    ("research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md", "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a"),
    ("research/tpc-big-road/bridge_b_joint_major_minor_and_low_christoffel.md", "c4b61b790911d2cfcb3d7a0139d368a35d0d0fdab2984637f3f2fe30638543ab"),
    ("research/tpc-big-road/tpc_bridge_b_joint_major_minor_checker.py", "a016840f1ce41b4ed7ee2e315e7848922da1247828f68dfaf3b62e46fac8fa8c"),
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
        if dict_type(candidate).get("V46_MAXIMUM_CLAIM") != literal_maximum_claim:
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

    def local_f(p: int, a: int) -> Fraction:
        return fraction_type(0) if (a + 2) % p == 0 else fraction_type(p, p - 1)

    def local_g(p: int, z: int, a: int) -> Fraction:
        if p <= z:
            return local_f(p, a)
        if a % p == 0:
            return fraction_type(p, p - 1)
        return fraction_type(p * (p - 2), (p - 1) * (p - 1))

    def gaussian_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
        return (a[0] + b[0], a[1] + b[1])

    def gaussian_scale(c: int, a: tuple[int, int]) -> tuple[int, int]:
        return (c * a[0], c * a[1])

    def gaussian_norm(a: tuple[int, int]) -> int:
        return a[0] * a[0] + a[1] * a[1]

    def i_power(k: int) -> tuple[int, int]:
        return ((1, 0), (0, 1), (-1, 0), (0, -1))[k % 4]

    def finite_items() -> tuple[tuple[str, object], ...]:
        delta5 = tuple_type(local_f(5, a) - local_g(5, 3, a) for a in range_fn(5))
        expected_delta5 = (
            fraction_type(0), fraction_type(5, 16), fraction_type(5, 16),
            fraction_type(-15, 16), fraction_type(5, 16),
        )
        if delta5 != expected_delta5 or sum_fn(delta5, fraction_type(0)) != 0 or delta5[0] != 0:
            raise failure_type("local profile fixture changed")

        d, t, h, u = 5, 35, 2, 37
        if t % d != 0 or (u - t) != h or delta5[h % d] != delta5[u % d]:
            raise failure_type("proper factor congruence changed")

        ap_vector = (2, -1, 3, -4)
        transforms = list_type()
        for r in range_fn(4):
            value = (0, 0)
            for a, coefficient in enumerate_fn(ap_vector):
                value = gaussian_add(value, gaussian_scale(coefficient, i_power(r * a)))
            transforms.append(value)
        transforms_tuple = tuple_type(transforms)
        parseval_left = sum_fn((gaussian_norm(value) for value in transforms_tuple), 0)
        parseval_right = 4 * sum_fn((value * value for value in ap_vector), 0)
        if transforms_tuple != ((0, 0), (-1, 3), (10, 0), (-1, -3)):
            raise failure_type("finite additive transform changed")
        if parseval_left != 120 or parseval_right != parseval_left:
            raise failure_type("finite Parseval changed")

        residues = list_type()
        pairs = list_type()
        for q in (7, 11):
            for m in (-2, -1, 1, 2):
                residue = m * pow_fn(q, -1, 5) % 5
                residues.append(residue)
                pairs.append((q, m, residue))
        counts = tuple_type(sum_fn((1 for residue in residues if residue == r), 0) for r in range_fn(5))
        occupancy_energy = sum_fn((count * count for count in counts), 0)
        collision_count = sum_fn(
            (1 for q1, m1, _ in pairs for q2, m2, _ in pairs if (m1 * q2 - m2 * q1) % 5 == 0),
            0,
        )
        if counts != (0, 2, 2, 2, 2) or occupancy_energy != 16 or collision_count != 16:
            raise failure_type("reciprocal occupancy fixture changed")

        h_exp = fraction_type(21, 32)
        q_exp = fraction_type(1, 3)
        u_exp = fraction_type(133, 400)
        y0_exp = h_exp - q_exp
        p_exp = 2 * q_exp - h_exp
        coefficient_energy_exp = 2 * p_exp
        ap_energy_exp = 1 + 2 * u_exp
        ap_sqrt_exp = ap_energy_exp / 2
        residual_numerator_exp = h_exp + p_exp + ap_sqrt_exp
        residual_normalized_exp = residual_numerator_exp - 2 * q_exp
        target_numerator_exp = fraction_type(1997, 1200)
        target_normalized_exp = fraction_type(399, 400)
        residual_margin = target_numerator_exp - residual_numerator_exp
        local_normalized_exp = fraction_type(1891, 1920)
        local_numerator_exp = local_normalized_exp + 2 * q_exp
        local_margin = target_numerator_exp - local_numerator_exp
        generic_large_sieve_gap = 2 - ap_energy_exp

        expected_exponents = (
            fraction_type(31, 96), fraction_type(1, 96), fraction_type(1, 48),
            fraction_type(333, 200), fraction_type(1799, 1200),
            fraction_type(333, 400), fraction_type(33, 200),
            fraction_type(1057, 640), fraction_type(121, 9600),
            fraction_type(67, 200),
        )
        actual_exponents = (
            y0_exp, p_exp, coefficient_energy_exp, ap_energy_exp,
            residual_numerator_exp, residual_normalized_exp, residual_margin,
            local_numerator_exp, local_margin, generic_large_sieve_gap,
        )
        if actual_exponents != expected_exponents:
            raise failure_type("rational exponent ledger changed")
        if target_normalized_exp - residual_normalized_exp != fraction_type(33, 200):
            raise failure_type("normalized residual margin changed")
        if not (u_exp < fraction_type(1, 2) and y0_exp < u_exp):
            raise failure_type("source range firewall changed")

        rho_sample = fraction_type(1, 10)
        rho_output = residual_numerator_exp + rho_sample / 2
        rho_margin = target_numerator_exp - rho_output
        if rho_margin != fraction_type(23, 200) or not (rho_sample < fraction_type(33, 100)):
            raise failure_type("rho slack compiler changed")

        return (
            ("delta5", tuple_type(str_type(value) for value in delta5)),
            ("delta5_sum", str_type(sum_fn(delta5, fraction_type(0)))),
            ("proper_factor_congruence_value", str_type(delta5[h % d])),
            ("dft4", transforms_tuple),
            ("parseval_energy", parseval_left),
            ("occupancy_counts", counts),
            ("occupancy_energy", occupancy_energy),
            ("collision_count", collision_count),
            ("Y0_exponent", str_type(y0_exp)),
            ("P_exponent", str_type(p_exp)),
            ("coefficient_energy_exponent", str_type(coefficient_energy_exp)),
            ("AP_energy_exponent", str_type(ap_energy_exp)),
            ("residual_numerator_exponent", str_type(residual_numerator_exp)),
            ("residual_normalized_exponent", str_type(residual_normalized_exp)),
            ("residual_margin", str_type(residual_margin)),
            ("local_numerator_exponent", str_type(local_numerator_exp)),
            ("local_margin", str_type(local_margin)),
            ("generic_large_sieve_gap", str_type(generic_large_sieve_gap)),
            ("rho_sample", str_type(rho_sample)),
            ("rho_sample_margin", str_type(rho_margin)),
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
