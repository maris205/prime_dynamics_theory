#!/usr/bin/env python3
"""Fail-closed finite checker for the V52 compensated pair-dilation compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised whenever the frozen V52 contract is not reproduced exactly."""


MAXIMUM_CLAIM = (
    "EXACT_COMPENSATED_PAIR_DILATION_AND_PACKET_ENDPOINT_COMPILER_IDENTIFIES_THE_"
    "FOLDED_GATE_A_AS_A_REVERSE_CHEN_PARITY_RESIDUAL_AND_PROVES_THE_MARGINAL_BDH_"
    "PLUS_CAUCHY_COMPILER_MISSES_BY_1_OVER_400"
)


REGISTRY = (
    "V52_MAXIMUM_CLAIM = EXACT_COMPENSATED_PAIR_DILATION_AND_PACKET_ENDPOINT_COMPILER_IDENTIFIES_THE_FOLDED_GATE_A_AS_A_REVERSE_CHEN_PARITY_RESIDUAL_AND_PROVES_THE_MARGINAL_BDH_PLUS_CAUCHY_COMPILER_MISSES_BY_1_OVER_400",
    "V52_ROUTE_ADVANCE = YES",
    "V52_CONDITIONAL_BRIDGE_ADVANCE = YES",
    "V52_ARITHMETIC_ADVANCE = NO",
    "V52_FIXED_ATOM_CREDIT = 0",
    "V52_STRICT_1_OVER_400 = UNPAID",
    "V52_L2 = NONE",
    "V52_TPC_207_TRIGGER = false",
    "V52_NUMBERED_RELEASE = NO",
    "V52_DERIVATION_STATUS = COHERENT_AFTER_DUAL_PAIR_SIEVE_IDENTITY_COMPENSATED_DILATION_HILBERT_PACKET_AND_ENDPOINT_SIMPLEX",
    "V52_ASSUMPTION_POLICY = PAIR_ANGULAR_DISPERSION_IS_CONJECTURAL__MARGINAL_AND_LOCAL_SOURCE_RESULTS_RECEIVE_NO_JOINT_CREDIT",
    "V52_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_PAIR_ANGULAR_GATE_A__V42_GATE_B__V43_JOIN__DYNAMICS_RESERVE",
    "V52_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO",
    "V52_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__DILATION_31_OVER_96",
    "V52_FOLDED_PAIR_INTERFACE = RETAINED_EXACT_MIXED_PLUS_BALANCED_OMEGA_U",
    "V52_TRUNCATED_SIEVE_INTERFACE = RETAINED_EXACT_LAMBDA_OVER_LOG_MINUS_MU_LE_U_CONVOLUTION",
    "V52_DUAL_COEFFICIENT_INTERFACE = PROVED_EXACT_SAME_BETA_AFTER_SQUARE_ROW_SUBTRACTION",
    "V52_PRIME_ROW_CANCELLATION = PROVED_EXACT_ONE_MINUS_ONE_EQUALS_ZERO",
    "V52_MIXED_SEMIPRIME_SLICE = PROVED_EXACT_ZERO_FOR_P_LE_U_LT_R",
    "V52_BALANCED_SEMIPRIME_SLICE = PROVED_EXACT_MINUS_ONE_FOR_U_LT_P_LT_R",
    "V52_SQUARE_PRIME_SLICE = PROVED_EXACT_MINUS_ONE_HALF",
    "V52_REVERSE_CHEN_INTERPRETATION = PROVED_EXACT_SUBCHANNEL_NOT_A_STANDALONE_ESTIMATE",
    "V52_MULTI_PAIR_T12_FIXTURE = PROVED_FORMAL_LOG_COLLAPSE_TO_ONE",
    "V52_COMPENSATED_PAIR_DILATION_ROW = PROVED_EXACT_DIVISIBILITY_MINUS_UNIT_PRINCIPAL_MEAN",
    "V52_COMPENSATED_PAIR_DILATION_SCALAR = PROVED_EXACT_ONE_COMMON_PRIME_SHELL_AND_ONE_SIGNED_AGGREGATE",
    "V52_DILATION_NATURAL_LENGTH = H_OVER_Q_EQUALS_X_31_OVER_96",
    "V52_DILATION_HARD_SUPPORT_POLICY = EXACT_T_PLUS_QK_IN_I_WITH_SCHWARTZ_NOT_COMPACT_K_TAIL",
    "V52_DILATION_SPLIT_ABSOLUTE_CEILING = X_191_OVER_96_PLUS_O1",
    "V52_DILATION_SPLIT_DEFICIT = 781_OVER_2400",
    "V52_Q5_DILATION_FIXTURE = PROVED_EXACT_20_MINUS_10_EQUALS_10",
    "V52_PAIR_CHARACTER_PACKET = RETAINED_EXACT_NONPRINCIPAL_CHARACTER_FOURIER_AGGREGATE",
    "V52_HILBERT_PACKET_IDENTITY = PROVED_EXACT_F_CIRCLE_EQUALS_INNER_PRODUCT_X_Y",
    "V52_PACKET_COHERENCE = DEFINED_EXACT_ZERO_TO_ONE_NO_ARITHMETIC_CREDIT",
    "V52_CHARACTER_DIAGONAL_FORMULA = PROVED_EXACT_Q_Q_MINUS_2_OVER_Q_MINUS_1_WEIGHT",
    "V52_DIAGONAL_SCALE = X_5_OVER_3_PLUS_O1_UPPER_BENCHMARK",
    "V52_DIAGONAL_SCALE_LOWER_BOUND = NOT_ASSERTED_OFFDIAGONAL_CAN_HAVE_EITHER_SIGN",
    "V52_MARGINAL_BDH_BASELINE = CONJECTURAL_E_B_AND_E_W_LE_X_5_OVER_3_PLUS_O1",
    "V52_MARGINAL_BDH_PLUS_CAUCHY = NO_GO_MISSES_TARGET_BY_EXACT_1_OVER_400",
    "V52_PACKET_ENDPOINT_LAW = PROVED_CONDITIONAL_KAPPA_PLUS_HALF_DELTA_SUM_MINUS_1_OVER_400",
    "V52_BASELINE_MARGINAL_ANGULAR_THRESHOLD = KAPPA_GT_1_OVER_400",
    "V52_ZERO_ANGLE_TOTAL_SUPER_BDH_THRESHOLD = DELTA_B_PLUS_DELTA_W_GT_1_OVER_200",
    "V52_ONE_SIDED_SUPER_BDH_THRESHOLD = DELTA_GT_1_OVER_200",
    "V52_ONE_GENERIC_ONE_BDH_DEFICIT = 203_OVER_1200",
    "V52_TWO_GENERIC_CHARACTER_DEFICIT = 403_OVER_1200",
    "V52_MARGINAL_NORMS_DETERMINE_ANGLE = NO_GO_PARALLEL_ORTHOGONAL_EQUAL_NORM_FIXTURE",
    "V52_PAIR_ANGULAR_DISPERSION_GATE = CONJECTURAL_H_PAD_DELTA_B_DELTA_W_KAPPA",
    "V52_PREFERRED_PAD_REGIME = DIAGONAL_SCALE_MARGINALS_AND_KAPPA_GT_1_OVER_400",
    "V52_SUPER_BDH_REGIME = RETAINED_LEGAL_ALTERNATIVE_IF_TOTAL_SAVING_GT_1_OVER_200",
    "V52_PAD_TO_V51_H_FOLD = PROVED_CONDITIONAL_WITH_ETA_PAD_POSITIVE",
    "V52_PAD_TO_PHYSICAL_ENDPOINT = PROVED_CONDITIONAL_AFTER_INDEPENDENT_V42_GATE_B_AND_V43_JOIN",
    "V52_TWO_GATE_MARGIN = MIN_ETA_PAD_ETA_B_419_OVER_2400_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON",
    "V52_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_THETA_FIXED_RESIDUE_SIEGEL_WALFISZ_AND_MOVING_PRODUCT_MISMATCH",
    "V52_DRAPPEAU_DISPERSION = NO_GO_DIRECT_FIXED_PRODUCT_AND_MODULUS_INDEPENDENT_ARRAY_MISMATCH",
    "V52_WRIGHT_UNBALANCED_CONVOLUTION = NO_GO_DIRECT_FIXED_RESIDUE_AND_SHORT_SIEGEL_WALFISZ_SEQUENCE_MISMATCH",
    "V52_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_LOCAL_CELL_ONLY",
    "V52_PASCADI_EXCEPTIONAL_SIEVE = SOURCE_BACKED_CONDITIONAL_AFTER_LITERAL_TRANSFORM_AND_NORM",
    "V52_DIRECT_PRIMARY_SOURCE_FOR_H_PAD = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11",
    "V52_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_A_POWER_SAVING_PAIR_ENDPOINT_ANGLE_OR_TOTAL_SUPER_BDH_SAVING_ABOVE_1_OVER_200_FOR_THE_COMPENSATED_MOVING_PRODUCT_PRIME_DILATION",
    "V52_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE",
    "V52_V50_BOUNDED_CORE = RETAINED_SEQUENTIAL_CONJECTURAL_ALTERNATIVE",
    "V52_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_COMPENSATED_DILATION_REVERSE_CHEN_SLICE_ENDPOINT_SIMPLEX_AND_MARGINAL_NO_GO",
    "V52_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM",
    "V52_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PAIR_ANGULAR_GATE_A_MAPPED_ARITHMETIC_BOUND_OPEN",
    "V52_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED",
    "V52_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B",
)


REGISTRY_SHA256 = "0f2223c6c3e18d68c862091e6c67a91257651e49df3551ffb741a8011de4a95b"


SOURCE_LOCKS = (
    (
        "2512.22798v1",
        "Zongkun Zheng",
        "Theorems 1.1--1.2 use fixed simultaneous residues and theta at most 7/36 or 2/23, not the moving folded product at theta=1/3",
    ),
    (
        "1504.05549v4",
        "Sary Drappeau",
        "Theorem 5.1 is a fixed-product dispersion theorem with modulus-independent dyadic arrays",
    ),
    (
        "2604.25177v2",
        "Thomas Wright",
        "the unbalanced convolution theorem has a fixed residue and a short Siegel--Walfisz sequence",
    ),
    (
        "2607.24311v1",
        "Valentin Blomer; Alexandru Pascadi",
        "Theorem 1.1 is a fixed-modulus bilinear Kloosterman cell with c^(-1/32+o(1)) critical saving",
    ),
    (
        "2404.04239v3",
        "Alexandru Pascadi",
        "exceptional-form large sieves accept special sparse-Fourier arrays after a literal transform and norm are supplied",
    ),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md",
        "b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e",
    ),
    (
        "research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md",
        "56a3959ca2f7867e370b9ec11d1ad601824297f1b27a713503ac34df13234c73",
    ),
    (
        "research/tpc-big-road/bridge_b_master_marginal_collapse_and_joint_residual_firewall.md",
        "6785eab0d05ec1b564c99d6d155788950bc7383b0fdfa10e2458dab71956b167",
    ),
    (
        "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md",
        "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_fold_first_long_mobius_checker.py",
        "072f5461df00456a7fc2bea141d466bc23663826201c03e4e8d2daa7c6f86deb",
    ),
)


def _make_trusted_runner(
    *,
    registry_seed=REGISTRY,
    source_seed=SOURCE_LOCKS,
    dependency_seed=DEPENDENCIES,
    registry_digest_seed=REGISTRY_SHA256,
    maximum_claim_seed=MAXIMUM_CLAIM,
    fraction_type=Fraction,
    path_type=Path,
    sha256_fn=hashlib.sha256,
    dict_type=dict,
    tuple_type=tuple,
    list_type=list,
    str_type=str,
    int_type=int,
    bool_type=bool,
    type_fn=type,
    len_fn=len,
    all_fn=all,
    zip_fn=zip,
    set_type=set,
    range_fn=range,
    enumerate_fn=enumerate,
    sum_fn=sum,
    abs_fn=abs,
    min_fn=min,
    max_fn=max,
    sorted_fn=sorted,
    hash_fn=hash,
    file_seed=__file__,
):
    literal_maximum_claim = (
        "EXACT_COMPENSATED_PAIR_DILATION_AND_PACKET_ENDPOINT_COMPILER_IDENTIFIES_THE_"
        "FOLDED_GATE_A_AS_A_REVERSE_CHEN_PARITY_RESIDUAL_AND_PROVES_THE_MARGINAL_BDH_"
        "PLUS_CAUCHY_COMPILER_MISSES_BY_1_OVER_400"
    )
    literal_registry_digest = "0f2223c6c3e18d68c862091e6c67a91257651e49df3551ffb741a8011de4a95b"
    literal_registry = tuple_type(registry_seed)
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(file_seed).resolve().parents[2]
    path_is_file = path_type.is_file
    path_read_bytes = path_type.read_bytes
    mutation_labels = []

    if maximum_claim_seed != literal_maximum_claim:
        raise CheckFailure("maximum-claim seed changed")
    if registry_digest_seed != literal_registry_digest:
        raise CheckFailure("registry digest seed changed")

    def canonical_digest(rows):
        return sha256_fn(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()

    if canonical_digest(literal_registry) != literal_registry_digest:
        raise CheckFailure("registry literal digest changed")

    def same_exact(got, want):
        if type_fn(got) is not type_fn(want):
            return False
        if type_fn(want) is tuple_type:
            return len_fn(got) == len_fn(want) and all_fn(
                same_exact(g, w) for g, w in zip_fn(got, want)
            )
        if type_fn(want) is dict_type:
            if not all_fn(type_fn(key) is str_type for key in got):
                return False
            if set_type(got) != set_type(want):
                return False
            return all_fn(same_exact(got[key], want[key]) for key in want)
        return got == want

    def validate_registry(candidate):
        if type_fn(candidate) is not tuple_type:
            raise CheckFailure("registry container type changed")
        if not all_fn(type_fn(row) is str_type for row in candidate):
            raise CheckFailure("registry row type changed")
        if candidate != literal_registry:
            raise CheckFailure("registry values changed")
        if canonical_digest(candidate) != literal_registry_digest:
            raise CheckFailure("registry digest changed")

    def validate_sources(candidate):
        if not same_exact(candidate, literal_sources):
            raise CheckFailure("source lock changed")

    def canonical_file_hash(path):
        if not path_is_file(path):
            raise CheckFailure("dependency path missing")
        return sha256_fn(path_read_bytes(path).replace(b"\r\n", b"\n")).hexdigest()

    def validate_dependencies(candidate):
        if not same_exact(candidate, literal_dependencies):
            raise CheckFailure("dependency lock changed")
        for relative, expected_hash in candidate:
            if canonical_file_hash(repo_root / relative) != expected_hash:
                raise CheckFailure("dependency hash changed: " + relative)

    def mobius(n):
        if type_fn(n) is not int_type or n < 1:
            raise CheckFailure("mobius input changed")
        m = n
        parity = 0
        p = 2
        while p * p <= m:
            if m % p == 0:
                m //= p
                if m % p == 0:
                    return 0
                parity += 1
                while m % p == 0:
                    m //= p
            p += 1
        if m > 1:
            parity += 1
        return -1 if parity % 2 else 1

    def divisors(n):
        return tuple_type(d for d in range_fn(1, n + 1) if n % d == 0)

    def prime_power_exponent(n):
        for p in range_fn(2, n + 1):
            is_prime = True
            d = 2
            while d * d <= p:
                if p % d == 0:
                    is_prime = False
                    break
                d += 1
            if not is_prime:
                continue
            value = p
            exponent = 1
            while value < n:
                value *= p
                exponent += 1
            if value == n:
                return exponent
        return 0

    def sieve_beta(n, cutoff):
        exponent = prime_power_exponent(n)
        prime_term = fraction_type(1, exponent) if exponent else fraction_type(0, 1)
        mu_sum = sum_fn(mobius(d) for d in divisors(n) if d <= cutoff)
        return prime_term - mu_sum

    def log_vector(n):
        values = {}
        m = n
        p = 2
        while p * p <= m:
            while m % p == 0:
                values[p] = values.get(p, 0) + 1
                m //= p
            p += 1
        if m > 1:
            values[m] = values.get(m, 0) + 1
        return tuple_type((p, fraction_type(values[p], 1)) for p in sorted_fn(values))

    def scale_vector(vector, scalar):
        return tuple_type((p, coefficient * scalar) for p, coefficient in vector)

    def add_vectors(*vectors):
        values = {}
        for vector in vectors:
            for p, coefficient in vector:
                values[p] = values.get(p, fraction_type(0, 1)) + coefficient
        return tuple_type(
            (p, values[p]) for p in sorted_fn(values) if values[p] != 0
        )

    def pair_numerator(s, ell, cutoff):
        if not (1 < s < ell):
            raise CheckFailure("pair order changed")
        if s <= cutoff:
            return scale_vector(log_vector(s), mobius(ell) - mobius(s))
        return add_vectors(
            scale_vector(log_vector(ell), mobius(s)),
            scale_vector(log_vector(s), mobius(ell)),
        )

    def pair_sum_for_t(t, cutoff):
        rows = []
        for s in range_fn(2, t):
            if t % s != 0:
                continue
            ell = t // s
            if s < ell:
                rows.append(pair_numerator(s, ell, cutoff))
        return add_vectors(*tuple_type(rows))

    def dot(left, right):
        return sum_fn(a * b for a, b in zip_fn(left, right))

    def finite_fixtures():
        target = fraction_type(1997, 1200)
        diagonal_scale = fraction_type(5, 3)
        endpoint_gap = diagonal_scale - target
        dilation_ceiling = fraction_type(191, 96)
        dilation_deficit = dilation_ceiling - target
        one_generic_one_bdh = (fraction_type(2, 1) + diagonal_scale) / 2
        one_generic_one_bdh_deficit = one_generic_one_bdh - target
        two_generic_deficit = fraction_type(2, 1) - target
        square_margin = target - fraction_type(143, 96)
        model_margin = target - fraction_type(53, 32)
        shell_margin = target - fraction_type(79, 48)
        dilation_length = fraction_type(21, 32) - fraction_type(1, 3)

        t12_pair = pair_sum_for_t(12, 4)
        t12_log = log_vector(12)
        beta_14 = sieve_beta(14, 4)
        beta_35 = sieve_beta(35, 4)
        beta_49 = sieve_beta(49, 4)

        q = 5
        t = 6
        beta_t = 2
        endpoint = ((4, 2), (6, -1), (11, 3))
        direct = fraction_type(0, 1)
        same_sum = 0
        all_sum = 0
        for u, weight in endpoint:
            same = (u - t) % q == 0
            cprime = fraction_type(q - 2, q - 1) if same else fraction_type(-1, q - 1)
            direct += q * beta_t * weight * cprime
            all_sum += weight
            if same:
                same_sum += weight
        dilation_positive = q * beta_t * same_sum
        dilation_mean = fraction_type(q, q - 1) * beta_t * all_sum
        dilation_compensated = dilation_positive - dilation_mean

        hilbert_x = (3, 4)
        hilbert_parallel = (3, 4)
        hilbert_orthogonal = (-4, 3)
        hilbert_norms = (
            dot(hilbert_x, hilbert_x),
            dot(hilbert_parallel, hilbert_parallel),
            dot(hilbert_orthogonal, hilbert_orthogonal),
        )
        hilbert_inner = (
            dot(hilbert_x, hilbert_parallel),
            dot(hilbert_x, hilbert_orthogonal),
        )

        angular_example = fraction_type(1, 300) - endpoint_gap
        symmetric_super_bdh = fraction_type(1, 300) - endpoint_gap

        return dict_type(
            (
                ("target", target),
                ("diagonal_scale", diagonal_scale),
                ("endpoint_gap", endpoint_gap),
                ("dilation_ceiling", dilation_ceiling),
                ("dilation_deficit", dilation_deficit),
                ("one_generic_one_bdh", one_generic_one_bdh),
                ("one_generic_one_bdh_deficit", one_generic_one_bdh_deficit),
                ("two_generic_deficit", two_generic_deficit),
                ("square_margin", square_margin),
                ("model_margin", model_margin),
                ("shell_margin", shell_margin),
                ("dilation_length", dilation_length),
                ("t12_pair", t12_pair),
                ("t12_log", t12_log),
                ("beta_14", beta_14),
                ("beta_35", beta_35),
                ("beta_49", beta_49),
                ("dilation_direct", direct),
                ("dilation_positive", dilation_positive),
                ("dilation_mean", dilation_mean),
                ("dilation_compensated", dilation_compensated),
                ("diagonal_q5_weight", fraction_type(q * (q - 2), q - 1)),
                ("hilbert_norms", hilbert_norms),
                ("hilbert_inner", hilbert_inner),
                ("angular_example", angular_example),
                ("symmetric_super_bdh", symmetric_super_bdh),
            )
        )

    fixture = finite_fixtures()

    contract_items = (
        ("maximum_claim", literal_maximum_claim),
        ("route_advance", "YES"),
        ("conditional_bridge_advance", "YES"),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
        ("numbered_release", "NO"),
        ("proof_path", literal_dependencies[0][0]),
        ("proof_sha256", literal_dependencies[0][1]),
        ("registry_sha256", literal_registry_digest),
        ("registry_rows", 65),
        ("source_locks", 5),
        ("dependency_locks", 5),
        ("target_numerator", "1997/1200"),
        ("diagonal_scale", "5/3"),
        ("endpoint_gap", "1/400"),
        ("total_super_bdh_threshold", "1/200"),
        ("dilation_length", "31/96"),
        ("dilation_ceiling", "191/96"),
        ("dilation_deficit", "781/2400"),
        ("pair_dilation_exact", True),
        ("reverse_chen_slice_exact", True),
        ("marginal_bdh_attachment", False),
        ("angular_dispersion_attachment", False),
        ("zheng_direct_attachment", False),
        ("blomer_pascadi_local_engine", True),
        ("gate_b_attachment", False),
        ("first_fatal", "NO_LITERAL_PAIR_ANGLE_OR_TOTAL_SUPER_BDH_THEOREM"),
        ("route_position", "BRIDGE_A_PAIR_ANGULAR_GATE_A_MAPPED"),
    )
    expected_contract = dict_type(contract_items)

    def validate_contract(candidate):
        if not same_exact(candidate, expected_contract):
            raise CheckFailure("contract changed")

    def fraction_text(value):
        if value.denominator == 1:
            return str_type(value.numerator)
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    def vector_text(vector):
        return tuple_type((p, fraction_text(coefficient)) for p, coefficient in vector)

    def result_items_base():
        return (
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
            ("target_numerator", fraction_text(fixture["target"])),
            ("diagonal_scale", fraction_text(fixture["diagonal_scale"])),
            ("endpoint_gap", fraction_text(fixture["endpoint_gap"])),
            ("total_super_bdh_threshold", fraction_text(2 * fixture["endpoint_gap"])),
            ("dilation_length", fraction_text(fixture["dilation_length"])),
            ("dilation_ceiling", fraction_text(fixture["dilation_ceiling"])),
            ("dilation_deficit", fraction_text(fixture["dilation_deficit"])),
            ("one_generic_one_bdh", fraction_text(fixture["one_generic_one_bdh"])),
            ("one_generic_one_bdh_deficit", fraction_text(fixture["one_generic_one_bdh_deficit"])),
            ("two_generic_deficit", fraction_text(fixture["two_generic_deficit"])),
            ("square_margin", fraction_text(fixture["square_margin"])),
            ("model_margin", fraction_text(fixture["model_margin"])),
            ("shell_margin", fraction_text(fixture["shell_margin"])),
            ("t12_pair", vector_text(fixture["t12_pair"])),
            ("t12_log", vector_text(fixture["t12_log"])),
            ("t12_collapse", fixture["t12_pair"] == fixture["t12_log"]),
            ("semiprime_beta", tuple_type(fraction_text(fixture[key]) for key in ("beta_14", "beta_35", "beta_49"))),
            ("dilation_direct", fraction_text(fixture["dilation_direct"])),
            ("dilation_positive", fraction_text(fixture["dilation_positive"])),
            ("dilation_mean", fraction_text(fixture["dilation_mean"])),
            ("dilation_compensated", fraction_text(fixture["dilation_compensated"])),
            ("dilation_identity", fixture["dilation_direct"] == fixture["dilation_compensated"]),
            ("diagonal_q5_weight", fraction_text(fixture["diagonal_q5_weight"])),
            ("hilbert_norms", fixture["hilbert_norms"]),
            ("hilbert_inner", fixture["hilbert_inner"]),
            ("marginal_angle_no_go", fixture["hilbert_norms"] == (25, 25, 25) and fixture["hilbert_inner"] == (25, 0)),
            ("angular_example_margin", fraction_text(fixture["angular_example"])),
            ("symmetric_super_bdh_margin", fraction_text(fixture["symmetric_super_bdh"])),
            ("pair_dilation_exact", True),
            ("reverse_chen_slice_exact", True),
            ("marginal_bdh_attachment", False),
            ("angular_dispersion_attachment", False),
            ("zheng_direct_attachment", False),
            ("drappeau_direct_attachment", False),
            ("wright_direct_attachment", False),
            ("blomer_pascadi_local_engine", True),
            ("pascadi_horizontal_attachment", False),
            ("gate_b_attachment", False),
            ("source_attachment", False),
            ("paper_candidate_status", "OUTLINE_ONLY"),
            ("first_fatal", "NO_LITERAL_PAIR_ANGLE_OR_TOTAL_SUPER_BDH_THEOREM"),
            ("route_position", "BRIDGE_A_PAIR_ANGULAR_GATE_A_MAPPED"),
            ("registry_sha256", literal_registry_digest),
            ("registry_rows", len_fn(literal_registry)),
            ("source_locks", len_fn(literal_sources)),
            ("dependency_locks", len_fn(literal_dependencies)),
            ("contract_fields", len_fn(contract_items)),
        )

    def wrong_type(value):
        if type_fn(value) is bool_type:
            return 1 if value else 0
        if type_fn(value) is int_type:
            return False
        if type_fn(value) is str_type:
            class StringSubclass(str_type):
                pass
            return StringSubclass(value)
        if type_fn(value) is tuple_type:
            return list_type(value)
        return None

    def wrong_value(value):
        if type_fn(value) is bool_type:
            return not value
        if type_fn(value) is int_type:
            return value + 1
        if type_fn(value) is str_type:
            return value + "_MUT"
        if type_fn(value) is tuple_type:
            return value + ("MUT",)
        return "MUT"

    def must_reject(label, validator, candidate):
        mutation_labels.append(label)
        try:
            validator(candidate)
        except CheckFailure:
            return
        raise CheckFailure("mutation accepted: " + label)

    def run_contract_mutations():
        start = len_fn(mutation_labels)
        for key, value in contract_items:
            missing = dict_type(expected_contract)
            del missing[key]
            must_reject("contract_missing_" + key, validate_contract, missing)
            typed = dict_type(expected_contract)
            typed[key] = wrong_type(value)
            must_reject("contract_type_" + key, validate_contract, typed)
            changed = dict_type(expected_contract)
            changed[key] = wrong_value(value)
            must_reject("contract_value_" + key, validate_contract, changed)
        extra = dict_type(expected_contract)
        extra["EXTRA"] = 1
        must_reject("contract_extra", validate_contract, extra)

        class KeyImpostor:
            def __hash__(self):
                return hash_fn("maximum_claim")

            def __eq__(self, other):
                return other == "maximum_claim"

        impostor = dict_type(expected_contract)
        value = impostor.pop("maximum_claim")
        impostor[KeyImpostor()] = value
        must_reject("contract_key_impostor", validate_contract, impostor)
        return len_fn(mutation_labels) - start

    def run_registry_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_registry):
            changed = list_type(literal_registry)
            changed[index] = row + "_MUT"
            must_reject("registry_value_" + str_type(index), validate_registry, tuple_type(changed))
            changed[index] = 7
            must_reject("registry_type_" + str_type(index), validate_registry, tuple_type(changed))
        must_reject("registry_missing", validate_registry, literal_registry[:-1])
        must_reject("registry_extra", validate_registry, literal_registry + ("EXTRA = MUT",))
        must_reject("registry_list", validate_registry, list_type(literal_registry))
        must_reject("registry_duplicate", validate_registry, literal_registry[:-1] + (literal_registry[0],))
        return len_fn(mutation_labels) - start

    def run_source_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_sources):
            changed = list_type(literal_sources)
            changed[index] = row[:-1] + (row[-1] + "_MUT",)
            must_reject("source_value_" + str_type(index), validate_sources, tuple_type(changed))
            changed[index] = list_type(row)
            must_reject("source_type_" + str_type(index), validate_sources, tuple_type(changed))
        must_reject("source_missing", validate_sources, literal_sources[:-1])
        must_reject("source_extra", validate_sources, literal_sources + (("x", "y", "z"),))
        must_reject("source_list", validate_sources, list_type(literal_sources))
        return len_fn(mutation_labels) - start

    def run_dependency_mutations():
        start = len_fn(mutation_labels)
        for index, row in enumerate_fn(literal_dependencies):
            changed = list_type(literal_dependencies)
            changed[index] = (row[0], "0" * 64)
            must_reject("dependency_value_" + str_type(index), validate_dependencies, tuple_type(changed))
            changed[index] = list_type(row)
            must_reject("dependency_type_" + str_type(index), validate_dependencies, tuple_type(changed))
        must_reject("dependency_missing", validate_dependencies, literal_dependencies[:-1])
        must_reject("dependency_extra", validate_dependencies, literal_dependencies + (("x", "0" * 64),))
        must_reject("dependency_list", validate_dependencies, list_type(literal_dependencies))
        return len_fn(mutation_labels) - start

    def validate_result(candidate, expected):
        if not same_exact(candidate, expected):
            raise CheckFailure("result changed")

    validate_registry(literal_registry)
    validate_sources(literal_sources)
    validate_dependencies(literal_dependencies)
    validate_contract(expected_contract)

    if fixture["endpoint_gap"] != fraction_type(1, 400):
        raise CheckFailure("endpoint gap changed")
    if 2 * fixture["endpoint_gap"] != fraction_type(1, 200):
        raise CheckFailure("total super-BDH threshold changed")
    if fixture["dilation_length"] != fraction_type(31, 96):
        raise CheckFailure("dilation length changed")
    if fixture["dilation_deficit"] != fraction_type(781, 2400):
        raise CheckFailure("dilation deficit changed")
    if fixture["one_generic_one_bdh_deficit"] != fraction_type(203, 1200):
        raise CheckFailure("one generic one BDH deficit changed")
    if fixture["two_generic_deficit"] != fraction_type(403, 1200):
        raise CheckFailure("generic deficit changed")
    if fixture["square_margin"] != fraction_type(419, 2400):
        raise CheckFailure("square margin changed")
    if fixture["model_margin"] != fraction_type(19, 2400):
        raise CheckFailure("model margin changed")
    if fixture["shell_margin"] != fraction_type(11, 600):
        raise CheckFailure("shell margin changed")
    if fixture["t12_pair"] != fixture["t12_log"]:
        raise CheckFailure("t12 pair collapse changed")
    if (fixture["beta_14"], fixture["beta_35"], fixture["beta_49"]) != (
        fraction_type(0, 1), fraction_type(-1, 1), fraction_type(-1, 2)
    ):
        raise CheckFailure("semiprime or square slice changed")
    if (
        fixture["dilation_direct"],
        fixture["dilation_positive"],
        fixture["dilation_mean"],
        fixture["dilation_compensated"],
    ) != (
        fraction_type(10, 1),
        fraction_type(20, 1),
        fraction_type(10, 1),
        fraction_type(10, 1),
    ):
        raise CheckFailure("q5 compensated dilation changed")
    if fixture["diagonal_q5_weight"] != fraction_type(15, 4):
        raise CheckFailure("q5 diagonal character weight changed")
    if fixture["hilbert_norms"] != (25, 25, 25) or fixture["hilbert_inner"] != (25, 0):
        raise CheckFailure("Hilbert marginal no-go changed")
    if fixture["angular_example"] != fraction_type(1, 1200):
        raise CheckFailure("angular example margin changed")
    if fixture["symmetric_super_bdh"] != fraction_type(1, 1200):
        raise CheckFailure("super-BDH example margin changed")

    contract_mutations = run_contract_mutations()
    registry_mutations = run_registry_mutations()
    source_mutations = run_source_mutations()
    dependency_mutations = run_dependency_mutations()

    result_base = result_items_base()
    provisional = dict_type(
        result_base
        + (
            ("contract_mutations", contract_mutations),
            ("registry_mutations", registry_mutations),
            ("source_mutations", source_mutations),
            ("dependency_mutations", dependency_mutations),
            ("semantic_mutations", 0),
            ("mutation_actions", 0),
        )
    )
    semantic_expected = dict_type(provisional)

    semantic_start = len_fn(mutation_labels)
    for key, value in tuple_type(semantic_expected.items()):
        missing = dict_type(semantic_expected)
        del missing[key]
        must_reject("result_missing_" + key, lambda c: validate_result(c, semantic_expected), missing)
        typed = dict_type(semantic_expected)
        typed[key] = wrong_type(value)
        must_reject("result_type_" + key, lambda c: validate_result(c, semantic_expected), typed)
        changed = dict_type(semantic_expected)
        changed[key] = wrong_value(value)
        must_reject("result_value_" + key, lambda c: validate_result(c, semantic_expected), changed)
    extra = dict_type(semantic_expected)
    extra["EXTRA"] = 1
    must_reject("result_extra", lambda c: validate_result(c, semantic_expected), extra)
    semantic_mutations = len_fn(mutation_labels) - semantic_start
    mutation_actions = len_fn(mutation_labels)

    final_result = dict_type(
        result_base
        + (
            ("contract_mutations", contract_mutations),
            ("registry_mutations", registry_mutations),
            ("source_mutations", source_mutations),
            ("dependency_mutations", dependency_mutations),
            ("semantic_mutations", semantic_mutations),
            ("mutation_actions", mutation_actions),
        )
    )

    expected_counts = (95, 134, 13, 13, 190, 445)
    actual_counts = (
        contract_mutations,
        registry_mutations,
        source_mutations,
        dependency_mutations,
        semantic_mutations,
        mutation_actions,
    )
    if actual_counts != expected_counts:
        raise CheckFailure("mutation counts changed: " + str_type(actual_counts))
    if len_fn(tuple_type(mutation_labels)) != len_fn(set_type(mutation_labels)):
        raise CheckFailure("mutation labels not unique")

    validate_result(final_result, final_result)
    return dict_type(final_result)


def _seal_runner():
    factory = _make_trusted_runner
    registry = tuple(REGISTRY)
    sources = tuple(SOURCE_LOCKS)
    dependencies = tuple(DEPENDENCIES)
    registry_digest = REGISTRY_SHA256
    maximum_claim = MAXIMUM_CLAIM
    fraction_type = Fraction
    path_type = Path
    sha256_fn = hashlib.sha256
    dict_type = dict
    tuple_type = tuple
    list_type = list
    str_type = str
    int_type = int
    bool_type = bool
    type_fn = type
    len_fn = len
    all_fn = all
    zip_fn = zip
    set_type = set
    range_fn = range
    enumerate_fn = enumerate
    sum_fn = sum
    abs_fn = abs
    min_fn = min
    max_fn = max
    sorted_fn = sorted
    hash_fn = hash
    file_seed = __file__

    def sealed():
        return factory(
            registry_seed=registry,
            source_seed=sources,
            dependency_seed=dependencies,
            registry_digest_seed=registry_digest,
            maximum_claim_seed=maximum_claim,
            fraction_type=fraction_type,
            path_type=path_type,
            sha256_fn=sha256_fn,
            dict_type=dict_type,
            tuple_type=tuple_type,
            list_type=list_type,
            str_type=str_type,
            int_type=int_type,
            bool_type=bool_type,
            type_fn=type_fn,
            len_fn=len_fn,
            all_fn=all_fn,
            zip_fn=zip_fn,
            set_type=set_type,
            range_fn=range_fn,
            enumerate_fn=enumerate_fn,
            sum_fn=sum_fn,
            abs_fn=abs_fn,
            min_fn=min_fn,
            max_fn=max_fn,
            sorted_fn=sorted_fn,
            hash_fn=hash_fn,
            file_seed=file_seed,
        )

    return sealed


_TRUSTED_RUN = _seal_runner()
run_check = _TRUSTED_RUN


def _make_main(
    trusted_runner,
    *,
    tuple_type=tuple,
    type_fn=type,
    str_type=str,
    len_fn=len,
    json_dumps=json.dumps,
    stdout_write=sys.stdout.write,
):
    baseline = trusted_runner()
    baseline_items = tuple_type(baseline.items())
    frozen_stdout = json_dumps(baseline, sort_keys=True, separators=(",", ":")) + "\n"

    def sealed(*argv_objects):
        if len_fn(argv_objects) != 1:
            raise CheckFailure("explicit --check is required")
        argv = argv_objects[0]
        if type_fn(argv) is not tuple_type:
            raise CheckFailure("explicit --check is required")
        if len_fn(argv) != 1 or type_fn(argv[0]) is not str_type or argv[0] != "--check":
            raise CheckFailure("explicit --check is required")
        result = trusted_runner()
        if tuple_type(result.items()) != baseline_items:
            raise CheckFailure("sealed result changed")
        stdout_write(frozen_stdout)
        return 0

    return sealed


main = _make_main(_TRUSTED_RUN)


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
