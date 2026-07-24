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
        "rh130_summary": ROOT.parent / "RH-130-floor-free-semidefinite-directional-audit/results/summary.json",
        "rh130_audit": ROOT.parent / "RH-130-floor-free-semidefinite-directional-audit/results/floor_free_audit.json",
        "rh132_summary": ROOT.parent / "RH-132-canonical-partial-isometry-forcing-gauge/results/summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/dyadic_packet_transport_gauge.pdf",
        "figures/dyadic_packet_transport_gauge.png", "main.pdf", "dyadic-packet-transport-gauge.pdf",
    )]
    dependency = {
        "status": "all_rh133_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "dyadic_gauge_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("dyadic_gauge_audit.json", "dyadic_gauge_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh133_dyadic_packet_transport_gauge_archived",
        "theorem": {
            "natural_dyadic_exact_gram_lift": True,
            "principal_angle_only_obstruction": True,
            "relative_tail_coherence_sufficient_bound": True,
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
