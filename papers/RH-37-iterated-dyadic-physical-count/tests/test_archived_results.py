from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_split_snapshot_and_second_block_certificate() -> None:
    metadata = load("second_dyadic_snapshot_sigma_1e-02.json")
    assert metadata["status"] == "stored_split_second_dyadic_factor_snapshot"
    for name, relative in metadata["snapshot_parts"].items():
        assert sha256_file(ROOT / relative) == metadata["snapshot_part_sha256"][name]
    block = load("second_dyadic_block_certificate_sigma_1e-02.json")
    assert block["status"] == "rigorous_second_dyadic_block_and_schur_gate"
    assert block["snapshot_part_sha256"] == metadata["snapshot_part_sha256"]
    gate = block["continuation_gate"]
    assert gate["detail_spectrum_outside_counting_circle"]
    assert gate["effective_perturbation_upper"] < 1.53e-4
    assert gate["admissible_coarse_resolvent_upper"] > 6537.0
    for certificate in block["block_certificates"].values():
        assert certificate["approximation_rank"] == 96
        assert certificate["residual_frobenius_upper"] < 1.6e-8


def test_inherited_count_replays_bitwise() -> None:
    replay = load("inherited_A4096_count_replay.json")
    assert replay["status"] == "exactly_replayed_inherited_A4096_count_one"
    assert replay["coarse_object_array_hash_match"]
    assert replay["snapshot_hash_match"]
    assert replay["rh37_coarse_physical_inside_count_certified"]
    assert replay["rh37_coarse_physical_inside_count"] == 1


def test_propagated_resolvent_atlas_closes_twice() -> None:
    atlas = load("propagated_resolvent_atlas.json")
    assert atlas["status"] == "full_iterated_propagated_resolvent_atlas"
    assert atlas["center_count"] == 183
    assert atlas["inherited_center_count"] == 170
    assert atlas["additional_center_count"] == 13
    assert atlas["closed_leaf_count"] == 324
    assert atlas["unresolved_leaf_count"] == 0
    assert atlas["exact_rational_partition_verified"]
    assert atlas["maximum_first_effective_product_upper"] < 0.748
    assert atlas["maximum_propagated_fine_resolvent_upper"] < 4844.0
    assert atlas["maximum_second_continuation_product_upper"] < 0.741
    rows = list(
        csv.DictReader(
            (ROOT / "results" / "propagated_resolvent_atlas_leaves.csv").open(
                encoding="utf-8", newline=""
            )
        )
    )
    assert len(rows) == 324
    assert max(float(row["first_effective_product_upper"]) for row in rows) == atlas[
        "maximum_first_effective_product_upper"
    ]
    assert max(float(row["second_continuation_product_upper"]) for row in rows) == atlas[
        "maximum_second_continuation_product_upper"
    ]


def test_final_count_chain_and_floating_localization() -> None:
    theorem = load("iterated_dyadic_physical_count_certificate.json")
    assert theorem["status"] == "rigorous_iterated_dyadic_physical_count_one"
    assert theorem["stored_object_identity_verified"]
    assert theorem["certified_count_chain"] == {
        "A2048": 1,
        "A4096": 1,
        "A8192": 1,
    }
    assert theorem["second_detail_inside_count"] == 0
    pilot = load("second_dyadic_spectrum_pilot_sigma_1e-02.json")
    assert pilot["evidence_level"] == "floating_not_validated"
    assert pilot["coarse_resolved_inside_count"] == 1
    assert pilot["fine_resolved_inside_count"] == 1
    assert pilot["inside_eigenvalue_displacement"] < 1.2e-5
    assert pilot["maximum_fine_residual"] < 2.0e-15


def test_compact_center_archive_when_built() -> None:
    path = ROOT / "results" / "coarse_resolvent_centers.csv"
    if not path.exists():
        return
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    assert len(rows) == 183
    assert len({row["center_id"] for row in rows}) == 183
    assert sum(row["archive_origin"] == "RH-37" for row in rows) == 13
    assert max(float(row["residual_frobenius_upper"]) for row in rows) < 1.0e-7
