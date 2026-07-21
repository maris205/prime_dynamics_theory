"""Build RH-60 dependency, result, and publication hashes."""

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
        "rh59_manuscript": PAPERS
        / "RH-59-flag-adapted-schur-stein-metrics"
        / "main.tex",
        "rh59_pilot": PAPERS
        / "RH-59-flag-adapted-schur-stein-metrics"
        / "results"
        / "flag_metric_pilot.json",
        "rh59_algebra": PAPERS
        / "RH-59-flag-adapted-schur-stein-metrics"
        / "src"
        / "flag_stein"
        / "algebra.py",
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
        ROOT / "figures" / "finite_horizon_phase_tail.pdf",
        ROOT / "figures" / "finite_horizon_phase_tail.png",
        ROOT / "main.pdf",
        ROOT / "finite-horizon-phase-aware-tails.pdf",
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
        ROOT / "results" / "phase_tail_pilot.json",
        ROOT / "results" / "phase_tail_pilot_smoke.json",
        ROOT / "results" / "arb_phase_tail_audit.json",
        dependency_path,
    ]
    pilot = json.loads(
        (ROOT / "results" / "phase_tail_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_phase_tail_audit.json").read_text(
            encoding="utf-8"
        )
    )
    smallest = pilot["rows"][-1]
    summary = {
        "status": "rh60_phase_aware_finite_horizon_and_stein_tail_audit",
        "theorem": {
            "finite_horizon_gram_positivity": True,
            "loewner_finite_horizon_stein_completion": True,
            "phase_aware_global_completion": True,
            "packetwise_hybrid_completion": True,
            "geometric_tail_decay": True,
        },
        "program_boundary": {
            "uniform_physical_horizon": False,
            "continuum_phase_gram_theorem": False,
            "polylogarithmic_tail_theorem": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "production_interval_audit": False,
            "arithmetic_trace_formula": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "rows": len(pilot["rows"]),
            "status": pilot["status"],
            "selected_horizon": pilot["selected_horizon"],
            "fits": pilot["fits"],
            "smallest_scale": {
                "sigma": smallest["sigma"],
                "left_exact": smallest["left"]["exact_hardy_energy"],
                "right_exact": smallest["right"]["exact_hardy_energy"],
                "left_upper": smallest["left"][
                    "selected_phase_aware_upper"
                ],
                "right_upper": smallest["right"][
                    "selected_phase_aware_upper"
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
                "supersolution_positive_definite_certified"
            ],
            "tail_certified": arb["tail_upper_certified"],
            "completion_certified": arb["completion_upper_certified"],
            "production_interval_audit_executed": arb[
                "production_interval_audit_executed"
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
