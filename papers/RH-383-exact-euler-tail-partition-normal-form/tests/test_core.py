"""Core exact-arithmetic tests for RH-383."""

from fractions import Fraction

import pytest

from euler_tail_normal_form import (
    ALL_PARTITIONS,
    DIRECT_CASES,
    EXPECTED_COUNTS,
    REMAINDER_MAJORANT_PI2,
    af_gamma_vector,
    build_certificate,
    cw_gamma_vector,
    endpoint_normal_form_pi2,
    finite_gap_pi2,
    remainder_bound_pi2_from_rho,
    require_truncation_degree,
)


def test_frozen_grids() -> None:
    assert len(ALL_PARTITIONS) == 271
    assert len(DIRECT_CASES) == 67
    assert EXPECTED_COUNTS["remainder"] == 67 * 12
    assert REMAINDER_MAJORANT_PI2 == Fraction(92, 3) < 31


def test_partition_compilers_agree() -> None:
    for partition in ALL_PARTITIONS:
        assert cw_gamma_vector(partition) == af_gamma_vector(partition)
        assert cw_gamma_vector(partition)[2] == 0


def test_endpoint_normal_form() -> None:
    for start, endpoint in DIRECT_CASES:
        assert finite_gap_pi2(start, endpoint) == endpoint_normal_form_pi2(start, endpoint)


@pytest.mark.parametrize("bad", [True, False, 1.0, 2.0, 0, -1])
def test_truncation_degree_fails_closed(bad: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        require_truncation_degree(bad)  # type: ignore[arg-type]


def test_rho_domain_fails_closed() -> None:
    assert remainder_bound_pi2_from_rho(Fraction(7, 8), 1) == Fraction(92, 3) * Fraction(7, 8) ** 2
    for bad in (36, Fraction(36), True, 0.5):
        with pytest.raises((TypeError, ValueError)):
            remainder_bound_pi2_from_rho(bad, 1)  # type: ignore[arg-type]


def test_full_certificate() -> None:
    certificate = build_certificate()
    assert certificate["all_pass"] is True
    assert certificate["sections"]["negative_mutations"]["count"] == 20
    assert certificate["sections"]["negative_mutations"]["rejected"] == 20
