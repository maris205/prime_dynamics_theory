"""Build RH-59 dependency, result, and publication hashes."""

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
        "rh14_operator": PAPERS
        / "RH-14-square-root-parity-boundary-layer"
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh50_manuscript": PAPERS
        / "RH-50-two-pole-hilbert-schmidt-hardy"
        / "main.tex",
        "rh58_manuscript": PAPERS
        / "RH-58-time-ordered-schur-cross-gramian"
        / "main.tex",
        "rh58_algebra": PAPERS
        / "RH-58-time-ordered-schur-cross-gramian"
        / "src"
        / "schur_fusion"
        / "algebra.py",
        "rh58_pilot": PAPERS
        / "RH-58-time-ordered-schur-cross-gramian"
        / "results"
        / "schur_fusion_pilot.json",
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
        ROOT / "figures" / "flag_adapted_schur_stein.pdf",
        ROOT / "figures" / "flag_adapted_schur_stein.png",
        ROOT / "main.pdf",
        ROOT / "flag-adapted-schur-stein-metrics.pdf",
    ]
    dependency = {
        "status": (
            "all_consumed_inputs_sources_and_publication_artifacts_hashed"
        ),
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

    result_paths = [
        ROOT / "results" / "flag_metric_pilot.json",
        ROOT / "results" / "flag_metric_pilot_smoke.json",
        ROOT / "results" / "arb_flag_metric_audit.json",
        dependency_path,
    ]
    pilot = json.loads(
        (ROOT / "results" / "flag_metric_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_flag_metric_audit.json").read_text(
            encoding="utf-8"
        )
    )
    smallest = pilot["rows"][-1]
    summary = {
        "status": "rh59_flag_metric_exact_dissipation_and_outer_packet_audit",
        "theorem": {
            "canonical_local_lyapunov_metrics": True,
            "flag_block_diagonal_metric_existence": True,
            "packetwise_exact_dissipation_supersolution": True,
            "exact_dissipation_dominates_contraction": True,
            "two_block_endpoint_tradeoff": True,
        },
        "program_boundary": {
            "noise_uniform_hierarchical_weights": False,
            "polylogarithmic_packet_budget": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "production_interval_schur_metric": False,
            "arithmetic_trace_formula": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "rows": len(pilot["rows"]),
            "status": pilot["status"],
            "fits": pilot["fits"],
            "smallest_scale": {
                "sigma": smallest["sigma"],
                "left_metric_upper": smallest["left"][
                    "metric_absolute_upper"
                ],
                "right_metric_upper": smallest["right"][
                    "metric_absolute_upper"
                ],
                "left_outer_packet_upper": smallest["left"]["packets"][-1][
                    "metric_energy_upper"
                ],
                "right_outer_packet_upper": smallest["right"]["packets"][-1][
                    "metric_energy_upper"
                ],
            },
        },
        "arb": {
            "status": arb["status"],
            "precision_bits": arb["precision_bits"],
            "local_identities_certified": arb[
                "local_lyapunov_identities_certified"
            ],
            "dissipation_certified": arb[
                "dissipation_positive_definite_certified"
            ],
            "supersolution_certified": arb[
                "supersolution_positive_semidefinite_certified"
            ],
            "packet_upper_certified": arb["packet_upper_certified"],
            "production_interval_schur_metric_executed": arb[
                "production_interval_schur_metric_executed"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
        "limitations": pilot["limitations"],
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
