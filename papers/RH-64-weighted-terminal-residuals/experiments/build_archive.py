"""Build RH-64 dependency and publication hashes."""

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
    external = {
        "rh63_pilot": PAPERS
        / "RH-63-nested-krylov-residual-closure"
        / "results"
        / "nested_krylov_pilot.json",
        "rh63_manuscript": PAPERS
        / "RH-63-nested-krylov-residual-closure"
        / "main.tex",
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
        ROOT / "figures" / "weighted_terminal_residuals.pdf",
        ROOT / "figures" / "weighted_terminal_residuals.png",
        ROOT / "main.pdf",
        ROOT / "weighted-terminal-residuals.pdf",
    ]
    dependency = {
        "status": "all_rh64_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
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
    pilot = json.loads(
        (ROOT / "results" / "weighted_residual_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_weighted_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "weighted_residual_pilot.json",
        ROOT / "results" / "weighted_residual_smoke.json",
        ROOT / "results" / "arb_weighted_audit.json",
        dependency_path,
    ]
    summary = {
        "status": "rh64_weighted_terminal_residual_audit",
        "theorem": {
            "positive_lyapunov_metric": True,
            "strict_weighted_contraction": True,
            "weighted_nested_certificate": True,
            "conditioning_transfer": True,
        },
        "program_boundary": {
            "uniform_metric_conditioning": False,
            "block_cross_column_fusion": False,
            "production_physical_family": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "model_count": len(pilot["models"]),
            "models": [
                {
                    "name": model["name"],
                    "euclidean_norm": model["euclidean_operator_norm"],
                    "metric_contraction": model["metric_contraction"],
                    "metric_condition_number": model[
                        "metric_condition_number"
                    ],
                    "one_level_gain": model["one_level_endpoint_gain"],
                }
                for model in pilot["models"]
            ],
        },
        "arb": {
            "precision_bits": arb["precision_bits"],
            "metric_positive": arb[
                "metric_positive_definite_certified"
            ],
            "lyapunov_identity": arb["lyapunov_identity_certified"],
            "strict_contraction": arb[
                "strict_metric_contraction_certified"
            ],
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
