#!/usr/bin/env python3
"""Fail-closed finite checker for the unnumbered V26 highway audit."""

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
        "EXACT_L0_COMPENSATED_PRIME_DILATION_AND_FACTORIZABLE_J1_SHORT_DUAL_"
        "NORMAL_FORMS_PLUS_SOURCE_BACKED_CRITICAL_SEED_ASIP_INTERFACE_AND_"
        "WHOLE_SHELL_BLOCK_RETYPE"
    ),
    "route_advance": "YES",
    "fixed_h0": 2,
    "physical_scale": "x=2X",
    "prime_shell_Q_exponent": "1/3",
    "prime_shell_delta_exponent": "-21/32",
    "difference_horizon_exponent": "21/32",
    "dilation_k_exponent": "31/96",
    "prime_normalization_exponent": "2/3",
    "endpoint_numerator_ceiling": "1997/1200",
    "square_root_numerator_exponent": "319/192",
    "square_root_output_exponent": "191/192",
    "strict_margin": "13/4800",
    "j1_local_error_exponent": "39/40",
    "j1_local_gross_margin": "9/400",
    "j1_dual_length_exponent": "1/14",
    "factorable_Q_exponent": "4/7",
    "single_lacunary_event": "STOP_SCOPED_FINITE_TOTAL_EVENT_MASS",
    "whole_shell_block_chebyshev": "PROVED_ELEMENTARY_SUMMABLE_HAAR_BAD_MASS",
    "critical_section_block_transfer": "OPEN_NEW_THEOREM",
    "critical_seed_asip": "SOURCE_BACKED_FIXED_HOLDER_OBSERVABLE",
    "arithmetic_advance": False,
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}


REGISTRY_ITEMS = (
    (
        "V26_MAXIMUM_CLAIM",
        "EXACT_L0_COMPENSATED_PRIME_DILATION_AND_FACTORIZABLE_J1_SHORT_DUAL_"
        "NORMAL_FORMS_PLUS_SOURCE_BACKED_CRITICAL_SEED_ASIP_INTERFACE_AND_"
        "WHOLE_SHELL_BLOCK_RETYPE",
    ),
    ("V26_ROUTE_ADVANCE", "YES"),
    ("V26_ARITHMETIC_ADVANCE", "NO"),
    ("V26_FIXED_ATOM_CREDIT", "0"),
    ("V26_STRICT_1_OVER_400", "UNPAID"),
    ("V26_L2", "NONE"),
    ("V26_TPC_207_TRIGGER", "false"),
    ("V26_PRIME_SHELL_COMPENSATED_DILATION_IDENTITY", "PROVED_EXACT_L0"),
    ("V26_PRIME_SHELL_SQUARE_ROOT_ENDPOINT_LEDGER", "PROVED_EXACT_RATIONAL_POSITIVE_MARGIN"),
    ("V26_PRIME_SHELL_RAMANUJAN_COMPENSATED_DILATION_COVARIANCE", "OPEN_NEW_THEOREM"),
    (
        "V26_DECLARED_DI_KUZNETSOV_DISPERSION_SHIFTED_CONVOLUTION_"
        "JUTILA_BP_PASCADI_PRIMARY_CORPUS_DIRECT_ATTACHMENT_V1",
        "STOP_SCOPED_NO_LITERAL_COLLECTIVE_PHYSICAL_SCALAR_THEOREM",
    ),
    ("V26_J1xJ1_SMOOTH_DETERMINANT_CELL", "SOURCE_BACKED_CONDITIONAL_LOCAL_ENGINE_ERROR_39_OVER_40_BEFORE_MAIN_REASSEMBLY"),
    ("V26_COMMON_FACTORABLE_J1_SHORT_DUAL_DETERMINANT", "PROVED_EXACT_L0_COPRIME_SMOOTH_CELL"),
    ("V26_COMMON_ENSEMBLE_GOOD_BAD_p_INCIDENCE", "PROVED_EXACT_L0_ANALYTIC_COST_OPEN"),
    ("V26_SINGLE_TEMPLATE_MASTER_FACTORIZATION", "STOP_SCOPED_FINITE_2X2_MINOR"),
    ("V26_ALL_HB2_TYPES_ONE_COMMON_SOURCE_ARRAY", "STOP_SCOPED_J2_DEGENERATE_AXIS_AND_NORMALIZATION_MISMATCH"),
    ("V26_HYBRID_TO_SAME_ARRAYS", "STOP_SCOPED_PROGRESS_MODULUS_MAIN_REASSEMBLY_MISMATCH"),
    ("V26_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER", "STOP_SCOPED_PARTIAL_J1_ONLY_NO_WHOLE_OBJECT"),
    ("V26_MIXED_HB_DETERMINANT_COMPILER", "OPEN_NEW_THEOREM_RANK1"),
    ("V26_LACUNARY_SINGLE_EVENT_DBC", "STOP_SCOPED_FINITE_TOTAL_EVENT_MASS"),
    ("V26_WHOLE_SHELL_BLOCK_CHEBYSHEV", "PROVED_ELEMENTARY_SUMMABLE_HAAR_BAD_MASS"),
    ("V26_LOGISTIC_CRITICAL_SEED_PARAMETER_ASIP", "SOURCE_BACKED_FIXED_HOLDER_OBSERVABLE"),
    ("V26_ARITHMETIC_SEED_TO_CRITICAL_SECTION_INTERTWINER", "ABSENT"),
    ("V26_GROWING_TRIANGULAR_CRITICAL_SECTION_THEOREM", "ABSENT"),
    ("V26_SAFE_LACUNARY_CRITICAL_SECTION_BLOCK_TRANSFER_THEOREM", "OPEN_NEW_THEOREM"),
    ("V26_HENON_SECTION_TRANSFER", "OPEN_ONLY_AFTER_EXACT_FACTOR"),
    ("V26_O161_PARENTS", "OPEN_UNCHANGED"),
    ("V26_PAIR_NATIVE_H1_GLOBAL", "OPEN_UNCHANGED"),
    ("V26_A1_A2", "INDEPENDENT_OPEN_RESERVES"),
    ("V26_NUMBERED_RELEASE", "NO"),
)


EXPECTED_REGISTRY_SHA256 = "23e400afbb8d57de0c143a3fecd648ce240a282600688cd56bd4cc75b1dcc6c0"


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
        "research/tpc-big-road/bridge_b_corrected_fourier_factorable_emitter.md",
        "b0d434776057c3c3310edb54f56a7ead098d613398b4e2b73aedb65012673f02",
    ),
    (
        "research/tpc-big-road/tpc_bridge_b_corrected_fourier_factorable_checker.py",
        "a4844782745a16a1f6b4554f7dea959b4a44a0b49ecd85c32f552e21a8e998a1",
    ),
    (
        "research/tpc-big-road/bridge_b_prime_shell_jutila_and_stable_dynamics.md",
        "7f8131f59a1161e795f6a982a80d4e4bdfee0d16ced49c43e25e84ef2957e955",
    ),
)


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_lf(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n")


def _mobius(n: int) -> int:
    if n < 1:
        raise CheckFailure("mobius domain")
    value = n
    primes = 0
    p = 2
    while p * p <= value:
        if value % p == 0:
            value //= p
            primes += 1
            if value % p == 0:
                return 0
            while value % p == 0:
                value //= p
        p += 1
    if value > 1:
        primes += 1
    return -1 if primes % 2 else 1


def _finite_fixtures() -> dict[str, object]:
    primes = (5, 7)
    beta = {1: Fraction(2), 2: Fraction(-1), 4: Fraction(3), 8: Fraction(-2)}
    residual = {2: Fraction(1), 3: Fraction(-2), 5: Fraction(4), 9: Fraction(3), 11: Fraction(-1)}
    interval = range(1, 13)

    def psi_hat(h: int) -> Fraction:
        return Fraction(1, abs(h) + 1)

    correlations: dict[int, Fraction] = {}
    for h in range(-11, 12):
        if h == 0:
            continue
        total = Fraction(0)
        for t in interval:
            u = t + h
            if u in interval:
                total += beta.get(t, Fraction(0)) * residual.get(u, Fraction(0))
        correlations[h] = psi_hat(h) * total

    normalization = sum(q - 1 for q in primes)
    multiplier_numerator = Fraction(0)
    same_residue_numerator = Fraction(0)
    for q in primes:
        for h, value in correlations.items():
            multiplier_numerator += value * (q * int(h % q == 0) - 1)
        for t in interval:
            for u in interval:
                if u == t:
                    continue
                same_residue_numerator += (
                    beta.get(t, Fraction(0))
                    * residual.get(u, Fraction(0))
                    * psi_hat(u - t)
                    * (q * int((u - t) % q == 0) - 1)
                )

    dilation_numerator = Fraction(0)
    all_h = sum(correlations.values(), Fraction(0))
    for q in primes:
        dilation_numerator += q * sum(
            (value for h, value in correlations.items() if h % q == 0), Fraction(0)
        )
    dilation_numerator -= len(primes) * all_h

    if multiplier_numerator != same_residue_numerator or multiplier_numerator != dilation_numerator:
        raise CheckFailure("prime-dilation normal forms disagree")

    endpoint_ceiling = Fraction(2, 3) + Fraction(399, 400)
    square_root_numerator = Fraction(1) + Fraction(1, 3) + Fraction(21, 64)
    square_root_output = square_root_numerator - Fraction(2, 3)
    strict_margin = Fraction(399, 400) - square_root_output
    if endpoint_ceiling != Fraction(1997, 1200):
        raise CheckFailure("endpoint numerator ceiling changed")
    if square_root_numerator != Fraction(319, 192):
        raise CheckFailure("square-root numerator changed")
    if square_root_output != Fraction(191, 192) or strict_margin != Fraction(13, 4800):
        raise CheckFailure("strict margin changed")

    analytic_x = 100
    rough_rows = ((2, 3), (2, 2))
    smooth_columns = ((16, 1), (2, 7))
    occurrence_kinds = ("E", "E", "F", "F")

    def tuple_product(values: tuple[int, ...]) -> int:
        product = 1
        for value in values:
            product *= value
        return product

    def v19_route(slots: tuple[int, ...], kinds: tuple[str, ...]) -> str:
        product = tuple_product(slots)
        if len(slots) != len(kinds):
            raise CheckFailure("V19 route arity changed")
        active = tuple(index for index, value in enumerate(slots) if value > 1)
        if not active:
            raise CheckFailure("V19 route lost all active slots")
        large = tuple(index for index in active if slots[index] ** 2 >= product)
        if large:
            first = large[0]
            complement = product // slots[first]
            if kinds[first] == "F" and complement**400 <= analytic_x**133:
                return "H2"
            group = complement if kinds[first] == "F" else slots[first]
        else:
            full_active_mask = sum(1 << index for index in active)
            group = 0
            for mask in range(1, 1 << len(slots)):
                if mask & ~full_active_mask or mask == full_active_mask:
                    continue
                candidate = tuple_product(
                    tuple(
                        slots[index]
                        for index in active
                        if mask & (1 << index)
                    )
                )
                if candidate**400 >= product**133 and candidate * candidate <= product:
                    group = candidate
                    break
            if not group:
                raise CheckFailure("V19 no-large route lost its first admissible mask")
        if not (group**400 > (analytic_x // 2) ** 133 and group * group <= analytic_x):
            raise CheckFailure("V19 MASTER group left the physical window")
        return "MASTER"

    route_factor_tuples = tuple(
        tuple(row + column for column in smooth_columns)
        for row in rough_rows
    )
    products = tuple(
        tuple(tuple_product(occurrence) for occurrence in row)
        for row in route_factor_tuples
    )
    route_types = tuple(
        tuple(v19_route(occurrence, occurrence_kinds) for occurrence in row)
        for row in route_factor_tuples
    )
    route_matrix = tuple(
        tuple(int(route == "MASTER") for route in row)
        for row in route_types
    )
    route_minor = route_matrix[0][0] * route_matrix[1][1] - route_matrix[0][1] * route_matrix[1][0]
    if (
        route_factor_tuples
        != (((2, 3, 16, 1), (2, 3, 2, 7)), ((2, 2, 16, 1), (2, 2, 2, 7)))
        or products != ((96, 84), (64, 56))
        or route_types != (("MASTER", "MASTER"), ("H2", "MASTER"))
        or route_minor != 1
        or any(not (50 < value <= analytic_x) for row in products for value in row)
    ):
        raise CheckFailure("MASTER selector falsifier changed")

    degenerate = (1, 6, 3, 3)
    degenerate_product = tuple_product(degenerate)
    degenerate_sign = -_mobius(degenerate[0]) * _mobius(degenerate[1])
    degenerate_route = v19_route(degenerate, occurrence_kinds)
    if (
        degenerate_product != 54
        or not (analytic_x // 2 < degenerate_product <= analytic_x)
        or degenerate_sign != -1
        or degenerate[2:] != (3, 3)
        or degenerate_route != "MASTER"
    ):
        raise CheckFailure("degenerate J2 witness changed")

    q5_solutions = [(x, y) for x in range(5) for y in range(5) if (x * y - 3) % 5 == 0]

    def constant_periodic_dft_support(q: int) -> tuple[int, ...]:
        support: list[int] = []
        for frequency in range(q):
            exponent_counts = [0] * q
            for residue in range(q):
                exponent_counts[(frequency * residue) % q] += 1
            if frequency == 0:
                if exponent_counts != [q] + [0] * (q - 1):
                    raise CheckFailure("constant DFT zero frequency changed")
                support.append(frequency)
            elif len(set(exponent_counts)) != 1:
                support.append(frequency)
        return tuple(support)

    q5_dft_support = constant_periodic_dft_support(5)
    q5_ramanujan_zero_axis = sum(1 for residue in range(5) if residue % 5)
    if len(q5_solutions) != 4 or q5_dft_support != (0,) or q5_ramanujan_zero_axis != 4:
        raise CheckFailure("q=5 zero-axis witness changed")

    q6_solutions = [(x, y) for x in range(6) for y in range(6) if (2 * x * y - 4) % 6 == 0]
    q6_units = [(x, y) for x, y in q6_solutions if x % 2 and x % 3 and y % 2 and y % 3]
    if len(q6_solutions) != 8 or len(q6_units) != 2:
        raise CheckFailure("q=6 nonunit witness changed")

    block_tail_ratio = Fraction(3**4, 8 * 2**4)
    if block_tail_ratio != Fraction(81, 128) or block_tail_ratio >= 1:
        raise CheckFailure("block bad-mass ratio changed")

    return {
        "normal_form_value": str(-multiplier_numerator / normalization),
        "normal_form_identity": True,
        "endpoint_numerator_ceiling": "1997/1200",
        "square_root_numerator": "319/192",
        "square_root_output": "191/192",
        "strict_margin": "13/4800",
        "route_factor_tuples": route_factor_tuples,
        "route_products": products,
        "route_types": route_types,
        "route_minor": route_minor,
        "degenerate_j2_product": degenerate_product,
        "degenerate_j2_route": degenerate_route,
        "q5_primal_solutions": len(q5_solutions),
        "q5_dft_support": q5_dft_support,
        "q5_zero_axis_mass": q5_ramanujan_zero_axis,
        "q6_all_solutions": len(q6_solutions),
        "q6_unit_solutions": len(q6_units),
        "single_event_series_exponent": 2,
        "block_bad_mass_tail_ratio": "81/128",
    }


def _make_trusted_runner(
    contract_seed: dict[str, object] = CONTRACT,
    registry_seed: tuple[tuple[str, str], ...] = REGISTRY_ITEMS,
    registry_digest_seed: str = EXPECTED_REGISTRY_SHA256,
    dependency_seed: tuple[tuple[str, str], ...] = DEPENDENCIES,
    fixture_seed: dict[str, object] = _finite_fixtures(),
    failure_type=CheckFailure,
    hash_constructor=hashlib.sha256,
    json_serializer=json.dumps,
    path_type=Path,
):
    literal_contract_items = tuple(contract_seed.items())
    literal_contract_keys = frozenset(key for key, _ in literal_contract_items)
    literal_registry = tuple(registry_seed)
    literal_registry_digest = registry_digest_seed
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

    def validate_contract(candidate: object) -> None:
        if type(candidate) is not dict:
            raise failure_type("contract must be a dict")
        if set(candidate) != literal_contract_keys:
            raise failure_type("contract key set changed")
        for key, expected in literal_contract_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"contract field {key} changed")

    def registry_digest(items: tuple[tuple[str, str], ...]) -> str:
        return local_sha256(local_canonical_json(list(items)))

    def validate_registry(candidate: object, claimed_digest: object) -> None:
        if type(candidate) is not tuple:
            raise failure_type("registry must be a tuple")
        if any(type(row) is not tuple or len(row) != 2 for row in candidate):
            raise failure_type("registry row shape changed")
        if any(type(k) is not str or type(v) is not str for k, v in candidate):
            raise failure_type("registry row type changed")
        if len(candidate) != len(literal_registry) or len({key for key, _ in candidate}) != len(candidate):
            raise failure_type("registry row count or uniqueness changed")
        if candidate != literal_registry:
            raise failure_type("registry semantic promotion")
        if type(claimed_digest) is not str or claimed_digest != literal_registry_digest:
            raise failure_type("registry literal digest changed")
        if registry_digest(candidate) != literal_registry_digest:
            raise failure_type("registry content digest changed")

    def validate_dependencies(candidate: object) -> None:
        if type(candidate) is not tuple or candidate != literal_dependencies:
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
        return count + 1

    def registry_mutations() -> int:
        count = 0
        for index, (key, value) in enumerate(literal_registry):
            changed = list(literal_registry)
            changed[index] = (key, value + "__PROMOTED")
            changed_tuple = tuple(changed)
            rebound = registry_digest(changed_tuple)
            must_reject(
                f"registry_value_{index+1}",
                lambda c=changed_tuple, d=rebound: validate_registry(c, d),
            )
            count += 1

            replaced = list(literal_registry)
            replaced[index] = (key + "__REPLACED", value)
            replaced_tuple = tuple(replaced)
            rebound = registry_digest(replaced_tuple)
            must_reject(
                f"registry_key_{index+1}",
                lambda c=replaced_tuple, d=rebound: validate_registry(c, d),
            )
            count += 1

        must_reject("registry_wrong_type", lambda: validate_registry(list(literal_registry), literal_registry_digest))
        must_reject("registry_false_release", lambda: validate_registry(literal_registry, "0" * 64))
        return count + 2

    def dependency_mutations() -> int:
        count = 0
        for index, (path, digest) in enumerate(literal_dependencies):
            changed_path = list(literal_dependencies)
            changed_path[index] = (path + ".wrong", digest)
            must_reject(f"dependency_path_{index+1}", lambda c=tuple(changed_path): validate_dependencies(c))
            count += 1
            changed_hash = list(literal_dependencies)
            changed_hash[index] = (path, "0" * 64)
            must_reject(f"dependency_hash_{index+1}", lambda c=tuple(changed_hash): validate_dependencies(c))
            count += 1
        return count

    expected_result_items = literal_fixture_items + (
        ("check", True),
        ("maximum_claim", literal_maximum_claim),
        ("route_advance", literal_route_advance),
        ("contract_fields", len(literal_contract_items)),
        ("registry_rows", len(literal_registry)),
        ("registry_sha256", literal_registry_digest),
        ("dependency_locks", len(literal_dependencies)),
        ("arithmetic_advance", False),
        ("fixed_atom_credit", 0),
        ("strict_1_over_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", False),
    )
    expected_result_keys = frozenset(key for key, _ in expected_result_items)
    expected_count_items = (
        ("contract_mutations", 3 * len(literal_contract_items) + 1),
        ("registry_mutations", 2 * len(literal_registry) + 2),
        ("dependency_mutations", 2 * len(literal_dependencies)),
    )
    expected_full_items = expected_result_items + expected_count_items
    expected_full_keys = frozenset(key for key, _ in expected_full_items)

    def validate_result(candidate: object) -> None:
        if type(candidate) is not dict or set(candidate) != expected_result_keys:
            raise failure_type("result schema changed")
        for key, expected in expected_result_items:
            value = candidate[key]
            if not exact_type(value, expected) or value != expected:
                raise failure_type(f"result field {key} changed")

    def trusted_run() -> dict[str, object]:
        validate_contract(dict(literal_contract_items))
        validate_registry(tuple(literal_registry), literal_registry_digest)
        validate_dependencies(tuple(literal_dependencies))
        result = dict(expected_result_items)
        validate_result(result)
        result["contract_mutations"] = contract_mutations()
        result["registry_mutations"] = registry_mutations()
        result["dependency_mutations"] = dependency_mutations()

        if tuple((key, result[key]) for key, _ in expected_full_items) != expected_full_items:
            raise failure_type("mutation execution counts changed")

        def validate_full(candidate: object) -> None:
            if type(candidate) is not dict or set(candidate) != expected_full_keys:
                raise failure_type("full result schema changed")
            for key, expected in expected_full_items:
                value = candidate[key]
                if not exact_type(value, expected) or value != expected:
                    raise failure_type(f"full result field {key} changed")

        validate_full(result)
        return result

    return trusted_run


_TRUSTED_RUN = _make_trusted_runner()


def _seal_runner(runner):
    def sealed() -> dict[str, object]:
        return runner()

    return sealed


run_check = _seal_runner(_TRUSTED_RUN)
del _seal_runner


def _seal_main(runner, argv_provider=sys.argv, serializer=json.dumps, failure_type=CheckFailure):
    def sealed(argv: list[str] | None = None) -> int:
        args = argv_provider[1:] if argv is None else argv
        if args != ["--check"]:
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
