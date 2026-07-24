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
        "rh121_summary": ROOT.parent / "RH-121-optimal-gram-gauge-pairing/results/summary.json",
        "rh125_summary": ROOT.parent / "RH-125-combined-directional-support-transfer/results/summary.json",
        "rh127_summary": ROOT.parent / "RH-127-outward-loewner-transport-guards/results/summary.json",
        "rh129_summary": ROOT.parent / "RH-129-ten-layer-gauge-recurrence-review/results/summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/floor_free_semidefinite_directional_audit.pdf",
        "figures/floor_free_semidefinite_directional_audit.png", "main.pdf",
        "floor-free-semidefinite-directional-audit.pdf",
    )]
    dependency = {
        "status": "all_rh130_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "floor_free_audit.json").read_text(encoding="utf-8"))
    results = [ROOT / "results" / name for name in ("floor_free_audit.json", "floor_free_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh130_floor_free_semidefinite_directional_audit_archived",
        "theorem": {"semidefinite_exact_gram_minimax": True, "rank_creation_obstruction": True},
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
