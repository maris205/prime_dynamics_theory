"""Build RH-118 dependency hashes and publication summary."""

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
        "rh110_summary": PAPERS / "RH-110-finite-memory-three-mode-capacity/results/summary.json",
        "rh111_summary": PAPERS / "RH-111-tail-energy-exterior-concentration/results/summary.json",
        "rh114_summary": PAPERS / "RH-114-psd-rayleigh-directional-tail/results/summary.json",
        "rh115_composite_audit": PAPERS / "RH-115-composite-directional-support-gate/results/composite_gate_audit.json",
        "rh116_depth_audit": PAPERS / "RH-116-monotone-memory-depth-optimization/results/memory_depth_audit.json",
        "rh117_summary": PAPERS / "RH-117-finite-anchor-scale-law-barrier/results/summary.json",
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
            "figures/conditional_composite_exterior_route.pdf",
            "figures/conditional_composite_exterior_route.png",
            "main.pdf",
            "conditional-composite-exterior-route.pdf",
        )
    ]
    dependency = {
        "status": "all_rh118_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: {"path": str(path.relative_to(REPO)), "sha256": sha(path)}
            for name, path in external.items()
        },
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "conditional_route_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "conditional_route_audit.json",
        ROOT / "results" / "conditional_route_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh118_conditional_composite_exterior_route_archived",
        "theorem": {
            "normalized_trace_factorization": True,
            "conditional_composite_liminf_theorem": True,
            "alternating_route_closure": True,
            "strict_margin_outward_robustness": True,
        },
        "audit": audit["audit_summary"],
        "threshold_summary": audit["threshold_summary"],
        "minimal_physical_packets": audit["minimal_physical_packets"],
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
