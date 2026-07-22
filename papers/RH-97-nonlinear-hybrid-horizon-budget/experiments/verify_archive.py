"""Verify RH-97 hashes, hybrid budgets, negative thresholds, and boundaries."""

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
    audit = load("results/hybrid_horizon_budget_audit.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]: raise RuntimeError(f"external hash mismatch: {path}")

    values = audit["audit_summary"]
    if len(audit["rows"]) != 5 or not audit["all_executed_primary_hybrid_budget_gates_green"]: raise RuntimeError("hybrid audit incomplete")
    if values["primary_omission_count"] != 5 or values["primary_telescoping_green_count"] != 10: raise RuntimeError("primary hybrid counts changed")
    if values["primary_maximum_absolute_horizon_budget_to_reference"] >= 1.1e-5: raise RuntimeError("primary absolute budget changed")
    if values["threshold_summaries"]["1e-06"]["maximum_absolute_horizon_budget_to_reference"] <= 0.02: raise RuntimeError("1e-6 negative branch changed")
    if values["threshold_summaries"]["1e-04"]["maximum_absolute_horizon_budget_to_reference"] <= 0.014: raise RuntimeError("1e-4 negative branch changed")
    if not all(summary["theorem"].values()): raise RuntimeError("theorem gate missing")
    for key in ("a_priori_refresh_lipschitz_law_proved", "uniform_block_propagation_envelope_proved", "repeated_block_contraction_proved", "uniform_stage_A1_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        if summary["program_boundary"][key]: raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("nonlinear hybrid telescoping theorem", "absolute propagated horizon budget", "sparse-decision reduction", "hybrid replay", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript: raise RuntimeError(f"missing phrase: {phrase}")

    archived = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "nonlinear-hybrid-horizon-budget.pdf", ROOT / "figures" / "nonlinear_hybrid_horizon_budget.pdf", ROOT / "figures" / "nonlinear_hybrid_horizon_budget.png", ROOT / "results" / "hybrid_horizon_budget_audit.json", ROOT / "results" / "hybrid_horizon_budget_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_hybrid_budgets_negative_thresholds_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
