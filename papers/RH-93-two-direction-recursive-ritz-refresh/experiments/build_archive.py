"""Build RH-93 dependency, result, and publication hashes."""

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
        "rh92_summary": PAPERS / "RH-92-block-schur-contraction-budgets" / "results" / "summary.json",
        "rh92_audit": PAPERS / "RH-92-block-schur-contraction-budgets" / "results" / "block_schur_budget_audit.json",
        "rh92_roadmap": PAPERS / "RH-92-block-schur-contraction-budgets" / "UPDATED_ROADMAP.md",
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
        ROOT / "figures" / "two_direction_recursive_ritz_refresh.pdf",
        ROOT / "figures" / "two_direction_recursive_ritz_refresh.png",
        ROOT / "main.pdf",
        ROOT / "two-direction-recursive-ritz-refresh.pdf",
    ]
    dependency = {
        "status": "all_rh93_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "two_direction_refresh_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "two_direction_refresh_audit.json",
        ROOT / "results" / "two_direction_refresh_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh93_two_direction_recursive_ritz_refresh_archived",
        "theorem": {
            "k_direction_complement_ritz_gain": True,
            "top_k_projected_cross_selection": True,
            "generalized_trial_frame_certificate": True,
            "recursive_reduced_block_closure": True,
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
                "one_direction_failures": audit["audit_summary"]["one_direction_subquarter_failure_count"],
                "two_direction_blocks": audit["audit_summary"]["two_direction_subquarter_block_count"],
                "maximum_two_direction_mean": audit["audit_summary"]["maximum_two_direction_block_geometric_mean"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
