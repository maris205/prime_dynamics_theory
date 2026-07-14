"""Small optional NumPy smoke tests; directly executable and pytest-compatible."""

from __future__ import annotations

import math

import lambda_transfer_diagnostics as diagnostic


def test_von_mangoldt_array() -> None:
    values, primes = diagnostic.von_mangoldt_array(100)
    assert 97 in primes.tolist()
    assert abs(values[2] - math.log(2)) < 1e-15
    assert abs(values[4] - math.log(2)) < 1e-15
    assert values[6] == 0.0


def test_small_direct_AP_crosscheck() -> None:
    payload = diagnostic.run_diagnostics(8, 1024, 5, 2, [1, 5])
    assert payload["parameters"]["eligible_rows"] > 0
    assert payload["max_direct_AP_crosscheck_error"] < 1e-10
    assert all(mode["l1_row_error_over_X"] >= 0 for mode in payload["modes"])


def test_rejects_nonpositive_target_range() -> None:
    try:
        diagnostic.run_diagnostics(2, 100, 5, -1001, [1])
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("a nonpositive target range was accepted")


def _run_directly() -> None:
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    _run_directly()
