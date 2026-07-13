#!/usr/bin/env python3
"""Regression tests for the exact small-box reference implementation."""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np

from reference_kernel import (
    DEFAULT_SEED,
    BoxSpec,
    analyze_small_box,
    build_kernel_direct_modulus,
    build_kernel_prime_loop,
    centered_survivor_matrix,
    deterministic_validation_specs,
    exact_double_center_binary,
    floating_double_center,
    kappa_for_shift,
    primes_in_window,
    validate_constructions,
)


HERE = Path(__file__).resolve().parent


class LocalDataTests(unittest.TestCase):
    def test_kappa_omits_prime_divisors_of_h(self) -> None:
        primes = primes_in_window(2, 7)
        self.assertEqual(primes, (3, 5, 7))
        self.assertEqual(kappa_for_shift(primes, 6), Fraction(5, 8))
        self.assertEqual(kappa_for_shift(primes, 30), Fraction(5, 6))

    def test_invalid_odd_or_zero_shift_is_rejected(self) -> None:
        for h in (0, 3, -5):
            with self.subTest(h=h), self.assertRaises(ValueError):
                BoxSpec(10, 5, 20, 5, 2, 7, h).validate()


class ConstructionTests(unittest.TestCase):
    def test_inactive_prime_remains_in_the_unit_support(self) -> None:
        h2 = build_kernel_prime_loop(BoxSpec(101, 30, 151, 28, 2, 13, 2))
        h6 = build_kernel_prime_loop(BoxSpec(101, 30, 151, 28, 2, 13, 6))
        self.assertEqual(h2.primes, h6.primes)
        self.assertEqual(h2.m_survivors, h6.m_survivors)
        self.assertEqual(h2.n_survivors, h6.n_survivors)
        self.assertIn(3, h6.primes)
        self.assertNotIn(3, h6.active_primes)
        self.assertTrue(all(value % 3 != 0 for value in h6.m_survivors))
        self.assertTrue(all(value % 3 != 0 for value in h6.n_survivors))

    def test_prime_loop_equals_direct_modulus_for_general_even_shifts(self) -> None:
        for h in (-30, -6, -2, 2, 6, 10, 30):
            with self.subTest(h=h):
                spec = BoxSpec(41, 17, 73, 19, 2, 19, h)
                first = build_kernel_prime_loop(spec)
                second = build_kernel_direct_modulus(spec)
                self.assertEqual(first.active_primes, second.active_primes)
                self.assertEqual(first.kappa, second.kappa)
                np.testing.assert_array_equal(first.kernel, second.kernel)

    def test_repeatable_generated_validation_cases(self) -> None:
        first = deterministic_validation_specs(DEFAULT_SEED)
        second = deterministic_validation_specs(DEFAULT_SEED)
        self.assertEqual(first, second)
        for spec in first:
            validate_constructions(spec)


class CenteringAndNormalizationTests(unittest.TestCase):
    def test_exact_double_centering_has_integer_zero_margins(self) -> None:
        kernel = np.array(
            [[1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0]], dtype=np.uint8
        )
        kappa = Fraction(5, 8)
        exact = exact_double_center_binary(kernel, kappa)
        self.assertTrue(exact.has_exact_zero_margins())
        raw = kernel.astype(float) / float(kappa) - 1.0
        np.testing.assert_allclose(
            exact.as_float(), floating_double_center(raw), rtol=1e-14, atol=1e-14
        )

    def test_reported_raw_and_survivor_normalizations(self) -> None:
        spec = BoxSpec(100, 12, 140, 10, 3, 13, 6)
        construction = validate_constructions(spec)
        report = analyze_small_box(spec)
        allowed = int(construction.kernel.sum())
        survivor_pairs = construction.kernel.shape[0] * construction.kernel.shape[1]
        exact_sum = Fraction(allowed, 1) / construction.kappa - survivor_pairs
        self.assertEqual(
            report["raw_centered_sum"]["exact"],
            str(exact_sum.numerator)
            if exact_sum.denominator == 1
            else f"{exact_sum.numerator}/{exact_sum.denominator}",
        )
        self.assertAlmostEqual(
            report["raw_centered_sum"]["raw_interval_normalized_float"],
            float(exact_sum / (spec.m_length * spec.n_length)),
        )
        self.assertAlmostEqual(
            report["raw_centered_sum"]["survivor_normalized_float"],
            float(exact_sum / survivor_pairs),
        )

    def test_full_period_single_prime_singular_values(self) -> None:
        # [1,5) is exactly F_5^x.  For one active prime p=5, the centered
        # matrix divided by |G| has the three nonconstant singular values 1/3.
        spec = BoxSpec(1, 4, 1, 4, 3, 5, 2)
        construction = validate_constructions(spec)
        centered = centered_survivor_matrix(construction)
        singular_values = np.linalg.svd(centered, compute_uv=False)
        expected = np.array([4.0 / 3.0, 4.0 / 3.0, 4.0 / 3.0, 0.0])
        np.testing.assert_allclose(singular_values, expected, atol=1e-12)


class CliSmokeTest(unittest.TestCase):
    def test_cli_writes_reproducible_json_and_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "report.json"
            command = [
                sys.executable,
                str(HERE / "reference_kernel.py"),
                "--m-start",
                "50",
                "--m-length",
                "9",
                "--n-start",
                "80",
                "--n-length",
                "8",
                "--w",
                "3",
                "--y",
                "13",
                "--h",
                "6",
                "--output",
                str(output),
            ]
            first = subprocess.run(command, check=True, capture_output=True, text=True)
            payload_first = output.read_bytes()
            second = subprocess.run(command, check=True, capture_output=True, text=True)
            payload_second = output.read_bytes()
            self.assertEqual(payload_first, payload_second)
            self.assertIn("WARNING", first.stderr)
            self.assertIn("WARNING", second.stderr)
            report = json.loads(payload_first)
            self.assertTrue(
                report["validation"]["prime_loop_equals_direct_active_modulus"]
            )
            self.assertFalse(report["validation"]["stochastic_sampling_used"])
            self.assertTrue(
                math.isfinite(
                    report["svd"]["survivor_double_centered_operator_normalization"]
                )
            )


if __name__ == "__main__":
    unittest.main()
