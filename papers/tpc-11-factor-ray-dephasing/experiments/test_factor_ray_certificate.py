import math
import unittest
from fractions import Fraction

from experiments.factor_ray_certificate import (
    build_certificate,
    compress_rays,
    direct_transform,
    endpoint_geometry,
    prime_power_base,
    ray_spacing,
    ray_transform,
    supported_pairs,
)


class FactorRayCertificateTests(unittest.TestCase):
    def test_prime_power_classifier(self) -> None:
        expected = {2: 2, 3: 3, 4: 2, 8: 2, 9: 3, 25: 5, 49: 7}
        for n, p in expected.items():
            self.assertEqual(prime_power_base(n), p)
        for n in (1, 6, 10, 12, 18, 45):
            self.assertIsNone(prime_power_base(n))

    def test_unique_fraction_compression(self) -> None:
        rows = supported_pairs(X=36, D=2, h=2, alpha=0.75, beta=2.25)
        rays = compress_rays(rows)
        self.assertTrue(all(isinstance(ray, Fraction) for ray in rays))
        for t in (0.0, 0.2, 1.0, 3.0):
            self.assertAlmostEqual(
                abs(direct_transform(rows, t) - ray_transform(rays, t)),
                0.0,
                places=10,
            )

    def test_hyperbolic_spacing(self) -> None:
        X, beta = 36, 2.25
        rows = supported_pairs(X=X, D=2, h=2, alpha=0.75, beta=beta)
        result = ray_spacing(compress_rays(rows), beta, X)
        self.assertTrue(result["bound_verified"])
        self.assertGreaterEqual(
            result["observed_min_gap"], result["theoretical_delta_X"] - 1e-14
        )

    def test_endpoint_geometry(self) -> None:
        X, D, alpha, beta = 36, 2, 0.75, 2.25
        rows = supported_pairs(X=X, D=D, h=2, alpha=alpha, beta=beta)
        endpoint = endpoint_geometry(rows, X, D, alpha, beta)
        self.assertTrue(endpoint["selector_verified"])
        self.assertLess(beta, 4.0 * alpha)
        self.assertLess(D, alpha * X)

    def test_complete_certificate(self) -> None:
        result = build_certificate(X=36, D=2, h=2, alpha=0.75, beta=2.25)
        self.assertTrue(result["all_checks_passed"])
        counts = [
            row["support_allowed_ordered_off_diagonal_pairs"]
            for row in result["determinant_layers"]
        ]
        self.assertTrue(all(a >= b for a, b in zip(counts, counts[1:])))
        self.assertTrue(
            all(row["determinant_bound_verified"] for row in result["determinant_layers"])
        )
        self.assertTrue(math.isfinite(result["hard_band"]["pair_form"]))


if __name__ == "__main__":
    unittest.main()
