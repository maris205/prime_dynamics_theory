"""Verify RH-105 hashes, cancellation audit, and claim boundary."""

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
    audit = load("results/observation_residual_audit.json")
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
        raise RuntimeError("five-anchor cancellation audit failed")
    if values["maximum_clock_rank"] != 7:
        raise RuntimeError("clock rank changed")
    if values["maximum_sqrt_sigma_observation_factor"] >= 2.13:
        raise RuntimeError("matched observation factor changed")
    if values["maximum_residual_over_sqrt_sigma"] >= 3.08e-9:
        raise RuntimeError("normalized residual changed")
    if values["maximum_weighted_residual"] >= 5.05e-9:
        raise RuntimeError("weighted residual changed")
    if values["maximum_recomposition_discrepancy"] >= 1.0e-12:
        raise RuntimeError("recomposition is no longer exact")
    if values["sharp_barrier_weighted_growth_power"] != 0.25:
        raise RuntimeError("sharpness barrier changed")
    scenarios = {item["name"]: item for item in audit["scenarios"]}
    if not scenarios["matched_square_root"]["zero_power"]:
        raise RuntimeError("matched cancellation lost")
    if scenarios["undercancellation"]["zero_power"]:
        raise RuntimeError("undercancellation boundary lost")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "uniform_observation_growth_law_proved",
        "uniform_clock_residual_decay_law_proved",
        "uniform_observation_residual_law_closed",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "full-future residual transfer",
        "observation--residual cancellation law",
        "matched-scale factorization",
        "finite-propagator fallback",
        "scalar under-cancellation barrier",
        "zero weighted power",
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
        ROOT / "observation-residual-cancellation-law.pdf",
        ROOT / "figures" / "observation_residual_cancellation.pdf",
        ROOT / "figures" / "observation_residual_cancellation.png",
        ROOT / "results" / "observation_residual_audit.json",
        ROOT / "results" / "observation_residual_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_signed_cancellation_rate_boundary_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
