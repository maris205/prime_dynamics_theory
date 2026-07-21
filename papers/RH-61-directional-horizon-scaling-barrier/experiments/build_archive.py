"""Build RH-61 dependency, result, and publication hashes."""

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


def external_inputs() -> dict[str, Path]:
    return {
        "rh59_metric_pilot": PAPERS
        / "RH-59-flag-adapted-schur-stein-metrics"
        / "results"
        / "flag_metric_pilot.json",
        "rh60_phase_pilot": PAPERS
        / "RH-60-finite-horizon-phase-aware-tails"
        / "results"
        / "phase_tail_pilot.json",
        "rh60_manuscript": PAPERS
        / "RH-60-finite-horizon-phase-aware-tails"
        / "main.tex",
    }


def main() -> None:
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
        ROOT / "figures" / "directional_horizon_scaling.pdf",
        ROOT / "figures" / "directional_horizon_scaling.png",
        ROOT / "main.pdf",
        ROOT / "directional-horizon-scaling-barrier.pdf",
    ]
    dependency = {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: entry(path) for name, path in external_inputs().items()
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
        (ROOT / "results" / "horizon_scaling_audit.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_horizon_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "horizon_scaling_audit.json",
        ROOT / "results" / "horizon_scaling_smoke.json",
        ROOT / "results" / "arb_horizon_audit.json",
        dependency_path,
    ]
    endpoint = audit["rows"][-1]
    summary = {
        "status": "rh61_directional_horizon_scaling_and_stein_barrier_audit",
        "theorem": {
            "packetwise_geometric_envelope": True,
            "exact_integer_horizon_search": True,
            "reducing_slow_mode_lower_bound": True,
            "power_gap_horizon_obstruction": True,
        },
        "program_boundary": audit["program_boundary"],
        "pilot": {
            "rows": len(audit["rows"]),
            "fits": audit["fits"],
            "endpoint": {
                "sigma": endpoint["sigma"],
                "left_phase_upper_ratio": endpoint["left"]["horizons"][
                    "32"
                ]["phase_upper_over_exact"],
                "right_phase_upper_ratio": endpoint["right"]["horizons"][
                    "32"
                ]["phase_upper_over_exact"],
                "left_phase_tail": endpoint["left"]["horizons"]["32"][
                    "phase_tail_sum"
                ],
                "right_phase_tail": endpoint["right"]["horizons"]["32"][
                    "phase_tail_sum"
                ],
                "left_geometric_horizon_05": endpoint["left"][
                    "geometric_horizons"
                ]["0.05"],
                "right_geometric_horizon_05": endpoint["right"][
                    "geometric_horizons"
                ]["0.05"],
            },
        },
        "arb": {
            "status": arb["status"],
            "precision_bits": arb["precision_bits"],
            "slow_mode_upper": arb[
                "slow_mode_upper_at_horizon_certified"
            ],
            "slow_mode_lower": arb[
                "slow_mode_failure_before_horizon_certified"
            ],
            "geometric_upper": arb[
                "geometric_upper_at_horizon_certified"
            ],
            "geometric_lower": arb[
                "geometric_failure_before_horizon_certified"
            ],
            "equality_case": arb["stein_tail_equality_case_certified"],
            "production_interval_audit_executed": arb[
                "production_interval_audit_executed"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
        "limitations": audit["limitations"],
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
                "result_count": len(result_paths),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
