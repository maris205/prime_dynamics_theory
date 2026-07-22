"""Build RH-76 archive manifests."""

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
        "rh58_schur_source": PAPERS / "RH-58-time-ordered-schur-cross-gramian" / "src" / "schur_fusion" / "algebra.py",
        "rh68_barrier_summary": PAPERS / "RH-68-phase-coherence-block-depth-barrier" / "results" / "summary.json",
        "rh75_scaling_summary": PAPERS / "RH-75-log-square-block-contraction-law" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "single_arc_phase_compression_barrier.pdf", ROOT / "figures" / "single_arc_phase_compression_barrier.png", ROOT / "main.pdf", ROOT / "single-arc-phase-compression-barrier.pdf"]
    dependency = {"status": "all_rh76_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "phase_compression_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    result_paths = [ROOT / "results" / "phase_compression_audit.json", ROOT / "results" / "phase_compression_smoke.json", dependency_path]
    summary = {
        "status": "rh76_single_arc_phase_compression_barrier_archived",
        "theorem": {"spectral_measure_krylov_identity": True, "arc_binomial_upper": True, "moment_coherence_lower": True},
        "audit": {"scale_count": len(audit["rows"]), "channel_count": len(channels), "all_moment_solves_certified": audit["all_executed_moment_solves_certified"], "maximum_99_percent_arc_width": max(c["weighted_arcs"]["mass_0.99"]["width_upper"] for c in channels), "minimum_finest_depth_M_residual": min(c["moment_gram"]["residual_lower"] for c in audit["rows"][-1]["channels"]), "full_depth_10_percent_channel_count": sum(c["required_depth_10_percent_diagnostic"] == c["horizon"] + 1 for c in channels), "full_depth_1_percent_channel_count": sum(c["required_depth_1_percent_diagnostic"] == c["horizon"] + 1 for c in channels)},
        "program_boundary": {"single_arc_phase_route_supported": False, "frozen_schur_surrogate_certified": True, "continuum_phase_measure_validated": False, "uniform_stage_A1_closed": False, "hilbert_polya_operator": False, "riemann_hypothesis": False},
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "channel_count": len(channels)}, sort_keys=True))


if __name__ == "__main__":
    main()
