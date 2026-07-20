"""Build RH-56 dependency, result, and publication hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path):
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def external_inputs():
    return {
        "rh13_manuscript": PAPERS
        / "RH-13-validated-reduced-sector-spectral-gap"
        / "main.tex",
        "rh13_certificate_source": PAPERS
        / "RH-13-validated-reduced-sector-spectral-gap"
        / "src"
        / "validated_gap"
        / "certificate.py",
        "rh13_certificate": PAPERS
        / "RH-13-validated-reduced-sector-spectral-gap"
        / "results"
        / "validated_spectral_gap_certificate.json",
        "rh15_manuscript": PAPERS
        / "RH-15-parity-extracted-bulk-scattering"
        / "main.tex",
        "rh50_pilot": PAPERS
        / "RH-50-two-pole-hilbert-schmidt-hardy"
        / "results"
        / "two_pole_hardy_pilot.json",
        "rh51_pilot": PAPERS
        / "RH-51-cyclic-rank-growing-horizon-stein"
        / "results"
        / "structured_stein_pilot.json",
        "rh53_pilot": PAPERS
        / "RH-53-deterministic-hardy-tail-cutoff"
        / "results"
        / "deterministic_tail_pilot.json",
        "rh54_manuscript": PAPERS
        / "RH-54-factor-aware-intrinsic-identification"
        / "main.tex",
        "rh55_manuscript": PAPERS
        / "RH-55-strong-weak-riesz-cutoff-transfer"
        / "main.tex",
        "roadmap": PAPERS / "RH-ROADMAP-after-RH50.md",
    }


def main() -> None:
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
        ROOT / "figures" / "growing_horizon_hard_space_barrier.pdf",
        ROOT / "figures" / "growing_horizon_hard_space_barrier.png",
        ROOT / "main.pdf",
        ROOT / "growing-horizon-hard-space-barrier.pdf",
    ]
    dependency = {
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
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result_paths = [
        ROOT / "results" / "hardy_barrier_certificate.json",
        ROOT / "results" / "hardy_barrier_pilot.json",
        ROOT / "results" / "hardy_barrier_pilot_smoke.json",
        ROOT / "results" / "arb_hardy_barrier_ledger.json",
        ROOT / "results" / "arb_sector_resonance_certificate.json",
        dependency_path,
    ]
    certificate = load(ROOT / "results" / "hardy_barrier_certificate.json")
    pilot = load(ROOT / "results" / "hardy_barrier_pilot.json")
    sector = load(ROOT / "results" / "arb_sector_resonance_certificate.json")
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_levels": certificate["evidence_levels"],
        "two_stage_theorem": certificate["two_stage_theorem"],
        "black_box_barrier": certificate["black_box_barrier"],
        "directional_overlap_theorem": certificate[
            "directional_overlap_theorem"
        ],
        "program_conclusion": certificate["program_conclusion"],
        "binary64_audit": certificate["binary64_audit"],
        "arb_audit": certificate["arb_audit"],
        "sector_certificate": {
            "status": sector["status"],
            "precision_bits": sector["precision_bits"],
            "finite_eigenvalues_in_contour": sector[
                "finite_eigenvalues_in_contour"
            ],
            "full_contour_perturbation_product_ball": sector[
                "full_contour_perturbation_product_ball"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
        "limitations": certificate["limitations"],
        "pilot_extrema": pilot["extrema"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "dependency_manifest": str(dependency_path.relative_to(ROOT)),
                "summary": str(summary_path.relative_to(ROOT)),
                "result_count": len(result_paths),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

