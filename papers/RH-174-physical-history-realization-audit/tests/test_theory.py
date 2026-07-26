from history_audit import metric_summary, threshold_count


def test_metric_reducers():
    rows = [{"x": 3.0}, {"x": 1.0}, {"x": 2.0}]
    assert metric_summary(rows, "x") == {"minimum": 1.0, "median": 2.0, "maximum": 3.0}
    assert threshold_count(rows, "x", 2.0) == 2
