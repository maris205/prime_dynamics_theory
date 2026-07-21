"""Verify RH-57 hashes, numerical gates, and theorem boundaries."""

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


def verify_theory(summary, pilot, arb) -> None:
    theorem = summary["theorem"]
    if not theorem["cross_stein_identity"]:
        raise RuntimeError("cross-Stein theorem missing")
    if theorem["requires_diagonalizability"]:
        raise RuntimeError("theorem boundary incorrectly requires diagonalization")
    boundary = summary["program_boundary"]
    for key in (
        "stage_A1_closed",
        "stage_A4_unconditional_closed",
        "production_interval_riesz_projector",
        "arithmetic_trace_formula",
        "hilbert_polya_operator",
    ):
        if boundary[key]:
            raise RuntimeError(f"overclaimed boundary: {key}")
    if len(pilot["rows"]) != 5:
        raise RuntimeError("five-scale pilot is incomplete")
    if pilot["evidence_level"].startswith("interval"):
        raise RuntimeError("binary64 pilot misclassified")
    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    if not arb["gram_positive_certified"] or not arb["coherence_bound_certified"]:
        raise RuntimeError("Arb scalar gates failed")

    smallest = pilot["rows"][-1]
    max_projector = max(
        block["projector_norm"]
        for side in ("left", "right")
        for block in smallest[side]["blocks"]
    )
    if max_projector < 1000.0:
        raise RuntimeError("radial obliqueness gate regressed")
    if smallest["right"]["signed_fusion_ratio"] >= 1.0e-4:
        raise RuntimeError("signed cancellation gate regressed")
    if max(
        row["left"]["block_reconstruction_relative_defect"]
        for row in pilot["rows"]
    ) >= 1.0e-9:
        raise RuntimeError("left Gram reconstruction residual too large")
    if max(
        row["right"]["block_reconstruction_relative_defect"]
        for row in pilot["rows"]
    ) >= 1.0e-9:
        raise RuntimeError("right Gram reconstruction residual too large")


def verify_text() -> None:
    text = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "cross-stein",
        "positive semidefinite",
        "binary64",
        "stage a1",
        "stage a4",
        "hilbert--polya",
        "prime-power",
        "t\\log t",
        "riemann-hypothesis",
    ):
        if phrase not in text:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    pilot = load("results/mixed_overlap_pilot.json")
    arb = load("results/arb_block_audit.json")
    verify_hashes(summary, dependency)
    verify_theory(summary, pilot, arb)
    verify_text()

    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "mixed-haar-channel-overlap-budget.pdf",
        ROOT / "figures" / "mixed_haar_channel_overlap.pdf",
        ROOT / "figures" / "mixed_haar_channel_overlap.png",
        ROOT / "results" / "mixed_overlap_pilot.json",
        ROOT / "results" / "mixed_overlap_pilot_smoke.json",
        ROOT / "results" / "arb_block_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_cross_stein_and_route_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "cross_stein_identity": summary["theorem"]["cross_stein_identity"],
            "radial_route_obstructed": True,
            "stage_A1_closed": summary["program_boundary"]["stage_A1_closed"],
            "stage_A4_closed": summary["program_boundary"][
                "stage_A4_unconditional_closed"
            ],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
