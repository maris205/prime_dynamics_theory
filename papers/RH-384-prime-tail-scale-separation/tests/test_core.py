"""Exact algebra, directed interval, and mutation tests for RH-384."""

from decimal import Clamped, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Underflow, localcontext
from fractions import Fraction

import pytest

from prime_tail_scales import (
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_SHA256,
    canonical_json_bytes,
    fixed_r_rows,
    gap_limit_rows,
    negative_mutation_rows,
    numeric_interval_certificate,
    partition_rows,
    payload_sha256,
    successor_rows,
    verify_certificate,
)
from prime_tail_scales.core import scale_separation_ledger, validate_pnt_provenance


def test_fixed_r_and_partition_compilers_are_algebraic() -> None:
    fixed = fixed_r_rows()
    assert len(fixed) == 8
    for row in fixed:
        r = row["r"]
        assert row["constant"] == str(Fraction(1, 2 * r - 1))
        assert row["p_exponent"] == 2 * r - 1
        assert row["log_exponent"] == 1

    partitions = partition_rows()
    assert len(partitions) == 66
    assert {row["degree"] for row in partitions} == set(range(1, 9))
    for row in partitions:
        parts = row["partition"]
        constant = Fraction(1)
        for part in parts:
            constant *= Fraction(1, 2 * part - 1)
        assert row["constant"] == str(constant)
        assert row["p_exponent"] == sum(2 * part - 1 for part in parts)
        assert row["p_exponent"] == 2 * row["degree"] - row["length"]
        assert row["log_exponent"] == row["length"]


def test_48_strict_successor_rows_are_exact_interface_checks() -> None:
    rows = successor_rows()
    assert len(rows) == 48
    assert {(row["r"], row["y"]) for row in rows} == {
        (r, y) for r in range(1, 9) for y in (1, 2, 3, 5, 8, 13)
    }
    for row in rows:
        assert Fraction(row["lhs"]) == Fraction(row["first_atom"]) + Fraction(row["successor_tail"])
        assert row["first_tail_prime"] > row["p_y"]
        assert row["inclusive_interface_mutation_rejected"]
        assert "do not change the leading PNT equivalent" in row["asymptotic_note"]


def test_scale_and_gap_ledgers_reconstruct_constants_and_exact_subtractions() -> None:
    scales = scale_separation_ledger()
    assert len(scales) == 5 and all(row["pass"] for row in scales)
    assert scales[0]["derived_constant"] == "1"
    assert scales[1]["derived_constant"] == "1"
    assert scales[4]["derived_constant"] == "1/3"
    assert scales[2]["derived_equivalent"] == "log(p_y)/(3*p_y)"
    assert scales[3]["derived_equivalent"] == "3/log(p_y)^2"

    limits = gap_limit_rows()
    assert len(limits) == 5 and all(row["pass"] for row in limits)
    assert limits[1]["exact_subtraction"] == ["A*T_y"]
    assert limits[1]["pnt_surrogates_forbidden"] == ["A/[p_y*log(p_y)]"]
    assert limits[2]["exact_subtraction"] == ["A*T_y", "B*T_y^2"]
    assert limits[2]["pnt_surrogates_forbidden"] == [
        "A/[p_y*log(p_y)]",
        "B/[p_y^2*log(p_y)^2]",
    ]
    assert [row["limit"] for row in limits] == ["A", "B", "C", "C", "C/3"]


def test_precision_80_interval_and_ten_numeric_rows() -> None:
    interval = numeric_interval_certificate()
    assert interval["all_pass"] and interval["numeric_row_count"] == 10
    assert interval["cutoff_anchor"] == 100000
    assert interval["last_prime_at_or_below_cutoff"] == 99991
    assert interval["first_prime_above_cutoff"] == 100003
    assert interval["odd_prime_count"] == 9591
    assert interval["tail_integer_bound"] == "200001/20000200000"
    assert interval["published_lower"] == "1.5463476716710499204"
    assert interval["published_upper"] == "1.5484488989771761113"
    assert interval["raw_lower"].startswith("1.5463476716710499204067249985")
    assert interval["raw_upper"].startswith("1.5484488989771761112886457157")
    assert [row["m"] for row in interval["u_intervals"]] == list(range(2, 9))
    theta = Fraction(interval["tail_integer_bound"])
    for row in interval["u_intervals"]:
        assert Fraction(row["tail_loss_upper"]) >= (row["m"] - 1) * theta
        assert Fraction(row["tail_factor_lower"]) <= 1 - (row["m"] - 1) * theta
    assert [row["name"] for row in interval["derived_intervals"]] == [
        "Y_infinity",
        "m_infinity",
        "Y_infinity-2m_infinity",
    ]


def test_hostile_ambient_decimal_contexts_do_not_change_certificate() -> None:
    baseline = canonical_json_bytes(verify_certificate())
    with localcontext() as ambient:
        for precision, rounding in ((7, ROUND_FLOOR), (29, ROUND_CEILING), (113, ROUND_HALF_EVEN)):
            ambient.prec = precision
            ambient.rounding = rounding
            ambient.Emin = -5
            ambient.Emax = 5
            ambient.traps[Underflow] = True
            ambient.traps[Clamped] = True
            assert canonical_json_bytes(verify_certificate()) == baseline


def test_certificate_fixture_and_20_genuine_mutations() -> None:
    certificate = verify_certificate()
    assert certificate["all_pass"]
    assert len(canonical_json_bytes(certificate)) == CERTIFICATE_FIXTURE_BYTES == 48689
    assert payload_sha256(certificate) == CERTIFICATE_FIXTURE_SHA256
    mutations = negative_mutation_rows()
    assert len(mutations) == 20
    assert all(row["rejected"] is True for row in mutations)
    assert sum(row["category"] == "interface" for row in mutations) == 2
    assert "not leading-asymptotic counterexamples" in certificate["negative_mutations"]["endpoint_asymptotic_disclosure"]


def test_real_provenance_flips_fail_the_validator() -> None:
    assert validate_pnt_provenance()
    cases = (
        {"release": "0" * 40},
        {"main_sha256": "0" * 64},
        {"references_sha256": "0" * 64},
        {"doi": "10.0000/wrong"},
    )
    for case in cases:
        with pytest.raises(ValueError):
            validate_pnt_provenance(**case)
