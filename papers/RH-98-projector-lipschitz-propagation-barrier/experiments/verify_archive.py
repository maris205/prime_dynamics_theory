"""Verify RH-98 hashes, projector bounds, counterexample, and boundaries."""

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


def load(path: str): return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json"); dependency = load("results/dependency_manifest.json"); audit = load("results/projector_propagation_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_projector_bounds_green"]: raise RuntimeError("projector audit incomplete")
    if values["production_omission_count"] != 38 or values["production_unit_tail_roundoff_count"] != 38: raise RuntimeError("production omission count changed")
    if not values["production_all_gap_distance_bounds_green"] or not values["production_all_endpoint_lipschitz_bounds_green"] or not values["production_all_conditional_envelopes_green"]: raise RuntimeError("projector bound failed")
    if values["counterexample_tail_amplification_lower"] <= 44.0 or not audit["counterexample"]["unit_tail_propagation_rejected"]: raise RuntimeError("unit-propagation counterexample changed")
    if audit["counterexample"]["g1_minimum_eigenvalue"] <= 0.0 or audit["counterexample"]["g2_minimum_eigenvalue"] <= 0.0: raise RuntimeError("counterexample lost positivity")
    if not all(summary["theorem"].values()): raise RuntimeError("theorem gate missing")
    for key in ("universal_unit_tail_propagation", "uniform_refresh_projector_lipschitz_constant_proved", "replay_free_uniform_block_envelope_proved", "repeated_block_contraction_proved", "hilbert_polya_operator", "riemann_hypothesis"):
        if summary["program_boundary"][key]: raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("endpoint tail/projector lipschitz theorem", "local gap loss-to-projector theorem", "conditional projector block envelope", "unit propagation is false", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript: raise RuntimeError(f"missing phrase: {phrase}")

    archived = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "projector-lipschitz-propagation-barrier.pdf", ROOT / "figures" / "projector_lipschitz_propagation_barrier.pdf", ROOT / "figures" / "projector_lipschitz_propagation_barrier.png", ROOT / "results" / "projector_propagation_audit.json", ROOT / "results" / "projector_propagation_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"; payload = {"status": "all_archived_hashes_projector_bounds_counterexample_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__": main()
