from shell_stability import minimal_shell_completion_rank, shell_completion_is_minimal


def test_minimal_completion_can_overshoot_by_one():
    assert minimal_shell_completion_rank([2, 1, 2, 2], 4) == 5
    assert shell_completion_is_minimal([2, 1, 2, 2], 4)


def test_exact_target_when_shell_boundary_agrees():
    assert minimal_shell_completion_rank([2, 2, 1], 4) == 4
    assert shell_completion_is_minimal([2, 2, 1], 4)
