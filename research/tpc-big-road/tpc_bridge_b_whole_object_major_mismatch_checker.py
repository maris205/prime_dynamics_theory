#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V31 whole-object compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_WHOLE_OBJECT_MODEL_LEVEL_MAJOR_ATTACHMENT_COMPILER_PLUS_"
    "CONDITIONAL_ENDPOINT_BUDGET_PLUS_EQUIVARIANT_QUOTIENT_NO_GO"
)


CONTRACT_ITEMS = (
    ("schema_version", "V31_WHOLE_OBJECT_COMPILER_V1"),
    ("artifact_name", "bridge_b_whole_object_major_mismatch_and_terminal_compiler.md"),
    ("baseline_commit", "7ec9b911df84b53bef9adc90e547cae153325978"),
    ("maximum_claim", MAXIMUM_CLAIM),
    ("selected_route", "B_THEN_A_THEN_C"),
    ("arithmetic_advance", False),
    ("fixed_atom_credit", 0),
    ("strict_1_over_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", False),
    ("numbered_release", "NO"),
    ("measure_normalization", "NORMALIZED_HAAR_ON_T"),
    ("fourier_coefficient_sign", "hat_f(h)=int_f(alpha)e(+h*alpha)dalpha"),
    ("P_definition", "P=B*conjugate(W)"),
    ("r_coefficient_identity", "r(h)=hat_P(h)"),
    ("L_definition", "L=sum_h_Mloc(h)e(-h*alpha)"),
    ("Mloc_coefficient_identity", "Mloc(h)=hat_L(h)"),
    ("Mloc_zero", 0),
    ("lambda_definition", "lambda=x^(1+nu)"),
    ("nu_range", "0<nu<13/4800"),
    ("model_major_definition", "M_lambda={abs(L)>lambda}"),
    ("major_predeclaration", "MODEL_ONLY_BEFORE_MISMATCH_AND_CELLS"),
    ("minor_complement", "m_lambda=T\\M_lambda_INCLUDES_EQUALITY"),
    ("MT_definition", "MT=hat(1_M*P)"),
    ("a_definition", "a=hat(1_M*P-L)"),
    ("n_definition", "n=hat(1_m*P)"),
    ("attachment_identity", "MT=Mloc+a"),
    ("residual_identity", "e=n+a"),
    ("axis_identity", "S=e(0)=n(0)+a(0)"),
    ("parseval_identity", "norm2(a)=major_mismatch+minor_model_energy"),
    ("major_mismatch_definition", "D_lambda=int_M_abs(P-L)^2"),
    ("major_mismatch_bound", "OPEN_x^(2+2nu+o(1))"),
    ("minor_model_bound", "int_m_abs(L)^2<=lambda^2"),
    ("weighted_a_bound", "OPEN_x^(1+nu+o(1))"),
    ("cell_partition", "2Y_HALF_OPEN_CELLS"),
    ("cell_product", "c_j=norm2_Ijcapm(B)*norm2_Ijcapm(W)"),
    ("global_c_bound", "ell1(c)<=x^(1+o(1))"),
    ("local_c_bound", "OPEN_ellinf(c)<=x^(1+2sigma_c+o(1))/Y"),
    ("MRT_reduction", "sum_window_abs(n)^2<=3Y*ell1(c)*ellinf(c)"),
    ("sigma_B", "max(nu,sigma_c)"),
    ("B_endpoint_condition", "sigma_B<13/4800"),
    ("E_margin", "13/4800-sigma_B"),
    ("qlocal_model_gap", "19/2400"),
    ("terminal_R_gate", "OPEN_eta_R>0"),
    ("eta_star_formula", "min(eta_R,19/2400,13/4800-sigma_B)"),
    ("large_spectrum_variant", "SCOPED_W_DEPENDENT_ZERO_CREDIT"),
    ("first_fatal", "MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_FOR_LITERAL_P_MINUS_L"),
    ("provenance_requirement", "ONE_LITERAL_TAGGED_OBJECT_ONE_OUTER_NORM"),
)


REGISTRY_ITEMS = (
    ("V31_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V31_ROUTE_ADVANCE", "YES"),
    ("V31_ARITHMETIC_ADVANCE", "NO"),
    ("V31_FIXED_ATOM_CREDIT", "0"),
    ("V31_STRICT_1_OVER_400", "UNPAID"),
    ("V31_L2", "NONE"),
    ("V31_TPC_207_TRIGGER", "false"),
    ("V31_NUMBERED_RELEASE", "NO"),
    (
        "V31_SELECTED_RESEARCH_ROUTE",
        "B_MODEL_MAJOR_MISMATCH_AND_MINOR_CROSS_FLATNESS_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK",
    ),
    (
        "V31_WHOLE_OBJECT_SPACE",
        "SAME_LITERAL_TAGGED_P_EQUALS_B_TIMES_WBAR_AND_OCCURRENCE_NATIVE_MLOC",
    ),
    ("V31_FOURIER_COEFFICIENT_CONVENTION", "PROVED_EXACT_PLUS_H_COEFFICIENT"),
    ("V31_MODEL_SPECTRUM", "L_X_EQUALS_SUM_H_MLOC_H_E_MINUS_H_ALPHA"),
    ("V31_MODEL_ONLY_LEVEL_MAJOR", "PROVED_EXACT_PREDECLARED_FROM_FROZEN_MODEL"),
    ("V31_MAJOR_PREDECLARATION", "REQUIRED_BEFORE_MISMATCH_OR_CELL_INSPECTION"),
    ("V31_MT_DEFINITION", "MT_M_H_EQUALS_HAT_OF_ONE_M_P_H"),
    ("V31_ATTACHMENT_IDENTITY", "PROVED_EXACT_MT_EQUALS_MLOC_PLUS_A"),
    (
        "V31_ATTACHMENT_PARSEVAL_IDENTITY",
        "PROVED_EXACT_MAJOR_MISMATCH_PLUS_MINOR_MODEL_ENERGY",
    ),
    ("V31_MAJOR_MISMATCH_ENERGY", "SELECTED_PRIMARY_OPEN_NEW_THEOREM"),
    ("V31_ACTUAL_ATTACHMENT_BOUND", "OPEN_X_1_PLUS_NU_WITH_NU_BELOW_13_OVER_4800"),
    ("V31_MINOR_COEFFICIENT_IDENTITY", "PROVED_EXACT_E_EQUALS_N_PLUS_A"),
    (
        "V31_MRT_PRODUCT_LOCAL_REDUCTION",
        "SOURCE_BACKED_REDUCTION_ONLY_PROP_3_1_EQ_54",
    ),
    ("V31_CELL_PRODUCT_COMPILER", "PROVED_EXACT_3Y_L1_LINF"),
    ("V31_CELL_L1_GLOBAL_BOUND", "PROVED_ELEMENTARY_X_1_PLUS_O1"),
    ("V31_CELL_LINF_CROSS_FLATNESS", "OPEN_ACTUAL_TAGGED_UNIFORM_THEOREM"),
    ("V31_B_AGGREGATE_EXPONENT", "PROVED_EXACT_SIGMA_B_EQUALS_MAX_NU_SIGMA_C"),
    ("V31_B_ENDPOINT_CONDITION", "SIGMA_B_STRICTLY_LESS_THAN_13_OVER_4800"),
    (
        "V31_FORMULA_PREDECLARED_LARGE_SPECTRUM",
        "SURVIVES_SCOPED_W_DEPENDENT_ZERO_CREDIT",
    ),
    (
        "V31_FORMULA_PREDECLARED_MINOR_FLATNESS",
        "PROVED_EXACT_POINTWISE_THRESHOLD_COMPILER",
    ),
    ("V31_ZERO_AXIS_REASSEMBLY", "PROVED_EXACT_S_EQUALS_N_ZERO_PLUS_A_ZERO"),
    (
        "V31_OFFZERO_B_ALONE",
        "STOP_SCOPED_AXIS_SURVIVES_ATTACHMENT_AND_MINOR_SPLIT",
    ),
    ("V31_QLOCAL_MODEL_BOUND", "PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1"),
    ("V31_A_TERMINAL_COVARIANCE", "SELECTED_TERMINAL_OPEN_NEW_THEOREM"),
    (
        "V31_A_B_TERMINAL_EQUIVALENCE",
        "PROVED_EXACT_AFTER_B_STRICT_EXPONENT_CLASS",
    ),
    ("V31_WHOLE_OBJECT_CLOSURE_THEOREM", "PROVED_EXACT_CONDITIONAL_ETA_STAR"),
    (
        "V31_ENDPOINT_MARGIN_FORMULA",
        "MIN_ETA_R_19_OVER_2400_13_OVER_4800_MINUS_SIGMA_B",
    ),
    (
        "V31_C_EQUIVARIANT_WHOLE_SHELL_QUOTIENT",
        "STOP_SCOPED_TRANSLATION_INVARIANCE_FORCES_INJECTIVITY",
    ),
    ("V31_C_FULL_COORDINATE_CHRISTOFFEL", "PROVED_EXACT_KAPPA_N_KAPPA0_N_MINUS_1"),
    (
        "V31_Q5_GAP2_LOCAL_DENSITY_KERNEL",
        "PROVED_EXACT_FINITE_LOW_CHRISTOFFEL_CARRIER",
    ),
    (
        "V31_Q5_TO_PHYSICAL_POSITIVE_MAIN",
        "STOP_SCOPED_LOCAL_ADMISSIBILITY_DOES_NOT_FORCE_PRIME_MASS",
    ),
    ("V31_FIXED_HARD_SET_ALONE", "STOP_SCOPED_MAJOR_MINOR_MASS_RELOCATION"),
    (
        "V31_MRT_APPLIED_MAJOR_ATTACHMENT",
        "STOP_SCOPED_STANDARD_LAMBDA_DK_OBJECTS_NOT_LITERAL_MASTER",
    ),
    (
        "V31_MRSTT_NILSEQUENCE_ATTACHMENT",
        "STOP_SCOPED_WRONG_PROXY_PAIR_FIXED_COMPLEXITY_AND_LOGARITHMIC_SAVING",
    ),
    ("V31_DIRECT_PRIMARY_SOURCE_ATTACHMENT", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08"),
    (
        "V31_NEXT_THEOREM",
        "MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_AND_MINOR_CROSS_FLATNESS_AT_COMMON_SIGMA_BELOW_13_OVER_4800",
    ),
    ("V31_FIRST_FATAL", "MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_FOR_LITERAL_P_MINUS_L"),
    ("V31_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
    ("V31_PROVENANCE_CASCADE", "REQUIRED"),
)


EXPECTED_REGISTRY_SHA256 = "bef0ac26480b783626dfdba126d8c62d70a15d2528a92a4d66f2a1b63287a980"


SOURCE_ITEMS = (
    ("MRT_ABSTRACT_PRODUCT", "arXiv:1707.01315v3_Proposition_3.1_equation_54"),
    ("MRT_APPLIED_BOUNDARY", "arXiv:1707.01315v3_Propositions_3.3_3.4"),
    ("MSTT_PROXY_BOUNDARY", "arXiv:2204.03754v4_Theorem_1.1"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_terminal_major_cross_flatness_and_equivariant_quotient.md",
        "5c3d59e3b324a8c67109566c5e54dd3d3fc381b295b2c6cce15c49762ea4bbf6",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_terminal_major_cross_flatness_checker.py",
        "662dbe9259f8a6176894711d692470608115b9df89f255e6c53dbd493e11cfcf",
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
    range_fn=range,
    sum_fn=sum,
    max_fn=max,
    min_fn=min,
    abs_fn=abs,
    all_fn=all,
    any_fn=any,
    enumerate_fn=enumerate,
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
    if dict_type(literal_registry).get("V31_MAXIMUM_CLAIM") != literal_maximum_claim:
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
        return b"".join((key + "=" + value + "\n").encode("utf-8") for key, value in candidate)

    def registry_digest(candidate: tuple[tuple[str, str], ...]) -> str:
        return digest_bytes(registry_bytes(candidate))

    def require_pairs(candidate: object, expected: tuple, label: str) -> None:
        if type_fn(candidate) is not tuple_type or len_fn(candidate) != len_fn(expected):
            raise failure_type(label + " shape changed")
        for row in candidate:
            if type_fn(row) is not tuple_type or len_fn(row) != 2:
                raise failure_type(label + " row shape changed")
            if not exact_str(row[0]) or not exact_str(row[1]):
                raise failure_type(label + " row type changed")
        if len_fn(set_type(key for key, _ in candidate)) != len_fn(candidate):
            raise failure_type(label + " keys not unique")
        if candidate != expected:
            raise failure_type(label + " semantic promotion")

    def require_mapping(candidate: object, expected: tuple, label: str) -> None:
        if type_fn(candidate) is not dict_type:
            raise failure_type(label + " outer type changed")
        if not all_fn(type_fn(key) is str_type for key in candidate):
            raise failure_type(label + " key type changed")
        expected_map = dict_type(expected)
        if set_type(candidate) != set_type(expected_map):
            raise failure_type(label + " key set changed")
        for key, value in expected:
            if type_fn(candidate[key]) is not type_fn(value) or candidate[key] != value:
                raise failure_type(label + " value changed at " + key)

    def validate_contract(candidate: object) -> None:
        require_mapping(candidate, literal_contract, "contract")

    def validate_registry(candidate: object, claimed_digest: object) -> None:
        require_pairs(candidate, literal_registry, "registry")
        if not exact_str(claimed_digest) or claimed_digest != literal_registry_digest:
            raise failure_type("registry digest changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry content digest changed")

    def validate_sources(candidate: object) -> None:
        require_pairs(candidate, literal_sources, "source")

    def validate_dependencies(candidate: object) -> None:
        require_pairs(candidate, literal_dependencies, "dependency")
        for relative, expected_hash in candidate:
            path = repo_root / relative
            if not path_is_file(path):
                raise failure_type("dependency missing: " + relative)
            actual = digest_bytes(canonical_bytes(path_read_bytes(path)))
            if actual != expected_hash:
                raise failure_type("dependency hash changed: " + relative)

    def c_add(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def c_sub(a, b):
        return (a[0] - b[0], a[1] - b[1])

    def c_mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def c_abs2(a):
        return a[0] * a[0] + a[1] * a[1]

    def dft4(values):
        roots = (
            (fraction_type(1), fraction_type(0)),
            (fraction_type(0), fraction_type(1)),
            (fraction_type(-1), fraction_type(0)),
            (fraction_type(0), fraction_type(-1)),
        )
        out = list_type()
        for h in range_fn(4):
            total = (fraction_type(0), fraction_type(0))
            for j in range_fn(4):
                total = c_add(total, c_mul((fraction_type(values[j]), fraction_type(0)), roots[(h * j) % 4]))
            out.append((total[0] / 4, total[1] / 4))
        return tuple_type(out)

    def ftext(value: Fraction) -> str:
        return str_type(value.numerator) + "/" + str_type(value.denominator)

    def ctext(value) -> str:
        return ftext(value[0]) + ("+" if value[1] >= 0 else "") + ftext(value[1]) + "i"

    def finite_items() -> tuple[tuple[str, object], ...]:
        p = (5, 1, -1, 3)
        ell = (2, 1, -2, -1)
        major = (1, 0, 1, 0)
        minor = (0, 1, 0, 1)
        r = dft4(p)
        mloc = dft4(ell)
        mt = dft4(tuple_type(p[i] * major[i] for i in range_fn(4)))
        a = dft4(tuple_type(p[i] * major[i] - ell[i] for i in range_fn(4)))
        n = dft4(tuple_type(p[i] * minor[i] for i in range_fn(4)))
        e = dft4(tuple_type(p[i] - ell[i] for i in range_fn(4)))
        wrong_a = dft4(tuple_type(major[i] * (p[i] - ell[i]) for i in range_fn(4)))
        if any_fn(c_add(mloc[i], a[i]) != mt[i] for i in range_fn(4)):
            raise failure_type("attachment identity failed")
        if any_fn(c_add(n[i], a[i]) != e[i] for i in range_fn(4)):
            raise failure_type("residual identity failed")
        if a == wrong_a:
            raise failure_type("parenthesis mutation survived")
        if (r[0], mloc[0], mt[0], a[0], n[0], e[0]) != (
            (fraction_type(2), fraction_type(0)),
            (fraction_type(0), fraction_type(0)),
            (fraction_type(1), fraction_type(0)),
            (fraction_type(1), fraction_type(0)),
            (fraction_type(1), fraction_type(0)),
            (fraction_type(2), fraction_type(0)),
        ):
            raise failure_type("zero-axis fixture changed")
        major_mismatch = sum_fn((fraction_type((p[i] - ell[i]) ** 2, 4) for i in (0, 2)), fraction_type(0))
        minor_leak = sum_fn((fraction_type(ell[i] ** 2, 4) for i in (1, 3)), fraction_type(0))
        a_norm = sum_fn((c_abs2(z) for z in a), fraction_type(0))
        if (major_mismatch, minor_leak, a_norm) != (
            fraction_type(5, 2), fraction_type(1, 2), fraction_type(3)
        ):
            raise failure_type("Parseval fixture changed")
        if a_norm != major_mismatch + minor_leak:
            raise failure_type("Parseval did not reassemble")

        nu = fraction_type(1, 2400)
        sigma_c = fraction_type(1, 4800)
        sigma_b = max_fn(nu, sigma_c)
        eta_r = fraction_type(1, 600)
        e_margin = fraction_type(13, 4800) - sigma_b
        eta_star = min_fn(eta_r, fraction_type(19, 2400), e_margin)
        if (sigma_b, e_margin, eta_star) != (
            fraction_type(1, 2400), fraction_type(11, 4800), fraction_type(1, 600)
        ):
            raise failure_type("endpoint budget changed")
        if max_fn(fraction_type(13, 4800), sigma_b) == sigma_b:
            raise failure_type("strict endpoint lost")

        threshold = fraction_type(4)
        cell_measure = fraction_type(1, 8)
        pointwise_cell_product = threshold * threshold * cell_measure
        if pointwise_cell_product != fraction_type(2):
            raise failure_type("large-spectrum cell compiler changed")

        fixed_major = (4, 0, 0, 0)
        fixed_minor = (0, 2, 0, 2)
        if sum_fn(fixed_major, 0) / 4 != 1 or sum_fn(fixed_minor, 0) / 4 != 1:
            raise failure_type("fixed hard-set no-go changed")

        point_kernel = (fraction_type(4), fraction_type(0), fraction_type(0), fraction_type(0))
        kappa = sum_fn((x * x for x in point_kernel), fraction_type(0)) / 4
        kappa0 = sum_fn(((x - 1) * (x - 1) for x in point_kernel), fraction_type(0)) / 4
        if (kappa, kappa0) != (fraction_type(4), fraction_type(3)):
            raise failure_type("equivariant quotient fixture changed")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("P", p),
            ("L", ell),
            ("major_mask", major),
            ("minor_mask", minor),
            ("r", tuple_type(ctext(z) for z in r)),
            ("Mloc", tuple_type(ctext(z) for z in mloc)),
            ("MT", tuple_type(ctext(z) for z in mt)),
            ("a", tuple_type(ctext(z) for z in a)),
            ("n", tuple_type(ctext(z) for z in n)),
            ("e", tuple_type(ctext(z) for z in e)),
            ("major_mismatch", ftext(major_mismatch)),
            ("minor_model_leak", ftext(minor_leak)),
            ("a_norm_squared", ftext(a_norm)),
            ("S", ftext(e[0][0])),
            ("a_zero", ftext(a[0][0])),
            ("n_zero", ftext(n[0][0])),
            ("nu", ftext(nu)),
            ("sigma_c", ftext(sigma_c)),
            ("sigma_B", ftext(sigma_b)),
            ("E_margin", ftext(e_margin)),
            ("eta_R", ftext(eta_r)),
            ("eta_star", ftext(eta_star)),
            ("large_spectrum_cell_product", ftext(pointwise_cell_product)),
            ("fixed_major_target", "1/1"),
            ("fixed_minor_target", "1/1"),
            ("full_coordinate_kappa", ftext(kappa)),
            ("full_coordinate_kappa0", ftext(kappa0)),
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

    def mutated(value: object) -> object:
        if exact_bool(value):
            return not value
        if exact_int(value):
            return value + 1
        if exact_str(value):
            return value + "_MUTATED"
        if type_fn(value) is tuple_type:
            return value + ("MUTATED",)
        raise failure_type("unsupported mutation value")

    def wrong_type(value: object) -> object:
        if exact_bool(value):
            return 1 if value else 0
        if exact_int(value):
            return str_type(value)
        if exact_str(value):
            return (value,)
        if type_fn(value) is tuple_type:
            return list_type(value)
        raise failure_type("unsupported mutation type")

    def mapping_mutations(expected: tuple, validator, prefix: str, types: bool) -> int:
        for index, (key, value) in enumerate_fn(expected):
            changed = dict_type(expected)
            changed[key] = mutated(value)
            must_reject(prefix + "_value_" + str_type(index), lambda c=changed: validator(c))
            rows = list_type(expected)
            rows[index] = (key + "_MUTATED", value)
            must_reject(prefix + "_key_" + str_type(index), lambda c=dict_type(rows): validator(c))
            if types:
                changed_type = dict_type(expected)
                changed_type[key] = wrong_type(value)
                must_reject(prefix + "_type_" + str_type(index), lambda c=changed_type: validator(c))
        must_reject(prefix + "_outer", lambda: validator(list_type(expected)))

        class StringImpostor(str_type):
            pass

        impostor = dict_type(expected)
        first_key, first_value = expected[0]
        del impostor[first_key]
        impostor[StringImpostor(first_key)] = first_value
        must_reject(prefix + "_key_subclass", lambda: validator(impostor))
        return (3 if types else 2) * len_fn(expected) + 2

    def pair_mutations(expected: tuple, validator, prefix: str, digest_mode: bool) -> int:
        for index, (key, value) in enumerate_fn(expected):
            rows = list_type(expected)
            rows[index] = (key, value + "_MUTATED")
            candidate = tuple_type(rows)
            if digest_mode:
                must_reject(prefix + "_value_" + str_type(index), lambda c=candidate: validator(c, registry_digest(c)))
            else:
                must_reject(prefix + "_value_" + str_type(index), lambda c=candidate: validator(c))
            rows = list_type(expected)
            rows[index] = (key + "_MUTATED", value)
            candidate = tuple_type(rows)
            if digest_mode:
                must_reject(prefix + "_key_" + str_type(index), lambda c=candidate: validator(c, registry_digest(c)))
            else:
                must_reject(prefix + "_key_" + str_type(index), lambda c=candidate: validator(c))
        if digest_mode:
            must_reject(prefix + "_outer", lambda: validator(list_type(expected), literal_registry_digest))
            must_reject(prefix + "_digest", lambda: validator(expected, "0" * 64))
        else:
            must_reject(prefix + "_outer", lambda: validator(list_type(expected)))

        class StringImpostor(str_type):
            pass

        rows = list_type(expected)
        rows[0] = (StringImpostor(rows[0][0]), rows[0][1])
        if digest_mode:
            must_reject(prefix + "_subclass", lambda: validator(tuple_type(rows), literal_registry_digest))
            return 2 * len_fn(expected) + 3
        must_reject(prefix + "_subclass", lambda: validator(tuple_type(rows)))
        return 2 * len_fn(expected) + 2

    def run() -> dict[str, object]:
        mutation_labels.clear()
        validate_contract(dict_type(literal_contract))
        validate_registry(literal_registry, literal_registry_digest)
        validate_sources(literal_sources)
        validate_dependencies(literal_dependencies)
        base = finite_items()
        require_mapping(dict_type(base), base, "result")
        contract_count = mapping_mutations(literal_contract, validate_contract, "contract", False)
        registry_count = pair_mutations(literal_registry, validate_registry, "registry", True)
        source_count = pair_mutations(literal_sources, validate_sources, "source", False)
        dependency_count = pair_mutations(literal_dependencies, validate_dependencies, "dependency", False)
        result_count = mapping_mutations(base, lambda c: require_mapping(c, base, "result"), "result", True)
        actions = contract_count + registry_count + source_count + dependency_count + result_count
        if len_fn(mutation_labels) != actions or len_fn(set_type(mutation_labels)) != actions:
            raise failure_type("mutation ledger changed")
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
            ("mutation_actions", actions),
        )
        require_mapping(dict_type(full), full, "full result")
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
        if len_fn(argv) != 1 or type_fn(argv[0]) is not str_type or argv != ("--check",):
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
_FROZEN_STDOUT = json.dumps(_BASELINE_RESULT, sort_keys=True, separators=(",", ":"))
main = _make_main(_TRUSTED_RUN, tuple(_BASELINE_RESULT.items()), _FROZEN_STDOUT)
del _BASELINE_RESULT


if __name__ == "__main__":
    try:
        raise SystemExit(main(tuple(sys.argv[1:])))
    except CheckFailure as exc:
        sys.stderr.write("CheckFailure: " + str(exc) + "\n")
        raise SystemExit(1)
