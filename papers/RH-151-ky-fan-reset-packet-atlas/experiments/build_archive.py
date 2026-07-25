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
        "rh84_summary": PAPERS / "RH-84-ky-fan-tail-majorization/results/summary.json",
        "rh94_summary": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh/results/summary.json",
        "rh96_audit": PAPERS / "RH-96-gap-weighted-weak-mode-quotient/results/weak_mode_quotient_audit.json",
        "rh150_summary": PAPERS / "RH-150-temporal-anchor-packet-transport-obstruction/results/summary.json",
        "rh150_archive": PAPERS / "RH-150-temporal-anchor-packet-transport-obstruction/results/archive_verification.json",
        "rh150_roadmap": PAPERS / "RH-150-temporal-anchor-packet-transport-obstruction/UPDATED_ROADMAP.md",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/ky_fan_reset_packet_atlas.pdf",
        "figures/ky_fan_reset_packet_atlas.png", "main.pdf", "ky-fan-reset-packet-atlas.pdf",
    )]
    dependency = {
        "status": "all_rh151_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    audit = json.loads((ROOT / "results/reset_packet_audit.json").read_text())
    result_files = [ROOT / "results" / name for name in ("reset_packet_audit.json", "reset_packet_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh151_ky_fan_reset_packet_atlas_archived",
        "theorem": {"ky_fan_packet_angle": True, "branch_free_energy_recursion": True, "direct_reset_packet_atlas": True},
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
