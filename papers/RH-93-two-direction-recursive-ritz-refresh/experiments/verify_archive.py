"""Verify RH-93 hashes, recursive gates, negative branch, and boundaries."""

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
    audit = load("results/two_direction_refresh_audit.json")
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

    values = audit["audit_summary"]
    if len(audit["rows"]) != 5 or not audit["all_executed_two_direction_gates_green"]:
        raise RuntimeError("two-direction audit incomplete")
    if values["two_direction_update_count"] != 40 or values["trial_frame_negative_count"] != 40:
        raise RuntimeError("trial-frame sign count changed")
    if values["one_direction_subquarter_failure_count"] != 4:
        raise RuntimeError("one-direction failure count changed")
    if values["two_direction_subquarter_block_count"] != 10:
        raise RuntimeError("two-direction block count changed")
    if values["maximum_two_direction_budget_geometric_mean"] >= 0.24 or values["maximum_two_direction_block_geometric_mean"] >= 0.24:
        raise RuntimeError("two-direction block target failed")
    if values["minimum_top_two_cross_energy_fraction"] <= 0.963:
        raise RuntimeError("top-two cross capture changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "uniform_all_level_two_direction_law_proved",
        "continuum_cross_direction_construction_proved",
        "uniform_stage_A1_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "two-direction recursive ritz refresh",
        "generalized trial-frame gain certificate",
        "recursive reduced block closure",
        "one direction fails",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")

    archived = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "two-direction-recursive-ritz-refresh.pdf",
        ROOT / "figures" / "two_direction_recursive_ritz_refresh.pdf",
        ROOT / "figures" / "two_direction_recursive_ritz_refresh.png",
        ROOT / "results" / "two_direction_refresh_audit.json",
        ROOT / "results" / "two_direction_refresh_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_recursive_two_direction_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
