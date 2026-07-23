"""Verify RH-107 hashes, support law, finite barrier, and claim boundary."""

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
    audit = load("results/source_seeded_support_audit.json")
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
    if len(audit["thresholds"]) != 3 or values["total_candidate_comparisons"] != 360:
        raise RuntimeError("support audit count changed")
    if values["total_weak_mode_events"] != 38:
        raise RuntimeError("weak-mode event count changed")
    if not values["all_finite_selector_equivalences_green"]:
        raise RuntimeError("selector equivalence failed")
    if not values["all_finite_fine_supports_empty"]:
        raise RuntimeError("fine support no longer empty")
    if values["primary_fine_support_start_level"] != 2:
        raise RuntimeError("primary fine boundary changed")
    if values["minimum_fine_support_margin"] <= 7.0:
        raise RuntimeError("fine support margin changed")
    if values["maximum_stopped_endpoint_ratio"] >= 1.007:
        raise RuntimeError("stopped endpoint gate changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "all_level_fine_support_separation_proved",
        "all_level_quotient_supply_closed",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "adaptive support equivalence",
        "coarse-support-to-price reduction",
        "support-reduced stopped endpoint law",
        "finite support-extrapolation barrier",
        "all-level asymptotic theorem",
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
        ROOT / "source-seeded-quotient-support-law.pdf",
        ROOT / "figures" / "source_seeded_quotient_support.pdf",
        ROOT / "figures" / "source_seeded_quotient_support.png",
        ROOT / "results" / "source_seeded_support_audit.json",
        ROOT / "results" / "source_seeded_support_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_support_reduction_finite_barrier_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
