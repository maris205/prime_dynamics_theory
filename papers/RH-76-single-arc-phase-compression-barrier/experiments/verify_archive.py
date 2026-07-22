"""Verify RH-76 hashes, negative gates, and boundaries."""

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
    audit = load("results/phase_compression_audit.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]: raise RuntimeError(f"external hash mismatch: {path}")
    if len(audit["rows"]) != 5 or not audit["all_executed_moment_solves_certified"]: raise RuntimeError("phase audit incomplete")
    if audit["route_verdict"]["single_arc_phase_compression_supported"]: raise RuntimeError("negative verdict was lost")
    if summary["audit"]["full_depth_10_percent_channel_count"] != 9: raise RuntimeError("10-percent depth count changed")
    if summary["audit"]["full_depth_1_percent_channel_count"] != 10: raise RuntimeError("1-percent depth count changed")
    if not all(summary["theorem"].values()): raise RuntimeError("theorem gate missing")
    boundary = summary["program_boundary"]
    if boundary["single_arc_phase_route_supported"] or not boundary["frozen_schur_surrogate_certified"]: raise RuntimeError("route verdict changed")
    if any(value for key, value in boundary.items() if key not in ("single_arc_phase_route_supported", "frozen_schur_surrogate_certified")): raise RuntimeError("claim boundary overrun")
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in ("phase-measure projection identity", "arc binomial krylov upper", "moment-coherence lower", "failed branch", "frozen-schur normal surrogate", "stage a1", "riemann hypothesis"):
        if phrase not in manuscript: raise RuntimeError(f"missing phrase: {phrase}")
    archived = [ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "single-arc-phase-compression-barrier.pdf", ROOT / "figures" / "single_arc_phase_compression_barrier.pdf", ROOT / "figures" / "single_arc_phase_compression_barrier.png", ROOT / "results" / "phase_compression_audit.json", ROOT / "results" / "phase_compression_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_phase_barrier_gates_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
