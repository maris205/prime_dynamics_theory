from triple_ledger import complete_count, coordinatewise_union, score


def test_two_scores_four_but_no_complete_branch():
    spectral = (True, False, True, True, True)
    counterloop = (True, True, False, True, True)
    assert score(spectral) == score(counterloop) == 4
    assert complete_count([spectral, counterloop]) == 0


def test_coordinatewise_union_is_all_true_but_typed_glue_is_external():
    union = coordinatewise_union(
        (True, False, True, True, True),
        (True, True, False, True, True),
    )
    assert all(union)
