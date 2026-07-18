"""Build dependency and publication archives for RH-38."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"


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
        "rh36_first_block_certificate": RH36
        / "results"
        / "nested_block_certificate_sigma_1e-02.json",
        "rh37_second_block_certificate": RH37
        / "results"
        / "second_dyadic_block_certificate_sigma_1e-02.json",
        "rh36_component_snapshot": RH36
        / "results"
        / "nested_grid_snapshot_sigma_1e-02.npz",
        "rh37_component_fine_object": RH37
        / "results"
        / "second_dyadic_fine_object_sigma_1e-02.npz",
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
        ROOT / "figures" / "dyadic_haar_block_decay.pdf",
        ROOT / "figures" / "dyadic_haar_block_decay.png",
        ROOT / "dyadic-haar-block-decay.pdf",
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
        ROOT / "results" / "dyadic_haar_block_decay_certificate.json"
    )
    pilot_path = ROOT / "results" / "component_scaling_pilot_sigma_1e-02.json"
    certificate = load(certificate_path)
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_levels": certificate["evidence_levels"],
        "analytic_rate_law": certificate["analytic_rate_law"],
        "rigorous_upper_ratios": certificate["rigorous_upper_ratios"],
        "renormalized_upper_spreads": certificate[
            "renormalized_upper_spreads"
        ],
        "maximum_floating_ratio_error_from_exact_quarter_half": certificate[
            "maximum_floating_ratio_error_from_exact_quarter_half"
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
