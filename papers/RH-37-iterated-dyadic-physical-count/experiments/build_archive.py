"""Build compact center, dependency, and theorem archives for RH-37."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"


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


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def write_center_archive() -> tuple[Path, dict[str, object]]:
    inherited_path = RH36 / "results" / "physical_resolvent_centers.csv"
    with inherited_path.open(encoding="utf-8", newline="") as handle:
        inherited = [dict(row, archive_origin="RH-36") for row in csv.DictReader(handle)]
    additional = []
    center_dir = ROOT / "results" / "physical_centers_sigma_1e-02"
    for path in sorted(center_dir.glob("*.json")):
        record = load(path)
        if record["status"] == "rigorous_physical_resolvent_center":
            additional.append(dict(record, archive_origin="RH-37"))
    records = {str(row["center_id"]): row for row in inherited}
    records.update({str(row["center_id"]): row for row in additional})
    ordered = sorted(
        records.values(),
        key=lambda row: Fraction(
            int(row["turn_numerator"]), int(row["turn_denominator"])
        ),
    )
    fields = [
        "status",
        "center_id",
        "archive_origin",
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
    output = ROOT / "results" / "coarse_resolvent_centers.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(ordered)
    manifest = {
        "status": "rigorous_combined_A2048_resolvent_center_archive",
        "center_count": len(ordered),
        "inherited_center_count": len(inherited),
        "additional_center_count": len(additional),
        "minimum_center_inverse_upper": min(
            float(row["center_inverse_two_norm_upper"]) for row in ordered
        ),
        "maximum_center_inverse_upper": max(
            float(row["center_inverse_two_norm_upper"]) for row in ordered
        ),
        "maximum_center_residual_upper": max(
            float(row["residual_frobenius_upper"]) for row in ordered
        ),
        "center_archive": relative(output),
        "center_archive_sha256": sha256_file(output),
        "inherited_archive": repository_entry(inherited_path),
        "center_ids": [str(row["center_id"]) for row in ordered],
    }
    manifest_path = ROOT / "results" / "coarse_resolvent_center_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return output, manifest


def dependency_manifest() -> dict[str, object]:
    external_inputs = {
        "rh28_scale_summary": RH28 / "results" / "arcwise_scale_summary.csv",
        "rh36_split_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh36_first_block_certificate": RH36
        / "results"
        / "nested_block_certificate_sigma_1e-02.json",
        "rh36_physical_count_theorem": RH36
        / "results"
        / "nested_grid_physical_count_certificate.json",
        "rh36_center_archive": RH36
        / "results"
        / "physical_resolvent_centers.csv",
    }
    external_code_paths = sorted(
        {
            *RH27.joinpath("src").rglob("*.py"),
            *RH28.joinpath("src").rglob("*.py"),
            *RH30.joinpath("src").rglob("*.py"),
            *RH33.joinpath("src").rglob("*.py"),
            *RH36.joinpath("src").rglob("*.py"),
            RH36 / "experiments" / "run_physical_resolvent_batch.py",
        }
    )
    local_sources = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    return {
        "status": "all_consumed_inputs_code_and_sources_hashed",
        "external_inputs": {
            name: repository_entry(path) for name, path in external_inputs.items()
        },
        "external_code": {
            str(path.relative_to(REPOSITORY)): sha256_file(path)
            for path in external_code_paths
        },
        "local_sources": {
            relative(path): sha256_file(path) for path in local_sources
        },
    }


def main() -> None:
    center_path, center_manifest = write_center_archive()
    dependency = dependency_manifest()
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    theorem_path = ROOT / "results" / "iterated_dyadic_physical_count_certificate.json"
    theorem = load(theorem_path)
    metadata = load(ROOT / "results" / "second_dyadic_snapshot_sigma_1e-02.json")
    result_paths = [
        ROOT / relative_path for relative_path in metadata["snapshot_parts"].values()
    ]
    result_paths.extend(
        [
            ROOT / "results" / "second_dyadic_snapshot_sigma_1e-02.json",
            ROOT / "results" / "second_dyadic_block_certificate_sigma_1e-02.json",
            ROOT / "results" / "propagated_resolvent_atlas.json",
            ROOT / "results" / "propagated_resolvent_atlas_leaves.csv",
            center_path,
            ROOT / "results" / "coarse_resolvent_center_manifest.json",
            ROOT / "results" / "inherited_A4096_count_replay.json",
            ROOT / "results" / "second_dyadic_pilot_sigma_1e-02.json",
            ROOT / "results" / "second_dyadic_spectrum_pilot_sigma_1e-02.json",
            ROOT / "results" / "second_dyadic_spectrum_pilot_sigma_1e-02.npz",
            theorem_path,
            dependency_path,
        ]
    )
    summary = {
        "status": theorem["status"],
        "scope": theorem["scope"],
        "sigma": theorem["sigma"],
        "certified_count_chain": theorem["certified_count_chain"],
        "second_effective_perturbation_upper": theorem["second_refinement"][
            "effective_perturbation_upper"
        ],
        "maximum_propagated_A4096_resolvent_upper": theorem[
            "propagated_atlas"
        ]["maximum_propagated_A4096_resolvent_upper"],
        "maximum_second_continuation_product_upper": theorem[
            "propagated_atlas"
        ]["maximum_second_continuation_product_upper"],
        "atlas_center_count": center_manifest["center_count"],
        "additional_center_count": center_manifest["additional_center_count"],
        "atlas_leaf_count": theorem["propagated_atlas"]["leaf_count"],
        "result_hashes": {
            relative(path): sha256_file(path) for path in result_paths
        },
        "limitations": theorem["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
