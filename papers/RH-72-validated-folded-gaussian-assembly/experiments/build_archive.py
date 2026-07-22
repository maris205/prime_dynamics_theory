"""Build RH-72 dependency and publication hashes."""

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
        "rh14_folded_gaussian_source": PAPERS
        / "RH-14-square-root-parity-boundary-layer"
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh55_strong_weak_summary": PAPERS
        / "RH-55-strong-weak-riesz-cutoff-transfer"
        / "results"
        / "summary.json",
        "rh70_frozen_audit": PAPERS
        / "RH-70-frozen-production-block-hardy-audit"
        / "results"
        / "frozen_production_interval_audit.json",
        "rh71_route_summary": PAPERS
        / "RH-71-directional-tail-route-review"
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
        ROOT / "figures" / "validated_folded_gaussian_assembly.pdf",
        ROOT / "figures" / "validated_folded_gaussian_assembly.png",
        ROOT / "main.pdf",
        ROOT / "validated-folded-gaussian-assembly.pdf",
    ]
    dependency = {
        "status": "all_rh72_inputs_sources_and_publication_artifacts_hashed",
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
        (ROOT / "results" / "interval_assembly_audit.json").read_text(
            encoding="utf-8"
        )
    )
    rows = audit["rows"]
    result_paths = [
        ROOT / "results" / "interval_assembly_audit.json",
        ROOT / "results" / "interval_assembly_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh72_validated_folded_gaussian_assembly_archived",
        "theorem": {
            "algebraic_parameter_unique_root_interval": True,
            "exact_full_sparse_row_l1_identity": True,
            "exact_dyadic_stochastic_repair": True,
            "row_column_to_two_norm_enclosure": True,
            "haar_compressed_assembly_bound": True,
        },
        "audit": {
            "scale_count": len(rows),
            "all_rows_certified": audit["all_rows_certified"],
            "maximum_full_sparse_row_l1": max(
                row["maximum_full_to_sparse_row_l1_upper"] for row in rows
            ),
            "maximum_full_repaired_two_norm": max(
                row["full_to_repaired_matrix_defect"]["two_norm_upper"]
                for row in rows
            ),
            "maximum_compressed_repaired_two_norm": max(
                row["coarse_and_cross_block_two_norm_defect_upper"][
                    "against_repaired_pipeline"
                ]
                for row in rows
            ),
            "maximum_repair_correction": max(
                row["maximum_exact_repair_correction_upper"] for row in rows
            ),
            "minimum_repaired_pivot": min(
                row["minimum_repaired_pivot_lower"] for row in rows
            ),
            "minimum_support_floor_margin": min(
                row["minimum_support_center_floor_margin"] for row in rows
            ),
        },
        "program_boundary": {
            "stationary_left_vector_validated": False,
            "parity_riesz_pair_validated": False,
            "rank_two_deflation_validated": False,
            "complete_upstream_triple_validated": False,
            "uniform_small_noise_assembly_theorem": False,
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
                "scale_count": len(rows),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
