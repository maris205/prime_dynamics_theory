"""Build RH-116 dependency hashes and publication summary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPO = PAPERS.parent


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    external = {
        "rh77_model_builder": PAPERS / "RH-77-postblock-effective-rank-compression/experiments/run_effective_rank_audit.py",
        "rh82_rank_clock": PAPERS / "RH-82-half-log-postblock-rank-clock/src/half_log_rank/bounds.py",
        "rh94_source_packet": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh/src/source_seeded_refresh/bounds.py",
        "rh96_refresh_step": PAPERS / "RH-96-gap-weighted-weak-mode-quotient/experiments/run_weak_mode_quotient_audit.py",
        "rh101_memory_action": PAPERS / "RH-101-finite-memory-packet-gram-action/src/finite_memory_gram/action.py",
        "rh115_summary": PAPERS / "RH-115-composite-directional-support-gate/results/summary.json",
    }
    local = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    publications = [
        ROOT / name
        for name in (
            ".gitignore",
            "README.md",
            "THEOREM_LEDGER.md",
            "UPDATED_ROADMAP.md",
            "main.tex",
            "references.bib",
            "pyproject.toml",
            "requirements.txt",
            "figures/monotone_memory_depth_optimization.pdf",
            "figures/monotone_memory_depth_optimization.png",
            "main.pdf",
            "monotone-memory-depth-optimization.pdf",
        )
    ]
    dependency = {
        "status": "all_rh116_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: {"path": str(path.relative_to(REPO)), "sha256": sha(path)}
            for name, path in external.items()
        },
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "memory_depth_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "memory_depth_audit.json",
        ROOT / "results" / "memory_depth_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh116_monotone_memory_depth_optimization_archived",
        "theorem": {
            "nested_weyl_lower_monotonicity": True,
            "first_passage_depth_is_cost_minimal": True,
            "finite_full_history_search_is_complete": True,
        },
        "audit": audit["audit_summary"],
        "threshold_summary": audit["threshold_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
