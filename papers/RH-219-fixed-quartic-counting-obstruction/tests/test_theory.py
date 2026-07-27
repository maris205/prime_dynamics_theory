import numpy as np

from fixed_quartic import canonical_shape_roots, distinct_support_count, height_count, repeated_profile


def test_repetition_changes_multiplicity_not_support():
    roots = canonical_shape_roots(0.7, -0.1)
    rows = repeated_profile(roots, (1, 8, 32), np.asarray([0.0, 1.0]))
    assert [row["distinct_support_count"] for row in rows] == [4, 4, 4]
    assert rows[-1]["degree_counting_multiplicity"] == 128
    assert height_count(roots, 2.0, 32) == 128


def test_generic_quartet_has_four_distinct_roots():
    assert distinct_support_count(canonical_shape_roots(0.7, -0.1)) == 4
