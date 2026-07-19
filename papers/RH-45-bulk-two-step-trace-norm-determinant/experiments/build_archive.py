"""Build dependency and publication archives for RH-45."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH10 = PAPERS / "RH-10-parity-renormalized-long-cycle-determinant"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"
RH44 = PAPERS / "RH-44-validated-rank-two-peripheral-complement"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def external_inputs() -> dict[str, Path]:
    return {
        "rh10_regularized_determinant_manuscript": RH10 / "main.tex",
        "rh36_stored_2048_4096_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh37_stored_8192_snapshot": RH37
        / "results"
        / "second_dyadic_fine_object_sigma_1e-02.npz",
        "rh39_cutoff_certificate": RH39
        / "results"
        / "uniform_gaussian_cutoff_bridge_certificate.json",
        "rh42_uniform_euclidean_certificate": RH42
        / "results"
        / "uniform_euclidean_parity_certificate.json",
        "rh42_hilbert_source": RH42
        / "src"
        / "euclidean_contour"
        / "hilbert.py",
        "rh43_weighted_schur_source": RH43
        / "src"
        / "weighted_kernel"
        / "bounds.py",
        "rh43_parity_kernel_certificate": RH43
        / "results"
        / "validated_weighted_parity_kernel.json",
        "rh44_rank_two_certificate": RH44
        / "results"
        / "validated_rank_two_peripheral_complement.json",
    }


def dependency_manifest() -> dict[str, object]:
    local_sources = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    publication_paths = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "bulk_two_step_trace_norm_determinant.pdf",
        ROOT / "figures" / "bulk_two_step_trace_norm_determinant.png",
        ROOT / "bulk-two-step-trace-norm-determinant.pdf",
    ]
    return {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: repository_entry(path)
            for name, path in external_inputs().items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in local_sources
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in publication_paths
        },
    }


def main() -> None:
    dependency = dependency_manifest()
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    certificate_path = (
        ROOT / "results" / "bulk_trace_norm_determinant_certificate.json"
    )
    pilot_path = ROOT / "results" / "stored_bulk_square_determinants.json"
    certificate = load(certificate_path)
    pilot = load(pilot_path)
    first = certificate["dimension_ledgers"]["65536"]
    last = certificate["dimension_ledgers"]["1073741824"]
    hashed_results = [certificate_path, pilot_path, dependency_path]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "continuum_bulk": certificate["continuum_bulk"],
        "main_theorems": certificate["main_theorems"],
        "gate_summary": {
            "all_displayed_contour_gates_closed": all(
                row["all_contour_gates_closed"]
                for row in certificate["dimension_ledgers"].values()
            ),
            "threshold_dimension": 65536,
            "threshold_full_bulk_hilbert_schmidt_error_upper": first[
                "full_bulk"
            ]["bulk_hilbert_schmidt_error_upper"],
            "threshold_full_square_trace_norm_error_upper": first[
                "full_bulk"
            ]["square_trace_norm_error_upper"],
            "last_dimension": 1073741824,
            "last_full_bulk_hilbert_schmidt_error_upper": last["full_bulk"]
            ["bulk_hilbert_schmidt_error_upper"],
            "last_full_square_trace_norm_error_upper": last["full_bulk"]
            ["square_trace_norm_error_upper"],
            "last_full_determinant_disk_1e_minus_2_error_upper": last[
                "determinant_disk_bounds"
            ]["0.01"]["full_fredholm_determinant_error_upper"],
        },
        "stored_determinant_pilot": {
            "status": pilot["status"],
            "evidence_level": pilot["evidence_level"],
            "dimensions": sorted(int(value) for value in pilot["levels"]),
            "maximum_symmetric_det2_identity_error": pilot[
                "maximum_symmetric_det2_identity_error"
            ],
            "determinant_at_w_1e_minus_2": {
                level: row["determinants"]["0.01"]["square_determinant"]
                for level, row in pilot["levels"].items()
            },
            "consecutive_absolute_differences": pilot[
                "consecutive_absolute_differences"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in hashed_results
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": certificate["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
