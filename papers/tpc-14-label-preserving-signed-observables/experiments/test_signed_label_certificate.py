"""Unit tests for the TPC-14 finite certificate."""

import math
import unittest

from experiments import signed_label_certificate as cert


class SignedLabelCertificateTests(unittest.TestCase):
    def test_complete_certificate(self) -> None:
        data = cert.build_certificate()
        cert.validate(data)

    def test_shell_identity(self) -> None:
        for n in range(2, 513):
            self.assertAlmostEqual(
                cert.shell_coefficient_direct(n),
                cert.shell_coefficient_closed(n),
                places=12,
            )

    def test_gcd_coordinates_are_bijective(self) -> None:
        for r in range(1, 513):
            ledger = cert.product_coordinate_ledger(r)
            self.assertEqual(len(ledger), len(cert.divisors(r)))
            self.assertEqual(len(ledger), len(set(ledger)))
            for a, b, k in ledger:
                self.assertEqual(math.gcd(a, b), 1)
                self.assertEqual(a * b * k * k, r)

    def test_vaughan_identity(self) -> None:
        for u, v in ((3, 5), (10, 10), (16, 7)):
            for n in range(2, 513):
                self.assertAlmostEqual(
                    sum(cert.vaughan_pointwise_terms(n, u, v)),
                    cert.von_mangoldt(n),
                    places=12,
                )

    def test_prime_semiprime_null_witness(self) -> None:
        p, q_1, q_2, r = 101, 11, 13, 10
        s = q_1 * q_2
        self.assertTrue(cert.is_prime(p))
        self.assertEqual(cert.divisor_signature(p, r), cert.divisor_signature(s, r))
        self.assertEqual(p % 7, s % 7)
        self.assertAlmostEqual(cert.hard_packet(p, r, r), 0.0)
        self.assertAlmostEqual(cert.hard_packet(s, r, r), -math.log(s))

    def test_signature_uses_only_proper_divisors(self) -> None:
        self.assertFalse(any(cert.divisor_signature(101, 150)))
        self.assertTrue(any(cert.divisor_signature(143, 150)))

    def test_shift_coordinate_radius(self) -> None:
        weights = [1.0, 2.0, 3.0, 2.0, 1.0]
        expected = 7.0 * math.sqrt(1.0 - 9.0 / 19.0)
        self.assertAlmostEqual(cert.shift_coordinate_radius(weights, 2, 7.0), expected)


if __name__ == "__main__":
    unittest.main()
