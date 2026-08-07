from shift_two_chowla import (
    ENDPOINT,
    mobius_prefix,
    pointwise_terms,
    verify_certificate,
)


def test_small_mobius_prefix():
    mu = mobius_prefix(12)
    assert mu[1:] == [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]


def test_boolean_identity_on_all_ternary_pairs():
    for left in (-1, 0, 1):
        for right in (-1, 0, 1):
            row = pointwise_terms(left, right)
            assert 4 * row["C_plus"] == row["Q2"] + row["U2"] + row["V2"] + row["D2"]
            assert 4 * row["C_minus"] == row["Q2"] - row["U2"] - row["V2"] + row["D2"]


def test_full_prefix_certificate():
    result = verify_certificate()
    assert result["all_pass"]
    assert result["endpoint"] == ENDPOINT
    assert result["pointwise_identity_count"] == ENDPOINT - 2
    assert result["cumulative_prefix_count"] == ENDPOINT


def test_even_start_and_rh371_alignment():
    result = verify_certificate()
    assert result["even_start_count"] == 524287
    assert result["even_start_zero_pass"]
    assert result["rh371_alignment_prefix_count"] == 1024
    assert result["rh371_alignment_sign_cells"] == 2048
    assert result["rh371_alignment_pass"]


def test_frozen_rows():
    rows = verify_certificate()["frozen_rows"]
    assert rows["1024"] == {"C_plus": 66, "C_minus": 82, "Q2": 330, "U2": -18, "V2": -14, "D2": -34}
    assert rows["65536"] == {"C_plus": 5293, "C_minus": 5301, "Q2": 21155, "U2": -51, "V2": 35, "D2": 33}
    assert rows["1048576"] == {"C_plus": 84630, "C_minus": 84346, "Q2": 338334, "U2": 130, "V2": 438, "D2": -382}
