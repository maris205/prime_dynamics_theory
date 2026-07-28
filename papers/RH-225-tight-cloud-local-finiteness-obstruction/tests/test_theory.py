from divisor_obstruction import divisor_mass_diverges, tightness_count_lower


def test_tightness_count_lower():
    assert tightness_count_lower(20, 0.25) == 15
    assert tightness_count_lower(21, 0.25) == 16


def test_strict_rank_growth_forces_compact_mass_growth_at_fixed_epsilon():
    assert divisor_mass_diverges([4, 6, 9, 12], 0.25)
