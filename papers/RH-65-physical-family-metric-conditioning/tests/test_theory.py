import mpmath as mp
import pytest

from metric_conditioning import (
    contraction_horizon,
    exact_two_step_metric,
    jordan_chain,
    lyapunov_metric,
    lyapunov_residual,
    max_abs_entry,
    metric_ledger,
    theoretical_exponents,
)


def test_exact_two_step_formula_matches_vectorized_solution() -> None:
    with mp.workdps(80):
        operator = jordan_chain(2, "0.01", "0.2")
        exact = exact_two_step_metric("0.01", "0.2")
        computed = lyapunov_metric(operator)
        assert max_abs_entry(exact - computed) < mp.mpf("1e-65")
        assert max_abs_entry(lyapunov_residual(operator, exact)) < mp.mpf(
            "1e-65"
        )


def test_metric_contraction_identity_is_exact_numerically() -> None:
    ledger = metric_ledger(3, "0.001", "0.05", dps=90)
    assert abs(
        ledger.contraction**2 - (1 - 1 / ledger.lambda_max)
    ) < mp.mpf("1e-75")


def test_matched_coupling_has_bounded_conditioning() -> None:
    ledger = metric_ledger(4, "1e-5", "2e-6", dps=100)
    assert ledger.condition_number < 2
    assert mp.mpf("0.3") < ledger.contraction_gap / ledger.gap < mp.mpf(
        "0.4"
    )


def test_fixed_coupling_exhibits_d4_power_barrier() -> None:
    coarse = metric_ledger(4, "1e-3", "0.2", dps=110)
    fine = metric_ledger(4, "1e-4", "0.2", dps=110)
    condition_ratio = fine.condition_number / coarse.condition_number
    gap_ratio = coarse.contraction_gap / fine.contraction_gap
    assert mp.mpf("9e5") < condition_ratio < mp.mpf("1.1e6")
    assert mp.mpf("9e6") < gap_ratio < mp.mpf("1.1e7")


def test_theoretical_exponents_and_horizon() -> None:
    assert theoretical_exponents(4, 0.5) == pytest.approx((3.0, 4.0))
    assert theoretical_exponents(4, 1.0) == pytest.approx((0.0, 1.0))
    assert contraction_horizon("0.9", "0.01") == 44


@pytest.mark.parametrize(
    "call",
    [
        lambda: jordan_chain(0, "0.1", "0.2"),
        lambda: jordan_chain(2, "1.0", "0.2"),
        lambda: jordan_chain(2, "0.1", "-0.2"),
        lambda: metric_ledger(2, "0.1", "0.2", dps=20),
        lambda: contraction_horizon("1.0", "0.1"),
        lambda: theoretical_exponents(2, -1.0),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
