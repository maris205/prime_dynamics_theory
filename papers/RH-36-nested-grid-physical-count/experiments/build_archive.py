"""Build compact center, dependency, and theorem archives for RH-36."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_center_archive() -> tuple[Path, dict[str, object]]:
    center_dir = ROOT / "results" / "physical_centers_sigma_1e-02"
    records = []
    for path in sorted(center_dir.glob("*.json")):
        record = load(path)
        if record["status"] == "rigorous_physical_resolvent_center":
            records.append(record)
    records.sort(
        key=lambda row: Fraction(
            int(row["turn_numerator"]), int(row["turn_denominator"])
        )
    )
    if not records:
        raise RuntimeError("no physical center records are available")
    fields = [
        "status",
        "center_id",
        "source_kind",
        "turn_numerator",
        "turn_denominator",
        "sigma",
        "spectral_parameter_real",
        "spectral_parameter_imag",
        "physical_dimension",
        "border_rank",
        "bordered_dimension",
        "matrix_nnz",
        "factor_nnz",
        "factor_seconds",
        "certificate_seconds",
        "approximate_inverse_frobenius_upper",
        "residual_frobenius_upper",
        "residual_center_frobenius_upper",
        "residual_radius_frobenius_upper",
        "center_inverse_two_norm_upper",
        "inverse_sha256",
        "residual_center_sha256",
        "residual_radius_sha256",
    ]
    output = ROOT / "results" / "physical_resolvent_centers.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(records)
    manifest = {
        "status": "rigorous_physical_resolvent_center_archive",
        "center_count": len(records),
        "minimum_center_inverse_upper": min(
            float(row["center_inverse_two_norm_upper"]) for row in records
        ),
        "maximum_center_inverse_upper": max(
            float(row["center_inverse_two_norm_upper"]) for row in records
        ),
        "maximum_center_residual_upper": max(
            float(row["residual_frobenius_upper"]) for row in records
        ),
        "center_archive": relative(output),
        "center_archive_sha256": sha256_file(output),
        "center_ids": [str(row["center_id"]) for row in records],
    }
    manifest_path = ROOT / "results" / "physical_center_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output, manifest


def hashed_entry(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(PAPERS.parent)), "sha256": sha256_file(path)}


def dependency_manifest() -> dict[str, object]:
    external = {
        "rh28_arcwise_contour_arcs": PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "results"
        / "arcwise_contour_arcs.csv",
        "rh28_arcwise_scale_summary": PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "results"
        / "arcwise_scale_summary.csv",
        "rh33_refined_leaf_ledger": PAPERS
        / "RH-33-certified-complement-resolvent-atlas"
        / "results"
        / "refined_atlas_sigma_1e-02_leaves.csv",
        "rh35_physical_count_certificate": PAPERS
        / "RH-35-exact-packet-pair-physical-count"
        / "results"
        / "packet_pair_certificate_sigma_1e-02.json",
        "rh35_exact_pair_defect": PAPERS
        / "RH-35-exact-packet-pair-physical-count"
        / "results"
        / "exact_packet_defect_sigma_1e-02.json",
        "rh35_transfer_ledger": PAPERS
        / "RH-35-exact-packet-pair-physical-count"
        / "results"
        / "packet_pair_transfer_sigma_1e-02.csv",
    }
    source_paths = [
        *list((ROOT / "src").rglob("*.py")),
        *list((ROOT / "experiments").glob("*.py")),
    ]
    if (ROOT / "tests").exists():
        source_paths.extend((ROOT / "tests").glob("*.py"))
    source_paths = sorted(source_paths)
    return {
        "status": "all_consumed_inputs_and_sources_hashed",
        "external_inputs": {
            name: hashed_entry(path) for name, path in external.items()
        },
        "local_sources": {
            relative(path): sha256_file(path) for path in source_paths
        },
    }


def main() -> None:
    center_path, center_manifest = write_center_archive()
    dependency = dependency_manifest()
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    theorem_path = ROOT / "results" / "nested_grid_physical_count_certificate.json"
    theorem = load(theorem_path)
    result_paths = [
        ROOT / "results" / "nested_grid_snapshot_sigma_1e-02.npz",
        ROOT / "results" / "nested_grid_snapshot_sigma_1e-02.json",
        ROOT / "results" / "nested_block_certificate_sigma_1e-02.json",
        ROOT / "results" / "physical_resolvent_atlas.json",
        ROOT / "results" / "physical_resolvent_atlas_leaves.csv",
        center_path,
        ROOT / "results" / "physical_center_manifest.json",
        ROOT / "results" / "coarse_count_replay.json",
        ROOT / "results" / "coarse_count_replay_pair_defect.json",
        ROOT / "results" / "coarse_count_replay_transfer.csv",
        ROOT / "results" / "fine_spectrum_pilot_sigma_1e-02.json",
        ROOT / "results" / "fine_spectrum_pilot_sigma_1e-02.npz",
        theorem_path,
        dependency_path,
    ]
    summary = {
        "status": theorem["status"],
        "scope": theorem["scope"],
        "sigma": theorem["sigma"],
        "coarse_dimension": theorem["coarse_dimension"],
        "fine_dimension": theorem["fine_dimension"],
        "coarse_physical_inside_count": theorem[
            "coarse_physical_inside_count"
        ],
        "fine_physical_inside_count": theorem["fine_physical_inside_count"],
        "detail_inside_count": theorem["detail_inside_count"],
        "effective_perturbation_upper": theorem[
            "effective_perturbation_upper"
        ],
        "maximum_continuation_product_upper": theorem[
            "maximum_continuation_product_upper"
        ],
        "atlas_center_count": center_manifest["center_count"],
        "atlas_leaf_count": theorem["atlas_leaf_count"],
        "result_hashes": {
            relative(path): sha256_file(path) for path in result_paths
        },
        "limitations": theorem["limitations"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
