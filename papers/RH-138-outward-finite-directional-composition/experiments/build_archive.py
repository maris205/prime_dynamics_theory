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
        "rh125_summary": ROOT.parent / "RH-125-combined-directional-support-transfer/results/summary.json",
        "rh127_summary": ROOT.parent / "RH-127-outward-loewner-transport-guards/results/summary.json",
        "rh137_summary": ROOT.parent / "RH-137-finite-horizon-young-tail-envelope/results/summary.json",
        "rh137_source": ROOT.parent / "RH-137-finite-horizon-young-tail-envelope/experiments/build_finite_horizon_audit.py",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/outward_finite_directional_composition.pdf",
        "figures/outward_finite_directional_composition.png", "main.pdf", "outward-finite-directional-composition.pdf",
    )]
    dependency = {
        "status": "all_rh138_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "outward_composition_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("outward_composition_audit.json", "outward_composition_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh138_outward_finite_directional_composition_archived",
        "theorem": {
            "outward_two_residual_composition": True,
            "outward_normalized_base_lower": True,
            "norm_ball_precision_barrier": True,
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
