"""Fast, zero-dependency tests; directly executable and pytest-compatible."""

from __future__ import annotations

import json
import tempfile
from fractions import Fraction
from pathlib import Path

import exact_transfer_certificate as exact


DATA_PATH = Path(__file__).resolve().parent / "data" / "exact-certificate.json"


def test_reference_certificate_validates_and_matches_json() -> None:
    certificate = exact.build_certificate()
    exact.validate_certificate(certificate)
    checked = json.loads(DATA_PATH.read_text("utf-8"))
    assert checked == certificate
    assert checked["normalization"]["kappa"] == "9/16"
    assert checked["normalization"]["survivors_per_row"] == 135


def test_reference_json_is_byte_deterministic() -> None:
    certificate = exact.build_certificate()
    expected = exact.render_certificate(certificate)
    assert DATA_PATH.read_bytes() == expected
    with tempfile.TemporaryDirectory() as directory:
        regenerated = Path(directory) / "exact-certificate.json"
        exact.write_certificate(regenerated)
        assert regenerated.read_bytes() == expected


def test_involutions_and_spectrum_counts() -> None:
    for divisor in exact.squarefree_divisors(exact.PRIMES):
        record = exact.involution_record(divisor)
        assert record["plus_eigenspace_dimension"] + record[
            "minus_eigenspace_dimension"
        ] == record["group_size"]
        for value in exact.units(divisor):
            image = exact.arithmetic_involution(value, divisor)
            assert exact.arithmetic_involution(image, divisor) == value


def test_bundle_reconstruction_on_all_rows() -> None:
    beta = exact.deterministic_beta(exact.Q)
    for m in exact.units(exact.Q):
        assert exact.transfer_average(beta, m, exact.Q) == exact.involution_bundle_average(
            beta, m, exact.Q
        )


def test_pointwise_survivor_inclusion_exclusion() -> None:
    for m in exact.units(exact.Q):
        for residue in exact.units(exact.Q):
            left, right = exact.survivor_inclusion_exclusion(
                m, residue, exact.Q
            )
            assert left == right


def test_all_quadratic_mode_multipliers() -> None:
    for conductor in exact.squarefree_divisors(exact.PRIMES):
        beta = exact.quadratic_mode(exact.Q, conductor)
        for m in exact.units(exact.Q):
            observed = exact.transfer_residue_sum(beta, m, exact.Q)
            predicted = exact.predicted_quadratic_residue_sum(
                m, exact.Q, conductor
            )
            assert observed == predicted
        record = exact.mode_record(exact.Q, conductor)
        expected_abs = Fraction(
            1,
            __import__("math").prod(
                prime - 2 for prime in exact.squarefree_primes(conductor)
            ),
        )
        assert record["normalized_multiplier_absolute_value"] == exact.fraction_text(
            expected_abs
        )


def test_exact_integer_and_formal_lambda_reindexing() -> None:
    record = exact.exact_progression_record()
    assert record["integer_reindexing_exact"] is True
    assert record["formal_lambda_reindexing_exact"] is True
    assert record["formal_lambda_nonzero_coefficients"] > 0


def _run_directly() -> None:
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    _run_directly()
