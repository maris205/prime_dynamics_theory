from decimal import ROUND_DOWN, ROUND_UP, getcontext, localcontext
from fractions import Fraction
import os
from pathlib import Path
import subprocess
import sys

import pytest

from two_scale_tail import (
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_SHA256,
    MEMORY_CHANNEL_CONSTANT,
    M_LIPSCHITZ_CONSTANT,
    PUBLISHED_REMAINDER_CONSTANT,
    TOTAL_REMAINDER_CONSTANT,
    X_CHANNEL_CONSTANT,
    X_QUADRATIC_CONSTANT,
    canonical_json_bytes,
    coefficient_ledger,
    exact_tail_algebra,
    finite_euler_values,
    finite_gap_row,
    normalized_memory,
    one_tail_sign_mutation,
    payload_sha256,
    product_expansion_row,
    square_run_counts,
    tail_weights,
    terminal_ledger,
    verify_certificate,
)


ROOT = Path(__file__).resolve().parents[1]


def test_exact_constant_ledger_is_931_4_63_and_3301_6() -> None:
    ledger = coefficient_ledger()
    assert X_QUADRATIC_CONSTANT == Fraction(931, 4)
    assert M_LIPSCHITZ_CONSTANT == 63
    assert X_CHANNEL_CONSTANT == Fraction(931, 2)
    assert MEMORY_CHANNEL_CONSTANT == Fraction(254, 3)
    assert TOTAL_REMAINDER_CONSTANT == Fraction(3301, 6)
    assert TOTAL_REMAINDER_CONSTANT < PUBLISHED_REMAINDER_CONSTANT == 551
    assert ledger["x_quadratic_total"] == "931/4"
    assert ledger["memory_lipschitz_total"] == "63"
    assert ledger["x_channel"] == "931/2"
    assert ledger["memory_channel"] == "254/3"
    assert ledger["total"] == "3301/6"
    assert ledger["strict_margin"] == "5/6"
    assert ledger["all_pass"]


def test_product_expansion_uses_all_order_inequalities() -> None:
    for m in range(3, 9):
        row = product_expansion_row(m, 1, 19)
        assert row["ratio_identity_pass"]
        assert row["P_le_inverse_pass"]
        assert row["delta_le_x_pass"]
        assert row["quadratic_remainder_pass"]
        assert row["all_pass"]


def test_memory_limit_and_terminal_E9_are_exact() -> None:
    for y in (1, 2, 3, 6, 19):
        value = normalized_memory(y)
        assert Fraction(0) <= value <= Fraction(1)
        assert finite_euler_values(y)[9] == 0
    terminal = terminal_ledger()
    assert terminal["E10_constructed"] is False
    assert terminal["all_pass"]
    assert all(row["E9"] == "0" for row in terminal["rows"])
    assert square_run_counts(1)[8] == 1


def test_tail_and_cube_telescopes_are_exact() -> None:
    row = exact_tail_algebra(tail_weights(1, 19))
    assert row["current_identity_pass"]
    assert row["next_identity_pass"]
    assert row["cross_cube_identity_pass"]
    assert row["right_square_cube_bound_pass"]
    assert row["left_square_cube_bound_pass"]
    assert row["all_pass"]


def test_finite_gap_rows_are_reproduction_only_and_obey_strong_budget() -> None:
    for start, endpoint in ((1, 8), (3, 12), (8, 19), (18, 19)):
        row = finite_gap_row(start, endpoint)
        assert row["strong_bound_pass"]
        assert row["published_bound_pass"]
        assert row["reproduction_only"] is True
        assert row["all_pass"]


def test_p71_memory_S_sign_mutation_is_unambiguous() -> None:
    row = one_tail_sign_mutation()
    assert row["prime"] == 71
    assert row["a"] == "1/5040"
    assert "-2*m_endpoint*S by +2*m_endpoint*S" in row["mutation"]
    assert "+Y*S is unchanged" in row["mutation"]
    assert row["correct_ratio_15dp"] == "0.042746686479386"
    assert row["wrong_ratio_15dp"] == "7.335622869337969"
    assert row["difference_is_4mS"] is True
    assert row["correct_sign_pass"] is True
    assert row["wrong_sign_rejected"] is True
    assert row["reproduction_only"] is True


def test_p71_decimal_display_is_independent_of_ambient_context() -> None:
    expected = ("0.042746686479386", "7.335622869337969")
    for precision, rounding in ((7, ROUND_UP), (9, ROUND_DOWN), (80, ROUND_UP)):
        with localcontext() as context:
            context.prec = precision
            context.rounding = rounding
            row = one_tail_sign_mutation()
            assert (row["correct_ratio_15dp"], row["wrong_ratio_15dp"]) == expected
    assert getcontext().prec > 0


def test_fraction_and_integer_type_guards_reject_bool_float() -> None:
    for bad in (True, 3.0, "3"):
        with pytest.raises(ValueError):
            product_expansion_row(bad, 1, 8)
    for bad_weights in ((True,), (Fraction(1, 2), True), (0.1,)):
        with pytest.raises(TypeError, match="exact Fraction"):
            exact_tail_algebra(bad_weights)
    with pytest.raises(TypeError, match="exact integers"):
        tail_weights(True, 8)


def test_certificate_fixture_is_frozen_and_complete() -> None:
    payload = verify_certificate()
    assert payload["all_pass"]
    assert len(payload["product_expansion_rows"]) == 24
    assert len(canonical_json_bytes(payload)) == CERTIFICATE_FIXTURE_BYTES == 22543
    assert payload_sha256(payload) == CERTIFICATE_FIXTURE_SHA256
    assert payload["proof_ledger"]["budget"] == "931/2+254/3=3301/6<551"
    assert payload["claim_boundary"]["gates_A_through_E"] == [False] * 5


def test_optimized_mode_keeps_release_checks() -> None:
    command = (
        "from two_scale_tail import verify_certificate,payload_sha256; "
        "v=verify_certificate(); print(payload_sha256(v),v['all_pass'])"
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(ROOT / "src")
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-OO", "-c", command],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert completed.stdout.strip() == f"{CERTIFICATE_FIXTURE_SHA256} True"
