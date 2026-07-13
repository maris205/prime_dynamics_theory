import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import exact_defect_certificate as defect


class ReferenceCertificateTests(unittest.TestCase):
    def test_reference_certificate_validates(self):
        certificate = defect.build_certificate()
        defect.validate_certificate(certificate)
        self.assertEqual(certificate["modulus"], 385)
        self.assertEqual(certificate["normalization"]["kappa"], "9/16")
        self.assertEqual(
            certificate["normalization"]["survivor_centered_kernel"], "7/9"
        )

    def test_checked_json_matches_exact_object(self):
        checked = json.loads(
            Path("data/exact-certificate.json").read_text(encoding="utf-8")
        )
        self.assertEqual(checked, defect.build_certificate())

    def test_checked_json_is_byte_for_byte_regenerable(self):
        expected = defect.render_certificate(defect.build_certificate())
        checked = Path("data/exact-certificate.json").read_bytes()
        self.assertEqual(checked, expected)
        with tempfile.TemporaryDirectory() as directory:
            regenerated = Path(directory) / "exact-certificate.json"
            defect.write_certificate(regenerated)
            self.assertEqual(regenerated.read_bytes(), checked)


class ExactArithmeticTests(unittest.TestCase):
    def test_targets_and_factorizations(self):
        self.assertEqual(defect.SQUARE_TARGET, 148996)
        self.assertEqual(defect.PRIME_TARGET, 149381)
        self.assertEqual(defect.factor_integer(defect.SQUARE_TARGET), {2: 2, 193: 2})
        self.assertEqual(defect.factor_integer(defect.PRIME_TARGET), {149381: 1})
        self.assertFalse(defect.is_prime(defect.SQUARE_TARGET))
        self.assertTrue(defect.is_prime(defect.PRIME_TARGET))

    def test_lucas_primality_certificate(self):
        certificate = defect.lucas_certificate(
            defect.PRIME_TARGET, defect.LUCAS_WITNESS
        )
        defect.validate_lucas_certificate(certificate)
        self.assertEqual(
            certificate["n_minus_1_factorization"],
            {"2": 2, "5": 1, "7": 1, "11": 1, "97": 1},
        )
        self.assertEqual(certificate["fermat_residue"], 1)
        self.assertTrue(
            all(
                check["gcd_residue_minus_one_with_n"] == 1
                for check in certificate["prime_divisor_checks"].values()
            )
        )

    def test_same_residue_pushforward_and_local_signatures(self):
        square_pair = (1, defect.SQUARE_TARGET - defect.SHIFT)
        prime_pair = (1, defect.PRIME_TARGET - defect.SHIFT)
        self.assertEqual(defect.residue_cell(*square_pair), (1, 384))
        self.assertEqual(defect.residue_cell(*square_pair), defect.residue_cell(*prime_pair))
        expected = {5: (1, 4, 1), 7: (1, 6, 1), 11: (1, 10, 1)}
        self.assertEqual(
            {
                p: defect.local_signature(*square_pair, defect.SHIFT, p)
                for p in defect.PRIMES
            },
            expected,
        )
        self.assertEqual(
            {
                p: defect.local_signature(*prime_pair, defect.SHIFT, p)
                for p in defect.PRIMES
            },
            expected,
        )

    def test_exact_centered_kernel(self):
        self.assertEqual(defect.kappa(defect.SHIFT), Fraction(9, 16))
        square_value = defect.centered_kernel(1, defect.SQUARE_TARGET - defect.SHIFT)
        prime_value = defect.centered_kernel(1, defect.PRIME_TARGET - defect.SHIFT)
        self.assertEqual(square_value, Fraction(7, 9))
        self.assertEqual(prime_value, square_value)

    def test_prime_and_liouville_functional_gaps(self):
        certificate = defect.build_certificate()["defect_linear_algebra"]
        self.assertEqual(certificate["local_pushforward_pairing"], 0)
        self.assertEqual(certificate["prime_functional"]["null_vector_pairing"], -1)
        self.assertEqual(
            certificate["prime_functional"]["minimax_absolute_error_lower_bound"],
            "1/2",
        )
        self.assertEqual(certificate["liouville_functional"]["null_vector_pairing"], 2)
        self.assertEqual(
            certificate["liouville_functional"]["minimax_absolute_error_lower_bound"],
            "1",
        )
        self.assertEqual(defect.liouville(defect.SQUARE_TARGET), 1)
        self.assertEqual(defect.liouville(defect.PRIME_TARGET), -1)


if __name__ == "__main__":
    unittest.main()
