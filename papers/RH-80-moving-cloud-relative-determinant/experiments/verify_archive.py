"""Verify RH-80 hashes, theorem gates, and claim boundaries."""

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
    audit = load("results/cloud_renormalization_audit.json")
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
    if len(audit["archived_cloud_rows"]) != 7 or audit["precision_bits"] != 256:
        raise RuntimeError("cloud audit incomplete")
    if audit["ideal_model"]["fixed_cancellation_locally_bounded_across_circle"]:
        raise RuntimeError("fixed-cancellation obstruction was lost")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    boundary = summary["program_boundary"]
    for key in ("actual_cloud_riesz_projection_constructed", "uniform_complement_trace_norm_proved", "canonical_cloud_identification_proved", "stage_A5_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        if boundary[key]:
            raise RuntimeError(f"claim boundary overrun: {key}")
    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("fixed-pole cancellation dichotomy", "moving-cloud relative determinant", "coefficient deconvolution", "stage a5", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")
    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "moving-cloud-relative-determinant.pdf",
        ROOT / "figures" / "moving_cloud_relative_determinant.pdf",
        ROOT / "figures" / "moving_cloud_relative_determinant.png",
        ROOT / "results" / "cloud_renormalization_audit.json",
        ROOT / "results" / "cloud_renormalization_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_moving_cloud_relative_determinant_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()

