"""Build RH-73 dependency, result, and publication hashes."""

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
        "rh14_operator_source": PAPERS / "RH-14-square-root-parity-boundary-layer" / "src" / "parity_boundary" / "operators.py",
        "rh42_grushin_source": PAPERS / "RH-42-uniform-euclidean-parity-contour" / "src" / "euclidean_contour" / "grushin.py",
        "rh72_repair_source": PAPERS / "RH-72-validated-folded-gaussian-assembly" / "src" / "folded_assembly" / "bounds.py",
        "rh72_summary": PAPERS / "RH-72-validated-folded-gaussian-assembly" / "results" / "summary.json",
    }
    local_paths = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publication_paths = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "validated_peripheral_rank_two.pdf",
        ROOT / "figures" / "validated_peripheral_rank_two.png",
        ROOT / "main.pdf",
        ROOT / "validated-peripheral-rank-two-deflation.pdf",
    ]
    dependency = {
        "status": "all_rh73_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external_paths.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local_paths},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publication_paths},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "peripheral_validation_audit.json").read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    result_paths = [
        ROOT / "results" / "peripheral_validation_audit.json",
        ROOT / "results" / "peripheral_validation_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh73_validated_peripheral_rank_two_deflation_archived",
        "theorem": {
            "stationary_neumann_validation": True,
            "perron_eigenvalue_simple": True,
            "bordered_newton_parity_pair": True,
            "left_parity_interval_solve": True,
            "normalized_projector_perturbation": True,
            "rank_two_bulk_deflation": True,
            "parity_contour_count_one": True,
        },
        "audit": {
            "scale_count": len(audit["rows"]),
            "channel_count": len(channels),
            "all_channels_green": audit["all_executed_channels_green"],
            "maximum_stationary_error": max(c["stationary"]["stationary_two_norm_error_upper"] for c in channels),
            "maximum_right_radius": max(c["parity_right"]["newton_radius_upper"] for c in channels),
            "maximum_left_error": max(c["parity_left"]["left_two_norm_error_upper"] for c in channels),
            "maximum_rank_two_projector_error": max(c["rank_two_projector_two_norm_error_upper"] for c in channels),
            "maximum_deflated_bulk_error": max(c["deflated_bulk_two_norm_error_upper"] for c in channels),
            "maximum_contour_transport": max(c["parity_contour"]["center_transport_product_upper"] for c in channels),
            "minimum_parity_gram_lower": min(c["approximate_parity_gram_lower"] for c in channels),
        },
        "program_boundary": {
            "source_observation_transfer_validated": False,
            "augmented_hardy_bridge_executed": False,
            "uniform_small_noise_peripheral_theorem": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
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
