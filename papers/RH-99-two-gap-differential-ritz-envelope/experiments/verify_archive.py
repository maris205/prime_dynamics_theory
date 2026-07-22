"""Verify RH-99 hashes, available probes, unavailable gaps, and boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]; REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""): digest.update(chunk)
    return digest.hexdigest()


def load(path: str): return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json"); dependency = load("results/dependency_manifest.json"); audit = load("results/two_gap_differential_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_available_two_gap_probe_bounds_green"]: raise RuntimeError("available two-gap probes failed")
    if audit["all_executed_two_gap_certificates_available"]: raise RuntimeError("negative gap branch disappeared")
    if values["update_count"] != 120 or values["probe_count"] != 720: raise RuntimeError("audit count changed")
    if values["differential_certificate_available_count"] != 115 or values["differential_certificate_unavailable_count"] != 5: raise RuntimeError("availability count changed")
    if values["ritz_gap_nonpositive_count"] != 5 or values["probe_green_update_count"] != 115: raise RuntimeError("Ritz-gap branch changed")
    if values["quotient_inside_linearized_radius_count"] != 0: raise RuntimeError("finite-radius negative branch changed")
    if values["maximum_two_gap_derivative_bound"] <= 1e40: raise RuntimeError("large-bound diagnostic changed")
    if not all(summary["theorem"].values()): raise RuntimeError("theorem gate missing")
    for key in ("all_frozen_output_ritz_gaps_certified", "finite_neighborhood_lipschitz_tube_proved", "adaptive_branch_uniformly_separated", "replay_free_block_envelope_proved", "repeated_block_contraction_proved", "hilbert_polya_operator", "riemann_hypothesis"):
        if summary["program_boundary"][key]: raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("cross covariance derivative formula", "spectral projector sylvester bound", "two-gap refresh derivative theorem", "finite neighborhood tube", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript: raise RuntimeError(f"missing phrase: {phrase}")

    archived = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "two-gap-differential-ritz-envelope.pdf", ROOT / "figures" / "two_gap_differential_ritz_envelope.pdf", ROOT / "figures" / "two_gap_differential_ritz_envelope.png", ROOT / "results" / "two_gap_differential_audit.json", ROOT / "results" / "two_gap_differential_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}; output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_two_gap_probes_unavailable_gaps_and_boundaries_verified", "file_count": len(files), "files": files}; output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__": main()
