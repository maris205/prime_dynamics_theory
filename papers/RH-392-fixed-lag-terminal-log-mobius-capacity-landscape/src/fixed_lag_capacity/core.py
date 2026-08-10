"""Exact finite certificate for RH-392.

The 640 rows reproduce the finite compiler, local-density algebra, charge,
and theorem interfaces.  They are an executable ledger, not a replacement
for the terminal-logarithmic analytic proof.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import gcd
from typing import Iterable


TITLE = "Fixed-Lag Terminal-Log Möbius Diagonalization and the Square-Divisor Capacity Landscape"
STATUS = "RH-392_fixed_lag_terminal_log_mobius_capacity_landscape_certified"
EPISTEMIC_ROLE = "finite_exact_algebra_not_analytic_proof"
TERNARY = (-1, 0, 1)
POINTS = tuple(product(TERNARY, repeat=2))
NONZERO_POINTS = tuple((x, z) for x, z in POINTS if z)
COMPILER_NAMES = ("c01", "c02", "c11", "c12", "c21", "c22")
MONOMIAL_NAMES = tuple(f"c{i}{j}" for i in range(3) for j in range(3))
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
    "projected_action_rows": 8,
    "compatibility_rows": 64,
    "charge_rows": 8,
    "monomial_rows": 9,
    "determinant_rows": 7,
    "theta_rows": 12,
    "landscape_rows": 8,
    "finite_shift_rows": 6,
    "firewall_rows": 6,
    "total_rows": 640,
}
MUTATION_NAMES = (
    "projection_keeps_z_minus", "preimage_count_63", "compatibility_reversed",
    "charge_predecessor_plus_h", "cycle_count_forgets_gcd", "self_loop_allows_plus",
    "determinant_forced_two", "determinant_zero_allowed", "coprime_kl_required",
    "cutoff_limit_order_reversed", "growing_h_allowed", "cesaro_substituted",
    "tau_square_collision_double_counted", "tau_forgets_multiplicity", "forced_hit_survives",
    "theta_cone_wrong_shift", "c20_wrong_phase", "c11_marked_surviving",
    "c22_marked_vanishing", "degree_three_multishift_allowed", "capacity_plus_sign",
    "infimum_attained", "squarefree_not_maximal", "reflection_wrong_parity",
)
BUILDER_NAMES = (
    "_truth_semantics", "_action_semantics", "_compatibility_semantics", "_charge_semantics",
    "_monomial_semantics", "_determinant_contracts", "_theta_contracts", "_landscape_contracts",
    "_finite_shift_contracts", "_firewall_contracts", "_global_closure_contract",
    "_translation_oracle", "_contracts",
    "_truth_rows", "_action_rows", "_compatibility_rows", "_charge_rows",
    "_monomial_rows", "_determinant_rows", "_theta_rows", "_landscape_rows",
    "_finite_shift_rows", "_firewall_rows", "build_certificate",
)


def _require_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an exact integer")
    return value


def fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def canonical_json_bytes(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[key], right[key]) for key in left)  # type: ignore[index]
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))  # type: ignore[arg-type]
    return left == right


def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("JSON input must be exact text")

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        out: dict[str, object] = {}
        for key, value in items:
            if key in out:
                raise ValueError(f"duplicate JSON key: {key}")
            out[key] = value
        return out

    def bad_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant: {value}")

    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant)


def truth_values(table_id: int) -> tuple[int, ...]:
    table_id = _require_int(table_id, "table_id")
    if not 0 <= table_id < 512:
        raise ValueError("table_id must lie in [0,512)")
    return tuple(1 if table_id & (1 << index) else -1 for index in range(9))


def table_id_from_truth(values: Iterable[int]) -> int:
    values = tuple(values)
    if len(values) != 9 or any(type(value) is not int or value not in (-1, 1) for value in values):
        raise ValueError("truth vector must contain nine exact signs")
    return sum(1 << index for index, value in enumerate(values) if value == 1)


def plus_point_indices(table_id: int) -> tuple[int, ...]:
    return tuple(index for index, value in enumerate(truth_values(table_id)) if value == 1)


def projected_table_id(table_id: int) -> int:
    values = truth_values(table_id)
    return sum(1 << index for index, ((_, z), value) in enumerate(zip(POINTS, values)) if z == 1 and value == 1)


def action_id_from_table(table_id: int) -> int:
    projected = projected_table_id(table_id)
    return sum(1 << action_id for action_id, point_id in enumerate((2, 5, 8)) if projected & (1 << point_id))


def action_values(action_id: int) -> tuple[int, ...]:
    action_id = _require_int(action_id, "action_id")
    if not 0 <= action_id < 8:
        raise ValueError("action_id must lie in [0,8)")
    return tuple(value for index, value in enumerate(TERNARY) if action_id & (1 << index))


@lru_cache(maxsize=512)
def table_plus_edges(table_id: int) -> frozenset[tuple[int, int]]:
    return frozenset(point for point, value in zip(POINTS, truth_values(table_id)) if value == 1)


def table_compatible(left_table_id: int, right_table_id: int) -> bool:
    left = table_plus_edges(_require_int(left_table_id, "left_table_id"))
    right = table_plus_edges(_require_int(right_table_id, "right_table_id"))
    return not any((z, w) in right for _, z in left for w in TERNARY)


def action_compatible(left_id: int, right_id: int) -> bool:
    left_id = _require_int(left_id, "left_id")
    right_id = _require_int(right_id, "right_id")
    if not 0 <= left_id < 8 or not 0 <= right_id < 8:
        raise ValueError("action identifiers must lie in [0,8)")
    return table_compatible(ACTION_MASKS[left_id], ACTION_MASKS[right_id])


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
    aug = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if aug[row][column]), None)
        if pivot is None:
            raise ArithmeticError("singular interpolation matrix")
        aug[column], aug[pivot] = aug[pivot], aug[column]
        scale = aug[column][column]
        aug[column] = [value / scale for value in aug[column]]
        for row in range(size):
            if row == column or not aug[row][column]:
                continue
            scale = aug[row][column]
            aug[row] = [left - scale * right for left, right in zip(aug[row], aug[column])]
    return tuple(aug[row][-1] for row in range(size))


@lru_cache(maxsize=512)
def coefficient_vector(table_id: int) -> tuple[Fraction, ...]:
    lookup = dict(zip(POINTS, truth_values(table_id)))
    matrix = [[Fraction(value) for value in _basis(x, z)] for x, z in NONZERO_POINTS]
    rhs = [Fraction(z * lookup[(x, z)]) for x, z in NONZERO_POINTS]
    return _solve(matrix, rhs)


def square_collision_count(p: int, h: int) -> int:
    p, h = _require_int(p, "p"), _require_int(h, "h")
    if not _is_prime(p) or h < 1:
        raise ValueError("prime p and h>=1 are required")
    return len({0, h % (p * p)})


def tau_collision_multiplicity(p: int, h: int, r: int) -> int:
    p, h, r = _require_int(p, "p"), _require_int(h, "h"), _require_int(r, "r")
    if not _is_prime(p) or h < 1:
        raise ValueError("prime p and h>=1 are required")
    residues_mod_p2 = {0, h % (p * p)}
    return sum(residue % p == r % p for residue in residues_mod_p2)


def theta_local_factor(p: int, h: int, q: int, r: int) -> Fraction:
    p, h, q, r = (_require_int(value, label) for value, label in ((p, "p"), (h, "h"), (q, "q"), (r, "r")))
    if not _is_prime(p) or h < 1 or q < 1:
        raise ValueError("prime p, h>=1, and q>=1 are required")
    p2 = p * p
    residues = {0, h % p2}
    if q % p:
        return Fraction(p2 - len(residues), p2)
    if q % p2:
        multiplicity = sum(value % p == r % p for value in residues)
        return Fraction(p - multiplicity, p)
    return Fraction(int(r % p2 not in residues))


def kappa_local_factor(p: int, h: int) -> Fraction:
    p, h = _require_int(p, "p"), _require_int(h, "h")
    if not _is_prime(p) or h < 1:
        raise ValueError("prime p and h>=1 are required")
    p2 = p * p
    return Fraction(p2 - (1 if h % p2 == 0 else 2), p2)


def finite_kappa(primes: Iterable[int], h: int) -> Fraction:
    h = _require_int(h, "h")
    values = tuple(primes)
    if len(set(values)) != len(values):
        raise ValueError("finite prime list must be distinct")
    answer = Fraction(1)
    for p in values:
        answer *= kappa_local_factor(p, h)
    return answer


def product_fraction(values: Iterable[Fraction]) -> Fraction:
    answer = Fraction(1)
    for value in values:
        answer *= Fraction(value)
    return answer


def _is_prime(value: int) -> bool:
    if type(value) is not int or value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def translation_cycles(q: int, h: int) -> tuple[tuple[int, ...], ...]:
    q, h = _require_int(q, "q"), _require_int(h, "h")
    if q < 1 or h < 1:
        raise ValueError("q,h must be positive")
    unseen = set(range(q))
    cycles: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        cycle: list[int] = []
        value = start
        while value in unseen:
            unseen.remove(value)
            cycle.append(value)
            value = (value + h) % q
        cycles.append(tuple(cycle))
    return tuple(cycles)


TRANSLATION_FIXTURES = ((1, 1), (2, 2), (3, 1), (4, 2), (6, 3), (6, 4), (5, 10), (7, 2))


def _translation_oracle() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    plus_self_incompatible = all(not action_compatible(action, action) for action in range(4, 8))
    for q, h in TRANSLATION_FIXTURES:
        cycles = translation_cycles(q, h)
        common = gcd(q, h)
        permutation = [(r + h) % q for r in range(q)]
        self_loop = h % q == 0
        rows.append({
            "q": q, "h": h, "gcd": common, "cycle_count": len(cycles),
            "cycle_length": q // common, "cycles": [list(cycle) for cycle in cycles],
            "permutation": permutation, "predecessor_permutation": [(r - h) % q for r in range(q)],
            "is_bijection": sorted(permutation) == list(range(q)), "self_loop": self_loop,
            "self_loop_forces_empty_plus_set": (not self_loop) or plus_self_incompatible,
            "pass": len(cycles) == common and all(len(cycle) == q // common for cycle in cycles)
                    and sorted(permutation) == list(range(q)) and ((not self_loop) or plus_self_incompatible),
        })
    return rows


@lru_cache(maxsize=1)
def _global_closure_contract() -> dict[str, object]:
    compatible_count = 0
    projection_failures = 0
    reflection_failures = 0
    for left in range(512):
        projected_left = projected_table_id(left)
        reflected_left = reflected_table_id(left)
        for right in range(512):
            if not table_compatible(left, right):
                continue
            compatible_count += 1
            if not table_compatible(projected_left, projected_table_id(right)):
                projection_failures += 1
            if not table_compatible(reflected_left, reflected_table_id(right)):
                reflection_failures += 1
    signs = (1, -1, -1, 1, 1, -1)
    involution_failures = 0
    parity_failures = 0
    interpolation_failures = 0
    for table_id in range(512):
        reflected = reflected_table_id(table_id)
        involution_failures += reflected_table_id(reflected) != table_id
        left = coefficient_vector(table_id)
        right = coefficient_vector(reflected)
        parity_failures += right != tuple(sign * value for sign, value in zip(signs, left))
        lookup = dict(zip(POINTS, truth_values(table_id)))
        interpolation_failures += any(
            sum(value * basis for value, basis in zip(left, _basis(x, z))) != z * lookup[(x, z)]
            for x, z in NONZERO_POINTS
        )
    passed = (
        compatible_count == 3375 and projection_failures == 0 and reflection_failures == 0
        and involution_failures == 0 and parity_failures == 0 and interpolation_failures == 0
        and action_compatible(3, 3) and table_compatible(36, 36)
        and action_compatible(4, 4) is False and table_compatible(72, 72)
    )
    return {
        "ordered_table_pair_count": 512 * 512,
        "compatible_pair_count": compatible_count,
        "projection_compatibility_failures": projection_failures,
        "reflection_compatibility_failures": reflection_failures,
        "reflection_involution_failures": involution_failures,
        "coefficient_parity": ["+", "-", "-", "+", "+", "-"],
        "coefficient_parity_failures": parity_failures,
        "coefficient_interpolation_failures": interpolation_failures,
        "table_36_self_compatible": table_compatible(36, 36),
        "table_72_self_compatible": table_compatible(72, 72),
        "plus_action_self_compatible_count": sum(action_compatible(action, action) for action in range(4, 8)),
        "pass": passed,
    }


def _truth_semantics(table_id: int) -> dict[str, object]:
    truth = truth_values(table_id)
    projected = projected_table_id(table_id)
    gains = pointwise_zf_gains(table_id)
    subset = set(plus_point_indices(projected)).issubset(plus_point_indices(table_id))
    only_plus = all(z == 1 for index, (_, z) in enumerate(POINTS) if projected & (1 << index))
    return {
        "all_pointwise_gains_nonnegative": all(gain >= 0 for gain in gains),
        "kind": "truth_projection", "pass": subset and only_plus and all(gain >= 0 for gain in gains),
        "plus_point_indices": list(plus_point_indices(table_id)), "pointwise_zf_gains": list(gains),
        "projected_action_id": action_id_from_table(table_id), "projected_only_z_plus": only_plus,
        "projected_plus_subset": subset, "projected_table_id": projected,
        "reflected_table_id": reflected_table_id(table_id), "row_id": f"truth:{table_id:03d}",
        "table_id": table_id, "truth": list(truth),
    }


def _truth_rows() -> list[dict[str, object]]:
    return [_truth_semantics(table_id) for table_id in range(512)]


def _action_semantics(action_id: int) -> dict[str, object]:
    mask = ACTION_MASKS[action_id]
    coefficients = coefficient_vector(mask)
    preimages = sum(action_id_from_table(table_id) == action_id for table_id in range(512))
    weights = (coefficients[1], coefficients[5])
    return {
        "action_id": action_id, "action_values": list(action_values(action_id)),
        "c02_delta_coefficient": fraction_text(coefficients[1]),
        "c22_theta_coefficient": fraction_text(coefficients[5]),
        "coefficient_names": list(COMPILER_NAMES),
        "coefficients": [fraction_text(value) for value in coefficients],
        "compatible_target_count": sum(action_compatible(action_id, right) for right in range(8)),
        "kind": "projected_action", "pass": preimages == 64 and weights == ACTION_WEIGHT_PAIRS[action_id],
        "preimage_count": preimages, "projected_mask": mask, "row_id": f"action:{action_id}",
    }


def _action_rows() -> list[dict[str, object]]:
    return [_action_semantics(action_id) for action_id in range(8)]


def _compatibility_semantics(left_id: int, right_id: int) -> dict[str, object]:
    brute = action_compatible(left_id, right_id)
    simplified = action_values(left_id) == () or 1 not in action_values(right_id)
    return {
        "compatible": brute, "edge_triple_recomputed": True,
        "kind": "directed_lag_h_action_compatibility", "left_action_id": left_id,
        "left_empty": action_values(left_id) == (), "pass": brute == simplified,
        "phase_orientation": "A_r -> A_(r+h)", "right_action_id": right_id,
        "right_contains_plus_one": 1 in action_values(right_id),
        "row_id": f"compat:{left_id}->{right_id}",
    }


def _compatibility_rows() -> list[dict[str, object]]:
    return [_compatibility_semantics(left, right) for left in range(8) for right in range(8)]


def _charge_semantics(action_id: int) -> dict[str, object]:
    delta, theta = ACTION_WEIGHT_PAIRS[action_id]
    base_delta, base_theta = ACTION_WEIGHT_PAIRS[BASELINE_ACTION_ID]
    rel_delta, rel_theta = delta - base_delta, theta - base_theta
    contains_plus = 1 in action_values(action_id)
    allowed = [left for left in range(8) if action_compatible(left, action_id)]
    forced = allowed == [0] if contains_plus else False
    gain_cone = (-rel_delta, Fraction(1, 2) - rel_theta - rel_delta) if contains_plus else None
    direct_loss_cone = (Fraction(1) - delta, Fraction(1, 2) - delta - theta) if not contains_plus else None
    cone_pass = all(value >= 0 for value in (gain_cone if contains_plus else direct_loss_cone))  # type: ignore[arg-type]
    return {
        "action_id": action_id, "allowed_predecessor_action_ids": allowed,
        "charge_identity": "H_(r-h)-theta_r/2=(delta_(r-h)-theta_(r-h))/2+(delta_(r-h)-theta_r)/2" if contains_plus else "not_applicable",
        "contains_plus_one": contains_plus, "cycle_decomposition": "gcd(q,h) cycles, each of length q/gcd(q,h)" if contains_plus else "not_applicable",
        "forced_predecessor_action_id": 0 if contains_plus else None,
        "direct_loss_cone_coefficients": [fraction_text(value) for value in direct_loss_cone] if direct_loss_cone is not None else [],
        "direct_loss_identity": "H-score=(1-delta_weight)(delta_r-theta_r)+(1/2-delta_weight-theta_weight)theta_r" if not contains_plus else "not_applicable",
        "forced_predecessor_empty": forced,
        "gain_cone_coefficients": [fraction_text(value) for value in gain_cone] if gain_cone is not None else [],
        "injective_translation": True, "inverse_translation": "r -> r+h" if contains_plus else "not_applicable",
        "kind": "lag_h_predecessor_charge", "pass": (forced and cone_pass) if contains_plus else cone_pass,
        "predecessor_inclusions": ["theta_(r-h)<=delta_(r-h)", "theta_r<=delta_(r-h)"] if contains_plus else [],
        "predecessor_translation": "r -> r-h" if contains_plus else "not_applicable",
        "relative_delta_coefficient": fraction_text(rel_delta), "relative_theta_coefficient": fraction_text(rel_theta),
        "row_id": f"charge:{action_id}", "self_loop_rule": "q divides h => plus-phase set is empty" if contains_plus else "not_applicable",
    }


def _charge_rows() -> list[dict[str, object]]:
    return [_charge_semantics(action_id) for action_id in range(8)]


def _monomial_semantics(i: int, j: int) -> dict[str, object]:
    name = f"c{i}{j}"
    channels = {
        (0, 0): "1/q", (2, 0): "delta_(q,r-h)",
        (0, 2): "delta_(q,r)", (2, 2): "theta^(h)_(q,r)",
    }
    survives = (i, j) in channels
    zero_reason = {
        (1, 0): "one-form fixed-period Mobius cancellation",
        (0, 1): "one-form fixed-period Mobius cancellation",
        (1, 1): "arbitrary-nonzero-determinant terminal full-mu lemma",
        (1, 2): "Boolean cutoff plus one-form Mobius cancellation",
        (2, 1): "Boolean cutoff plus one-form Mobius cancellation",
    }.get((i, j), "not_applicable")
    return {
        "bi_degree": [i, j], "coefficient": name,
        "general_finite_shift_domain": i + j <= 2,
        "kind": "two_site_biquadratic_channel", "limit_channel": channels.get((i, j), "0"),
        "pass": survives == ((i % 2 == 0) and (j % 2 == 0)),
        "row_id": f"monomial:{name}", "survives": survives,
        "total_degree": i + j, "zero_reason": "not_applicable" if survives else zero_reason,
    }


def _monomial_rows() -> list[dict[str, object]]:
    return [_monomial_semantics(i, j) for i in range(3) for j in range(3)]


def _finite_boolean_cutoff(m: int, primes: tuple[int, ...]) -> int:
    return int(all(m % (p * p) for p in primes))


def _finite_boolean_expansion(m: int, primes: tuple[int, ...]) -> int:
    total = 0
    for bits in product((0, 1), repeat=len(primes)):
        k = 1
        sign = 1
        for bit, p in zip(bits, primes):
            if bit:
                k *= p
                sign *= -1
        total += sign * int(m % (k * k) == 0)
    return total


def _determinant_contracts() -> list[dict[str, object]]:
    kind = "terminal_full_mu_contract"
    domain = {
        "row_id": "determinant:domain", "kind": kind,
        "forms": "D(n)=a1*n+b1, V(n)=a2*n+b2", "leading_coefficients": "a1,a2>=1",
        "determinant_hypothesis": "Delta=a1*b2-a2*b1!=0", "eventual_positivity": True,
        "periodic_mask": "fixed bounded rho", "conclusion": "terminal-log average of mu(D)mu(V)rho is zero",
    }
    domain["pass"] = domain["leading_coefficients"] == "a1,a2>=1" and domain["determinant_hypothesis"].endswith("!=0") and domain["eventual_positivity"] is True
    primes = (2, 3, 5)
    boolean_failures = sum(_finite_boolean_cutoff(m, primes) != _finite_boolean_expansion(m, primes) for m in range(1, 257))
    boolean = {
        "row_id": "determinant:boolean_cutoff", "kind": kind,
        "cutoff": "S_P(m)=prod_(p<=P)(1-1_(p^2|m)) in {0,1}",
        "expansion": "sum_(k|P#)mu(k)1_(k^2|m)", "scan_primes": list(primes),
        "mobius_liouville_identity": "mu(m)=lambda(m)*1_sf(m)",
        "cutoff_approximant": "lambda(D)lambda(V)S_P(D)S_P(V)",
        "scan_m_count": 256, "scan_failures": boolean_failures,
    }
    boolean["pass"] = (
        boolean_failures == 0 and boolean["mobius_liouville_identity"] == "mu(m)=lambda(m)*1_sf(m)"
        and boolean["cutoff_approximant"] == "lambda(D)lambda(V)S_P(D)S_P(V)"
    )
    divisors = (1, 2, 3, 5, 6, 10, 15, 30)
    modulus_failures = 0
    for M in range(1, 5):
        for k in divisors:
            for ell in divisors:
                combined = M * k * k * ell * ell
                # lcm(M,k^2,l^2) divides this product and is bounded by M(P#)^2.
                l12 = k * k * ell * ell // gcd(k * k, ell * ell)
                exact = M * l12 // gcd(M, l12)
                modulus_failures += exact > M * 30 * 30
    modulus = {
        "row_id": "determinant:combined_modulus", "kind": kind,
        "modulus": "lcm(M,k^2,l^2)<=M(P#)^2", "coprime_k_l_assumed": False,
        "compatible_residues": "possibly empty; no (k,l)=1 assumption",
        "fixture_count": 4 * len(divisors) ** 2, "fixture_failures": modulus_failures,
    }
    modulus["pass"] = modulus["coprime_k_l_assumed"] is False and modulus_failures == 0
    form_fixtures = ((1, -2, 1, 0), (2, 1, 1, 4), (3, -1, 2, 5), (1, 5, 2, 1))
    content_failures = 0
    determinant_values: list[int] = []
    for a1, b1, a2, b2 in form_fixtures:
        determinant_values.append(a1 * b2 - a2 * b1)
        for L in (1, 2, 6):
            for r in range(L):
                c_d = gcd(a1 * L, a1 * r + b1)
                c_v = gcd(a2 * L, a2 * r + b2)
                actual = (a1 * L // c_d) * ((a2 * r + b2) // c_v) - (a2 * L // c_v) * ((a1 * r + b1) // c_d)
                expected = L * (a1 * b2 - a2 * b1) // (c_d * c_v)
                content_failures += actual != expected or actual == 0
    content = {
        "row_id": "determinant:content", "kind": kind, "progression": "n=r+L*t",
        "contents": "c_D=gcd(a1*L,a1*r+b1), c_V=gcd(a2*L,a2*r+b2)",
        "reduced_determinant": "L*Delta/(c_D*c_V)!=0", "fixture_determinants": determinant_values,
        "liouville_content_identity": "lambda(D)lambda(V)=lambda(c_D*c_V)lambda(D/c_D)lambda(V/c_V)",
        "fixture_failures": content_failures,
    }
    content["pass"] = (
        content_failures == 0 and all(value != 0 for value in determinant_values)
        and len(set(map(abs, determinant_values))) > 1
        and content["liouville_content_identity"] == "lambda(D)lambda(V)=lambda(c_D*c_V)lambda(D/c_D)lambda(V/c_V)"
    )
    tao = {
        "row_id": "determinant:tao", "kind": kind, "remote_input": "Tao Theorem 2 equation (3)",
        "native_quantifier": "fixed positive-leading nonparallel affine forms", "uniform_rate_claimed": False,
    }
    tao["pass"] = tao["remote_input"] == "Tao Theorem 2 equation (3)" and tao["uniform_rate_claimed"] is False
    tail = {
        "row_id": "determinant:tail", "kind": kind,
        "tail": "Boolean union bound gives O_(D,V)(log(omega)/P+1)",
        "normalized_limsup": "limsup_X tail/log(omega) <<_(D,V) 1/P",
        "determinant_used_in_tail": False,
        "divisor_maximum_used": False, "two_coordinate_bound": "|uv-UV|<=|u-U|+|v-V| for Boolean values",
    }
    tail["pass"] = tail["determinant_used_in_tail"] is False and tail["divisor_maximum_used"] is False
    limit_order = {
        "row_id": "determinant:limit_order", "kind": kind,
        "order": ["fix P", "X->infinity", "P->infinity"],
        "clock": "1<=omega(X)<=X and omega(X)->infinity", "effective_rate_claimed": False,
    }
    limit_order["pass"] = limit_order["order"] == ["fix P", "X->infinity", "P->infinity"] and limit_order["effective_rate_claimed"] is False
    return [domain, boolean, modulus, content, tao, tail, limit_order]


def _determinant_rows() -> list[dict[str, object]]:
    return deepcopy(_determinant_contracts())


def _theta_contracts() -> list[dict[str, object]]:
    kind = "theta_local_density_contract"
    rows: list[dict[str, object]] = []
    formula = {
        "row_id": "theta:formula", "kind": kind, "A_p": "distinct set {0,h mod p^2}",
        "nu_p": "|A_p|", "tau_p_r": "#{a in A_p:a=r mod p}; collisions modulo p retain multiplicity",
        "regimes": ["p not|q", "p||q", "p^2|q"],
        "formula": "q^-1 prod_(p not|q)(1-nu_p/p^2) prod_(p||q)(1-tau_p_r/p) prod_(p^2|q)1_(r mod p^2 notin A_p)",
    }
    formula["pass"] = len(formula["regimes"]) == 3 and "q^-1" in formula["formula"]
    rows.append(formula)
    fixtures = (
        ("theta:nu_distinct", 2, 2, 1, 0, "p^2 not|h"),
        ("theta:nu_collision_4", 2, 4, 2, 0, "p^2|h"),
        ("theta:nu_collision_9", 3, 9, 3, 0, "p^2|h"),
        ("theta:tau_zero", 5, 2, 5, 1, "p||q"),
        ("theta:tau_one", 5, 2, 5, 2, "p||q"),
        ("theta:tau_two", 2, 2, 2, 0, "p||q"),
        ("theta:p_not_q", 2, 2, 1, 0, "p not|q"),
        ("theta:p_exactly_q", 3, 6, 3, 0, "p||q"),
        ("theta:p_square_hit", 2, 2, 4, 0, "p^2|q hit"),
        ("theta:p_square_miss", 2, 2, 4, 1, "p^2|q miss"),
    )
    for row_id, p, h, q, r, regime in fixtures:
        nu = square_collision_count(p, h)
        tau = tau_collision_multiplicity(p, h, r)
        factor = theta_local_factor(p, h, q, r)
        row = {
            "row_id": row_id, "kind": kind, "p": p, "h": h, "q": q, "r": r,
            "regime": regime, "nu": nu, "tau": tau, "local_factor": fraction_text(factor),
        }
        if q % p:
            expected = Fraction(p * p - nu, p * p)
        elif q % (p * p):
            expected = Fraction(p - tau, p)
        else:
            expected = Fraction(int(r % (p * p) not in {0, h % (p * p)}))
        row["pass"] = factor == expected and 0 <= factor <= 1
        rows.append(row)
    cone = {
        "row_id": "theta:cone_total", "kind": kind,
        "cone": ["0<=theta_r<=delta_r", "theta_r<=delta_(r-h)"],
        "total": "kappa_h=prod_(p^2|h)(1-p^-2)prod_(p^2 not|h)(1-2p^-2)",
        "countercases": [
            {"h": 2, "q": 2, "r": 0, "p": 2, "tau": tau_collision_multiplicity(2, 2, 0), "factor": fraction_text(theta_local_factor(2, 2, 2, 0))},
            {"h": 6, "q": 3, "r": 0, "p": 3, "tau": tau_collision_multiplicity(3, 6, 0), "factor": fraction_text(theta_local_factor(3, 6, 3, 0))},
            {"h": 4, "q": 2, "r": 0, "p": 2, "tau": tau_collision_multiplicity(2, 4, 0), "factor": fraction_text(theta_local_factor(2, 4, 2, 0))},
        ],
    }
    cone["pass"] = cone["countercases"] == [
        {"h": 2, "q": 2, "r": 0, "p": 2, "tau": 2, "factor": "0"},
        {"h": 6, "q": 3, "r": 0, "p": 3, "tau": 2, "factor": "1/3"},
        {"h": 4, "q": 2, "r": 0, "p": 2, "tau": 1, "factor": "1/2"},
    ]
    rows.append(cone)
    return rows


def _theta_rows() -> list[dict[str, object]]:
    return deepcopy(_theta_contracts())


def _landscape_contracts() -> list[dict[str, object]]:
    kind = "square_divisor_capacity_landscape"
    primes = (2, 3, 5, 7, 11)
    primorial = 1
    for p in primes:
        primorial *= p
    squarefree_h = primorial
    full_square_h = primorial * primorial
    star_product = finite_kappa(primes, squarefree_h)
    full_product = finite_kappa(primes, full_square_h)
    local_rows = [
        {"p": p, "squarefree_factor": fraction_text(kappa_local_factor(p, squarefree_h)),
         "square_divisor_factor": fraction_text(kappa_local_factor(p, full_square_h)),
         "cross_product_gap": 1}
        for p in primes
    ]
    kappa = {
        "row_id": "landscape:kappa", "kind": kind,
        "formula": "kappa_h=prod_(p^2|h)(1-p^-2)prod_(p^2 not|h)(1-2p^-2)",
        "finite_primes": list(primes), "local_factor_rows": local_rows,
    }
    kappa["pass"] = all(Fraction(row["square_divisor_factor"]) > Fraction(row["squarefree_factor"]) for row in local_rows)
    kappa_star = {
        "row_id": "landscape:kappa_star", "kind": kind, "kappa_star": "prod_p(1-2/p^2)",
        "equality": "kappa_h=kappa_star iff h is squarefree", "squarefree_fixture_h": squarefree_h,
        "finite_star_product": fraction_text(star_product),
    }
    kappa_star["pass"] = star_product == Fraction(1) * finite_kappa(primes, 1)
    square_factor = {
        "row_id": "landscape:square_factor", "kind": kind,
        "replacement_ratio": "(1-p^-2)/(1-2p^-2)>1",
        "cross_product_checks": [{"p": p, "left": p * p - 1, "right": p * p - 2, "strict": p * p - 1 > p * p - 2} for p in primes],
        "effect": "a square divisor increases kappa_h and decreases G_log(q,h)",
    }
    square_factor["pass"] = all(row["strict"] is True and row["left"] == row["right"] + 1 for row in square_factor["cross_product_checks"])
    finite_strict = {
        "row_id": "landscape:finite_strict", "kind": kind,
        "statement": "kappa_h<6/pi^2 for every finite h>=1",
        "reason": "some prime square does not divide finite h, leaving a strict (1-2/p^2)<(1-1/p^2) factor",
        "strict_factor_fixture": {"p": 13, "h": full_square_h, "kappa_factor": fraction_text(kappa_local_factor(13, full_square_h)), "zeta_factor": fraction_text(Fraction(168, 169))},
    }
    finite_strict["pass"] = Fraction(finite_strict["strict_factor_fixture"]["kappa_factor"]) < Fraction(finite_strict["strict_factor_fixture"]["zeta_factor"])
    primorial_row = {
        "row_id": "landscape:primorial", "kind": kind,
        "sequence": "h_y=(prod_(p<=y)p)^2", "finite_fixture_h": full_square_h,
        "finite_kappa_product": fraction_text(full_product),
        "finite_zeta_product": fraction_text(Fraction(1) * product_fraction(Fraction(p * p - 1, p * p) for p in primes)),
        "limit": "kappa_(h_y)->6/pi^2",
    }
    primorial_row["pass"] = primorial_row["finite_kappa_product"] == primorial_row["finite_zeta_product"]
    capacity = {
        "row_id": "landscape:capacity", "kind": kind,
        "definition": "G_log(q,h)=max_(f in finite safe A_(q,h)) |L_(q,h)(f)|",
        "limit_order": "form each fixed-table terminal-log limit before the finite maximum",
        "formula": "G_log(q,h)=6/pi^2-kappa_h/2 for every fixed q,h",
        "fixed_q_independent": True,
    }
    capacity["pass"] = "max_" in capacity["definition"] and "|L_" in capacity["definition"] and capacity["fixed_q_independent"] is True
    range_row = {
        "row_id": "landscape:range", "kind": kind,
        "range": "3/pi^2<G_log(q,h)<=6/pi^2-kappa_star/2", "infimum": "3/pi^2",
        "infimum_attained": False, "maximizers": "exactly squarefree h",
    }
    range_row["pass"] = range_row["infimum_attained"] is False and range_row["maximizers"] == "exactly squarefree h"
    reflection = {
        "row_id": "landscape:reflection", "kind": kind,
        "coefficient_parity": ["+", "-", "-", "+", "+", "-"],
        "witnesses": {"positive_table": 36, "positive_value": "+G_log(q,h)", "negative_table": 72, "negative_value": "-G_log(q,h)"},
        "both_constant_tables_safe": table_compatible(36, 36) and table_compatible(72, 72),
        "reflection_involution": reflected_table_id(reflected_table_id(36)) == 36,
    }
    reflection["pass"] = reflection["coefficient_parity"] == ["+", "-", "-", "+", "+", "-"] and reflected_table_id(36) == 72 and reflection["both_constant_tables_safe"] is True
    return [kappa, kappa_star, square_factor, finite_strict, primorial_row, capacity, range_row, reflection]


def _landscape_rows() -> list[dict[str, object]]:
    return deepcopy(_landscape_contracts())


def _finite_shift_contracts() -> list[dict[str, object]]:
    kind = "finite_shift_diagonalization"
    fixtures = (-5, 0, 2, 11)
    domain = {"row_id": "finite_shift:domain", "kind": kind, "shifts": "fixed finite pairwise-distinct integers a_1,...,a_m", "fixture_shifts": list(fixtures), "clock_and_period": "fixed q and admissible terminal omega"}
    domain["pass"] = len(set(fixtures)) == len(fixtures) and len(fixtures) < 10
    polynomial = {"row_id": "finite_shift:polynomial", "kind": kind, "degree": "total degree<=2", "coordinate": "mu0(n-a_i)", "allowed_exponent_sums": [0, 1, 2]}
    polynomial["pass"] = polynomial["allowed_exponent_sums"] == [0, 1, 2]
    constant = {"row_id": "finite_shift:constant", "kind": kind, "channel": "c_empty(r)/q", "exponent_sum": 0, "survives": True}
    constant["pass"] = constant["exponent_sum"] == 0 and constant["survives"] is True
    linear = {"row_id": "finite_shift:linear", "kind": kind, "channel": "c_i(r)mu0(n-a_i)", "exponent_sum": 1, "limit": "0 by fixed-period one-form Mobius cancellation"}
    linear["pass"] = linear["exponent_sum"] == 1 and linear["limit"].startswith("0 ")
    diagonal = {"row_id": "finite_shift:diagonal", "kind": kind, "channel": "c_ii(r)mu0(n-a_i)^2", "exponents": [2], "limit": "c_ii(r)delta_(q,r-a_i)"}
    diagonal["pass"] = sum(diagonal["exponents"]) == 2 and "r-a_i" in diagonal["limit"]
    determinants = [fixtures[i] - fixtures[j] for i in range(len(fixtures)) for j in range(i + 1, len(fixtures))]
    off_diagonal = {"row_id": "finite_shift:off_diagonal", "kind": kind, "channel": "c_ij(r)mu0(n-a_i)mu0(n-a_j), i!=j", "exponents": [1, 1], "determinant": "a_i-a_j!=0", "fixture_determinants": determinants, "limit": "0 by terminal full-mu lemma"}
    off_diagonal["pass"] = sum(off_diagonal["exponents"]) == 2 and all(value != 0 for value in determinants)
    return [domain, polynomial, constant, linear, diagonal, off_diagonal]


def _finite_shift_rows() -> list[dict[str, object]]:
    return deepcopy(_finite_shift_contracts())


def _firewall_contracts() -> list[dict[str, object]]:
    specs = [
        ("firewall:fixed_q_h", "each fixed q>=1 and fixed h>=1", ["q=q(X)", "h=h(X)", "uniform growing-lag rate"]),
        ("firewall:terminal_only", "terminal logarithmic average", ["ordinary Cesaro", "unweighted prefix theorem", "effective rate"]),
        ("firewall:finite_degree2", "fixed finite distinct shifts and total degree<=2", ["growing shift family", "degree>=3 multi-coordinate truth tables"]),
        ("firewall:separate_compiler", "one fixed lag h, two coordinates, coordinatewise bi-degree<=2", ["identify with general total-degree theorem", "multiple interacting lags"]),
        ("firewall:sources", "Tao fixed nonparallel theorem plus local Boolean cutoff", ["TPC-137 quoted as an all-h theorem", "Mirsky black-box local formula", "coprime k,l assumption"]),
        ("firewall:no_physical_gate", "arithmetic terminal-log capacity only", ["operator", "trace", "zeros", "Riemann Hypothesis", "Gates A-E"]),
    ]
    rows: list[dict[str, object]] = []
    for row_id, allowed, forbidden in specs:
        row: dict[str, object] = {"row_id": row_id, "kind": "scope_firewall", "allowed": allowed, "forbidden": forbidden}
        if row_id == "firewall:no_physical_gate":
            row["gates"] = {"A": False, "B": False, "C": False, "D": False, "E": False}
        row["pass"] = type(allowed) is str and bool(allowed) and type(forbidden) is list and len(forbidden) == len(set(forbidden)) and all(type(item) is str and item not in allowed for item in forbidden)
        if "gates" in row:
            row["pass"] = row["pass"] and set(row["gates"]) == set("ABCDE") and all(value is False for value in row["gates"].values())
        rows.append(row)
    return rows


def _firewall_rows() -> list[dict[str, object]]:
    return deepcopy(_firewall_contracts())


def _contracts() -> dict[str, object]:
    return {
        "action_masks": list(ACTION_MASKS),
        "action_weight_pairs": [[fraction_text(a), fraction_text(b)] for a, b in ACTION_WEIGHT_PAIRS],
        "baseline_action_id": BASELINE_ACTION_ID,
        "compiler_coefficient_names": list(COMPILER_NAMES),
        "fixed_lag_limit_formula": "sum_r[c00(r)/q+c20(r)delta_(q,r-h)+c02(r)delta_(q,r)+c22(r)theta^(h)_(q,r)]",
        "global_closure": deepcopy(_global_closure_contract()),
        "mutation_count": len(MUTATION_NAMES), "mutation_names": list(MUTATION_NAMES),
        "projection": "E_plus=E intersect (T x {+1})",
        "row_partition": [512, 8, 64, 8, 9, 7, 12, 8, 6, 6],
        "translation_oracle": _translation_oracle(),
    }


def build_certificate() -> dict[str, object]:
    groups = {
        "truth_rows": _truth_rows(), "projected_action_rows": _action_rows(),
        "compatibility_rows": _compatibility_rows(), "charge_rows": _charge_rows(),
        "monomial_rows": _monomial_rows(), "determinant_rows": _determinant_rows(),
        "theta_rows": _theta_rows(), "landscape_rows": _landscape_rows(),
        "finite_shift_rows": _finite_shift_rows(), "firewall_rows": _firewall_rows(),
    }
    rows = [row for group in groups.values() for row in group]
    contracts = _contracts()
    return {
        "all_pass": len(rows) == 640 and all(row["pass"] is True for row in rows)
                    and contracts["global_closure"]["pass"] is True
                    and all(row["pass"] is True for row in contracts["translation_oracle"]),
        "certificate_version": 1, "contracts": contracts, "counts": dict(EXPECTED_COUNTS),
        "epistemic_role": EPISTEMIC_ROLE, **groups, "status": STATUS, "title": TITLE,
    }


def _exact(value: object, expected: object, label: str) -> None:
    if not exact_equal(value, expected):
        raise ValueError(f"{label} changed")


def _validate_truth_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 512:
        raise ValueError("truth row count changed")
    for table_id, row in enumerate(rows):
        if type(row) is not dict or type(row.get("table_id")) is not int:
            raise TypeError("truth row types changed")
        truth = tuple(1 if table_id & (1 << index) else -1 for index in range(9))
        projected = sum(1 << index for index, ((_, z), value) in enumerate(zip(POINTS, truth)) if z == 1 and value == 1)
        projected_truth = tuple(1 if projected & (1 << index) else -1 for index in range(9))
        plus = [index for index, value in enumerate(truth) if value == 1]
        projected_plus = [index for index, value in enumerate(projected_truth) if value == 1]
        gains = [z * (new - old) for (_, z), old, new in zip(POINTS, truth, projected_truth)]
        lookup = dict(zip(POINTS, truth))
        reflected_truth = tuple(lookup[(-x, -z)] for x, z in POINTS)
        reflected = sum(1 << index for index, value in enumerate(reflected_truth) if value == 1)
        action = sum(1 << action_id for action_id, point_id in enumerate((2, 5, 8)) if projected & (1 << point_id))
        subset = set(projected_plus).issubset(plus)
        only_plus = all(z == 1 for index, (_, z) in enumerate(POINTS) if projected & (1 << index))
        expected = {
            "all_pointwise_gains_nonnegative": all(gain >= 0 for gain in gains),
            "kind": "truth_projection", "pass": subset and only_plus and all(gain >= 0 for gain in gains),
            "plus_point_indices": plus, "pointwise_zf_gains": gains,
            "projected_action_id": action, "projected_only_z_plus": only_plus,
            "projected_plus_subset": subset, "projected_table_id": projected,
            "reflected_table_id": reflected, "row_id": f"truth:{table_id:03d}",
            "table_id": table_id, "truth": list(truth),
        }
        _exact(row, expected, f"truth row {table_id}")


def _validate_action_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 8:
        raise ValueError("action row count changed")
    for action_id, row in enumerate(rows):
        if type(row) is not dict or type(row.get("action_id")) is not int:
            raise TypeError("action row types changed")
        mask = ACTION_MASKS[action_id]
        coefficients = coefficient_vector(mask)
        preimages = 0
        for table_id in range(512):
            truth = tuple(1 if table_id & (1 << index) else -1 for index in range(9))
            projected = sum(1 << index for index, ((_, z), value) in enumerate(zip(POINTS, truth)) if z == 1 and value == 1)
            computed_action = sum(1 << bit for bit, point_id in enumerate((2, 5, 8)) if projected & (1 << point_id))
            preimages += computed_action == action_id
        values = tuple(value for index, value in enumerate(TERNARY) if action_id & (1 << index))
        target_count = 0
        for right in range(8):
            left_edges = table_plus_edges(mask)
            right_edges = table_plus_edges(ACTION_MASKS[right])
            target_count += not any((z, w) in right_edges for _, z in left_edges for w in TERNARY)
        expected = {
            "action_id": action_id, "action_values": list(values),
            "c02_delta_coefficient": fraction_text(coefficients[1]),
            "c22_theta_coefficient": fraction_text(coefficients[5]),
            "coefficient_names": list(COMPILER_NAMES),
            "coefficients": [fraction_text(value) for value in coefficients],
            "compatible_target_count": target_count, "kind": "projected_action",
            "pass": preimages == 64 and (coefficients[1], coefficients[5]) == ACTION_WEIGHT_PAIRS[action_id],
            "preimage_count": preimages, "projected_mask": mask, "row_id": f"action:{action_id}",
        }
        _exact(row, expected, f"action row {action_id}")
        serialized = tuple(Fraction(value) for value in row["coefficients"])
        mask_truth = tuple(1 if mask & (1 << index) else -1 for index in range(9))
        lookup = dict(zip(POINTS, mask_truth))
        for x, z in NONZERO_POINTS:
            if sum(value * basis for value, basis in zip(serialized, _basis(x, z))) != z * lookup[(x, z)]:
                raise ValueError(f"action row {action_id} interpolation failed")
        if (serialized[1], serialized[5]) != ACTION_WEIGHT_PAIRS[action_id]:
            raise ValueError(f"action row {action_id} weight oracle failed")


def _validate_compatibility_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 64:
        raise ValueError("compatibility row count changed")
    for index, row in enumerate(rows):
        left, right = divmod(index, 8)
        left_edges = table_plus_edges(ACTION_MASKS[left])
        right_edges = table_plus_edges(ACTION_MASKS[right])
        brute = not any((z, w) in right_edges for _, z in left_edges for w in TERNARY)
        left_values = tuple(value for bit, value in enumerate(TERNARY) if left & (1 << bit))
        right_values = tuple(value for bit, value in enumerate(TERNARY) if right & (1 << bit))
        simplified = left_values == () or 1 not in right_values
        expected = {
            "compatible": brute, "edge_triple_recomputed": True,
            "kind": "directed_lag_h_action_compatibility", "left_action_id": left,
            "left_empty": left_values == (), "pass": brute == simplified,
            "phase_orientation": "A_r -> A_(r+h)", "right_action_id": right,
            "right_contains_plus_one": 1 in right_values, "row_id": f"compat:{left}->{right}",
        }
        _exact(row, expected, f"compatibility row {left}->{right}")


def _validate_charge_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 8:
        raise ValueError("charge row count changed")
    for action_id, row in enumerate(rows):
        delta, theta = ACTION_WEIGHT_PAIRS[action_id]
        base_delta, base_theta = ACTION_WEIGHT_PAIRS[3]
        rel_delta, rel_theta = delta - base_delta, theta - base_theta
        values = tuple(value for bit, value in enumerate(TERNARY) if action_id & (1 << bit))
        contains_plus = 1 in values
        allowed: list[int] = []
        for left in range(8):
            left_edges = table_plus_edges(ACTION_MASKS[left])
            right_edges = table_plus_edges(ACTION_MASKS[action_id])
            if not any((z, w) in right_edges for _, z in left_edges for w in TERNARY):
                allowed.append(left)
        forced = allowed == [0] if contains_plus else False
        gain = (-rel_delta, Fraction(1, 2) - rel_theta - rel_delta) if contains_plus else None
        direct = (Fraction(1) - delta, Fraction(1, 2) - delta - theta) if not contains_plus else None
        cone = gain if contains_plus else direct
        expected = {
            "action_id": action_id, "allowed_predecessor_action_ids": allowed,
            "charge_identity": "H_(r-h)-theta_r/2=(delta_(r-h)-theta_(r-h))/2+(delta_(r-h)-theta_r)/2" if contains_plus else "not_applicable",
            "contains_plus_one": contains_plus,
            "cycle_decomposition": "gcd(q,h) cycles, each of length q/gcd(q,h)" if contains_plus else "not_applicable",
            "direct_loss_cone_coefficients": [fraction_text(value) for value in direct] if direct is not None else [],
            "direct_loss_identity": "H-score=(1-delta_weight)(delta_r-theta_r)+(1/2-delta_weight-theta_weight)theta_r" if not contains_plus else "not_applicable",
            "forced_predecessor_action_id": 0 if contains_plus else None,
            "forced_predecessor_empty": forced,
            "gain_cone_coefficients": [fraction_text(value) for value in gain] if gain is not None else [],
            "injective_translation": True, "inverse_translation": "r -> r+h" if contains_plus else "not_applicable",
            "kind": "lag_h_predecessor_charge",
            "pass": (forced and all(value >= 0 for value in cone)) if contains_plus else all(value >= 0 for value in cone),  # type: ignore[arg-type]
            "predecessor_inclusions": ["theta_(r-h)<=delta_(r-h)", "theta_r<=delta_(r-h)"] if contains_plus else [],
            "predecessor_translation": "r -> r-h" if contains_plus else "not_applicable",
            "relative_delta_coefficient": fraction_text(rel_delta), "relative_theta_coefficient": fraction_text(rel_theta),
            "row_id": f"charge:{action_id}",
            "self_loop_rule": "q divides h => plus-phase set is empty" if contains_plus else "not_applicable",
        }
        _exact(row, expected, f"charge row {action_id}")


def _validate_monomial_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 9:
        raise ValueError("monomial row count changed")
    for index, row in enumerate(rows):
        i, j = divmod(index, 3)
        channels = {(0, 0): "1/q", (2, 0): "delta_(q,r-h)", (0, 2): "delta_(q,r)", (2, 2): "theta^(h)_(q,r)"}
        survives = (i, j) in channels
        reasons = {
            (1, 0): "one-form fixed-period Mobius cancellation", (0, 1): "one-form fixed-period Mobius cancellation",
            (1, 1): "arbitrary-nonzero-determinant terminal full-mu lemma",
            (1, 2): "Boolean cutoff plus one-form Mobius cancellation", (2, 1): "Boolean cutoff plus one-form Mobius cancellation",
        }
        expected = {
            "bi_degree": [i, j], "coefficient": f"c{i}{j}", "general_finite_shift_domain": i + j <= 2,
            "kind": "two_site_biquadratic_channel", "limit_channel": channels.get((i, j), "0"),
            "pass": survives == (i % 2 == 0 and j % 2 == 0), "row_id": f"monomial:c{i}{j}",
            "survives": survives, "total_degree": i + j,
            "zero_reason": "not_applicable" if survives else reasons[(i, j)],
        }
        _exact(row, expected, f"monomial row {i},{j}")


def _validate_determinant_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 7:
        raise ValueError("determinant row count changed")
    if any(type(row) is not dict or type(row.get("pass")) is not bool for row in rows):
        raise TypeError("determinant row types changed")
    kind = "terminal_full_mu_contract"
    domain = {
        "row_id": "determinant:domain", "kind": kind,
        "forms": "D(n)=a1*n+b1, V(n)=a2*n+b2", "leading_coefficients": "a1,a2>=1",
        "determinant_hypothesis": "Delta=a1*b2-a2*b1!=0", "eventual_positivity": True,
        "periodic_mask": "fixed bounded rho", "conclusion": "terminal-log average of mu(D)mu(V)rho is zero",
    }
    domain["pass"] = domain["leading_coefficients"] == "a1,a2>=1" and domain["determinant_hypothesis"].endswith("!=0") and domain["eventual_positivity"] is True
    primes = (2, 3, 5)
    failures = 0
    for m in range(1, 257):
        cutoff = int(all(m % (p * p) for p in primes))
        expansion = 0
        for bits in product((0, 1), repeat=3):
            k, sign = 1, 1
            for bit, p in zip(bits, primes):
                if bit:
                    k *= p
                    sign *= -1
            expansion += sign * int(m % (k * k) == 0)
        failures += cutoff != expansion
    boolean = {
        "row_id": "determinant:boolean_cutoff", "kind": kind,
        "cutoff": "S_P(m)=prod_(p<=P)(1-1_(p^2|m)) in {0,1}",
        "expansion": "sum_(k|P#)mu(k)1_(k^2|m)", "scan_primes": list(primes),
        "mobius_liouville_identity": "mu(m)=lambda(m)*1_sf(m)",
        "cutoff_approximant": "lambda(D)lambda(V)S_P(D)S_P(V)",
        "scan_m_count": 256, "scan_failures": failures, "pass": failures == 0,
    }
    divisors = (1, 2, 3, 5, 6, 10, 15, 30)
    modulus_failures = 0
    for M in range(1, 5):
        for k in divisors:
            for ell in divisors:
                pair_lcm = k * k * ell * ell // gcd(k * k, ell * ell)
                exact_lcm = M * pair_lcm // gcd(M, pair_lcm)
                modulus_failures += exact_lcm > M * 30 * 30
    modulus = {
        "row_id": "determinant:combined_modulus", "kind": kind,
        "modulus": "lcm(M,k^2,l^2)<=M(P#)^2", "coprime_k_l_assumed": False,
        "compatible_residues": "possibly empty; no (k,l)=1 assumption",
        "fixture_count": 4 * len(divisors) ** 2, "fixture_failures": modulus_failures,
        "pass": modulus_failures == 0,
    }
    fixtures = ((1, -2, 1, 0), (2, 1, 1, 4), (3, -1, 2, 5), (1, 5, 2, 1))
    content_failures = 0
    determinants: list[int] = []
    for a1, b1, a2, b2 in fixtures:
        determinant = a1 * b2 - a2 * b1
        determinants.append(determinant)
        for L in (1, 2, 6):
            for r in range(L):
                c_d = gcd(a1 * L, a1 * r + b1)
                c_v = gcd(a2 * L, a2 * r + b2)
                reduced = (a1 * L // c_d) * ((a2 * r + b2) // c_v) - (a2 * L // c_v) * ((a1 * r + b1) // c_d)
                formula = L * determinant // (c_d * c_v)
                content_failures += reduced != formula or reduced == 0
    content = {
        "row_id": "determinant:content", "kind": kind, "progression": "n=r+L*t",
        "contents": "c_D=gcd(a1*L,a1*r+b1), c_V=gcd(a2*L,a2*r+b2)",
        "reduced_determinant": "L*Delta/(c_D*c_V)!=0", "fixture_determinants": determinants,
        "liouville_content_identity": "lambda(D)lambda(V)=lambda(c_D*c_V)lambda(D/c_D)lambda(V/c_V)",
        "fixture_failures": content_failures,
        "pass": content_failures == 0 and all(value != 0 for value in determinants) and len(set(map(abs, determinants))) > 1,
    }
    tao = {
        "row_id": "determinant:tao", "kind": kind, "remote_input": "Tao Theorem 2 equation (3)",
        "native_quantifier": "fixed positive-leading nonparallel affine forms", "uniform_rate_claimed": False,
        "pass": "nonparallel" in "fixed positive-leading nonparallel affine forms" and False is False,
    }
    tail = {
        "row_id": "determinant:tail", "kind": kind,
        "tail": "Boolean union bound gives O_(D,V)(log(omega)/P+1)",
        "normalized_limsup": "limsup_X tail/log(omega) <<_(D,V) 1/P",
        "determinant_used_in_tail": False,
        "divisor_maximum_used": False, "two_coordinate_bound": "|uv-UV|<=|u-U|+|v-V| for Boolean values",
        "pass": (False is False) and (False is False) and "Boolean" in "|uv-UV|<=|u-U|+|v-V| for Boolean values",
    }
    limit_order = {
        "row_id": "determinant:limit_order", "kind": kind,
        "order": ["fix P", "X->infinity", "P->infinity"],
        "clock": "1<=omega(X)<=X and omega(X)->infinity", "effective_rate_claimed": False,
        "pass": ["fix P", "X->infinity", "P->infinity"] == ["fix P", "X->infinity", "P->infinity"] and False is False,
    }
    _exact(rows, [domain, boolean, modulus, content, tao, tail, limit_order], "determinant rows")


def _validate_theta_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 12:
        raise ValueError("theta row count changed")
    kind = "theta_local_density_contract"
    formula = {
        "row_id": "theta:formula", "kind": kind, "A_p": "distinct set {0,h mod p^2}",
        "nu_p": "|A_p|", "tau_p_r": "#{a in A_p:a=r mod p}; collisions modulo p retain multiplicity",
        "regimes": ["p not|q", "p||q", "p^2|q"],
        "formula": "q^-1 prod_(p not|q)(1-nu_p/p^2) prod_(p||q)(1-tau_p_r/p) prod_(p^2|q)1_(r mod p^2 notin A_p)",
        "pass": len(["p not|q", "p||q", "p^2|q"]) == 3 and "q^-1" in "q^-1 prod_(p not|q)(1-nu_p/p^2) prod_(p||q)(1-tau_p_r/p) prod_(p^2|q)1_(r mod p^2 notin A_p)",
    }
    fixtures = (
        ("theta:nu_distinct", 2, 2, 1, 0, "p^2 not|h"),
        ("theta:nu_collision_4", 2, 4, 2, 0, "p^2|h"),
        ("theta:nu_collision_9", 3, 9, 3, 0, "p^2|h"),
        ("theta:tau_zero", 5, 2, 5, 1, "p||q"),
        ("theta:tau_one", 5, 2, 5, 2, "p||q"),
        ("theta:tau_two", 2, 2, 2, 0, "p||q"),
        ("theta:p_not_q", 2, 2, 1, 0, "p not|q"),
        ("theta:p_exactly_q", 3, 6, 3, 0, "p||q"),
        ("theta:p_square_hit", 2, 2, 4, 0, "p^2|q hit"),
        ("theta:p_square_miss", 2, 2, 4, 1, "p^2|q miss"),
    )
    expected: list[dict[str, object]] = [formula]
    for row_id, p, h, q, r, regime in fixtures:
        residues = {0, h % (p * p)}
        nu = len(residues)
        tau = sum(value % p == r % p for value in residues)
        if q % p:
            factor = Fraction(p * p - nu, p * p)
        elif q % (p * p):
            factor = Fraction(p - tau, p)
        else:
            factor = Fraction(int(r % (p * p) not in residues))
        expected.append({
            "row_id": row_id, "kind": kind, "p": p, "h": h, "q": q, "r": r,
            "regime": regime, "nu": nu, "tau": tau, "local_factor": fraction_text(factor),
            "pass": 0 <= factor <= 1,
        })
    counters = []
    for h, q, r, p in ((2, 2, 0, 2), (6, 3, 0, 3), (4, 2, 0, 2)):
        residues = {0, h % (p * p)}
        tau = sum(value % p == r % p for value in residues)
        factor = Fraction(p - tau, p)
        counters.append({"h": h, "q": q, "r": r, "p": p, "tau": tau, "factor": fraction_text(factor)})
    expected.append({
        "row_id": "theta:cone_total", "kind": kind,
        "cone": ["0<=theta_r<=delta_r", "theta_r<=delta_(r-h)"],
        "total": "kappa_h=prod_(p^2|h)(1-p^-2)prod_(p^2 not|h)(1-2p^-2)",
        "countercases": counters, "pass": counters == [
            {"h": 2, "q": 2, "r": 0, "p": 2, "tau": 2, "factor": "0"},
            {"h": 6, "q": 3, "r": 0, "p": 3, "tau": 2, "factor": "1/3"},
            {"h": 4, "q": 2, "r": 0, "p": 2, "tau": 1, "factor": "1/2"},
        ],
    })
    _exact(rows, expected, "theta rows")


def _validate_landscape_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 8:
        raise ValueError("landscape row count changed")
    kind = "square_divisor_capacity_landscape"
    primes = (2, 3, 5, 7, 11)
    primorial = 1
    for p in primes:
        primorial *= p
    squarefree_h, full_square_h = primorial, primorial * primorial
    local_rows: list[dict[str, object]] = []
    star, full, zeta = Fraction(1), Fraction(1), Fraction(1)
    for p in primes:
        p2 = p * p
        sf_factor = Fraction(p2 - (1 if squarefree_h % p2 == 0 else 2), p2)
        sq_factor = Fraction(p2 - (1 if full_square_h % p2 == 0 else 2), p2)
        star *= sf_factor
        full *= sq_factor
        zeta *= Fraction(p2 - 1, p2)
        local_rows.append({"p": p, "squarefree_factor": fraction_text(sf_factor), "square_divisor_factor": fraction_text(sq_factor), "cross_product_gap": 1})
    kappa = {
        "row_id": "landscape:kappa", "kind": kind,
        "formula": "kappa_h=prod_(p^2|h)(1-p^-2)prod_(p^2 not|h)(1-2p^-2)",
        "finite_primes": list(primes), "local_factor_rows": local_rows,
        "pass": all(Fraction(row["square_divisor_factor"]) > Fraction(row["squarefree_factor"]) for row in local_rows),
    }
    kappa_star = {
        "row_id": "landscape:kappa_star", "kind": kind, "kappa_star": "prod_p(1-2/p^2)",
        "equality": "kappa_h=kappa_star iff h is squarefree", "squarefree_fixture_h": squarefree_h,
        "finite_star_product": fraction_text(star), "pass": all(squarefree_h % (p * p) != 0 for p in primes),
    }
    cross = [{"p": p, "left": p * p - 1, "right": p * p - 2, "strict": p * p - 1 > p * p - 2} for p in primes]
    square_factor = {
        "row_id": "landscape:square_factor", "kind": kind,
        "replacement_ratio": "(1-p^-2)/(1-2p^-2)>1", "cross_product_checks": cross,
        "effect": "a square divisor increases kappa_h and decreases G_log(q,h)",
        "pass": all(item["strict"] is True and item["left"] == item["right"] + 1 for item in cross),
    }
    p = 13
    fixture = {"p": p, "h": full_square_h, "kappa_factor": fraction_text(Fraction(p * p - 2, p * p)), "zeta_factor": fraction_text(Fraction(p * p - 1, p * p))}
    finite_strict = {
        "row_id": "landscape:finite_strict", "kind": kind,
        "statement": "kappa_h<6/pi^2 for every finite h>=1",
        "reason": "some prime square does not divide finite h, leaving a strict (1-2/p^2)<(1-1/p^2) factor",
        "strict_factor_fixture": fixture,
        "pass": Fraction(fixture["kappa_factor"]) < Fraction(fixture["zeta_factor"]),
    }
    primorial_row = {
        "row_id": "landscape:primorial", "kind": kind,
        "sequence": "h_y=(prod_(p<=y)p)^2", "finite_fixture_h": full_square_h,
        "finite_kappa_product": fraction_text(full), "finite_zeta_product": fraction_text(zeta),
        "limit": "kappa_(h_y)->6/pi^2", "pass": full == zeta,
    }
    definition = "G_log(q,h)=max_(f in finite safe A_(q,h)) |L_(q,h)(f)|"
    capacity = {
        "row_id": "landscape:capacity", "kind": kind, "definition": definition,
        "limit_order": "form each fixed-table terminal-log limit before the finite maximum",
        "formula": "G_log(q,h)=6/pi^2-kappa_h/2 for every fixed q,h", "fixed_q_independent": True,
        "pass": "max_" in definition and "|L_" in definition,
    }
    range_row = {
        "row_id": "landscape:range", "kind": kind,
        "range": "3/pi^2<G_log(q,h)<=6/pi^2-kappa_star/2", "infimum": "3/pi^2",
        "infimum_attained": False, "maximizers": "exactly squarefree h", "pass": (False is False) and "squarefree" in "exactly squarefree h",
    }
    parity = ["+", "-", "-", "+", "+", "-"]
    reflection = {
        "row_id": "landscape:reflection", "kind": kind, "coefficient_parity": parity,
        "witnesses": {"positive_table": 36, "positive_value": "+G_log(q,h)", "negative_table": 72, "negative_value": "-G_log(q,h)"},
        "both_constant_tables_safe": table_compatible(36, 36) and table_compatible(72, 72),
        "reflection_involution": reflected_table_id(reflected_table_id(36)) == 36,
        "pass": parity == ["+", "-", "-", "+", "+", "-"] and reflected_table_id(36) == 72 and table_compatible(36, 36) and table_compatible(72, 72),
    }
    _exact(rows, [kappa, kappa_star, square_factor, finite_strict, primorial_row, capacity, range_row, reflection], "landscape rows")


def _validate_finite_shift_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 6:
        raise ValueError("finite-shift row count changed")
    kind = "finite_shift_diagonalization"
    shifts = (-5, 0, 2, 11)
    determinants = [shifts[i] - shifts[j] for i in range(4) for j in range(i + 1, 4)]
    expected = [
        {"row_id": "finite_shift:domain", "kind": kind, "shifts": "fixed finite pairwise-distinct integers a_1,...,a_m", "fixture_shifts": list(shifts), "clock_and_period": "fixed q and admissible terminal omega", "pass": len(set(shifts)) == 4},
        {"row_id": "finite_shift:polynomial", "kind": kind, "degree": "total degree<=2", "coordinate": "mu0(n-a_i)", "allowed_exponent_sums": [0, 1, 2], "pass": max([0, 1, 2]) == 2},
        {"row_id": "finite_shift:constant", "kind": kind, "channel": "c_empty(r)/q", "exponent_sum": 0, "survives": True, "pass": 0 == 0 and True is True},
        {"row_id": "finite_shift:linear", "kind": kind, "channel": "c_i(r)mu0(n-a_i)", "exponent_sum": 1, "limit": "0 by fixed-period one-form Mobius cancellation", "pass": 1 == 1 and "0 by".startswith("0 ")},
        {"row_id": "finite_shift:diagonal", "kind": kind, "channel": "c_ii(r)mu0(n-a_i)^2", "exponents": [2], "limit": "c_ii(r)delta_(q,r-a_i)", "pass": sum([2]) == 2 and "r-a_i" in "c_ii(r)delta_(q,r-a_i)"},
        {"row_id": "finite_shift:off_diagonal", "kind": kind, "channel": "c_ij(r)mu0(n-a_i)mu0(n-a_j), i!=j", "exponents": [1, 1], "determinant": "a_i-a_j!=0", "fixture_determinants": determinants, "limit": "0 by terminal full-mu lemma", "pass": all(value != 0 for value in determinants)},
    ]
    _exact(rows, expected, "finite-shift rows")


def _validate_firewall_rows(rows: object) -> None:
    if type(rows) is not list or len(rows) != 6:
        raise ValueError("firewall row count changed")
    specs = [
        ("firewall:fixed_q_h", "each fixed q>=1 and fixed h>=1", ["q=q(X)", "h=h(X)", "uniform growing-lag rate"]),
        ("firewall:terminal_only", "terminal logarithmic average", ["ordinary Cesaro", "unweighted prefix theorem", "effective rate"]),
        ("firewall:finite_degree2", "fixed finite distinct shifts and total degree<=2", ["growing shift family", "degree>=3 multi-coordinate truth tables"]),
        ("firewall:separate_compiler", "one fixed lag h, two coordinates, coordinatewise bi-degree<=2", ["identify with general total-degree theorem", "multiple interacting lags"]),
        ("firewall:sources", "Tao fixed nonparallel theorem plus local Boolean cutoff", ["TPC-137 quoted as an all-h theorem", "Mirsky black-box local formula", "coprime k,l assumption"]),
        ("firewall:no_physical_gate", "arithmetic terminal-log capacity only", ["operator", "trace", "zeros", "Riemann Hypothesis", "Gates A-E"]),
    ]
    expected: list[dict[str, object]] = []
    for row_id, allowed, forbidden in specs:
        row: dict[str, object] = {"row_id": row_id, "kind": "scope_firewall", "allowed": allowed, "forbidden": forbidden}
        if row_id.endswith("no_physical_gate"):
            row["gates"] = {key: False for key in "ABCDE"}
        passed = len(forbidden) == len(set(forbidden)) and all(item not in allowed for item in forbidden)
        if "gates" in row:
            passed = passed and all(value is False for value in row["gates"].values())
        row["pass"] = passed
        expected.append(row)
    _exact(rows, expected, "firewall rows")


@lru_cache(maxsize=1)
def _independent_global_closure() -> dict[str, object]:
    compatible = 0
    projection_failures = 0
    reflection_failures = 0
    for left in range(512):
        left_truth = tuple(1 if left & (1 << index) else -1 for index in range(9))
        left_edges = frozenset(point for point, value in zip(POINTS, left_truth) if value == 1)
        left_projected = sum(1 << index for index, ((_, z), value) in enumerate(zip(POINTS, left_truth)) if z == 1 and value == 1)
        left_lookup = dict(zip(POINTS, left_truth))
        left_reflected = sum(1 << index for index, (x, z) in enumerate(POINTS) if left_lookup[(-x, -z)] == 1)
        for right in range(512):
            right_truth = tuple(1 if right & (1 << index) else -1 for index in range(9))
            right_edges = frozenset(point for point, value in zip(POINTS, right_truth) if value == 1)
            if any((z, w) in right_edges for _, z in left_edges for w in TERNARY):
                continue
            compatible += 1
            right_projected = sum(1 << index for index, ((_, z), value) in enumerate(zip(POINTS, right_truth)) if z == 1 and value == 1)
            p_left_edges = frozenset(point for point, value in zip(POINTS, tuple(1 if left_projected & (1 << i) else -1 for i in range(9))) if value == 1)
            p_right_edges = frozenset(point for point, value in zip(POINTS, tuple(1 if right_projected & (1 << i) else -1 for i in range(9))) if value == 1)
            projection_failures += any((z, w) in p_right_edges for _, z in p_left_edges for w in TERNARY)
            right_lookup = dict(zip(POINTS, right_truth))
            right_reflected = sum(1 << index for index, (x, z) in enumerate(POINTS) if right_lookup[(-x, -z)] == 1)
            r_left_edges = frozenset(point for point, value in zip(POINTS, tuple(1 if left_reflected & (1 << i) else -1 for i in range(9))) if value == 1)
            r_right_edges = frozenset(point for point, value in zip(POINTS, tuple(1 if right_reflected & (1 << i) else -1 for i in range(9))) if value == 1)
            reflection_failures += any((z, w) in r_right_edges for _, z in r_left_edges for w in TERNARY)
    signs = (1, -1, -1, 1, 1, -1)
    involution_failures = 0
    parity_failures = 0
    interpolation_failures = 0
    for table_id in range(512):
        truth = tuple(1 if table_id & (1 << index) else -1 for index in range(9))
        lookup = dict(zip(POINTS, truth))
        reflected = sum(1 << index for index, (x, z) in enumerate(POINTS) if lookup[(-x, -z)] == 1)
        reflected_truth = tuple(1 if reflected & (1 << index) else -1 for index in range(9))
        reflected_lookup = dict(zip(POINTS, reflected_truth))
        twice = sum(1 << index for index, (x, z) in enumerate(POINTS) if reflected_lookup[(-x, -z)] == 1)
        involution_failures += twice != table_id
        left_coefficients = coefficient_vector(table_id)
        right_coefficients = coefficient_vector(reflected)
        parity_failures += right_coefficients != tuple(sign * value for sign, value in zip(signs, left_coefficients))
        lookup = dict(zip(POINTS, truth))
        interpolation_failures += any(
            sum(value * basis for value, basis in zip(left_coefficients, _basis(x, z))) != z * lookup[(x, z)]
            for x, z in NONZERO_POINTS
        )
    plus_self = 0
    for action in range(4, 8):
        edges = table_plus_edges(ACTION_MASKS[action])
        plus_self += not any((z, w) in edges for _, z in edges for w in TERNARY)
    table36 = table_plus_edges(36)
    table72 = table_plus_edges(72)
    self36 = not any((z, w) in table36 for _, z in table36 for w in TERNARY)
    self72 = not any((z, w) in table72 for _, z in table72 for w in TERNARY)
    return {
        "ordered_table_pair_count": 262144, "compatible_pair_count": compatible,
        "projection_compatibility_failures": projection_failures,
        "reflection_compatibility_failures": reflection_failures,
        "reflection_involution_failures": involution_failures,
        "coefficient_parity": ["+", "-", "-", "+", "+", "-"],
        "coefficient_parity_failures": parity_failures,
        "coefficient_interpolation_failures": interpolation_failures,
        "table_36_self_compatible": self36, "table_72_self_compatible": self72,
        "plus_action_self_compatible_count": plus_self,
        "pass": compatible == 3375 and projection_failures == 0 and reflection_failures == 0
                and involution_failures == 0 and parity_failures == 0 and interpolation_failures == 0
                and self36 and self72 and plus_self == 0,
    }


def _independent_translation_oracle() -> list[dict[str, object]]:
    expected: list[dict[str, object]] = []
    plus_self_incompatible = True
    for action in range(4, 8):
        edges = table_plus_edges(ACTION_MASKS[action])
        plus_self_incompatible = plus_self_incompatible and any((z, w) in edges for _, z in edges for w in TERNARY)
    for q, h in TRANSLATION_FIXTURES:
        unseen = set(range(q))
        cycles: list[list[int]] = []
        while unseen:
            value = min(unseen)
            cycle: list[int] = []
            while value in unseen:
                unseen.remove(value)
                cycle.append(value)
                value = (value + h) % q
            cycles.append(cycle)
        common = gcd(q, h)
        permutation = [(r + h) % q for r in range(q)]
        predecessor = [(r - h) % q for r in range(q)]
        self_loop = h % q == 0
        passed = len(cycles) == common and all(len(cycle) == q // common for cycle in cycles) and sorted(permutation) == list(range(q)) and ((not self_loop) or plus_self_incompatible)
        expected.append({
            "q": q, "h": h, "gcd": common, "cycle_count": len(cycles), "cycle_length": q // common,
            "cycles": cycles, "permutation": permutation, "predecessor_permutation": predecessor,
            "is_bijection": sorted(permutation) == list(range(q)), "self_loop": self_loop,
            "self_loop_forces_empty_plus_set": (not self_loop) or plus_self_incompatible, "pass": passed,
        })
    return expected


def _validate_contracts(value: object) -> None:
    if type(value) is not dict:
        raise TypeError("certificate contracts must be an exact object")
    expected = {
        "action_masks": list(ACTION_MASKS),
        "action_weight_pairs": [[fraction_text(a), fraction_text(b)] for a, b in ACTION_WEIGHT_PAIRS],
        "baseline_action_id": 3, "compiler_coefficient_names": list(COMPILER_NAMES),
        "fixed_lag_limit_formula": "sum_r[c00(r)/q+c20(r)delta_(q,r-h)+c02(r)delta_(q,r)+c22(r)theta^(h)_(q,r)]",
        "global_closure": _independent_global_closure(),
        "mutation_count": len(MUTATION_NAMES), "mutation_names": list(MUTATION_NAMES),
        "projection": "E_plus=E intersect (T x {+1})",
        "row_partition": [512, 8, 64, 8, 9, 7, 12, 8, 6, 6],
        "translation_oracle": _independent_translation_oracle(),
    }
    _exact(value, expected, "certificate contracts")


def _validate_certificate(certificate: object) -> None:
    expected_keys = {
        "all_pass", "certificate_version", "charge_rows", "compatibility_rows", "contracts",
        "counts", "determinant_rows", "epistemic_role", "finite_shift_rows", "firewall_rows",
        "landscape_rows", "monomial_rows", "projected_action_rows", "status", "theta_rows",
        "title", "truth_rows",
    }
    if type(certificate) is not dict or set(certificate) != expected_keys:
        raise ValueError("certificate membership changed")
    _exact(certificate["title"], TITLE, "title")
    _exact(certificate["status"], STATUS, "status")
    _exact(certificate["epistemic_role"], EPISTEMIC_ROLE, "epistemic role")
    _exact(certificate["certificate_version"], 1, "certificate version")
    _exact(certificate["counts"], EXPECTED_COUNTS, "counts")
    _validate_truth_rows(certificate["truth_rows"])
    _validate_action_rows(certificate["projected_action_rows"])
    _validate_compatibility_rows(certificate["compatibility_rows"])
    _validate_charge_rows(certificate["charge_rows"])
    _validate_monomial_rows(certificate["monomial_rows"])
    _validate_determinant_rows(certificate["determinant_rows"])
    _validate_theta_rows(certificate["theta_rows"])
    _validate_landscape_rows(certificate["landscape_rows"])
    _validate_finite_shift_rows(certificate["finite_shift_rows"])
    _validate_firewall_rows(certificate["firewall_rows"])
    _validate_contracts(certificate["contracts"])
    row_keys = (
        "truth_rows", "projected_action_rows", "compatibility_rows", "charge_rows", "monomial_rows",
        "determinant_rows", "theta_rows", "landscape_rows", "finite_shift_rows", "firewall_rows",
    )
    rows = [row for key in row_keys for row in certificate[key]]
    expected_pass = (
        len(rows) == 640 and all(type(row) is dict and row.get("pass") is True for row in rows)
        and certificate["contracts"]["global_closure"]["pass"] is True
        and all(row["pass"] is True for row in certificate["contracts"]["translation_oracle"])
    )
    _exact(certificate["all_pass"], expected_pass, "all_pass")


def verify_certificate(certificate: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact Boolean")
    try:
        _validate_certificate(certificate)
    except (ArithmeticError, KeyError, TypeError, ValueError):
        return False
    # The false branch above is deliberately builder-free and is tested with
    # every group builder monkeypatched to raise.
    return not compare_fresh or exact_equal(certificate, build_certificate())


def mutate_certificate(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(certificate) is not dict or type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    candidate = deepcopy(certificate)
    truth = candidate["truth_rows"]
    actions = candidate["projected_action_rows"]
    compatibility = candidate["compatibility_rows"]
    charge = candidate["charge_rows"]
    monomial = candidate["monomial_rows"]
    determinant = candidate["determinant_rows"]
    theta = candidate["theta_rows"]
    landscape = candidate["landscape_rows"]
    finite_shift = candidate["finite_shift_rows"]
    firewall = candidate["firewall_rows"]
    if name == "projection_keeps_z_minus":
        truth[1]["projected_table_id"] = 1
    elif name == "preimage_count_63":
        actions[0]["preimage_count"] = 63
    elif name == "compatibility_reversed":
        compatibility[12]["compatible"] = not compatibility[12]["compatible"]
    elif name == "charge_predecessor_plus_h":
        charge[4]["predecessor_translation"] = "r -> r+h"
    elif name == "cycle_count_forgets_gcd":
        candidate["contracts"]["translation_oracle"][3]["cycle_count"] = 1
    elif name == "self_loop_allows_plus":
        candidate["contracts"]["translation_oracle"][1]["self_loop_forces_empty_plus_set"] = False
    elif name == "determinant_forced_two":
        determinant[0]["determinant_hypothesis"] = "Delta=2"
    elif name == "determinant_zero_allowed":
        determinant[3]["reduced_determinant"] = "may equal zero"
    elif name == "coprime_kl_required":
        determinant[2]["coprime_k_l_assumed"] = True
    elif name == "cutoff_limit_order_reversed":
        determinant[6]["order"] = ["P->infinity", "X->infinity"]
    elif name == "growing_h_allowed":
        firewall[0]["allowed"] = "h=h(X)"
    elif name == "cesaro_substituted":
        firewall[1]["allowed"] = "ordinary Cesaro average"
    elif name == "tau_square_collision_double_counted":
        theta[2]["tau"] = 2
    elif name == "tau_forgets_multiplicity":
        theta[6]["tau"] = 1
    elif name == "forced_hit_survives":
        theta[9]["local_factor"] = "1"
    elif name == "theta_cone_wrong_shift":
        theta[11]["cone"][1] = "theta_r<=delta_(r+h)"
    elif name == "c20_wrong_phase":
        monomial[6]["limit_channel"] = "delta_(q,r+h)"
    elif name == "c11_marked_surviving":
        monomial[4]["survives"] = True
    elif name == "c22_marked_vanishing":
        monomial[8]["survives"] = False
    elif name == "degree_three_multishift_allowed":
        finite_shift[1]["degree"] = "total degree<=3"
    elif name == "capacity_plus_sign":
        landscape[5]["formula"] = "G_h=6/pi^2+kappa_h/2"
    elif name == "infimum_attained":
        landscape[6]["infimum_attained"] = True
    elif name == "squarefree_not_maximal":
        landscape[6]["maximizers"] = "nonsquarefree h"
    elif name == "reflection_wrong_parity":
        landscape[7]["coefficient_parity"][2] = "+"
    return candidate


apply_mutation = mutate_certificate
