#!/usr/bin/env python3
"""Read-only exact checker for the V60 moving-hole translation compiler."""

from __future__ import annotations

import argparse
import cmath
import json
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised for any failed V60 contract check."""


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_moving_hole_bdh_translation_compiler.md"
PAPER = ROOT / "papers/tpc-207-critical-moving-hole-bdh-defect"

REGISTRY = (
    "V60_MAXIMUM_CLAIM = EXACT_MOVING_HOLE_PROJECTOR_AND_Q_MINUS_2_DIAGONAL_COMPILER_PLUS_DETERMINISTIC_X_POWER_53_OVER_32_COLLECTIVE_TRANSLATION_DEFECT_BOUND",
    "V60_ROUTE_ADVANCE = YES",
    "V60_STRUCTURAL_THRESHOLD_A = PASS",
    "V60_TRANSLATION_SUBGATE_DELTA = 1_OVER_96_PROVED",
    "V60_TRANSLATION_SUBGATE_STRICT_1_OVER_400 = PAID",
    "V60_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "V60_ARITHMETIC_ADVANCE = NO",
    "V60_GLOBAL_GATE_B_ADVANCE = NO",
    "V60_FIXED_ATOM_CREDIT = 0",
    "V60_L2 = NONE",
    "V60_TPC_207_TRIGGER = true",
    "V60_MOVING_HOLE_IDENTITY = PROVED_EXACT_V_H_EQUALS_V_ALL_MINUS_Q_OVER_Q_MINUS_1_TIMES_SELECTED_CENTERED_COORDINATE_SQUARED",
    "V60_PROJECTOR_REPRESENTATION = PROVED_EXACT_V_H_EQUALS_V_ALL_MINUS_ABS_INNER_PRODUCT_Z_V_H_SQUARED",
    "V60_TRANSLATION_DEFECT_RANK = PROVED_AT_MOST_TWO",
    "V60_TRANSLATION_DEFECT_SPECTRUM = PROVED_PLUS_MINUS_SQRT_Q_Q_MINUS_2_OVER_Q_MINUS_1_FOR_Q_GT_2_AND_NONZERO_HOLE",
    "V60_TRANSLATION_DEFECT_NORM = PROVED_TENDS_TO_ONE_SO_RANK_TWO_ALONE_GIVES_NO_SAVING",
    "V60_Q_MINUS_2_DIAGONAL_LIFT = PROVED_EXACT_R_H_MINUS_R_0_EQUALS_LEVERAGE_DIFFERENCE_PLUS_KAPPA_E_H_MINUS_E_0",
    "V60_OUTER_Q_LIFT = PROVED_EXACT_Q_TIMES_THE_COMPLETE_REMAINDER_DIFFERENCE",
    "V60_PHYSICAL_TRANSLATION_SIGN = PROVED_H_Q_EQUALS_MINUS_S_MOD_Q_FOR_N_EQUALS_S_PLUS_M",
    "V60_COMMON_ORIGIN_POLICY = REQUIRED_B_AND_W_ROWS_SHARE_ONE_PHYSICAL_ORIGIN",
    "V60_FOUR_PACKET_DEFECT = PROVED_EXACT_AFTER_I_POWER_J_POLARIZATION_BEFORE_ANY_PACKET_ABSOLUTE_VALUE",
    "V60_DFT_REFINEMENT = PROVED_LEVERAGE_EQUAL_FREQUENCIES_CANCEL_WHILE_DIAGONAL_F_TERM_REMAINS",
    "V60_CENTERED_SELECTOR_L1 = PROVED_H_OVER_Q_PLUS_ONE",
    "V60_KERNEL_FIRST_POLICY = PROVED_INTEGRATE_TO_K_H_BEFORE_ESTIMATING_BLOCK_PAIRS",
    "V60_BLOCK_SEPARATION_SUM = PROVED_SCHWARTZ_WEIGHTS_GIVE_J_NOT_J_SQUARED",
    "V60_DIAGONAL_BLOCK_COUNT = PROVED_BOUNDED_OVERLAP_GIVES_J_NOT_J_SQUARED",
    "V60_GENERAL_DEFECT_BOUND = PROVED_J_TIMES_H_SQUARED_PLUS_H_Q_PLUS_Q_SQUARED_WITH_COEFFICIENT_ENVELOPES",
    "V60_LITERAL_COEFFICIENT_ENVELOPE = RETAINED_X_POWER_O1",
    "V60_LITERAL_DEFECT_BOUND = PROVED_X_POWER_53_OVER_32_PLUS_O1",
    "V60_NATURAL_SCALE_RATIO = PROVED_X_H_OVER_X_Q_SQUARED_EQUALS_X_POWER_MINUS_1_OVER_96",
    "V60_TRANSLATION_COMPONENT_STATUS = PAID_FOR_EVERY_FIXED_DELTA_PRIME_BETWEEN_1_OVER_400_AND_1_OVER_96",
    "V60_CORRECTED_Q5_FIXTURE = PROVED_E_0_50_E_1_1_GIVES_R_0_ZERO_AND_R_1_75_OVER_2",
    "V60_HARPER_PRIME_ROW_CROSSWALK = SOURCE_LOCKED_PRIME_GCD_GROUPED_VARIANCE_EQUALS_STANDARD_ZERO_HOLE_VARIANCE",
    "V60_HARPER_TRANSLATION_MISMATCH = RESOLVED_EXACTLY_AND_DEFECT_PAID",
    "V60_HARPER_INPUT_CONDITIONS = OPEN_UNVERIFIED_UNIFORMLY_FOR_LITERAL_PACKETS_BLOCKS_AND_V",
    "V60_HARPER_MODULUS_SUBSET = OPEN_ALL_MODULI_THEOREM_DOES_NOT_CONTROL_PRIME_ONLY_SIGNED_REMAINDER",
    "V60_ZERO_HOLE_POWER_THEOREM = OPEN_PRIME_ONLY_Q_WEIGHTED_KERNEL_LOCALIZED_Q_MINUS_2_DIAGONAL_SUBTRACTED_FOUR_PACKET_SIGNED_REMAINDER",
    "V60_BLOMER_PASCADI_ATTACHMENT = STILL_POST_EMITTER_ONLY",
    "V60_FIRST_FATAL = NO_THEOREM_CONTROLS_THE_STANDARD_ZERO_HOLE_PRIME_ONLY_Q_WEIGHTED_KERNEL_LOCALIZED_EXACT_DIAGONAL_SUBTRACTED_SIGNED_REMAINDER_FOR_THE_FOUR_LITERAL_PACKETS_OR_PERFORMS_ITS_COLLECTIVE_REASSEMBLY",
    "V60_NUMBERED_RELEASE = TPC_207_STRUCTURAL_THRESHOLD_A",
    "V60_ROUND2_CLUE = EXPAND_THE_ZERO_HOLE_CENTERED_SELECTOR_IN_ADDITIVE_FREQUENCIES_AND_COMPILE_ONLY_THE_OFF_EQUAL_FREQUENCY_LEVERAGE_PART_WHILE_RETAINING_THE_SEPARATE_DIAGONAL_F_TERM",
    "V60_REUSABLE_STRUCTURE = NORMALIZED_CENTERED_RESIDUE_SELECTOR_PLUS_POLARIZE_THEN_INTEGRATE_THEN_ESTIMATE_ORDER",
    "V60_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_TRANSLATION_SUBGATE_PAID_ZERO_HOLE_PRIME_SIGNED_BDH_GATE_OPEN",
)


def fail(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def mean(values: tuple[complex, ...], omit: int | None = None) -> complex:
    selected = [value for idx, value in enumerate(values) if idx != omit]
    return sum(selected, 0j) / len(selected)


def variance(values: tuple[complex, ...], omit: int | None = None) -> float:
    center = mean(values, omit)
    return sum(abs(value - center) ** 2 for idx, value in enumerate(values) if idx != omit)


def check_moving_hole() -> int:
    count = 0
    for q in (2, 3, 5, 7):
        values = tuple(complex(r + 1, -1 if r % 2 else 1) for r in range(q))
        mu = mean(values)
        all_variance = variance(values)
        for hole in range(q):
            lhs = variance(values, hole)
            rhs = all_variance - q / (q - 1) * abs(values[hole] - mu) ** 2
            fail(abs(lhs - rhs) < 1e-10, f"moving-hole identity failed q={q}, h={hole}")
            count += 1
    return count


def check_diagonal_lift() -> int:
    count = 0
    for q in (3, 5, 7):
        values = tuple(complex(r + 2, 2 * r - 1) for r in range(q))
        energies = tuple(Fraction((r + 1) * (r + 2), 2) for r in range(q))
        mu = mean(values)
        kappa = Fraction(q - 2, q - 1)
        for hole in range(q):
            r_h = variance(values, hole) - float(kappa * sum(energies[r] for r in range(q) if r != hole))
            r_0 = variance(values, 0) - float(kappa * sum(energies[r] for r in range(q) if r != 0))
            rhs = q / (q - 1) * (abs(values[0] - mu) ** 2 - abs(values[hole] - mu) ** 2)
            rhs += float(kappa * (energies[hole] - energies[0]))
            fail(abs((r_h - r_0) - rhs) < 1e-10, f"diagonal lift failed q={q}, h={hole}")
            count += 1
    values = (10 + 0j, 1 + 0j, 0j, 0j, 0j)
    energies = (50, 1, 0, 0, 0)
    kappa = Fraction(3, 4)
    r0 = variance(values, 0) - float(kappa * sum(energies[1:]))
    r1 = variance(values, 1) - float(kappa * (energies[0] + sum(energies[2:])))
    fail(abs(r0) < 1e-12, "corrected q=5 fixture R0 changed")
    fail(abs(r1 - 37.5) < 1e-12, "corrected q=5 fixture R1 changed")
    return count + 2


def check_polarization() -> int:
    fixtures = (
        (2 + 3j, -1 + 2j),
        (Fraction(3, 2) + Fraction(5, 3) * 1j, Fraction(-7, 4) + Fraction(2, 5) * 1j),
    )
    for x, y in fixtures:
        rhs = sum((1j**j) * abs(x + (1j**j) * y) ** 2 for j in range(4)) / 4
        fail(abs(x * y.conjugate() - rhs) < 1e-10, "polarization orientation failed")
    return len(fixtures)


def check_spectrum_and_exponents() -> int:
    count = 0
    for q in (2, 3, 5, 7, 11):
        square = Fraction(q * (q - 2), (q - 1) ** 2)
        fail(Fraction(0) <= square <= Fraction(1), f"spectrum square out of range q={q}")
        if q == 2:
            fail(square == 0, "q=2 spectrum did not degenerate")
        count += 1
    h_exp = Fraction(21, 32)
    q_exp = Fraction(1, 3)
    j_exp = 1 - h_exp
    natural = 1 + 2 * q_exp
    defect = j_exp + 2 * h_exp
    fail(defect == Fraction(53, 32), "defect exponent changed")
    fail(natural - defect == Fraction(1, 96), "critical saving changed")
    fail(Fraction(1, 96) - Fraction(1, 400) == Fraction(19, 2400), "strict margin changed")
    fail(j_exp + h_exp + q_exp == Fraction(4, 3), "diagonal exponent changed")
    return count + 4


def check_translation_sign() -> int:
    count = 0
    for q in (3, 5, 7):
        for s in (-11, -1, 0, 1, 8, 19):
            hole = (-s) % q
            fail((s + hole) % q == 0, f"translation sign failed q={q}, s={s}")
            count += 1
    return count


def check_files() -> int:
    fail(PROOF.is_file(), "V60 proof missing")
    proof_text = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        fail(row in proof_text, f"registry row missing from V60 proof: {row}")
    required_paper = (
        "README.md",
        "paper/main.tex",
        "paper/references.bib",
        "paper/paper.pdf",
        "code/moving_hole.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required_paper:
        fail((PAPER / relative).is_file(), f"TPC-207 artifact missing: {relative}")
    return len(REGISTRY) + len(required_paper) + 1


def run() -> dict[str, object]:
    counts = {
        "moving_hole_rows": check_moving_hole(),
        "diagonal_rows": check_diagonal_lift(),
        "polarization_rows": check_polarization(),
        "spectrum_exponent_rows": check_spectrum_and_exponents(),
        "translation_rows": check_translation_sign(),
        "file_contract_rows": check_files(),
    }
    return {
        "classification": "V60_MOVING_HOLE_TRANSLATION_COMPILER_L1",
        "verdict": "PASS",
        "counts": counts,
        "translation_defect_exponent": "53/32",
        "critical_saving": "1/96",
        "full_gate_b": "OPEN",
        "arithmetic_advance": False,
        "l2": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run the read-only V60 checks")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        payload = run()
    except CheckFailure as exc:
        print(f"TPC V60 moving-hole checker: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
