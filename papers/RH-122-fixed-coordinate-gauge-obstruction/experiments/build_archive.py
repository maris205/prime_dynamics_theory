from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/fixed_coordinate_gauge_obstruction.pdf",
        "figures/fixed_coordinate_gauge_obstruction.png", "main.pdf", "fixed-coordinate-gauge-obstruction.pdf",
    )]
    dependency = {
        "status": "all_rh122_sources_and_publication_artifacts_hashed",
        "external_inputs": {},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "fixed_coordinate_audit.json").read_text(encoding="utf-8"))
    results = [ROOT / "results" / name for name in ("fixed_coordinate_audit.json", "fixed_coordinate_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh122_fixed_coordinate_gauge_obstruction_archived",
        "theorem": {"sharp_identity_gauge_constants": True, "fixed_coordinate_unboundedness": True, "exact_gauge_recovery": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in results},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
