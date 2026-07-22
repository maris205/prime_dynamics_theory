"""Verify RH-82 hashes, rank-clock gates, and claim boundaries."""

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
    audit = load("results/half_log_rank_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_clock_gates_green"]:
        raise RuntimeError("physical clock audit incomplete")
    if len(audit["endpoint_linear_row_model"]["rows"]) != 6:
        raise RuntimeError("endpoint model audit incomplete")
    if audit["audit_summary"]["maximum_relative_residual"] >= 2.4e-7:
        raise RuntimeError("postblock clock residual gate failed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    boundary = summary["program_boundary"]
    for key in ("actual_endpoint_postblock_factorization_proved", "uniform_stage_A1_closed", "stage_A4_unconditional_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        if boundary[key]:
            raise RuntimeError(f"claim boundary overrun: {key}")
    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("exponential excess-rank tail", "endpoint-to-postblock ideal-property transfer", "sufficient stage-a rank corridor", "actual endpoint-to-postblock factorization", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")
    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "half-log-postblock-rank-clock.pdf",
        ROOT / "figures" / "half_log_postblock_rank_clock.pdf",
        ROOT / "figures" / "half_log_postblock_rank_clock.png",
        ROOT / "results" / "half_log_rank_audit.json",
        ROOT / "results" / "half_log_rank_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_half_log_rank_clock_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()

