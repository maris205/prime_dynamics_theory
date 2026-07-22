"""Build RH-81 dependency, result, and publication hashes."""

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
    return {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}


def main() -> None:
    external = {}
    for number, directory in {
        72: "RH-72-validated-folded-gaussian-assembly",
        73: "RH-73-validated-peripheral-rank-two-deflation",
        74: "RH-74-validated-upstream-hardy-bridge",
        75: "RH-75-log-square-block-contraction-law",
        76: "RH-76-single-arc-phase-compression-barrier",
        77: "RH-77-postblock-effective-rank-compression",
        78: "RH-78-two-corridor-stage-A1-composition",
        79: "RH-79-intrinsic-determinant-diagonal-transfer",
        80: "RH-80-moving-cloud-relative-determinant",
    }.items():
        external[f"rh{number}_summary"] = PAPERS / directory / "results" / "summary.json"
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "stage_A_to_A5_route_review.pdf",
        ROOT / "figures" / "stage_A_to_A5_route_review.png",
        ROOT / "main.pdf",
        ROOT / "stage-A-to-A5-route-review.pdf",
    ]
    dependency = {
        "status": "all_rh81_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    review = json.loads((ROOT / "results" / "route_review.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "results" / "arb_frontier_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "route_review.json",
        ROOT / "results" / "route_review_smoke.json",
        ROOT / "results" / "arb_frontier_audit.json",
        ROOT / "results" / "arb_frontier_smoke.json",
        dependency_path,
    ]
    margin = {row["metric"]: row["certified_lower"] for row in audit["rows"]}
    summary = {
        "status": "rh81_stage_A_to_A5_route_review_archived",
        "theorem": review["theorem"],
        "ledger": {
            "input_paper_count": len(review["paper_ledger"]),
            "input_theorem_gate_count": review["input_theorem_gate_count"],
            "all_input_theorem_gates_true": review["all_input_theorem_gates_true"],
        },
        "minimal_completion_bundles": review["minimal_completion_bundles"],
        "audit": {
            "precision_bits": audit["precision_bits"],
            "all_margin_gates_green": audit["all_executed_margin_gates_green"],
            **margin,
        },
        "stage_ledger": review["stage_ledger"],
        "program_boundary": review["program_boundary"],
        "next_priority": review["next_priority"],
        "route_consequence": review["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "paper_count": len(review["paper_ledger"]), "stage_A_bundle_count": len(review["minimal_completion_bundles"]["stage_A1"])}, sort_keys=True))


if __name__ == "__main__":
    main()

