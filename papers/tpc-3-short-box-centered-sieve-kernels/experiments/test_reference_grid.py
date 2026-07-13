#!/usr/bin/env python3
"""Regression tests for the checked-in deterministic reference grid."""

from __future__ import annotations

import csv
import io
import math
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path

from run_reference_grid import (
    DEFAULT_CERTIFICATE_OUTPUT,
    DEFAULT_OUTPUT,
    FIELDNAMES,
    REFERENCE_GRID,
    render_reference_grid,
    render_theorem_4_3_certificate,
)
from shift_completion_reference import (
    DEFAULT_ALPHA,
    DEFAULT_BETA,
    default_theorem_4_3_certificate,
)


HERE = Path(__file__).resolve().parent


def rows_by_id() -> dict[str, dict[str, str]]:
    return {
        row["case_id"]: row
        for row in csv.DictReader(io.StringIO(render_reference_grid()))
    }


class ReferenceGridTests(unittest.TestCase):
    def test_grid_is_byte_deterministic(self) -> None:
        self.assertEqual(render_reference_grid(), render_reference_grid())

    def test_schema_and_case_order_are_fixed(self) -> None:
        reader = csv.DictReader(io.StringIO(render_reference_grid()))
        self.assertEqual(tuple(reader.fieldnames or ()), FIELDNAMES)
        rows = list(reader)
        self.assertEqual(
            [row["case_id"] for row in rows],
            [case.case_id for case in REFERENCE_GRID],
        )

    def test_primes_dividing_h_remain_in_support_modulus(self) -> None:
        rows = rows_by_id()
        base_ids = ("base-h2", "base-h6", "base-h30", "base-h-minus6")
        support_shapes = {
            (rows[case_id]["survivor_rows"], rows[case_id]["survivor_columns"])
            for case_id in base_ids
        }
        base_prime_sets = {rows[case_id]["base_primes"] for case_id in base_ids}
        self.assertEqual(support_shapes, {("12", "11")})
        self.assertEqual(base_prime_sets, {"3;5;7;11;13"})

        self.assertEqual(rows["base-h2"]["inactive_prime_divisors_of_h"], "")
        self.assertEqual(rows["base-h6"]["inactive_prime_divisors_of_h"], "3")
        self.assertEqual(rows["base-h-minus6"]["inactive_prime_divisors_of_h"], "3")
        self.assertEqual(rows["base-h30"]["inactive_prime_divisors_of_h"], "3;5")
        self.assertEqual(rows["base-h6"]["active_primes"], "5;7;11;13")
        self.assertEqual(rows["base-h30"]["active_primes"], "7;11;13")

    def test_shift_dependent_kappa_values(self) -> None:
        rows = rows_by_id()
        self.assertEqual(rows["base-h2"]["kappa_exact"], "33/128")
        self.assertEqual(rows["base-h6"]["kappa_exact"], "33/64")
        self.assertEqual(rows["base-h30"]["kappa_exact"], "11/16")

    def test_checked_csv_matches_regeneration(self) -> None:
        self.assertTrue(DEFAULT_OUTPUT.exists())
        self.assertTrue(DEFAULT_CERTIFICATE_OUTPUT.exists())
        self.assertEqual(
            DEFAULT_OUTPUT.read_text(encoding="utf-8"), render_reference_grid()
        )
        self.assertEqual(
            DEFAULT_CERTIFICATE_OUTPUT.read_text(encoding="utf-8"),
            render_theorem_4_3_certificate(),
        )

    def test_exact_theorem_4_3_brute_force_certificate(self) -> None:
        certificate = default_theorem_4_3_certificate()
        self.assertEqual(certificate.modulus, 15)
        self.assertEqual(certificate.kappa, Fraction(3, 8))
        self.assertEqual(certificate.normalization, Fraction(23, 15))
        self.assertNotEqual(certificate.normalization, Fraction(23, 8))
        self.assertEqual(certificate.alpha_l1, Fraction(35, 12))
        self.assertEqual(certificate.beta_l1, Fraction(17, 6))
        self.assertEqual(certificate.short_energy, Fraction(7254509, 46656))
        self.assertEqual(certificate.complete_energy, Fraction(20869, 216))
        self.assertEqual(
            certificate.scaled_complete_energy, Fraction(479987, 3240)
        )
        self.assertEqual(certificate.discrepancy, Fraction(1713481, 233280))
        self.assertEqual(certificate.completion_cost, Fraction(1492, 9))
        self.assertEqual(certificate.theorem_bound, Fraction(132051325, 11664))
        self.assertEqual(
            certificate.slack,
            certificate.theorem_bound - certificate.discrepancy,
        )
        self.assertGreaterEqual(certificate.slack, 0)
        self.assertTrue(certificate.holds)

        # Independent gcd-based enumeration of the same rational specialization.
        # This does not call the prime-loop bilinear-form implementation used by
        # the certificate generator.
        def direct_form(ell: int) -> Fraction:
            total = Fraction(0, 1)
            for m, alpha_m in DEFAULT_ALPHA:
                if math.gcd(m, 15) != 1:
                    continue
                for n, beta_n in DEFAULT_BETA:
                    if math.gcd(n, 15) != 1:
                        continue
                    allowed = math.gcd(m * n + 2 * ell, 15) == 1
                    total += alpha_m * beta_n * (
                        Fraction(int(allowed), 1) / Fraction(3, 8) - 1
                    )
            return total

        direct_short = sum(
            (
                direct_form(ell) ** 2
                for ell in range(7, 30)
                if math.gcd(ell, 15) == 1
            ),
            Fraction(0, 1),
        )
        direct_complete = sum(
            (
                direct_form(ell) ** 2
                for ell in range(15)
                if math.gcd(ell, 15) == 1
            ),
            Fraction(0, 1),
        )
        self.assertEqual(direct_short, certificate.short_energy)
        self.assertEqual(direct_complete, certificate.complete_energy)
        self.assertLessEqual(
            abs(direct_short - Fraction(23, 15) * direct_complete),
            certificate.theorem_bound,
        )

    def test_cli_check_mode(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(HERE / "run_reference_grid.py"),
                "--check",
                "--output",
                str(DEFAULT_OUTPUT),
                "--certificate-output",
                str(DEFAULT_CERTIFICATE_OUTPUT),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("WARNING", completed.stderr)
        self.assertIn("7 grid rows", completed.stderr)


if __name__ == "__main__":
    unittest.main()
