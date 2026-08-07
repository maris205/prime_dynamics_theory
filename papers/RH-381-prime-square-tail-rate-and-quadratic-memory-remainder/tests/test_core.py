from decimal import Context, Decimal, ROUND_FLOOR
from fractions import Fraction
import os
from pathlib import Path
import subprocess
import sys

import pytest

from prime_square_tail import (
    CANONICAL_FIXTURE_SHA256,
    CUTOFF,
    NUMERIC_PLAN_INTERVAL_SHA256,
    PRECISION,
    canonical_fixture,
    coefficient_ledger,
    exact_identity_rows,
    finite_tail_identity,
    interval_fixture,
    normalized_x,
    run_statistics,
    square_run_counts,
    verify_certificate,
)
from prime_square_tail import core
from prime_square_tail.core import (
    canonical_json_bytes,
    certify_upper_le_lower,
    integer_square_tail_bound,
    payload_sha256,
    prime_square_weight,
)


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_exact_fixture_is_independently_frozen() -> None:
    payload = canonical_fixture()
    assert len(payload["rows"]) == 6
    assert len(canonical_json_bytes(payload)) == 2574
    assert payload_sha256(payload) == CANONICAL_FIXTURE_SHA256
    assert payload["rows"][0]["X_normalized"] == "3/4"
    assert payload["rows"][5]["M_over_A"] == "84354127/445906944"
    assert payload["telescoping"]["1_to_6"] == {
        "inv_pi2": "214088545939/1605264998400",
        "kappa2": "-117716501208/15493998579703",
    }


def test_locked_run_and_normalized_x_rows() -> None:
    expected_runs = (
        {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1},
        {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 17},
        {1: 154, 2: 148, 3: 142, 4: 136, 5: 130, 6: 124, 7: 118, 8: 697},
    )
    expected_x = (Fraction(3, 4), Fraction(19, 32), Fraction(275, 512))
    for y in (1, 2, 3):
        assert square_run_counts(y) == expected_runs[y - 1]
        assert normalized_x(y) == expected_x[y - 1]
        statistics = run_statistics(y)
        assert statistics["X"] == statistics["L"] - 2 * statistics["E"]


def test_exact_finite_tail_sum_identity_rows() -> None:
    rows = exact_identity_rows()
    assert len(rows) == 4
    assert all(row["all_pass"] for row in rows)
    assert all(row["current_identity_pass"] and row["next_identity_pass"] for row in rows)
    for bad in ((True,), (False,), (Fraction(1, 2), True)):
        with pytest.raises(TypeError, match="exact Fraction"):
            finite_tail_identity(bad)


def test_coefficient_ledger_is_170_then_340_plus_2() -> None:
    ledger = coefficient_ledger()
    assert ledger["x_contributions"] == {"4": 6, "5": 16, "6": 30, "7": 48, "8": 70}
    assert ledger["x_lipschitz"] == 170
    assert ledger["main_remainder"] == 340
    assert ledger["memory_remainder"] == 2
    assert ledger["total_remainder"] == 342
    assert ledger["pass"]


def test_outward_interval_fixture_has_frozen_digest_and_rows() -> None:
    payload = interval_fixture()
    assert len(canonical_json_bytes(payload)) == 6851
    assert payload_sha256(payload) == NUMERIC_PLAN_INTERVAL_SHA256
    assert payload["prime_count"] == 9592
    assert payload["last_prime"] == 99991
    assert payload["integer_tail_bound"] == "200001/20000200000"
    assert [row["y"] for row in payload["rows"]] == [1, 2, 3, 5, 10, 25]
    assert all(row["bound_pass"] and row["x_bound_pass"] for row in payload["rows"])
    assert payload["rows"][0]["bound_margin"] == (
        "2.94925432063879301356911298069930985543323835594671686244870"
    )
    assert payload["rows"][-1]["bound_margin"] == (
        "0.00085362331504062996631285357523996420791285090601448172653106"
    )


def test_release_constants_and_interval_digest_fail_closed(monkeypatch) -> None:
    with pytest.raises(ValueError, match="Lipschitz"):
        verify_certificate(x_lipschitz=169)
    with pytest.raises(ValueError, match="remainder"):
        verify_certificate(remainder_constant=341)
    with pytest.raises(ValueError, match="protocol"):
        verify_certificate(cutoff=CUTOFF - 1)
    with pytest.raises(ValueError, match="protocol"):
        verify_certificate(precision=PRECISION - 1)
    for keyword, value in (
        ("x_lipschitz", 170.0),
        ("remainder_constant", 342.0),
        ("cutoff", 100000.0),
        ("precision", 60.0),
        ("x_lipschitz", True),
        ("remainder_constant", True),
        ("cutoff", True),
        ("precision", True),
    ):
        with pytest.raises(TypeError, match="exact integer"):
            verify_certificate(**{keyword: value})
    monkeypatch.setattr(core, "NUMERIC_PLAN_INTERVAL_SHA256", "0" * 64)
    with pytest.raises(ArithmeticError, match="independent frozen audit"):
        core.verify_certificate()


def test_interval_comparison_fails_closed_and_margin_is_floor_context() -> None:
    context = Context(prec=60, rounding=ROUND_FLOOR)
    assert certify_upper_le_lower(Decimal("1.0"), Decimal("1.1"), "fixture", context) == Decimal("0.1")
    with pytest.raises(ArithmeticError, match="not certified"):
        certify_upper_le_lower(Decimal("1.1"), Decimal("1.0"), "fixture", context)


def test_integer_square_tail_is_exact() -> None:
    assert integer_square_tail_bound(100_000) == Fraction(200001, 20000200000)
    with pytest.raises(ValueError):
        integer_square_tail_bound(1)
    assert prime_square_weight(3) == Fraction(1, 8)
    for invalid in (True, 2, 4, 9, 15):
        with pytest.raises(ValueError, match="odd prime"):
            prime_square_weight(invalid)


def test_optimized_mode_keeps_all_release_checks() -> None:
    command = (
        "from prime_square_tail import verify_certificate; "
        "v=verify_certificate(); "
        "print(v['interval_fixture_bytes'],v['interval_fixture_sha256'],v['all_pass'])"
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
    assert completed.stdout.strip() == f"6851 {NUMERIC_PLAN_INTERVAL_SHA256} True"
    assert "assert " not in (ROOT / "src/prime_square_tail/core.py").read_text()


def test_full_certificate() -> None:
    certificate = verify_certificate()
    assert certificate["all_pass"]
    assert certificate["interval_digest_matches_independent_plan"]
    assert certificate["claim_boundary"]["gates_A_through_E"] == [False] * 5
