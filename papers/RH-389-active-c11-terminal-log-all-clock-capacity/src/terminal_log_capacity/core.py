"""Exact finite compiler for RH-389.

The 602 certificate rows reproduce the Boolean projection, eight-action
weights, directed compatibility graph, charging algebra, and frozen analytic
interfaces.  They do not prove the cited analytic density or logarithmic
correlation theorems.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from typing import Iterable


TERNARY = (-1, 0, 1)
POINTS = tuple(product(TERNARY, repeat=2))
NONZERO_POINTS = tuple((x, z) for x, z in POINTS if z)
COEFFICIENT_NAMES = ("c01", "c02", "c11", "c12", "c21", "c22")
ACTION_MASKS = (0, 4, 32, 36, 256, 260, 288, 292)
ACTION_WEIGHT_PAIRS = (
    (Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(1, 2)),
    (Fraction(1), Fraction(-1)),
    (Fraction(1), Fraction(-1, 2)),
    (Fraction(0), Fraction(1, 2)),
    (Fraction(0), Fraction(1)),
    (Fraction(1), Fraction(-1, 2)),
    (Fraction(1), Fraction(0)),
)
BASELINE_ACTION_ID = 3
EXPECTED_COUNTS = {
    "truth_rows": 512,
    "action_rows": 8,
    "compatibility_rows": 64,
    "charge_rows": 8,
    "analytic_rows": 6,
    "scope_rows": 4,
    "total_rows": 602,
}
REPRODUCTION_LABEL = "finite_reproduction_not_analytic_proof"
MUTATION_NAMES = (
    "projection_keeps_z_minus",
    "projection_drops_z_plus",
    "negative_pointwise_gain",
    "wrong_input_reflection",
    "preimage_count_63",
    "wrong_delta_weight",
    "wrong_theta_weight",
    "wrong_active_c11_interpolation",
    "empty_left_not_all_targets",
    "nonempty_left_allows_plus_target",
    "nonempty_target_count_three",
    "missing_forced_empty_predecessor",
    "wrong_predecessor_offset",
    "noninjective_charge_map",
    "missing_theta_half_gain",
    "drop_predecessor_theta_term",
    "wrong_single_density_total",
    "wrong_pair_density_total",
    "disable_active_c11",
    "wrong_affine_determinant",
    "bounded_omega",
    "replace_terminal_log_by_cesaro",
    "allow_growing_q",
    "max_before_limit",
)


def _require_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an exact integer")
    return value


def fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    if type(value) is not str:
        raise TypeError("fraction must be serialized as exact text")
    return Fraction(value)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def payload_sha256(value: object) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[key], right[key]) for key in left)  # type: ignore[index]
    if type(left) is list:
        return len(left) == len(right) and all(  # type: ignore[arg-type]
            exact_equal(a, b) for a, b in zip(left, right)  # type: ignore[arg-type]
        )
    return left == right


def truth_values(table_id: int) -> tuple[int, ...]:
    table_id = _require_int(table_id, "table_id")
    if not 0 <= table_id < 512:
        raise ValueError("table_id must lie in [0,512)")
    return tuple(1 if (table_id >> index) & 1 else -1 for index in range(9))


def table_id_from_truth(values: Iterable[int]) -> int:
    values = tuple(values)
    if len(values) != 9 or any(type(value) is not int or value not in (-1, 1) for value in values):
        raise ValueError("truth vector must have nine exact signs")
    return sum(1 << index for index, value in enumerate(values) if value == 1)


def plus_point_indices(table_id: int) -> tuple[int, ...]:
    return tuple(index for index, value in enumerate(truth_values(table_id)) if value == 1)


def projected_table_id(table_id: int) -> int:
    values = truth_values(table_id)
    return sum(1 << index for index, ((_, z), value) in enumerate(zip(POINTS, values)) if z == 1 and value == 1)


def action_id_from_table(table_id: int) -> int:
    projected = projected_table_id(table_id)
    return sum(1 << action_index for action_index, point_index in enumerate((2, 5, 8)) if projected & (1 << point_index))


def action_values(action_id: int) -> tuple[int, ...]:
    action_id = _require_int(action_id, "action_id")
    if not 0 <= action_id < 8:
        raise ValueError("action_id must lie in [0,8)")
    return tuple(value for index, value in enumerate(TERNARY) if action_id & (1 << index))


@lru_cache(maxsize=512)
def table_plus_edges(table_id: int) -> frozenset[tuple[int, int]]:
    return frozenset(point for point, value in zip(POINTS, truth_values(table_id)) if value == 1)


def pointwise_zf_gains(table_id: int) -> tuple[int, ...]:
    original = truth_values(table_id)
    projected = truth_values(projected_table_id(table_id))
    return tuple(z * (new - old) for (_, z), old, new in zip(POINTS, original, projected))


def reflected_table_id(table_id: int) -> int:
    lookup = dict(zip(POINTS, truth_values(table_id)))
    return table_id_from_truth(lookup[(-x, -z)] for x, z in POINTS)


def _basis(x: int, z: int) -> tuple[int, ...]:
    return (z, z * z, x * z, x * z * z, x * x * z, x * x * z * z)


def _solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> tuple[Fraction, ...]:
    size = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column]), None)
        if pivot is None:
            raise ArithmeticError("singular interpolation matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [left - scale * right for left, right in zip(augmented[row], augmented[column])]
    return tuple(augmented[row][-1] for row in range(size))


@lru_cache(maxsize=512)
def coefficient_vector(table_id: int) -> tuple[Fraction, ...]:
    lookup = dict(zip(POINTS, truth_values(table_id)))
    matrix = [[Fraction(value) for value in _basis(x, z)] for x, z in NONZERO_POINTS]
    rhs = [Fraction(z * lookup[(x, z)]) for x, z in NONZERO_POINTS]
    return _solve(matrix, rhs)


def action_compatible(left_id: int, right_id: int) -> bool:
    left_id = _require_int(left_id, "left_id")
    right_id = _require_int(right_id, "right_id")
    if not 0 <= left_id < 8 or not 0 <= right_id < 8:
        raise ValueError("action identifiers must lie in [0,8)")
    return table_compatible(ACTION_MASKS[left_id], ACTION_MASKS[right_id])


def table_compatible(left_id: int, right_id: int) -> bool:
    left_edges = table_plus_edges(_require_int(left_id, "left_table_id"))
    right_edges = table_plus_edges(_require_int(right_id, "right_table_id"))
    return not any((z, w) in right_edges for _, z in left_edges for w in TERNARY)


@lru_cache(maxsize=1)
def _finite_symmetry_contracts_cached() -> tuple[dict[str, object], dict[str, object]]:
    compatible_pairs = 0
    projection_failures = 0
    reflection_failures = 0
    for left_id in range(512):
        for right_id in range(512):
            if not table_compatible(left_id, right_id):
                continue
            compatible_pairs += 1
            if not table_compatible(projected_table_id(left_id), projected_table_id(right_id)):
                projection_failures += 1
            if not table_compatible(reflected_table_id(left_id), reflected_table_id(right_id)):
                reflection_failures += 1
    sign_pattern = (1, -1, -1, 1, 1, -1)
    involution_failures = sum(reflected_table_id(reflected_table_id(table_id)) != table_id for table_id in range(512))
    coefficient_failures = 0
    for table_id in range(512):
        original = coefficient_vector(table_id)
        reflected = coefficient_vector(reflected_table_id(table_id))
        if reflected != tuple(sign * value for sign, value in zip(sign_pattern, original)):
            coefficient_failures += 1
    projection = {
        "compatible_original_pair_count": compatible_pairs,
        "ordered_table_pair_count": 512 * 512,
        "pass": compatible_pairs == 3375 and projection_failures == 0,
        "projection_compatibility_failures": projection_failures,
        "table_count": 512,
    }
    reflection = {
        "coefficient_parity_failure_count": coefficient_failures,
        "coefficient_sign_pattern": ["+", "-", "-", "+", "+", "-"],
        "compatible_original_pair_count": compatible_pairs,
        "involution_failure_count": involution_failures,
        "ordered_table_pair_count": 512 * 512,
        "pass": (
            compatible_pairs == 3375
            and reflection_failures == 0
            and involution_failures == 0
            and coefficient_failures == 0
        ),
        "reflection_compatibility_failure_count": reflection_failures,
        "table_count": 512,
    }
    return projection, reflection


def finite_symmetry_contracts() -> tuple[dict[str, object], dict[str, object]]:
    projection, reflection = _finite_symmetry_contracts_cached()
    return deepcopy(projection), deepcopy(reflection)


def _truth_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for table_id in range(512):
        truth = truth_values(table_id)
        projected = projected_table_id(table_id)
        gains = pointwise_zf_gains(table_id)
        rows.append({
            "all_pointwise_gains_nonnegative": all(gain >= 0 for gain in gains),
            "kind": "truth_projection",
            "pass": (
                set(plus_point_indices(projected)).issubset(plus_point_indices(table_id))
                and all(z == 1 for index, (_, z) in enumerate(POINTS) if projected & (1 << index))
                and all(gain >= 0 for gain in gains)
            ),
            "plus_point_indices": list(plus_point_indices(table_id)),
            "pointwise_zf_gains": list(gains),
            "projected_action_id": action_id_from_table(table_id),
            "projected_only_z_plus": all(z == 1 for index, (_, z) in enumerate(POINTS) if projected & (1 << index)),
            "projected_plus_subset": set(plus_point_indices(projected)).issubset(plus_point_indices(table_id)),
            "projected_table_id": projected,
            "reflected_table_id": reflected_table_id(table_id),
            "row_id": f"truth:{table_id:03d}",
            "table_id": table_id,
            "truth": list(truth),
        })
    return rows


def _action_rows() -> list[dict[str, object]]:
    preimages = [sum(action_id_from_table(table_id) == action_id for table_id in range(512)) for action_id in range(8)]
    rows: list[dict[str, object]] = []
    for action_id, mask in enumerate(ACTION_MASKS):
        coefficients = coefficient_vector(mask)
        weight = (coefficients[1], coefficients[5])
        target_count = sum(action_compatible(action_id, right_id) for right_id in range(8))
        rows.append({
            "action_id": action_id,
            "action_values": list(action_values(action_id)),
            "c02_delta_coefficient": fraction_text(coefficients[1]),
            "c22_theta_coefficient": fraction_text(coefficients[5]),
            "coefficient_names": list(COEFFICIENT_NAMES),
            "coefficients": [fraction_text(value) for value in coefficients],
            "compatible_target_count": target_count,
            "kind": "projected_action",
            "pass": mask == ACTION_MASKS[action_id] and preimages[action_id] == 64 and weight == ACTION_WEIGHT_PAIRS[action_id],
            "preimage_count": preimages[action_id],
            "projected_mask": mask,
            "row_id": f"action:{action_id}",
        })
    return rows


def _compatibility_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for left_id in range(8):
        for right_id in range(8):
            compatible = action_compatible(left_id, right_id)
            simplified = action_values(left_id) == () or 1 not in action_values(right_id)
            rows.append({
                "compatible": compatible,
                "edge_triple_recomputed": True,
                "kind": "directed_action_compatibility",
                "left_action_id": left_id,
                "left_empty": action_values(left_id) == (),
                "pass": compatible == simplified,
                "right_action_id": right_id,
                "right_contains_plus_one": 1 in action_values(right_id),
                "row_id": f"compat:{left_id}->{right_id}",
            })
    return rows


def _charge_semantics(action_id: int) -> dict[str, object]:
    delta, theta = ACTION_WEIGHT_PAIRS[action_id]
    base_delta, base_theta = ACTION_WEIGHT_PAIRS[BASELINE_ACTION_ID]
    relative_delta = delta - base_delta
    relative_theta = theta - base_theta
    contains_plus = 1 in action_values(action_id)
    cap = Fraction(1, 2) if contains_plus else Fraction(0)
    cone_delta_minus_theta = -relative_delta
    cone_theta = cap - relative_theta - relative_delta
    allowed_predecessors = [left_id for left_id in range(8) if action_compatible(left_id, action_id)]
    offset = -2 if contains_plus else None
    inverse_offset = 2 if contains_plus else None
    composition_offset = offset + inverse_offset if contains_plus else None
    translation_bijection = composition_offset == 0 if contains_plus else True
    decomposition = (Fraction(1, 2), Fraction(1, 2)) if contains_plus else (Fraction(0), Fraction(0))
    expanded = (
        decomposition[0] + decomposition[1],
        -decomposition[0],
        -decomposition[1],
    )
    target_expanded = (Fraction(1), Fraction(-1, 2), Fraction(-1, 2)) if contains_plus else (Fraction(0),) * 3
    forced_empty = allowed_predecessors == [0] if contains_plus else False
    phase_disjoint = forced_empty and 1 not in action_values(0) if contains_plus else True
    return {
        "action_id": action_id,
        "allowed_predecessor_action_ids": allowed_predecessors,
        "cap_theta_coefficient": fraction_text(cap),
        "composition_offset_mod_q": composition_offset,
        "contains_plus_one": contains_plus,
        "forced_predecessor_action_id": 0 if contains_plus else None,
        "forced_predecessor_empty": forced_empty,
        "gain_cap_cone_coefficients": [fraction_text(cone_delta_minus_theta), fraction_text(cone_theta)],
        "injective_predecessor_map": translation_bijection,
        "inverse_offset_mod_q": inverse_offset,
        "kind": "baseline_charge",
        "pass": (
            cone_delta_minus_theta >= 0
            and cone_theta >= 0
            and translation_bijection
            and expanded == target_expanded
            and phase_disjoint
        ),
        "predecessor_loss_decomposition": [fraction_text(value) for value in decomposition],
        "predecessor_loss_expanded_coefficients": [fraction_text(value) for value in expanded],
        "predecessor_loss_identity": "H_(r-2)-theta_r/2=(delta_(r-2)-theta_(r-2))/2+(delta_(r-2)-theta_r)/2" if contains_plus else "not_applicable",
        "predecessor_offset_mod_q": offset,
        "predecessor_pair_inclusions": ["theta_(r-2)<=delta_(r-2)", "theta_r<=delta_(r-2)"] if contains_plus else [],
        "plus_phase_disjointness": phase_disjoint,
        "plus_phase_disjointness_statement": "P intersect (P-2)=empty; q in {1,2} implies P=empty" if contains_plus else "not_applicable",
        "relative_delta_coefficient": fraction_text(relative_delta),
        "relative_theta_coefficient": fraction_text(relative_theta),
        "row_id": f"charge:{action_id}",
        "translation_domain": "Z/qZ" if contains_plus else "not_applicable",
    }


def _charge_data(action_id: int) -> dict[str, object]:
    return _charge_semantics(action_id)


def _charge_rows() -> list[dict[str, object]]:
    return [_charge_data(action_id) for action_id in range(8)]


def charge_global_contract() -> dict[str, object]:
    plus_actions = [action_id for action_id in range(8) if 1 in action_values(action_id)]
    rows = [_charge_semantics(action_id) for action_id in range(8)]
    unique_empty_predecessor = all(row["allowed_predecessor_action_ids"] == [0] for row in rows if row["contains_plus_one"])
    local_caps = all(row["pass"] is True for row in rows)
    translation = all(row["injective_predecessor_map"] is True for row in rows if row["contains_plus_one"])
    disjoint = all(row["plus_phase_disjointness"] is True for row in rows if row["contains_plus_one"])
    baseline_self_compatible = action_compatible(BASELINE_ACTION_ID, BASELINE_ACTION_ID)
    baseline_weight = ACTION_WEIGHT_PAIRS[BASELINE_ACTION_ID]
    self_loop_moduli = [q for q in range(1, 9) if (-2) % q == 0]
    no_plus_action_self_compatible = all(not action_compatible(action_id, action_id) for action_id in plus_actions)
    small_q_plus_set_empty = self_loop_moduli == [1, 2] and no_plus_action_self_compatible
    return {
        "baseline_action_id": BASELINE_ACTION_ID,
        "baseline_attains_for_every_fixed_q": baseline_self_compatible,
        "baseline_self_compatible": baseline_self_compatible,
        "baseline_total_from_density_sums": "6/pi^2-kappa2/2",
        "baseline_weight_pair": [fraction_text(value) for value in baseline_weight],
        "charge_conclusion": "sum phase weights <= sum_r [delta_(q,r)-theta_(q,r)/2]",
        "charged_empty_set": "P-2",
        "local_gain_caps_verified": local_caps,
        "pass": (
            plus_actions == [4, 5, 6, 7]
            and unique_empty_predecessor
            and local_caps
            and translation
            and disjoint
            and baseline_self_compatible
            and baseline_weight == (Fraction(1), Fraction(-1, 2))
            and small_q_plus_set_empty
        ),
        "plus_action_ids": plus_actions,
        "plus_phase_set": "P={r mod q: +1 belongs to A_r}",
        "plus_set_disjoint_from_charged_empty_set": disjoint,
        "plus_actions_self_incompatible": no_plus_action_self_compatible,
        "self_loop_moduli_for_offset_minus_two": self_loop_moduli,
        "small_q_plus_set_empty_verified": small_q_plus_set_empty,
        "translation_bijection_verified": translation,
        "unique_empty_predecessor_verified": unique_empty_predecessor,
    }


def _analytic_rows() -> list[dict[str, object]]:
    return [
        {
            "clock_quantifier": "q is fixed before X tends to infinity",
            "kind": "analytic_contract",
            "omega_limit": "omega(X)->infinity",
            "omega_range": "1<=omega(X)<=X",
            "pass": True,
            "row_id": "analytic:terminal_log_domain",
            "score": "(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n) f_(n mod q)(mu0(n-2),mu(n))/n",
            "table_quantifier": "f is fixed and q-periodic before X tends to infinity",
        },
        {
            "D": {"intercept": -2, "slope": 1},
            "V": {"intercept": 0, "slope": 1},
            "active_c11": True,
            "determinant": 2,
            "kind": "analytic_contract",
            "pass": 1 * 0 - 1 * (-2) == 2,
            "periodic_weight": "rho(n)=c11(n mod q), fixed and bounded",
            "row_id": "analytic:active_c11_tpc137",
            "source_role": "TPC-137 Theorem main/equation main gives full mu(D)mu(V) fixed-period terminal-log cancellation; Tao Theorem 2 equation (3) is its upstream Liouville input",
        },
        {
            "abel_channels": ["c01", "c02", "c12", "c21", "c22"],
            "kind": "analytic_contract",
            "limit_formula": "sum_(r mod q) [c02(r)*delta_(q,r)+c22(r)*theta_(q,r)]",
            "mobius_zero_channels": ["c01", "c12", "c21"],
            "nonzero_density_channels": ["c02", "c22"],
            "pass": True,
            "row_id": "analytic:abel_density_channels",
            "zero_padding": "mu0(m)=0 for m<=0 changes finitely many terms only",
        },
        {
            "inequalities": ["0<=theta_(q,r)<=delta_(q,r)", "theta_(q,r)<=delta_(q,r-2)"],
            "kind": "analytic_contract",
            "pair_density_total": "sum_(r mod q) theta_(q,r)=kappa2",
            "pair_product": "kappa2=prod_p(1-2/p^2)",
            "pass": True,
            "row_id": "analytic:density_ledger",
            "single_density_total": "sum_(r mod q) delta_(q,r)=6/pi^2",
        },
        {
            "attained_by": {"action_id": 3, "projected_mask": 36, "q": "every fixed q>=1", "set": [-1, 0], "table_id": 36},
            "charge_contract": charge_global_contract(),
            "charge_upper": "sum_r [delta_(q,r)-theta_(q,r)/2]",
            "kind": "analytic_contract",
            "pass": charge_global_contract()["pass"] is True and reflected_table_id(36) == 72,
            "reflected_witness_table_id": 72,
            "row_id": "analytic:capacity_optimizer",
            "signed_capacity": "6/pi^2-kappa2/2",
        },
        {
            "absolute_capacity": "G_log(q)=6/pi^2-kappa2/2 for every fixed q>=1",
            "global_reflection_contract": finite_symmetry_contracts()[1],
            "input_reflection": "f^rho_r(x,z)=f_r(-x,-z) preserves compatibility; c02,c11,c22 negate while c01,c12,c21 stay unchanged and have zero terminal limits",
            "kind": "analytic_contract",
            "limit_order": "first take the terminal-log limit for each fixed f, then maximize over the finite fixed-q safe family",
            "negative_witness": {"q": "every fixed q>=1", "table_id": 72},
            "pass": finite_symmetry_contracts()[1]["pass"] is True,
            "witness_coefficient_reflection": {
                "table_36": ["0", "1", "-1/2", "-1/2", "-1/2", "-1/2"],
                "table_72": ["0", "-1", "1/2", "-1/2", "-1/2", "1/2"],
            },
            "row_id": "analytic:reflection_and_absolute_max",
        },
    ]


def _scope_rows() -> list[dict[str, object]]:
    return [
        {
            "allowed": "every individually fixed q>=1",
            "forbidden": ["q=q(X)", "uniformity in growing q", "unrestricted simultaneous q"],
            "kind": "scope_firewall",
            "pass": True,
            "row_id": "scope:fixed_clock_only",
        },
        {
            "allowed": "terminal logarithmic average with admissible omega",
            "forbidden": ["ordinary Cesaro average", "all-prefix power saving", "effective rate"],
            "kind": "scope_firewall",
            "pass": True,
            "row_id": "scope:terminal_log_only",
        },
        {
            "allowed": "maximum of already-established fixed-table limits",
            "forbidden": ["max before limit", "projectively compatible selector", "K_N"],
            "kind": "scope_firewall",
            "pass": True,
            "row_id": "scope:limit_before_max",
        },
        {
            "allowed": "active c11 through the fixed TPC-137 theorem",
            "forbidden": ["operator", "trace", "zeros", "Riemann Hypothesis", "Gates A-E"],
            "gates": {"A": False, "B": False, "C": False, "D": False, "E": False},
            "kind": "scope_firewall",
            "pass": True,
            "row_id": "scope:no_operator_RH_gates",
        },
    ]


def _contracts() -> dict[str, object]:
    return {
        "action_masks": list(ACTION_MASKS),
        "action_weight_pairs": [[fraction_text(a), fraction_text(b)] for a, b in ACTION_WEIGHT_PAIRS],
        "baseline_action_id": BASELINE_ACTION_ID,
        "coefficient_names": list(COEFFICIENT_NAMES),
        "mutation_count": len(MUTATION_NAMES),
        "mutation_names": list(MUTATION_NAMES),
        "projection": "E_plus=E intersect (T x {+1})",
        "projection_global_contract": finite_symmetry_contracts()[0],
        "row_partition": [512, 8, 64, 8, 6, 4],
    }


def build_certificate() -> dict[str, object]:
    truth = _truth_rows()
    actions = _action_rows()
    compatibility = _compatibility_rows()
    charge = _charge_rows()
    analytic = _analytic_rows()
    scope = _scope_rows()
    contracts = _contracts()
    groups = (truth, actions, compatibility, charge, analytic, scope)
    return {
        "all_pass": (
            all(row["pass"] is True for group in groups for row in group)
            and contracts["projection_global_contract"]["pass"] is True  # type: ignore[index]
        ),
        "analytic_rows": analytic,
        "certificate_version": 1,
        "charge_rows": charge,
        "compatibility_rows": compatibility,
        "contracts": contracts,
        "counts": dict(EXPECTED_COUNTS),
        "epistemic_role": REPRODUCTION_LABEL,
        "projected_action_rows": actions,
        "scope_rows": scope,
        "status": "RH-389_active_c11_terminal_log_capacity_exact_certificate",
        "truth_rows": truth,
    }


def _keys(row: object, expected: set[str], label: str) -> dict[str, object]:
    if type(row) is not dict or set(row) != expected:
        raise ValueError(f"{label} row membership changed")
    return row


def _exact(value: object, expected: object, label: str) -> None:
    if not exact_equal(value, expected):
        raise ValueError(f"{label} changed")


def _validate_truth_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 512:
        raise ValueError("truth row count changed")
    expected_keys = {
        "all_pointwise_gains_nonnegative", "kind", "pass", "plus_point_indices",
        "pointwise_zf_gains", "projected_action_id", "projected_only_z_plus",
        "projected_plus_subset", "projected_table_id", "reflected_table_id",
        "row_id", "table_id", "truth",
    }
    for table_id, candidate in enumerate(rows):
        row = _keys(candidate, expected_keys, "truth")
        if type(row["table_id"]) is not int or row["table_id"] != table_id:
            raise ValueError("truth table id changed")
        truth = truth_values(table_id)
        projected = projected_table_id(table_id)
        plus = plus_point_indices(table_id)
        projected_plus = plus_point_indices(projected)
        gains = pointwise_zf_gains(table_id)
        subset = set(projected_plus).issubset(plus)
        only_plus = all(z == 1 for index, (_, z) in enumerate(POINTS) if projected & (1 << index))
        nonnegative = all(gain >= 0 for gain in gains)
        checks = {
            "row_id": f"truth:{table_id:03d}",
            "kind": "truth_projection",
            "truth": list(truth),
            "plus_point_indices": list(plus),
            "projected_table_id": projected,
            "projected_action_id": action_id_from_table(table_id),
            "projected_plus_subset": subset,
            "projected_only_z_plus": only_plus,
            "pointwise_zf_gains": list(gains),
            "all_pointwise_gains_nonnegative": nonnegative,
            "reflected_table_id": reflected_table_id(table_id),
            "pass": subset and only_plus and nonnegative,
        }
        for key, expected in checks.items():
            _exact(row[key], expected, f"truth {table_id} {key}")


def _validate_action_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 8:
        raise ValueError("action row count changed")
    expected_keys = {
        "action_id", "action_values", "c02_delta_coefficient", "c22_theta_coefficient",
        "coefficient_names", "coefficients", "compatible_target_count", "kind", "pass",
        "preimage_count", "projected_mask", "row_id",
    }
    preimages = [sum(action_id_from_table(table_id) == action_id for table_id in range(512)) for action_id in range(8)]
    for action_id, candidate in enumerate(rows):
        row = _keys(candidate, expected_keys, "action")
        if type(row["action_id"]) is not int or row["action_id"] != action_id:
            raise ValueError("action id changed")
        mask = ACTION_MASKS[action_id]
        coefficients = coefficient_vector(mask)
        weight = ACTION_WEIGHT_PAIRS[action_id]
        checks = {
            "row_id": f"action:{action_id}",
            "kind": "projected_action",
            "action_values": list(action_values(action_id)),
            "projected_mask": mask,
            "preimage_count": preimages[action_id],
            "coefficient_names": list(COEFFICIENT_NAMES),
            "coefficients": [fraction_text(value) for value in coefficients],
            "c02_delta_coefficient": fraction_text(coefficients[1]),
            "c22_theta_coefficient": fraction_text(coefficients[5]),
            "compatible_target_count": sum(action_compatible(action_id, right) for right in range(8)),
            "pass": preimages[action_id] == 64 and (coefficients[1], coefficients[5]) == weight,
        }
        for key, expected in checks.items():
            _exact(row[key], expected, f"action {action_id} {key}")


def _validate_compatibility_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 64:
        raise ValueError("compatibility row count changed")
    expected_keys = {
        "compatible", "edge_triple_recomputed", "kind", "left_action_id", "left_empty", "pass",
        "right_action_id", "right_contains_plus_one", "row_id",
    }
    for index, candidate in enumerate(rows):
        left_id, right_id = divmod(index, 8)
        row = _keys(candidate, expected_keys, "compatibility")
        brute_compatible = action_compatible(left_id, right_id)
        simplified = not action_values(left_id) or 1 not in action_values(right_id)
        checks = {
            "row_id": f"compat:{left_id}->{right_id}",
            "kind": "directed_action_compatibility",
            "left_action_id": left_id,
            "right_action_id": right_id,
            "left_empty": action_values(left_id) == (),
            "right_contains_plus_one": 1 in action_values(right_id),
            "compatible": brute_compatible,
            "edge_triple_recomputed": True,
            "pass": brute_compatible == simplified,
        }
        for key, expected in checks.items():
            _exact(row[key], expected, f"compatibility {left_id}->{right_id} {key}")


def _validate_charge_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 8:
        raise ValueError("charge row count changed")
    expected_keys = {
        "action_id", "allowed_predecessor_action_ids", "cap_theta_coefficient",
        "composition_offset_mod_q", "contains_plus_one",
        "forced_predecessor_action_id", "forced_predecessor_empty",
        "gain_cap_cone_coefficients", "injective_predecessor_map", "inverse_offset_mod_q", "kind", "pass",
        "predecessor_loss_decomposition", "predecessor_loss_expanded_coefficients",
        "predecessor_loss_identity", "predecessor_offset_mod_q",
        "predecessor_pair_inclusions", "plus_phase_disjointness", "plus_phase_disjointness_statement",
        "relative_delta_coefficient", "relative_theta_coefficient", "row_id",
        "translation_domain",
    }
    for action_id, candidate in enumerate(rows):
        row = _keys(candidate, expected_keys, "charge")
        if type(row["action_id"]) is not int or row["action_id"] != action_id:
            raise ValueError("charge action id changed")
        _exact(row, _charge_semantics(action_id), f"charge {action_id}")


def _analytic_contracts_for_validation() -> dict[str, dict[str, object]]:
    rows = {
        "analytic:terminal_log_domain": {
            "clock_quantifier": "q is fixed before X tends to infinity",
            "kind": "analytic_contract",
            "omega_limit": "omega(X)->infinity",
            "omega_range": "1<=omega(X)<=X",
            "pass": True,
            "row_id": "analytic:terminal_log_domain",
            "score": "(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n) f_(n mod q)(mu0(n-2),mu(n))/n",
            "table_quantifier": "f is fixed and q-periodic before X tends to infinity",
        },
        "analytic:active_c11_tpc137": {
            "D": {"intercept": -2, "slope": 1},
            "V": {"intercept": 0, "slope": 1},
            "active_c11": True,
            "determinant": 2,
            "kind": "analytic_contract",
            "pass": True,
            "periodic_weight": "rho(n)=c11(n mod q), fixed and bounded",
            "row_id": "analytic:active_c11_tpc137",
            "source_role": "TPC-137 Theorem main/equation main gives full mu(D)mu(V) fixed-period terminal-log cancellation; Tao Theorem 2 equation (3) is its upstream Liouville input",
        },
        "analytic:abel_density_channels": {
            "abel_channels": ["c01", "c02", "c12", "c21", "c22"],
            "kind": "analytic_contract",
            "limit_formula": "sum_(r mod q) [c02(r)*delta_(q,r)+c22(r)*theta_(q,r)]",
            "mobius_zero_channels": ["c01", "c12", "c21"],
            "nonzero_density_channels": ["c02", "c22"],
            "pass": True,
            "row_id": "analytic:abel_density_channels",
            "zero_padding": "mu0(m)=0 for m<=0 changes finitely many terms only",
        },
        "analytic:density_ledger": {
            "inequalities": ["0<=theta_(q,r)<=delta_(q,r)", "theta_(q,r)<=delta_(q,r-2)"],
            "kind": "analytic_contract",
            "pair_density_total": "sum_(r mod q) theta_(q,r)=kappa2",
            "pair_product": "kappa2=prod_p(1-2/p^2)",
            "pass": True,
            "row_id": "analytic:density_ledger",
            "single_density_total": "sum_(r mod q) delta_(q,r)=6/pi^2",
        },
        "analytic:capacity_optimizer": {
            "attained_by": {"action_id": 3, "projected_mask": 36, "q": "every fixed q>=1", "set": [-1, 0], "table_id": 36},
            "charge_contract": charge_global_contract(),
            "charge_upper": "sum_r [delta_(q,r)-theta_(q,r)/2]",
            "kind": "analytic_contract",
            "pass": True,
            "reflected_witness_table_id": 72,
            "row_id": "analytic:capacity_optimizer",
            "signed_capacity": "6/pi^2-kappa2/2",
        },
        "analytic:reflection_and_absolute_max": {
            "absolute_capacity": "G_log(q)=6/pi^2-kappa2/2 for every fixed q>=1",
            "global_reflection_contract": finite_symmetry_contracts()[1],
            "input_reflection": "f^rho_r(x,z)=f_r(-x,-z) preserves compatibility; c02,c11,c22 negate while c01,c12,c21 stay unchanged and have zero terminal limits",
            "kind": "analytic_contract",
            "limit_order": "first take the terminal-log limit for each fixed f, then maximize over the finite fixed-q safe family",
            "negative_witness": {"q": "every fixed q>=1", "table_id": 72},
            "pass": finite_symmetry_contracts()[1]["pass"] is True,
            "row_id": "analytic:reflection_and_absolute_max",
            "witness_coefficient_reflection": {
                "table_36": ["0", "1", "-1/2", "-1/2", "-1/2", "-1/2"],
                "table_72": ["0", "-1", "1/2", "-1/2", "-1/2", "1/2"],
            },
        },
    }
    rows["analytic:active_c11_tpc137"]["pass"] = (
        rows["analytic:active_c11_tpc137"]["D"]["slope"] * rows["analytic:active_c11_tpc137"]["V"]["intercept"]  # type: ignore[index,operator]
        - rows["analytic:active_c11_tpc137"]["V"]["slope"] * rows["analytic:active_c11_tpc137"]["D"]["intercept"]  # type: ignore[index,operator]
        == rows["analytic:active_c11_tpc137"]["determinant"]
    )
    rows["analytic:capacity_optimizer"]["pass"] = charge_global_contract()["pass"] is True and reflected_table_id(36) == 72
    return rows


def _validate_analytic_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 6:
        raise ValueError("analytic row count changed")
    expected = _analytic_contracts_for_validation()
    expected_order = list(expected)
    for index, candidate in enumerate(rows):
        if type(candidate) is not dict or candidate.get("row_id") != expected_order[index]:
            raise ValueError("analytic row order changed")
        _exact(candidate, expected[expected_order[index]], f"analytic {expected_order[index]}")


def _scope_contracts_for_validation() -> dict[str, dict[str, object]]:
    return {
        "scope:fixed_clock_only": {
            "allowed": "every individually fixed q>=1",
            "forbidden": ["q=q(X)", "uniformity in growing q", "unrestricted simultaneous q"],
            "kind": "scope_firewall", "pass": True, "row_id": "scope:fixed_clock_only",
        },
        "scope:terminal_log_only": {
            "allowed": "terminal logarithmic average with admissible omega",
            "forbidden": ["ordinary Cesaro average", "all-prefix power saving", "effective rate"],
            "kind": "scope_firewall", "pass": True, "row_id": "scope:terminal_log_only",
        },
        "scope:limit_before_max": {
            "allowed": "maximum of already-established fixed-table limits",
            "forbidden": ["max before limit", "projectively compatible selector", "K_N"],
            "kind": "scope_firewall", "pass": True, "row_id": "scope:limit_before_max",
        },
        "scope:no_operator_RH_gates": {
            "allowed": "active c11 through the fixed TPC-137 theorem",
            "forbidden": ["operator", "trace", "zeros", "Riemann Hypothesis", "Gates A-E"],
            "gates": {"A": False, "B": False, "C": False, "D": False, "E": False},
            "kind": "scope_firewall", "pass": True, "row_id": "scope:no_operator_RH_gates",
        },
    }


def _validate_scope_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 4:
        raise ValueError("scope row count changed")
    expected = _scope_contracts_for_validation()
    for index, (row_id, contract) in enumerate(expected.items()):
        _exact(rows[index], contract, f"scope {row_id}")


def _validate_contracts(value: object) -> None:
    if type(value) is not dict or set(value) != {
        "action_masks", "action_weight_pairs", "baseline_action_id", "coefficient_names",
        "mutation_count", "mutation_names", "projection", "projection_global_contract", "row_partition",
    }:
        raise ValueError("contract membership changed")
    expected = {
        "action_masks": list(ACTION_MASKS),
        "action_weight_pairs": [[fraction_text(a), fraction_text(b)] for a, b in ACTION_WEIGHT_PAIRS],
        "baseline_action_id": 3,
        "coefficient_names": list(COEFFICIENT_NAMES),
        "mutation_count": 24,
        "mutation_names": list(MUTATION_NAMES),
        "projection": "E_plus=E intersect (T x {+1})",
        "projection_global_contract": finite_symmetry_contracts()[0],
        "row_partition": [512, 8, 64, 8, 6, 4],
    }
    _exact(value, expected, "contracts")


def _validate_certificate(certificate: object) -> None:
    if type(certificate) is not dict or set(certificate) != {
        "all_pass", "analytic_rows", "certificate_version", "charge_rows",
        "compatibility_rows", "contracts", "counts", "epistemic_role",
        "projected_action_rows", "scope_rows", "status", "truth_rows",
    }:
        raise ValueError("certificate membership changed")
    _exact(certificate["status"], "RH-389_active_c11_terminal_log_capacity_exact_certificate", "status")
    _exact(certificate["epistemic_role"], REPRODUCTION_LABEL, "epistemic role")
    _exact(certificate["certificate_version"], 1, "certificate version")
    _exact(certificate["counts"], EXPECTED_COUNTS, "counts")
    _validate_contracts(certificate["contracts"])
    _validate_truth_rows(certificate["truth_rows"])
    _validate_action_rows(certificate["projected_action_rows"])
    _validate_compatibility_rows(certificate["compatibility_rows"])
    _validate_charge_rows(certificate["charge_rows"])
    _validate_analytic_rows(certificate["analytic_rows"])
    _validate_scope_rows(certificate["scope_rows"])
    all_rows = (
        certificate["truth_rows"] + certificate["projected_action_rows"]  # type: ignore[operator]
        + certificate["compatibility_rows"] + certificate["charge_rows"]  # type: ignore[operator]
        + certificate["analytic_rows"] + certificate["scope_rows"]  # type: ignore[operator]
    )
    expected_all_pass = (
        len(all_rows) == 602
        and all(row["pass"] is True for row in all_rows)
        and certificate["contracts"]["projection_global_contract"]["pass"] is True  # type: ignore[index]
    )
    _exact(certificate["all_pass"], expected_all_pass, "all_pass")


def verify_certificate(certificate: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact Boolean")
    try:
        _validate_certificate(certificate)
    except (ArithmeticError, KeyError, TypeError, ValueError):
        return False
    if compare_fresh and not exact_equal(certificate, build_certificate()):
        return False
    return True


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(certificate) is not dict or type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    candidate = deepcopy(certificate)
    truth = candidate["truth_rows"]  # type: ignore[assignment]
    actions = candidate["projected_action_rows"]  # type: ignore[assignment]
    compat = candidate["compatibility_rows"]  # type: ignore[assignment]
    charge = candidate["charge_rows"]  # type: ignore[assignment]
    analytic = candidate["analytic_rows"]  # type: ignore[assignment]
    scope = candidate["scope_rows"]  # type: ignore[assignment]
    if name == "projection_keeps_z_minus":
        truth[1]["projected_table_id"] = 1
    elif name == "projection_drops_z_plus":
        truth[4]["projected_table_id"] = 0
    elif name == "negative_pointwise_gain":
        truth[1]["pointwise_zf_gains"][0] = -2
    elif name == "wrong_input_reflection":
        truth[36]["reflected_table_id"] = 73
    elif name == "preimage_count_63":
        actions[0]["preimage_count"] = 63
    elif name == "wrong_delta_weight":
        actions[3]["c02_delta_coefficient"] = "0"
    elif name == "wrong_theta_weight":
        actions[3]["c22_theta_coefficient"] = "-1"
    elif name == "wrong_active_c11_interpolation":
        actions[1]["coefficients"][2] = "0"
    elif name == "empty_left_not_all_targets":
        compat[7]["compatible"] = False
    elif name == "nonempty_left_allows_plus_target":
        compat[8 + 4]["compatible"] = True
    elif name == "nonempty_target_count_three":
        actions[1]["compatible_target_count"] = 3
    elif name == "missing_forced_empty_predecessor":
        charge[4]["allowed_predecessor_action_ids"] = [0, 1]
        charge[4]["forced_predecessor_empty"] = False
    elif name == "wrong_predecessor_offset":
        charge[4]["predecessor_offset_mod_q"] = 2
    elif name == "noninjective_charge_map":
        charge[4]["inverse_offset_mod_q"] = -2
    elif name == "missing_theta_half_gain":
        charge[7]["cap_theta_coefficient"] = "0"
    elif name == "drop_predecessor_theta_term":
        charge[4]["predecessor_loss_decomposition"][1] = "0"
    elif name == "wrong_single_density_total":
        analytic[3]["single_density_total"] = "sum_(r mod q) delta_(q,r)=1"
    elif name == "wrong_pair_density_total":
        analytic[3]["pair_density_total"] = "sum_(r mod q) theta_(q,r)=1"
    elif name == "disable_active_c11":
        analytic[1]["active_c11"] = False
    elif name == "wrong_affine_determinant":
        analytic[1]["determinant"] = 1
    elif name == "bounded_omega":
        analytic[0]["omega_limit"] = "omega(X)=1"
    elif name == "replace_terminal_log_by_cesaro":
        scope[1]["allowed"] = "ordinary Cesaro average"
    elif name == "allow_growing_q":
        scope[0]["allowed"] = "q=q(X)"
    elif name == "max_before_limit":
        scope[2]["allowed"] = "maximize before taking the limit"
    return candidate
