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
        "rh139_summary": ROOT.parent / "RH-139-ten-layer-controlled-viability-review/results/summary.json",
        "rh139_roadmap": ROOT.parent / "RH-139-ten-layer-controlled-viability-review/UPDATED_ROADMAP.md",
    }
    for number in range(140, 149):
        summary = next(ROOT.parent.glob(f"RH-{number}-*/results/summary.json"))
        external[f"rh{number}_summary"] = summary
        external[f"rh{number}_archive"] = summary.with_name("archive_verification.json")
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/ten_layer_source_support_review.pdf",
        "figures/ten_layer_source_support_review.png", "main.pdf", "ten-layer-source-support-review.pdf",
    )]
    dependency = {
        "status": "all_rh149_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results/dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results/ten_layer_source_support_review.json").read_text())
    result_files = [ROOT / "results" / name for name in ("ten_layer_source_support_review.json", "ten_layer_source_support_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh149_ten_layer_source_support_review_archived",
        "theorem": {"three_interface_sufficiency": True, "inclusion_minimal_frontier": True, "route_priority_revision": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()

