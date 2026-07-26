from clock_cycle_calibration import cycle_clock_translation, possible_gap_values


def test_exact_integer_translation():
    record = cycle_clock_translation(4.445622727523028, 3)
    assert record["clock_rank"] == 7
    assert record["cycle_length"] == 4
    assert record["rank_cycle_gap"] == 3
    assert record["translated_rank_cycle_gap"] == 3


def test_defect_corridor_maps_to_two_gaps():
    assert possible_gap_values(1.4, 2.4) == (3, 4)
