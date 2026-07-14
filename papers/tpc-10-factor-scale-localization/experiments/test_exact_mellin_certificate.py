import unittest
from fractions import Fraction

from exact_mellin_certificate import (
    ANNIHILATOR,
    MU_MINUS,
    MU_PLUS,
    NODES,
    WINDOW,
    best_polynomial_value,
    build_certificate,
    integer_moment,
    is_prime,
    moment,
    pairing,
)


class ExactMellinCertificateTests(unittest.TestCase):
    def test_prime_target_row(self):
        self.assertEqual(3**4 + 2, 83)
        self.assertTrue(is_prime(83))

    def test_profiles_are_probabilities(self):
        self.assertEqual(sum(MU_PLUS), 1)
        self.assertEqual(sum(MU_MINUS), 1)
        self.assertTrue(all(value >= 0 for value in MU_PLUS + MU_MINUS))

    def test_first_four_moments_agree(self):
        expected = (Fraction(1), Fraction(0), Fraction(4), Fraction(0))
        self.assertEqual(tuple(moment(MU_PLUS, k) for k in range(4)), expected)
        self.assertEqual(tuple(moment(MU_MINUS, k) for k in range(4)), expected)

    def test_central_window_gap(self):
        self.assertEqual(pairing(MU_PLUS, WINDOW), Fraction(3, 4))
        self.assertEqual(pairing(MU_MINUS, WINDOW), Fraction(0))

    def test_annihilator_kills_cubics(self):
        self.assertEqual([integer_moment(ANNIHILATOR, k) for k in range(4)], [0, 0, 0, 0])

    def test_sharp_dual_lower_bound(self):
        self.assertEqual(sum(abs(value) for value in ANNIHILATOR), 16)
        self.assertEqual(pairing(ANNIHILATOR, WINDOW), 6)
        self.assertEqual(pairing(ANNIHILATOR, WINDOW) / 16, Fraction(3, 8))

    def test_best_polynomial_equioscillates(self):
        residual = [Fraction(v) - best_polynomial_value(x) for x, v in zip(NODES, WINDOW)]
        self.assertEqual(residual, [Fraction(3, 8), Fraction(-3, 8), Fraction(3, 8), Fraction(-3, 8), Fraction(3, 8)])

    def test_serialized_certificate_contains_exact_radius(self):
        payload = build_certificate()
        self.assertEqual(payload["minimax"]["sharp_radius"], "3/8")
        self.assertTrue(payload["target"]["r_plus_h_is_prime"])


if __name__ == "__main__":
    unittest.main()
