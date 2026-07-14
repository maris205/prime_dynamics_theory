"""Unit tests for the deterministic TPC-13 certificate."""

from __future__ import annotations

import unittest

from experiments.radial_mellin_certificate import build_certificate


class RadialMellinCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = build_certificate(X=240, D=7, h=3)

    def test_coordinate_bijection_and_transform(self) -> None:
        self.assertTrue(self.certificate["checks"]["coordinate_bijection"])
        self.assertTrue(
            self.certificate["checks"]["joint_transform_compression"]
        )

    def test_sector_gaps(self) -> None:
        self.assertTrue(self.certificate["checks"]["explicit_sector_gaps"])

    def test_tensor_fejer_identities(self) -> None:
        self.assertTrue(self.certificate["checks"]["tensor_fejer_parseval"])
        self.assertTrue(self.certificate["checks"]["tensor_fejer_recovery"])

    def test_product_center_identity(self) -> None:
        self.assertTrue(self.certificate["checks"]["product_center_identity"])

    def test_energy_minimax_witness(self) -> None:
        self.assertTrue(self.certificate["checks"]["energy_minimax_witness"])


if __name__ == "__main__":
    unittest.main()
