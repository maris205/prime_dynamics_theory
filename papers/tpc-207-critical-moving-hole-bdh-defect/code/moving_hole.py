"""Exact Gaussian-rational arithmetic for the TPC-207 certificate.

This module is deliberately standard-library only.  Complex numbers are
represented by pairs of fractions, so every finite identity is checked
without floating-point tolerance.  The executable checks are finite QA for
the paper; they are not a substitute for its general proofs.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable, Sequence, Tuple

Gaussian = Tuple[Fraction, Fraction]

ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))
I: Gaussian = (Fraction(0), Fraction(1))


def gaussian(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gneg(value: Gaussian) -> Gaussian:
    return (-value[0], -value[1])


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return gadd(left, gneg(right))


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gscale(scale: int | Fraction, value: Gaussian) -> Gaussian:
    scale = Fraction(scale)
    return (scale * value[0], scale * value[1])


def gconj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def gabs2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def gsum(values: Iterable[Gaussian]) -> Gaussian:
    total = ZERO
    for value in values:
        total = gadd(total, value)
    return total


def ipow(power: int) -> Gaussian:
    return (ONE, I, gneg(ONE), gneg(I))[power % 4]


def mean(row: Sequence[Gaussian]) -> Gaussian:
    if not row:
        raise ValueError("row must be nonempty")
    return gscale(Fraction(1, len(row)), gsum(row))


def leave_one_mean(row: Sequence[Gaussian], hole: int) -> Gaussian:
    q = len(row)
    if q < 2:
        raise ValueError("q must be at least 2")
    if not 0 <= hole < q:
        raise IndexError("hole outside row")
    return gscale(Fraction(1, q - 1), gsum(row[r] for r in range(q) if r != hole))


def all_variance(row: Sequence[Gaussian]) -> Fraction:
    center = mean(row)
    return sum((gabs2(gsub(value, center)) for value in row), Fraction(0))


def leave_one_variance(row: Sequence[Gaussian], hole: int) -> Fraction:
    center = leave_one_mean(row, hole)
    return sum(
        (gabs2(gsub(value, center)) for r, value in enumerate(row) if r != hole),
        Fraction(0),
    )


def moving_hole_rhs(row: Sequence[Gaussian], hole: int) -> Fraction:
    q = len(row)
    center = mean(row)
    return all_variance(row) - Fraction(q, q - 1) * gabs2(gsub(row[hole], center))


def remainder(row: Sequence[Gaussian], energies: Sequence[Fraction], hole: int) -> Fraction:
    q = len(row)
    if len(energies) != q:
        raise ValueError("energy row length mismatch")
    kappa = Fraction(q - 2, q - 1)
    diagonal = kappa * sum((energies[r] for r in range(q) if r != hole), Fraction(0))
    return leave_one_variance(row, hole) - diagonal


def remainder_defect_rhs(
    row: Sequence[Gaussian], energies: Sequence[Fraction], hole: int
) -> Fraction:
    q = len(row)
    center = mean(row)
    leverage = Fraction(q, q - 1) * (
        gabs2(gsub(row[0], center)) - gabs2(gsub(row[hole], center))
    )
    diagonal = Fraction(q - 2, q - 1) * (energies[hole] - energies[0])
    return leverage + diagonal


def rows_and_energies(
    coefficients: Sequence[Sequence[Gaussian]],
) -> tuple[list[Gaussian], list[Fraction]]:
    rows = [gsum(residue) for residue in coefficients]
    energies = [sum((gabs2(value) for value in residue), Fraction(0)) for residue in coefficients]
    return rows, energies


def packet_coefficients(
    beta: Sequence[Sequence[Gaussian]],
    omega: Sequence[Sequence[Gaussian]],
    phase: Gaussian,
) -> list[list[Gaussian]]:
    if len(beta) != len(omega):
        raise ValueError("residue count mismatch")
    packet: list[list[Gaussian]] = []
    for beta_residue, omega_residue in zip(beta, omega):
        width = max(len(beta_residue), len(omega_residue))
        packet.append(
            [
                gadd(
                    beta_residue[index] if index < len(beta_residue) else ZERO,
                    gmul(phase, omega_residue[index]) if index < len(omega_residue) else ZERO,
                )
                for index in range(width)
            ]
        )
    return packet


def cross_diagonal(
    beta: Sequence[Sequence[Gaussian]], omega: Sequence[Sequence[Gaussian]]
) -> list[Gaussian]:
    if len(beta) != len(omega):
        raise ValueError("residue count mismatch")
    result: list[Gaussian] = []
    for beta_residue, omega_residue in zip(beta, omega):
        width = max(len(beta_residue), len(omega_residue))
        result.append(
            gsum(
                gmul(
                    beta_residue[index] if index < len(beta_residue) else ZERO,
                    gconj(omega_residue[index] if index < len(omega_residue) else ZERO),
                )
                for index in range(width)
            )
        )
    return result


def polarized_remainder_defect(
    beta: Sequence[Sequence[Gaussian]],
    omega: Sequence[Sequence[Gaussian]],
    hole: int,
) -> Gaussian:
    total = ZERO
    for j in range(4):
        packet = packet_coefficients(beta, omega, ipow(j))
        row, energies = rows_and_energies(packet)
        scalar_defect = remainder(row, energies, hole) - remainder(row, energies, 0)
        total = gadd(total, gscale(scalar_defect, ipow(j)))
    return gscale(Fraction(1, 4), total)


def polarized_defect_rhs(
    beta: Sequence[Sequence[Gaussian]],
    omega: Sequence[Sequence[Gaussian]],
    hole: int,
) -> Gaussian:
    q = len(beta)
    beta_row, _ = rows_and_energies(beta)
    omega_row, _ = rows_and_energies(omega)
    beta_mean = mean(beta_row)
    omega_mean = mean(omega_row)
    term_zero = gmul(gsub(beta_row[0], beta_mean), gconj(gsub(omega_row[0], omega_mean)))
    term_hole = gmul(
        gsub(beta_row[hole], beta_mean),
        gconj(gsub(omega_row[hole], omega_mean)),
    )
    leverage = gscale(Fraction(q, q - 1), gsub(term_zero, term_hole))
    diagonal = cross_diagonal(beta, omega)
    diagonal_defect = gscale(
        Fraction(q - 2, q - 1), gsub(diagonal[hole], diagonal[0])
    )
    return gadd(leverage, diagonal_defect)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def gaussian_json(value: Gaussian) -> dict[str, str]:
    return {"re": fraction_text(value[0]), "im": fraction_text(value[1])}


def build_certificate() -> dict[str, object]:
    identity_rows: dict[str, object] = {}
    diagonal_rows: dict[str, object] = {}
    spectrum_rows: dict[str, object] = {}
    translation_rows: dict[str, object] = {}

    for q in (2, 3, 5, 7):
        row = [gaussian(r + 1, 1 if r % 2 == 0 else -1) for r in range(q)]
        energies = [gabs2(value) + r for r, value in enumerate(row)]
        holes: list[dict[str, object]] = []
        diagonal_holes: list[dict[str, object]] = []
        for hole in range(q):
            lhs = leave_one_variance(row, hole)
            rhs = moving_hole_rhs(row, hole)
            if lhs != rhs:
                raise AssertionError((q, hole, "moving-hole identity"))
            holes.append({"hole": hole, "lhs": fraction_text(lhs), "rhs": fraction_text(rhs)})

            defect = remainder(row, energies, hole) - remainder(row, energies, 0)
            defect_rhs = remainder_defect_rhs(row, energies, hole)
            if defect != defect_rhs:
                raise AssertionError((q, hole, "diagonal lift"))
            diagonal_holes.append(
                {"hole": hole, "lhs": fraction_text(defect), "rhs": fraction_text(defect_rhs)}
            )

        identity_rows[str(q)] = holes
        diagonal_rows[str(q)] = diagonal_holes
        spectrum_rows[str(q)] = {
            "nonzero_eigenvalue_square": fraction_text(Fraction(q * (q - 2), (q - 1) ** 2)),
            "rank": 0 if q == 2 else 2,
            "degeneracy": "zero defect" if q == 2 else "plus/minus square root",
        }
        translation_rows[str(q)] = [
            {"s": s, "moving_hole": (-s) % q} for s in (0, 1, q - 1, q + 2)
        ]

    beta_template = [
        [gaussian(1, 1), gaussian(2, -1)],
        [gaussian(-1, 2)],
        [gaussian(3, 0), gaussian(0, 1)],
        [gaussian(2, -2)],
        [gaussian(-2, 1), gaussian(1, 0)],
        [gaussian(1, -3)],
        [gaussian(0, 2), gaussian(2, 2)],
    ]
    omega_template = [
        [gaussian(2, 0), gaussian(-1, 1)],
        [gaussian(1, -2), gaussian(1, 0)],
        [gaussian(0, 1)],
        [gaussian(-2, -1), gaussian(1, 1)],
        [gaussian(3, 2)],
        [gaussian(-1, 0), gaussian(0, -1)],
        [gaussian(2, -2)],
    ]
    polarization: dict[str, object] = {}
    for q in (2, 3, 5, 7):
        beta = beta_template[:q]
        omega = omega_template[:q]
        rows: list[dict[str, object]] = []
        for hole in range(q):
            lhs = polarized_remainder_defect(beta, omega, hole)
            rhs = polarized_defect_rhs(beta, omega, hole)
            if lhs != rhs:
                raise AssertionError((q, hole, "polarization"))
            rows.append({"hole": hole, "lhs": gaussian_json(lhs), "rhs": gaussian_json(rhs)})
        polarization[str(q)] = rows

    fixture_coefficients = [
        [gaussian(5), gaussian(5)],
        [gaussian(1)],
        [],
        [],
        [],
    ]
    fixture_row, fixture_energy = rows_and_energies(fixture_coefficients)
    fixture_r0 = remainder(fixture_row, fixture_energy, 0)
    fixture_r1 = remainder(fixture_row, fixture_energy, 1)
    if fixture_r0 != 0 or fixture_r1 != Fraction(75, 2):
        raise AssertionError("corrected q=5 fixture")

    exponent_ledger = {
        "H": "21/32",
        "Q": "1/3",
        "J": "11/32",
        "JH2_equals_xH": "53/32",
        "target_5_over_3": "5/3",
        "translation_delta": "1/96",
        "identity": "53/32 = 5/3 - 1/96",
        "strict_1_over_400": (
            "paid for translation subgate only, for every fixed "
            "1/400 < delta_prime < 1/96"
        ),
    }
    if Fraction(53, 32) != Fraction(5, 3) - Fraction(1, 96):
        raise AssertionError("exponent identity")
    if not Fraction(1, 400) < Fraction(1, 96):
        raise AssertionError("strict endpoint comparison")

    return {
        "schema": "TPC207_MOVING_HOLE_CERTIFICATE_V1",
        "arithmetic": "exact Gaussian rationals; no floating-point tolerance",
        "moving_hole_identity": identity_rows,
        "q_minus_2_diagonal_lift": diagonal_rows,
        "translation_sign": {
            "convention": "n=s+m",
            "formula": "h_q=-s mod q",
            "fixtures": translation_rows,
        },
        "four_packet_polarization": {
            "packet": "beta+i^j omega",
            "weight": "i^j/4",
            "fixtures": polarization,
        },
        "spectrum_square": spectrum_rows,
        "corrected_q5_fixture": {
            "coefficients": {"residue_0": ["5", "5"], "residue_1": ["1"]},
            "row": [gaussian_json(value) for value in fixture_row],
            "energy": [fraction_text(value) for value in fixture_energy],
            "R_0": fraction_text(fixture_r0),
            "R_1": fraction_text(fixture_r1),
        },
        "rational_exponent_ledger": exponent_ledger,
        "claim_firewall": {
            "claim_level": "PROVED_STRUCTURAL_L1",
            "V60_ROUTE_ADVANCE": "YES",
            "V60_TRANSLATION_SUBGATE_DELTA": "1_OVER_96_PROVED",
            "V60_TRANSLATION_SUBGATE_STRICT_1_OVER_400": "PAID",
            "V60_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID",
            "V60_ARITHMETIC_ADVANCE": "NO",
            "V60_FIXED_ATOM_CREDIT": 0,
            "V60_L2": "NONE",
            "TPC_207_TRIGGER": True,
            "twin_prime_theorem": False,
            "checker_role": "finite QA, not theorem evidence",
        },
    }
