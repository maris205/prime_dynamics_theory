"""Verify RH-68 hashes, depth barriers, and boundaries."""

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
    for key, value in summary["theorem"].items():
        if not value:
            raise RuntimeError(f"theorem gate missing: {key}")
    for key, value in summary["program_boundary"].items():
        if value:
            raise RuntimeError(f"overclaimed boundary: {key}")
    rings = pilot["exact_rings"]
    if len(rings) != 4:
        raise RuntimeError("exact ring scaling audit is incomplete")
    for ring in rings:
        if ring["required_depth_for_10_percent_error"] != ring["horizon"] + 1:
            raise RuntimeError("exact ring depth law changed")
        horizon_row = next(
            row for row in ring["depths"] if row["depth"] == ring["horizon"]
        )
        if horizon_row["projection_error"] < 0.999999:
            raise RuntimeError("exact ring unit error disappeared")
        if ring["canonical_metric_condition_number"] != 1.0:
            raise RuntimeError("exact metric conditioning changed")
    jitters = pilot["jittered_rings"]
    if any(row["required_depth_for_10_percent_error"] != 33 for row in jitters):
        raise RuntimeError("jittered ring depth barrier regressed")
    for family in jitters:
        for row in family["depths"]:
            if row["spectral_lower_bound"] > row["projection_error"] + 1.0e-10:
                raise RuntimeError("spectral lower bound is invalid")
    if jitters[-1]["depths"][2]["projection_error"] <= 0.98:
        raise RuntimeError("half-cell perturbation witness disappeared")
    expected_depths = [1, 2, 3, 7, 16, 28, 33]
    actual_depths = [
        row["required_depth_for_10_percent_error"]
        for row in pilot["phase_arcs"]
    ]
    if actual_depths != expected_depths:
        raise RuntimeError("phase compression ledger changed")
    required_arb = (
        "unit_norm_certified",
        "all_distinct_fourier_vectors_orthogonal_certified",
        "target_orthogonal_to_depth_space_certified",
        "strict_stability_and_positive_metric_certified",
    )
    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    for key in required_arb:
        if not arb[key]:
            raise RuntimeError(f"Arb gate failed: {key}")
    if arb["production_interval_audit_executed"]:
        raise RuntimeError("production interval scope overclaimed")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "fourier-ring depth barrier",
        "metric and residual do not repair the ring",
        "spectral projection lower bound",
        "mutual-coherence barrier",
        "no universal fixed depth",
        "binary64",
        "stage a1",
        "stage a4",
        "hilbert--polya",
        "prime-power",
        "t\\log t",
        "riemann-hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing boundary phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    pilot = load("results/depth_barrier_pilot.json")
    arb = load("results/arb_fourier_ring_audit.json")
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
        ROOT / "phase-coherence-block-depth-barrier.pdf",
        ROOT / "figures" / "phase_coherence_block_depth_barrier.pdf",
        ROOT / "figures" / "phase_coherence_block_depth_barrier.png",
        ROOT / "results" / "depth_barrier_pilot.json",
        ROOT / "results" / "depth_barrier_smoke.json",
        ROOT / "results" / "arb_fourier_ring_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_depth_barrier_and_boundary_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "universal_fixed_depth_no_go": summary["theorem"][
                "universal_fixed_depth_no_go"
            ],
            "production_phase_compression": summary["program_boundary"][
                "production_phase_compression"
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
