import math
import unittest

import numpy as np

from defect_shift_diagnostics import (
    all_shift_correlations,
    arithmetic_arrays,
    euler_phi,
    periodic_projection_energy,
    run_diagnostics,
    truncated_source_weight,
)


class ArithmeticArrayTests(unittest.TestCase):
    def test_mobius_and_von_mangoldt(self):
        mu, lam, primes = arithmetic_arrays(50)
        self.assertEqual(mu[1:11].tolist(), [1, -1, -1, 0, -1, 1, -1, 0, 0, 1])
        self.assertAlmostEqual(lam[2], math.log(2))
        self.assertAlmostEqual(lam[4], math.log(2))
        self.assertEqual(lam[6], 0.0)
        self.assertIn(47, primes.tolist())

    def test_truncated_source_identity_at_full_cutoff(self):
        x = 40
        length = 100
        mu, lam, _ = arithmetic_arrays(length - 1)
        short = truncated_source_weight(mu, x, 2 * x, length)
        np.testing.assert_allclose(
            short[x + 1 : 2 * x + 1],
            lam[x + 1 : 2 * x + 1],
            atol=1e-12,
        )


class CorrelationTests(unittest.TestCase):
    def test_fft_matches_direct(self):
        f = np.zeros(32)
        g = np.zeros(32)
        f[5:12] = np.arange(1.0, 8.0)
        g[3:20] = np.arange(2.0, 19.0)
        values = all_shift_correlations(f, g, 7)
        direct = np.array([np.dot(f[:-h], g[h:]) for h in range(1, 8)])
        np.testing.assert_allclose(values, direct, atol=1e-10)

    def test_periodic_projection_constant_case(self):
        values = np.ones(12)
        energy = periodic_projection_energy(values, 1, 5)
        self.assertAlmostEqual(energy, 12.0)

    def test_small_shift_and_generator_inputs(self):
        payload = run_diagnostics(
            128,
            5,
            (theta for theta in [0.25]),
            (q for q in [2, 6]),
        )
        self.assertEqual(payload["parameters"]["cutoff_exponents"], [0.25])
        self.assertEqual(payload["parameters"]["moduli"], [2, 6])
        self.assertEqual(len(payload["shift_defect"]), 1)
        self.assertEqual([row["q"] for row in payload["periodic_energy"]], [2, 6])

    def test_euler_phi(self):
        self.assertEqual(euler_phi(1), 1)
        self.assertEqual(euler_phi(30), 8)
        self.assertEqual(euler_phi(2310), 480)


if __name__ == "__main__":
    unittest.main()
