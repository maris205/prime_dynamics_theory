#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V32 residual compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


MAXIMUM_CLAIM = (
    "EXACT_SINGLE_SCALE_ZERO_AXIS_QUOTIENTED_WIENER_CELL_COMPILER_"
    "FOR_THE_LITERAL_WHOLE_RESIDUAL"
)


CONTRACT_ITEMS = (
    ("schema_version", "V32_RESIDUAL_OSCILLATION_COMPILER_V1"),
    ("artifact_name", "bridge_b_base_scale_residual_oscillation_compiler.md"),
    ("baseline_commit", "e08b1c04e0ebb92867d5a4370e4d245de2185965"),
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
    ("L_definition", "L=sum_h_Mloc(h)e(-h*alpha)"),
    ("Mloc_zero", 0),
    ("R_definition", "R=P-L"),
    ("residual_coefficient_identity", "hat_R(h)=e(h)=r(h)-Mloc(h)"),
    ("axis_identity", "S=e(0)=hat_R(0)"),
    ("occurrence_emitter", "MASTER_MASKED_PLUS2_MINUS1_MOBIUS_LOG_W_MINUS_DELTA"),
    ("base_scale", "Y0=smallest_dyadic_with_H<=Y0<2H"),
    ("cell_partition", "2Y_ALIGNED_HALF_OPEN_CELLS"),
    ("cell_mass", "q_Yj(c)=int_Ij_abs(R-c)"),
    ("oscillation_functional", "Qosc_Y=inf_c_Y_sum_j_q_Yj(c)^2"),
    ("constant_scope", "ONE_GLOBAL_COMPLEX_CONSTANT_PER_SCALE"),
    ("translation_invariance", "Qosc(R+C)=Qosc(R)"),
    ("infimum_status", "ATTAINED_BY_CONTINUITY_AND_COERCIVITY"),
    ("fejer_constant", 16),
    ("band_bound", "sum_0<abs(h)<=Y_abs(e(h))^2<=16*Qosc_Y"),
    ("refinement_bound", "Qosc_2Y<=2*Qosc_Y"),
    ("schwartz_reassembly", "ONE_BASE_SCALE_CONTROLS_ALL_PHYSICAL_SHELLS"),
    ("oscillation_bound", "OPEN_Qosc_Y0<=x^(2+2sigma+o(1))"),
    ("sigma_range", "0<=sigma<13/4800"),
    ("weighted_residual_bound", "CONDITIONAL_x^(1+sigma+o(1))"),
    ("E_exponent", "191/192+sigma"),
    ("E_margin", "13/4800-sigma"),
    ("V31_implication", "D_lambda_PLUS_CELL_CROSS_FLATNESS_IMPLIES_Qosc"),
    ("converse_status", "FALSE_BY_DISJOINT_FACTORS_AND_NARROW_SPIKE"),
    ("qlocal_model_gap", "19/2400"),
    ("terminal_R_gate", "OPEN_eta_R>0"),
    ("eta_star_formula", "min(eta_R,19/2400,13/4800-sigma)"),
    ("first_fatal", "BASE_SCALE_COLLECTIVE_OSCILLATION_BOUND_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER"),
    ("provenance_requirement", "ONE_LITERAL_TAGGED_OBJECT_ONE_OUTER_NORM"),
)


REGISTRY_ITEMS = (
    ("V32_MAXIMUM_CLAIM", MAXIMUM_CLAIM),
    ("V32_ROUTE_ADVANCE", "YES"),
    ("V32_ARITHMETIC_ADVANCE", "NO"),
    ("V32_FIXED_ATOM_CREDIT", "0"),
    ("V32_STRICT_1_OVER_400", "UNPAID"),
    ("V32_L2", "NONE"),
    ("V32_TPC_207_TRIGGER", "false"),
    ("V32_NUMBERED_RELEASE", "NO"),
    ("V32_SELECTED_RESEARCH_ROUTE", "B_SINGLE_SCALE_RESIDUAL_OSCILLATION_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK"),
    ("V32_WHOLE_OBJECT_SPACE", "SAME_LITERAL_TAGGED_P_MINUS_OCCURRENCE_NATIVE_L"),
    ("V32_LITERAL_OCCURRENCE_EMITTER", "PROVED_EXACT_MASTER_MASKED_PLUS2_MINUS1_MOBIUS_LOG_HYBRID_FORM"),
    ("V32_FOURIER_COEFFICIENT_IDENTITY", "PROVED_EXACT_HAT_R_PLUS_H_EQUALS_E_H"),
    ("V32_PHYSICAL_DIFFERENCE_SUPPORT", "PROVED_EXACT_ABS_H_LESS_THAN_X_OVER_2"),
    ("V32_BASE_SCALE", "Y0_SMALLEST_DYADIC_WITH_H_LE_Y0_LESS_THAN_2H"),
    ("V32_ALIGNED_CELL_PARTITION", "PROVED_EXACT_2Y_HALF_OPEN_CELLS"),
    ("V32_GLOBAL_CONSTANT_QUOTIENT", "PROVED_EXACT_COMPLEX_ONE_CONSTANT_PER_SCALE"),
    ("V32_QUOTIENT_INFIMUM", "PROVED_ATTAINED_CONTINUOUS_COERCIVE"),
    ("V32_QUOTIENT_TRANSLATION_INVARIANCE", "PROVED_EXACT_ZERO_FOURIER_ONLY"),
    ("V32_CELL_DEPENDENT_CONSTANTS", "STOP_SCOPED_NONZERO_FOURIER_CONTAMINATION"),
    ("V32_FEJER_KERNEL", "PROVED_EXACT_POSITIVE_TRIANGULAR_KERNEL"),
    ("V32_FEJER_BAND_CELL_BOUND", "PROVED_EXACT_SAFE_CONSTANT_16"),
    ("V32_DYADIC_REFINEMENT", "PROVED_EXACT_Q_2Y_LE_2_Q_Y"),
    ("V32_SINGLE_SCALE_TO_ALL_SCHWARTZ_SHELLS", "PROVED_EXACT_A_GREATER_THAN_1_GEOMETRIC_REASSEMBLY"),
    ("V32_BASE_SCALE_OSCILLATION_BOUND", "SELECTED_PRIMARY_OPEN_NEW_THEOREM"),
    ("V32_BASE_SCALE_OSCILLATION_EXPONENT", "OPEN_SIGMA_STRICTLY_BELOW_13_OVER_4800"),
    ("V32_WEIGHTED_RESIDUAL_NORM", "PROVED_CONDITIONAL_X_1_PLUS_SIGMA"),
    ("V32_E_ERROR_EXPONENT", "PROVED_CONDITIONAL_191_OVER_192_PLUS_SIGMA"),
    ("V32_E_ENDPOINT_MARGIN", "PROVED_EXACT_13_OVER_4800_MINUS_SIGMA"),
    ("V32_V31_PAIR_IMPLIES_V32_GATE", "PROVED_EXACT_MINKOWSKI_CELL_COMPILER"),
    ("V32_V32_GATE_IMPLIES_V31_PAIR", "STOP_SCOPED_DISJOINT_FACTOR_AND_NARROW_SPIKE_FALSIFIERS"),
    ("V32_FULL_PARSEVAL_EQUIVALENCE", "STOP_SCOPED_SINGLE_BASE_SCALE_ONLY"),
    ("V32_UNIFORM_ALL_SCALE_SAME_BOUND", "STOP_SCOPED_TERMINAL_SCALE_OVERPAYMENT"),
    ("V32_ZERO_AXIS_FIREWALL", "PROVED_EXACT_CONSTANT_RESIDUAL_HAS_Q_ZERO_AND_AXIS_ARBITRARY"),
    ("V32_OFFZERO_B_ALONE", "STOP_SCOPED_TERMINAL_A_SURVIVES"),
    ("V32_QLOCAL_MODEL_BOUND", "RETAINED_PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1"),
    ("V32_A_TERMINAL_COVARIANCE", "RETAINED_SELECTED_TERMINAL_OPEN_NEW_THEOREM"),
    ("V32_CONDITIONAL_ENDPOINT_FORMULA", "MIN_ETA_R_19_OVER_2400_13_OVER_4800_MINUS_SIGMA"),
    ("V32_MRT_DIRECT_ATTACHMENT", "STOP_SCOPED_NO_LITERAL_RESIDUAL_OSCILLATION_BOUND"),
    ("V32_GUTH_MAYNARD_DIRECT_ATTACHMENT", "STOP_SCOPED_MULTIPLICATIVE_PHASE_MARGINAL_LARGE_VALUES"),
    ("V32_HARPER_BDH_DIRECT_ATTACHMENT", "STOP_SCOPED_SINGLE_SEQUENCE_MODULUS_AVERAGE_WRONG_NORM"),
    ("V32_BAZIN_DIRECT_ATTACHMENT", "STOP_SCOPED_TYPE_I_II_RATIONAL_TUBES_NO_LITERAL_EMITTER"),
    ("V32_GRANVILLE_LAMZOURI_DIRECT_ATTACHMENT", "STOP_SCOPED_ONE_BOUNDED_MULTIPLICATIVE_WRONG_COEFFICIENT"),
    ("V32_DIRECT_PRIMARY_SOURCE_ATTACHMENT", "NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08"),
    ("V32_NEXT_THEOREM", "BASE_SCALE_COLLECTIVE_OSCILLATION_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER"),
    ("V32_FIRST_FATAL", "BASE_SCALE_COLLECTIVE_OSCILLATION_BOUND_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER"),
    ("V32_SOURCE_LOCK_POLICY", "PRIMARY_SOURCES_ONLY_FAIL_CLOSED"),
    ("V32_PROVENANCE_CASCADE", "REQUIRED"),
)


EXPECTED_REGISTRY_SHA256 = "8d654f428dc5452f31b0c86d3e0e41270e0dc69df372bc3329c9b968ac63f41b"


SOURCE_ITEMS = (
    ("MRT_ABSTRACT_PRODUCT", "arXiv:1707.01315v3_Proposition_3.1_equation_54"),
    ("GUTH_MAYNARD_LARGE_VALUES", "arXiv:2405.20552v2_Theorem_1.1"),
    ("HARPER_GENERAL_BDH", "arXiv:2412.19644v1_Theorems_1_2"),
    ("BAZIN_TYPE_I_II_BV", "arXiv:2607.15137v1_Theorems_2_8"),
    ("GRANVILLE_LAMZOURI_ADDITIVE_LARGE_VALUES", "arXiv:2604.02306v1_Theorem_1.1"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_whole_object_major_mismatch_and_terminal_compiler.md",
        "54258b95f3678625a8a09f5be00509a602bc6cfceb8d1e00d2259c479ed0809e",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_whole_object_major_mismatch_checker.py",
        "5370460f351a3374610fea39f2e1e099c255beb5d3b2828db3b105a89e67f64c",
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
    if dict_type(literal_registry).get("V32_MAXIMUM_CLAIM") != literal_maximum_claim:
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

    def oscillation_real(values, groups, y):
        vals = tuple_type(fraction_type(v) for v in values)
        atom_measure = fraction_type(1, len_fn(vals))
        breaks = tuple_type(sorted(set_type(vals)))
        candidates = set_type(breaks)
        intervals = list_type()
        intervals.append((None, breaks[0]))
        for left, right in zip(breaks, breaks[1:]):
            intervals.append((left, right))
        intervals.append((breaks[-1], None))
        for left, right in intervals:
            if left is None:
                sample = right - 1
            elif right is None:
                sample = left + 1
            else:
                sample = (left + right) / 2
            linear = list_type()
            for group in groups:
                slope = fraction_type(0)
                intercept = fraction_type(0)
                for index in group:
                    value = vals[index]
                    if sample > value:
                        slope += 1
                        intercept -= value
                    else:
                        slope -= 1
                        intercept += value
                linear.append((slope * atom_measure, intercept * atom_measure))
            denom = sum_fn((a * a for a, _ in linear), fraction_type(0))
            if denom:
                vertex = -sum_fn((a * b for a, b in linear), fraction_type(0)) / denom
                if (left is None or vertex >= left) and (right is None or vertex <= right):
                    candidates.add(vertex)

        def objective(c):
            masses = tuple_type(
                sum_fn((abs_fn(vals[index] - c) * atom_measure for index in group), fraction_type(0))
                for group in groups
            )
            return fraction_type(y) * sum_fn((mass * mass for mass in masses), fraction_type(0))

        scored = tuple_type((objective(c), c) for c in candidates)
        return min_fn(scored)

    def finite_items() -> tuple[tuple[str, object], ...]:
        p = (5, 1, -1, 3)
        ell = (2, 1, -2, -1)
        residual = tuple_type(p[i] - ell[i] for i in range_fn(4))
        residual_dft = dft4(residual)
        singleton_groups = ((0,), (1,), (2,), (3,))
        qosc, minimizer = oscillation_real(residual, singleton_groups, 2)
        qzero = fraction_type(2) * sum_fn((fraction_type(v * v, 16) for v in residual), fraction_type(0))
        offzero_energy = sum_fn((c_abs2(residual_dft[h]) for h in (1, 2, 3)), fraction_type(0))
        if (residual, qosc, minimizer, qzero, offzero_energy) != (
            (3, 0, 1, 4), fraction_type(5, 4), fraction_type(2),
            fraction_type(13, 4), fraction_type(5, 2)
        ):
            raise failure_type("quotient Z4 fixture changed")
        shifted_q, shifted_minimizer = oscillation_real(
            tuple_type(v + 37 for v in residual), singleton_groups, 2
        )
        if (shifted_q, shifted_minimizer) != (qosc, fraction_type(39)):
            raise failure_type("translation invariance changed")

        constant = (37, 37, 37, 37)
        constant_q, constant_minimizer = oscillation_real(constant, singleton_groups, 2)
        constant_dft = dft4(constant)
        if constant_q != 0 or constant_minimizer != 37 or constant_dft[0] != (37, 0):
            raise failure_type("zero-axis constant fixture changed")
        if any_fn(constant_dft[h] != (0, 0) for h in (1, 2, 3)):
            raise failure_type("constant leaked to nonzero frequency")

        nested_values = (5, 4, 1, 0, -1, -2, 3, 2)
        parent_groups = ((0, 1), (2, 3), (4, 5), (6, 7))
        child_groups = tuple_type((i,) for i in range_fn(8))
        q_parent, c_parent = oscillation_real(nested_values, parent_groups, 2)
        q_child, c_child = oscillation_real(nested_values, child_groups, 4)
        if q_child > 2 * q_parent:
            raise failure_type("dyadic refinement failed")

        l_overpay = (2, -2, 2, -2)
        p_overpay = tuple_type(v + 37 for v in l_overpay)
        r_overpay = tuple_type(p_overpay[i] - l_overpay[i] for i in range_fn(4))
        overpay_q, _ = oscillation_real(r_overpay, singleton_groups, 2)
        overpay_d = sum_fn((fraction_type(v * v, 4) for v in r_overpay), fraction_type(0))
        if (overpay_q, overpay_d, dft4(l_overpay)[0]) != (0, fraction_type(1369), (0, 0)):
            raise failure_type("major mismatch overpayment fixture changed")

        b = (8, 0, 0, 0)
        w = (0, 8, 0, 0)
        product = tuple_type(b[i] * w[i] for i in range_fn(4))
        marginal_product = fraction_type(16)
        if product != (0, 0, 0, 0) or marginal_product != 16:
            raise failure_type("disjoint marginal fixture changed")

        spike_amplitude = fraction_type(100)
        spike_width = fraction_type(1, 100)
        spike_l2 = spike_amplitude * spike_amplitude * spike_width
        spike_cell_square = fraction_type(2) * (spike_amplitude * spike_width) ** 2
        spike_ratio = spike_l2 / spike_cell_square
        if (spike_l2, spike_cell_square, spike_ratio) != (100, 2, 50):
            raise failure_type("narrow spike fixture changed")

        near_row = fraction_type(6)
        far_row = fraction_type(2)
        schur_row = near_row + far_row
        fejer_outer = fraction_type(2)
        fejer_constant = schur_row * fejer_outer
        if fejer_constant != 16:
            raise failure_type("Fejer constant changed")

        schwartz_a = fraction_type(2)
        shell_ratio = fraction_type(2) ** (1 - schwartz_a)
        if shell_ratio != fraction_type(1, 2) or not shell_ratio < 1:
            raise failure_type("Schwartz shell convergence changed")

        occurrence_t = (10, 11)
        occurrence_a = (fraction_type(2), fraction_type(-1))
        shell = (10, 11, 12)
        w_values = {10: fraction_type(3), 11: fraction_type(5), 12: fraction_type(7)}
        deltas = (
            {-1: fraction_type(0), 0: fraction_type(0), 1: fraction_type(1), 2: fraction_type(-1)},
            {-1: fraction_type(-1), 0: fraction_type(0), 1: fraction_type(2), 2: fraction_type(0)},
        )
        direct_frequency = {}
        occurrence_e = {}
        for h in (-1, 0, 1, 2):
            total = fraction_type(0)
            for index in range_fn(2):
                u = occurrence_t[index] + h
                if u in shell:
                    total += occurrence_a[index] * (w_values[u] - deltas[index][h])
            occurrence_e[h] = total
        for index in range_fn(2):
            for u in shell:
                frequency = occurrence_t[index] - u
                h = u - occurrence_t[index]
                direct_frequency[frequency] = direct_frequency.get(frequency, fraction_type(0)) + occurrence_a[index] * (w_values[u] - deltas[index][h])
        if tuple_type(occurrence_e[h] for h in (-1, 0, 1, 2)) != (-4, 1, 3, 16):
            raise failure_type("occurrence emitter values changed")
        if any_fn(direct_frequency.get(-h, 0) != occurrence_e[h] for h in (-1, 0, 1, 2)):
            raise failure_type("occurrence Fourier sign changed")
        if all_fn(direct_frequency.get(h, 0) == occurrence_e[h] for h in (-1, 1, 2)):
            raise failure_type("opposite Fourier sign survived")

        sigma = fraction_type(1, 4800)
        eta_r = fraction_type(1, 600)
        e_margin = fraction_type(13, 4800) - sigma
        eta_star = min_fn(eta_r, fraction_type(19, 2400), e_margin)
        if (e_margin, eta_star) != (fraction_type(1, 400), fraction_type(1, 600)):
            raise failure_type("endpoint budget changed")
        if not sigma < fraction_type(13, 4800):
            raise failure_type("strict endpoint lost")

        return (
            ("check", True),
            ("maximum_claim", literal_maximum_claim),
            ("route_advance", "YES"),
            ("P", p),
            ("L", ell),
            ("R", residual),
            ("R_dft", tuple_type(ctext(z) for z in residual_dft)),
            ("Qosc_Y2", ftext(qosc)),
            ("Qosc_minimizer", ftext(minimizer)),
            ("Q_uncentered", ftext(qzero)),
            ("offzero_energy", ftext(offzero_energy)),
            ("translated_Qosc", ftext(shifted_q)),
            ("translated_minimizer", ftext(shifted_minimizer)),
            ("constant_axis", ftext(constant_dft[0][0])),
            ("constant_Qosc", ftext(constant_q)),
            ("parent_Qosc", ftext(q_parent)),
            ("parent_minimizer", ftext(c_parent)),
            ("child_Qosc", ftext(q_child)),
            ("child_minimizer", ftext(c_child)),
            ("refinement_ratio", ftext(q_child / q_parent)),
            ("major_overpay_Qosc", ftext(overpay_q)),
            ("major_overpay_D", ftext(overpay_d)),
            ("marginal_disjoint_product", ftext(marginal_product)),
            ("spike_L2", ftext(spike_l2)),
            ("spike_cell_square", ftext(spike_cell_square)),
            ("spike_ratio", ftext(spike_ratio)),
            ("fejer_near_row", ftext(near_row)),
            ("fejer_far_row", ftext(far_row)),
            ("fejer_constant", ftext(fejer_constant)),
            ("schwartz_A", ftext(schwartz_a)),
            ("schwartz_shell_ratio", ftext(shell_ratio)),
            ("occurrence_e", tuple_type(ftext(occurrence_e[h]) for h in (-1, 0, 1, 2))),
            ("sigma", ftext(sigma)),
            ("E_margin", ftext(e_margin)),
            ("eta_R", ftext(eta_r)),
            ("eta_star", ftext(eta_star)),
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
