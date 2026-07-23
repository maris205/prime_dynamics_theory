"""Verify RH-104 hashes, prefix certificates, barrier, and claim boundary."""

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
    audit = load("results/prefix_transient_audit.json")
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
    if len(audit["rows"]) != 5 or values["channel_count"] != 10:
        raise RuntimeError("five-anchor prefix audit failed")
    if values["maximum_actual_directional_prefix_energy"] >= 1.77:
        raise RuntimeError("directional prefix envelope changed")
    if values["maximum_source_block_energy"] >= 3.11:
        raise RuntimeError("source block envelope changed")
    if values["maximum_crude_prefix_upper"] <= 28.0:
        raise RuntimeError("crude-product separation disappeared")
    if values["maximum_crude_to_directional_ratio"] <= 16.0:
        raise RuntimeError("directional advantage disappeared")
    barrier = audit["barrier"]
    if barrier["block_contraction"] != 0.0 or barrier["normalized_packet_relative_tail"] != 0.0:
        raise RuntimeError("nilpotent barrier changed")
    if abs(barrier["prefix_energy_power"] - 1.5) >= 1e-12:
        raise RuntimeError("barrier power changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "uniform_directional_prefix_law_proved",
        "block_contraction_alone_closes_prefix",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "exact directional prefix identity",
        "source-weighted block-tail transfer",
        "dyadic source-weighted finite-prefix criterion",
        "block-contraction and packet-normalization barrier",
        "uniform directional prefix control remains open",
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
        ROOT / "source-weighted-prefix-law.pdf",
        ROOT / "figures" / "source_weighted_prefix_law.pdf",
        ROOT / "figures" / "source_weighted_prefix_law.png",
        ROOT / "results" / "prefix_transient_audit.json",
        ROOT / "results" / "prefix_transient_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_prefix_laws_nilpotent_barrier_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
