"""Verify RH-108 hashes, support certificate, barrier, and claim boundary."""

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
    audit = load("results/fourth_cross_support_audit.json")
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
    if values["scale_count"] != 5 or values["channel_count"] != 10 or values["update_count"] != 360:
        raise RuntimeError("support audit count changed")
    if values["fine_update_count"] != 234:
        raise RuntimeError("fine support count changed")
    if values["minimum_fine_certificate_margin_ratio"] <= 7.3:
        raise RuntimeError("fine support margin changed")
    if values["certificate_implication_violation_count"] != 0:
        raise RuntimeError("certificate implication failed")
    if values["selector_equivalence_failure_count"] != 0:
        raise RuntimeError("selector equivalence failed")
    if values["observed_cross_error_bound_failure_count"] != 0:
        raise RuntimeError("finite-memory tail bound failed")
    if not audit["barrier"]["trace_clock_constant"] or not audit["barrier"]["diagonal_blocks_constant"]:
        raise RuntimeError("barrier invariants changed")
    if audit["barrier"]["maximum_ratio_formula_error"] >= 1e-14:
        raise RuntimeError("barrier ratio formula changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem ledger is incomplete")
    for key in (
        "all_level_fourth_cross_lower_bound_proved",
        "source_seeded_physical_transversality_proved",
        "uniform_fine_support_separation_proved",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "finite-memory fourth-cross weyl certificate",
        "threshold form",
        "source-seeded normalized-memory barrier",
        "all-level physical fourth-cross lower bound",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript phrase: {phrase}")

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
        ROOT / "finite-memory-fourth-cross-support.pdf",
        ROOT / "figures" / "finite_memory_fourth_cross_support.pdf",
        ROOT / "figures" / "finite_memory_fourth_cross_support.png",
        ROOT / "results" / "fourth_cross_support_audit.json",
        ROOT / "results" / "fourth_cross_support_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_support_certificate_barrier_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
