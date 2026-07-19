"""Build dependency and publication archives for RH-51."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
ROADMAP = PAPERS / "RH-ROADMAP-after-RH50.md"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path):
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def external_inputs():
    return {
        "rh14_folded_gaussian_source": RH14
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh49_quarter_power_manuscript": RH49 / "main.tex",
        "rh50_hardy_stein_manuscript": RH50 / "main.tex",
        "rh50_hardy_certificate": RH50
        / "results"
        / "two_pole_hardy_certificate.json",
        "post_rh50_roadmap": ROADMAP,
    }


def main() -> None:
    local_sources = sorted(
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
        ROOT / "figures" / "structured_stein_geometry.pdf",
        ROOT / "figures" / "structured_stein_geometry.png",
        ROOT / "main.pdf",
        ROOT / "cyclic-rank-growing-horizon-stein-certificates.pdf",
    ]
    dependency = {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: repository_entry(path)
            for name, path in external_inputs().items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in local_sources
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

    certificate_path = ROOT / "results" / "structured_stein_certificate.json"
    result_paths = [
        certificate_path,
        ROOT / "results" / "structured_stein_pilot.json",
        ROOT / "results" / "structured_stein_pilot_smoke.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    audit = certificate["floating_five_scale_audit"]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "minimal_gramian": certificate["minimal_gramian"],
        "cyclic_rank_obstruction": certificate["cyclic_rank_obstruction"],
        "low_rank_plus_floor": certificate["low_rank_plus_floor"],
        "block_stein": certificate["block_stein"],
        "isotropic_block_completion": certificate[
            "isotropic_block_completion"
        ],
        "anisotropic_residual_completion": certificate[
            "anisotropic_residual_completion"
        ],
        "conic_dual_no_go": certificate["conic_dual_no_go"],
        "program_conclusion": certificate["program_conclusion"],
        "floating_five_scale_audit": {
            "noise_levels": audit["noise_levels"],
            "largest_dimension": audit["largest_dimension"],
            "resolution": audit["resolution"],
            "hardy_radius": audit["hardy_radius"],
            "left_cyclic_rank_power_fit": audit[
                "left_cyclic_rank_power_fit"
            ],
            "left_rank99_power_fit": audit["left_rank99_power_fit"],
            "right_rank99_power_fit": audit["right_rank99_power_fit"],
            "selected_horizon_log2_fit": audit[
                "selected_horizon_log2_fit"
            ],
            "maximum_left_block_relative_excess": audit[
                "maximum_left_block_relative_excess"
            ],
            "maximum_right_block_relative_excess": audit[
                "maximum_right_block_relative_excess"
            ],
            "identity_cone_obstructed_levels": audit[
                "identity_cone_obstructed_levels"
            ],
            "diagonal_extraction_failed_levels": audit[
                "diagonal_extraction_failed_levels"
            ],
            "finest_row": audit["rows"][-1],
            "interval_validated": audit["interval_validated"],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": certificate["limitations"],
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
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
