"""Unit tests for the deterministic TPC-12 certificate."""

from __future__ import annotations

import unittest

from experiments.short_shift_certificate import build_certificate


class ShortShiftCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = build_certificate(X=240, D=7, h=3)

    def test_ray_compression(self) -> None:
        self.assertTrue(self.certificate["checks"]["ray_compression"])

    def test_source_regrouping_and_transfer(self) -> None:
        self.assertTrue(self.certificate["checks"]["source_diagonal_regrouping"])
        self.assertTrue(self.certificate["checks"]["finite_exceptional_transfer"])

    def test_sign_coherent_ray(self) -> None:
        self.assertTrue(self.certificate["checks"]["sign_coherent_identity"])

    def test_quadratic_embedding(self) -> None:
        self.assertTrue(self.certificate["checks"]["quadratic_embedding_identity"])

    def test_radial_minimax(self) -> None:
        self.assertTrue(self.certificate["checks"]["radial_minimax_l2"])


if __name__ == "__main__":
    unittest.main()
