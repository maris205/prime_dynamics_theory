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
        "rh135_builder": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/experiments/build_relative_affine_audit.py",
        "rh135_audit": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/results/relative_affine_audit.json",
        "rh135_summary": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/results/summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/projective_gram_base_recurrence.pdf",
        "figures/projective_gram_base_recurrence.png", "main.pdf", "projective-gram-base-recurrence.pdf",
    )]
    dependency = {
        "status": "all_rh146_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results/dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results/projective_gram_audit.json").read_text())
    result_files = [ROOT / "results" / name for name in ("projective_gram_audit.json", "projective_gram_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh146_projective_gram_base_recurrence_archived",
        "theorem": {"sharp_projective_recurrence": True, "summable_variation_corollary": True, "bounded_distortion_obstruction": True},
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

