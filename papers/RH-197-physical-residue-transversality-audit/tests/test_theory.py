from physical_transversality import conditioning_ratio, normalized_residue_condition, optimal_packet_condition, summarize


def test_condition_and_summary_helpers():
    assert optimal_packet_condition(0.25) == 4.0
    assert conditioning_ratio(4.2, 4.0) == 1.05
    assert normalized_residue_condition(0.02) == 50.0
    assert summarize([1.0, 2.0, 7.0]) == {"minimum": 1.0, "median": 2.0, "maximum": 7.0}
