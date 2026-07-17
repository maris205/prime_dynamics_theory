"""Verify RH-36 hashes, exact partitions, and theorem gates."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_array(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).view(np.uint8)).hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_partition(rows: list[dict[str, str]]) -> bool:
    intervals = sorted(
        (
            Fraction(int(row["start_numerator"]), int(row["turn_denominator"])),
            Fraction(int(row["end_numerator"]), int(row["turn_denominator"])),
        )
        for row in rows
    )
    return bool(
        intervals
        and intervals[0][0] == 0
        and intervals[-1][1] == 1
        and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:]))
    )


def main() -> None:
    summary = load(ROOT / "results" / "summary.json")
    for relative, expected in summary["result_hashes"].items():
        path = ROOT / relative
        if sha256_file(path) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")

    dependency = load(ROOT / "results" / "dependency_manifest.json")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external dependency mismatch: {path}")
    for relative, expected in dependency["local_sources"].items():
        path = ROOT / relative
        if sha256_file(path) != expected:
            raise RuntimeError(f"local source mismatch: {relative}")

    snapshot_path = ROOT / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    snapshot_metadata = load(snapshot_path.with_suffix(".json"))
    if sha256_file(snapshot_path) != snapshot_metadata["snapshot_sha256"]:
        raise RuntimeError("snapshot file hash mismatch")
    with np.load(snapshot_path) as data:
        for name, expected in snapshot_metadata["array_sha256"].items():
            if sha256_array(data[name]) != expected:
                raise RuntimeError(f"snapshot array mismatch: {name}")

    centers = read_csv(ROOT / "results" / "physical_resolvent_centers.csv")
    center_manifest = load(ROOT / "results" / "physical_center_manifest.json")
    if len(centers) != int(center_manifest["center_count"]):
        raise RuntimeError("center count mismatch")
    if len({row["center_id"] for row in centers}) != len(centers):
        raise RuntimeError("duplicate center identifier")
    if not all(row["status"] == "rigorous_physical_resolvent_center" for row in centers):
        raise RuntimeError("non-rigorous center in archive")
    if max(float(row["residual_frobenius_upper"]) for row in centers) >= 1.0:
        raise RuntimeError("a center Neumann residual is not admissible")

    leaves_path = ROOT / "results" / "physical_resolvent_atlas_leaves.csv"
    leaves = read_csv(leaves_path)
    atlas = load(ROOT / "results" / "physical_resolvent_atlas.json")
    if not verify_partition(leaves):
        raise RuntimeError("the atlas leaves do not form an exact partition")
    if len(leaves) != int(atlas["closed_leaf_count"]):
        raise RuntimeError("atlas leaf count mismatch")
    maximum_product = max(
        float(row["continuation_product_upper"]) for row in leaves
    )
    if maximum_product != float(atlas["maximum_continuation_product_upper"]):
        raise RuntimeError("atlas product mismatch")
    if maximum_product >= 1.0:
        raise RuntimeError("the continuation product does not close")

    theorem = load(
        ROOT / "results" / "nested_grid_physical_count_certificate.json"
    )
    if theorem["status"] != "rigorous_nested_grid_physical_count_one":
        raise RuntimeError("the final theorem status is not rigorous")
    if not theorem["fine_physical_inside_count_certified"]:
        raise RuntimeError("the fine-grid count is not certified")
    if int(theorem["fine_physical_inside_count"]) != 1:
        raise RuntimeError("unexpected fine-grid contour count")

    archived_files = [
        ROOT / "README.md",
        ROOT / "nested-grid-physical-count.pdf",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "figures" / "nested_grid_physical_count.pdf",
        ROOT / "figures" / "nested_grid_physical_count.png",
        ROOT / "src" / "nested_grid" / "certificate.py",
        ROOT / "results" / "summary.json",
        ROOT / "results" / "physical_resolvent_centers.csv",
        ROOT / "results" / "physical_resolvent_atlas_leaves.csv",
        ROOT / "results" / "nested_grid_physical_count_certificate.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_files
    }
    payload = {
        "status": "all_archived_hashes_and_nested_grid_count_gates_verified",
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "coarse_physical_inside_count": int(
                theorem["coarse_physical_inside_count"]
            ),
            "detail_inside_count": int(theorem["detail_inside_count"]),
            "fine_physical_inside_count": int(
                theorem["fine_physical_inside_count"]
            ),
            "effective_perturbation_upper": float(
                theorem["effective_perturbation_upper"]
            ),
            "maximum_continuation_product_upper": maximum_product,
            "atlas_center_count": len(centers),
            "atlas_leaf_count": len(leaves),
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
