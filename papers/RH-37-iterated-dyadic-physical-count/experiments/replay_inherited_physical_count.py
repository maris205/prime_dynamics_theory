"""Verify that RH-37's coarse object is exactly RH-36's certified fine object."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"


def sha256_array(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).view(np.uint8)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    metadata_path = ROOT / "results" / "second_dyadic_snapshot_sigma_1e-02.json"
    metadata = load(metadata_path)
    inherited_snapshot = Path(metadata["inherited_snapshot"])
    inherited_theorem_path = (
        RH36 / "results" / "nested_grid_physical_count_certificate.json"
    )
    inherited_theorem = load(inherited_theorem_path)
    names = {
        "matrix_data": "fine_matrix_data",
        "matrix_indices": "fine_matrix_indices",
        "matrix_indptr": "fine_matrix_indptr",
        "right_modes": "fine_right_modes",
        "left_modes": "fine_left_modes",
        "peripheral_values": "fine_peripheral_values",
    }
    with np.load(inherited_snapshot) as data:
        actual_hashes = {
            name: sha256_array(np.asarray(data[array_name]))
            for name, array_name in names.items()
        }
        dimension = int(data["fine_dimension"])

    expected_hashes = dict(metadata["inherited_coarse_object_array_sha256"])
    object_hash_match = actual_hashes == expected_hashes
    snapshot_hash = sha256_file(inherited_snapshot)
    snapshot_hash_match = bool(
        snapshot_hash == metadata["inherited_snapshot_sha256"]
        and snapshot_hash == inherited_theorem["snapshot_sha256"]
    )
    inherited_count_gate = bool(
        inherited_theorem["status"] == "rigorous_nested_grid_physical_count_one"
        and inherited_theorem["fine_physical_inside_count_certified"]
        and int(inherited_theorem["fine_physical_inside_count"]) == 1
    )
    replayed = bool(object_hash_match and snapshot_hash_match and inherited_count_gate)
    payload = {
        "status": (
            "exactly_replayed_inherited_A4096_count_one"
            if replayed
            else "inherited_A4096_count_replay_mismatch"
        ),
        "evidence_level": "bitwise_object_identity_and_hashed_theorem_replay",
        "sigma": float(metadata["sigma"]),
        "dimension": dimension,
        "inherited_snapshot": str(inherited_snapshot),
        "inherited_snapshot_sha256": snapshot_hash,
        "snapshot_hash_match": snapshot_hash_match,
        "expected_object_array_sha256": expected_hashes,
        "actual_object_array_sha256": actual_hashes,
        "coarse_object_array_hash_match": object_hash_match,
        "inherited_theorem": str(inherited_theorem_path),
        "inherited_theorem_sha256": sha256_file(inherited_theorem_path),
        "inherited_theorem_status": inherited_theorem["status"],
        "inherited_physical_inside_count_certified": inherited_count_gate,
        "inherited_physical_inside_count": 1 if inherited_count_gate else None,
        "rh37_coarse_physical_inside_count_certified": replayed,
        "rh37_coarse_physical_inside_count": 1 if replayed else None,
    }
    output = ROOT / "results" / "inherited_A4096_count_replay.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not replayed:
        raise RuntimeError("the inherited A4096 count did not replay")


if __name__ == "__main__":
    main()
