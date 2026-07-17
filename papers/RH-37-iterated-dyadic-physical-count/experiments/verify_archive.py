"""Verify RH-37 hashes, split arrays, partitions, and theorem gates."""

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
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")

    dependency = load(ROOT / "results" / "dependency_manifest.json")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external input mismatch: {path}")
    for relative, expected in dependency["external_code"].items():
        if sha256_file(REPOSITORY / relative) != expected:
            raise RuntimeError(f"external code mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"local source mismatch: {relative}")

    metadata = load(ROOT / "results" / "second_dyadic_snapshot_sigma_1e-02.json")
    for name, relative in metadata["snapshot_parts"].items():
        if sha256_file(ROOT / relative) != metadata["snapshot_part_sha256"][name]:
            raise RuntimeError(f"snapshot part mismatch: {name}")
    object_path = ROOT / metadata["snapshot_parts"]["fine_object"]
    with np.load(object_path) as data:
        for key in data.files:
            if sha256_array(data[key]) != metadata["local_array_sha256"][key]:
                raise RuntimeError(f"fine object array mismatch: {key}")
    for name in (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    ):
        with np.load(ROOT / metadata["snapshot_parts"][name]) as data:
            for short, suffix in (
                ("left", "left"),
                ("singular_values", "singular_values"),
                ("right_adjoint", "right_adjoint"),
            ):
                key = f"{name}_{suffix}"
                if sha256_array(data[short]) != metadata["local_array_sha256"][key]:
                    raise RuntimeError(f"low-rank center array mismatch: {key}")

    centers = read_csv(ROOT / "results" / "coarse_resolvent_centers.csv")
    center_manifest = load(
        ROOT / "results" / "coarse_resolvent_center_manifest.json"
    )
    if len(centers) != int(center_manifest["center_count"]):
        raise RuntimeError("center count mismatch")
    if len({row["center_id"] for row in centers}) != len(centers):
        raise RuntimeError("duplicate center identifier")
    if not all(row["status"] == "rigorous_physical_resolvent_center" for row in centers):
        raise RuntimeError("non-rigorous center in archive")
    if max(float(row["residual_frobenius_upper"]) for row in centers) >= 1.0:
        raise RuntimeError("a center residual is not admissible")

    leaves = read_csv(ROOT / "results" / "propagated_resolvent_atlas_leaves.csv")
    atlas = load(ROOT / "results" / "propagated_resolvent_atlas.json")
    if not verify_partition(leaves):
        raise RuntimeError("the propagated leaves do not form an exact partition")
    if len(leaves) != int(atlas["closed_leaf_count"]):
        raise RuntimeError("propagated leaf count mismatch")
    maximum_first = max(float(row["first_effective_product_upper"]) for row in leaves)
    maximum_second = max(
        float(row["second_continuation_product_upper"]) for row in leaves
    )
    if maximum_first != float(atlas["maximum_first_effective_product_upper"]):
        raise RuntimeError("first product mismatch")
    if maximum_second != float(atlas["maximum_second_continuation_product_upper"]):
        raise RuntimeError("second product mismatch")
    if maximum_first >= 1.0 or maximum_second >= 1.0:
        raise RuntimeError("an iterated continuation gate does not close")

    theorem = load(
        ROOT / "results" / "iterated_dyadic_physical_count_certificate.json"
    )
    if theorem["status"] != "rigorous_iterated_dyadic_physical_count_one":
        raise RuntimeError("the final theorem status is not rigorous")
    if theorem["certified_count_chain"] != {"A2048": 1, "A4096": 1, "A8192": 1}:
        raise RuntimeError("unexpected certified count chain")

    archived_files = [
        ROOT / "README.md",
        ROOT / "iterated-dyadic-physical-count.pdf",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "figures" / "iterated_dyadic_physical_count.pdf",
        ROOT / "figures" / "iterated_dyadic_physical_count.png",
        ROOT / "src" / "iterated_grid" / "certificate.py",
        ROOT / "results" / "summary.json",
        ROOT / "results" / "coarse_resolvent_centers.csv",
        ROOT / "results" / "propagated_resolvent_atlas_leaves.csv",
        ROOT / "results" / "iterated_dyadic_physical_count_certificate.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived_files}
    payload = {
        "status": "all_archived_hashes_and_iterated_count_gates_verified",
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "A2048_inside_count": 1,
            "A4096_inside_count": 1,
            "second_detail_inside_count": 0,
            "A8192_inside_count": 1,
            "second_effective_perturbation_upper": theorem[
                "second_refinement"
            ]["effective_perturbation_upper"],
            "maximum_propagated_A4096_resolvent_upper": theorem[
                "propagated_atlas"
            ]["maximum_propagated_A4096_resolvent_upper"],
            "maximum_second_continuation_product_upper": maximum_second,
            "atlas_center_count": len(centers),
            "atlas_leaf_count": len(leaves),
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
