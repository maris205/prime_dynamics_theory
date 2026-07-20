"""Build dependency, result, and publication hashes for RH-54."""

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
        "rh39_cutoff_manuscript": PAPERS
        / "RH-39-uniform-gaussian-cutoff-bridge"
        / "main.tex",
        "rh47_conditioning_manuscript": PAPERS
        / "RH-47-logarithmic-peripheral-conditioning"
        / "main.tex",
        "rh48_identification_manuscript": PAPERS
        / "RH-48-intrinsic-riesz-identification"
        / "main.tex",
        "rh49_directional_manuscript": PAPERS
        / "RH-49-directional-reduced-resolvent"
        / "main.tex",
        "rh50_hardy_manuscript": PAPERS
        / "RH-50-two-pole-hilbert-schmidt-hardy"
        / "main.tex",
        "rh51_stein_manuscript": PAPERS
        / "RH-51-cyclic-rank-growing-horizon-stein"
        / "main.tex",
        "rh52_factor_manuscript": PAPERS
        / "RH-52-intrinsic-peripheral-residue-transfer"
        / "main.tex",
        "rh53_tail_manuscript": PAPERS
        / "RH-53-deterministic-hardy-tail-cutoff"
        / "main.tex",
        "rh53_tail_algebra": PAPERS
        / "RH-53-deterministic-hardy-tail-cutoff"
        / "src"
        / "hardy_tail"
        / "algebra.py",
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
        ROOT / "figures" / "factor_aware_intrinsic_identification.pdf",
        ROOT / "figures" / "factor_aware_intrinsic_identification.png",
        ROOT / "main.pdf",
        ROOT / "factor-aware-intrinsic-riesz-identification.pdf",
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

    certificate_path = (
        ROOT / "results" / "intrinsic_identification_closure_certificate.json"
    )
    result_paths = [
        certificate_path,
        ROOT / "results" / "factor_aware_transfer_pilot.json",
        ROOT / "results" / "factor_aware_transfer_pilot_smoke.json",
        ROOT / "results" / "arb_factor_transfer_audit.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    audit = certificate["floating_five_scale_audit"]
    conclusion = certificate["program_conclusion"]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_levels": certificate["evidence_levels"],
        "normalized_coupling_theorem": certificate[
            "normalized_coupling_theorem"
        ],
        "riesz_conditioning_ledger": certificate["riesz_conditioning_ledger"],
        "factor_aware_triple_transfer": certificate[
            "factor_aware_triple_transfer"
        ],
        "growing_horizon_transfer": certificate["growing_horizon_transfer"],
        "conditional_identification_composition": certificate[
            "conditional_identification_composition"
        ],
        "nonnormal_no_go": certificate["nonnormal_no_go"],
        "program_conclusion": conclusion,
        "floating_five_scale_audit": {
            "noise_levels": audit["noise_levels"],
            "dimensions": audit["dimensions"],
            "horizons": audit["horizons"],
            "cutoff_multiples": audit["cutoff_multiples"],
            "extrema": audit["extrema"],
            "finest_stress_row": audit["stress_rows"][-1],
            "interval_validated": audit["interval_validated"],
        },
        "arb_audit": {
            "status": certificate["arb_audit"]["status"],
            "precision_bits": certificate["arb_audit"]["precision_bits"],
            "normalization_bound_certified": certificate["arb_audit"][
                "normalization_bound_certified"
            ],
            "transferred_block_contraction_certified": certificate[
                "arb_audit"
            ]["transferred_block_contraction_certified"],
            "production_intrinsic_riesz_interval_executed": certificate[
                "arb_audit"
            ]["production_intrinsic_riesz_interval_executed"],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
        "limitations": certificate["limitations"],
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
