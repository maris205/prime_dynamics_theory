"""Verify RH-71 hashes, stack/frontier gates, and claim boundaries."""

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


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def verify_hashes(summary, dependency) -> None:
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"local source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external input hash mismatch: {path}")


def verify_review(summary, route, arb) -> None:
    if len(route["paper_ledger"]) != 9:
        raise RuntimeError("nine input papers were not audited")
    if summary["audit"]["synthesis_layer_count"] != 10:
        raise RuntimeError("ten-layer synthesis count changed")
    if summary["audit"]["archived_input_theorem_gate_count"] != 40:
        raise RuntimeError("input theorem gate count changed")
    for row in route["paper_ledger"]:
        if not row["all_theorem_gates_true"] or row["stage_A1_closed"]:
            raise RuntimeError("paper ledger boundary changed")
    if route["frontiers"]["finite_scale"] != [
        "upstream_interval_triple"
    ]:
        raise RuntimeError("finite-scale frontier changed")
    if set(route["frontiers"]["stage_A1"]) != {
        "upstream_interval_triple",
        "uniform_family_scaling",
    }:
        raise RuntimeError("Stage A1 frontier changed")
    if len(arb["rows"]) != 10:
        raise RuntimeError("bridge slack audit is incomplete")
    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision changed")
    if not arb["all_one_percent_slacks_positive"]:
        raise RuntimeError("one-percent bridge slack gate failed")
    if arb["minimum_one_percent_relative_slack_lower"] <= 0.0:
        raise RuntimeError("minimum bridge slack is not positive")
    for key, value in summary["theorem"].items():
        if not value:
            raise RuntimeError(f"theorem gate missing: {key}")
    for key, value in summary["program_boundary"].items():
        if value:
            raise RuntimeError(f"overclaimed boundary: {key}")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    roadmap = (ROOT / "UPDATED_ROADMAP.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in (
        "certificate-stack closure",
        "candidate-independent bridge",
        "first-open frontier",
        "two distinct frontiers",
        "upstream interval triple",
        "uniform family scaling",
        "rh-67 also corrected",
        "stage a1",
        "stage a5",
        "hilbert--polya",
        "t\\log t",
        "prime-power",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript phrase: {phrase}")
    for phrase in (
        "continuation, fallback, and stopping",
        "failure of the 1% bridge target alone is not a stopping condition",
        "t log t",
        "tpc branch remains an independent",
    ):
        if phrase not in roadmap:
            raise RuntimeError(f"missing roadmap phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    route = load("results/route_review.json")
    arb = load("results/arb_bridge_slack_audit.json")
    verify_hashes(summary, dependency)
    verify_review(summary, route, arb)
    verify_text()
    archived = [
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "directional-tail-route-review.pdf",
        ROOT / "figures" / "directional_tail_route_review.pdf",
        ROOT / "figures" / "directional_tail_route_review.png",
        ROOT / "results" / "route_review.json",
        ROOT / "results" / "route_review_smoke.json",
        ROOT / "results" / "arb_bridge_slack_audit.json",
        ROOT / "results" / "arb_bridge_slack_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_stack_frontiers_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "all_one_percent_slacks_positive": summary["audit"][
                "all_one_percent_slacks_positive"
            ],
            "finite_scale_frontier": summary["frontiers"]["finite_scale"],
            "stage_A1_closed": summary["program_boundary"][
                "uniform_stage_A1_closed"
            ],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "file_count": len(files),
                "status": payload["status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
