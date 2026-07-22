"""Build RH-77 archive manifests."""

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
        "rh70_frozen_audit": PAPERS / "RH-70-frozen-production-block-hardy-audit" / "results" / "frozen_production_interval_audit.json",
        "rh76_phase_summary": PAPERS / "RH-76-single-arc-phase-compression-barrier" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "postblock_effective_rank_compression.pdf", ROOT / "figures" / "postblock_effective_rank_compression.png", ROOT / "main.pdf", ROOT / "postblock-effective-rank-compression.pdf"]
    dependency = {"status": "all_rh77_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    result_paths = [ROOT / "results" / "effective_rank_audit.json", ROOT / "results" / "effective_rank_smoke.json", dependency_path]
    summary = {
        "status": "rh77_postblock_effective_rank_compression_archived",
        "theorem": {"block_observability_upper": True, "full_future_low_rank_transfer": True, "eckart_young_optimal_residual": True},
        "audit": {"scale_count": len(audit["rows"]), "channel_count": len(channels), "all_rank_gates_green": audit["all_executed_rank_gates_green"], "maximum_participation_rank": max(c["rank_diagnostics"]["participation_rank_diagnostic"] for c in channels), "minimum_rank2_capture": min(c["validated_rank_compression"]["rank_2"]["energy_capture_lower"] for c in channels), "minimum_rank4_capture": min(c["validated_rank_compression"]["rank_4"]["energy_capture_lower"] for c in channels), "maximum_rank4_future_hardy_error": max(c["validated_rank_compression"]["rank_4"]["full_future_hardy_perturbation_upper"] for c in channels)},
        "program_boundary": {"frozen_rank4_compression_validated": True, "uniform_analytic_effective_rank_proved": False, "uniform_stage_A1_closed": False, "stage_A4_unconditional_closed": False, "hilbert_polya_operator": False, "riemann_hypothesis": False},
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "channel_count": len(channels)}, sort_keys=True))


if __name__ == "__main__":
    main()
