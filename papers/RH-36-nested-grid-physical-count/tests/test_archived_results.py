from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_snapshot_and_block_certificate() -> None:
    metadata = load("nested_grid_snapshot_sigma_1e-02.json")
    snapshot = ROOT / metadata["snapshot"]
    assert sha256_file(snapshot) == metadata["snapshot_sha256"]
    block = load("nested_block_certificate_sigma_1e-02.json")
    assert block["status"] == "rigorous_nested_grid_block_and_schur_gate"
    assert block["snapshot_sha256"] == metadata["snapshot_sha256"]
    gate = block["continuation_gate"]
    assert gate["detail_spectrum_outside_counting_circle"]
    assert gate["effective_perturbation_upper"] < 6.12e-4
    assert gate["admissible_coarse_resolvent_upper"] > 1634.0
    for certificate in block["block_certificates"].values():
        assert certificate["approximation_rank"] == 96
        assert certificate["residual_frobenius_upper"] < 3.1e-8


def test_coarse_count_replays_bitwise() -> None:
    replay = load("coarse_count_replay.json")
    assert replay["status"] == "bitwise_replayed_coarse_physical_count_one"
    assert replay["pair_defect_hash_match"]
    assert replay["transfer_ledger_hash_match"]
    assert replay["coarse_physical_inside_count_certified"]
    assert replay["coarse_physical_inside_count"] == 1


def test_physical_resolvent_atlas_closes() -> None:
    atlas = load("physical_resolvent_atlas.json")
    assert atlas["status"] == "full_physical_resolvent_continuation_atlas"
    assert atlas["center_count"] == 170
    assert atlas["closed_leaf_count"] == 314
    assert atlas["unresolved_leaf_count"] == 0
    assert atlas["exact_rational_partition_verified"]
    assert atlas["maximum_continuation_product_upper"] < 0.9
    rows = list(
        csv.DictReader(
            (ROOT / "results" / "physical_resolvent_atlas_leaves.csv").open(
                encoding="utf-8", newline=""
            )
        )
    )
    assert len(rows) == 314
    assert max(float(row["continuation_product_upper"]) for row in rows) == atlas[
        "maximum_continuation_product_upper"
    ]


def test_final_count_and_floating_localization() -> None:
    theorem = load("nested_grid_physical_count_certificate.json")
    assert theorem["status"] == "rigorous_nested_grid_physical_count_one"
    assert theorem["stored_object_identity_verified"]
    assert theorem["coarse_physical_inside_count"] == 1
    assert theorem["detail_inside_count"] == 0
    assert theorem["fine_physical_inside_count"] == 1
    pilot = load("fine_spectrum_pilot_sigma_1e-02.json")
    assert pilot["evidence_level"] == "floating_not_validated"
    assert pilot["coarse_resolved_inside_count"] == 1
    assert pilot["fine_resolved_inside_count"] == 1
    assert pilot["inside_eigenvalue_displacement"] < 4.5e-5
    assert pilot["maximum_fine_residual"] < 1.0e-14


def test_compact_center_archive_when_built() -> None:
    path = ROOT / "results" / "physical_resolvent_centers.csv"
    if not path.exists():
        return
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    assert len(rows) == 170
    assert len({row["center_id"] for row in rows}) == 170
    assert max(float(row["residual_frobenius_upper"]) for row in rows) < 1.0e-7
