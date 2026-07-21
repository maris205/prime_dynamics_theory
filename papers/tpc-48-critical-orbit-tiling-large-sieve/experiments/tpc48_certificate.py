#!/usr/bin/env python3
"""Deterministic exact certificate for TPC-48.

The certificate checks a finite model of the orbit-tiling and
large-sieve mechanisms used in the paper.

* Over F_601 on Z/60Z, four translated residue-comb cells form an
  exact Fourier partition.  Their full ranks and their compressed
  physical-window traces are checked exactly.
* Nine determinant rows are routed through an exhaustive resonance
  tile/channel map.  The unlabelled synthesis has norm squared K=9;
  retaining the tile channel lowers the exact collision norm squared
  to R=4.  All tube first and second moments are enumerated.
* Over the rational numbers, a common translated profile has an exact
  Gram identity and an exact Gershgorin large-sieve bound.
* Rational Hadamard and channel-collapse witnesses record why output
  Parseval alone gives no atomic gain and why erasing the channel can
  restore the full K loss.

This finite cyclic calculation is an analogue and regression
certificate.  It is not a proof of the continuous or asymptotic
theorems in the paper.  No floating-point arithmetic or randomness is
used.
"""

from __future__ import annotations

import ast
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from math import gcd
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def prime_divisors(n: int) -> tuple[int, ...]:
    answer = []
    work = n
    divisor = 2
    while divisor * divisor <= work:
        if work % divisor == 0:
            answer.append(divisor)
            while work % divisor == 0:
                work //= divisor
        divisor += 1
    if work > 1:
        answer.append(work)
    return tuple(answer)


def primitive_root(prime: int) -> int:
    require(is_prime(prime), "primitive-root modulus is prime")
    factors = prime_divisors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise RuntimeError("primitive root not found")


def matrix_product_mod(
    left: list[list[int]], right: list[list[int]], modulus: int
) -> list[list[int]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    transposed = [
        [right[r][c] for r in range(middle)]
        for c in range(columns)
    ]
    return [
        [
            sum(x * y for x, y in zip(left[r], transposed[c]))
            % modulus
            for c in range(columns)
        ]
        for r in range(rows)
    ]


def matrix_rank_mod(matrix: list[list[int]], modulus: int) -> int:
    if not matrix:
        return 0
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (r for r in range(rank, rows) if work[r][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, modulus)
        work[rank] = [
            inverse * entry % modulus for entry in work[rank]
        ]
        for r in range(rows):
            if r == rank or not work[r][column]:
                continue
            factor = work[r][column]
            work[r] = [
                (work[r][c] - factor * work[rank][c]) % modulus
                for c in range(columns)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def fourier_projection_matrix(
    n: int, band: set[int], omega: int, modulus: int
) -> list[list[int]]:
    inverse_n = pow(n, -1, modulus)
    return [
        [
            inverse_n
            * sum(
                pow(omega, ((j - k) * frequency) % n, modulus)
                for frequency in band
            )
            % modulus
            for k in range(n)
        ]
        for j in range(n)
    ]


def check_critical_orbit_partition() -> dict:
    """Verify the exact all-band partition and trace ledger."""
    start = CHECKS
    n = 60
    h0 = 3
    ell_count = 4
    physical_length = ell_count
    modulus = 601

    require(n % (h0 * ell_count) == 0,
            "orbit size is divisible by H0 times L")
    cell_width = n // (h0 * ell_count)
    branch_period = n // h0
    require(cell_width == 5, "finite cell width")
    require(branch_period == ell_count * cell_width,
            "each progression branch is tiled")

    bands = []
    for ell in range(ell_count):
        band = {
            (branch * branch_period + ell * cell_width + local) % n
            for branch in range(h0)
            for local in range(cell_width)
        }
        bands.append(band)
        require(len(band) == h0 * cell_width,
                "each residue-comb cell has equal size")

    for ell in range(ell_count):
        translated = {
            (frequency + ell * cell_width) % n
            for frequency in bands[0]
        }
        require(translated == bands[ell],
                "cells are exact translates of the base comb cell")
    for left in range(ell_count):
        for right in range(ell_count):
            if left != right:
                require(not bands[left].intersection(bands[right]),
                        "distinct orbit cells are disjoint")
    require(set().union(*bands) == set(range(n)),
            "all orbit cells cover every Fourier frequency")

    generator = primitive_root(modulus)
    omega = pow(generator, (modulus - 1) // n, modulus)
    require(pow(omega, n, modulus) == 1,
            "finite Fourier root closes")
    for exponent in range(1, n):
        require(pow(omega, exponent, modulus) != 1,
                "finite Fourier root has exact order")

    projectors = [
        fourier_projection_matrix(n, band, omega, modulus)
        for band in bands
    ]
    expected_diagonal = (
        len(bands[0]) * pow(n, -1, modulus)
    ) % modulus
    ranks = []
    full_traces = []
    compressed_traces = []
    for ell, projector in enumerate(projectors):
        for j in range(n):
            require(projector[j][j] == expected_diagonal,
                    "Fourier multiplier has constant diagonal")
        rank = matrix_rank_mod(projector, modulus)
        trace = sum(projector[j][j] for j in range(n)) % modulus
        compressed = sum(
            projector[j][j] for j in range(physical_length)
        ) % modulus
        ranks.append(rank)
        full_traces.append(trace)
        compressed_traces.append(compressed)
        require(rank == len(bands[ell]),
                "projector rank equals its Fourier cell size")
        require(trace == len(bands[ell]),
                "full projector trace equals rank")
        require(compressed == 1,
                "critical physical-window trace equals one")

    zero = [[0 for _ in range(n)] for _ in range(n)]
    for left in range(ell_count):
        for right in range(ell_count):
            product = matrix_product_mod(
                projectors[left], projectors[right], modulus
            )
            expected = projectors[left] if left == right else zero
            for j in range(n):
                for k in range(n):
                    require(product[j][k] == expected[j][k],
                            "orbit projectors are orthogonal idempotents")

    for j in range(n):
        for k in range(n):
            total = sum(
                projectors[ell][j][k] for ell in range(ell_count)
            ) % modulus
            require(total == int(j == k),
                    "all orbit projectors sum to the identity")

    rational_trace = Fraction(
        physical_length * len(bands[0]), n
    )
    require(rational_trace == 1,
            "rational critical trace is exactly one")
    require(ell_count * rational_trace == physical_length,
            "compressed traces sum to physical dimension")

    return {
        "checks": CHECKS - start,
        "arithmetic": "F_601 on Z/60Z plus rational trace",
        "N": n,
        "H0": h0,
        "L": ell_count,
        "J": physical_length,
        "N_divisible_by_H0_times_L": True,
        "cell_width": cell_width,
        "band_sizes": [len(band) for band in bands],
        "projector_ranks": ranks,
        "full_projector_traces": full_traces,
        "compressed_trace_per_band": fraction_text(rational_trace),
        "compressed_trace_sum": fraction_text(
            ell_count * rational_trace
        ),
    }


def tile_index(q: int, n: int, h0: int, ell_count: int) -> int:
    branch_period = n // h0
    cell_width = branch_period // ell_count
    return (q % branch_period) // cell_width


def check_resonance_channels_and_moments() -> dict:
    """Exhaust the resonance map, its norms, and tube moments."""
    start = CHECKS
    n = 60
    h0 = 3
    ell_count = 4
    slopes = (1, 7, 11, 13, 17, 19, 23, 29, 31)
    intercepts = tuple(2 * row for row in range(len(slopes)))
    source_count = len(slopes)

    for slope in slopes:
        require(gcd(slope, n) == 1,
                "each finite determinant slope is invertible")
    require(len(set(slopes)) == source_count,
            "finite source slopes are distinct")

    atoms = []
    unlabelled_preimages = defaultdict(list)
    tube_preimages = defaultdict(list)
    atom_to_tube = {}
    atom_to_channel = {}
    for row, (slope, intercept) in enumerate(
        zip(slopes, intercepts)
    ):
        inverse = pow(slope, -1, n)
        row_channels = set()
        for q in range(n):
            ell = tile_index(q, n, h0, ell_count)
            channel = ((intercept - q) * inverse) % n
            atom = (row, q)
            tube = (ell, channel)
            atoms.append(atom)
            atom_to_tube[atom] = tube
            atom_to_channel[atom] = channel
            unlabelled_preimages[channel].append(atom)
            tube_preimages[tube].append(atom)
            row_channels.add(channel)
            require((q + slope * channel - intercept) % n == 0,
                    "resonance congruence")
            recovered_q = (intercept - slope * channel) % n
            require(recovered_q == q,
                    "resonance channel map has exact inverse")
        require(row_channels == set(range(n)),
                "each determinant row is a channel permutation")

    require(len(atoms) == source_count * n,
            "all row-frequency atoms are present")
    for channel in range(n):
        require(len(unlabelled_preimages[channel]) == source_count,
                "every unlabelled output row has multiplicity K")
    for left in range(n):
        left_set = set(unlabelled_preimages[left])
        for right in range(n):
            gram_entry = len(
                left_set.intersection(unlabelled_preimages[right])
            )
            expected = source_count if left == right else 0
            require(gram_entry == expected,
                    "unlabelled synthesis has TT-star equal K identity")

    unrestricted_witness = unlabelled_preimages[0]
    unrestricted_domain_energy = len(unrestricted_witness)
    unrestricted_output_energy = len(unrestricted_witness) ** 2
    require(
        unrestricted_output_energy
        == source_count * unrestricted_domain_energy,
        "coherent unlabelled witness attains norm squared K",
    )

    all_tubes = [
        (ell, channel)
        for ell in range(ell_count)
        for channel in range(n)
    ]
    loads = {
        tube: len(tube_preimages.get(tube, [])) for tube in all_tubes
    }
    collision_norm = max(loads.values())
    require(collision_norm == 4,
            "exact channel collision norm squared is R=4")
    distribution = Counter(loads.values())
    require(
        distribution == Counter({0: 30, 1: 6, 2: 102, 3: 78, 4: 24}),
        "exact tube-load distribution",
    )

    seen_atoms = set()
    for tube in all_tubes:
        preimage = set(tube_preimages.get(tube, []))
        require(not seen_atoms.intersection(preimage),
                "different tube rows have disjoint domain support")
        seen_atoms.update(preimage)
    require(seen_atoms == set(atoms),
            "tube rows partition every domain atom")
    for atom in atoms:
        require(atom_to_tube[atom][1] == atom_to_channel[atom],
                "erasing the tile label gives the unlabelled channel")

    maximal_tube = next(
        tube for tube in all_tubes if loads[tube] == collision_norm
    )
    resolved_witness = tube_preimages[maximal_tube]
    resolved_domain_energy = len(resolved_witness)
    resolved_output_energy = len(resolved_witness) ** 2
    require(
        resolved_output_energy
        == collision_norm * resolved_domain_energy,
        "maximal tube witness attains collision norm squared R",
    )

    first_moment = sum(loads.values())
    second_moment = sum(load * load for load in loads.values())
    require(first_moment == source_count * n,
            "tube first moment counts all atoms")
    require(second_moment == 1500,
            "exact tube second moment")

    per_tile_first = []
    per_tile_second = []
    for ell in range(ell_count):
        tile_loads = [loads[(ell, channel)] for channel in range(n)]
        first = sum(tile_loads)
        second = sum(load * load for load in tile_loads)
        per_tile_first.append(first)
        per_tile_second.append(second)
        require(first == source_count * n // ell_count,
                "each tile has the same first moment")
    require(per_tile_second == [405, 345, 405, 345],
            "per-tile second moments")

    exhaustive_ordered_collisions = 0
    for left_atom in atoms:
        left_tube = atom_to_tube[left_atom]
        for right_atom in atoms:
            if left_tube == atom_to_tube[right_atom]:
                exhaustive_ordered_collisions += 1
    require(exhaustive_ordered_collisions == second_moment,
            "exhaustive ordered-pair count equals second moment")

    return {
        "checks": CHECKS - start,
        "arithmetic": "integer exhaustive enumeration on Z/60Z",
        "K_source_slopes": source_count,
        "slopes": list(slopes),
        "intercepts": list(intercepts),
        "resonance_equation": "q + m*k = a (mod N)",
        "unlabelled_synthesis_norm_squared_K": source_count,
        "resolved_channel_collision_norm_squared_R": collision_norm,
        "erasing_tile_channel_restores_norm_squared_K": source_count,
        "tube_count": len(all_tubes),
        "populated_tube_count": sum(
            int(load > 0) for load in loads.values()
        ),
        "load_distribution": {
            str(load): distribution[load]
            for load in sorted(distribution)
        },
        "first_moment": first_moment,
        "second_moment": second_moment,
        "exhaustive_ordered_collision_count":
            exhaustive_ordered_collisions,
        "per_tile_first_moments": per_tile_first,
        "per_tile_second_moments": per_tile_second,
    }


def translate_cyclic(
    profile: list[Fraction], center: int
) -> list[Fraction]:
    n = len(profile)
    return [profile[(j - center) % n] for j in range(n)]


def dot_rational(
    left: list[Fraction], right: list[Fraction]
) -> Fraction:
    return sum(
        (x * y for x, y in zip(left, right)), Fraction(0)
    )


def rational_ldlt(
    matrix: list[list[Fraction]],
) -> tuple[list[list[Fraction]], list[Fraction]]:
    """Return an exact positive-pivot LDL^T decomposition."""
    n = len(matrix)
    lower = [
        [Fraction(0) for _ in range(n)] for _ in range(n)
    ]
    pivots = []
    for i in range(n):
        lower[i][i] = Fraction(1)
        pivot = matrix[i][i] - sum(
            (
                lower[i][k] * lower[i][k] * pivots[k]
                for k in range(i)
            ),
            Fraction(0),
        )
        require(pivot > 0, "large-sieve defect has positive LDL pivot")
        pivots.append(pivot)
        for j in range(i + 1, n):
            numerator = matrix[j][i] - sum(
                (
                    lower[j][k] * lower[i][k] * pivots[k]
                    for k in range(i)
                ),
                Fraction(0),
            )
            lower[j][i] = Fraction(numerator, pivot)
    return lower, pivots


def check_common_profile_large_sieve() -> dict:
    """Check a rational common-profile Gram/large-sieve analogue."""
    start = CHECKS
    n = 20
    common_profile = [
        Fraction(1),
        Fraction(-1, 2),
        Fraction(2, 3),
        Fraction(1, 4),
        Fraction(-1, 5),
    ] + [Fraction(0) for _ in range(15)]
    centers = (0, 3, 6, 10, 13, 16)
    vectors = [
        translate_cyclic(common_profile, center) for center in centers
    ]
    gram = [
        [dot_rational(left, right) for right in vectors]
        for left in vectors
    ]
    profile_energy = dot_rational(common_profile, common_profile)
    require(profile_energy == Fraction(6469, 3600),
            "exact common-profile energy")
    for row in range(len(centers)):
        require(gram[row][row] == profile_energy,
                "Gram diagonal is common-profile energy")
        for column in range(len(centers)):
            require(gram[row][column] == gram[column][row],
                    "common-profile Gram matrix is symmetric")

    row_absolute_sums = [
        sum((abs(entry) for entry in row), Fraction(0))
        for row in gram
    ]
    large_sieve_constant = max(row_absolute_sums)
    off_diagonal_budget = max(
        row_absolute_sums[row] - profile_energy
        for row in range(len(centers))
    )
    require(large_sieve_constant == Fraction(8989, 3600),
            "exact rational Gram row-sum constant")
    require(off_diagonal_budget == Fraction(7, 10),
            "exact rational collision budget")
    require(
        large_sieve_constant
        < len(centers) * profile_energy,
        "common profile improves the arbitrary coherent K bound",
    )

    defect = [
        [
            large_sieve_constant * int(row == column)
            - gram[row][column]
            for column in range(len(centers))
        ]
        for row in range(len(centers))
    ]
    lower, pivots = rational_ldlt(defect)
    for row in range(len(centers)):
        for column in range(len(centers)):
            reconstructed = sum(
                (
                    lower[row][k] * pivots[k] * lower[column][k]
                    for k in range(len(centers))
                ),
                Fraction(0),
            )
            require(reconstructed == defect[row][column],
                    "exact LDL reconstruction of large-sieve defect")

    coefficient_cases = 0
    for integer_coefficients in itertools.product(
        (-1, 0, 1), repeat=len(centers)
    ):
        if not any(integer_coefficients):
            continue
        coefficients = [
            Fraction(coefficient) for coefficient in integer_coefficients
        ]
        synthesis = [
            sum(
                (
                    coefficients[row] * vectors[row][j]
                    for row in range(len(centers))
                ),
                Fraction(0),
            )
            for j in range(n)
        ]
        synthesis_energy = dot_rational(synthesis, synthesis)
        gram_energy = sum(
            (
                coefficients[row]
                * gram[row][column]
                * coefficients[column]
                for row in range(len(centers))
                for column in range(len(centers))
            ),
            Fraction(0),
        )
        coefficient_energy = sum(
            (coefficient * coefficient for coefficient in coefficients),
            Fraction(0),
        )
        require(synthesis_energy == gram_energy,
                "exact common-profile Gram identity")
        require(
            gram_energy <= large_sieve_constant * coefficient_energy,
            "exact rational large-sieve row-sum bound",
        )
        coefficient_cases += 1
    require(coefficient_cases == 728,
            "all ternary nonzero coefficient vectors are checked")

    return {
        "checks": CHECKS - start,
        "arithmetic": "fractions.Fraction only",
        "cyclic_profile_length": n,
        "common_profile_support_length": 5,
        "translation_centers": list(centers),
        "profile_energy": fraction_text(profile_energy),
        "gram_matrix": [
            [fraction_text(entry) for entry in row] for row in gram
        ],
        "large_sieve_row_sum_constant":
            fraction_text(large_sieve_constant),
        "off_diagonal_collision_budget":
            fraction_text(off_diagonal_budget),
        "large_sieve_defect_LDL_pivots": [
            fraction_text(pivot) for pivot in pivots
        ],
        "enumerated_nonzero_coefficient_vectors": coefficient_cases,
        "boundary": (
            "This is a finite rational common-profile Gram analogue, "
            "not the continuous determinant large-sieve theorem."
        ),
    }


def hadamard_transform(values: list[Fraction]) -> list[Fraction]:
    signs = (
        (1, 1, 1, 1),
        (1, -1, 1, -1),
        (1, 1, -1, -1),
        (1, -1, -1, 1),
    )
    return [
        Fraction(
            sum(sign * value for sign, value in zip(row, values)), 2
        )
        for row in signs
    ]


def rational_energy(values: list[Fraction]) -> Fraction:
    return sum((value * value for value in values), Fraction(0))


def check_failure_witnesses() -> dict:
    """Certify the Parseval and channel-erasure failure modes."""
    start = CHECKS

    flat_input = [Fraction(1, 2) for _ in range(4)]
    concentrated_output = hadamard_transform(flat_input)
    delta_input = [
        Fraction(1), Fraction(0), Fraction(0), Fraction(0)
    ]
    flat_output = hadamard_transform(delta_input)
    require(rational_energy(flat_input) == 1,
            "flat Hadamard input has unit energy")
    require(rational_energy(concentrated_output) == 1,
            "Hadamard Parseval for concentrated output")
    require(concentrated_output == [
        Fraction(1), Fraction(0), Fraction(0), Fraction(0)
    ], "unit energy may occupy one output atom")
    require(rational_energy(delta_input) == 1,
            "delta Hadamard input has unit energy")
    require(rational_energy(flat_output) == 1,
            "Hadamard Parseval for flat output")
    require(flat_output == [Fraction(1, 2) for _ in range(4)],
            "the same total energy may be uniformly spread")
    require(
        max(value * value for value in concentrated_output) == 1,
        "Parseval alone permits atomic mass equal to total mass",
    )
    require(
        max(value * value for value in flat_output) == Fraction(1, 4),
        "Parseval alone does not select the flat alternative",
    )

    source_count = 9
    resolved_collision = 4
    collapsed_input = [Fraction(1) for _ in range(source_count)]
    collapsed_domain_energy = rational_energy(collapsed_input)
    collapsed_output = sum(collapsed_input, Fraction(0))
    collapsed_output_energy = collapsed_output * collapsed_output
    require(collapsed_domain_energy == source_count,
            "collapsed witness domain energy")
    require(
        collapsed_output_energy
        == source_count * collapsed_domain_energy,
        "erasing all channel labels restores norm squared K",
    )

    resolved_input = [Fraction(1) for _ in range(resolved_collision)]
    resolved_domain_energy = rational_energy(resolved_input)
    resolved_output = sum(resolved_input, Fraction(0))
    require(
        resolved_output * resolved_output
        == resolved_collision * resolved_domain_energy,
        "resolved collision witness has norm squared R",
    )
    require(resolved_collision < source_count,
            "channel resolution can reduce but not remove collisions")

    return {
        "checks": CHECKS - start,
        "witnesses": {
            "output_parseval_no_atomic_gain": {
                "total_energy": "1",
                "concentrated_max_atom": "1",
                "flat_max_atom": "1/4",
            },
            "channel_collapse_restores_K": {
                "resolved_norm_squared_R": resolved_collision,
                "collapsed_norm_squared_K": source_count,
            },
        },
    }


def check_exponent_ledger() -> dict:
    """Verify the critical TPC-48 exponent arithmetic exactly."""
    start = CHECKS
    mu = Fraction(267, 400)
    nu = Fraction(133, 400)
    kappa = Fraction(1, 400)
    band_count_exponent = nu
    physical_length_exponent = nu
    per_band_trace_exponent = (
        physical_length_exponent - band_count_exponent
    )
    tube_half_width_exponent = -(mu + nu)
    critical_collision_load = mu - nu
    allowance_gap = critical_collision_load - kappa

    require(mu + nu == 1, "M times J has exponent one")
    require(band_count_exponent == physical_length_exponent,
            "critical tiling has L comparable to J")
    require(per_band_trace_exponent == 0,
            "critical per-band trace exponent is zero")
    require(tube_half_width_exponent == -1,
            "critical tube half-width exponent is minus one")
    require(critical_collision_load == Fraction(67, 200),
            "critical collision load is 67/200")
    require(allowance_gap == Fraction(133, 400),
            "gap from critical load to TPC allowance is 133/400")
    require(allowance_gap == nu,
            "remaining allowance gap equals the orbit exponent nu")
    require(mu == 2 * nu + kappa,
            "endpoint identity mu equals two nu plus kappa")

    return {
        "checks": CHECKS - start,
        "mu_slope_exponent": fraction_text(mu),
        "nu_orbit_length_exponent": fraction_text(nu),
        "kappa_TPC_allowance_exponent": fraction_text(kappa),
        "L_band_count_exponent": fraction_text(band_count_exponent),
        "per_band_trace_exponent":
            fraction_text(per_band_trace_exponent),
        "tube_half_width_exponent":
            fraction_text(tube_half_width_exponent),
        "critical_collision_load":
            fraction_text(critical_collision_load),
        "allowance_gap": fraction_text(allowance_gap),
        "identity": (
            "critical_collision_load=mu-nu=67/200; "
            "allowance_gap=(mu-nu)-kappa=nu=133/400"
        ),
    }


def check_source_constraints() -> dict:
    start = CHECKS
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    float_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    assert_nodes = [
        node for node in ast.walk(tree) if isinstance(node, ast.Assert)
    ]
    true_divisions = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    allowed_roots = {
        "__future__", "ast", "collections", "fractions", "hashlib",
        "itertools", "json", "math", "pathlib",
    }
    require(not float_nodes, "certificate source has no float literal")
    require(not assert_nodes, "certificate source has no assert statement")
    require(not true_divisions,
            "certificate source has no true-division expression")
    require(not any(
        name == "random" or name.startswith("random.") for name in imports
    ), "certificate source has no random import")
    require(all(name.split(".")[0] in allowed_roots for name in imports),
            "certificate imports only Python standard-library modules")
    return {
        "checks": CHECKS - start,
        "no_float_literals": True,
        "no_randomness": True,
        "no_assert_statements": True,
        "no_true_division": True,
        "stdlib_only": True,
    }


def main() -> None:
    results = {
        "critical_orbit_partition": check_critical_orbit_partition(),
        "resonance_channels_and_tube_moments":
            check_resonance_channels_and_moments(),
        "common_profile_gram_large_sieve":
            check_common_profile_large_sieve(),
        "failure_witnesses": check_failure_witnesses(),
        "endpoint_exponent_ledger": check_exponent_ledger(),
        "source_constraints": check_source_constraints(),
    }
    claims = {
        "finite_cyclic_model_is_only_an_analogue": True,
        "exact_all_band_fourier_partition": True,
        "exact_equal_band_rank_and_trace": True,
        "critical_compressed_trace_per_band_is_one": True,
        "exact_resonance_tile_channel_map": True,
        "unlabelled_synthesis_norm_squared_is_K": True,
        "resolved_channel_collision_norm_squared_is_R": True,
        "exact_tube_first_and_second_moments": True,
        "common_profile_rational_gram_identity": True,
        "common_profile_rational_large_sieve_bound": True,
        "output_parseval_implies_atomic_gain": False,
        "channel_labels_may_be_erased_without_loss": False,
        "continuous_asymptotic_large_sieve_proved_by_certificate": False,
        "actual_projective_square_envelope_certified": False,
        "residual_grouping_controlled": False,
        "fixed_shift_prime_pair_bound": False,
        "parity_barrier_broken": False,
        "twin_prime_conjecture": False,
    }
    normalized_source = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    payload = {
        "arithmetic": (
            "finite-field, integer exhaustive enumeration, and "
            "fractions.Fraction; no floats or randomness"
        ),
        "certificate_version": 1,
        "check_total": CHECKS,
        "claims": claims,
        "normalized_source_sha256": sha256(normalized_source).hexdigest(),
        "paper": "TPC-48",
        "results": results,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    payload["certificate_digest"] = sha256(canonical).hexdigest()
    output = Path(__file__).with_name("tpc48_certificate.json")
    output_bytes = (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True)
        + "\n"
    ).encode("utf-8")
    output.write_bytes(output_bytes)
    print(
        "TPC-48 exact certificate:"
        f" {CHECKS} checks;"
        f" digest {payload['certificate_digest']};"
        f" source_sha256 {payload['normalized_source_sha256']};"
        f" json_sha256 {sha256(output_bytes).hexdigest()};"
        f" wrote {output.name}"
    )


if __name__ == "__main__":
    main()
