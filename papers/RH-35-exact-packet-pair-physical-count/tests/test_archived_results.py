from __future__ import annotations

from fractions import Fraction
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_certificate_proves_one_physical_eigenvalue() -> None:
    result = load_json("packet_pair_certificate_sigma_1e-02.json")
    assert result["status"] == (
        "rigorous_exact_packet_pair_correction_physical_count_one"
    )
    assert result["dimension"] == 2048
    assert result["packet_rank"] == 4
    assert result["leaf_count"] == 949
    assert result["exact_pair_defect"]["pair_defect_frobenius_upper"] < 1.0e-14
    assert result["all_corrected_complement_homotopies_certified"]
    assert result["all_corrected_feshbach_homotopies_certified"]
    assert result["maximum_complement_neumann_product_upper"] < 1.0
    assert result["maximum_feshbach_rouche_product_upper"] < 1.0
    assert result["corrected_complement_count"] == 0
    assert result["corrected_feshbach_winding"] == 1
    assert result["zero_outside_counting_circle_exact"]
    assert result["physical_two_step_inside_count_certified"]
    assert result["physical_two_step_inside_count"] == 1


def test_exact_packet_defect_entries_reconstruct_reported_bound() -> None:
    result = load_json("exact_packet_defect_sigma_1e-02.json")
    entries = [
        [
            Fraction(item["numerator"], item["denominator"])
            for item in row
        ]
        for row in result["pair_defect_entries"]
    ]
    square = sum(
        (value * value for row in entries for value in row), Fraction(0)
    )
    assert float(square) ** 0.5 <= result["pair_defect_frobenius_upper"]


def test_every_leaf_closes_both_homotopies() -> None:
    result = load_json("packet_pair_certificate_sigma_1e-02.json")
    with (ROOT / result["transfer_ledger"]).open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 949
    assert all(
        row["complement_homotopy_certified"] == "True" for row in rows
    )
    assert all(row["feshbach_homotopy_certified"] == "True" for row in rows)
    assert max(
        float(row["complement_neumann_product_upper"]) for row in rows
    ) < 1.0
    assert max(
        float(row["feshbach_rouche_product_upper"]) for row in rows
    ) < 1.0


def test_compact_summary_hashes() -> None:
    summary = load_json("summary.json")
    dependency = load_json("dependency_manifest.json")
    assert summary["physical_two_step_inside_count"] == 1
    assert dependency["status"] == "all_consumed_inputs_and_sources_hashed"
    for name, expected in summary["result_hashes"].items():
        actual = hashlib.sha256((ROOT / "results" / name).read_bytes()).hexdigest()
        assert actual == expected
