"""Build RH-66 dependency and publication hashes."""

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
        "rh65_summary": PAPERS
        / "RH-65-physical-family-metric-conditioning"
        / "results"
        / "summary.json",
        "rh65_manuscript": PAPERS
        / "RH-65-physical-family-metric-conditioning"
        / "main.tex",
        "rh58_summary": PAPERS
        / "RH-58-time-ordered-schur-cross-gramian"
        / "results"
        / "summary.json",
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
        ROOT / "figures" / "block_cross_column_krylov_gram.pdf",
        ROOT / "figures" / "block_cross_column_krylov_gram.png",
        ROOT / "main.pdf",
        ROOT / "block-cross-column-krylov-gram.pdf",
    ]
    dependency = {
        "status": "all_rh66_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: entry(path) for name, path in external.items()
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
    pilot = json.loads(
        (ROOT / "results" / "block_gram_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_cancellation_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "block_gram_pilot.json",
        ROOT / "results" / "block_gram_smoke.json",
        ROOT / "results" / "arb_cancellation_audit.json",
        dependency_path,
    ]
    summary = {
        "status": "rh66_block_cross_column_krylov_gram_audit",
        "theorem": {
            "block_galerkin_power_identity": True,
            "directional_center_radius_certificate": True,
            "uniform_psd_gram_envelope": True,
            "exact_fused_cancellation_criterion": True,
            "invariant_block_exactness": True,
        },
        "program_boundary": {
            "coefficient_adapted_uniform_psd_envelope": False,
            "uniform_physical_family_block_depth": False,
            "production_interval_packet_transfer": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "model_count": len(pilot["models"]),
            "models": [
                {
                    "name": model["name"],
                    "dimension": model["dimension"],
                    "source_columns": model["source_columns"],
                    "horizon": model["horizon"],
                    "depths": model["depths"],
                }
                for model in pilot["models"]
            ],
        },
        "arb": {
            key: value
            for key, value in arb.items()
            if key.endswith("certified")
            or key in ("precision_bits", "production_interval_audit_executed")
        },
        "limitations": pilot["limitations"],
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
                "dependency_manifest": str(
                    dependency_path.relative_to(ROOT)
                ),
                "summary": str(summary_path.relative_to(ROOT)),
                "result_count": len(result_paths),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
