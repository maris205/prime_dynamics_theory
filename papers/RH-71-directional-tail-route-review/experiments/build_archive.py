"""Build RH-71 dependency, result, and publication hashes."""

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
    paper_directories = {
        62: "RH-62-krylov-residual-stein-tails",
        63: "RH-63-nested-krylov-residual-closure",
        64: "RH-64-weighted-terminal-residuals",
        65: "RH-65-physical-family-metric-conditioning",
        66: "RH-66-block-cross-column-krylov-gram",
        67: "RH-67-physical-covariance-block-envelopes",
        68: "RH-68-phase-coherence-block-depth-barrier",
        69: "RH-69-adaptive-certificate-portfolio",
        70: "RH-70-frozen-production-block-hardy-audit",
    }
    external_paths = {
        f"rh{number}_summary": PAPERS
        / directory
        / "results"
        / "summary.json"
        for number, directory in paper_directories.items()
    }
    external_paths["rh70_interval_audit"] = (
        PAPERS
        / paper_directories[70]
        / "results"
        / "frozen_production_interval_audit.json"
    )
    external_paths["roadmap_after_rh50"] = (
        PAPERS / "RH-ROADMAP-after-RH50.md"
    )
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
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "directional_tail_route_review.pdf",
        ROOT / "figures" / "directional_tail_route_review.png",
        ROOT / "main.pdf",
        ROOT / "directional-tail-route-review.pdf",
    ]
    dependency = {
        "status": "all_rh71_inputs_sources_and_publication_artifacts_hashed",
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

    route = json.loads(
        (ROOT / "results" / "route_review.json").read_text(encoding="utf-8")
    )
    arb = json.loads(
        (ROOT / "results" / "arb_bridge_slack_audit.json").read_text(
            encoding="utf-8"
        )
    )
    theorem_gate_count = sum(
        int(row["theorem_count"]) for row in route["paper_ledger"]
    )
    result_paths = [
        ROOT / "results" / "route_review.json",
        ROOT / "results" / "route_review_smoke.json",
        ROOT / "results" / "arb_bridge_slack_audit.json",
        ROOT / "results" / "arb_bridge_slack_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh71_directional_tail_route_review_archived",
        "theorem": route["theorem"],
        "audit": {
            "input_paper_count": len(route["paper_ledger"]),
            "synthesis_layer_count": len(route["paper_ledger"]) + 1,
            "archived_input_theorem_gate_count": theorem_gate_count,
            "bridge_row_count": len(arb["rows"]),
            "all_one_percent_slacks_positive": arb[
                "all_one_percent_slacks_positive"
            ],
            "minimum_one_percent_slack_lower": arb[
                "minimum_one_percent_slack_lower"
            ],
            "minimum_one_percent_relative_slack_lower": arb[
                "minimum_one_percent_relative_slack_lower"
            ],
        },
        "frontiers": route["frontiers"],
        "stage_ledger": route["stage_ledger"],
        "program_boundary": route["program_boundary"],
        "route_consequence": route["route_consequence"],
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
                "input_papers": len(route["paper_ledger"]),
                "theorem_gates": theorem_gate_count,
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
