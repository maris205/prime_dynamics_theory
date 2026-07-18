"""Build dependency and publication archives for RH-42."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"
RH41 = PAPERS / "RH-41-validated-parity-continuum-contour"


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
    paths = {
        "rh36_factor_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh39_cutoff_certificate": RH39
        / "results"
        / "uniform_gaussian_cutoff_bridge_certificate.json",
        "rh40_weighted_riesz_manuscript": RH40 / "main.tex",
        "rh41_coarse_source": RH41
        / "experiments"
        / "run_coarse_grushin_certificate.py",
        "rh41_midpoint_bridge_source": RH41
        / "experiments"
        / "build_midpoint_bridge_certificate.py",
        "rh41_continuum_certificate": RH41
        / "results"
        / "validated_parity_continuum_certificate.json",
    }
    for path in sorted(
        (RH27 / "src" / "outward_residuals").glob("*.py")
    ):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh27_outward_{name}_source"] = path
    for path in sorted((RH41 / "src" / "parity_contour").glob("*.py")):
        name = path.stem.replace("__init__", "package_exports")
        paths[f"rh41_parity_{name}_source"] = path
    return paths


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
        ROOT / "figures" / "uniform_euclidean_parity_contour.pdf",
        ROOT / "figures" / "uniform_euclidean_parity_contour.png",
        ROOT / "uniform-euclidean-parity-contour.pdf",
    ]
    return {
        "status": (
            "all_consumed_inputs_sources_and_publication_artifacts_hashed"
        ),
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

    rigorous_paths = [
        ROOT / "results" / "euclidean_grushin_contour_certificate.json",
        ROOT / "results" / "euclidean_stored_to_midpoint_bridge.json",
        ROOT / "results" / "hilbert_schmidt_envelope_certificate.json",
        ROOT / "results" / "uniform_euclidean_parity_certificate.json",
    ]
    pilot_path = ROOT / "results" / "hilbert_constants_pilot.json"
    uniform = load(rigorous_paths[-1])
    hashed_results = [*rigorous_paths, pilot_path, dependency_path]
    summary = {
        "status": uniform["status"],
        "scope": uniform["scope"],
        "evidence_level": uniform["evidence_level"],
        "contour": uniform["contour"],
        "stored_euclidean_theorem": uniform[
            "stored_euclidean_theorem"
        ],
        "stored_to_exact_midpoint_4096": uniform[
            "stored_to_exact_midpoint_4096"
        ],
        "midpoint_to_galerkin_4096": uniform[
            "midpoint_to_galerkin_4096"
        ],
        "dyadic_hilbert_galerkin_steps": uniform[
            "dyadic_hilbert_galerkin_steps"
        ],
        "galerkin_to_continuum_L2": uniform[
            "galerkin_to_continuum_L2"
        ],
        "continuum_L2_conclusion": uniform["continuum_L2_conclusion"],
        "uniform_matrix_family": uniform["uniform_matrix_family"],
        "gate_summary": uniform["gate_summary"],
        "hilbert_schmidt_envelope": uniform[
            "hilbert_schmidt_envelope"
        ],
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in hashed_results
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": uniform["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
