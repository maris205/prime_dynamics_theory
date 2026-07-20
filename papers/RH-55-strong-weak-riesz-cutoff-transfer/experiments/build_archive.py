"""Build dependency, result, and publication hashes for RH-55."""

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
        "rh14_boundary_layer_manuscript": PAPERS
        / "RH-14-square-root-parity-boundary-layer"
        / "main.tex",
        "rh39_cutoff_manuscript": PAPERS
        / "RH-39-uniform-gaussian-cutoff-bridge"
        / "main.tex",
        "rh39_cutoff_bounds": PAPERS
        / "RH-39-uniform-gaussian-cutoff-bridge"
        / "src"
        / "cutoff_bridge"
        / "bounds.py",
        "rh47_conditioning_manuscript": PAPERS
        / "RH-47-logarithmic-peripheral-conditioning"
        / "main.tex",
        "rh52_factor_manuscript": PAPERS
        / "RH-52-intrinsic-peripheral-residue-transfer"
        / "main.tex",
        "rh53_hardy_tail_manuscript": PAPERS
        / "RH-53-deterministic-hardy-tail-cutoff"
        / "main.tex",
        "rh54_factor_aware_manuscript": PAPERS
        / "RH-54-factor-aware-intrinsic-identification"
        / "main.tex",
        "rh54_factor_pilot": PAPERS
        / "RH-54-factor-aware-intrinsic-identification"
        / "results"
        / "factor_aware_transfer_pilot.json",
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
        ROOT / "figures" / "strong_weak_riesz_cutoff_transfer.pdf",
        ROOT / "figures" / "strong_weak_riesz_cutoff_transfer.png",
        ROOT / "main.pdf",
        ROOT / "strong-weak-riesz-cutoff-transfer.pdf",
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

    certificate_path = ROOT / "results" / "riesz_cutoff_closure_certificate.json"
    result_paths = [
        certificate_path,
        ROOT / "results" / "riesz_cutoff_pilot.json",
        ROOT / "results" / "riesz_cutoff_pilot_smoke.json",
        ROOT / "results" / "arb_riesz_cutoff_ledger.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    pilot = load(ROOT / "results" / "riesz_cutoff_pilot.json")
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_levels": certificate["evidence_levels"],
        "midpoint_ulam_theorem": certificate["midpoint_ulam_theorem"],
        "sandwich_riesz_theorem": certificate["sandwich_riesz_theorem"],
        "mass_only_route": certificate["mass_only_route"],
        "gaussian_shape_route": certificate["gaussian_shape_route"],
        "fixed_window_no_go": certificate["fixed_window_no_go"],
        "program_conclusion": certificate["program_conclusion"],
        "binary64_audit": {
            "midpoint_ulam_levels": len(pilot["midpoint_ulam_audit"]),
            "factor_rows": len(pilot["archived_intrinsic_factor_audit"]),
            "extrema": pilot["extrema"],
            "interval_validated": False,
        },
        "arb_audit": certificate["arb_audit"],
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
