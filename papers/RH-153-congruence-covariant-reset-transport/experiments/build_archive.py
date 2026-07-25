from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = ROOT.parent


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    external = {
        "rh151_audit": PAPERS / "RH-151-ky-fan-reset-packet-atlas/results/reset_packet_audit.json",
        "rh151_summary": PAPERS / "RH-151-ky-fan-reset-packet-atlas/results/summary.json",
        "rh152_audit": PAPERS / "RH-152-reset-transition-overlap-coherence/results/overlap_audit.json",
        "rh152_summary": PAPERS / "RH-152-reset-transition-overlap-coherence/results/summary.json",
        "rh152_archive": PAPERS / "RH-152-reset-transition-overlap-coherence/results/archive_verification.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/congruence_covariant_reset_transport.pdf",
        "figures/congruence_covariant_reset_transport.png", "main.pdf", "congruence-covariant-reset-transport.pdf",
    )]
    dependency = {
        "status": "all_rh153_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    audit = json.loads((ROOT / "results/congruence_audit.json").read_text())
    result_files = [ROOT / "results" / name for name in ("congruence_audit.json", "congruence_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh153_congruence_covariant_reset_transport_archived",
        "theorem": {
            "loewner_congruence_covariance": True,
            "generalized_tail_ratio_invariance": True,
            "sharp_transported_base_lower": True,
            "independent_inverse_congruence_radius": True,
        },
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
