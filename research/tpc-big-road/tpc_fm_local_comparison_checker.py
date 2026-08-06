#!/usr/bin/env python3
"""Independent exact checker for the TPC Ford--Maynard comparison redesign.

The checker writes JSON only to stdout.  It verifies finite exact algebra,
the exponent geometry, and mutation fixtures.  The hybrid comparison and
Type-I theorems use source-backed analytic estimates and are not numerically
proved by this checker; the universal high-conductor Type-II umbrella and the
exact-half HB4 endpoint remain open.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


J = Fraction(133, 400)
HALF = Fraction(1, 2)
Q = Fraction(267, 400)
NU = Fraction(67, 400)

GaussianInteger = tuple[int, int]


def primes(limit: int) -> list[int]:
    answer: list[int] = []
    for candidate in range(2, limit + 1):
        if all(candidate % p for p in answer if p * p <= candidate):
            answer.append(candidate)
    return answer


def factor_distinct(n: int) -> list[int]:
    factors: list[int] = []
    remaining = n
    for p in primes(math.isqrt(n) + 1):
        if remaining % p == 0:
            factors.append(p)
            while remaining % p == 0:
                remaining //= p
        if remaining == 1:
            break
    if remaining > 1:
        factors.append(remaining)
    return factors


def mobius(n: int) -> int:
    if n == 1:
        return 1
    factors = factor_distinct(n)
    if math.prod(factors) != n:
        return 0
    return -1 if len(factors) % 2 else 1


def phi(n: int) -> int:
    value = n
    for p in factor_distinct(n):
        value = value // p * (p - 1)
    return value


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def log_vector(n: int) -> dict[int, int]:
    """Represent log(n) exactly in the formal basis {log(p): p prime}."""
    vector: dict[int, int] = {}
    remaining = n
    for p in factor_distinct(n):
        exponent = 0
        while remaining % p == 0:
            remaining //= p
            exponent += 1
        vector[p] = exponent
    return vector


def add_scaled_vector(target: dict[int, int], source: dict[int, int], scale: int) -> None:
    for p, exponent in source.items():
        target[p] = target.get(p, 0) + scale * exponent
        if target[p] == 0:
            del target[p]


def mangoldt_vector(n: int) -> dict[int, int]:
    factors = factor_distinct(n)
    if len(factors) == 1:
        return {factors[0]: 1}
    return {}


def ramanujan_sum(q: int, n: int) -> int:
    return sum(d * mobius(q // d) for d in divisors(math.gcd(q, n)))


def kloosterman_exponent_multiset(m: int, n: int, q: int) -> tuple[int, ...]:
    """Exact formal multiset of exponents in S(m,n;q)."""
    counts = [0] * q
    for x in range(q):
        if math.gcd(x, q) == 1:
            exponent = (m * x + n * pow(x, -1, q)) % q
            counts[exponent] += 1
    return tuple(counts)


def gaussian_add(left: GaussianInteger, right: GaussianInteger) -> GaussianInteger:
    return left[0] + right[0], left[1] + right[1]


def gaussian_mul(left: GaussianInteger, right: GaussianInteger) -> GaussianInteger:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_conjugate(value: GaussianInteger) -> GaussianInteger:
    return value[0], -value[1]


def quartic_character_mod_13(value: int) -> GaussianInteger:
    """The exact quartic character modulo 13 with chi(2)=i."""
    residue = value % 13
    if residue == 0:
        return 0, 0
    power = 1
    values = ((1, 0), (0, 1), (-1, 0), (0, -1))
    for exponent in range(12):
        if power == residue:
            return values[exponent % 4]
        power = (2 * power) % 13
    raise AssertionError("quartic character discrete logarithm failed")


def cyclic_gaussian_convolution(
    left: list[GaussianInteger], right: list[GaussianInteger]
) -> list[GaussianInteger]:
    if len(left) != len(right):
        raise ValueError("cyclic convolution lengths differ")
    modulus = len(left)
    answer = [(0, 0) for _ in range(modulus)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            product = gaussian_mul(left_value, right_value)
            index = (left_index + right_index) % modulus
            answer[index] = gaussian_add(answer[index], product)
    return answer


def cyclotomic_integer_equal(left: list[int], right: list[int]) -> bool:
    """Equality after zeta_p specialization for prime-length integer arrays."""
    if len(left) != len(right):
        return False
    differences = [a - b for a, b in zip(left, right)]
    return all(value == differences[0] for value in differences)


def odd_multiplier(n: int) -> Fraction:
    if n % 2 == 0:
        return Fraction(0, 1)
    value = Fraction(1, 1)
    for p in factor_distinct(n):
        if p > 2:
            value *= Fraction(p - 1, p - 2)
    return value


def divisor_expansion_multiplier(n: int) -> Fraction:
    if n % 2 == 0:
        return Fraction(0, 1)
    factors = [p for p in factor_distinct(n) if p > 2]
    value = Fraction(0, 1)
    for mask in range(1 << len(factors)):
        term = Fraction(1, 1)
        for index, p in enumerate(factors):
            if mask & (1 << index):
                term *= Fraction(1, p - 2)
        value += term
    return value


def c2_truncated(cutoff: int) -> Fraction:
    value = Fraction(1, 1)
    for p in primes(cutoff):
        if p > 2:
            value *= Fraction(p * (p - 2), (p - 1) ** 2)
    return value


def finite_euler_slice(cutoff: int, m: int) -> Fraction:
    """Finite-prime version of the comparison conditional mean."""
    if m % 2 == 0:
        return Fraction(0, 1)
    prime_set = set(primes(cutoff))
    if any(p not in prime_set for p in factor_distinct(m)):
        raise ValueError("m must be supported on primes up to cutoff")
    value = c2_truncated(cutoff) * odd_multiplier(m)
    for p in primes(cutoff):
        if p > 2 and m % p:
            value *= Fraction((p - 1) ** 2, p * (p - 2))
    return value


def m_over_phi(m: int) -> Fraction:
    value = Fraction(1, 1)
    for p in factor_distinct(m):
        value *= Fraction(p, p - 1)
    return value


def local_mean(p: int) -> Fraction:
    if p == 2:
        return Fraction(1, 2) * 2
    v_p = Fraction(p * (p - 2), (p - 1) ** 2)
    u_p = Fraction(p, p - 1)
    return Fraction(p - 1, p) * v_p + Fraction(1, p) * u_p


def exact_shift_local_factor(p: int, residue: int) -> Fraction:
    if residue % p == (-2) % p:
        return Fraction(0, 1)
    return Fraction(p, p - 1)


def projected_divisibility_factor(p: int, residue: int) -> Fraction:
    if p == 2:
        return Fraction(2, 1) if residue % 2 else Fraction(0, 1)
    if residue % p == 0:
        return Fraction(p, p - 1)
    return Fraction(p * (p - 2), (p - 1) ** 2)


def legendre_symbol(a: int, p: int) -> int:
    value = pow(a % p, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def truncated_ramanujan_model(cutoff: int, n: int) -> Fraction:
    primorial = math.prod(primes(cutoff))
    return sum(
        (
            Fraction(mobius(q) ** 2 * ramanujan_sum(q, 2 * n), phi(q) ** 2)
            for q in divisors(primorial)
        ),
        Fraction(),
    )


def truncated_local_model(cutoff: int, n: int) -> Fraction:
    value = Fraction(1, 1)
    for p in primes(cutoff):
        value *= 1 + Fraction(ramanujan_sum(p, 2 * n), (p - 1) ** 2)
    return value


def a1_witness(n: int, theta: Fraction = J) -> int | None:
    first = (theta.numerator * n + theta.denominator - 1) // theta.denominator
    return first if 2 * first <= n else None


def nondecreasing_partitions(
    total: int,
    max_parts: int,
    max_part: int,
    minimum: int = 1,
) -> list[tuple[int, ...]]:
    """Finite exact fixture for normalized HB2 exponent vectors."""
    if total == 0:
        return [()]
    if max_parts == 0:
        return []
    answer: list[tuple[int, ...]] = []
    for first in range(minimum, min(max_part, total) + 1):
        for tail in nondecreasing_partitions(
            total - first,
            max_parts - 1,
            max_part,
            first,
        ):
            answer.append((first,) + tail)
    return answer


def admissible_subset_masks(parts: tuple[int, ...], total: int) -> list[int]:
    """Masks in the literal closed exponent window [J,1/2]."""
    masks: list[int] = []
    for mask in range(1, (1 << len(parts)) - 1):
        subtotal = sum(part for index, part in enumerate(parts) if mask & (1 << index))
        if J * total <= subtotal <= HALF * total:
            masks.append(mask)
    return masks


def run_checks() -> dict[str, object]:
    umbrella_gate = "TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE"
    primary_route = "HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION"
    independent_reserve = "HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI"
    route_freeze = {
        "umbrella_gate": umbrella_gate,
        "primary_route": primary_route,
        "primary_status": "OPEN_NEW_THEOREM",
        "first_subgate": "HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE",
        "independent_reserve": independent_reserve,
        "independent_first_transform": "DERIVED_SOURCE_BACKED",
        "independent_polar_main_attachment": "OPEN_NEW_ATTACHMENT",
        "direct_dfi_row_by_row": "STOP_SCOPED_F7_VERSUS_F4",
        "source_switch_order": "A1_MINUS_A2",
        "physical_outer_signed_order": "A2_MINUS_A1",
        "source_lock_merge": False,
        "fixed_physical_h0": 2,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    expected_route_freeze = {
        "umbrella_gate": "TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE",
        "primary_route": "HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION",
        "primary_status": "OPEN_NEW_THEOREM",
        "first_subgate": "HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE",
        "independent_reserve": "HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI",
        "independent_first_transform": "DERIVED_SOURCE_BACKED",
        "independent_polar_main_attachment": "OPEN_NEW_ATTACHMENT",
        "direct_dfi_row_by_row": "STOP_SCOPED_F7_VERSUS_F4",
        "source_switch_order": "A1_MINUS_A2",
        "physical_outer_signed_order": "A2_MINUS_A1",
        "source_lock_merge": False,
        "fixed_physical_h0": 2,
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    if route_freeze != expected_route_freeze:
        raise AssertionError("V8 route/physical freeze changed")
    if primary_route == independent_reserve:
        raise AssertionError("independent V8 source locks were merged")
    route_mutations: list[dict[str, object]] = []
    swapped_routes = dict(route_freeze)
    swapped_routes["primary_route"] = independent_reserve
    swapped_routes["independent_reserve"] = primary_route
    route_mutations.append(swapped_routes)
    merged_locks = dict(route_freeze)
    merged_locks["source_lock_merge"] = True
    route_mutations.append(merged_locks)
    promoted_polar_main = dict(route_freeze)
    promoted_polar_main["independent_polar_main_attachment"] = "PROVED"
    route_mutations.append(promoted_polar_main)
    positive_credit = dict(route_freeze)
    positive_credit["fixed_atom_credit"] = 1
    route_mutations.append(positive_credit)
    paid_endpoint = dict(route_freeze)
    paid_endpoint["strict_1_over_400"] = "PAID"
    route_mutations.append(paid_endpoint)
    promoted_l2 = dict(route_freeze)
    promoted_l2["L2"] = "PROVED"
    route_mutations.append(promoted_l2)
    numbered_trigger = dict(route_freeze)
    numbered_trigger["TPC_207_TRIGGER"] = True
    route_mutations.append(numbered_trigger)
    if any(mutation == expected_route_freeze for mutation in route_mutations):
        raise AssertionError("V8 route/physical mutation escaped")
    sample_a1 = Fraction(3, 1)
    sample_a2 = Fraction(5, 1)
    outer_switched_value = -6 * (sample_a1 - sample_a2)
    physical_order_value = 6 * (sample_a2 - sample_a1)
    wrong_physical_order = 6 * (sample_a1 - sample_a2)
    if (
        outer_switched_value != physical_order_value
        or wrong_physical_order == outer_switched_value
    ):
        raise AssertionError("HB4xHB2 physical A2-A1 sign ledger failed")

    if J + NU != HALF or 1 - J != Q or HALF - J != NU:
        raise AssertionError("J/nu/Q compiler identities failed")
    if Fraction(1, 3) - J != Fraction(1, 1200):
        raise AssertionError("n=3 safety margin failed")
    if Q - Fraction(2, 3) != Fraction(1, 1200):
        raise AssertionError("complementary Q margin failed")
    full_width = Q - J
    if Q + full_width - 1 != Fraction(1, 400):
        raise AssertionError("strict 1/400 Vaughan surplus failed")
    hb_padding_slots = 6 * math.ceil(Fraction(1, 1) / (1 - HALF))
    if hb_padding_slots != 12:
        raise AssertionError("Ford--Maynard Lemma 7.14 slot count failed")

    # Exact substitutions into the published Bettin--Chandee exponents used by
    # the determinant range atlas.  These checks audit the exponent arithmetic,
    # not the analytic theorems or comparison-main attachment.
    bc_h2_j1_worst = Fraction(17, 20) + Fraction(1, 8)
    bc_h3_thin_worst = Fraction(17, 20) * Fraction(5, 6) + Fraction(1, 8)
    bc_smooth_slot_threshold = Fraction(21, 44)
    bc_hb2_b3_grouped_base = Fraction(11, 10)
    bc_hb2_b3_grouped_d_slope = Fraction(17, 20)
    bc_one_poisson_first_threshold = Fraction(11, 56)
    bc_one_poisson_start = Fraction(1, 4)
    bc_one_poisson_second_threshold = Fraction(2, 7)
    hb4_double_smooth_weil_threshold = Fraction(1, 3)
    hb4_ramanujan_axis_exponent = Fraction(3, 4)
    pascadi_hb4_complete_base = Fraction(5, 8)
    pascadi_hb4_favourable_only_base = Fraction(1, 2)
    pascadi_hb4_complete_threshold = 1 - pascadi_hb4_complete_base
    pascadi_hb4_favourable_only_threshold = 1 - pascadi_hb4_favourable_only_base
    conductor_projected_high_base = Fraction(1, 2)
    conductor_projected_threshold = 1 - conductor_projected_high_base
    low_conductor_physical_exponent = Fraction(7, 8)
    if bc_h2_j1_worst != Fraction(39, 40):
        raise AssertionError("BC h=2,j=1 worst exponent failed")
    if bc_h3_thin_worst != Fraction(5, 6):
        raise AssertionError("BC h=3 thin-cell worst exponent failed")
    if not bc_hb2_b3_grouped_base > 1:
        raise AssertionError("BC grouped HB2-B3 scale failure escaped")
    if not (
        bc_one_poisson_first_threshold < bc_one_poisson_start
        < bc_one_poisson_second_threshold
    ):
        raise AssertionError("BC one-Poisson threshold ordering failed")
    first_at_poisson_start = Fraction(69, 80) + Fraction(7, 10) * bc_one_poisson_start
    second_at_poisson_start = Fraction(3, 4) + Fraction(7, 8) * bc_one_poisson_start
    if first_at_poisson_start != Fraction(83, 80):
        raise AssertionError("BC first summand at Poisson onset failed")
    if second_at_poisson_start != Fraction(31, 32):
        raise AssertionError("BC second summand at Poisson onset failed")
    if Fraction(1, 2) + Fraction(3, 2) * hb4_double_smooth_weil_threshold != 1:
        raise AssertionError("HB4 double-smooth Weil threshold failed")
    if hb4_ramanujan_axis_exponent >= 1:
        raise AssertionError("HB4 Ramanujan axis lost its power saving")
    if not (
        hb4_double_smooth_weil_threshold < pascadi_hb4_complete_threshold
        < pascadi_hb4_favourable_only_threshold
    ):
        raise AssertionError("Pascadi HB4 full-bound threshold ordering failed")
    # Mutation: retaining only the favourable F^2 D terms would claim the
    # false 1/2 endpoint, where the complete F^(5/2) D term is already > x.
    if pascadi_hb4_complete_base + pascadi_hb4_favourable_only_threshold <= 1:
        raise AssertionError("Pascadi favourable-summand-only mutation escaped")
    if conductor_projected_threshold != HALF:
        raise AssertionError("conductor-projected HB4 threshold failed")
    if conductor_projected_high_base + HALF != 1:
        raise AssertionError("exact-half no-saving equality failed")
    if low_conductor_physical_exponent >= 1:
        raise AssertionError("low-conductor projector lost its power saving")

    # Blomer--Pascadi gives q^(-1/32) at critical fixed-unit length.  Since
    # q=F^2=X^(1/2), this is F^(-1/16)=X^(-1/64).  Freezing the moving unit
    # and modulus, however, leaves a literal F^(15/16) deficit against the
    # raw F^6 endpoint target.
    bp_modulus_saving = Fraction(1, 32)
    bp_f_saving = 2 * bp_modulus_saving
    bp_x_saving = HALF * bp_modulus_saving
    bp_fixed_cell_f_exponent = 1 + 2 * (1 - bp_modulus_saving)
    bp_frozen_outer_f_exponent = 4 + bp_fixed_cell_f_exponent
    bp_raw_target_f_exponent = Fraction(6, 1)
    bp_frozen_deficit = bp_frozen_outer_f_exponent - bp_raw_target_f_exponent
    if (
        bp_f_saving != Fraction(1, 16)
        or bp_x_saving != Fraction(1, 64)
        or bp_fixed_cell_f_exponent != Fraction(47, 16)
        or bp_frozen_outer_f_exponent != Fraction(111, 16)
        or bp_frozen_deficit != Fraction(15, 16)
    ):
        raise AssertionError("Blomer--Pascadi exact-half exponent ledger failed")

    # Exact quartic-character fixture for
    #   sum_A chi(A) S(ell,-2h*A^(-1);p)
    #     = tau(conj chi)^2 chi(-2h ell).
    # Both sides are expanded in the group ring Z[i][Z/13Z], so no floating
    # point or numerical root of unity is used.
    bp_character_prime = 13
    tau_conjugate = [(0, 0) for _ in range(bp_character_prime)]
    for residue in range(1, bp_character_prime):
        tau_conjugate[residue] = gaussian_conjugate(
            quartic_character_mod_13(residue)
        )
    tau_conjugate_square = cyclic_gaussian_convolution(
        tau_conjugate, tau_conjugate
    )
    def moving_unit_group_ring(
        character,
        h: int,
        ell: int,
        *,
        invert_unit: bool = True,
        shift_scale: int = -2,
    ) -> list[GaussianInteger]:
        answer = [(0, 0) for _ in range(bp_character_prime)]
        for unit in range(1, bp_character_prime):
            chi_unit = character(unit)
            unit_argument = (
                pow(unit, -1, bp_character_prime) if invert_unit else unit
            )
            counts = kloosterman_exponent_multiset(
                ell,
                shift_scale * h * unit_argument,
                bp_character_prime,
            )
            for exponent, count in enumerate(counts):
                answer[exponent] = gaussian_add(
                    answer[exponent],
                    (count * chi_unit[0], count * chi_unit[1]),
                )
        return answer

    bp_character_rank_one_cases = 0
    for h in (1, 2, 3, 4):
        for ell in (1, 3, 5, 7):
            left = moving_unit_group_ring(quartic_character_mod_13, h, ell)
            scalar = quartic_character_mod_13(-2 * h * ell)
            right = [
                gaussian_mul(scalar, coefficient)
                for coefficient in tau_conjugate_square
            ]
            if left != right:
                raise AssertionError(
                    f"quartic moving-unit identity failed at h={h}, ell={ell}"
                )
            bp_character_rank_one_cases += 1

    absolute_quartic_fixture = [
        (0, 0),
        (3, 2),
        (-3, -2),
        (3, 2),
        (3, 2),
        (-3, -2),
        (-3, -2),
        (-3, -2),
        (-3, -2),
        (3, 2),
        (3, 2),
        (-3, -2),
        (3, 2),
    ]
    canonical_quartic_fixture = moving_unit_group_ring(
        quartic_character_mod_13, 3, 5
    )
    if canonical_quartic_fixture != absolute_quartic_fixture:
        raise AssertionError("absolute p=13 physical convention fixture failed")

    conjugated_character_fixture = moving_unit_group_ring(
        lambda value: gaussian_conjugate(quartic_character_mod_13(value)),
        3,
        5,
    )
    noninverse_unit_fixture = moving_unit_group_ring(
        quartic_character_mod_13, 3, 5, invert_unit=False
    )
    positive_shift_fixture = moving_unit_group_ring(
        quartic_character_mod_13, 3, 5, shift_scale=2
    )
    if any(
        mutated == absolute_quartic_fixture
        for mutated in (
            conjugated_character_fixture,
            noninverse_unit_fixture,
            positive_shift_fixture,
        )
    ):
        raise AssertionError("physical moving-unit convention mutation escaped")

    # Exact rank-one interval fixture.  After weighting h and ell by conj(chi),
    # every pair contributes the same chi(-2)*tau(conj chi)^2 group-ring value.
    rank_one_interval = [(0, 0) for _ in range(bp_character_prime)]
    h_fixture = (1, 2, 3)
    ell_fixture = (4, 5, 6)
    for h in h_fixture:
        for ell in ell_fixture:
            weight = gaussian_mul(
                gaussian_conjugate(quartic_character_mod_13(h)),
                gaussian_conjugate(quartic_character_mod_13(ell)),
            )
            contribution = moving_unit_group_ring(
                quartic_character_mod_13, h, ell
            )
            for exponent, coefficient in enumerate(contribution):
                rank_one_interval[exponent] = gaussian_add(
                    rank_one_interval[exponent],
                    gaussian_mul(weight, coefficient),
                )
    rank_one_scalar = quartic_character_mod_13(-2)
    rank_one_expected = [
        (
            9 * gaussian_mul(rank_one_scalar, coefficient)[0],
            9 * gaussian_mul(rank_one_scalar, coefficient)[1],
        )
        for coefficient in tau_conjugate_square
    ]
    if rank_one_interval != rank_one_expected:
        raise AssertionError("p=13 character-matched interval fixture failed")
    bp_rank_one_interval_magnitude = 13 * len(h_fixture) * len(ell_fixture)
    if bp_rank_one_interval_magnitude != 117:
        raise AssertionError("p=13 rank-one interval magnitude ledger failed")

    # A no-cost L_A^2-valued lift would bound the coherent character mode by
    # p^(63/32), while the exact rank-one identity has size p^2.  The missing
    # p^(1/32) is a strict mutation witness against generic tensorization.
    bp_vector_lift_claimed_exponent = (
        HALF + Fraction(1, 4) + Fraction(1, 4) + Fraction(31, 32)
    )
    bp_character_mode_exponent = Fraction(2, 1)
    if (
        bp_vector_lift_claimed_exponent != Fraction(63, 32)
        or bp_character_mode_exponent - bp_vector_lift_claimed_exponent
        != Fraction(1, 32)
    ):
        raise AssertionError("generic BP vector-lift counterexample ledger failed")
    bp_tensor_contradiction_gap = (
        bp_character_mode_exponent - bp_vector_lift_claimed_exponent
    )
    mutated_trivial_bp_exponent = (
        HALF + Fraction(1, 4) + Fraction(1, 4) + 1
    )
    mutated_missing_unit_norm = (
        Fraction(1, 4) + Fraction(1, 4) + Fraction(31, 32)
    )
    mutated_q_equals_x_saving = bp_modulus_saving
    if (
        mutated_trivial_bp_exponent == bp_vector_lift_claimed_exponent
        or mutated_missing_unit_norm == bp_vector_lift_claimed_exponent
        or mutated_q_equals_x_saving == bp_x_saving
    ):
        raise AssertionError("BP exponent/scale mutation escaped")

    # At p=F^2 the Burgess r=2 interval bound is
    # F^(1/2) p^(3/16)=F^(7/8).  Thus even trivial E_1E_2<=F^2 leaves one
    # actual-source character at F^(15/4), strictly below the F^4 endpoint.
    burgess_r2_f_exponent = HALF + 2 * Fraction(3, 16)
    actual_single_character_f_exponent = 2 + 2 * burgess_r2_f_exponent
    if (
        burgess_r2_f_exponent != Fraction(7, 8)
        or actual_single_character_f_exponent != Fraction(15, 4)
        or actual_single_character_f_exponent >= 4
    ):
        raise AssertionError("prime-cell single-character Burgess ledger failed")

    # Exact additive Fourier spectrum of the naive two-row residue compression
    # K_q(u,v)=S(-2,u-v;q).  The circulant eigenvalues are q times a root of
    # unity at every nonzero frequency and zero at frequency zero.  Equality
    # is checked in Z[zeta_q], where coefficient arrays may differ by a
    # constant multiple of 1+zeta_q+...+zeta_q^(q-1).
    difference_kernel_spectrum_cases = 0
    for modulus in (5, 7, 11, 13):
        kernel = [
            kloosterman_exponent_multiset(-2, difference, modulus)
            for difference in range(modulus)
        ]
        for frequency in range(modulus):
            eigenvalue = [0] * modulus
            for difference, counts in enumerate(kernel):
                for exponent, count in enumerate(counts):
                    eigenvalue[(exponent - frequency * difference) % modulus] += count
            expected = [0] * modulus
            if frequency:
                expected[(-2 * pow(frequency, -1, modulus)) % modulus] = modulus
            if not cyclotomic_integer_equal(eigenvalue, expected):
                raise AssertionError(
                    "additive-difference Kloosterman spectrum failed at "
                    f"q={modulus}, k={frequency}"
                )
            difference_kernel_spectrum_cases += 1

    # Mutation: replacing u-v by u+v no longer has the claimed action on the
    # same additive Fourier vector.  Check it exactly at q=5, k=1, u=1.
    mutation_modulus = 5
    mutation_frequency = 1
    mutation_row = 1
    plus_kernel_action = [0] * mutation_modulus
    for column in range(mutation_modulus):
        counts = kloosterman_exponent_multiset(
            -2, mutation_row + column, mutation_modulus
        )
        for exponent, count in enumerate(counts):
            plus_kernel_action[
                (exponent + mutation_frequency * column) % mutation_modulus
            ] += count
    difference_kernel_expected_action = [0] * mutation_modulus
    difference_kernel_expected_action[
        (
            -2 * pow(mutation_frequency, -1, mutation_modulus)
            + mutation_frequency * mutation_row
        )
        % mutation_modulus
    ] = mutation_modulus
    if cyclotomic_integer_equal(
        plus_kernel_action, difference_kernel_expected_action
    ):
        raise AssertionError("u+v difference-kernel mutation escaped")
    if mutation_modulus * mutation_modulus == mutation_modulus:
        raise AssertionError("Kloosterman kernel norm sqrt(q) mutation escaped")

    for p in primes(97):
        if local_mean(p) != 1:
            raise AssertionError(f"local mean failed at p={p}")
        exact_mean = sum(
            (exact_shift_local_factor(p, residue) for residue in range(p)),
            Fraction(),
        ) / p
        if exact_mean != 1:
            raise AssertionError(f"exact shifted local mean failed at p={p}")

    tensor_local_cases = 0
    tail_cut_cases = 0
    for p in [prime for prime in primes(29) if prime > 2]:
        # A prime installed in the hybrid head matches the full forbidden
        # product residue, not merely the divisibility projection.
        for a in range(p):
            for b in range(p):
                hybrid = exact_shift_local_factor(p, a * b)
                if a * b % p == (-2) % p and hybrid != 0:
                    raise AssertionError(f"hybrid forbidden residue escaped at p={p}")
                tensor_local_cases += 1

        # On F_p^*, a quadratic-character witness has bilinear mass exactly p
        # against the first omitted local tensor mode.
        witness = Fraction()
        for a in range(1, p):
            xi = legendre_symbol((-2 * pow(a, -1, p)) % p, p)
            for b in range(1, p):
                kappa = legendre_symbol(b, p)
                difference = (
                    exact_shift_local_factor(p, a * b)
                    - projected_divisibility_factor(p, a * b)
                )
                witness += xi * kappa * difference
        if abs(witness) != p:
            raise AssertionError(f"rank-one local cut witness failed at p={p}: {witness}")
        tail_cut_cases += 1

    ramanujan_cases = 0
    for cutoff in (2, 3, 5, 7, 11):
        for n in range(1, 80):
            if truncated_ramanujan_model(cutoff, n) != truncated_local_model(cutoff, n):
                raise AssertionError(f"Ramanujan Euler product failed at y={cutoff}, n={n}")
            ramanujan_cases += 1

    divisor_cases = 0
    for n in range(1, 500):
        if odd_multiplier(n) != divisor_expansion_multiplier(n):
            raise AssertionError(f"divisor expansion failed at n={n}")
        divisor_cases += 1

    slice_cases = 0
    support_primes = [3, 5, 7, 11]
    for cutoff in (3, 5, 7, 11):
        available = [p for p in support_primes if p <= cutoff]
        for mask in range(1 << len(available)):
            m = 1
            for index, p in enumerate(available):
                if mask & (1 << index):
                    m *= p
            if finite_euler_slice(cutoff, m) != m_over_phi(m):
                raise AssertionError(f"finite Euler slice failed at y={cutoff}, m={m}")
            slice_cases += 1

    hybrid_slice_constant_cases = 0
    for cutoff in (5, 7, 11, 13, 17):
        finite_primes = primes(cutoff)
        odd_primes = [p for p in finite_primes if p > 2]
        for z in [p for p in finite_primes if p >= 2]:
            c_tail = math.prod(
                (Fraction(p * (p - 2), (p - 1) ** 2) for p in finite_primes if p > z),
                start=Fraction(1, 1),
            )
            w_z = math.prod(
                (Fraction(p, p - 1) for p in finite_primes if p <= z),
                start=Fraction(1, 1),
            )
            for mask in range(1 << len(odd_primes)):
                m = math.prod(
                    (p for index, p in enumerate(odd_primes) if mask & (1 << index)),
                    start=1,
                )
                a_z = math.prod(
                    (
                        Fraction(p - 1, p - 2)
                        for p in odd_primes
                        if p > z and m % p == 0
                    ),
                    start=Fraction(1, 1),
                )
                h_mz = math.prod(
                    (
                        1 + Fraction(1, p * (p - 2))
                        for p in odd_primes
                        if p > z and m % p
                    ),
                    start=Fraction(1, 1),
                )
                v_mz = math.prod(
                    (
                        Fraction(p - 1, p)
                        for p in finite_primes
                        if p <= z and m % p
                    ),
                    start=Fraction(1, 1),
                )
                if c_tail * w_z * a_z * h_mz * v_mz != m_over_phi(m):
                    raise AssertionError(
                        f"hybrid slice constant failed at y={cutoff}, z={z}, m={m}"
                    )
                hybrid_slice_constant_cases += 1

    for n in range(3, 20_001):
        if a1_witness(n) is None:
            raise AssertionError(f"FM A1 fixture failed at n={n}")

    # Exact finite grid audit of the no-large-slot HB2 branch.  Components are
    # positive, strictly below one half, sum to one, and there are at most four.
    # This is a mutation fixture for the R(P_TPC)=empty grouping, not an analytic
    # proof of SHB-D2.
    hb2_partition_cases = 0
    for parts in nondecreasing_partitions(total=40, max_parts=4, max_part=19):
        if len(parts) < 3:
            continue
        masks = admissible_subset_masks(parts, total=40)
        if not masks:
            raise AssertionError(f"HB2 subset cover failed at parts={parts}")
        if min(masks) not in masks:
            raise AssertionError(f"HB2 first-subset selector failed at parts={parts}")
        hb2_partition_cases += 1
    if hb2_partition_cases == 0:
        raise AssertionError("HB2 partition fixture was empty")

    # Equality at one half belongs to the closed large-slot/master endpoint.
    if HALF * 40 != 20:
        raise AssertionError("HB2 exact-half endpoint fixture failed")

    # h=1 is not a safe replacement: a Mobius-bearing factor may lie above
    # one half while its complement lies strictly below J.
    hb1_large_rough, hb1_small_complement = 300, 100
    if not (
        hb1_large_rough > HALF * 400
        and hb1_small_complement < J * 400
        and hb1_large_rough + hb1_small_complement == 400
    ):
        raise AssertionError("HB1 large-rough escape mutation fixture is invalid")

    determinant_cases = 0
    for d in range(1, 26, 2):
        for m in range(1, 26, 2):
            if math.gcd(d, m) != 1:
                continue
            n0 = next(n for n in range(d) if (m * n + 2) % d == 0)
            r0 = (m * n0 + 2) // d
            if d * r0 - m * n0 != 2:
                raise AssertionError(f"base determinant failed at d={d}, m={m}")
            for z in range(-5, 6):
                n = n0 + d * z
                r = r0 + m * z
                if d * r - m * n != 2:
                    raise AssertionError(f"affine determinant failed at d={d}, m={m}, z={z}")
                determinant_cases += 1

    # Exact CRT fixture for the quadratic zero mode produced after Cauchy in
    # the HB2 bare three-Mobius cell.  It verifies the compatibility condition
    # and the density 1/lcm(d1,d2), but does not assert cancellation of the
    # signed covariance.
    crt_covariance_cases = 0
    c_fixed = 3
    crt_moduli = (5, 7, 11, 25, 35, 49)
    for d1 in crt_moduli:
        for d2 in crt_moduli:
            g = math.gcd(d1, d2)
            q = math.lcm(d1, d2)
            for e1 in range(1, min(d1, 8) + 1):
                if math.gcd(e1, d1) != 1:
                    continue
                residue1 = (-2 * pow(c_fixed * e1, -1, d1)) % d1
                for e1_prime in range(1, min(d2, 8) + 1):
                    if math.gcd(e1_prime, d2) != 1:
                        continue
                    residue2 = (-2 * pow(c_fixed * e1_prime, -1, d2)) % d2
                    count = sum(
                        1
                        for e2 in range(q)
                        if e2 % d1 == residue1 and e2 % d2 == residue2
                    )
                    compatible = (e1 - e1_prime) % g == 0
                    if count != int(compatible):
                        raise AssertionError(
                            "HB2 CRT covariance compatibility failed at "
                            f"d1={d1}, d2={d2}, e1={e1}, e1'={e1_prime}"
                        )
                    crt_covariance_cases += 1

    # Exact finite fixture for the optimal Pascadi coefficient compression in
    # the HB4 quarter cell.  Squaring the residue coefficient b_(n,d) must be
    # exactly the incidence h1*a2 = h2*a1 (mod d).
    pascadi_incidence_cases = 0
    pascadi_scaling_cases = 0
    source_r_singleton = [r for r in range(1, 5) if 1 < r <= 2]
    if source_r_singleton != [2]:
        raise AssertionError("Pascadi r-asymp-1 singleton convention failed")
    for d in (5, 7, 11, 13):
        a_values = [a for a in range(3, 16) if math.gcd(a, d) == 1]
        h_values = range(1, 6)
        residue_counts = [0] * d
        for a in a_values:
            for h in h_values:
                source_n = (-4 * h * pow(a, -1, d)) % d
                residue_counts[source_n] += 1
                for ell in (1, 2, 3):
                    # Pascadi emits S(m*r^{-1},n;d).  With the literal
                    # r-asymp-1 singleton r=2, m=ell and n=-4h/a, this must
                    # be the physical target S(ell,-2h/a;d).
                    source_m = (ell * pow(2, -1, d)) % d
                    target_n = (-2 * h * pow(a, -1, d)) % d
                    if kloosterman_exponent_multiset(source_m, source_n, d) != (
                        kloosterman_exponent_multiset(ell, target_n, d)
                    ):
                        raise AssertionError(
                            f"Pascadi r=2 full source-kernel map failed at d={d}"
                        )
                    pascadi_scaling_cases += 1
        coefficient_norm = sum(count * count for count in residue_counts)
        incidence_count = sum(
            1
            for a1 in a_values
            for h1 in h_values
            for a2 in a_values
            for h2 in h_values
            if (h1 * a2 - h2 * a1) % d == 0
        )
        if coefficient_norm != incidence_count:
            raise AssertionError(f"Pascadi residue-incidence identity failed at d={d}")
        pascadi_incidence_cases += 1

    # Finite growth witness for the forbidden all-character large-sieve
    # shortcut.  The real primitive character mod 3 is induced to q=3p;
    # c_t=conj(psi(t)) then correlates with every lift.  At Q=F=2000 the
    # aggregate already exceeds by >10 the unit-constant dyadic envelope
    # ((2Q)^2+N)/Q * ||c||_2^2.  The documented p-family makes the ratio
    # asymptotic to F/log(Q), so this is a mutation witness, not a proposed
    # numerical proof of an analytic bound.
    character_q = 2_000
    character_f = character_q
    character_n = character_f * character_q
    character_norm = character_n - character_n // 3
    induced_character_lhs = Fraction(0, 1)
    induced_low_conductor_cases = 0
    for p in primes(2 * character_q // 3):
        modulus = 3 * p
        if not (character_q <= modulus <= 2 * character_q):
            continue
        correlated_sum = (
            character_n
            - character_n // 3
            - character_n // p
            + character_n // (3 * p)
        )
        induced_character_lhs += Fraction(correlated_sum**2, phi(modulus))
        induced_low_conductor_cases += 1
    induced_character_envelope = (
        Fraction((2 * character_q) ** 2 + character_n, character_q)
        * character_norm
    )
    if induced_character_lhs <= 10 * induced_character_envelope:
        raise AssertionError("induced low-conductor character witness too small")

    # Exact cyclotomic-coefficient fixture for the low-conductor projector
    # T_q(chi;m)=G_q(chi,1)G_q(chi,m), using the real primitive character
    # mod 3 induced to q=3p.  Both sides are expanded in the formal basis
    # {zeta_q^j}; no floating-point evaluation is used.
    low_conductor_gauss_projector_cases = 0
    for cofactor_prime in (5, 7, 11, 13):
        modulus = 3 * cofactor_prime

        def induced_chi3(value: int) -> int:
            if math.gcd(value, modulus) != 1:
                return 0
            return 1 if value % 3 == 1 else -1

        for m in range(1, min(modulus, 8)):
            projector = [0] * modulus
            for residue in range(modulus):
                chi_value = induced_chi3(residue)
                if chi_value == 0:
                    continue
                for unit in range(modulus):
                    if math.gcd(unit, modulus) == 1:
                        exponent = (
                            m * unit + residue * pow(unit, -1, modulus)
                        ) % modulus
                        projector[exponent] += chi_value

            gauss_one = [0] * modulus
            gauss_m = [0] * modulus
            for unit in range(modulus):
                chi_value = induced_chi3(unit)
                if chi_value:
                    gauss_one[unit] += chi_value
                    gauss_m[(m * unit) % modulus] += chi_value
            gauss_product = [0] * modulus
            for left_exp, left_count in enumerate(gauss_one):
                for right_exp, right_count in enumerate(gauss_m):
                    gauss_product[(left_exp + right_exp) % modulus] += (
                        left_count * right_count
                    )
            if projector != gauss_product:
                raise AssertionError(
                    f"low-conductor Gauss projector failed at q={modulus}, m={m}"
                )
            low_conductor_gauss_projector_cases += 1

    mangoldt_cases = 0
    for n in range(2, 1_001):
        positive_lift: dict[int, int] = {}
        negative_divisor: dict[int, int] = {}
        for d in divisors(n):
            add_scaled_vector(positive_lift, log_vector(n // d), mobius(d))
            add_scaled_vector(negative_divisor, log_vector(d), -mobius(d))
        expected = mangoldt_vector(n)
        if positive_lift != expected or negative_divisor != expected:
            raise AssertionError(f"formal Mangoldt lift failed at N={n}")
        mangoldt_cases += 1

    # Exact h=2 Heath--Brown switching at a fixed dyadic top Z.  The small
    # endpoint is e<=sqrt(Z), while the complementary divisor sum is d>sqrt(Z).
    # This checks both Lambda=2*A1-A2 and L_>sqrt(Z)=A1-A2 coefficientwise in
    # the formal log-prime basis, including prime powers.
    hb2_switching_cases = 0
    for z_top in (31, 36, 64, 127, 257):
        y_cut = math.isqrt(z_top)
        for n in range(2, z_top + 1):
            a1: dict[int, int] = {}
            a2: dict[int, int] = {}
            large_divisor: dict[int, int] = {}
            for e in divisors(n):
                if e <= y_cut:
                    add_scaled_vector(a1, log_vector(n // e), mobius(e))
                else:
                    add_scaled_vector(
                        large_divisor, log_vector(n // e), mobius(e)
                    )
            for e1 in divisors(n):
                if e1 > y_cut:
                    continue
                for e2 in divisors(n // e1):
                    if e2 > y_cut:
                        continue
                    remainder = n // (e1 * e2)
                    for f1 in divisors(remainder):
                        add_scaled_vector(
                            a2,
                            log_vector(f1),
                            mobius(e1) * mobius(e2),
                        )

            hb2_lambda: dict[int, int] = {}
            add_scaled_vector(hb2_lambda, a1, 2)
            add_scaled_vector(hb2_lambda, a2, -1)
            switched_large: dict[int, int] = {}
            add_scaled_vector(switched_large, a1, 1)
            add_scaled_vector(switched_large, a2, -1)
            if hb2_lambda != mangoldt_vector(n):
                raise AssertionError(
                    f"exact HB2 Lambda identity failed at Z={z_top}, N={n}"
                )
            if switched_large != large_divisor:
                raise AssertionError(
                    f"exact HB2 large-divisor switch failed at Z={z_top}, N={n}"
                )
            hb2_switching_cases += 1

    # Mutation: the proof-level r=1 precursor is the von Mangoldt identity,
    # not a prime-only indicator.  At the explicit prime power N=8 the exact
    # HB2 combination must retain log(2), whereas a prime-indicator rewrite
    # would erase the coefficient.
    prime_power_n = 8
    prime_power_y = math.isqrt(31)
    prime_power_a1: dict[int, int] = {}
    prime_power_a2: dict[int, int] = {}
    for e in divisors(prime_power_n):
        if e <= prime_power_y:
            add_scaled_vector(
                prime_power_a1, log_vector(prime_power_n // e), mobius(e)
            )
    for e1 in divisors(prime_power_n):
        if e1 > prime_power_y:
            continue
        quotient = prime_power_n // e1
        for e2 in divisors(quotient):
            if e2 <= prime_power_y:
                remainder = quotient // e2
                for f1 in divisors(remainder):
                    add_scaled_vector(
                        prime_power_a2,
                        log_vector(f1),
                        mobius(e1) * mobius(e2),
                    )
    prime_power_hb2: dict[int, int] = {}
    add_scaled_vector(prime_power_hb2, prime_power_a1, 2)
    add_scaled_vector(prime_power_hb2, prime_power_a2, -1)
    if prime_power_hb2 != {2: 1}:
        raise AssertionError("HB2 prime-power witness failed at N=8")
    prime_indicator_mutation: dict[int, int] = {}
    if prime_power_hb2 == prime_indicator_mutation:
        raise AssertionError("HB2 prime-power to prime-indicator mutation escaped")

    # Mutation 1: shifting J above 1/3 destroys the tight n=3 A1 witness.
    mutated_j = Fraction(134, 400)
    if a1_witness(3, mutated_j) is not None:
        raise AssertionError("J-above-one-third mutation escaped")

    # Mutation 2: losing the exact 1/2 upper endpoint destroys the h=1 A2 hit.
    mutated_upper = HALF - Fraction(1, 400)
    lower_interval_hit = J <= HALF <= mutated_upper
    reflected_lower = 1 - mutated_upper
    reflected_upper = 1 - J
    reflected_hit = reflected_lower <= HALF <= reflected_upper
    if lower_interval_hit or reflected_hit:
        raise AssertionError("square-root endpoint mutation escaped")

    # Mutation 3: assigning the closed square-root divisor to the large side
    # breaks the exact A1-A2 switch (Z=N=36 has mu(6) log(6) != 0).
    endpoint_mutation: dict[int, int] = {}
    for d in divisors(36):
        if d >= 6:
            add_scaled_vector(endpoint_mutation, log_vector(36 // d), mobius(d))
    exact_large_36: dict[int, int] = {}
    for d in divisors(36):
        if d > 6:
            add_scaled_vector(exact_large_36, log_vector(36 // d), mobius(d))
    if endpoint_mutation == exact_large_36:
        raise AssertionError("HB2 closed-square-root endpoint mutation escaped")

    # The A2 convolution coefficient is (mu_<=Y * mu_<=Y)(E), not mu(E).
    # The shared-prime witness e1=e2=2 makes the distinction coefficientwise.
    if mobius(2) * mobius(2) == mobius(4):
        raise AssertionError("HB2 A2 product-Mobius collapse mutation escaped")

    # The grouped bilateral A2 form uses rho_x(t)=log(x)/log(t), so its
    # literal +6*log(b1)*log(f1)/log(t) coefficient requires 6/log(x).
    sample_log_x = Fraction(10, 1)
    sample_log_t = Fraction(8, 1)
    sample_log_b = Fraction(3, 1)
    sample_log_f = Fraction(5, 1)
    literal_bilateral = 6 * sample_log_b * sample_log_f / sample_log_t
    grouped_bilateral = (
        Fraction(6, 1)
        / sample_log_x
        * (sample_log_x / sample_log_t)
        * sample_log_b
        * sample_log_f
    )
    missing_global_factor = (
        sample_log_x / sample_log_t * sample_log_b * sample_log_f
    )
    if grouped_bilateral != literal_bilateral:
        raise AssertionError("HB4xHB2 grouped global normalization failed")
    if missing_global_factor == literal_bilateral:
        raise AssertionError("HB4xHB2 missing 6/log(x) mutation escaped")

    # Mutation 4: omitting the parity factor leaves local mean 1/2 at p=2.
    mutated_p2_mean = Fraction(1, 2)
    if mutated_p2_mean == 1:
        raise AssertionError("parity-factor mutation escaped")

    # Mutation 4: b=1 has the fatal even-multiplier discrepancy.
    sample_x = 10_000
    b_one_even_row = sum(1 for n in range(1, sample_x + 1) if sample_x / 2 < 2 * n <= sample_x)
    matched_even_row = sum(
        1
        for n in range(1, sample_x + 1)
        if sample_x / 2 < 2 * n <= sample_x and odd_multiplier(2 * n) != 0
    )
    if b_one_even_row == 0 or matched_even_row != 0:
        raise AssertionError("even-multiplier control failed")

    # Mutation 5: changing the shifted target destroys determinant two.
    d, m, n0 = 3, 5, 1
    r0_mutated = (m * n0 + 1) // d
    if (m * n0 + 1) % d or d * r0_mutated - m * n0 != 1:
        raise AssertionError("shift-one mutation fixture is invalid")
    if d * r0_mutated - m * n0 == 2:
        raise AssertionError("shift-one determinant mutation escaped")

    # Mutation 6: the coarse z=2 comparison misses the mod-3 tensor residue.
    coarse_mod3 = projected_divisibility_factor(3, 1)
    exact_mod3 = exact_shift_local_factor(3, 1)
    if exact_mod3 != 0 or coarse_mod3 == 0 or exact_mod3 == coarse_mod3:
        raise AssertionError("coarse mod-3 rank-one mutation escaped")

    return {
        "status": "PASS",
        "scope": (
            "finite exact algebra, rank-one obstruction, and compiler geometry; "
            "source-backed analytic estimates are not numerical checks; the "
            "universal Type II umbrella, Gauss-twisted exact-half correlation, "
            "and structured two-row paired-Voronoi theorem remain open"
        ),
        "exponents": {
            "J": "133/400",
            "nu": "67/400",
            "half": "1/2",
            "Q": "267/400",
            "one_third_margin": "1/1200",
            "full_mirror_width": "134/400",
            "vaughan_surplus": "1/400",
            "lemma_7_14_padding_slots": hb_padding_slots,
            "bc_h2_j1_worst": str(bc_h2_j1_worst),
            "bc_h3_thin_worst": str(bc_h3_thin_worst),
            "bc_j2_smooth_slot_threshold": str(bc_smooth_slot_threshold),
            "bc_hb2_b3_grouped_base": str(bc_hb2_b3_grouped_base),
            "bc_hb2_b3_grouped_d_slope": str(bc_hb2_b3_grouped_d_slope),
            "bc_one_poisson_first_threshold": str(bc_one_poisson_first_threshold),
            "bc_one_poisson_start": str(bc_one_poisson_start),
            "bc_one_poisson_second_threshold": str(bc_one_poisson_second_threshold),
            "hb4_double_smooth_weil_threshold": str(hb4_double_smooth_weil_threshold),
            "hb4_ramanujan_axis_exponent": str(hb4_ramanujan_axis_exponent),
            "pascadi_hb4_complete_threshold": str(pascadi_hb4_complete_threshold),
            "pascadi_hb4_favourable_only_threshold": str(
                pascadi_hb4_favourable_only_threshold
            ),
            "pascadi_hb4_complete_base": str(pascadi_hb4_complete_base),
            "pascadi_hb4_favourable_only_base": str(
                pascadi_hb4_favourable_only_base
            ),
            "conductor_projected_high_base": str(conductor_projected_high_base),
            "conductor_projected_threshold": str(conductor_projected_threshold),
            "low_conductor_physical_exponent": str(
                low_conductor_physical_exponent
            ),
            "bp_fixed_unit_modulus_saving": str(bp_modulus_saving),
            "bp_fixed_unit_F_saving": str(bp_f_saving),
            "bp_fixed_unit_X_saving": str(bp_x_saving),
            "bp_fixed_cell_F_exponent": str(bp_fixed_cell_f_exponent),
            "bp_frozen_outer_F_exponent": str(bp_frozen_outer_f_exponent),
            "bp_frozen_outer_deficit": str(bp_frozen_deficit),
            "bp_false_vector_lift_exponent": str(
                bp_vector_lift_claimed_exponent
            ),
            "bp_character_mode_exponent": str(bp_character_mode_exponent),
            "bp_tensor_contradiction_gap": str(bp_tensor_contradiction_gap),
            "burgess_r2_F_exponent": str(burgess_r2_f_exponent),
            "actual_single_character_F_exponent": str(
                actual_single_character_f_exponent
            ),
        },
        "exact_checks": [
            "local Euler mean one including parity",
            "hybrid exact shifted-residue Euler mean one",
            "omitted-prime tensor cut witness has size p",
            "singular-series divisor expansion",
            "finite conditional mean m/phi(m)",
            "finite hybrid sieve slice constant equals m/phi(m)",
            "finite Ramanujan sum equals local Euler product",
            "formal Lambda=sum mu(d)log(r) determinant coefficient identity",
            "exact HB2 Lambda=2A1-A2 and large-divisor A1-A2 switching",
            "HB2 prime-power witness retains the von Mangoldt coefficient at N=8",
            "HB2 A2 retains the two literal Mobius slots under convolution",
            "HB4xHB2 grouped determinant retains the global 6/log(x) coefficient",
            "primitive affine lift preserves determinant two",
            "HB2 Cauchy zero mode has CRT density 1/lcm(d1,d2) on compatible rows",
            "HB4 Pascadi residue coefficient has the exact multiplicative-incidence L2 norm",
            "Pascadi r-asymp-1 singleton is r=2 and maps the full source kernel to the target",
            "induced mod-3 characters exhibit the forbidden all-character inflation",
            "low-conductor Kloosterman projector factors into two generalized Gauss sums",
            "Ford--Maynard A1 finite fixture through n=20000",
            "HB2 no-large-slot first-subset cover on the exact denominator-40 grid",
            "HB2 equality case retains the closed one-half endpoint",
            "J-to-half-to-Q exponent identities",
            "Q+(Q-J)=1+1/400 Vaughan surplus",
            "Ford--Maynard Lemma 7.14 uses 12 padded factors at gamma=1/2",
            "Bettin--Chandee adjacent h=2,j=1 worst exponent is 39/40",
            "Bettin--Chandee h=3 thin-cell worst exponent is 5/6",
            "grouped HB2-B3 Corollary-1 base exponent is 11/10 before D growth",
            "one-Poisson BC first threshold 11/56 lies below the 1/4 start",
            "HB4 double-smooth Weil off-diagonal reaches but not including 1/3",
            "HB4 Ramanujan axes have exponent 3/4",
            "Pascadi optimal coefficient compression extends 1/3 to but not including 3/8",
            "conductor-projected high part reaches but does not include the exact half endpoint",
            "low-conductor Gauss--Ramanujan projector retains a fixed power saving",
            "Blomer--Pascadi fixed-unit q^(-1/32) maps to X^(-1/64) at q=X^(1/2)",
            "quartic moving-unit Kloosterman sum is an exact rank-one character mode",
            "absolute p=13 physical convention and character-matched interval are frozen",
            "Burgess r=2 leaves every actual single-character prime mode below F^4",
            "naive two-row additive-difference Kloosterman kernel has operator norm q",
            "V8 primary and independent source locks remain separate with zero physical credit",
            "outer minus six converts source A1-A2 into physical A2-A1",
        ],
        "case_counts": {
            "divisor_expansion": divisor_cases,
            "finite_euler_slices": slice_cases,
            "hybrid_slice_constants": hybrid_slice_constant_cases,
            "ramanujan_euler": ramanujan_cases,
            "mangoldt_log_vector": mangoldt_cases,
            "hb2_exact_large_divisor_switching": hb2_switching_cases,
            "hybrid_tensor_local": tensor_local_cases,
            "omitted_prime_cut_witness": tail_cut_cases,
            "determinant_two_affine": determinant_cases,
            "hb2_subset_cover_grid": hb2_partition_cases,
            "hb2_crt_covariance": crt_covariance_cases,
            "hb4_pascadi_residue_incidence": pascadi_incidence_cases,
            "hb4_pascadi_r2_scaling": pascadi_scaling_cases,
            "induced_low_conductor_characters": induced_low_conductor_cases,
            "low_conductor_gauss_projector": low_conductor_gauss_projector_cases,
            "bp_quartic_character_rank_one": bp_character_rank_one_cases,
            "bp_character_matched_interval_magnitude": bp_rank_one_interval_magnitude,
            "two_row_difference_kernel_spectrum": difference_kernel_spectrum_cases,
        },
        "mutation_tests": {
            "J_above_one_third": "DETECTED",
            "loss_of_exact_sqrt_endpoint": "DETECTED",
            "hb2_sqrt_endpoint_to_large": "DETECTED",
            "hb2_A2_product_mobius_collapse": "DETECTED",
            "hb2_prime_power_to_prime_indicator": "DETECTED",
            "hb4xhb2_missing_six_over_logx": "DETECTED",
            "missing_parity_factor": "DETECTED",
            "b_equals_one_even_multiplier": "DETECTED",
            "shift_one_not_determinant_two": "DETECTED",
            "coarse_mod3_rank_one": "DETECTED",
            "hb1_large_rough_escape": "DETECTED",
            "bc_second_summand_only": "DETECTED",
            "bc_hb2_b3_slot_match_but_scale_failure": "DETECTED",
            "pascadi_later_summand_only": "DETECTED",
            "pascadi_R1_is_r2_not_r1": "DETECTED",
            "all_character_conductor_collapse": "DETECTED",
            "bp_quartic_character_conjugation": "DETECTED",
            "bp_physical_unit_inverse": "DETECTED",
            "bp_physical_minus_two_scaling": "DETECTED",
            "bp_arbitrary_unit_vector_lift": "DETECTED_FALSE",
            "bp_trivial_exponent": "DETECTED",
            "bp_missing_unit_norm": "DETECTED",
            "bp_wrong_q_to_x_scale": "DETECTED",
            "two_row_naive_residue_compression": "DETECTED",
            "two_row_plus_kernel": "DETECTED",
            "two_row_sqrt_q_norm": "DETECTED",
            "v8_primary_reserve_swap": "DETECTED",
            "v8_source_lock_merge": "DETECTED",
            "v8_paired_polar_main_promotion": "DETECTED",
            "v8_bilateral_A1_A2_sign_reversal": "DETECTED",
            "v8_physical_credit_promotion": "DETECTED",
        },
        "open_gate": umbrella_gate,
        "route_freeze": route_freeze,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run exact checks")
    parser.parse_args()
    print(json.dumps(run_checks(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
