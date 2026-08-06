from distance_capacity import (
    ENDPOINT,
    PERIOD_WORDS,
    capacity_from_formula,
    cyclic_pair_ledger,
    dp_capacity,
    mobius_prefix,
    open_pair_ledger,
    periodic_capacity,
    polynomial_certificate,
)


def test_eight_run_formula_matches_path_dp() -> None:
    mu = mobius_prefix(1024)
    for limit in range(1, 257):
        formula = capacity_from_formula(mu, limit)
        dynamic = dp_capacity(mu, limit)
        for key in ("M_N", "W_plus", "W_minus", "maximum", "minimum", "K_N"):
            assert formula[key] == dynamic[key]


def test_frozen_endpoint() -> None:
    mu = mobius_prefix(ENDPOINT)
    result = capacity_from_formula(mu, ENDPOINT)
    assert result["M_N"] == 257
    assert result["W_plus"] == 258120
    assert result["W_minus"] == 257953
    assert result["K_N"] == 516163


def test_periodic_ledger_and_capacity_obstruction() -> None:
    u = PERIOD_WORDS["u"]
    v = PERIOD_WORDS["v"]
    assert cyclic_pair_ledger(u) == cyclic_pair_ledger(v)
    assert open_pair_ledger(u, 2) != open_pair_ledger(v, 2)
    assert [periodic_capacity(u, q)["K_N"] for q in range(1, 17)] == [10 * q for q in range(1, 17)]
    assert [periodic_capacity(v, q)["K_N"] for q in range(1, 17)] == [12 * q for q in range(1, 17)]
    assert polynomial_certificate()
