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
        "rh77_model_builder": PAPERS / "RH-77-postblock-effective-rank-compression/experiments/run_effective_rank_audit.py",
        "rh82_rank_clock": PAPERS / "RH-82-half-log-postblock-rank-clock/src/half_log_rank/bounds.py",
        "rh94_source_audit": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh/experiments/run_source_seeded_horizon_audit.py",
        "rh96_audit": PAPERS / "RH-96-gap-weighted-weak-mode-quotient/results/weak_mode_quotient_audit.json",
        "rh96_summary": PAPERS / "RH-96-gap-weighted-weak-mode-quotient/results/summary.json",
        "rh142_audit": PAPERS / "RH-142-factorized-arb-snapshot-packet-closure/results/factorized_arb_audit.json",
        "rh142_summary": PAPERS / "RH-142-factorized-arb-snapshot-packet-closure/results/summary.json",
        "rh142_archive": PAPERS / "RH-142-factorized-arb-snapshot-packet-closure/results/archive_verification.json",
        "rh143_summary": PAPERS / "RH-143-threshold-branch-stability-radius/results/summary.json",
        "rh143_archive": PAPERS / "RH-143-threshold-branch-stability-radius/results/archive_verification.json",
        "rh143_bounds": PAPERS / "RH-143-threshold-branch-stability-radius/src/threshold_branch/bounds.py",
        "rh149_roadmap": PAPERS / "RH-149-ten-layer-source-support-review/UPDATED_ROADMAP.md",
    }
    local = sorted({
        *(ROOT / "src").rglob("*.py"),
        *(ROOT / "experiments").glob("*.py"),
        *(ROOT / "tests").glob("*.py"),
    })
    publications = [ROOT / name for name in (
        ".gitignore",
        "README.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "references.bib",
        "pyproject.toml",
        "requirements.txt",
        "figures/temporal_anchor_packet_transport.pdf",
        "figures/temporal_anchor_packet_transport.png",
        "main.pdf",
        "temporal-anchor-packet-transport-obstruction.pdf",
    )]
    dependency = {
        "status": "all_rh150_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)}
            for key, path in external.items()
        },
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results/dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results/packet_transport_audit.json").read_text())
    result_files = [ROOT / "results" / name for name in (
        "packet_transport_audit.json",
        "packet_transport_smoke.json",
        "dependency_manifest.json",
    )]
    summary = {
        "status": "rh150_temporal_anchor_packet_transport_obstruction_archived",
        "theorem": {
            "typed_temporal_rank_anchor": True,
            "outward_one_step_packet_transport": True,
            "finite_universal_information_obstruction": True,
        },
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
