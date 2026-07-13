"""Regression tests for the exact low-conductor certificates."""

import unittest
from fractions import Fraction

from exact_diagnostics import (
    PRIMES,
    Q,
    build_certificate,
    designed_square_certificate,
    exact_support_contributions,
    local_box_form,
    nonempty_supports,
    rough_fiber_certificate,
)


class RoughCharacterTests(unittest.TestCase):
    def test_fiber_and_character_bounds(self) -> None:
        for start in (-400, 0, 37, Q):
            for length in (0, 1, 83, Q - 1, Q):
                for support in nonempty_supports(PRIMES):
                    record = rough_fiber_certificate(start, length, PRIMES, support)
                    self.assertTrue(record["fiber_bound_verified"])
                    self.assertTrue(record["character_bound_verified"])


class DesignedSquareTests(unittest.TestCase):
    def test_exact_q_385_certificate(self) -> None:
        record = designed_square_certificate()
        self.assertEqual(record["A"], {"numerator": 7, "denominator": 8})
        self.assertEqual(record["C"], {"numerator": 8, "denominator": 11})
        self.assertEqual(record["mean_weight"], {"numerator": 93, "denominator": 121})
        self.assertEqual(
            record["t"],
            {
                "5": {"numerator": 16, "denominator": 11},
                "7": {"numerator": 12, "denominator": 11},
                "11": {"numerator": 10, "denominator": 11},
            },
        )
        self.assertTrue(record["upper_bound_verified"])
        self.assertTrue(record["all_one_prime_modes_zero"])
        self.assertTrue(record["pointwise_pair_hoeffding_identity_verified"])
        self.assertTrue(record["pair_parseval_verified"])
        self.assertEqual(
            record["centered_second_moment"],
            {"numerator": 2096, "denominator": 2883},
        )
        self.assertEqual(record["nonzero_support_moduli"], [35, 55, 77])
        self.assertEqual(
            record["pair_fourier_coefficient_magnitudes"],
            {
                "35": {"numerator": 16, "denominator": 93},
                "55": {"numerator": 8, "denominator": 93},
                "77": {"numerator": 4, "denominator": 93},
            },
        )


class KernelTests(unittest.TestCase):
    def test_all_finite_inequalities(self) -> None:
        record = build_certificate()["kernel"]
        self.assertTrue(record["fixed_parts_reconstruct"])
        self.assertTrue(record["energy_parts_reconstruct"])
        self.assertTrue(record["fixed_low_bound_verified"])
        self.assertTrue(record["fixed_high_bound_verified"])
        self.assertTrue(record["complete_low_bound_verified"])
        self.assertTrue(record["complete_high_bound_verified"])

    def test_exact_reference_values(self) -> None:
        record = build_certificate()["kernel"]
        self.assertEqual(record["unit_counts"], {"I": 50, "J": 51})
        self.assertEqual(record["h_2_allowed_pair_count"], 1439)
        self.assertEqual(
            record["h_2_centered_box_form"],
            {"numerator": 74, "denominator": 9},
        )
        self.assertEqual(record["complete_shift_mean"], {"numerator": 0, "denominator": 1})
        self.assertEqual(
            record["complete_shift_mean_square"],
            {"numerator": 65348, "denominator": 1215},
        )
        self.assertEqual(
            record["fixed_contributions_by_conductor"],
            {
                "5": {"numerator": 2, "denominator": 3},
                "7": {"numerator": 0, "denominator": 1},
                "11": {"numerator": -10, "denominator": 9},
                "35": {"numerator": 92, "denominator": 15},
                "55": {"numerator": 82, "denominator": 27},
                "77": {"numerator": 4, "denominator": 9},
                "385": {"numerator": -128, "denominator": 135},
            },
        )

    def test_kernel_invariants(self) -> None:
        base = local_box_form(19, 73, 83, 2)
        self.assertEqual(base, local_box_form(19 + Q, 73, 83, 2))
        self.assertEqual(base, local_box_form(19, 73 - Q, 83, 2))
        swapped = local_box_form(73, 19, 83, 2)
        self.assertEqual(base[3], swapped[3])
        self.assertEqual(local_box_form(19, 73, 83, 2 * Q)[3], Fraction(0))
        self.assertEqual(local_box_form(0, 73, Q, 2)[3], Fraction(0))


class ValidationTests(unittest.TestCase):
    def test_invalid_parameters(self) -> None:
        with self.assertRaises(ValueError):
            designed_square_certificate((3, 5, 7))
        with self.assertRaises(ValueError):
            designed_square_certificate((5, 7, 11), forbidden_residue=5)
        with self.assertRaises(ValueError):
            rough_fiber_certificate(0, 10, PRIMES, ())
        with self.assertRaises(ValueError):
            rough_fiber_certificate(0, -1, PRIMES, (5,))
        with self.assertRaises(ValueError):
            exact_support_contributions(0, 0, 10, 5, PRIMES)


if __name__ == "__main__":
    unittest.main()
