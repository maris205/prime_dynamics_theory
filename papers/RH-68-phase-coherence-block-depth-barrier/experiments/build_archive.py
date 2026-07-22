"""Build RH-68 dependency and publication hashes."""

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
        "rh67_summary": PAPERS
        / "RH-67-physical-covariance-block-envelopes"
        / "results"
        / "summary.json",
        "rh67_manuscript": PAPERS
        / "RH-67-physical-covariance-block-envelopes"
        / "main.tex",
        "rh61_summary": PAPERS
        / "RH-61-directional-horizon-scaling-barrier"
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
        ROOT / "figures" / "phase_coherence_block_depth_barrier.pdf",
        ROOT / "figures" / "phase_coherence_block_depth_barrier.png",
        ROOT / "main.pdf",
        ROOT / "phase-coherence-block-depth-barrier.pdf",
    ]
    dependency = {
        "status": "all_rh68_inputs_sources_and_publication_artifacts_hashed",
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
        (ROOT / "results" / "depth_barrier_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_fourier_ring_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "depth_barrier_pilot.json",
        ROOT / "results" / "depth_barrier_smoke.json",
        ROOT / "results" / "arb_fourier_ring_audit.json",
        dependency_path,
    ]
    summary = {
        "status": "rh68_phase_coherence_block_depth_barrier_audit",
        "theorem": {
            "exact_fourier_ring_depth_barrier": True,
            "canonical_metric_does_not_repair_ring": True,
            "spectral_projection_lower_bound": True,
            "mutual_coherence_block_bound": True,
            "universal_fixed_depth_no_go": True,
        },
        "program_boundary": {
            "production_phase_compression": False,
            "production_effective_rank_decay": False,
            "admissible_growing_depth_budget": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "exact_rings": pilot["exact_rings"],
            "jittered_rings": pilot["jittered_rings"],
            "phase_arcs": pilot["phase_arcs"],
        },
        "arb": {
            key: value
            for key, value in arb.items()
            if key.endswith("certified")
            or key in ("precision_bits", "production_interval_audit_executed")
        },
        "route_consequence": pilot["route_consequence"],
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
