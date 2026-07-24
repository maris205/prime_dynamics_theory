from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    external = {
        "rh96_audit": ROOT.parent / "RH-96-gap-weighted-weak-mode-quotient/results/weak_mode_quotient_audit.json",
        "rh96_summary": ROOT.parent / "RH-96-gap-weighted-weak-mode-quotient/results/summary.json",
        "rh96_source": ROOT.parent / "RH-96-gap-weighted-weak-mode-quotient/experiments/run_weak_mode_quotient_audit.py",
        "rh142_summary": ROOT.parent / "RH-142-factorized-arb-snapshot-packet-closure/results/summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/threshold_branch_stability.pdf",
        "figures/threshold_branch_stability.png", "main.pdf", "threshold-branch-stability-radius.pdf",
    )]
    dependency = {
        "status": "all_rh143_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "threshold_branch_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("threshold_branch_audit.json", "threshold_branch_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh143_threshold_branch_stability_radius_archived",
        "theorem": {"sharp_threshold_branch_radius": True, "projected_cross_lipschitz_bound": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()

