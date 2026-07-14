"""Unit tests for the TPC-16 finite certificate."""

from __future__ import annotations

import unittest

from experiments.square_root_gate_certificate import build_certificate, canonical_digest


class SquareRootGateCertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = build_certificate()

    def test_complete_period_means(self) -> None:
        self.assertTrue(all(item["mean_ok"] for item in self.payload["row_checks"]))

    def test_drift_tail_identity(self) -> None:
        self.assertTrue(all(item["tail_ok"] for item in self.payload["row_checks"]))

    def test_asymmetric_vaughan_identity(self) -> None:
        self.assertLess(max(item["error"] for item in self.payload["vaughan_errors"]), 1e-10)

    def test_hyperbolic_peeling(self) -> None:
        self.assertTrue(self.payload["peeling_all_exact"])

    def test_simplified_wedge_drift(self) -> None:
        self.assertTrue(all(item["ok"] for item in self.payload["simplified_drift_checks"]))

    def test_exponent_ledger(self) -> None:
        self.assertTrue(self.payload["exponent_ledger_ok"])

    def test_cross_spectrum_convention(self) -> None:
        self.assertLess(self.payload["cross_spectrum_max_error"], 1e-10)

    def test_payload_hash(self) -> None:
        payload_without_hash = dict(self.payload)
        digest = payload_without_hash.pop("sha256")
        self.assertEqual(digest, canonical_digest(payload_without_hash))


if __name__ == "__main__":
    unittest.main()
