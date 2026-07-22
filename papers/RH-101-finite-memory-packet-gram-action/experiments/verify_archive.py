"""Verify RH-101 hashes, action bounds, depth threshold, and boundaries."""

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
    audit = load("results/finite_memory_gram_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_action_bounds_green"]:
        raise RuntimeError("finite-memory action audit failed")
    if values["update_count"] != 120 or values["channel_count"] != 10:
        raise RuntimeError("audit count changed")
    if values["minimum_successful_uniform_depth"] != 5:
        raise RuntimeError("first common depth changed")
    if values["depth_summary"]["4"]["endpoint_green_count"] != 9:
        raise RuntimeError("depth-four negative channel changed")
    if values["depth_summary"]["5"]["endpoint_green_count"] != 10:
        raise RuntimeError("depth-five closure changed")
    if values["maximum_full_history_to_assembled_action_error"] >= 1e-14:
        raise RuntimeError("full-history action agreement degraded")
    if values["maximum_direct_to_structured_projector_distance"] <= 1e-4:
        raise RuntimeError("Ritz sensitivity boundary disappeared")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "state_packet_multiplication_removed",
        "source_coordinate_svd_removed",
        "uniform_all_level_ritz_stability_proved",
        "uniform_stage_A_closed",
        "moving_cloud_A5_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "structured finite-memory packet gram action theorem",
        "geometric packet-action tail",
        "first common tested depth",
        "sensitivity boundary",
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
        ROOT / "finite-memory-packet-gram-action.pdf",
        ROOT / "figures" / "finite_memory_packet_gram_action.pdf",
        ROOT / "figures" / "finite_memory_packet_gram_action.png",
        ROOT / "results" / "finite_memory_gram_audit.json",
        ROOT / "results" / "finite_memory_gram_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_action_bounds_depth_threshold_sensitivity_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
