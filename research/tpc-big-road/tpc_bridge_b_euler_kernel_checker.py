#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V28 big-road audit."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_OCCURRENCE_NATIVE_EULER_ZERO_AXIS_AND_REDUCED_RADICAL_CORRIDOR_"
    "PLUS_SOURCE_BACKED_CONDITIONAL_BETTIN_CHANDEE_ENGINE_PLUS_STATIONARY_"
    "FACTOR_NO_GO_AND_COMPRESSED_KERNEL_ROUTE"
)


CONTRACT = {
    "maximum_claim": MAXIMUM_CLAIM,
    "route_advance": "YES",
    "fixed_h0": 2,
    "physical_scale": "x=2X",
    "comparison_cutoff": "z=(log x)^K",
    "prime_shell_Q_exponent": "1/3",
    "difference_horizon_exponent": "21/32",
    "master_group_lower_exponent": "133/400",
    "master_group_upper_exponent": "1/2",
    "local_prime_shift": "-2",
    "local_euler_zero": "PROVED_EXACT",
    "local_euler_mean": "PROVED_EXACT",
    "ramanujan_pairing": "PROVED_EXACT",
    "local_main_actual_AP_status": "OPEN_ATTACHMENT",
    "generic_smooth_main": "STOP_SCOPED_CIRCULAR_COEFFICIENT_ONE",
    "joint_local_main_J_plus_E": "PROVED_EXACT_ZERO",
    "reduced_radical": "R=D/gcd(n,D)",
    "F_phase": "mu(R)/phi(R)*e_R(+2*a*q_inverse)",
    "G_phase": "mu(R0)/(phi(R0)*phi(R1)^2)*e_R0(+2*a*(qR1)_inverse)",
    "active_reduced_radical_exponent": "31/96",
    "dual_length_upper_exponent": "17/96",
    "primitive_lower_master_dual_exponent": "23/2400",
    "selected_master_radical_l2": "PROVED_ELEMENTARY",
    "BC_source": "arXiv:1502.00769v1_Theorem_1",
    "BC_corridor_status": "SOURCE_BACKED_CONDITIONAL_COMPILER",
    "BC_corridor_exponent": "1891/1920",
    "BC_margin_to_endpoint": "121/9600",
    "BC_literal_emitter": "OPEN_EXACT_COMPILER",
    "boundary_exponent": "47/48",
    "boundary_margin": "11/600",
    "bulk_absolute_ceiling": "1",
    "bulk_required_saving": "1/400",
    "residual_theta_ceiling": "13/4800",
    "MRT_abstract_reduction": "SOURCE_BACKED_ABSTRACT_INTERFACE_ONLY",
    "literal_product_local_flatness": "OPEN_NEW_THEOREM",
    "one_sided_MRT": "STOP_SCOPED_H_QUARTER_LOSS",
    "primary_analytic_gate": "TAGGED_JOINT_MAIN_ERROR_RESIDUAL_COMPILER",
    "stationary_factor": "STOP_SCOPED_ROOT_OF_UNITY_EIGENFUNCTION",
    "dynamics_mode": "NONAUTONOMOUS_LOW_NORM_KERNEL_OPEN",
    "kernel_mean_normalization": "INTEGRAL_K_EQUALS_1",
    "kernel_sufficient_condition": "NORM_K_TIMES_V=o(x/log^2x)",
    "primorial_riesz_norm": "SQRT_P",
    "henon_status": "SOURCE_BACKED_GEOMETRY_ONLY",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
    "numbered_release": "NO",
}


REGISTRY_ITEMS = (
    ("V28_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V28_ROUTE_ADVANCE", "YES"),
    ("V28_ARITHMETIC_ADVANCE", "NO"),
    ("V28_FIXED_ATOM_CREDIT", "0"),
    ("V28_STRICT_1_OVER_400", "UNPAID"),
    ("V28_L2", "NONE"),
    ("V28_TPC_207_TRIGGER", "false"),
    ("V28_NUMBERED_RELEASE", "NO"),
    (
        "V28_MASTER_OCCURRENCE_LOCAL_EULER_TENSOR",
        "PROVED_EXACT_ALGEBRAIC",
    ),
    (
        "V28_LOCAL_EULER_ZERO_MEAN_RAMANUJAN_ORTHOGONALITY",
        "PROVED_EXACT_ALGEBRAIC",
    ),
    (
        "V28_LOCAL_EULER_TENSOR_AS_ACTUAL_WEIGHTED_AP_MAIN",
        "OPEN_ATTACHMENT",
    ),
    (
        "V28_SMOOTH_MAIN_WITH_M0_EQUAL_PHYSICAL_TARGET",
        "STOP_SCOPED_CIRCULAR_ZERO_AXIS_COEFFICIENT_ONE",
    ),
    (
        "V28_LOCAL_MAIN_JUTILA_J_PLUS_E_CANCELLATION",
        "PROVED_EXACT_ALGEBRAIC",
    ),
    (
        "V28_REDUCED_RADICAL_CRT_PHASE",
        "PROVED_EXACT_G_CANCELLATION_AND_PLUS_TWO_PHASE",
    ),
    (
        "V28_LOCAL_MAIN_SHARED_Q_DIVIDES_RADICAL_BRANCH",
        "PROVED_EXACT_AFTER_FULL_UNIT_FREQUENCY_SUM",
    ),
    (
        "V28_SELECTED_MASTER_RADICAL_L2_ENVELOPE",
        "PROVED_ELEMENTARY_FROM_ORDERED_D2_D4_AND_RADICAL_EULER_SUM",
    ),
    (
        "V28_SHORT_INVERSE_RESIDUE_BETTIN_CHANDEE_CORRIDOR",
        "SOURCE_BACKED_POWER_SAVING_AFTER_EXACT_COMPILER",
    ),
    (
        "V28_SHORT_INVERSE_RESIDUE_CORRIDOR_EXPONENT",
        "1891/1920",
    ),
    (
        "V28_SHORT_INVERSE_RESIDUE_CORRIDOR_MARGIN_TO_399_400",
        "121/9600",
    ),
    (
        "V28_LITERAL_MASTER_CORRIDOR_SMOOTH_EMITTER_AND_G_REASSEMBLY",
        "OPEN_EXACT_COMPILER",
    ),
    (
        "V28_LOCAL_MAIN_HARD_SHELL_ENDPOINT",
        "PROVED_ELEMENTARY_X_47_OVER_48_PLUS_EPSILON",
    ),
    (
        "V28_MRT_ABSTRACT_PRODUCT_LOCAL_L2_REDUCTION",
        "SOURCE_BACKED_ABSTRACT_INTERFACE_ONLY",
    ),
    (
        "V28_LITERAL_BILINEAR_PRODUCT_LOCAL_FLATNESS",
        "OPEN_NEW_THEOREM",
    ),
    (
        "V28_ONE_SIDED_MRT_TO_ENDPOINT",
        "STOP_SCOPED_H_QUARTER_LOSS",
    ),
    (
        "V28_TAGGED_RESIDUAL_JUTILA_MAIN_ERROR_REASSEMBLY",
        "SELECTED_PRIMARY_OPEN_ATTACHMENT",
    ),
    (
        "V28_STATIONARY_MIXING_TO_ROTATION_ODOMETER_FACTOR",
        "STOP_SCOPED_ROOT_OF_UNITY_EIGENFUNCTION_NO_GO",
    ),
    (
        "V28_NONAUTONOMOUS_POINTED_ESCAPE",
        "LOGICALLY_OPEN_EXACT_STAGE_DIAGRAM_REQUIRED",
    ),
    (
        "V28_LOW_NORM_POINT_EVALUATION_KERNEL_CRITERION",
        "PROVED_EXACT_ALGEBRAIC",
    ),
    (
        "V28_POSITIVE_MEAN_WITHOUT_KERNEL_COVARIANCE_CONTROL",
        "STOP_SCOPED_EXACT_TWO_POINT_FALSIFIERS",
    ),
    (
        "V28_FULL_PRIMORIAL_POINT_RIESZ_NORM",
        "PROVED_EXACT_FINITE_PLUS_STANDARD_PNT_ASYMPTOTIC",
    ),
    (
        "V28_COMPRESSED_TARGET_INDEPENDENT_KERNEL_WHOLE_SHELL_COMPILER",
        "SELECTED_DYNAMICS_OPEN_NEW_THEOREM",
    ),
    (
        "V28_ABP_HNTV_INTERFACES",
        "SOURCE_BACKED_TOOL_CLASSES_ONLY",
    ),
    (
        "V28_HENON_WANG_YOUNG_DENSE_TREE_NATURAL_EXTENSION",
        "SOURCE_BACKED_TOPOLOGICAL_GEOMETRY_ONLY",
    ),
    (
        "V28_HENON_TPC_STAGE_EVENT_MEASURE_SEED_FUNCTIONAL_DIAGRAM",
        "OPEN_ATTACHMENT",
    ),
    ("V28_O161_PARENTS_PAIR_NATIVE_H1_GLOBAL", "OPEN_UNCHANGED"),
    (
        "V28_A1_A2_TAIL_SELECTION_PACKET_PROVENANCE",
        "INDEPENDENT_AND_UNPAID",
    ),
)


EXPECTED_REGISTRY_SHA256 = "2926e4dc94080ff3179970dc134c1a1edb76bcb5b7f64be783b4bc747d5c7a0b"


SOURCE_ITEMS = (
    ("MRT_PRODUCT_L2", "arXiv:1707.01315v3_Proposition_3.1"),
    ("BETTIN_CHANDEE", "arXiv:1502.00769v1_Theorem_1"),
    ("ABP_CRITICAL_SEED", "arXiv:2212.12202v2_Theorem_1.1"),
    ("HNTV_SEQUENTIAL", "arXiv:1406.4266_Theorem_3.1"),
    (
        "BORONSKI_STIMAC_HENON",
        "arXiv:2104.14780_Wang_Young_natural_extension_geometry",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_shbd2_innovation.md",
        "95c4ba99be6927b38adb4b5fdda19191413720eaf3cc621e6f0d0309211e111e",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py",
        "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519",
    ),
    (
        "research/tpc-big-road/fm_local_comparison_compiler.md",
        "4f7537ff5a10d53634638afff508ee6e3401364dab7970852b327470918c644f",
    ),
    (
        "research/tpc-big-road/bridge_b_ramanujan_energy_and_pointed_block_gate.md",
        "90f8cd26b9dd6b99a4f5083e80cdf13fc6ec2498081e269455f9b12726e66c5c",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_ramanujan_energy_checker.py",
        "61bba5c8f860617e5e938b29a77d2ca85adddd4ce79f1b3e33811c31ab1d4580",
    ),
    (
        "research/tpc-big-road/bridge_b_euler_zero_axis_and_kernel_carrier.md",
        "922d5601b088a8a3a8dd52d3e9d186c85e7fea00ca670f3c6f324c1d433da464",
    ),
)


def _prime_factors(value: int) -> tuple[int, ...]:
    factors: list[int] = []
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def _phi(value: int) -> int:
    result = value
    for prime in _prime_factors(value):
        result = result // prime * (prime - 1)
    return result


def _mu_squarefree(value: int) -> int:
    return -1 if len(_prime_factors(value)) % 2 else 1


def _ramanujan_prime(prime: int, residue: int) -> int:
    return prime - 1 if residue % prime == 0 else -1


def _F(prime: int, residue: int) -> Fraction:
    if (residue + 2) % prime == 0:
        return Fraction(0)
    return Fraction(prime, prime - 1)


def _G(prime: int, cutoff: int, residue: int) -> Fraction:
    if prime <= cutoff:
        return _F(prime, residue)
    if residue % prime == 0:
        return Fraction(prime, prime - 1)
    return Fraction(prime * (prime - 2), (prime - 1) ** 2)


def _delta(modulus_source: int, cutoff: int, residue: int) -> Fraction:
    p_value = Fraction(1)
    b_value = Fraction(1)
    for prime in _prime_factors(modulus_source):
        p_value *= _F(prime, residue)
        b_value *= _G(prime, cutoff, residue)
    return p_value - b_value


def _finite_fixtures() -> dict[str, object]:
    local = tuple(_delta(5, 3, residue) for residue in range(5))
    if local != (
        Fraction(0),
        Fraction(5, 16),
        Fraction(5, 16),
        Fraction(-15, 16),
        Fraction(5, 16),
    ):
        raise CheckFailure("local p=5 Euler profile changed")
    if sum(local) != 0:
        raise CheckFailure("local Euler mean changed")
    if sum(_ramanujan_prime(5, h) * local[h] for h in range(5)) != 0:
        raise CheckFailure("local Ramanujan pairing changed")

    tensor_cases = (
        (30, 5, 7),
        (1122, 5, 13),
        (187, 5, 13),
        (187, 5, 11),
        (1309, 7, 19),
    )
    tensor_rows = 0
    tensor_support = 0
    for source, cutoff, q in tensor_cases:
        radical = math.prod(_prime_factors(source))
        period = math.lcm(radical, q)
        values = tuple(_delta(source, cutoff, h) for h in range(period))
        if values[0] != 0:
            raise CheckFailure("composite Euler zero changed")
        if sum(values) != 0:
            raise CheckFailure("composite Euler mean changed")
        if sum(_ramanujan_prime(q, h) * values[h] for h in range(period)) != 0:
            raise CheckFailure("composite Ramanujan orthogonality changed")
        tensor_rows += period
        tensor_support += sum(value != 0 for value in values)
        if source == 30 and any(values):
            raise CheckFailure("all-small-prime tensor must vanish")
    if tensor_support == 0:
        raise CheckFailure("composite tensor fixtures are vacuous")

    D = 30
    q = 11
    n = 2
    inverse_q_D = pow(q, -1, D)
    r = n * inverse_q_D % D
    local_indices = tuple(
        (prime, r * pow(D // prime, -1, prime) % prime)
        for prime in _prime_factors(D)
    )
    g = math.gcd(n, D)
    R = D // g
    a = n // g
    correct_phase = 2 * a * pow(q, -1, R) % R
    wrong_g_phase = 2 * g * a * pow(q, -1, R) % R
    if (
        inverse_q_D != 11
        or r != 22
        or local_indices != ((2, 0), (3, 1), (5, 2))
        or R != 15
        or correct_phase != 7
        or wrong_g_phase != 14
    ):
        raise CheckFailure("reduced-radical CRT phase changed")
    for prime, index in local_indices:
        if prime in _prime_factors(R):
            reconstructed = correct_phase * pow(R // prime, -1, prime) % prime
            if reconstructed != 2 * index % prime:
                raise CheckFailure("CRT phase does not reconstruct local +2 phase")

    D_g = 165
    q_g = 7
    n_g = 6
    cutoff_g = 5
    g_g = math.gcd(D_g, n_g)
    R_g = D_g // g_g
    a_g = n_g // g_g
    R0 = math.prod(p for p in _prime_factors(R_g) if p <= cutoff_g)
    R1 = math.prod(p for p in _prime_factors(R_g) if p > cutoff_g)
    g_phase = 2 * a_g * pow(q_g * R1, -1, R0) % R0
    g_amplitude = Fraction(_mu_squarefree(R0), _phi(R0) * _phi(R1) ** 2)
    if (g_g, R_g, R0, R1, g_phase, g_amplitude) != (
        3,
        55,
        5,
        11,
        2,
        Fraction(-1, 400),
    ):
        raise CheckFailure("hybrid reduced phase changed")

    active = tuple(
        a0
        for a0 in range(-10, 11)
        if a0 and abs(a0) * 100 <= 11 * 13 and math.gcd(a0, 11 * 13) == 1
    )
    empty = tuple(
        a0
        for a0 in range(-10, 11)
        if a0 and abs(a0) * 100 <= 11 * 7 and math.gcd(a0, 11 * 7) == 1
    )
    if active != (-1, 1) or empty:
        raise CheckFailure("reduced corridor support changed")

    radical_euler_30 = Fraction(1, _phi(30))
    if radical_euler_30 != Fraction(1, 8):
        raise CheckFailure("radical Euler sum changed")

    active_exponent = Fraction(21, 32) - Fraction(1, 3)
    dual_upper = Fraction(1, 3) + Fraction(1, 2) - Fraction(21, 32)
    primitive_lower = Fraction(1, 3) + Fraction(133, 400) - Fraction(21, 32)
    boundary = Fraction(21, 32) * 2 - Fraction(1, 3)
    boundary_margin = Fraction(399, 400) - boundary
    residual_margin = Fraction(399, 400) - Fraction(191, 192)
    one_sided_loss = Fraction(21, 128)
    one_sided_deficit = one_sided_loss - residual_margin
    bc_left = Fraction(2077, 1920) - Fraction(3, 10) * active_exponent
    bc_at_third_left = Fraction(2077, 1920) - Fraction(1, 10)
    bc_at_third_right = Fraction(639, 640) - Fraction(1, 60)
    bc_margin = Fraction(399, 400) - bc_left
    bc_F_second_low = Fraction(737, 768)
    bc_F_second_high = Fraction(23, 24)
    bc_G_first_branch_one = (
        Fraction(2077, 1920) - Fraction(3, 10) * Fraction(31, 96)
    )
    bc_G_first_branch_two = Fraction(1917, 1920) - Fraction(1, 60)
    bc_G_second_branch_one = Fraction(1) - Fraction(31, 96) / 8
    bc_G_second_branch_two = Fraction(23, 24)
    if (
        active_exponent != Fraction(31, 96)
        or dual_upper != Fraction(17, 96)
        or primitive_lower != Fraction(23, 2400)
        or boundary != Fraction(47, 48)
        or boundary_margin != Fraction(11, 600)
        or residual_margin != Fraction(13, 4800)
        or one_sided_deficit != Fraction(1549, 9600)
        or bc_left != Fraction(1891, 1920)
        or bc_at_third_left != Fraction(377, 384)
        or bc_at_third_right != Fraction(377, 384)
        or bc_margin != Fraction(121, 9600)
        or bc_F_second_low != Fraction(737, 768)
        or bc_F_second_high != Fraction(23, 24)
        or bc_G_first_branch_one != Fraction(1891, 1920)
        or bc_G_first_branch_two != Fraction(377, 384)
        or bc_G_second_branch_one != Fraction(737, 768)
        or bc_G_second_branch_two != Fraction(23, 24)
    ):
        raise CheckFailure("V28 exponent ledger changed")

    kappa = {-1: Fraction(1, 3), 0: Fraction(1), 1: Fraction(-1, 4)}
    circular = {-1: Fraction(2), 0: Fraction(7), 1: Fraction(-3)}
    local_main = {-1: Fraction(2), 0: Fraction(0), 1: Fraction(-3)}

    def joint(values: dict[int, Fraction]) -> tuple[Fraction, Fraction]:
        j_value = sum(kappa[h] * values[h] for h in kappa)
        return j_value, values[0] - j_value

    circular_j, circular_e = joint(circular)
    local_j, local_e = joint(local_main)
    if (
        circular_j,
        circular_e,
        circular_j + circular_e,
        local_j,
        local_e,
        local_j + local_e,
    ) != (
        Fraction(101, 12),
        Fraction(-17, 12),
        Fraction(7),
        Fraction(17, 12),
        Fraction(-17, 12),
        Fraction(0),
    ):
        raise CheckFailure("joint J plus E fixture changed")

    mixing_correlations = tuple(1 if n0 % 2 == 0 else -1 for n0 in range(4))
    if mixing_correlations != (1, -1, 1, -1):
        raise CheckFailure("rotation eigenfunction fixture changed")

    signed_K = (Fraction(3), Fraction(-1))
    signed_S = (Fraction(1), Fraction(3))
    nonnegative_K = (Fraction(2), Fraction(0))
    nonnegative_S = (Fraction(0), Fraction(1))

    def mean(values: tuple[Fraction, ...]) -> Fraction:
        return sum(values) / len(values)

    signed_pairing = mean(tuple(k * s for k, s in zip(signed_K, signed_S)))
    nonnegative_pairing = mean(
        tuple(k * s for k, s in zip(nonnegative_K, nonnegative_S))
    )
    if (
        mean(signed_K),
        mean(signed_S),
        signed_pairing,
        mean(nonnegative_K),
        mean(nonnegative_S),
        nonnegative_pairing,
    ) != (
        Fraction(1),
        Fraction(2),
        Fraction(0),
        Fraction(1),
        Fraction(1, 2),
        Fraction(0),
    ):
        raise CheckFailure("pointed kernel falsifier changed")

    primorial_norms = tuple(
        int(sum(Fraction(P * P if index == 0 else 0, P) for index in range(P)))
        for P in (30, 210)
    )
    if primorial_norms != (30, 210):
        raise CheckFailure("primorial Riesz norm changed")

    return {
        "local_delta_profile": tuple(str(value) for value in local),
        "tensor_cases": len(tensor_cases),
        "tensor_rows": tensor_rows,
        "tensor_support": tensor_support,
        "crt_local_indices": local_indices,
        "crt_correct_phase_mod_15": correct_phase,
        "crt_wrong_g_phase_mod_15": wrong_g_phase,
        "hybrid_R0_R1": (R0, R1),
        "hybrid_phase_mod_R0": g_phase,
        "hybrid_amplitude": str(g_amplitude),
        "corridor_active_a": active,
        "corridor_empty": len(empty) == 0,
        "radical_euler_sum_D30": str(radical_euler_30),
        "active_radical_exponent": str(active_exponent),
        "dual_upper_exponent": str(dual_upper),
        "primitive_lower_dual_exponent": str(primitive_lower),
        "boundary_exponent": str(boundary),
        "boundary_margin": str(boundary_margin),
        "residual_margin": str(residual_margin),
        "one_sided_deficit": str(one_sided_deficit),
        "BC_corridor_exponent": str(bc_left),
        "BC_margin": str(bc_margin),
        "BC_F_second_term_maxima": (
            str(bc_F_second_low),
            str(bc_F_second_high),
        ),
        "BC_G_first_term_endpoints": (
            str(bc_G_first_branch_one),
            str(bc_G_first_branch_two),
        ),
        "BC_G_second_term_maxima": (
            str(bc_G_second_branch_one),
            str(bc_G_second_branch_two),
        ),
        "BC_F_parameter_map": "A=QR/H,M=Q,N=R,theta=plus_or_minus_2",
        "BC_G_parameter_map": "A=QR0R1/H,M=QR1,N=R0",
        "BC_outside_normalization": "H/L_pr",
        "BC_coprimality": "(M,N)=1_AFTER_MOBIUS_SPLIT",
        "BC_array_norms": "Q^(1/2+o),A^(1/2+o),R_ARRAY_FROM_5_12_5_13",
        "joint_circular_output": str(circular_j + circular_e),
        "joint_local_output": str(local_j + local_e),
        "mixing_correlations": mixing_correlations,
        "signed_kernel_pairing": str(signed_pairing),
        "nonnegative_kernel_pairing": str(nonnegative_pairing),
        "primorial_norms_squared": primorial_norms,
    }


def _make_trusted_runner(
    contract_seed=tuple(CONTRACT.items()),
    registry_seed=REGISTRY_ITEMS,
    registry_digest_seed=EXPECTED_REGISTRY_SHA256,
    source_seed=SOURCE_ITEMS,
    dependency_seed=DEPENDENCIES,
    fixture_seed=tuple(_finite_fixtures().items()),
    root_seed=Path(__file__).resolve().parents[2],
    failure_type=CheckFailure,
    serializer=json.dumps,
    hash_constructor=hashlib.sha256,
    dict_type=dict,
    type_type=type,
    bool_type=bool,
    int_type=int,
    tuple_type=tuple,
    str_type=str,
    list_type=list,
    set_type=set,
    frozenset_type=frozenset,
    len_fn=len,
    any_fn=any,
    next_fn=next,
):
    builtin_dict = dict_type
    builtin_type = type_type
    builtin_bool = bool_type
    builtin_int = int_type
    builtin_tuple = tuple_type
    builtin_str = str_type
    builtin_list = list_type
    builtin_set = set_type
    builtin_frozenset = frozenset_type
    builtin_len = len_fn
    builtin_any = any_fn
    builtin_next = next_fn
    literal_contract = builtin_tuple(contract_seed)
    literal_contract_keys = builtin_frozenset(key for key, _ in literal_contract)
    literal_registry = builtin_tuple(registry_seed)
    literal_registry_digest = registry_digest_seed
    literal_sources = builtin_tuple(source_seed)
    literal_dependencies = builtin_tuple(dependency_seed)
    literal_fixtures = builtin_tuple(fixture_seed)
    literal_root = root_seed
    literal_maximum = builtin_next(
        value for key, value in literal_contract if key == "maximum_claim"
    )
    literal_route = builtin_next(
        value for key, value in literal_contract if key == "route_advance"
    )

    def canonical_json(value: object) -> bytes:
        return serializer(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def sha256(value: bytes) -> str:
        return hash_constructor(value).hexdigest()

    def exact_type(value: object, expected: object) -> bool:
        return builtin_type(value) is builtin_type(expected)

    def key_impostor(items: tuple[tuple[str, object], ...], target: str) -> dict[object, object]:
        class KeyImpostor:
            def __hash__(self) -> int:
                return hash(target)

            def __eq__(self, other: object) -> bool:
                return other == target

        output = builtin_dict()
        output[KeyImpostor()] = builtin_next(
            value for key, value in items if key == target
        )
        output.update((key, value) for key, value in items if key != target)
        return output

    def validate_contract(candidate: object) -> None:
        if (
            builtin_type(candidate) is not builtin_dict
            or builtin_any(builtin_type(key) is not builtin_str for key in candidate)
            or builtin_set(candidate) != literal_contract_keys
        ):
            raise failure_type("contract schema changed")
        for key, expected in literal_contract:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"contract field {key} changed")

    def registry_digest(candidate: tuple[tuple[str, str], ...]) -> str:
        return sha256(canonical_json(builtin_list(candidate)))

    def validate_registry(candidate: object, claimed_digest: object) -> None:
        if builtin_type(candidate) is not builtin_tuple:
            raise failure_type("registry outer type changed")
        if builtin_any(
            builtin_type(row) is not builtin_tuple or builtin_len(row) != 2
            for row in candidate
        ):
            raise failure_type("registry row shape changed")
        if builtin_any(
            builtin_type(key) is not builtin_str or builtin_type(value) is not builtin_str
            for key, value in candidate
        ):
            raise failure_type("registry row type changed")
        if builtin_len({key for key, _ in candidate}) != builtin_len(candidate):
            raise failure_type("registry keys not unique")
        if candidate != literal_registry:
            raise failure_type("registry semantic promotion")
        if (
            builtin_type(claimed_digest) is not builtin_str
            or claimed_digest != literal_registry_digest
        ):
            raise failure_type("registry literal digest changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry content digest changed")

    def validate_sources(candidate: object) -> None:
        if builtin_type(candidate) is not builtin_tuple or candidate != literal_sources:
            raise failure_type("source locks changed")
        if builtin_any(
            builtin_type(row) is not builtin_tuple or builtin_len(row) != 2
            for row in candidate
        ):
            raise failure_type("source row shape changed")
        if builtin_any(
            builtin_type(key) is not builtin_str or builtin_type(value) is not builtin_str
            for key, value in candidate
        ):
            raise failure_type("source row type changed")

    def validate_dependencies(candidate: object) -> None:
        if builtin_type(candidate) is not builtin_tuple or candidate != literal_dependencies:
            raise failure_type("dependency locks changed")
        if builtin_any(
            builtin_type(row) is not builtin_tuple or builtin_len(row) != 2
            for row in candidate
        ):
            raise failure_type("dependency row shape changed")
        if builtin_any(
            builtin_type(path) is not builtin_str
            or builtin_type(digest) is not builtin_str
            for path, digest in candidate
        ):
            raise failure_type("dependency row type changed")
        for relative, expected in literal_dependencies:
            path = literal_root / relative
            if not path.is_file():
                raise failure_type(f"dependency missing: {relative}")
            actual = sha256(path.read_bytes().replace(b"\r\n", b"\n"))
            if actual != expected:
                raise failure_type(f"dependency hash changed: {relative}")

    def must_reject(label: str, action) -> None:
        try:
            action()
        except failure_type:
            return
        raise failure_type(f"mutation escaped: {label}")

    def wrong_value(expected: object) -> object:
        if builtin_type(expected) is builtin_bool:
            return not expected
        if builtin_type(expected) is builtin_int:
            return expected + 1
        if builtin_type(expected) is builtin_tuple:
            return expected + ("MUTATED",)
        return builtin_str(expected) + "__MUTATED"

    def contract_mutations() -> int:
        count = 0
        for key, expected in literal_contract:
            missing = builtin_dict(literal_contract)
            del missing[key]
            must_reject(f"contract_missing_{key}", lambda c=missing: validate_contract(c))
            count += 1
            wrong_t = builtin_dict(literal_contract)
            wrong_t[key] = (
                builtin_str(expected)
                if builtin_type(expected) is not builtin_str
                else 0
            )
            must_reject(f"contract_type_{key}", lambda c=wrong_t: validate_contract(c))
            count += 1
            wrong_v = builtin_dict(literal_contract)
            wrong_v[key] = wrong_value(expected)
            must_reject(f"contract_value_{key}", lambda c=wrong_v: validate_contract(c))
            count += 1
        extra = builtin_dict(literal_contract)
        extra["UNDECLARED"] = "PROMOTION"
        must_reject("contract_extra", lambda: validate_contract(extra))
        must_reject(
            "contract_key_impostor",
            lambda: validate_contract(key_impostor(literal_contract, "maximum_claim")),
        )
        return count + 2

    def registry_mutations() -> int:
        count = 0
        for index, (key, value) in enumerate(literal_registry):
            rows = builtin_list(literal_registry)
            rows[index] = (key, value + "__PROMOTED")
            candidate = builtin_tuple(rows)
            must_reject(
                f"registry_value_{index+1}",
                lambda c=candidate, d=registry_digest(candidate): validate_registry(c, d),
            )
            count += 1
            rows = builtin_list(literal_registry)
            rows[index] = (key + "__REPLACED", value)
            candidate = builtin_tuple(rows)
            must_reject(
                f"registry_key_{index+1}",
                lambda c=candidate, d=registry_digest(candidate): validate_registry(c, d),
            )
            count += 1
        must_reject(
            "registry_wrong_outer_type",
            lambda: validate_registry(
                builtin_list(literal_registry), literal_registry_digest
            ),
        )
        must_reject(
            "registry_false_digest",
            lambda: validate_registry(literal_registry, "0" * 64),
        )
        class TextSubclass(str):
            pass
        rows = builtin_list(literal_registry)
        rows[0] = (TextSubclass(rows[0][0]), rows[0][1])
        must_reject(
            "registry_string_subclass",
            lambda: validate_registry(builtin_tuple(rows), literal_registry_digest),
        )
        return count + 3

    def source_mutations() -> int:
        count = 0
        for index, (key, value) in enumerate(literal_sources):
            rows = builtin_list(literal_sources)
            rows[index] = (key, value + "__PROMOTED")
            must_reject(
                f"source_value_{index+1}",
                lambda c=builtin_tuple(rows): validate_sources(c),
            )
            count += 1
            rows = builtin_list(literal_sources)
            rows[index] = (key + "__REPLACED", value)
            must_reject(
                f"source_key_{index+1}",
                lambda c=builtin_tuple(rows): validate_sources(c),
            )
            count += 1
        must_reject(
            "source_wrong_outer_type",
            lambda: validate_sources(builtin_list(literal_sources)),
        )
        must_reject("source_missing", lambda: validate_sources(literal_sources[:-1]))
        return count + 2

    def dependency_mutations() -> int:
        count = 0
        for index, (path, digest) in enumerate(literal_dependencies):
            rows = builtin_list(literal_dependencies)
            rows[index] = (path + ".wrong", digest)
            must_reject(
                f"dependency_path_{index+1}",
                lambda c=builtin_tuple(rows): validate_dependencies(c),
            )
            count += 1
            rows = builtin_list(literal_dependencies)
            rows[index] = (path, "0" * 64)
            must_reject(
                f"dependency_hash_{index+1}",
                lambda c=builtin_tuple(rows): validate_dependencies(c),
            )
            count += 1
        must_reject(
            "dependency_wrong_outer_type",
            lambda: validate_dependencies(builtin_list(literal_dependencies)),
        )
        rows = builtin_list(literal_dependencies)
        rows[0] = builtin_list(rows[0])
        must_reject(
            "dependency_wrong_row",
            lambda: validate_dependencies(builtin_tuple(rows)),
        )
        class TextSubclass(str):
            pass
        rows = builtin_list(literal_dependencies)
        rows[0] = (TextSubclass(rows[0][0]), rows[0][1])
        must_reject(
            "dependency_string_subclass",
            lambda: validate_dependencies(builtin_tuple(rows)),
        )
        return count + 3

    base_result_items = literal_fixtures + (
        ("check", True),
        ("maximum_claim", literal_maximum),
        ("route_advance", literal_route),
        ("contract_fields", builtin_len(literal_contract)),
        ("registry_rows", builtin_len(literal_registry)),
        ("registry_sha256", literal_registry_digest),
        ("source_locks", builtin_len(literal_sources)),
        ("dependency_locks", builtin_len(literal_dependencies)),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
    )
    base_keys = builtin_frozenset(key for key, _ in base_result_items)

    def validate_result(candidate: object) -> None:
        if (
            builtin_type(candidate) is not builtin_dict
            or builtin_any(builtin_type(key) is not builtin_str for key in candidate)
            or builtin_set(candidate) != base_keys
        ):
            raise failure_type("result schema changed")
        for key, expected in base_result_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"result field {key} changed")

    def result_mutations() -> int:
        count = 0
        for key, expected in base_result_items:
            missing = builtin_dict(base_result_items)
            del missing[key]
            must_reject(f"result_missing_{key}", lambda c=missing: validate_result(c))
            count += 1
            wrong_t = builtin_dict(base_result_items)
            wrong_t[key] = (
                builtin_str(expected)
                if builtin_type(expected) is not builtin_str
                else 0
            )
            must_reject(f"result_type_{key}", lambda c=wrong_t: validate_result(c))
            count += 1
            wrong_v = builtin_dict(base_result_items)
            wrong_v[key] = wrong_value(expected)
            must_reject(f"result_value_{key}", lambda c=wrong_v: validate_result(c))
            count += 1
        extra = builtin_dict(base_result_items)
        extra["UNDECLARED"] = "PROMOTION"
        must_reject("result_extra", lambda: validate_result(extra))
        must_reject(
            "result_key_impostor",
            lambda: validate_result(key_impostor(base_result_items, "arithmetic_advance")),
        )
        return count + 2

    expected_count_items = (
        ("contract_mutations", 3 * builtin_len(literal_contract) + 2),
        ("registry_mutations", 2 * builtin_len(literal_registry) + 3),
        ("source_mutations", 2 * builtin_len(literal_sources) + 2),
        ("dependency_mutations", 2 * builtin_len(literal_dependencies) + 3),
        ("result_mutations", 3 * builtin_len(base_result_items) + 2),
    )
    full_result_items = base_result_items + expected_count_items
    full_keys = builtin_frozenset(key for key, _ in full_result_items)

    def validate_full_result(candidate: object) -> None:
        if (
            builtin_type(candidate) is not builtin_dict
            or builtin_any(builtin_type(key) is not builtin_str for key in candidate)
            or builtin_set(candidate) != full_keys
        ):
            raise failure_type("full result schema changed")
        for key, expected in full_result_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"full result field {key} changed")

    def trusted_run() -> dict[str, object]:
        validate_contract(builtin_dict(literal_contract))
        validate_registry(builtin_tuple(literal_registry), literal_registry_digest)
        validate_sources(builtin_tuple(literal_sources))
        validate_dependencies(builtin_tuple(literal_dependencies))
        result = builtin_dict(base_result_items)
        validate_result(result)
        result["contract_mutations"] = contract_mutations()
        result["registry_mutations"] = registry_mutations()
        result["source_mutations"] = source_mutations()
        result["dependency_mutations"] = dependency_mutations()
        result["result_mutations"] = result_mutations()
        if (
            builtin_tuple((key, result[key]) for key, _ in full_result_items)
            != full_result_items
        ):
            raise failure_type("mutation execution counts changed")
        validate_full_result(result)
        final_result = builtin_dict(result)
        if builtin_type(final_result) is not builtin_dict:
            raise failure_type("final result constructor changed")
        validate_full_result(final_result)
        return final_result

    return trusted_run


_TRUSTED_RUN = _make_trusted_runner()


def _seal_runner(runner):
    def sealed() -> dict[str, object]:
        return runner()

    return sealed


run_check = _seal_runner(_TRUSTED_RUN)
del _seal_runner


def _seal_main(
    runner,
    expected_text,
    failure_type=CheckFailure,
    tuple_type=tuple,
    len_fn=len,
    print_fn=print,
):
    def sealed(*argv_objects: object) -> int:
        if len_fn(argv_objects) != 1:
            raise failure_type("explicit --check is required")
        args = tuple_type(argv_objects[0])
        if args != ("--check",):
            raise failure_type("explicit --check is required")
        runner()
        print_fn(expected_text)
        return 0

    return sealed


_EXPECTED_STDOUT = json.dumps(
    _TRUSTED_RUN(),
    ensure_ascii=False,
    sort_keys=True,
)
main = _seal_main(_TRUSTED_RUN, _EXPECTED_STDOUT)
del _EXPECTED_STDOUT
del _seal_main


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        print(f"CheckFailure: {exc}", file=sys.stderr)
        raise SystemExit(1)
