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
        "rh134_summary": ROOT.parent / "RH-134-moving-frame-memory-tail-recurrence/results/summary.json",
        "rh134_audit": ROOT.parent / "RH-134-moving-frame-memory-tail-recurrence/results/memory_tail_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/relative_metric_affine_tail_recurrence.pdf",
        "figures/relative_metric_affine_tail_recurrence.png", "main.pdf", "relative-metric-affine-tail-recurrence.pdf",
    )]
    dependency = {
        "status": "all_rh135_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "relative_affine_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("relative_affine_audit.json", "relative_affine_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh135_relative_metric_affine_tail_recurrence_archived",
        "theorem": {
            "sharp_relative_affine_coefficients": True,
            "metric_gap_obstructions": True,
            "young_fixed_floor_optimization": True,
        },
        "audit": audit["audit_summary"], "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
