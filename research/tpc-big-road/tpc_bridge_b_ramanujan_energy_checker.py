#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V27 highway audit."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


CONTRACT = {
    "maximum_claim": (
        "EXACT_PRIME_SHELL_WEIGHT_ENERGY_AND_ENDPOINT_REDUCTION_PLUS_"
        "SOURCE_CORPUS_STOPS_AND_POINTED_WHOLE_SHELL_ROUTE"
    ),
    "route_advance": "YES",
    "fixed_h0": 2,
    "physical_scale": "x=2X",
    "prime_shell_Q_exponent": "1/3",
    "difference_horizon_exponent": "21/32",
    "prime_normalization_exponent": "2/3",
    "weight_squared_norm_exponent": "127/96",
    "weight_norm_exponent": "127/192",
    "weight_to_normalization_exponent": "-1/192",
    "theta_zero_output_exponent": "191/192",
    "strict_margin": "13/4800",
    "coefficient_l2_weight": "ABS_HATPSI",
    "residual_l2_weight": "ABS_HATPSI",
    "physical_hatpsi_count": 1,
    "effective_horizon": "SCHWARTZ_NOT_HARD_SUPPORT",
    "smooth_main_after_zero_deletion": "STOP_SCOPED_ZERO_AXIS_MINUS_F_OF_ZERO",
    "selected_analytic_gate": "OPEN_NEW_THEOREM",
    "mixed_hb_gate": "OPEN_TAGGED_VECTOR_THEOREM",
    "parameter_averaged_same_output": "STOP_SCOPED_TAUTOLOGICAL_MEAN_OR_NULL_GRAPH",
    "pointed_block_gate": "OPEN_AFTER_EXACT_SINGLE_PARAMETER_FACTOR",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
    "numbered_release": "NO",
}


REGISTRY_ITEMS = (
    (
        "V27_MAXIMUM_CLAIM",
        "EXACT_PRIME_SHELL_WEIGHT_ENERGY_AND_ENDPOINT_REDUCTION_PLUS_"
        "SOURCE_CORPUS_STOPS_AND_POINTED_WHOLE_SHELL_ROUTE",
    ),
    ("V27_ROUTE_ADVANCE", "YES"),
    ("V27_ARITHMETIC_ADVANCE", "NO"),
    ("V27_FIXED_ATOM_CREDIT", "0"),
    ("V27_STRICT_1_OVER_400", "UNPAID"),
    ("V27_L2", "NONE"),
    ("V27_TPC_207_TRIGGER", "false"),
    ("V27_NUMBERED_RELEASE", "NO"),
    (
        "V27_PRIME_SHELL_HARD_WINDOW_RAMANUJAN_L2_IDENTITY",
        "PROVED_EXACT_L0_FOR_N_LT_FIRST_DISTINCT_PRIME_PRODUCT",
    ),
    (
        "V27_PRIME_SHELL_RAMANUJAN_WEIGHTED_ENERGY",
        "PROVED_EXACT_FINITE_PLUS_SCHWARTZ_ASYMPTOTIC",
    ),
    (
        "V27_EFFECTIVE_HORIZON_AS_HARD_SUPPORT",
        "STOP_SCOPED_FALSE_SCHWARTZ_TAIL_AND_DOUBLE_DIVISOR_CROSS_TERMS",
    ),
    (
        "V27_ONE_PSI_WEIGHTED_CAUCHY_INTERFACE",
        "PROVED_EXACT_ABS_PSI_HALF_WEIGHT_ON_BOTH_FACTORS",
    ),
    (
        "V27_LITERAL_PRIME_SHELL_RAMANUJAN_VECTOR_COVARIANCE",
        "SELECTED_OPEN_NEW_THEOREM",
    ),
    (
        "V27_FULL_LATTICE_SMOOTH_MAIN_POISSON_IDENTITY",
        "PROVED_EXACT_DETERMINISTIC_INTERFACE",
    ),
    (
        "V27_AUTOMATIC_SMOOTH_LOCAL_MAIN_ANNIHILATION_AFTER_CORRELATION_ZERO_SHIFT_DELETION",
        "STOP_SCOPED_ZERO_AXIS_MINUS_F_OF_ZERO",
    ),
    (
        "V27_SIGNED_LOCAL_MAIN_ZERO_AXIS_AND_RESIDUAL_REASSEMBLY",
        "OPEN_NEW_THEOREM",
    ),
    (
        "V27_MRSTT_ALL_INTERVAL_LAMBDA_MINUS_LAMBDASHARP_LINEAR_PHASE",
        "SOURCE_BACKED_LOCAL_LOG_INPUT",
    ),
    (
        "V27_MRSTT_LAMBDASHARP_TO_TENSOR_LOCAL_BZ_TRANSFER",
        "OPEN_NEW_COMPARISON_THEOREM",
    ),
    (
        "V27_MRT_MRSTT_TO_LITERAL_PRIME_RAMANUJAN_WEIGHTED_NUMERATOR",
        "STOP_SCOPED_NO_COLLECTIVE_POWER_NORM",
    ),
    (
        "V27_LEUNG_ARBITRARY_WEIGHTED_SHIFT_ARCHITECTURE",
        "SOURCE_BACKED_AUTOMORPHIC_ANALOGUE_ONLY",
    ),
    (
        "V27_EXISTING_SHIFTED_CONVOLUTION_SPECTRAL_CORPUS_DIRECT_ATTACHMENT",
        "STOP_SCOPED_NO_LITERAL_WHOLE_PHYSICAL_SCALAR",
    ),
    (
        "V27_MIXED_HB2_ONE_COMMON_SOURCE_ARRAY",
        "STOP_SCOPED_FINITE_SELECTOR_MINOR_ONE",
    ),
    (
        "V27_TAGGED_VECTOR_MIXED_HB2_DETERMINANT_REASSEMBLY",
        "OPEN_NEW_THEOREM",
    ),
    (
        "V27_PARAMETER_AVERAGED_EXACT_SAME_ARITHMETIC_OUTPUT_CARRIER",
        "STOP_SCOPED_TAUTOLOGICAL_MEAN_OR_NULL_GRAPH",
    ),
    (
        "V27_STAGEWISE_TRANSVERSE_PARAMETER_RESELECTION",
        "STOP_SCOPED_NO_COMMON_PARAMETER",
    ),
    (
        "V27_POINTED_CRITICAL_SECTION_WHOLE_SHELL_DISCREPANCY",
        "OPEN_NEW_THEOREM_AFTER_EXACT_SINGLE_PARAMETER_FACTOR",
    ),
    (
        "V27_HENON_POINTED_WHOLE_SHELL_SECTION_TRANSFER",
        "OPEN_ONLY_AFTER_EXACT_NATURAL_SECTION_DIAGRAM",
    ),
    ("V27_O161_PARENTS", "OPEN_UNCHANGED"),
    ("V27_PAIR_NATIVE_H1_GLOBAL", "OPEN_UNCHANGED"),
    ("V27_A1_A2", "INDEPENDENT_OPEN_RESERVES"),
    ("V27_TAIL_FAILURE_A_B_PACKET_PROVENANCE", "UNPAID_UNCHANGED"),
)


EXPECTED_REGISTRY_SHA256 = "dfce061f4324601dc57e6ae402fbda95b427622ae381355ddac9bdd23efb52bd"


SOURCE_ITEMS = (
    ("MRT_LONG_SHIFTS", "arXiv:1707.01315v3_Theorem_1.3_Propositions_3.1_3.4_6.1"),
    ("HIGHER_UNIFORMITY_I", "arXiv:2204.03754_Theorem_1.1(ii)"),
    (
        "HIGHER_UNIFORMITY_II",
        "arXiv:2411.05770v2_Theorem_1.1(ii)_Corollary_1.2_Theorems_1.5_1.8",
    ),
    ("LEUNG_WEIGHTED_SHIFTS", "arXiv:2210.13081v2_Theorems_1.1_1.2"),
    ("BETTIN_CHANDEE", "arXiv:1502.00769v1_Corollary_1"),
    ("DRAPPEAU", "arXiv:1504.05549v4_Theorems_2.1_5.1"),
    ("ABP_CRITICAL_SEED", "arXiv:2212.12202v2_Theorem_1.1"),
    ("HNTV", "arXiv:1406.4266_Theorems_3.1_4.1"),
    ("KOREPANOV", "arXiv:1703.09176_FIXED_OBSERVABLE_ASIP"),
)


DEPENDENCIES = (
    (
        "research/tpc-big-road/bridge_b_mesoscopic_covariance.md",
        "e9838ebee8aa027421dad9bc2d05cb7b3655d2de413da0aa11aa143095636c37",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_mesoscopic_covariance_checker.py",
        "b6350ce0f7ed38dd7671f5076a0c26bf82bb57850ec35505c4cfec3239ad336e",
    ),
    (
        "research/tpc-big-road/bridge_b_corrected_fourier_factorable_emitter.md",
        "b0d434776057c3c3310edb54f56a7ead098d613398b4e2b73aedb65012673f02",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_corrected_fourier_factorable_checker.py",
        "a4844782745a16a1f6b4554f7dea959b4a44a0b49ecd85c32f552e21a8e998a1",
    ),
    (
        "research/tpc-big-road/bridge_b_compensated_dilation_and_block_highway.md",
        "96fb71f5e24c3d04a27724b964010066d721d453139e0e84117d3bb9e6bdaa65",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_compensated_dilation_block_checker.py",
        "d3fa5285543d879429f832dcb1a51152521a518da136ddd53291aa90150be9a8",
    ),
)


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_lf(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n")


def _ramanujan_prime(q: int, h: int) -> int:
    return q - 1 if h % q == 0 else -1


def _poly_multiply(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    output = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return tuple(output)


def _finite_fixtures() -> dict[str, object]:
    primes = (11, 13)
    count = len(primes)
    normalization = sum(q - 1 for q in primes)

    def weight(h: int) -> int:
        return sum(_ramanujan_prime(q, h) for q in primes)

    hard_horizon = 40
    direct_hard_norm = sum(weight(h) ** 2 for h in range(-hard_horizon, hard_horizon + 1) if h)
    formula_hard_norm = 2 * (
        hard_horizon * count * count
        + sum(
            (hard_horizon // q) * (q * q - 2 * q * count)
            for q in primes
        )
    )
    if direct_hard_norm != 1484 or formula_hard_norm != direct_hard_norm:
        raise CheckFailure("hard-window Ramanujan energy changed")

    cross_horizon = 143
    direct_cross_norm = sum(weight(h) ** 2 for h in range(-cross_horizon, cross_horizon + 1) if h)
    no_cross_formula = 2 * (
        cross_horizon * count * count
        + sum(
            (cross_horizon // q) * (q * q - 2 * q * count)
            for q in primes
        )
    )
    cross_defect = direct_cross_norm - no_cross_formula
    if direct_cross_norm != 6292 or no_cross_formula != 5720 or cross_defect != 572:
        raise CheckFailure("double-divisor cross fixture changed")

    period = primes[0] * primes[1]
    complete_sum = sum(weight(h) for h in range(period))
    nonzero_sum = sum(weight(h) for h in range(1, period))
    if complete_sum != 0 or weight(0) != normalization or nonzero_sum != -normalization:
        raise CheckFailure("zero-axis complete-period identity changed")

    coefficient_norm_exponent = (Fraction(21, 32) + Fraction(2, 3)) / 2
    coefficient_ratio_exponent = coefficient_norm_exponent - Fraction(2, 3)
    output_exponent = Fraction(1) + coefficient_ratio_exponent
    strict_margin = Fraction(399, 400) - output_exponent
    if (
        coefficient_norm_exponent != Fraction(127, 192)
        or coefficient_ratio_exponent != Fraction(-1, 192)
        or output_exponent != Fraction(191, 192)
        or strict_margin != Fraction(13, 4800)
    ):
        raise CheckFailure("endpoint exponent ledger changed")
    if output_exponent + Fraction(13, 4800) != Fraction(399, 400):
        raise CheckFailure("theta equality firewall changed")
    if not output_exponent + Fraction(12, 4800) < Fraction(399, 400):
        raise CheckFailure("strict theta witness changed")

    mrt_energy_exponent = Fraction(1) + Fraction(21, 64)
    mrt_numerator_exponent = mrt_energy_exponent + coefficient_norm_exponent
    target_numerator_exponent = Fraction(2, 3) + Fraction(399, 400)
    mrt_deficit = mrt_numerator_exponent - target_numerator_exponent
    mrstt_triangle_exponent = Fraction(1) + Fraction(21, 32) + Fraction(2, 3)
    leung_exponent = Fraction(3, 4) + Fraction(21, 64) + coefficient_norm_exponent
    leung_deficit = leung_exponent - target_numerator_exponent
    if (
        mrt_numerator_exponent != Fraction(191, 96)
        or mrt_deficit != Fraction(781, 2400)
        or mrstt_triangle_exponent != Fraction(223, 96)
        or leung_exponent != Fraction(167, 96)
        or leung_deficit != Fraction(181, 2400)
    ):
        raise CheckFailure("source power ledger changed")

    psi_values = {
        h: Fraction((-1) ** h * (h + 1), h + 2)
        for h in range(1, 11)
    }
    residual = {h: Fraction(h - 6, h + 1) for h in range(1, 11)}
    scalar = sum(psi_values[h] * weight(h) * residual[h] for h in residual)
    coefficient_energy = sum(abs(psi_values[h]) * weight(h) ** 2 for h in residual)
    residual_energy = sum(abs(psi_values[h]) * residual[h] ** 2 for h in residual)
    cauchy_gap = coefficient_energy * residual_energy - scalar * scalar
    if cauchy_gap < 0:
        raise CheckFailure("one-psi weighted Cauchy failed")

    x1_at_3 = Fraction(3, 4)
    a2 = Fraction(7, 2)
    x2_at_a2 = a2 * a2 * (4 - a2) / 16
    x2_derivative_at_a2 = a2 * (8 - 3 * a2) / 16
    x2_residual_at_3 = Fraction(3 * 3 * (4 - 3), 16) - Fraction(49, 128)
    if (
        x1_at_3 != Fraction(3, 4)
        or x2_at_a2 != Fraction(49, 128)
        or x2_derivative_at_a2 != Fraction(-35, 64)
        or x2_residual_at_3 != Fraction(23, 128)
    ):
        raise CheckFailure("stagewise parameter falsifier changed")

    polynomial = (Fraction(1),)
    for point in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
        polynomial = _poly_multiply(polynomial, (point * point, -2 * point, Fraction(1)))
    extension_integral = sum(coefficient / Fraction(index + 1) for index, coefficient in enumerate(polynomial))
    if extension_integral != Fraction(107, 107520):
        raise CheckFailure("off-orbit extension mean changed")

    carrier_values = (7, 7, 7, 7)
    carrier_mean = Fraction(sum(carrier_values), len(carrier_values))
    carrier_variance = sum((Fraction(value) - carrier_mean) ** 2 for value in carrier_values) / len(carrier_values)
    if carrier_mean != 7 or carrier_variance != 0:
        raise CheckFailure("same-output parameter tautology changed")

    return {
        "fixture_primes": "11,13",
        "hard_horizon": hard_horizon,
        "hard_norm_squared": direct_hard_norm,
        "cross_horizon": cross_horizon,
        "direct_cross_norm_squared": direct_cross_norm,
        "no_cross_norm_squared": no_cross_formula,
        "double_divisor_cross_defect": cross_defect,
        "period": period,
        "complete_period_sum": complete_sum,
        "zero_axis": weight(0),
        "nonzero_period_sum": nonzero_sum,
        "coefficient_norm_exponent": str(coefficient_norm_exponent),
        "coefficient_ratio_exponent": str(coefficient_ratio_exponent),
        "theta_zero_output_exponent": str(output_exponent),
        "strict_margin": str(strict_margin),
        "mrt_power_deficit": str(mrt_deficit),
        "mrstt_triangle_exponent": str(mrstt_triangle_exponent),
        "leung_power_deficit": str(leung_deficit),
        "cauchy_gap": str(cauchy_gap),
        "stage2_common_parameter_residual": str(x2_residual_at_3),
        "off_orbit_extension_integral": str(extension_integral),
        "same_output_parameter_mean": str(carrier_mean),
        "same_output_parameter_variance": str(carrier_variance),
    }


def _make_trusted_runner(
    contract_seed=tuple(CONTRACT.items()),
    registry_seed=REGISTRY_ITEMS,
    registry_digest_seed=EXPECTED_REGISTRY_SHA256,
    source_seed=SOURCE_ITEMS,
    dependency_seed=DEPENDENCIES,
    fixture_seed=_finite_fixtures(),
    failure_type=CheckFailure,
    json_serializer=json.dumps,
    hash_constructor=hashlib.sha256,
    path_type=Path,
):
    literal_contract_items = tuple(contract_seed)
    literal_contract_keys = frozenset(key for key, _ in literal_contract_items)
    literal_registry = tuple(registry_seed)
    literal_registry_digest = registry_digest_seed
    literal_sources = tuple(source_seed)
    literal_dependencies = tuple(dependency_seed)
    literal_fixture_items = tuple(fixture_seed.items())
    literal_maximum_claim = next(
        value for key, value in literal_contract_items if key == "maximum_claim"
    )
    literal_route_advance = next(
        value for key, value in literal_contract_items if key == "route_advance"
    )

    def local_canonical_json(value: object) -> bytes:
        return json_serializer(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def local_sha256(value: bytes) -> str:
        return hash_constructor(value).hexdigest()

    def local_canonical_lf(value: bytes) -> bytes:
        return value.replace(b"\r\n", b"\n")

    def exact_type(value: object, expected: object) -> bool:
        return type(value) is type(expected)

    def key_impostor_mapping(
        items: tuple[tuple[str, object], ...], target: str
    ) -> dict[object, object]:
        class KeyImpostor:
            def __init__(self, text: str):
                self.text = text

            def __hash__(self) -> int:
                return hash(self.text)

            def __eq__(self, other: object) -> bool:
                return other == self.text

        result: dict[object, object] = {
            KeyImpostor(target): next(value for key, value in items if key == target)
        }
        result.update((key, value) for key, value in items if key != target)
        return result

    def validate_contract(candidate: object) -> None:
        if (
            type(candidate) is not dict
            or any(type(key) is not str for key in candidate)
            or set(candidate) != literal_contract_keys
        ):
            raise failure_type("contract schema changed")
        for key, expected in literal_contract_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"contract field {key} changed")

    def registry_digest(items: tuple[tuple[str, str], ...]) -> str:
        return local_sha256(local_canonical_json(list(items)))

    def validate_registry(candidate: object, claimed_digest: object) -> None:
        if type(candidate) is not tuple:
            raise failure_type("registry must be tuple")
        if any(type(row) is not tuple or len(row) != 2 for row in candidate):
            raise failure_type("registry row shape changed")
        if any(type(key) is not str or type(value) is not str for key, value in candidate):
            raise failure_type("registry row type changed")
        if len(candidate) != len(literal_registry):
            raise failure_type("registry row count changed")
        if len({key for key, _ in candidate}) != len(candidate):
            raise failure_type("registry keys not unique")
        if candidate != literal_registry:
            raise failure_type("registry semantic promotion")
        if type(claimed_digest) is not str or claimed_digest != literal_registry_digest:
            raise failure_type("registry literal digest changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry content digest changed")

    def validate_sources(candidate: object) -> None:
        if type(candidate) is not tuple or candidate != literal_sources:
            raise failure_type("source lock changed")
        if any(type(row) is not tuple or len(row) != 2 for row in candidate):
            raise failure_type("source row shape changed")
        if any(type(key) is not str or type(value) is not str for key, value in candidate):
            raise failure_type("source row type changed")

    def validate_dependencies(candidate: object) -> None:
        if type(candidate) is not tuple:
            raise failure_type("dependency registry must be tuple")
        if any(type(row) is not tuple or len(row) != 2 for row in candidate):
            raise failure_type("dependency row shape changed")
        if any(type(path) is not str or type(digest) is not str for path, digest in candidate):
            raise failure_type("dependency row type changed")
        if candidate != literal_dependencies:
            raise failure_type("dependency lock changed")
        root = path_type(__file__).resolve().parents[2]
        for relative, expected in literal_dependencies:
            path = root / relative
            if not path.is_file():
                raise failure_type(f"dependency missing: {relative}")
            actual = local_sha256(local_canonical_lf(path.read_bytes()))
            if actual != expected:
                raise failure_type(f"dependency hash changed: {relative}")

    def must_reject(label: str, action) -> None:
        try:
            action()
        except failure_type:
            return
        raise failure_type(f"mutation escaped: {label}")

    def contract_mutations() -> int:
        count = 0
        for key, expected in literal_contract_items:
            missing = dict(literal_contract_items)
            del missing[key]
            must_reject(f"contract_missing_{key}", lambda c=missing: validate_contract(c))
            count += 1

            wrong_type = dict(literal_contract_items)
            wrong_type[key] = str(expected) if type(expected) is not str else 0
            must_reject(f"contract_type_{key}", lambda c=wrong_type: validate_contract(c))
            count += 1

            wrong_value = dict(literal_contract_items)
            if type(expected) is bool:
                wrong_value[key] = not expected
            elif type(expected) is int:
                wrong_value[key] = expected + 1
            else:
                wrong_value[key] = expected + "__MUTATED"
            must_reject(f"contract_value_{key}", lambda c=wrong_value: validate_contract(c))
            count += 1

        extra = dict(literal_contract_items)
        extra["UNDECLARED"] = "PROMOTION"
        must_reject("contract_extra", lambda: validate_contract(extra))
        key_type = key_impostor_mapping(literal_contract_items, "maximum_claim")
        must_reject("contract_key_type", lambda: validate_contract(key_type))
        return count + 2

    def registry_mutations() -> int:
        count = 0
        for index, (key, value) in enumerate(literal_registry):
            changed_value = list(literal_registry)
            changed_value[index] = (key, value + "__PROMOTED")
            changed_value_tuple = tuple(changed_value)
            changed_value_digest = registry_digest(changed_value_tuple)
            must_reject(
                f"registry_value_{index+1}",
                lambda c=changed_value_tuple, d=changed_value_digest: validate_registry(c, d),
            )
            count += 1

            changed_key = list(literal_registry)
            changed_key[index] = (key + "__REPLACED", value)
            changed_key_tuple = tuple(changed_key)
            changed_key_digest = registry_digest(changed_key_tuple)
            must_reject(
                f"registry_key_{index+1}",
                lambda c=changed_key_tuple, d=changed_key_digest: validate_registry(c, d),
            )
            count += 1

        must_reject(
            "registry_wrong_type",
            lambda: validate_registry(list(literal_registry), literal_registry_digest),
        )
        must_reject(
            "registry_false_digest",
            lambda: validate_registry(literal_registry, "0" * 64),
        )
        return count + 2

    def source_mutations() -> int:
        count = 0
        for index, (key, value) in enumerate(literal_sources):
            changed_value = list(literal_sources)
            changed_value[index] = (key, value + "__PROMOTED")
            must_reject(
                f"source_value_{index+1}",
                lambda c=tuple(changed_value): validate_sources(c),
            )
            count += 1

            changed_key = list(literal_sources)
            changed_key[index] = (key + "__REPLACED", value)
            must_reject(
                f"source_key_{index+1}",
                lambda c=tuple(changed_key): validate_sources(c),
            )
            count += 1

        must_reject("source_wrong_type", lambda: validate_sources(list(literal_sources)))
        must_reject("source_missing", lambda: validate_sources(literal_sources[:-1]))
        return count + 2

    def dependency_mutations() -> int:
        count = 0
        for index, (path, digest) in enumerate(literal_dependencies):
            changed_path = list(literal_dependencies)
            changed_path[index] = (path + ".wrong", digest)
            must_reject(
                f"dependency_path_{index+1}",
                lambda c=tuple(changed_path): validate_dependencies(c),
            )
            count += 1

            changed_hash = list(literal_dependencies)
            changed_hash[index] = (path, "0" * 64)
            must_reject(
                f"dependency_hash_{index+1}",
                lambda c=tuple(changed_hash): validate_dependencies(c),
            )
            count += 1
        must_reject(
            "dependency_wrong_outer_type",
            lambda: validate_dependencies(list(literal_dependencies)),
        )
        wrong_row = list(literal_dependencies)
        wrong_row[0] = list(wrong_row[0])
        must_reject(
            "dependency_wrong_row_shape",
            lambda c=tuple(wrong_row): validate_dependencies(c),
        )
        class TextSubclass(str):
            pass

        wrong_field = list(literal_dependencies)
        wrong_field[0] = (TextSubclass(wrong_field[0][0]), wrong_field[0][1])
        must_reject(
            "dependency_wrong_field_type",
            lambda c=tuple(wrong_field): validate_dependencies(c),
        )
        return count + 3

    expected_result_items = literal_fixture_items + (
        ("check", True),
        ("maximum_claim", literal_maximum_claim),
        ("route_advance", literal_route_advance),
        ("contract_fields", len(literal_contract_items)),
        ("registry_rows", len(literal_registry)),
        ("registry_sha256", literal_registry_digest),
        ("source_locks", len(literal_sources)),
        ("dependency_locks", len(literal_dependencies)),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
    )
    expected_result_keys = frozenset(key for key, _ in expected_result_items)

    def validate_result(candidate: object) -> None:
        if (
            type(candidate) is not dict
            or any(type(key) is not str for key in candidate)
            or set(candidate) != expected_result_keys
        ):
            raise failure_type("result schema changed")
        for key, expected in expected_result_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"result field {key} changed")

    def semantic_mutations() -> int:
        fields = (
            "maximum_claim",
            "route_advance",
            "arithmetic_advance",
            "fixed_atom_credit",
            "strict_1_over_400",
            "L2",
            "TPC_207_TRIGGER",
        )
        count = 0
        for key in fields:
            expected = dict(expected_result_items)[key]
            wrong_value = dict(expected_result_items)
            if type(expected) is bool:
                wrong_value[key] = not expected
            elif type(expected) is int:
                wrong_value[key] = expected + 1
            else:
                wrong_value[key] = expected + "__FALSE_PROMOTION"
            must_reject(
                f"result_value_{key}",
                lambda c=wrong_value: validate_result(c),
            )
            count += 1

            wrong_type = dict(expected_result_items)
            wrong_type[key] = str(expected) if type(expected) is not str else 0
            must_reject(
                f"result_type_{key}",
                lambda c=wrong_type: validate_result(c),
            )
            count += 1
        key_type = key_impostor_mapping(expected_result_items, "arithmetic_advance")
        must_reject("result_key_type", lambda: validate_result(key_type))
        count += 1

        full_key_type = key_impostor_mapping(expected_full_items, "arithmetic_advance")
        must_reject("full_result_key_type", lambda: validate_full_result(full_key_type))
        return count + 1

    expected_count_items = (
        ("contract_mutations", 3 * len(literal_contract_items) + 2),
        ("registry_mutations", 2 * len(literal_registry) + 2),
        ("source_mutations", 2 * len(literal_sources) + 2),
        ("dependency_mutations", 2 * len(literal_dependencies) + 3),
        ("semantic_mutations", 16),
    )
    expected_full_items = expected_result_items + expected_count_items
    expected_full_keys = frozenset(key for key, _ in expected_full_items)

    def validate_full_result(candidate: object) -> None:
        if (
            type(candidate) is not dict
            or any(type(key) is not str for key in candidate)
            or set(candidate) != expected_full_keys
        ):
            raise failure_type("full result schema changed")
        for key, expected in expected_full_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"full result field {key} changed")

    def trusted_run() -> dict[str, object]:
        validate_contract(dict(literal_contract_items))
        validate_registry(tuple(literal_registry), literal_registry_digest)
        validate_sources(tuple(literal_sources))
        validate_dependencies(tuple(literal_dependencies))
        result = dict(expected_result_items)
        validate_result(result)
        result["contract_mutations"] = contract_mutations()
        result["registry_mutations"] = registry_mutations()
        result["source_mutations"] = source_mutations()
        result["dependency_mutations"] = dependency_mutations()
        result["semantic_mutations"] = semantic_mutations()

        if tuple((key, result[key]) for key, _ in expected_full_items) != expected_full_items:
            raise failure_type("mutation execution counts changed")

        validate_full_result(result)
        return result

    return trusted_run


_TRUSTED_RUN = _make_trusted_runner()


def _seal_runner(runner):
    def sealed() -> dict[str, object]:
        return runner()

    return sealed


run_check = _seal_runner(_TRUSTED_RUN)
del _seal_runner


def _seal_main(runner, frozen_argv=tuple(sys.argv), serializer=json.dumps, failure_type=CheckFailure):
    def sealed(argv: list[str] | None = None) -> int:
        args = frozen_argv[1:] if argv is None else tuple(argv)
        if tuple(args) != ("--check",):
            raise failure_type("explicit --check is required")
        result = runner()
        print(serializer(result, ensure_ascii=False, sort_keys=True))
        return 0

    return sealed


main = _seal_main(_TRUSTED_RUN)
del _seal_main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as exc:
        print(f"CheckFailure: {exc}", file=sys.stderr)
        raise SystemExit(1)
