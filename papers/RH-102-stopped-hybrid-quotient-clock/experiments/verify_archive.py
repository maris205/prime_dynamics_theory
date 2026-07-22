"""Verify RH-102 hashes, stopped clocks, endpoint gates, and boundaries."""

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
    audit = load("results/stopped_hybrid_clock_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_stopped_clock_gates_green"]:
        raise RuntimeError("stopped clock audit failed")
    if values["all_threshold_chain_count"] != 30 or values["all_threshold_endpoint_green_count"] != 30:
        raise RuntimeError("clock count or endpoint gate changed")
    if values["primary_accepted_quotient_count"] != 5 or values["primary_stopped_channel_count"] != 0:
        raise RuntimeError("primary clock changed")
    medium = values["threshold_summary"]["1e-06"]
    coarse = values["threshold_summary"]["1e-04"]
    if medium["rejected_quotient_count"] != 1 or medium["stopped_channel_count"] != 1:
        raise RuntimeError("medium-threshold stop changed")
    if coarse["rejected_quotient_count"] != 2 or coarse["stopped_channel_count"] != 2:
        raise RuntimeError("coarse-threshold stops changed")
    if medium["maximum_unrestricted_endpoint_to_reference_ratio"] <= 1.02 or medium["maximum_final_endpoint_to_reference_ratio"] >= 1.01:
        raise RuntimeError("medium-threshold salvage changed")
    if coarse["maximum_unrestricted_endpoint_to_reference_ratio"] <= 1.014 or coarse["maximum_final_endpoint_to_reference_ratio"] >= 1.01:
        raise RuntimeError("coarse-threshold salvage changed")
    for row in audit["rows"]:
        for channel in row["channels"]:
            for chain in channel["chains"].values():
                if not (
                    chain["endpoint_gate_green"]
                    and chain["telescoping_error_contains_zero"]
                    and chain["all_hybrid_continuity_errors_contain_zero"]
                    and chain["all_accepted_local_gap_certificates_green"]
                ):
                    raise RuntimeError("individual stopped certificate failed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "hybrid_replay_removed",
        "uniform_gap_aware_quotient_law_proved",
        "uniform_stage_A_closed",
        "moving_cloud_A5_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "exact accepted-hybrid telescoping",
        "stopped hybrid endpoint-budget theorem",
        "local-global stopped composition",
        "a conservative stop",
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
        ROOT / "stopped-hybrid-quotient-clock.pdf",
        ROOT / "figures" / "stopped_hybrid_quotient_clock.pdf",
        ROOT / "figures" / "stopped_hybrid_quotient_clock.png",
        ROOT / "results" / "stopped_hybrid_clock_audit.json",
        ROOT / "results" / "stopped_hybrid_clock_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_stopped_clocks_endpoint_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
