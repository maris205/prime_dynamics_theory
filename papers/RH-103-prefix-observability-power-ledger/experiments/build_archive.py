"""Build RH-103 dependency, result, and publication hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}


def main() -> None:
    external = {
        "rh52_summary": PAPERS / "RH-52-intrinsic-peripheral-residue-transfer" / "results" / "summary.json",
        "rh54_summary": PAPERS / "RH-54-factor-aware-intrinsic-identification" / "results" / "summary.json",
        "rh74_audit": PAPERS / "RH-74-validated-upstream-hardy-bridge" / "results" / "validated_upstream_bridge_audit.json",
        "rh75_audit": PAPERS / "RH-75-log-square-block-contraction-law" / "results" / "log_square_block_audit.json",
        "rh77_audit": PAPERS / "RH-77-postblock-effective-rank-compression" / "results" / "effective_rank_audit.json",
        "rh78_audit": PAPERS / "RH-78-two-corridor-stage-A1-composition" / "results" / "stage_composition_audit.json",
        "rh82_audit": PAPERS / "RH-82-half-log-postblock-rank-clock" / "results" / "half_log_rank_audit.json",
        "rh100_roadmap": PAPERS / "RH-100-hundred-layer-route-review" / "UPDATED_ROADMAP.md",
        "rh101_audit": PAPERS / "RH-101-finite-memory-packet-gram-action" / "results" / "finite_memory_gram_audit.json",
        "rh102_audit": PAPERS / "RH-102-stopped-hybrid-quotient-clock" / "results" / "stopped_hybrid_clock_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "prefix_observability_power_ledger.pdf",
        ROOT / "figures" / "prefix_observability_power_ledger.png",
        ROOT / "main.pdf",
        ROOT / "prefix-observability-power-ledger.pdf",
    ]
    dependency = {
        "status": "all_rh103_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ledger = json.loads((ROOT / "results" / "prefix_observability_power_ledger.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "prefix_observability_power_ledger.json",
        ROOT / "results" / "prefix_observability_power_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh103_prefix_observability_power_ledger_archived",
        "theorem": {
            "explicit_directional_norm_ledger": True,
            "signed_max_plus_power_composition": True,
            "prefix_independence_barrier": True,
            "observation_independence_barrier": True,
        },
        "audit": ledger["audit_summary"],
        "program_boundary": ledger["theorem_boundary"],
        "route_consequence": ledger["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **ledger["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
