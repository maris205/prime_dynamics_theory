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
        "rh141_audit": ROOT.parent / "RH-141-gap-stable-spectral-packet-enclosure/results/spectral_packet_audit.json",
        "rh141_summary": ROOT.parent / "RH-141-gap-stable-spectral-packet-enclosure/results/summary.json",
        "rh141_source": ROOT.parent / "RH-141-gap-stable-spectral-packet-enclosure/src/spectral_packet/enclosure.py",
        "rh77_model_source": ROOT.parent / "RH-77-postblock-effective-rank-compression/experiments/run_effective_rank_audit.py",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/factorized_arb_snapshot_packet.pdf",
        "figures/factorized_arb_snapshot_packet.png", "main.pdf", "factorized-arb-snapshot-packet-closure.pdf",
    )]
    dependency = {
        "status": "all_rh142_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "factorized_arb_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("factorized_arb_audit.json", "factorized_arb_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh142_factorized_arb_snapshot_packet_closure_archived",
        "theorem": {"factorized_normalized_gap_lower": True, "direct_arb_snapshot_enclosure": True, "hybrid_packet_closure": True},
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

