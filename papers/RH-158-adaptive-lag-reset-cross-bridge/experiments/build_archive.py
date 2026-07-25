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
        "rh151_reset_audit": PAPERS / "RH-151-ky-fan-reset-packet-atlas/results/reset_packet_audit.json",
        "rh152_overlap_audit": PAPERS / "RH-152-reset-transition-overlap-coherence/results/overlap_audit.json",
        "rh154_suffix_audit": PAPERS / "RH-154-half-horizon-delayed-reset-suffix/results/suffix_audit.json",
        "rh157_summary": PAPERS / "RH-157-spectral-reset-cross-action-cancellation/results/summary.json",
        "rh157_archive": PAPERS / "RH-157-spectral-reset-cross-action-cancellation/results/archive_verification.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/adaptive_lag_reset_cross_bridge.pdf",
        "figures/adaptive_lag_reset_cross_bridge.png", "main.pdf", "adaptive-lag-reset-cross-bridge.pdf",
    )]
    dependency = {
        "status": "all_rh158_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    audit = json.loads((ROOT / "results/lag_audit.json").read_text())
    result_files = [ROOT / "results" / name for name in ("lag_audit.json", "lag_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh158_adaptive_lag_reset_cross_bridge_archived",
        "theorem": {
            "general_lag_identity": True,
            "scalar_centered_action_radius": True,
            "asymptotically_sharp_spread_coefficient": True,
            "finite_eight_lag_bridge": True,
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
