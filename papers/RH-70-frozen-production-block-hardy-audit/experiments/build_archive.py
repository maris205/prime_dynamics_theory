"""Build RH-70 dependency and publication hashes."""

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
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def main() -> None:
    external_paths = {
        "rh14_folded_gaussian_operator": PAPERS
        / "RH-14-square-root-parity-boundary-layer"
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh58_schur_fusion_pipeline": PAPERS
        / "RH-58-time-ordered-schur-cross-gramian"
        / "experiments"
        / "run_schur_fusion_pilot.py",
        "rh59_flag_metric_pipeline": PAPERS
        / "RH-59-flag-adapted-schur-stein-metrics"
        / "experiments"
        / "run_flag_metric_pilot.py",
        "rh60_phase_tail_pilot": PAPERS
        / "RH-60-finite-horizon-phase-aware-tails"
        / "results"
        / "phase_tail_pilot.json",
    }
    local_paths = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    publication_paths = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "frozen_production_block_hardy_audit.pdf",
        ROOT / "figures" / "frozen_production_block_hardy_audit.png",
        ROOT / "main.pdf",
        ROOT / "frozen-production-block-hardy-audit.pdf",
    ]
    dependency = {
        "status": "all_rh70_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: entry(path) for name, path in external_paths.items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in local_paths
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in publication_paths
        },
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    audit = json.loads(
        (ROOT / "results" / "frozen_production_interval_audit.json").read_text(
            encoding="utf-8"
        )
    )
    channels = [
        channel for row in audit["rows"] for channel in row["channels"]
    ]
    result_paths = [
        ROOT / "results" / "frozen_production_interval_audit.json",
        ROOT / "results" / "frozen_production_interval_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh70_frozen_production_block_hardy_audit_archived",
        "theorem": {
            "finite_prefix_block_power_tail_bound": True,
            "scalar_sharpness": True,
            "stable_matrix_eventual_block_contraction": True,
            "exact_dyadic_interval_execution_soundness": True,
            "augmented_difference_bridge": True,
        },
        "audit": {
            "scale_count": len(audit["rows"]),
            "channel_count": len(channels),
            "all_frozen_green": all(
                channel["frozen_matrix_green_at_one_percent"]
                for channel in channels
            ),
            "maximum_completion_factor": max(
                channel["relative_enclosure_width_upper"]
                for channel in channels
            ),
            "maximum_block_power_frobenius_upper": max(
                float(
                    channel["block_power_frobenius_ball"]
                    .split()[0]
                    .lstrip("[")
                )
                for channel in channels
            ),
            "all_archived_binary64_energies_enclosed": all(
                channel["archived_energy_inside_interval"]
                for channel in channels
            ),
        },
        "program_boundary": {
            "folded_gaussian_assembly_interval_enclosed": False,
            "spectral_deflation_interval_enclosed": False,
            "source_observation_transfer_interval_enclosed": False,
            "uniform_small_sigma_bound": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
        },
        "route_consequence": audit["route_consequence"],
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "dependency_manifest": str(dependency_path.relative_to(ROOT)),
                "summary": str(summary_path.relative_to(ROOT)),
                "channel_count": len(channels),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
