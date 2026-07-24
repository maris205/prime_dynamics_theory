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
    upstream_names = [
        "RH-130-floor-free-semidefinite-directional-audit",
        "RH-131-singular-gram-support-rayleigh-theory",
        "RH-132-canonical-partial-isometry-forcing-gauge",
        "RH-133-dyadic-packet-transport-gauge",
        "RH-134-moving-frame-memory-tail-recurrence",
        "RH-135-relative-metric-affine-tail-recurrence",
        "RH-136-metric-balanced-packet-gauge",
        "RH-137-finite-horizon-young-tail-envelope",
        "RH-138-outward-finite-directional-composition",
    ]
    external = {
        f"rh{130 + index}_summary": ROOT.parent / name / "results" / "summary.json"
        for index, name in enumerate(upstream_names)
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/ten_layer_controlled_viability_review.pdf",
        "figures/ten_layer_controlled_viability_review.png", "main.pdf", "ten-layer-controlled-viability-review.pdf",
    )]
    dependency = {
        "status": "all_rh139_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "ten_layer_review.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("ten_layer_review.json", "ten_layer_review_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh139_ten_layer_controlled_viability_review_archived",
        "theorem": {
            "controlled_viability_eventual_support": True,
            "tail_gap_and_base_liminf_architecture_sharp": True,
            "revised_minimal_frontier": True,
        },
        "audit": audit["audit_summary"], "program_boundary": audit["theorem_boundary"],
        "revised_frontier": audit["revised_frontier"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
