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
        "rh130_audit": ROOT.parent / "RH-130-floor-free-semidefinite-directional-audit/results/floor_free_audit.json",
        "rh134_summary": ROOT.parent / "RH-134-moving-frame-memory-tail-recurrence/results/summary.json",
        "rh134_source": ROOT.parent / "RH-134-moving-frame-memory-tail-recurrence/src/memory_tail_recurrence/__init__.py",
        "rh135_summary": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/results/summary.json",
        "rh135_source": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/src/relative_affine_tail/__init__.py",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/metric_balanced_packet_gauge.pdf",
        "figures/metric_balanced_packet_gauge.png", "main.pdf", "metric-balanced-packet-gauge.pdf",
    )]
    dependency = {
        "status": "all_rh136_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "metric_balanced_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("metric_balanced_audit.json", "metric_balanced_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh136_metric_balanced_packet_gauge_archived",
        "theorem": {
            "orthogonal_metric_minimax": True,
            "universal_orthogonal_contractivity_wall": True,
            "finite_family_contractivity_complete": True,
            "global_affine_optimizer": False,
        },
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
