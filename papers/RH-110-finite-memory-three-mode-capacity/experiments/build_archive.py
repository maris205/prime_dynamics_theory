"""Build RH-110 hashes and publication archive."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPO = PAPERS.parent

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    external = {
        "rh94_audit": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh/results/source_seeded_horizon_audit.json",
        "rh96_audit": PAPERS / "RH-96-gap-weighted-weak-mode-quotient/results/weak_mode_quotient_audit.json",
        "rh108_summary": PAPERS / "RH-108-finite-memory-fourth-cross-support/results/summary.json",
        "rh109_summary": PAPERS / "RH-109-exterior-power-fourth-cross-support/results/summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md",
        "main.tex", "references.bib", "pyproject.toml", "requirements.txt",
        "figures/finite_memory_three_mode_capacity.pdf",
        "figures/finite_memory_three_mode_capacity.png",
        "main.pdf", "finite-memory-three-mode-capacity.pdf")]
    dependency = {
        "status": "all_rh110_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dep_path = ROOT / "results/dependency_manifest.json"
    dep_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results/three_mode_capacity_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results/three_mode_capacity_audit.json", ROOT / "results/three_mode_capacity_smoke.json", dep_path]
    summary = {
        "status": "rh110_finite_memory_three_mode_capacity_archived",
        "theorem": {"finite_memory_capacity_interval": True, "capacity_aware_volume_recovery": True, "sharp_fixed_volume_capacity_interval": True},
        "audit": audit["audit_summary"],
        "threshold_summary": audit["threshold_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results/summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))

if __name__ == "__main__":
    main()
