"""Verify RH-96 hashes, quotient gates, threshold failures, and boundaries."""

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
    audit = load("results/weak_mode_quotient_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_primary_quotient_gates_green"]:
        raise RuntimeError("weak-mode quotient audit incomplete")
    if values["primary_update_count"] != 120 or values["primary_omitted_update_count"] != 5 or values["primary_gap_certificate_count"] != 5:
        raise RuntimeError("primary quotient counts changed")
    if values["primary_maximum_endpoint_to_reference_ratio"] >= 1.01 or values["primary_maximum_adaptive_to_full_tail_ratio"] >= 1.00001:
        raise RuntimeError("primary adaptive gate failed")
    if values["threshold_summaries"]["1e-06"]["all_endpoints_green"] or values["threshold_summaries"]["1e-04"]["all_endpoints_green"]:
        raise RuntimeError("aggressive-cutoff negative branch changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in ("weak_cross_modes_geometrically_identified", "uniform_retained_to_omitted_gap_proved", "uniform_adaptive_width_law_proved", "repeated_block_contraction_proved", "uniform_stage_A1_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("universal omitted-block bound", "gap-weighted weak-mode tail-loss theorem", "adaptive width", "local certificates do not compose automatically", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")

    archived = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "gap-weighted-weak-mode-quotient.pdf", ROOT / "figures" / "gap_weighted_weak_mode_quotient.pdf", ROOT / "figures" / "gap_weighted_weak_mode_quotient.png", ROOT / "results" / "weak_mode_quotient_audit.json", ROOT / "results" / "weak_mode_quotient_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_weak_mode_quotient_gates_negative_thresholds_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
