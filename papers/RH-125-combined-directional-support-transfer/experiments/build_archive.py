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
        "rh121_audit": ROOT.parent / "RH-121-optimal-gram-gauge-pairing/results/optimal_gauge_audit.json",
        "rh123_summary": ROOT.parent / "RH-123-defect-stable-rayleigh-recurrence/results/summary.json",
        "rh124_summary": ROOT.parent / "RH-124-spectral-normalization-capacity-transport/results/summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/combined_directional_support_transfer.pdf",
        "figures/combined_directional_support_transfer.png", "main.pdf", "combined-directional-support-transfer.pdf",
    )]
    dependency = {
        "status": "all_rh125_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "combined_transfer_audit.json").read_text(encoding="utf-8"))
    results = [ROOT / "results" / name for name in ("combined_transfer_audit.json", "combined_transfer_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh125_combined_directional_support_transfer_archived",
        "theorem": {"combined_directional_transfer": True, "iterated_candidate_lower": True},
        "audit": audit["audit_summary"], "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in results},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
