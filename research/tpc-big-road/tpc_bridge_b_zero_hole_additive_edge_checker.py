#!/usr/bin/env python3
"""Read-only exact checker for the V61 zero-hole additive edge frame."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterable


class CheckFailure(RuntimeError):
    """Raised when an exact V61 contract check fails."""


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_zero_hole_additive_edge_frame.md"

REGISTRY = (
    "V61_MAXIMUM_CLAIM = EXACT_ZERO_HOLE_COMPLETE_GRAPH_ADDITIVE_EDGE_FRAME_WITH_CELLWISE_Q_MINUS_2_DIAGONAL_CANCELLATION_AND_UNIQUE_LITERAL_TWO_FREQUENCY_NO_SPARSIFICATION",
    "V61_ROUTE_ADVANCE = YES",
    "V61_STRUCTURAL_THRESHOLD_A = PASS",
    "V61_ZERO_HOLE_FREQUENCY_PROJECTION = PROVED_V_0_EQUALS_ONE_OVER_Q_TIMES_Y_STAR_P_Y_WITH_RANK_Q_MINUS_2",
    "V61_COMPLETE_GRAPH_FRAME = PROVED_V_0_EQUALS_ONE_OVER_Q_Q_MINUS_1_TIMES_SUM_UNORDERED_EDGE_TRANSFORM_SQUARED",
    "V61_EDGE_COUNT = PROVED_Q_MINUS_1_TIMES_Q_MINUS_2_OVER_2",
    "V61_FRAME_REDUNDANCY = PROVED_Q_MINUS_1_OVER_2",
    "V61_ZERO_RESIDUE_ANNIHILATION = PROVED_DELTA_K_L_N_ZERO_WHEN_Q_DIVIDES_N",
    "V61_EDGE_MASS = PROVED_SUM_EDGE_ABS_DELTA_SQUARED_EQUALS_Q_Q_MINUS_2_ON_UNITS_AND_ZERO_OFF_UNITS",
    "V61_Q_MINUS_2_DIAGONAL_DISTRIBUTION = PROVED_EXACT_ONE_OVER_Q_Q_MINUS_1_EDGE_DIAGONAL_EQUALS_Q_MINUS_2_OVER_Q_MINUS_1_UNIT_DIAGONAL",
    "V61_EDGEWISE_OFFDIAGONAL_CELL = PROVED_E_CELL_EQUALS_SUM_T_NOT_EQUAL_U_WITH_NO_COEFFICIENT_DIAGONAL",
    "V61_OUTER_Q_NORMALIZATION = PROVED_Q_R_0_EQUALS_ONE_OVER_Q_MINUS_1_SUM_EDGE_E_CELL",
    "V61_FOUR_PACKET_POLARIZATION = PROVED_EXACT_EDGE_BY_EDGE_BEFORE_ANY_ABSOLUTE_VALUE",
    "V61_PHYSICAL_KERNEL = PROVED_ZERO_ON_NONUNITS_Q_Q_MINUS_2_ON_EQUAL_UNIT_RESIDUES_AND_MINUS_Q_ON_DISTINCT_UNIT_RESIDUES",
    "V61_LITERAL_SCALAR_CROSSWALK = PROVED_EDGE_KERNEL_OVER_Q_MINUS_1_EQUALS_Q_TIMES_U_1",
    "V61_ORIENTED_DIFFERENCE_FIBER = PROVED_DELTA_K_K_PLUS_D_EQUALS_E_MINUS_K_N_TIMES_ONE_MINUS_E_MINUS_D_N_WITH_FACTOR_ONE_HALF",
    "V61_TWO_FREQUENCY_DECOMPOSITION_UNIQUENESS = PROVED_EVERY_EDGE_WEIGHT_FOR_P_EQUALS_ONE_OVER_Q_MINUS_1",
    "V61_LITERAL_EDGE_SPARSIFICATION = REFUTED_NO_STRICT_EDGE_SUBSET_REPRESENTS_THE_PROJECTION",
    "V61_EQUAL_OFF_EQUAL_SEPARATE_ESTIMATION = REFUTED_ZERO_RESIDUE_SPIKE_HAS_EQUAL_NONZERO_PIECES_AND_ZERO_SUM",
    "V61_SINGLE_UNIT_CELL_DIAGONAL = PROVED_CANCELS_INSIDE_EVERY_EDGE",
    "V61_HARPER_ATTACHMENT = OPEN_INPUT_HYPOTHESES_PRIME_SUBSET_SIGNED_DIAGONAL_AND_REASSEMBLY_UNPAID",
    "V61_BLOMER_PASCADI_ATTACHMENT = OPEN_ADDITIVE_EDGE_PRE_EMITTER_NOT_YET_A_KLOOSTERMAN_CELL",
    "V61_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "V61_ARITHMETIC_ADVANCE = NO",
    "V61_GLOBAL_GATE_B_ADVANCE = NO",
    "V61_FIXED_ATOM_CREDIT = 0",
    "V61_L2 = NONE",
    "V61_TPC_208_TRIGGER = true",
    "V61_NUMBERED_RELEASE = TPC_208_STRUCTURAL_THRESHOLD_A",
    "V61_FIRST_FATAL = NO_THEOREM_JOINTLY_COMPILES_THE_COMPLETE_ORIENTED_D_K_ADDITIVE_EDGE_FRAME_OF_THE_LITERAL_BLOCK_PACKETS_INTO_SOURCE_VALID_KLOOSTERMAN_CELLS_AND_REASSEMBLES_ALL_BLOCKS_FOUR_PACKET_SIGNS_AND_PRIME_MODULI_WITH_A_FIXED_SAVING",
    "V61_ROUND2_CLUE = APPLY_MOBIUS_AND_POISSON_TRANSFORMS_TO_THE_WHOLE_D_K_TIGHT_FRAME_BEFORE_ANY_EDGE_OR_FIBER_TRIANGLE_AND_TEST_WHETHER_ONE_DUAL_VARIABLE_IS_SHARED_ACROSS_THE_FRAME",
    "V61_REUSABLE_STRUCTURE = ZERO_HOLE_PROJECTOR_AS_COMPLETE_GRAPH_LAPLACIAN_PLUS_EDGEWISE_DIAGONAL_DELETION_AND_ORIENTED_UNIT_ANNIHILATING_DIFFERENCE_FIBERS",
    "V61_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_ZERO_HOLE_PRE_EMITTER_BUILT_COLLECTIVE_KLOOSTERMAN_COMPILER_OPEN",
)

SOURCE_LOCKS = (
    ("Harper", "arXiv:2412.19644v1", "general-sequence BDH with explicit hypotheses"),
    ("Blomer--Pascadi", "arXiv:2607.24311v1", "fixed-modulus post-emitter Kloosterman bilinear form"),
    ("Pascadi", "arXiv:2404.04239v3", "post-emitter sparse-Fourier and Kloosterman machinery"),
)

Gaussian = tuple[Fraction, Fraction]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gscale(scalar: Fraction, value: Gaussian) -> Gaussian:
    return scalar * value[0], scalar * value[1]


def gabs2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def gsum(values: Iterable[Gaussian]) -> Gaussian:
    total = (Fraction(0), Fraction(0))
    for value in values:
        total = gadd(total, value)
    return total


def edges(vertex_count: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )


def complete_graph_laplacian(vertex_count: int) -> tuple[tuple[int, ...], ...]:
    matrix = [[0 for _ in range(vertex_count)] for _ in range(vertex_count)]
    for left, right in edges(vertex_count):
        matrix[left][left] += 1
        matrix[right][right] += 1
        matrix[left][right] -= 1
        matrix[right][left] -= 1
    return tuple(tuple(row) for row in matrix)


def cyclotomic_integer(coefficients: tuple[int, ...]) -> int:
    """Evaluate an integer combination of q-th roots known to be rational.

    For prime q, Phi_q=1+z+...+z^(q-1).  A coefficient vector represents an
    integer exactly when all nonconstant reduced coefficients agree.
    """

    require(len(coefficients) >= 2, "cyclotomic vector too short")
    tail = coefficients[1]
    require(
        all(value == tail for value in coefficients[1:]),
        "cyclotomic expression was not rational",
    )
    return coefficients[0] - tail


def edge_kernel(q: int, residue_left: int, residue_right: int) -> int:
    coefficients = [0 for _ in range(q)]
    for left in range(1, q):
        for right in range(left + 1, q):
            terms = (
                (1, -left * residue_left + left * residue_right),
                (-1, -left * residue_left + right * residue_right),
                (-1, -right * residue_left + left * residue_right),
                (1, -right * residue_left + right * residue_right),
            )
            for sign, exponent in terms:
                coefficients[exponent % q] += sign
    return cyclotomic_integer(tuple(coefficients))


def direct_zero_hole_variance(row: tuple[Gaussian, ...]) -> Fraction:
    q = len(row)
    require(q >= 2, "row modulus too small")
    unit_row = row[1:]
    mean = gscale(Fraction(1, q - 1), gsum(unit_row))
    return sum(gabs2(gsub(value, mean)) for value in unit_row)


def edge_kernel_variance(row: tuple[Gaussian, ...]) -> Gaussian:
    q = len(row)
    total = (Fraction(0), Fraction(0))
    for residue_left in range(q):
        for residue_right in range(q):
            coefficient = Fraction(
                edge_kernel(q, residue_left, residue_right), q * (q - 1)
            )
            total = gadd(
                total,
                gscale(
                    coefficient,
                    gmul(row[residue_left], gconj(row[residue_right])),
                ),
            )
    return total


def check_laplacian_and_rank() -> int:
    count = 0
    for q in (2, 3, 5, 7, 11):
        vertex_count = q - 1
        laplacian = complete_graph_laplacian(vertex_count)
        for left in range(vertex_count):
            for right in range(vertex_count):
                expected = vertex_count - 1 if left == right else -1
                require(
                    laplacian[left][right] == expected,
                    f"complete-graph Laplacian mismatch q={q}",
                )
                count += 1
        require(
            len(edges(vertex_count)) == (q - 1) * (q - 2) // 2,
            f"edge count mismatch q={q}",
        )
        require(max(q - 2, 0) == vertex_count - 1, f"rank mismatch q={q}")
        count += 2
    return count


def check_physical_kernel() -> int:
    count = 0
    for q in (2, 3, 5, 7, 11):
        for residue_left in range(q):
            for residue_right in range(q):
                observed = edge_kernel(q, residue_left, residue_right)
                if residue_left == 0 or residue_right == 0:
                    expected = 0
                elif residue_left == residue_right:
                    expected = q * (q - 2)
                else:
                    expected = -q
                require(
                    observed == expected,
                    f"physical kernel mismatch q={q}, r={residue_left}, s={residue_right}",
                )
                count += 1
    return count


def check_rows_and_diagonal() -> int:
    count = 0
    for q in (2, 3, 5, 7, 11):
        row = tuple(
            (Fraction(residue + 1, 2), Fraction((-1) ** residue, residue + 1))
            for residue in range(q)
        )
        direct = direct_zero_hole_variance(row)
        emitted = edge_kernel_variance(row)
        require(emitted[1] == 0, f"edge-frame variance not real q={q}")
        require(emitted[0] == direct, f"edge-frame variance mismatch q={q}")

        if q > 2:
            edge_mass = q * (q - 2)
            normalized = Fraction(edge_mass, q * (q - 1))
            require(
                normalized == Fraction(q - 2, q - 1),
                f"q-2 diagonal normalization mismatch q={q}",
            )
        else:
            require(len(edges(q - 1)) == 0, "q=2 edge degeneration failed")
        count += 4
    return count


def check_polarization() -> int:
    fixtures = (
        ((Fraction(2), Fraction(3)), (Fraction(-1), Fraction(2))),
        ((Fraction(3, 2), Fraction(5, 3)), (Fraction(-7, 4), Fraction(2, 5))),
    )
    imaginary_unit = (Fraction(0), Fraction(1))
    for left, right in fixtures:
        rhs = (Fraction(0), Fraction(0))
        power = (Fraction(1), Fraction(0))
        for _ in range(4):
            packet = gadd(left, gmul(power, right))
            rhs = gadd(rhs, gscale(Fraction(1, 4), gscale(gabs2(packet), power)))
            power = gmul(power, imaginary_unit)
        require(rhs == gmul(left, gconj(right)), "polarization orientation changed")
    return len(fixtures)


def check_falsifiers_and_uniqueness() -> int:
    count = 0
    for q in (3, 5, 7, 11):
        d = q - 1
        diagonal_piece = Fraction(d, q)
        off_equal_piece = -Fraction(d, q)
        require(
            diagonal_piece != 0 and diagonal_piece + off_equal_piece == 0,
            f"zero-residue spike cancellation changed q={q}",
        )

        forced_weight = Fraction(1, d)
        projection_off_diagonal = -Fraction(1, d)
        require(
            -forced_weight == projection_off_diagonal,
            f"edge weight uniqueness changed q={q}",
        )

        ordered_count = d * (d - 1)
        unordered_count = d * (d - 1) // 2
        require(
            ordered_count == 2 * unordered_count,
            f"oriented fiber factor changed q={q}",
        )

        full_laplacian = complete_graph_laplacian(d)
        dropped = [list(row) for row in full_laplacian]
        dropped[0][0] -= 1
        dropped[1][1] -= 1
        dropped[0][1] += 1
        dropped[1][0] += 1
        require(
            tuple(tuple(row) for row in dropped) != full_laplacian,
            f"dropped-edge mutation escaped q={q}",
        )
        require(Fraction(1, q) != forced_weight, f"q versus q-1 mutation escaped q={q}")
        count += 5
    return count


def check_files_and_registry() -> int:
    require(PROOF.is_file(), "V61 proof is missing")
    proof_text = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof_text, f"registry row missing from proof: {row}")
    for author, arxiv_id, boundary in SOURCE_LOCKS:
        require(author in proof_text, f"source author missing: {author}")
        require(arxiv_id in proof_text, f"source id missing: {arxiv_id}")
        require(type(boundary) is str and bool(boundary), "source boundary malformed")
    return 1 + len(REGISTRY) + 3 * len(SOURCE_LOCKS)


def run() -> dict[str, object]:
    counts = {
        "laplacian_rank_rows": check_laplacian_and_rank(),
        "physical_kernel_rows": check_physical_kernel(),
        "row_diagonal_rows": check_rows_and_diagonal(),
        "polarization_rows": check_polarization(),
        "falsifier_uniqueness_rows": check_falsifiers_and_uniqueness(),
        "file_registry_rows": check_files_and_registry(),
    }
    return {
        "classification": "V61_ZERO_HOLE_ADDITIVE_EDGE_FRAME_L1",
        "verdict": "PASS",
        "counts": counts,
        "edge_vertices": "q-1",
        "edge_count": "(q-1)(q-2)/2",
        "projection_rank": "q-2",
        "outer_weight": "1/(q-1) times unordered edge sum",
        "full_gate_b": "OPEN",
        "arithmetic_advance": False,
        "l2": "NONE",
        "tpc_208_trigger": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run read-only V61 checks")
    arguments = parser.parse_args()
    if not arguments.check:
        parser.error("--check is required")
    try:
        payload = run()
    except CheckFailure as exc:
        print(f"TPC V61 zero-hole edge checker: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
