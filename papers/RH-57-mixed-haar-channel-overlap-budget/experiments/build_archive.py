"""Build RH-57 dependency, result, and publication hashes."""

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
        "rh50_manuscript": PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy" / "main.tex",
        "rh51_pilot": PAPERS
        / "RH-51-cyclic-rank-growing-horizon-stein"
        / "results"
        / "structured_stein_pilot.json",
        "rh54_manuscript": PAPERS
        / "RH-54-factor-aware-intrinsic-identification"
        / "main.tex",
        "rh55_manuscript": PAPERS
        / "RH-55-strong-weak-riesz-cutoff-transfer"
        / "main.tex",
        "rh56_manuscript": PAPERS
        / "RH-56-growing-horizon-hard-space-barrier"
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
        ROOT / "figures" / "mixed_haar_channel_overlap.pdf",
        ROOT / "figures" / "mixed_haar_channel_overlap.png",
        ROOT / "main.pdf",
        ROOT / "mixed-haar-channel-overlap-budget.pdf",
    ]
    dependency = {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: entry(path) for name, path in external_inputs().items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in local_paths
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in publication_paths
        },
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    result_paths = [
        ROOT / "results" / "mixed_overlap_pilot.json",
        ROOT / "results" / "mixed_overlap_pilot_smoke.json",
        ROOT / "results" / "arb_block_audit.json",
        dependency_path,
    ]
    pilot = json.loads(
        (ROOT / "results" / "mixed_overlap_pilot.json").read_text(encoding="utf-8")
    )
    arb = json.loads(
        (ROOT / "results" / "arb_block_audit.json").read_text(encoding="utf-8")
    )
    summary = {
        "status": "rh57_cross_stein_identity_and_radial_block_route_audit",
        "theorem": {
            "cross_stein_identity": True,
            "requires_diagonalizability": False,
            "coherence_bound": True,
            "simple_mode_cauchy_kernel": True,
        },
        "program_boundary": {
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "production_interval_riesz_projector": False,
            "arithmetic_trace_formula": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "rows": len(pilot["rows"]),
            "status": pilot["status"],
            "fits": pilot["fits"],
        },
        "arb": {
            "status": arb["status"],
            "precision_bits": arb["precision_bits"],
            "gram_positive_certified": arb["gram_positive_certified"],
            "coherence_bound_certified": arb["coherence_bound_certified"],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
        "limitations": pilot["limitations"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
