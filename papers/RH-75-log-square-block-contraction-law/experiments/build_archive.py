"""Build RH-75 archive manifests."""

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
        "rh74_true_bridge_audit": PAPERS / "RH-74-validated-upstream-hardy-bridge" / "results" / "validated_upstream_bridge_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "log_square_block_contraction.pdf", ROOT / "figures" / "log_square_block_contraction.png", ROOT / "main.pdf", ROOT / "log-square-block-contraction-law.pdf"]
    dependency = {
        "status": "all_rh75_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "log_square_block_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    result_paths = [ROOT / "results" / "log_square_block_audit.json", ROOT / "results" / "log_square_block_smoke.json", dependency_path]
    summary = {
        "status": "rh75_log_square_block_contraction_law_archived",
        "theorem": {"log_square_horizon_criterion": True, "square_root_mesh_cancellation": True, "polylogarithmic_hardy_consequence": True, "critical_one_half_exponent": True},
        "audit": {
            "scale_count": len(audit["rows"]), "channel_count": len(channels), "all_anchors_green": audit["all_executed_anchors_green"],
            "maximum_q_over_sqrt_sigma": max(c["normalized_q_over_sqrt_sigma_upper"] for c in channels),
            "maximum_observation_density": max(c["observation_density_upper"] for c in channels),
            "maximum_source_block": max(c["source_block_upper"] for c in channels),
            "maximum_actual_tail": max(c["actual_tail_energy_squared_upper"] for c in channels),
            "common_tail_envelope": max(c["uniform_tail_envelope_upper"] for c in channels),
        },
        "program_boundary": {"five_anchor_law_validated": True, "all_dyadic_levels_proved": False, "uniform_stage_A1_closed": False, "stage_A4_unconditional_closed": False, "hilbert_polya_operator": False, "riemann_hypothesis": False},
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "channel_count": len(channels)}, sort_keys=True))


if __name__ == "__main__":
    main()
