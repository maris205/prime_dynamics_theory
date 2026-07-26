import pytest

from r_interface_frontier import physical_r_frontier, physical_r_status


def test_current_frontier():
    statuses = {leaf: "open" for leaf in ("X_phys", "D_phys", "K_phys", "H_phys")}
    assert physical_r_frontier(statuses) == (frozenset(statuses),)
    assert physical_r_status(statuses) == "open"


def test_closed_frontier():
    statuses = {leaf: "proved" for leaf in ("X_phys", "D_phys", "K_phys", "H_phys")}
    assert physical_r_frontier(statuses) == (frozenset(),)
    assert physical_r_status(statuses) == "proved"


def test_no_go_rejects_branch():
    statuses = {leaf: "proved" for leaf in ("X_phys", "D_phys", "K_phys", "H_phys")}
    statuses["X_phys"] = "no_go"
    assert physical_r_frontier(statuses) == ()
    assert physical_r_status(statuses) == "branch_rejected"


def test_invalid_status():
    statuses = {leaf: "open" for leaf in ("X_phys", "D_phys", "K_phys", "H_phys")}
    statuses["D_phys"] = "maybe"
    with pytest.raises(ValueError):
        physical_r_frontier(statuses)
