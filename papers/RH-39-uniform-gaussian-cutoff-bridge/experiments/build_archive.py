"""Build dependency and publication archives for RH-39."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH5 = PAPERS / "RH-5-renormalized-gaussian-response"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"


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
        "rh5_twice_tail_manuscript": RH5 / "main.tex",
        "rh18_archived_sparse_builder": RH18
        / "src"
        / "gaussian_return"
        / "operators.py",
        "rh38_component_pilot": RH38
        / "results"
        / "component_scaling_pilot_sigma_1e-02.json",
        "rh38_decay_certificate": RH38
        / "results"
        / "dyadic_haar_block_decay_certificate.json",
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
        ROOT / "figures" / "uniform_gaussian_cutoff_bridge.pdf",
        ROOT / "figures" / "uniform_gaussian_cutoff_bridge.png",
        ROOT / "uniform-gaussian-cutoff-bridge.pdf",
    ]
    return {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: repository_entry(path) for name, path in external_inputs.items()
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
        ROOT / "results" / "uniform_gaussian_cutoff_bridge_certificate.json"
    )
    pilot_path = ROOT / "results" / "cutoff_pilot_sigma_1e-02.json"
    certificate = load(certificate_path)
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_levels": certificate["evidence_levels"],
        "fixed_eight_sigma_two_norm_uppers": {
            dimension: row["two_norm_upper"]
            for dimension, row in certificate["fixed_eight_sigma_levels"].items()
        },
        "fixed_eight_sigma_continuum_omitted_mass": certificate[
            "fixed_eight_sigma_nonvanishing_limit"
        ]["mean_zero_continuum_omitted_mass_upper"],
        "maximum_cutoff_upper_over_floating_markov_block": certificate[
            "maximum_cutoff_upper_over_floating_markov_block"
        ],
        "eight_sigma_crossover_dimension_floor": certificate["schedule"][
            "eight_sigma_crossover_dimension_floor"
        ],
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
