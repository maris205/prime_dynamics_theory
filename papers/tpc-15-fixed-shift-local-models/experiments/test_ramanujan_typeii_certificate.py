"""Unit tests for the TPC-15 finite certificate."""

import math
import unittest
from fractions import Fraction

from experiments import ramanujan_typeii_certificate as cert


class RamanujanTypeIICertificateTests(unittest.TestCase):
    def test_complete_certificate(self) -> None:
        data = cert.build_certificate()
        cert.validate(data)

    def test_ramanujan_divisor_expansion(self) -> None:
        for q_cut in range(1, 13):
            for n in range(1, 129):
                self.assertEqual(
                    cert.hb_lambda(q_cut, n),
                    cert.hb_lambda_from_divisors(q_cut, n),
                )

    def test_progression_calibration_up_to_cutoff(self) -> None:
        for q_cut in range(2, 10):
            for h in (1, 2, 3, 6):
                for m in range(1, q_cut + 1):
                    self.assertEqual(
                        cert.progression_mean(q_cut, m, h), cert.rho(h, m)
                    )

    def test_calibration_can_fail_beyond_cutoff(self) -> None:
        self.assertEqual(cert.progression_mean(5, 6, 1), Fraction(5, 2))
        self.assertEqual(cert.rho(1, 6), Fraction(3, 1))

    def test_periodic_correlation_is_truncated_singular_series(self) -> None:
        for q_cut in range(2, 11):
            for h in (1, 2, 3, 4, 6, 10):
                self.assertEqual(
                    cert.periodic_model_correlation(q_cut, h),
                    cert.truncated_singular_series(q_cut, h),
                )

    def test_shell_local_coefficients(self) -> None:
        self.assertEqual(cert.beta_h(2), Fraction(1, 3))
        self.assertEqual(cert.phi_ratio(2) - cert.beta_h(2), Fraction(1, 6))
        for h in (2, 6, 10, 30, 42):
            self.assertGreater(cert.phi_ratio(h) - cert.beta_h(h), 0)

    def test_vaughan_identity(self) -> None:
        for u, v in ((3, 5), (7, 4), (10, 10)):
            for n in range(2, 513):
                self.assertAlmostEqual(
                    sum(cert.vaughan_pointwise_terms(n, u, v)),
                    cert.von_mangoldt(n),
                    places=12,
                )

    def test_finite_selector_inequality(self) -> None:
        states = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 1],
        ]
        events, pair_counts = cert.selector_counts(states)
        self.assertGreaterEqual(sum(pair_counts.values()), events)
        self.assertGreaterEqual(
            max(pair_counts.values()), math.ceil(events / math.comb(4, 2))
        )


if __name__ == "__main__":
    unittest.main()
