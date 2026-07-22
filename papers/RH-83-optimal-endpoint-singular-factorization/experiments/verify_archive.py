"""Verify RH-83 hashes, factorization gates, and boundaries."""

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
    audit = load("results/singular_factorization_audit.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]: raise RuntimeError(f"external hash mismatch: {path}")
    if len(audit["rows"]) != 5 or not audit["all_executed_factorization_gates_green"]: raise RuntimeError("factorization audit incomplete")
    if audit["audit_summary"]["maximum_optimal_factor_constant"] >= 0.162: raise RuntimeError("factor constant gate failed")
    if audit["audit_summary"]["minimum_coordinate_dictionary_relative_residual"] <= 0.46: raise RuntimeError("coordinate barrier gate failed")
    if not all(summary["theorem"].values()): raise RuntimeError("theorem gate missing")
    boundary = summary["program_boundary"]
    for key in ("coordinate_identity_endpoint_route_supported", "all_level_singular_majorization_proved", "uniform_stage_A1_closed", "riemann_hypothesis"):
        if boundary[key]: raise RuntimeError(f"claim boundary overrun: {key}")
    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("optimal endpoint singular factorization", "optimal approximate factorization", "coordinate identity branch verdict", "all-level majorization", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript: raise RuntimeError(f"missing phrase: {phrase}")
    archived = [ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "optimal-endpoint-singular-factorization.pdf", ROOT / "figures" / "optimal_endpoint_singular_factorization.pdf", ROOT / "figures" / "optimal_endpoint_singular_factorization.png", ROOT / "results" / "singular_factorization_audit.json", ROOT / "results" / "singular_factorization_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_optimal_endpoint_factorization_gates_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()

