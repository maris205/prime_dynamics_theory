"""Build RH-63 dependency and publication hashes."""

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
        "rh62_pilot": PAPERS
        / "RH-62-krylov-residual-stein-tails"
        / "results"
        / "krylov_tail_pilot.json",
        "rh61_audit": PAPERS
        / "RH-61-directional-horizon-scaling-barrier"
        / "results"
        / "horizon_scaling_audit.json",
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
        ROOT / "figures" / "nested_krylov_closure.pdf",
        ROOT / "figures" / "nested_krylov_closure.png",
        ROOT / "main.pdf",
        ROOT / "nested-krylov-residual-closure.pdf",
    ]
    dependency = {
        "status": "all_rh63_inputs_sources_and_publication_artifacts_hashed",
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
        (ROOT / "results" / "nested_krylov_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_nested_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "nested_krylov_pilot.json",
        ROOT / "results" / "nested_krylov_smoke.json",
        ROOT / "results" / "arb_nested_audit.json",
        dependency_path,
    ]
    summary = {
        "status": "rh63_nested_krylov_residual_closure_audit",
        "theorem": {
            "coherent_nested_identity": True,
            "positive_terminal_remainder": True,
            "breakdown_exactness": True,
        },
        "program_boundary": {
            "uniform_residual_depth": False,
            "terminal_directional_propagator": False,
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
                    "one_level_gain": model["one_level_endpoint_gain"],
                    "fully_nested_gain": model[
                        "fully_nested_endpoint_gain"
                    ],
                }
                for model in pilot["models"]
            ],
        },
        "arb": {
            "precision_bits": arb["precision_bits"],
            "coherent_identity_certified": arb[
                "coherent_identity_certified"
            ],
            "terminal_residual_zero_certified": arb[
                "terminal_residual_zero_certified"
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
