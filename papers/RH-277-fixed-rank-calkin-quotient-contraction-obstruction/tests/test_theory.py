from calkin_no_go import fixed_rank_contour_compatible, hardy_lower


def test_hardy_lower_is_superunit():
    assert hardy_lower(1) > 1
    assert hardy_lower(12) > hardy_lower(1)


def test_rank_change_breaks_single_fixed_rank_contour():
    assert fixed_rank_contour_compatible([6, 6, 6])
    assert not fixed_rank_contour_compatible([6, 8])
