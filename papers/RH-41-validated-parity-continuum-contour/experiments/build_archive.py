"""Build dependency and publication archives for RH-41."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"


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
        "rh27_componentwise_rounding": RH27
        / "src"
        / "outward_residuals"
        / "componentwise.py",
        "rh27_package_exports": RH27
        / "src"
        / "outward_residuals"
        / "__init__.py",
        "rh36_factor_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh38_haar_manuscript": RH38 / "main.tex",
        "rh39_cutoff_certificate": RH39
        / "results"
        / "uniform_gaussian_cutoff_bridge_certificate.json",
        "rh40_weighted_riesz_manuscript": RH40 / "main.tex",
        "rh40_leading_spectrum_pilot": RH40
        / "results"
        / "weighted_projector_pilot_sigma_1e-02.json",
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
        ROOT / "figures" / "validated_parity_continuum_contour.pdf",
        ROOT / "figures" / "validated_parity_continuum_contour.png",
        ROOT / "validated-parity-continuum-contour.pdf",
    ]
    return {
        "status": (
            "all_consumed_inputs_sources_and_publication_artifacts_hashed"
        ),
        "external_inputs": {
            name: repository_entry(path)
            for name, path in external_inputs.items()
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

    result_paths = [
        ROOT / "results" / "coarse_grushin_contour_certificate.json",
        ROOT / "results" / "stored_to_midpoint_bridge_certificate.json",
        ROOT / "results" / "validated_parity_continuum_certificate.json",
    ]
    continuum = load(result_paths[-1])
    summary = {
        "status": continuum["status"],
        "scope": continuum["scope"],
        "evidence_level": continuum["evidence_level"],
        "critical_parameter": continuum["critical_parameter"],
        "contour": continuum["contour"],
        "coarse_stored_theorem": continuum["coarse_stored_theorem"],
        "stored_to_galerkin_4096": continuum["stored_to_galerkin_4096"],
        "dyadic_galerkin_steps": continuum["dyadic_galerkin_steps"],
        "galerkin_to_continuum": continuum["galerkin_to_continuum"],
        "continuum_conclusion": continuum["continuum_conclusion"],
        "continuum_to_exact_midpoint_family": continuum[
            "continuum_to_exact_midpoint_family"
        ],
        "weighted_riesz_consequence": continuum[
            "weighted_riesz_consequence"
        ],
        "gate_summary": continuum["gate_summary"],
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in (*result_paths, dependency_path)
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": continuum["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
