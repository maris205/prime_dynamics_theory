"""Build RH-117 dependency hashes and publication summary."""

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
        "rh110_capacity_audit": PAPERS / "RH-110-finite-memory-three-mode-capacity/results/three_mode_capacity_audit.json",
        "rh111_concentration_audit": PAPERS / "RH-111-tail-energy-exterior-concentration/results/exterior_concentration_audit.json",
        "rh116_depth_audit": PAPERS / "RH-116-monotone-memory-depth-optimization/results/memory_depth_audit.json",
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
            "figures/finite_anchor_scale_law_barrier.pdf",
            "figures/finite_anchor_scale_law_barrier.png",
            "main.pdf",
            "finite-anchor-scale-law-barrier.pdf",
        )
    ]
    dependency = {
        "status": "all_rh117_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: {"path": str(path.relative_to(REPO)), "sha256": sha(path)}
            for name, path in external.items()
        },
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "scale_law_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "scale_law_audit.json",
        ROOT / "results" / "scale_law_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh117_finite_anchor_scale_law_barrier_archived",
        "theorem": {
            "positive_smooth_anchor_extension": True,
            "bounded_interval_anchor_extension": True,
            "finite_anchor_asymptotic_nonidentifiability": True,
        },
        "audit": audit["audit_summary"],
        "descriptive_power_law_fits": audit["descriptive_power_law_fits"],
        "continuation_barrier": audit["continuation_barrier"],
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
