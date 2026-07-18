"""Build dependency and publication archives for RH-40."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH6 = PAPERS / "RH-6-continuum-spectral-double-limits"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"


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


def dependency_manifest() -> dict[str, object]:
    external_inputs = {
        "rh6_continuum_nystrom_manuscript": RH6 / "main.tex",
        "rh24_peripheral_mode_builder": RH24
        / "experiments"
        / "run_contour_feshbach_audit.py",
        "rh36_factor_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh36_factor_metadata": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.json",
        "rh37_fine_factor_snapshot": RH37
        / "results"
        / "second_dyadic_fine_object_sigma_1e-02.npz",
        "rh37_fine_factor_metadata": RH37
        / "results"
        / "second_dyadic_snapshot_sigma_1e-02.json",
        "rh38_decay_certificate": RH38
        / "results"
        / "dyadic_haar_block_decay_certificate.json",
        "rh39_cutoff_certificate": RH39
        / "results"
        / "uniform_gaussian_cutoff_bridge_certificate.json",
    }
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
        ROOT / "figures" / "weighted_riesz_projector_bridge.pdf",
        ROOT / "figures" / "weighted_riesz_projector_bridge.png",
        ROOT / "weighted-riesz-projector-bridge.pdf",
    ]
    return {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: repository_entry(path) for name, path in external_inputs.items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in local_sources
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
        ROOT / "results" / "weighted_riesz_projector_bridge_certificate.json"
    )
    pilot_path = ROOT / "results" / "weighted_projector_pilot_sigma_1e-02.json"
    certificate = load(certificate_path)
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_levels": certificate["evidence_levels"],
        "analytic_statements": certificate["analytic_statements"],
        "exact_stored_frobenius_ratios": certificate[
            "exact_stored_frobenius_ratios"
        ],
        "maximum_exact_stored_biorthogonality_upper": certificate[
            "maximum_exact_stored_biorthogonality_upper"
        ],
        "parity_convergence": certificate["parity_convergence"],
        "floating_isolation_audit": certificate["floating_isolation_audit"],
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in (certificate_path, pilot_path, dependency_path)
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
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
