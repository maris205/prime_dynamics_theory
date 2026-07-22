"""Verify RH-81 hashes, completion frontiers, and theorem boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    review = load("results/route_review.json")
    audit = load("results/arb_frontier_audit.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external hash mismatch: {path}")
    if len(review["paper_ledger"]) != 9 or review["input_theorem_gate_count"] != 41:
        raise RuntimeError("ten-layer ledger incomplete")
    if not review["all_input_theorem_gates_true"] or not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    if len(review["minimal_completion_bundles"]["stage_A1"]) != 2:
        raise RuntimeError("Stage-A corridor count changed")
    a5 = review["minimal_completion_bundles"]["stage_A5_relative_fixed_disk_limit"]
    if len(a5) != 2 or any(len(bundle) != 4 for bundle in a5):
        raise RuntimeError("A5 completion antichain changed")
    if not audit["all_executed_margin_gates_green"]:
        raise RuntimeError("margin audit failed")
    boundary = summary["program_boundary"]
    for key in ("uniform_stage_A1_closed", "stage_A4_unconditional_closed", "stage_A5_relative_limit_closed", "canonical_scattering_object", "self_adjoint_generator", "T_log_T_counting_law", "prime_power_trace_formula", "completed_zeta_identity", "riemann_hypothesis"):
        if boundary[key]:
            raise RuntimeError(f"claim boundary overrun: {key}")
    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("monotone completion-antichain theorem", "current completion frontiers", "single-arc phase compression", "moving-cloud", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")
    roadmap = " ".join((ROOT / "UPDATED_ROADMAP.md").read_text(encoding="utf-8").lower().split())
    for phrase in ("immediate priority: rh-82", "all-level postblock", "fixed scalar pole cancellation", "claim boundary"):
        if phrase not in roadmap:
            raise RuntimeError(f"roadmap phrase missing: {phrase}")
    archived = [
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "stage-A-to-A5-route-review.pdf",
        ROOT / "figures" / "stage_A_to_A5_route_review.pdf",
        ROOT / "figures" / "stage_A_to_A5_route_review.png",
        ROOT / "results" / "route_review.json",
        ROOT / "results" / "route_review_smoke.json",
        ROOT / "results" / "arb_frontier_audit.json",
        ROOT / "results" / "arb_frontier_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_stage_A_to_A5_frontiers_margins_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()

