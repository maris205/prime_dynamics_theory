#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V29 big-road audit."""

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
    "EXACT_LOCAL_CARRIER_BETTIN_CHANDEE_COMPILER_PLUS_ZERO_AXIS_TWO_GATE_"
    "FIREWALL_PLUS_LOW_CHRISTOFFEL_RIESZ_CRITERION"
)


CONTRACT = {
    "maximum_claim": MAXIMUM_CLAIM,
    "route_advance": "YES",
    "fixed_h0": 2,
    "physical_scale": "x=2X",
    "prime_shell_Q_exponent": "1/3",
    "difference_horizon_exponent": "21/32",
    "master_group_lower_exponent": "133/400",
    "zero_axis_identity": "S=J(e)+E(e)",
    "zero_axis_dirac": "e=T*delta_0_IMPLIES_E=0_AND_J=T",
    "independent_major_gate": "OPEN_NEW_THEOREM",
    "offzero_weighted_L2_gate": "OPEN_NEW_THEOREM",
    "two_gate_closure": "OPEN_MAJOR_AND_MINOR_THEOREM",
    "major_target": "abs(J(e))<<x^(399/400-eta_M)",
    "minor_theta_ceiling": "13/4800",
    "minor_output_exponent": "191/192+theta+epsilon_N",
    "common_epsilon": "epsilon<min(eta_M,(13/4800-theta)/2)",
    "MRT_source": "arXiv:1707.01315v3_Proposition_3.1",
    "MRT_product_condition": "P0*PY<<x^(2+2theta+2epsilon)/Y",
    "actual_major_attachment": "M_T=Mloc+a_WITH_WEIGHTED_L2_A",
    "boundary_exponent": "47/48+epsilon",
    "boundary_epsilon_ceiling": "11/1920",
    "active_reduced_radical_exponent": "31/96",
    "dual_length_upper_exponent": "17/96",
    "q_divides_g": "EMPTY_BY_g_LT_q",
    "F_phase": "mu(R)/phi(R)*e_R(+2*a*q_inverse)",
    "G_phase": "mu(R0)/(phi(R0)*phi(R1)^2)*e_R0(+2*a*(qR1)_inverse)",
    "F_coprimality_cost": "d^-2",
    "G_coprimality_cost": "d0^-2*d1^-3",
    "exact_R1_triangle": "L_FACTOR_PAID",
    "BC_source": "arXiv:1502.00769v1_Theorem_1",
    "BC_local_exponent": "1891/1920",
    "BC_margin_to_endpoint": "121/9600",
    "local_AP_main": "OPEN_ATTACHMENT",
    "riesz_kernel": "MINIMUM_NORM_EXACT",
    "christoffel_threshold": "kappa0=o(x/log^4x)",
    "cyclic_spectral_kappa": "frequency_dimension",
    "whole_shell_low_christoffel": "OPEN_NEW_THEOREM",
    "positive_kernel_main": "OPEN_INDEPENDENT_ATTACHMENT",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
    "numbered_release": "NO",
}


REGISTRY_ITEMS = (
    ("V29_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V29_ROUTE_ADVANCE", "YES"),
    ("V29_ARITHMETIC_ADVANCE", "NO"),
    ("V29_FIXED_ATOM_CREDIT", "0"),
    ("V29_STRICT_1_OVER_400", "UNPAID"),
    ("V29_L2", "NONE"),
    ("V29_TPC_207_TRIGGER", "false"),
    ("V29_NUMBERED_RELEASE", "NO"),
    (
        "V29_ZERO_AXIS_RESIDUAL_IDENTITY",
        "PROVED_EXACT_FROM_V28_TAGGED_DEFINITION",
    ),
    (
        "V29_ZERO_AXIS_DIRAC_FIREWALL",
        "PROVED_EXACT_FINITE_E_ZERO_J_FULL_EXAMPLE",
    ),
    (
        "V29_OFFZERO_RESIDUAL_ENERGY_ALONE",
        "STOP_SCOPED_DELTA_ZERO_SELF_RETURN",
    ),
    (
        "V29_TAGGED_RESIDUAL_INDEPENDENT_JUTILA_MAJOR",
        "SELECTED_PRIMARY_OPEN_NEW_THEOREM",
    ),
    (
        "V29_TAGGED_RESIDUAL_OFFZERO_WEIGHTED_L2",
        "OPEN_NEW_THEOREM",
    ),
    (
        "V29_TAGGED_RESIDUAL_TWO_GATE_CLOSURE",
        "OPEN_MAJOR_AND_MINOR_THEOREM",
    ),
    (
        "V29_MRT_ABSTRACT_PRODUCT_LOCAL_L2",
        "SOURCE_BACKED_REDUCTION_ONLY",
    ),
    (
        "V29_WEAKEST_PRODUCT_LOCAL_CONDITION",
        "PRODUCT_P0_TIMES_PY_WITH_HARD_MAJOR_ATTACHMENT",
    ),
    (
        "V29_ACTUAL_MAJOR_COEFFICIENT_MLOC_PLUS_A",
        "OPEN_WEIGHTED_AP_ATTACHMENT",
    ),
    (
        "V29_DIRECT_PRIMARY_SOURCE_ATTACHMENT",
        "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08",
    ),
    (
        "V29_MASTER_INTERIOR_BOUNDARY_EXACT_COVER",
        "PROVED_WITH_X_47_OVER_48_PLUS_EPSILON",
    ),
    (
        "V29_Q_DIVIDES_D_PRE_ABSOLUTE_CANCELLATION",
        "PROVED_EXACT_FULL_LATTICE_BULK",
    ),
    (
        "V29_Q_DIVIDES_G_CORRECTION",
        "PROVED_EMPTY_BY_G_LT_Q",
    ),
    (
        "V29_F_G_SIGNED_REDUCED_RADICAL_EMITTER",
        "PROVED_EXACT",
    ),
    (
        "V29_R1_EQUAL_ONE_PRE_ABSOLUTE_CANCELLATION",
        "PROVED_EXACT",
    ),
    (
        "V29_F_COPRIMALITY_MOBIUS_COMPILER",
        "PROVED_D_MINUS_2_SUMMABLE",
    ),
    (
        "V29_G_COPRIMALITY_MOBIUS_COMPILER",
        "PROVED_D0_MINUS_2_D1_MINUS_3_SUMMABLE",
    ),
    (
        "V29_EXACT_R1_LOCAL_TRIANGLE",
        "PROVED_L_FACTOR_PAID_IN_EXPONENT_LEDGER",
    ),
    (
        "V29_SMOOTH_DYADIC_SEPARATION",
        "PROVED_EXACT_LOG_FOURIER_X_O1",
    ),
    (
        "V29_LOCAL_CARRIER_BC_BOUND",
        "PROVED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1",
    ),
    ("V29_LOCAL_CARRIER_BC_EXPONENT", "1891/1920"),
    (
        "V29_LOCAL_CARRIER_BC_MARGIN_TO_399_400",
        "121/9600",
    ),
    (
        "V29_LOCAL_EULER_TENSOR_AS_ACTUAL_AP_MAIN",
        "OPEN_ATTACHMENT",
    ),
    (
        "V29_PREDECLARED_SUBSPACE_MINIMUM_RIESZ_KERNEL",
        "PROVED_EXACT_FINITE_HILBERT",
    ),
    (
        "V29_EVALUATION_FACTORIZATION_GATE",
        "PROVED_EXACT_KER_Q_SUBSET_KER_L_IFF",
    ),
    (
        "V29_VARIANCE_O_X_CHRISTOFFEL_THRESHOLD",
        "PROVED_EXACT_KAPPA0_O_X_OVER_LOG4",
    ),
    (
        "V29_FINITE_CYCLIC_SPECTRAL_KERNEL",
        "PROVED_EXACT_KAPPA_EQUALS_FREQUENCY_DIMENSION",
    ),
    (
        "V29_NONCONSTANT_LOW_NORM_KERNEL_CHANNEL",
        "PROVED_NONEMPTY_EXACT_FINITE_MODEL",
    ),
    (
        "V29_COARSE_CELL_AS_POINT_EVALUATION",
        "STOP_SCOPED_EXACT_FOUR_POINT_COUNTEREXAMPLE",
    ),
    (
        "V29_SPARSE_MARTINGALE_LEVEL_COUNT",
        "STOP_SCOPED_ORTHOGONAL_ENERGY_REASSEMBLES_SINGLETON_NORM",
    ),
    (
        "V29_TARGET_CALIBRATED_SINGLE_BLOCK_KERNEL",
        "STOP_SCOPED_EXACT_CIRCULAR_ONE_VECTOR_FIT",
    ),
    (
        "V29_STAGE_TAG_SKEW_PRODUCT_NORM_GAIN",
        "STOP_SCOPED_EXACT_KAPPA_DIVIDED_BY_FIBER_MASS",
    ),
    (
        "V29_ACTUAL_WHOLE_SHELL_LOW_CHRISTOFFEL_QUOTIENT",
        "SELECTED_DYNAMICS_OPEN_NEW_THEOREM",
    ),
    (
        "V29_INDEPENDENT_POSITIVE_KERNEL_MAIN",
        "OPEN_ATTACHMENT_NOT_SAME_OUTPUT_MEAN",
    ),
)


EXPECTED_REGISTRY_SHA256 = "39b3aaf04f28763bca249ef874f07ade304e71d3e4eb390613fa1870455826a6"


SOURCE_ITEMS = (
    ("BETTIN_CHANDEE", "arXiv:1502.00769v1_Theorem_1"),
    ("MRT_PRODUCT_L2", "arXiv:1707.01315v3_Proposition_3.1"),
    ("ABP_CRITICAL_SEED", "arXiv:2212.12202v2_Theorem_1.1"),
    ("HNTV_SEQUENTIAL", "arXiv:1406.4266_Theorem_3.1"),
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
    (
        "research/tpc-big-road/tpc_bridge_b_euler_kernel_checker.py",
        "dddff8b09472fe9fc563caa3f6c204c24895aa45613781efba0877ae3fc421a7",
    ),
)


def _mu_squarefree(value: int) -> int:
    count = 0
    remaining = value
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            count += 1
            remaining //= candidate
            if remaining % candidate == 0:
                return 0
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        count += 1
    return -1 if count % 2 else 1


def _mean(values: tuple[Fraction, ...]) -> Fraction:
    return sum(values, Fraction(0)) / len(values)


def _inner(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return _mean(tuple(a * b for a, b in zip(left, right)))


def _finite_fixtures() -> dict[str, object]:
    # The zero coordinate cannot be recovered from off-zero energy.
    kernel = {-1: Fraction(1, 3), 0: Fraction(1), 1: Fraction(-1, 4)}
    delta = {-1: Fraction(0), 0: Fraction(7), 1: Fraction(0)}
    j_delta = sum(kernel[h] * delta[h] for h in kernel)
    e_delta = delta[0] - j_delta
    if (j_delta, e_delta, j_delta + e_delta) != (7, 0, 7):
        raise CheckFailure("zero-axis Dirac firewall changed")

    active = Fraction(21, 32) - Fraction(1, 3)
    dual = Fraction(1, 3) + Fraction(1, 2) - Fraction(21, 32)
    primitive = Fraction(1, 3) + Fraction(133, 400) - Fraction(21, 32)
    coefficient = (
        Fraction(1, 2) * (Fraction(21, 32) + Fraction(2, 3))
        - Fraction(2, 3)
    )
    minor_margin = Fraction(399, 400) - Fraction(191, 192)
    one_sided = Fraction(21, 128) - minor_margin
    bc = Fraction(1891, 1920)
    bc_margin = Fraction(399, 400) - bc
    boundary = 2 * Fraction(21, 32) - Fraction(1, 3)
    boundary_epsilon = bc - boundary
    degenerate = Fraction(65, 96)
    g_gap = Fraction(1, 3) - dual
    if (
        active != Fraction(31, 96)
        or dual != Fraction(17, 96)
        or primitive != Fraction(23, 2400)
        or coefficient != Fraction(-1, 192)
        or minor_margin != Fraction(13, 4800)
        or one_sided != Fraction(1549, 9600)
        or bc_margin != Fraction(121, 9600)
        or boundary != Fraction(47, 48)
        or boundary_epsilon != Fraction(11, 1920)
        or degenerate != Fraction(65, 96)
        or g_gap != Fraction(5, 32)
    ):
        raise CheckFailure("V29 exponent ledger changed")

    # Decisive reduced-radical CRT sign and removal of the zero-mode gcd.
    D, q, n = 30, 11, 2
    q_inverse_D = pow(q, -1, D)
    residue = n * q_inverse_D % D
    g = math.gcd(n, D)
    R = D // g
    a = n // g
    phase = 2 * a * pow(q, -1, R) % R
    wrong_g_phase = 2 * g * a * pow(q, -1, R) % R
    local_indices = tuple(
        (p, residue * pow(D // p, -1, p) % p) for p in (2, 3, 5)
    )
    if (
        q_inverse_D,
        residue,
        g,
        R,
        a,
        phase,
        wrong_g_phase,
        local_indices,
    ) != (11, 22, 2, 15, 1, 7, 14, ((2, 0), (3, 1), (5, 2))):
        raise CheckFailure("reduced-radical CRT fixture changed")

    cutoff = 3
    R0 = math.prod(p for p in (3, 5) if p <= cutoff)
    R1 = math.prod(p for p in (3, 5) if p > cutoff)
    f_amplitude = Fraction(_mu_squarefree(R), 8)
    g_amplitude = Fraction(_mu_squarefree(R0), 2 * 4 * 4)
    g_phase = 2 * a * pow(q * R1, -1, R0) % R0
    if (R0, R1, f_amplitude, g_amplitude, g_phase) != (
        3,
        5,
        Fraction(1, 8),
        Fraction(-1, 32),
        2,
    ):
        raise CheckFailure("F/G reduced-radical split changed")
    if tuple(_mu_squarefree(1) for _ in range(2)) != (1, 1):
        raise CheckFailure("R1=1 cancellation seed changed")

    # Exact Mobius coprimality compiler.
    coprime_rows = []
    for value in range(1, 7):
        gcd_value = math.gcd(value, 6)
        mobius_sum = sum(
            _mu_squarefree(d) for d in range(1, gcd_value + 1) if gcd_value % d == 0
        )
        coprime_rows.append(mobius_sum)
    if tuple(coprime_rows) != (1, 0, 0, 0, 1, 0):
        raise CheckFailure("Mobius coprimality compiler changed")

    # q|D cancellation exists only after the complete residue sum.
    local_delta = (
        Fraction(0),
        Fraction(5, 16),
        Fraction(5, 16),
        Fraction(-15, 16),
        Fraction(5, 16),
    )
    ramanujan = (4, -1, -1, -1, -1)
    signed_pair = sum(a0 * b0 for a0, b0 in zip(local_delta, ramanujan))
    absolute_pair = sum(abs(a0 * b0) for a0, b0 in zip(local_delta, ramanujan))
    if signed_pair != 0 or absolute_pair != Fraction(30, 16):
        raise CheckFailure("pre-absolute q-divides-D cancellation changed")

    # Unique half-open dyadic ownership.
    boundaries = (1, 2, 4, 8, 16)
    ids = tuple(
        next(index for index in range(4) if boundaries[index] <= value < boundaries[index + 1])
        for value in (1, 2, 3, 4, 7, 8, 15)
    )
    if ids != (0, 1, 1, 2, 2, 3, 3):
        raise CheckFailure("half-open dyadic ownership changed")

    # Minimum Riesz kernel and a nonconstant low-complexity survivor.
    K = tuple(Fraction(v) for v in (3, 1, -1, 1))
    S = tuple(Fraction(v) for v in (4, 2, 0, 2))
    mean_K = _mean(K)
    kappa = _inner(K, K)
    pairing = _inner(K, S)
    kappa0 = _inner(tuple(v - 1 for v in K), tuple(v - 1 for v in K))
    if (mean_K, kappa, kappa0, pairing, S[0]) != (1, 3, 2, 4, 4):
        raise CheckFailure("finite spectral Riesz survivor changed")

    coarse_K = tuple(Fraction(v) for v in (2, 2, 0, 0))
    coarse_S = tuple(Fraction(v) for v in (2, 0, 0, 0))
    if (_mean(coarse_K), _inner(coarse_K, coarse_S), coarse_S[0]) != (1, 1, 2):
        raise CheckFailure("coarse-cell point-evaluation falsifier changed")

    martingale = (
        (1, 1, 1, 1, 1, 1, 1, 1),
        (2, 2, 2, 2, 0, 0, 0, 0),
        (4, 4, 0, 0, 0, 0, 0, 0),
        (8, 0, 0, 0, 0, 0, 0, 0),
    )
    martingale_q = tuple(tuple(Fraction(v) for v in row) for row in martingale)
    kernel_energies = tuple(_inner(row, row) for row in martingale_q)
    increment_energies = tuple(
        _inner(
            tuple(right[i] - left[i] for i in range(8)),
            tuple(right[i] - left[i] for i in range(8)),
        )
        for left, right in zip(martingale_q[:-1], martingale_q[1:])
    )
    if kernel_energies != (1, 2, 4, 8) or increment_energies != (1, 2, 4):
        raise CheckFailure("martingale singleton energy changed")

    fit_S = (Fraction(0), Fraction(2))
    fit_K = (Fraction(-1), Fraction(3))
    if (_mean(fit_K), _inner(fit_K, fit_S), _inner(fit_K, fit_K)) != (1, 3, 5):
        raise CheckFailure("target-calibrated one-vector fit changed")

    fiber_weight = Fraction(1, 4)
    if kappa / fiber_weight != 12:
        raise CheckFailure("skew-product norm scaling changed")

    return {
        "zero_axis_J": str(j_delta),
        "zero_axis_E": str(e_delta),
        "active_radical_exponent": str(active),
        "dual_upper_exponent": str(dual),
        "primitive_dual_exponent": str(primitive),
        "coefficient_ratio_exponent": str(coefficient),
        "minor_margin": str(minor_margin),
        "one_sided_deficit": str(one_sided),
        "BC_corridor_exponent": str(bc),
        "BC_margin": str(bc_margin),
        "boundary_exponent": str(boundary),
        "boundary_epsilon_ceiling": str(boundary_epsilon),
        "g_less_q_exponent_gap": str(g_gap),
        "crt_local_indices": local_indices,
        "crt_correct_phase_mod_15": phase,
        "crt_wrong_g_phase_mod_15": wrong_g_phase,
        "FG_split_R0_R1": (R0, R1),
        "F_amplitude": str(f_amplitude),
        "G_amplitude": str(g_amplitude),
        "G_phase_mod_R0": g_phase,
        "coprimality_rows_mod_6": tuple(coprime_rows),
        "q_divides_D_signed_pair": str(signed_pair),
        "q_divides_D_absolute_pair": str(absolute_pair),
        "dyadic_ids": ids,
        "spectral_kernel_mean": str(mean_K),
        "spectral_kappa": str(kappa),
        "spectral_kappa0": str(kappa0),
        "spectral_pairing": str(pairing),
        "coarse_pairing": "1_not_2",
        "martingale_kernel_energies": tuple(str(v) for v in kernel_energies),
        "martingale_increment_energies": tuple(str(v) for v in increment_energies),
        "one_vector_fit_norm2": "5",
        "skew_kappa_at_weight_1_4": "12",
        "christoffel_threshold": "kappa0=o(x/log^4x)",
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
    enumerate_fn=enumerate,
    hash_fn=hash,
    is_file_fn=Path.is_file,
    read_bytes_fn=Path.read_bytes,
    joinpath_fn=Path.joinpath,
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
    builtin_enumerate = enumerate_fn
    builtin_hash = hash_fn
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

    def registry_bytes(candidate: tuple[tuple[str, str], ...]) -> bytes:
        pieces = []
        for key, value in candidate:
            key_bytes = key.encode("utf-8")
            value_bytes = value.encode("utf-8")
            pieces.append(
                builtin_str(builtin_len(key_bytes)).encode("ascii")
                + b":"
                + key_bytes
                + builtin_str(builtin_len(value_bytes)).encode("ascii")
                + b":"
                + value_bytes
                + b"\n"
            )
        return b"".join(pieces)

    def sha256(value: bytes) -> str:
        return hash_constructor(value).hexdigest()

    def exact_type(value: object, expected: object) -> bool:
        return builtin_type(value) is builtin_type(expected)

    def key_impostor(items: tuple[tuple[str, object], ...], target: str):
        class KeyImpostor:
            def __hash__(self) -> int:
                return builtin_hash(target)

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
                raise failure_type("contract field changed: " + key)

    def registry_digest(candidate: tuple[tuple[str, str], ...]) -> str:
        return sha256(registry_bytes(candidate))

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
        if builtin_len(builtin_set(key for key, _ in candidate)) != builtin_len(candidate):
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
            path = joinpath_fn(literal_root, relative)
            if not is_file_fn(path):
                raise failure_type("dependency missing: " + relative)
            actual = sha256(read_bytes_fn(path).replace(b"\r\n", b"\n"))
            if actual != expected:
                raise failure_type("dependency hash changed: " + relative)

    def must_reject(label: str, action) -> None:
        try:
            action()
        except failure_type:
            return
        raise failure_type("mutation escaped: " + label)

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
            must_reject("contract_missing_" + key, lambda c=missing: validate_contract(c))
            count += 1
            wrong_t = builtin_dict(literal_contract)
            wrong_t[key] = builtin_str(expected) if builtin_type(expected) is not builtin_str else 0
            must_reject("contract_type_" + key, lambda c=wrong_t: validate_contract(c))
            count += 1
            wrong_v = builtin_dict(literal_contract)
            wrong_v[key] = wrong_value(expected)
            must_reject("contract_value_" + key, lambda c=wrong_v: validate_contract(c))
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
        for index, (key, value) in builtin_enumerate(literal_registry):
            rows = builtin_list(literal_registry)
            rows[index] = (key, value + "__PROMOTED")
            candidate = builtin_tuple(rows)
            must_reject(
                "registry_value_" + builtin_str(index + 1),
                lambda c=candidate, d=registry_digest(candidate): validate_registry(c, d),
            )
            count += 1
            rows = builtin_list(literal_registry)
            rows[index] = (key + "__REPLACED", value)
            candidate = builtin_tuple(rows)
            must_reject(
                "registry_key_" + builtin_str(index + 1),
                lambda c=candidate, d=registry_digest(candidate): validate_registry(c, d),
            )
            count += 1
        must_reject(
            "registry_wrong_outer_type",
            lambda: validate_registry(builtin_list(literal_registry), literal_registry_digest),
        )
        must_reject(
            "registry_false_digest",
            lambda: validate_registry(literal_registry, "0" * 64),
        )
        class TextSubclass(builtin_str):
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
        for index, (key, value) in builtin_enumerate(literal_sources):
            rows = builtin_list(literal_sources)
            rows[index] = (key, value + "__PROMOTED")
            must_reject(
                "source_value_" + builtin_str(index + 1),
                lambda c=builtin_tuple(rows): validate_sources(c),
            )
            count += 1
            rows = builtin_list(literal_sources)
            rows[index] = (key + "__REPLACED", value)
            must_reject(
                "source_key_" + builtin_str(index + 1),
                lambda c=builtin_tuple(rows): validate_sources(c),
            )
            count += 1
        must_reject("source_wrong_outer_type", lambda: validate_sources(builtin_list(literal_sources)))
        must_reject("source_missing", lambda: validate_sources(literal_sources[:-1]))
        return count + 2

    def dependency_mutations() -> int:
        count = 0
        for index, (path, digest) in builtin_enumerate(literal_dependencies):
            rows = builtin_list(literal_dependencies)
            rows[index] = (path + ".wrong", digest)
            must_reject(
                "dependency_path_" + builtin_str(index + 1),
                lambda c=builtin_tuple(rows): validate_dependencies(c),
            )
            count += 1
            rows = builtin_list(literal_dependencies)
            rows[index] = (path, "0" * 64)
            must_reject(
                "dependency_hash_" + builtin_str(index + 1),
                lambda c=builtin_tuple(rows): validate_dependencies(c),
            )
            count += 1
        must_reject(
            "dependency_wrong_outer_type",
            lambda: validate_dependencies(builtin_list(literal_dependencies)),
        )
        rows = builtin_list(literal_dependencies)
        rows[0] = builtin_list(rows[0])
        must_reject("dependency_wrong_row", lambda: validate_dependencies(builtin_tuple(rows)))
        class TextSubclass(builtin_str):
            pass
        rows = builtin_list(literal_dependencies)
        rows[0] = (TextSubclass(rows[0][0]), rows[0][1])
        must_reject(
            "dependency_string_subclass",
            lambda: validate_dependencies(builtin_tuple(rows)),
        )
        return count + 3

    base_result_items = literal_fixtures + (
        ("schema", "TPC_V29_CHECK_RESULT_V1"),
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
        ("numbered_release", "NO"),
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
                raise failure_type("result field changed: " + key)

    def result_mutations() -> int:
        count = 0
        for key, expected in base_result_items:
            missing = builtin_dict(base_result_items)
            del missing[key]
            must_reject("result_missing_" + key, lambda c=missing: validate_result(c))
            count += 1
            wrong_t = builtin_dict(base_result_items)
            wrong_t[key] = builtin_str(expected) if builtin_type(expected) is not builtin_str else 0
            must_reject("result_type_" + key, lambda c=wrong_t: validate_result(c))
            count += 1
            wrong_v = builtin_dict(base_result_items)
            wrong_v[key] = wrong_value(expected)
            must_reject("result_value_" + key, lambda c=wrong_v: validate_result(c))
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
                raise failure_type("full result field changed: " + key)

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
        if builtin_tuple((key, result[key]) for key, _ in full_result_items) != full_result_items:
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


_EXPECTED_STDOUT = json.dumps(_TRUSTED_RUN(), ensure_ascii=False, sort_keys=True)
main = _seal_main(_TRUSTED_RUN, _EXPECTED_STDOUT)
del _EXPECTED_STDOUT
del _seal_main


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        print("CheckFailure: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
