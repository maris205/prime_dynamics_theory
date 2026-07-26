from cycle_riesz import cycle_shell_budget, root_half_spacing


def test_root_half_spacing():
    assert abs(root_half_spacing(6, 2.0) - 1.0) < 1e-14


def test_explicit_budget():
    budget = cycle_shell_budget(8, 1.0, 0.1, 0.02, 2.0, 0.1, 0.1)
    assert budget["geometry_admissible"]
    assert budget["packet_admissible"]
    assert budget["directed_schur_product"] < 1.0
    assert budget["certificate_admissible"]
