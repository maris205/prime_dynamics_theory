import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import exact_weighted_diagnostics as diag


class ReferenceCertificateTests(unittest.TestCase):
    def test_reference_values_and_reconstructions(self):
        certificate = diag.build_certificate()
        diag.validate_certificate(certificate)
        self.assertEqual(certificate["modulus"], 385)
        self.assertEqual(certificate["kappa_h2"], "9/16")
        self.assertEqual(certificate["fixed_h2"]["weighted_target"], 362)
        self.assertEqual(certificate["fixed_h2"]["direct_box"], "-112/9")
        self.assertEqual(
            certificate["complete_shift"]["mean_square"], "2650976/1215"
        )

    def test_checked_json_matches_regeneration(self):
        checked = json.loads(
            Path("data/exact-certificate.json").read_text(encoding="utf-8")
        )
        self.assertEqual(checked, diag.build_certificate())

    def test_json_render_is_byte_deterministic(self):
        expected = json.dumps(diag.build_certificate(), indent=2, sort_keys=True) + "\n"
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "certificate.json"
            target.write_text(expected, encoding="utf-8", newline="\n")
            self.assertEqual(target.read_bytes(), expected.encode("utf-8"))


class ExactIdentityTests(unittest.TestCase):
    def setUp(self):
        self.a = diag.q_unit_coefficients(
            diag.interval(-8, 19), lambda n: (n % 5) - 2
        )
        self.b = diag.q_unit_coefficients(
            diag.interval(31, 17), lambda n: ((3 * n + 1) % 7) - 3
        )

    def test_fixed_conductor_sum_matches_direct_box(self):
        direct = diag.box_form(self.a, self.b, 2)
        reconstructed = sum(
            (
                diag.fixed_support_contribution(q, self.a, self.b, 2)
                for q in diag.nonempty_supports()
            ),
            Fraction(0),
        )
        self.assertEqual(direct, reconstructed)

    def test_complete_shift_parseval(self):
        direct = sum(
            (
                diag.box_form(self.a, self.b, 2 * ell) ** 2
                for ell in diag.units(diag.Q)
            ),
            Fraction(0),
        ) / len(diag.units(diag.Q))
        spectral = sum(
            (
                diag.exact_conductor_energy(q, self.a, self.b)
                for q in diag.nonempty_supports()
            ),
            Fraction(0),
        )
        self.assertEqual(direct, spectral)

    def test_exact_conductor_orthogonality_bound(self):
        energy = sum(value * value for value in self.a.values())
        for q in diag.nonempty_supports():
            moment = diag.second_character_energy(q, self.a)
            self.assertGreaterEqual(moment, 0)
            self.assertLessEqual(moment, (q + 19) * energy)

    def test_inactive_shift_is_rejected_by_conductor_formula(self):
        with self.assertRaises(ValueError):
            diag.fixed_support_contribution(5, self.a, self.b, 5)


if __name__ == "__main__":
    unittest.main()
