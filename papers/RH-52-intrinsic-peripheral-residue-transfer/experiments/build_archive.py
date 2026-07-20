"""Build dependency and publication archives for RH-52."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH51 = PAPERS / "RH-51-cyclic-rank-growing-horizon-stein"


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
        "rh14_boundary_layer_manuscript": RH14 / "main.tex",
        "rh14_folded_gaussian_source": RH14
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh47_log_conditioning_manuscript": RH47 / "main.tex",
        "rh49_directional_manuscript": RH49 / "main.tex",
        "rh49_stable_coupling_audit": RH49
        / "results"
        / "coupling_stable_rank_pilot.json",
        "rh50_hardy_manuscript": RH50 / "main.tex",
        "rh51_structured_stein_manuscript": RH51 / "main.tex",
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
        ROOT / "figures" / "factor_residue_transfer.pdf",
        ROOT / "figures" / "factor_residue_transfer.png",
        ROOT / "main.pdf",
        ROOT / "intrinsic-peripheral-residue-transfer.pdf",
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

    certificate_path = ROOT / "results" / "factor_transfer_certificate.json"
    result_paths = [
        certificate_path,
        ROOT / "results" / "factor_transfer_pilot.json",
        ROOT / "results" / "factor_transfer_pilot_smoke.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    audit = certificate["floating_five_scale_audit"]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "weak_finite_factor_theorem": certificate[
            "weak_finite_factor_theorem"
        ],
        "direct_kernel_bounds": certificate["direct_kernel_bounds"],
        "direct_residue_closure": certificate["direct_residue_closure"],
        "sharp_detail_barrier": certificate["sharp_detail_barrier"],
        "program_conclusion": certificate["program_conclusion"],
        "floating_five_scale_audit": {
            "noise_levels": audit["noise_levels"],
            "largest_dimension": audit["largest_dimension"],
            "fine_resolution_target": audit["fine_resolution_target"],
            "fits": audit["fits"],
            "maximum_parity_weak_condition_product": audit[
                "maximum_parity_weak_condition_product"
            ],
            "maximum_parity_sharp_detail_ratio": audit[
                "maximum_parity_sharp_detail_ratio"
            ],
            "maximum_parity_adjacent_left_l1_error": audit[
                "maximum_parity_adjacent_left_l1_error"
            ],
            "maximum_parity_adjacent_right_linf_error": audit[
                "maximum_parity_adjacent_right_linf_error"
            ],
            "maximum_parity_adjacent_projector_relative_defect": audit[
                "maximum_parity_adjacent_projector_relative_defect"
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
