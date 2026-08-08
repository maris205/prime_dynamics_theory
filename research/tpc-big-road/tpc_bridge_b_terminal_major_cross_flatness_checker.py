#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V30 big-road audit."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_QLOCAL_MAJOR_MODEL_X_95_OVER_96_PLUS_CELL_PRODUCT_MRT_REDUCTION_"
    "PLUS_ENDPOINT_EQUIVALENCE_PLUS_EQUIVARIANT_QUOTIENT_NO_GO"
)


CONTRACT_ITEMS = (
    ("maximum_claim", MAXIMUM_CLAIM),
    ("route_advance", "YES"),
    ("fixed_h0", 2),
    ("physical_scale", "x=2X"),
    ("prime_shell_Q_exponent", "1/3"),
    ("difference_horizon_exponent", "21/32"),
    ("psi_support", "[-1,1]"),
    ("psi_integral", "1"),
    ("fourier_transform", "hatpsi_plus(xi)=int_psi(v)e(+xi*v)dv"),
    ("jutila_kernel_sign", "G_USES_chi_AND_B_conjW_USES_chi_reflected"),
    ("zero_axis_identity", "S=J(e)+E(e)"),
    ("endpoint_exponent", "399/400"),
    ("offzero_coefficient_exponent", "-1/192"),
    ("endpoint_margin", "13/4800"),
    ("terminal_equivalence", "A_IFF_PHYSICAL_AFTER_B_IN_STRICT_POWER_CLASS"),
    ("selected_route", "B_THEN_A_THEN_C"),
    ("q_local_profile", "F_MINUS_G_THREE_VALUE_PERIODIC"),
    ("ramanujan_pairing", "mean(c_q*Delta)=Delta(0)"),
    ("poisson_constant", "H*psi(0)"),
    ("alias_condition", "H>2Q"),
    ("q_local_model_exponent", "95/96"),
    ("q_local_model_margin", "19/2400"),
    ("boundary_exponent", "47/48+epsilon"),
    ("boundary_epsilon_ceiling", "11/1920"),
    ("q_local_diagonal_exponent", "2/3"),
    ("residual_major", "OPEN_SIGNED_QLOCAL_COVARIANCE"),
    ("local_BC_exponent", "1891/1920"),
    ("cell_count", "2Y"),
    ("window_cell_overlap", 3),
    ("cross_flatness", "OPEN_ACTUAL_TAGGED_LOCAL_THEOREM"),
    ("cell_l1_global", "x^(1+o(1))"),
    ("actual_major_attachment", "M_T=Mloc+a_WITH_WEIGHTED_L2_A"),
    ("hard_major", "PREDECLARED"),
    ("MRT_source", "arXiv:1707.01315v3_Proposition_3.1"),
    (
        "MRT_fourier_source",
        "arXiv:1812.01224v1_Theorem_1.2_LIOUVILLE_Theorem_1.4_INVERSE",
    ),
    ("Guth_Maynard_source", "arXiv:2405.20552v2_Theorem_1.1"),
    ("equivariant_quotient", "FULL_COORDINATE_FACTOR_IMPLIES_INJECTIVE"),
    ("full_coordinate_kappa", "N"),
    ("full_coordinate_kappa0", "N-1"),
    ("q5_kernel", "K5=(5/3)*1_{1,2,4}"),
    ("q5_kappa", "5/3"),
    ("q5_kappa0", "2/3"),
    ("first_fatal", "MLOC_ATTACHMENT_AND_TAGGED_CROSS_FLATNESS_MISSING"),
    ("arithmetic_advance", False),
    ("fixed_atom_credit", 0),
    ("strict_1_over_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", False),
    ("numbered_release", "NO"),
)


REGISTRY_ITEMS = (
    ("V30_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V30_ROUTE_ADVANCE", "YES"),
    ("V30_ARITHMETIC_ADVANCE", "NO"),
    ("V30_FIXED_ATOM_CREDIT", "0"),
    ("V30_STRICT_1_OVER_400", "UNPAID"),
    ("V30_L2", "NONE"),
    ("V30_TPC_207_TRIGGER", "false"),
    ("V30_NUMBERED_RELEASE", "NO"),
    (
        "V30_SELECTED_RESEARCH_ROUTE",
        "B_TAGGED_HARD_MAJOR_CELL_PRODUCT_AND_MLOC_ATTACHMENT",
    ),
    (
        "V30_LOGICAL_TERMINAL_GATE",
        "A_TAGGED_QLOCAL_RESIDUAL_MAJOR_AFTER_B",
    ),
    (
        "V30_LITERAL_JUTILA_MAJOR_SCALAR",
        "PROVED_EXACT_L0_WITH_REFLECTED_KERNEL_SIGN",
    ),
    ("V30_J_ZERO_AXIS_SELF_RETURN", "PROVED_EXACT_S_PLUS_OFFZERO"),
    (
        "V30_OFFZERO_GATE_TO_E_MARGIN",
        "PROVED_EXACT_CONDITIONAL_13_OVER_4800_MINUS_THETA_MINUS_EPSILON",
    ),
    (
        "V30_A_B_ENDPOINT_EQUIVALENCE",
        "PROVED_EXACT_STRICT_EXPONENT_CLASS",
    ),
    (
        "V30_A_AS_EASIER_PRELIMINARY",
        "STOP_SCOPED_TERMINAL_EQUIVALENCE_AFTER_B",
    ),
    (
        "V30_A_ADJOINT_CONVOLUTION_IDENTITY",
        "PROVED_EXACT_ALGEBRAIC",
    ),
    ("V30_QLOCAL_F_G_DELTA_PROFILE", "PROVED_EXACT_FINITE_PERIOD"),
    (
        "V30_QLOCAL_RAMANUJAN_PAIRING",
        "PROVED_EXACT_NORMALIZED_MEAN_EQUALS_DELTA_AT_ZERO",
    ),
    (
        "V30_QLOCAL_POISSON_CONSTANT",
        "PROVED_EXACT_H_TIMES_PSI_AT_ZERO",
    ),
    (
        "V30_QLOCAL_UNIT_NONUNIT_LEDGER",
        "PROVED_EXACT_ZERO_NUMERATOR_ADDED_AND_SUBTRACTED_ONCE",
    ),
    (
        "V30_QLOCAL_MODEL_RESIDUAL_REASSEMBLY",
        "PROVED_EXACT_OCCURRENCEWISE",
    ),
    (
        "V30_QLOCAL_MODEL_BOUND",
        "PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1",
    ),
    ("V30_QLOCAL_MODEL_MARGIN_TO_399_400", "19/2400"),
    ("V30_QLOCAL_BOUNDARY", "PROVED_X_47_OVER_48_PLUS_EPSILON"),
    (
        "V30_QLOCAL_DIAGONAL_MODEL_BOUND",
        "PROVED_X_2_OVER_3_PLUS_O1",
    ),
    (
        "V30_QLOCAL_PHYSICAL_DIAGONAL_SURVIVES",
        "PROVED_EXACT_COEFFICIENT_ONE_MINUS_SMALL_MODEL",
    ),
    (
        "V30_TAGGED_QLOCAL_RESIDUAL_MAJOR_COVARIANCE",
        "SELECTED_TERMINAL_OPEN_NEW_THEOREM",
    ),
    (
        "V30_A_FIRST_FATAL",
        "TAGGED_QLOCAL_RESIDUAL_MAJOR_COVARIANCE",
    ),
    (
        "V30_DIRECT_BV_BDH_ATTACHMENT",
        "STOP_SCOPED_WRONG_SIGNED_COVARIANCE_OBJECT",
    ),
    (
        "V30_LOCAL_BC_CARRIER",
        "PROVED_SOURCE_BACKED_X_1891_OVER_1920_BUT_ZERO_GLOBAL_CREDIT",
    ),
    (
        "V30_B_MRT_PRODUCT_LOCAL_REDUCTION",
        "SOURCE_BACKED_REDUCTION_ONLY",
    ),
    (
        "V30_B_HARD_MAJOR_PREDECLARATION",
        "REQUIRED_CIRCULARITY_FIREWALL",
    ),
    (
        "V30_B_CELL_PRODUCT_CERTIFICATE",
        "PROVED_EXACT_PARTITION_AND_CAUCHY_SCHWARZ",
    ),
    (
        "V30_B_CELL_L1_GLOBAL_BOUND",
        "PROVED_ELEMENTARY_X_1_PLUS_O1",
    ),
    (
        "V30_B_CELL_LINF_CROSS_FLATNESS",
        "OPEN_ACTUAL_TAGGED_LOCAL_THEOREM",
    ),
    ("V30_B_ACTUAL_CELL_ENERGY_BOUND", "OPEN_NEW_THEOREM"),
    ("V30_B_MLOC_PLUS_A_ATTACHMENT", "OPEN_WEIGHTED_AP_ATTACHMENT"),
    (
        "V30_B_CROSS_FLATNESS_STRICTLY_WEAKER",
        "PROVED_EXACT_ANTISPIKE_FAMILY",
    ),
    (
        "V30_B_ADAPTIVE_LARGE_SPECTRUM_EXCISION",
        "STOP_SCOPED_MAJOR_ABSORBS_TARGET_WITHOUT_MLOC_ATTACHMENT",
    ),
    (
        "V30_MRT_FOURIER_UNIFORMITY_ATTACHMENT",
        "STOP_SCOPED_LIOUVILLE_OR_NONPRETENTIOUS_1_BOUNDED_AVERAGED_WRONG_QUANTIFIERS",
    ),
    (
        "V30_GUTH_MAYNARD_LARGE_VALUES_ATTACHMENT",
        "STOP_SCOPED_MULTIPLICATIVE_FREQUENCY_WRONG_TRANSFORM",
    ),
    (
        "V30_DIRECT_PRIMARY_SOURCE_ATTACHMENT",
        "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08",
    ),
    (
        "V30_C_EQUIVARIANT_WHOLE_SHELL_QUOTIENT",
        "STOP_SCOPED_TRANSLATION_INVARIANCE_FORCES_INJECTIVITY",
    ),
    (
        "V30_C_FULL_COORDINATE_CHRISTOFFEL",
        "PROVED_EXACT_KAPPA_N_KAPPA0_N_MINUS_1",
    ),
    (
        "V30_C_DISTINGUISHED_SEED_SYMMETRY_BREAK",
        "SURVIVES_SCOPED_OPEN",
    ),
    ("V30_C_ACTUAL_ARITHMETIC_QUOTIENT", "OPEN_NEW_THEOREM"),
    (
        "V30_Q5_GAP2_LOCAL_DENSITY_KERNEL",
        "PROVED_EXACT_FINITE_LOW_CHRISTOFFEL_CARRIER",
    ),
    (
        "V30_Q5_TO_PHYSICAL_POSITIVE_MAIN",
        "STOP_SCOPED_LOCAL_ADMISSIBILITY_DOES_NOT_FORCE_PRIME_MASS",
    ),
    (
        "V30_NEXT_THEOREM",
        "TAGGED_HARD_MAJOR_CELL_CROSS_FLATNESS_PLUS_MLOC_WEIGHTED_ATTACHMENT",
    ),
    (
        "V30_FIRST_FATAL",
        "MISSING_LITERAL_MT_EQUALS_MLOC_PLUS_A_AND_TAGGED_CELL_CROSS_FLATNESS",
    ),
    ("V30_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
    ("V30_PROVENANCE_CASCADE", "REQUIRED"),
)


EXPECTED_REGISTRY_SHA256 = "acead73d0c6e12b03d30d40f35ea345c32d859bea5106456f33b4724fdf23563"


SOURCE_ITEMS = (
    ("BLOMER_LI_JUTILA", "arXiv:2511.03294v1_Lemma_1"),
    ("MRT_PRODUCT_L2", "arXiv:1707.01315v3_Proposition_3.1"),
    (
        "MRT_FOURIER_AVERAGE",
        "arXiv:1812.01224v1_Theorem_1.2_LIOUVILLE_Theorem_1.4_INVERSE",
    ),
    ("GUTH_MAYNARD_LARGE_VALUES", "arXiv:2405.20552v2_Theorem_1.1"),
    ("BETTIN_CHANDEE", "arXiv:1502.00769v1_Theorem_1"),
    ("ABP_CRITICAL_SEED", "arXiv:2212.12202v2_Theorem_1.1"),
    ("HNTV_SEQUENTIAL", "arXiv:1406.4266_Theorem_3.1"),
)


DEPENDENCIES = (
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
    (
        "research/tpc-big-road/bridge_b_joint_major_minor_and_low_christoffel.md",
        "c4b61b790911d2cfcb3d7a0139d368a35d0d0fdab2984637f3f2fe30638543ab",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_joint_major_minor_checker.py",
        "a016840f1ce41b4ed7ee2e315e7848922da1247828f68dfaf3b62e46fac8fa8c",
    ),
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
    enumerate_fn=enumerate,
    range_fn=range,
    sum_fn=sum,
    abs_fn=abs,
    all_fn=all,
    any_fn=any,
    map_fn=map,
    max_fn=max,
):
    literal_maximum_claim = maximum_claim_seed
    literal_contract = tuple_type(contract_seed)
    literal_registry = tuple_type(registry_seed)
    literal_registry_digest = registry_digest_seed
    literal_sources = tuple_type(source_seed)
    literal_dependencies = tuple_type(dependency_seed)
    repo_root = path_type(root_seed)
    if dict_type(literal_contract).get("maximum_claim") != literal_maximum_claim:
        raise failure_type("maximum claim contract seed changed")
    if dict_type(literal_registry).get("V30_MAXIMUM_CLAIM") != literal_maximum_claim:
        raise failure_type("maximum claim registry seed changed")

    def exact_str(value: object) -> bool:
        return type_fn(value) is str_type

    def exact_int(value: object) -> bool:
        return type_fn(value) is int_type

    def exact_bool(value: object) -> bool:
        return type_fn(value) is bool_type

    def canonical_bytes(raw: bytes) -> bytes:
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    def digest_bytes(raw: bytes) -> str:
        return sha256_fn(raw).hexdigest()

    def registry_bytes(candidate: tuple[tuple[str, str], ...]) -> bytes:
        chunks = list_type()
        for key, value in candidate:
            chunks.append((key + "=" + value + "\n").encode("utf-8"))
        return b"".join(chunks)

    def registry_digest(candidate: tuple[tuple[str, str], ...]) -> str:
        return digest_bytes(registry_bytes(candidate))

    def require_pair_tuple(candidate: object, expected: tuple, label: str) -> None:
        if type_fn(candidate) is not tuple_type:
            raise failure_type(label + " outer type changed")
        if len_fn(candidate) != len_fn(expected):
            raise failure_type(label + " length changed")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type(label + " row shape changed")
            if not exact_str(row[0]) or not exact_str(row[1]):
                raise failure_type(label + " row type changed")
        if len_fn(set_type(key for key, _ in candidate)) != len_fn(candidate):
            raise failure_type(label + " keys not unique")
        if candidate != expected:
            raise failure_type(label + " semantic promotion")

    def require_exact_mapping(candidate: object, expected: tuple, label: str) -> None:
        if type_fn(candidate) is not dict_type:
            raise failure_type(label + " outer type changed")
        if not all_fn(type_fn(key) is str_type for key in candidate):
            raise failure_type(label + " key type changed")
        expected_map = dict_type(expected)
        if set_type(candidate) != set_type(expected_map):
            raise failure_type(label + " key set changed")
        for key, value in expected:
            if type_fn(candidate[key]) is not type_fn(value):
                raise failure_type(label + " value type changed at " + key)
            if candidate[key] != value:
                raise failure_type(label + " value changed at " + key)

    def validate_contract(candidate: object) -> None:
        require_exact_mapping(candidate, literal_contract, "contract")

    def validate_registry(candidate: object, claimed_digest: object) -> None:
        require_pair_tuple(candidate, literal_registry, "registry")
        if not exact_str(claimed_digest):
            raise failure_type("registry digest type changed")
        if claimed_digest != literal_registry_digest:
            raise failure_type("registry literal digest changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry content digest changed")

    def validate_sources(candidate: object) -> None:
        require_pair_tuple(candidate, literal_sources, "source")

    def validate_dependencies(candidate: object) -> None:
        require_pair_tuple(candidate, literal_dependencies, "dependency")
        for relative, expected_hash in candidate:
            path = repo_root / relative
            if not path_is_file(path):
                raise failure_type("dependency missing: " + relative)
            actual = digest_bytes(canonical_bytes(path_read_bytes(path)))
            if actual != expected_hash:
                raise failure_type("dependency hash changed: " + relative)

    def delta_value(q: int, a: int, h: int) -> Fraction:
        residue = (a + h) % q
        if residue == q - 2:
            return -fraction_type(q * (q - 2), (q - 1) ** 2)
        if residue == 0:
            return fraction_type(0)
        return fraction_type(q, (q - 1) ** 2)

    def c_q(q: int, h: int) -> int:
        return q - 1 if h % q == 0 else -1

    def delta_vector(q: int) -> tuple[Fraction, ...]:
        return tuple_type(delta_value(q, a, 0) for a in range_fn(q))

    def normalized_mean(values: tuple[Fraction, ...]) -> Fraction:
        return sum_fn(values, fraction_type(0)) / len_fn(values)

    def profile_checks(q: int) -> tuple:
        vectors = tuple_type(
            tuple_type(delta_value(q, a, h) for h in range_fn(q))
            for a in range_fn(q)
        )
        if any_fn(normalized_mean(row) != 0 for row in vectors):
            raise failure_type("Delta period mean changed")
        for a, row in enumerate_fn(vectors):
            pairing = normalized_mean(
                tuple_type(fraction_type(c_q(q, h)) * row[h] for h in range_fn(q))
            )
            if pairing != delta_value(q, a, 0):
                raise failure_type("Ramanujan pairing changed")
        vector = delta_vector(q)
        if sum_fn(vector, fraction_type(0)) != 0:
            raise failure_type("delta residue sum changed")
        return (
            vector,
            sum_fn((abs_fn(value) for value in vector), fraction_type(0)),
        )

    def cyclic_correlation(
        beta: tuple[Fraction, ...], w: tuple[Fraction, ...]
    ) -> tuple[Fraction, ...]:
        size = len_fn(beta)
        return tuple_type(
            sum_fn(
                (
                    beta[t] * w[(t + h) % size]
                    for t in range_fn(size)
                ),
                fraction_type(0),
            )
            for h in range_fn(size)
        )

    def adjoint_apply(
        kappa: tuple[Fraction, ...], w: tuple[Fraction, ...]
    ) -> tuple[Fraction, ...]:
        size = len_fn(w)
        return tuple_type(
            sum_fn(
                (
                    kappa[h] * w[(t + h) % size]
                    for h in range_fn(size)
                ),
                fraction_type(0),
            )
            for t in range_fn(size)
        )

    def fraction_text(value: Fraction) -> str:
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    def finite_result_items() -> tuple[tuple[str, object], ...]:
        q5, q5_l1 = profile_checks(5)
        q7, q7_l1 = profile_checks(7)
        expected_q5 = (
            fraction_type(0),
            fraction_type(5, 16),
            fraction_type(5, 16),
            fraction_type(-15, 16),
            fraction_type(5, 16),
        )
        expected_q7 = (
            fraction_type(0),
            fraction_type(7, 36),
            fraction_type(7, 36),
            fraction_type(7, 36),
            fraction_type(7, 36),
            fraction_type(-35, 36),
            fraction_type(7, 36),
        )
        if q5 != expected_q5 or q7 != expected_q7:
            raise failure_type("finite delta vector changed")
        if q5_l1 != fraction_type(15, 8) or q7_l1 != fraction_type(35, 18):
            raise failure_type("delta L1 changed")

        qs = (5, 7)
        l_pr = sum_fn((q - 1 for q in qs), 0)
        kernel = tuple_type(
            fraction_type(sum_fn((c_q(q, h) for q in qs), 0), l_pr)
            for h in (0, 1, 5, 7, 35)
        )
        expected_kernel = (
            fraction_type(1),
            fraction_type(-1, 5),
            fraction_type(3, 10),
            fraction_type(1, 2),
            fraction_type(1),
        )
        if kernel != expected_kernel:
            raise failure_type("prime-shell kernel changed")

        diagonal_model = (
            fraction_type(4) * fraction_type(5, 16)
            + fraction_type(6) * fraction_type(7, 36)
        ) / l_pr
        diagonal_residual = fraction_type(10) - diagonal_model
        if diagonal_model != fraction_type(29, 120):
            raise failure_type("q-local diagonal model changed")
        if diagonal_residual != fraction_type(1171, 120):
            raise failure_type("q-local diagonal residual changed")
        if diagonal_model + diagonal_residual != 10:
            raise failure_type("physical diagonal did not reassemble")

        endpoint = fraction_type(399, 400)
        offzero = fraction_type(191, 192)
        qlocal = fraction_type(95, 96)
        bc = fraction_type(1891, 1920)
        boundary = fraction_type(47, 48) + fraction_type(11, 1920)
        if endpoint - offzero != fraction_type(13, 4800):
            raise failure_type("offzero endpoint margin changed")
        if endpoint - qlocal != fraction_type(19, 2400):
            raise failure_type("q-local endpoint margin changed")
        if qlocal - bc != fraction_type(3, 640):
            raise failure_type("q-local/BC gap changed")
        if qlocal - boundary != fraction_type(3, 640):
            raise failure_type("q-local/boundary gap changed")

        beta = tuple_type(map_fn(fraction_type, (1, 2, 0, 1)))
        w = tuple_type(map_fn(fraction_type, (3, -1, 2, 0)))
        kappa = (
            fraction_type(1),
            fraction_type(1, 2),
            fraction_type(1, 3),
            fraction_type(-1, 2),
        )
        r = cyclic_correlation(beta, w)
        tkw = adjoint_apply(kappa, w)
        jr = sum_fn((kappa[h] * r[h] for h in range_fn(4)), fraction_type(0))
        adjoint_pair = sum_fn(
            (beta[t] * tkw[t] for t in range_fn(4)), fraction_type(0)
        )
        if r != tuple_type(map_fn(fraction_type, (1, 6, 1, 8))):
            raise failure_type("cyclic correlation changed")
        expected_tkw = (
            fraction_type(19, 6),
            fraction_type(-3, 2),
            fraction_type(7, 2),
            fraction_type(1, 6),
        )
        if tkw != expected_tkw or jr != fraction_type(1, 3):
            raise failure_type("adjoint fixture changed")
        if jr != adjoint_pair:
            raise failure_type("adjoint identity failed")

        anti_u = (
            fraction_type(4),
            fraction_type(1, 4),
            fraction_type(0),
            fraction_type(0),
        )
        anti_v = (
            fraction_type(1, 4),
            fraction_type(4),
            fraction_type(0),
            fraction_type(0),
        )
        anti_c = tuple_type(anti_u[i] * anti_v[i] for i in range_fn(4))
        if anti_c != tuple_type(map_fn(fraction_type, (1, 1, 0, 0))):
            raise failure_type("anti-spike cross product changed")
        if max_fn(anti_c) != 1 or max_fn(anti_u) != 4 or max_fn(anti_v) != 4:
            raise failure_type("anti-spike strictness changed")

        adaptive_u = tuple_type(map_fn(fraction_type, (4, 0, 0, 0)))
        adaptive_c = tuple_type(value * value for value in adaptive_u)
        if sum_fn(adaptive_c, fraction_type(0)) != 16:
            raise failure_type("adaptive major fixture changed")

        orbit = tuple_type(
            tuple_type(fraction_type(1 if i == j else 0) for i in range_fn(4))
            for j in range_fn(4)
        )
        if len_fn(set_type(orbit)) != 4:
            raise failure_type("translation orbit lost injectivity witness")
        point_kernel = tuple_type(map_fn(fraction_type, (4, 0, 0, 0)))
        point_mean = sum_fn(point_kernel, fraction_type(0)) / 4
        point_kappa = sum_fn((x * x for x in point_kernel), fraction_type(0)) / 4
        point_kappa0 = sum_fn(
            ((x - 1) * (x - 1) for x in point_kernel), fraction_type(0)
        ) / 4
        if (point_mean, point_kappa, point_kappa0) != (
            fraction_type(1),
            fraction_type(4),
            fraction_type(3),
        ):
            raise failure_type("full-coordinate Christoffel fixture changed")

        admissible = (1, 2, 4)
        q5_density = fraction_type(len_fn(admissible), 5)
        q5_factor = q5_density / fraction_type(16, 25)
        q5_kernel = tuple_type(
            fraction_type(5, 3) if value in admissible else fraction_type(0)
            for value in range_fn(5)
        )
        q5_mean = sum_fn(q5_kernel, fraction_type(0)) / 5
        q5_kappa = sum_fn((x * x for x in q5_kernel), fraction_type(0)) / 5
        q5_kappa0 = sum_fn(
            ((x - 1) * (x - 1) for x in q5_kernel), fraction_type(0)
        ) / 5
        if (q5_density, q5_factor, q5_mean, q5_kappa, q5_kappa0) != (
            fraction_type(3, 5),
            fraction_type(15, 16),
            fraction_type(1),
            fraction_type(5, 3),
            fraction_type(2, 3),
        ):
            raise failure_type("q=5 low-Christoffel fixture changed")

        psi_at_zero = fraction_type(3, 4)
        hatpsi_at_zero = fraction_type(1)
        sample_h = 100
        poisson_multiplier = sample_h * psi_at_zero
        wrong_multiplier = sample_h * hatpsi_at_zero
        if poisson_multiplier != 75 or wrong_multiplier != 100:
            raise failure_type("Poisson normalization fixture changed")

        species = (fraction_type(11), fraction_type(-11))
        if sum_fn(species, fraction_type(0)) != 0:
            raise failure_type("joint sign fixture changed")
        if sum_fn((abs_fn(x) for x in species), fraction_type(0)) != 22:
            raise failure_type("specieswise absolute fixture changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("q5_delta", tuple_type(fraction_text(x) for x in q5)),
            ("q7_delta", tuple_type(fraction_text(x) for x in q7)),
            ("q5_delta_l1", fraction_text(q5_l1)),
            ("q7_delta_l1", fraction_text(q7_l1)),
            ("prime_shell_kernel", tuple_type(fraction_text(x) for x in kernel)),
            ("q_local_diagonal_model", fraction_text(diagonal_model)),
            ("q_local_diagonal_residual", fraction_text(diagonal_residual)),
            ("physical_diagonal_reassembly", "10/1"),
            ("q_local_model_exponent", "95/96"),
            ("q_local_margin", "19/2400"),
            ("offzero_margin", "13/4800"),
            ("boundary_gap", "3/640"),
            ("local_BC_gap", "3/640"),
            ("adjoint_r", tuple_type(fraction_text(x) for x in r)),
            ("adjoint_Tkw", tuple_type(fraction_text(x) for x in tkw)),
            ("adjoint_J", fraction_text(jr)),
            ("adjoint_pair", fraction_text(adjoint_pair)),
            ("cell_Y", 2),
            ("cell_count", 4),
            ("window_cell_overlap", 3),
            ("anti_spike_u", tuple_type(fraction_text(x) for x in anti_u)),
            ("anti_spike_v", tuple_type(fraction_text(x) for x in anti_v)),
            ("anti_spike_c", tuple_type(fraction_text(x) for x in anti_c)),
            ("anti_spike_cross_max", "1/1"),
            ("anti_spike_marginal_max", "4/1"),
            ("adaptive_major_absorbed", "16/1"),
            ("adaptive_minor_after_excision", "0/1"),
            ("translation_orbit_rank", 4),
            ("full_coordinate_kappa", "4/1"),
            ("full_coordinate_kappa0", "3/1"),
            ("q5_admissible", admissible),
            ("q5_density", fraction_text(q5_density)),
            ("q5_singular_factor", fraction_text(q5_factor)),
            ("q5_kernel_mean", fraction_text(q5_mean)),
            ("q5_kernel_kappa", fraction_text(q5_kappa)),
            ("q5_kernel_kappa0", fraction_text(q5_kappa0)),
            ("q5_zero_target", "0/1"),
            ("poisson_multiplier", fraction_text(poisson_multiplier)),
            ("wrong_hatpsi_multiplier", fraction_text(wrong_multiplier)),
            ("one_outer_absolute_joint", "0/1"),
            ("specieswise_absolute", "22/1"),
            ("selected_route", "B_THEN_A_THEN_C"),
            ("arithmetic_advance", False),
            ("fixed_atom_credit", 0),
            ("strict_1_over_400", "UNPAID"),
            ("L2", "NONE"),
            ("TPC_207_TRIGGER", False),
            ("numbered_release", "NO"),
        )

    mutation_labels: list[str] = []

    def must_reject(label: str, action) -> None:
        try:
            action()
        except failure_type:
            mutation_labels.append(label)
            return
        raise failure_type("mutation accepted: " + label)

    def mutated_value(value: object) -> object:
        if exact_bool(value):
            return not value
        if exact_int(value):
            return value + 1
        if exact_str(value):
            return value + "_MUTATED"
        if type_fn(value) is tuple_type:
            return value + ("MUTATED",)
        raise failure_type("unsupported mutation type")

    def wrong_type(value: object) -> object:
        if exact_bool(value):
            return 1 if value else 0
        if exact_int(value):
            return str_type(value)
        if exact_str(value):
            return (value,)
        if type_fn(value) is tuple_type:
            return list_type(value)
        raise failure_type("unsupported wrong type")

    def mapping_mutations(expected: tuple, validator, prefix: str, triple: bool) -> int:
        for index, (key, value) in enumerate_fn(expected):
            changed = dict_type(expected)
            changed[key] = mutated_value(value)
            must_reject(
                prefix + "_value_" + str_type(index + 1),
                lambda c=changed: validator(c),
            )
            changed_key = list_type(expected)
            changed_key[index] = (key + "_MUTATED", value)
            must_reject(
                prefix + "_key_" + str_type(index + 1),
                lambda c=dict_type(changed_key): validator(c),
            )
            if triple:
                changed_type = dict_type(expected)
                changed_type[key] = wrong_type(value)
                must_reject(
                    prefix + "_type_" + str_type(index + 1),
                    lambda c=changed_type: validator(c),
                )
        must_reject(prefix + "_wrong_outer", lambda: validator(list_type(expected)))

        class StringImpostor(str):
            pass

        impostor = dict_type(expected)
        first_key, first_value = expected[0]
        del impostor[first_key]
        impostor[StringImpostor(first_key)] = first_value
        must_reject(prefix + "_key_subclass", lambda: validator(impostor))
        return (3 if triple else 2) * len_fn(expected) + 2

    def pair_mutations(expected: tuple, validator, prefix: str, digest_mode: bool) -> int:
        for index, (key, value) in enumerate_fn(expected):
            rows = list_type(expected)
            rows[index] = (key, value + "_MUTATED")
            candidate = tuple_type(rows)
            if digest_mode:
                must_reject(
                    prefix + "_value_" + str_type(index + 1),
                    lambda c=candidate: validator(c, registry_digest(c)),
                )
            else:
                must_reject(
                    prefix + "_value_" + str_type(index + 1),
                    lambda c=candidate: validator(c),
                )
            rows = list_type(expected)
            rows[index] = (key + "_MUTATED", value)
            candidate = tuple_type(rows)
            if digest_mode:
                must_reject(
                    prefix + "_key_" + str_type(index + 1),
                    lambda c=candidate: validator(c, registry_digest(c)),
                )
            else:
                must_reject(
                    prefix + "_key_" + str_type(index + 1),
                    lambda c=candidate: validator(c),
                )
        if digest_mode:
            must_reject(
                prefix + "_wrong_outer",
                lambda: validator(list_type(expected), literal_registry_digest),
            )
            must_reject(
                prefix + "_false_digest",
                lambda: validator(expected, "0" * 64),
            )
        else:
            must_reject(prefix + "_wrong_outer", lambda: validator(list_type(expected)))

        class StringImpostor(str):
            pass

        rows = list_type(expected)
        rows[0] = (StringImpostor(rows[0][0]), rows[0][1])
        if digest_mode:
            must_reject(
                prefix + "_string_subclass",
                lambda: validator(tuple_type(rows), literal_registry_digest),
            )
            return 2 * len_fn(expected) + 3
        must_reject(
            prefix + "_string_subclass",
            lambda: validator(tuple_type(rows)),
        )
        return 2 * len_fn(expected) + 2

    def validate_base_result(candidate: object, expected: tuple) -> None:
        require_exact_mapping(candidate, expected, "result")

    def run() -> dict[str, object]:
        mutation_labels.clear()
        validate_contract(dict_type(literal_contract))
        validate_registry(literal_registry, literal_registry_digest)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)
        base = finite_result_items()
        validate_base_result(dict_type(base), base)

        contract_count = mapping_mutations(
            literal_contract, validate_contract, "contract", False
        )
        registry_count = pair_mutations(
            literal_registry, validate_registry, "registry", True
        )
        source_count = pair_mutations(
            literal_sources, validate_sources, "source", False
        )
        dependency_count = pair_mutations(
            literal_dependencies, validate_dependencies, "dependency", False
        )
        result_count = mapping_mutations(
            base,
            lambda candidate: validate_base_result(candidate, base),
            "result",
            True,
        )
        expected_actions = (
            contract_count
            + registry_count
            + source_count
            + dependency_count
            + result_count
        )
        if len_fn(mutation_labels) != expected_actions:
            raise failure_type("mutation action count changed")
        if len_fn(set_type(mutation_labels)) != expected_actions:
            raise failure_type("mutation labels not unique")

        full = base + (
            ("contract_fields", len_fn(literal_contract)),
            ("registry_rows", len_fn(literal_registry)),
            ("source_locks", len_fn(literal_sources)),
            ("dependency_locks", len_fn(literal_dependencies)),
            ("registry_sha256", literal_registry_digest),
            ("contract_mutations", contract_count),
            ("registry_mutations", registry_count),
            ("source_mutations", source_count),
            ("dependency_mutations", dependency_count),
            ("result_mutations", result_count),
            ("mutation_actions", expected_actions),
        )
        require_exact_mapping(dict_type(full), full, "full result")
        return dict_type(full)

    return run


def _make_main(
    runner,
    baseline_items,
    frozen_stdout,
    writer=sys.stdout.write,
    tuple_type=tuple,
    str_type=str,
    type_fn=type,
    len_fn=len,
    failure_type=CheckFailure,
):
    literal_baseline = tuple_type(baseline_items)
    literal_stdout = frozen_stdout

    def sealed(*argv_objects) -> int:
        if len_fn(argv_objects) != 1:
            raise failure_type("explicit --check is required")
        argv = argv_objects[0]
        if type_fn(argv) is not tuple_type:
            raise failure_type("explicit --check is required")
        if len_fn(argv) != 1 or type_fn(argv[0]) is not str_type:
            raise failure_type("explicit --check is required")
        if argv != ("--check",):
            raise failure_type("explicit --check is required")
        result = runner()
        if tuple_type(result.items()) != literal_baseline:
            raise failure_type("sealed result changed")
        writer(literal_stdout + "\n")
        return 0

    return sealed


_TRUSTED_RUN = _make_trusted_runner()
run_check = _TRUSTED_RUN
_BASELINE_RESULT = _TRUSTED_RUN()
_FROZEN_STDOUT = json.dumps(
    _BASELINE_RESULT, sort_keys=True, separators=(",", ":")
)
main = _make_main(
    _TRUSTED_RUN,
    tuple(_BASELINE_RESULT.items()),
    _FROZEN_STDOUT,
)
del _BASELINE_RESULT


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
