"""Build RH-92 dependency, result, and publication hashes."""

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


def entry(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}


def main() -> None:
    external = {
        "rh77_model_source": PAPERS / "RH-77-postblock-effective-rank-compression" / "experiments" / "run_effective_rank_audit.py",
        "rh77_summary": PAPERS / "RH-77-postblock-effective-rank-compression" / "results" / "summary.json",
        "rh82_clock_source": PAPERS / "RH-82-half-log-postblock-rank-clock" / "src" / "half_log_rank" / "bounds.py",
        "rh82_summary": PAPERS / "RH-82-half-log-postblock-rank-clock" / "results" / "summary.json",
        "rh90_summary": PAPERS / "RH-90-schur-secular-subquarter-certificate" / "results" / "summary.json",
        "rh91_summary": PAPERS / "RH-91-schur-packet-route-review" / "results" / "summary.json",
        "rh91_roadmap": PAPERS / "RH-91-schur-packet-route-review" / "UPDATED_ROADMAP.md",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "block_schur_contraction_budgets.pdf",
        ROOT / "figures" / "block_schur_contraction_budgets.png",
        ROOT / "main.pdf",
        ROOT / "block-schur-contraction-budgets.pdf",
    ]
    dependency = {
        "status": "all_rh92_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "block_schur_budget_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "block_schur_budget_audit.json",
        ROOT / "results" / "block_schur_budget_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh92_block_schur_contraction_budgets_archived",
        "theorem": {
            "exact_schur_threshold_dichotomy": True,
            "coercive_trial_defect_identity": True,
            "variable_budget_correction_and_refresh": True,
            "block_contraction_bootstrap": True,
        },
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "summary": str(summary_path.relative_to(ROOT)),
                "update_count": audit["audit_summary"]["update_count"],
                "pointwise_obstructions": audit["audit_summary"]["pointwise_subquarter_failure_count"],
                "maximum_block_mean": audit["audit_summary"]["maximum_block_budget_geometric_mean"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
