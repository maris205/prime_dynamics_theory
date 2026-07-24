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
        **{f"rh{number}_summary": ROOT.parent / f"RH-{number}-{slug}/results/summary.json" for number, slug in (
            (120, "gauge-covariant-rayleigh-transfer"),
            (121, "optimal-gram-gauge-pairing"),
            (122, "fixed-coordinate-gauge-obstruction"),
            (123, "defect-stable-rayleigh-recurrence"),
            (124, "spectral-normalization-capacity-transport"),
            (125, "combined-directional-support-transfer"),
            (126, "direct-margin-scale-recurrence"),
            (127, "outward-loewner-transport-guards"),
            (128, "conditional-eventual-directional-support"),
        )},
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/ten_layer_gauge_recurrence_review.pdf",
        "figures/ten_layer_gauge_recurrence_review.png", "main.pdf", "ten-layer-gauge-recurrence-review.pdf",
    )]
    dependency = {
        "status": "all_rh129_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "ten_layer_review_audit.json").read_text(encoding="utf-8"))
    results = [ROOT / "results" / name for name in ("ten_layer_review_audit.json", "ten_layer_review_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh129_ten_layer_gauge_recurrence_review_archived",
        "theorem": {"refined_frontier_antichain": True, "ten_layer_route_classification": True},
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
