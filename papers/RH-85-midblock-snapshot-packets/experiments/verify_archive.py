"""Verify RH-85 hashes, packet gates, and claim boundaries."""

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
    audit = load("results/snapshot_packet_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_packet_gates_green"]:
        raise RuntimeError("snapshot packet audit incomplete")
    if audit["audit_summary"]["maximum_interval_relative_terminal_residual"] >= 4.5e-6:
        raise RuntimeError("packet residual gate failed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in ("all_level_packet_decay_proved", "uniform_stage_A1_closed", "riemann_hypothesis"):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")
    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("snapshot transfer theorem", "prefix-only certificate", "unweighted prefix-gramian no-go", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")
    archived = [ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "midblock-snapshot-packets.pdf", ROOT / "figures" / "midblock_snapshot_packets.pdf", ROOT / "figures" / "midblock_snapshot_packets.png", ROOT / "results" / "snapshot_packet_audit.json", ROOT / "results" / "snapshot_packet_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_snapshot_packet_gates_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
