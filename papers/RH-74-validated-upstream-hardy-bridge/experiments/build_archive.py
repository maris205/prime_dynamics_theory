"""Build RH-74 dependency, result, and publication hashes."""

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
    external_paths = {
        "rh70_frozen_audit": PAPERS / "RH-70-frozen-production-block-hardy-audit" / "results" / "frozen_production_interval_audit.json",
        "rh71_bridge_slack": PAPERS / "RH-71-directional-tail-route-review" / "results" / "arb_bridge_slack_audit.json",
        "rh72_assembly_audit": PAPERS / "RH-72-validated-folded-gaussian-assembly" / "results" / "interval_assembly_audit.json",
        "rh73_peripheral_audit": PAPERS / "RH-73-validated-peripheral-rank-two-deflation" / "results" / "peripheral_validation_audit.json",
        "rh58_production_constructor": PAPERS / "RH-58-time-ordered-schur-cross-gramian" / "experiments" / "run_schur_fusion_pilot.py",
    }
    local_paths = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publication_paths = [
        ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex",
        ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt",
        ROOT / "figures" / "validated_upstream_hardy_bridge.pdf",
        ROOT / "figures" / "validated_upstream_hardy_bridge.png",
        ROOT / "main.pdf", ROOT / "validated-upstream-hardy-bridge.pdf",
    ]
    dependency = {
        "status": "all_rh74_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external_paths.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local_paths},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publication_paths},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "validated_upstream_bridge_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    result_paths = [
        ROOT / "results" / "validated_upstream_bridge_audit.json",
        ROOT / "results" / "validated_upstream_bridge_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh74_validated_upstream_hardy_bridge_archived",
        "theorem": {
            "analytic_stationary_factor_transfer": True,
            "analytic_bordered_parity_transfer": True,
            "normalized_coupling_perturbation": True,
            "complete_triple_error_enclosure": True,
            "volterra_power_perturbation": True,
            "robust_four_block_hardy_bridge": True,
            "finite_scale_end_to_end_composition": True,
        },
        "audit": {
            "scale_count": len(audit["rows"]),
            "channel_count": len(channels),
            "all_channels_green": audit["all_executed_channels_green"],
            "maximum_operator_error": max(c["triple_error"]["operator_two_norm_error_upper"] for c in channels),
            "maximum_source_error": max(c["triple_error"]["source_frobenius_error_upper"] for c in channels),
            "maximum_observation_error": max(c["triple_error"]["observation_frobenius_error_upper"] for c in channels),
            "maximum_bridge": max(c["robust_hardy_bridge"]["bridge_energy_upper"] for c in channels),
            "maximum_bridge_to_slack_ratio": max(c["bridge_to_slack_ratio_upper"] for c in channels),
            "maximum_true_block_contraction": max(c["robust_hardy_bridge"]["true_block_contraction_upper"] for c in channels),
        },
        "program_boundary": {
            "finite_scale_end_to_end_hardy_closed": True,
            "uniform_small_noise_family_bound": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "renormalized_determinant_limit_closed": False,
            "self_adjoint_generator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"dependency_manifest": str(dependency_path.relative_to(ROOT)), "summary": str(summary_path.relative_to(ROOT)), "channel_count": len(channels)}, sort_keys=True))


if __name__ == "__main__":
    main()
