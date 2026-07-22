"""Verify RH-94 hashes, horizon gates, and claim boundaries."""

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
    audit = load("results/source_seeded_horizon_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_source_seeded_gates_green"]:
        raise RuntimeError("source-seeded audit incomplete")
    if values["primary_update_count"] != 120 or values["width_four_endpoint_green_count"] != 10:
        raise RuntimeError("full-prefix update count changed")
    if values["maximum_width_four_endpoint_to_reference_ratio"] >= 1.01:
        raise RuntimeError("width-four endpoint gate failed")
    if values["maximum_width_two_endpoint_to_reference_ratio"] <= 11.0 or values["maximum_width_three_endpoint_to_reference_ratio"] <= 1.4:
        raise RuntimeError("width threshold evidence changed")
    if values["minimum_width_four_cross_energy_fraction"] <= 0.975:
        raise RuntimeError("width-four cross capture changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "source_coordinate_svd_removed",
        "ambient_gram_packet_action_removed",
        "uniform_all_level_four_direction_law_proved",
        "uniform_stage_A1_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "source-seed equivalence",
        "source-seeded recursive horizon theorem",
        "width four",
        "late ambient seed",
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
        ROOT / "source-seeded-four-direction-horizon-refresh.pdf",
        ROOT / "figures" / "source_seeded_four_direction_horizon.pdf",
        ROOT / "figures" / "source_seeded_four_direction_horizon.png",
        ROOT / "results" / "source_seeded_horizon_audit.json",
        ROOT / "results" / "source_seeded_horizon_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_source_seeded_horizon_gates_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
