"""Verify RH-103 hashes, max-plus ledger, barriers, and claim boundaries."""

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
    ledger = load("results/prefix_observability_power_ledger.json")
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

    values = ledger["audit_summary"]
    if len(ledger["rows"]) != 5 or not values["all_finite_anchor_gates_green"]:
        raise RuntimeError("five-anchor ledger failed")
    if values["maximum_clock_rank"] != 7 or values["finite_memory_depth"] != 5:
        raise RuntimeError("packet overhead changed")
    if values["maximum_stopped_primary_endpoint_ratio"] >= 1.01:
        raise RuntimeError("stopped endpoint gate failed")
    if values["stress_identification_envelope_last"] >= values["stress_identification_envelope_first"]:
        raise RuntimeError("stress identification envelope no longer decreases")
    if abs(values["prefix_counterexample_fitted_power"] - 1.25) >= 1e-12:
        raise RuntimeError("prefix barrier power changed")
    if abs(values["observation_counterexample_fitted_power"] - 0.75) >= 1e-12:
        raise RuntimeError("observation barrier power changed")
    scenarios = {item["name"]: item for item in ledger["scenarios"]}
    if scenarios["one_sided_observability_leak"]["rh49_full_strict_mesh_range_green"]:
        raise RuntimeError("observation leak incorrectly green")
    if scenarios["two_sided_prefix_leak"]["rh49_full_strict_mesh_range_green"]:
        raise RuntimeError("prefix leak incorrectly green")
    if scenarios["observation_residual_cancellation"]["total_hardy_power"] != 0.0:
        raise RuntimeError("signed cancellation ledger changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "prefix_observability_gate_closed",
        "only_uniform_quotient_gate_remains",
        "uniform_stage_A_closed",
        "moving_cloud_A5_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "explicit prefix--packet--observability ledger",
        "max-plus directional hardy power theorem",
        "finite-prefix independence barrier",
        "observation independence barrier",
        "only the uniform quotient law",
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
        ROOT / "prefix-observability-power-ledger.pdf",
        ROOT / "figures" / "prefix_observability_power_ledger.pdf",
        ROOT / "figures" / "prefix_observability_power_ledger.png",
        ROOT / "results" / "prefix_observability_power_ledger.json",
        ROOT / "results" / "prefix_observability_power_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_max_plus_ledger_independence_barriers_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
