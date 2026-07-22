"""Verify RH-72 hashes, assembly gates, and claim boundaries."""

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


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def verify_hashes(summary, dependency) -> None:
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"local source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external input hash mismatch: {path}")


def verify_audit(summary, audit) -> None:
    if len(audit["rows"]) != 5 or not audit["all_rows_certified"]:
        raise RuntimeError("five-scale assembly audit is incomplete")
    if not audit["critical_parameter_certificate"]["unique_root_certified"]:
        raise RuntimeError("algebraic parameter gate failed")
    for row in audit["rows"]:
        if not row["all_support_centers_interval_stable"]:
            raise RuntimeError("support-center floor gate failed")
        if not row["exact_stochastic_repair_certified"]:
            raise RuntimeError("stochastic repair gate failed")
        if not row["exact_perron_right_vector_for_repaired_matrix"]:
            raise RuntimeError("Perron right-vector gate failed")
    metrics = summary["audit"]
    if metrics["maximum_full_sparse_row_l1"] >= 1.0e-15:
        raise RuntimeError("sparse truncation exceeded budget")
    if metrics["maximum_full_repaired_two_norm"] >= 2.0e-14:
        raise RuntimeError("matrix assembly defect exceeded budget")
    if metrics["maximum_compressed_repaired_two_norm"] >= 2.0e-14:
        raise RuntimeError("compressed assembly defect exceeded budget")
    if metrics["maximum_repair_correction"] >= 1.0e-15:
        raise RuntimeError("stochastic repair exceeded budget")
    if metrics["minimum_repaired_pivot"] <= 0.07:
        raise RuntimeError("repaired pivot positivity margin changed")
    for key, value in summary["theorem"].items():
        if not value:
            raise RuntimeError(f"theorem gate missing: {key}")
    for key, value in summary["program_boundary"].items():
        if value:
            raise RuntimeError(f"overclaimed boundary: {key}")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "full/sparse row identity",
        "exact dyadic stochastic repair",
        "induced two-norm enclosure",
        "haar compressed assembly bound",
        "perron right vector",
        "stationary left vector",
        "parity riesz pair",
        "rank-two deflation",
        "stage a1",
        "stage a4",
        "hilbert--polya",
        "t\\log t",
        "prime-power",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing boundary phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/interval_assembly_audit.json")
    verify_hashes(summary, dependency)
    verify_audit(summary, audit)
    verify_text()
    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "validated-folded-gaussian-assembly.pdf",
        ROOT / "figures" / "validated_folded_gaussian_assembly.pdf",
        ROOT / "figures" / "validated_folded_gaussian_assembly.png",
        ROOT / "results" / "interval_assembly_audit.json",
        ROOT / "results" / "interval_assembly_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_assembly_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "all_rows_certified": summary["audit"]["all_rows_certified"],
            "rank_two_deflation_validated": summary["program_boundary"][
                "rank_two_deflation_validated"
            ],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "file_count": len(files),
                "status": payload["status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
