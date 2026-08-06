from __future__ import annotations

from parity_capacity import capacity_formula, finite_checks, mobius_prefix, parity_statistics


def test_small_mobius_prefix_and_a2_formula() -> None:
    values = mobius_prefix(12)
    assert values == [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]
    result = capacity_formula(values)
    assert result["capacity"] == 6
    assert result["best_key"] in {"positive_0", "negative_0", "positive_1", "negative_1"}
    assert all(sign in {-1, 1} for sign in result["witness"])


def test_parity_counts_are_exact() -> None:
    stats = parity_statistics(mobius_prefix(12))
    assert stats["total_mertens"] == -2
    assert stats["residues"][0]["squarefree"] == 3
    assert stats["residues"][1]["squarefree"] == 5


def test_formula_matches_bruteforce() -> None:
    checks = finite_checks(12)
    assert checks["all_pass"] is True
    assert all(row["pass"] for row in checks["rows"])
