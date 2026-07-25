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
        "rh154_audit": PAPERS / "RH-154-half-horizon-delayed-reset-suffix/results/suffix_audit.json",
        "rh156_audit": PAPERS / "RH-156-native-reset-support-floor/results/support_audit.json",
        "rh156_summary": PAPERS / "RH-156-native-reset-support-floor/results/summary.json",
        "rh156_archive": PAPERS / "RH-156-native-reset-support-floor/results/archive_verification.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/spectral_reset_cross_action_cancellation.pdf",
        "figures/spectral_reset_cross_action_cancellation.png", "main.pdf", "spectral-reset-cross-action-cancellation.pdf",
    )]
    dependency = {
        "status": "all_rh157_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    audit = json.loads((ROOT / "results/cross_audit.json").read_text())
    result_files = [ROOT / "results" / name for name in ("cross_audit.json", "cross_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh157_spectral_reset_cross_action_cancellation_archived",
        "theorem": {"exact_cross_cancellation": True, "tail_coupling_radius": True, "no_positive_native_cross_lower": True},
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
