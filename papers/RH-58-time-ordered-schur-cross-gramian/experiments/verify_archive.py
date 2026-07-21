"""Verify RH-58 hashes, numerical gates, and theorem boundaries."""

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
    for key in (
        "dual_positive_packet_identities",
        "reverse_cross_stein_recursion",
        "block_power_stein_gain",
        "scalar_absolute_path_majorant",
    ):
        if not theorem[key]:
            raise RuntimeError(f"theorem gate missing: {key}")
    if theorem["requires_diagonalizability"]:
        raise RuntimeError("theorem boundary incorrectly requires diagonalization")

    boundary = summary["program_boundary"]
    for key in (
        "dyadically_uniform_packet_budget",
        "stage_A1_closed",
        "stage_A4_unconditional_closed",
        "production_interval_schur",
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
    for key in (
        "all_recursion_residuals_contain_zero",
        "primal_dual_identity_certified",
        "path_majorant_certified",
    ):
        if not arb[key]:
            raise RuntimeError(f"Arb gate failed: {key}")
    if arb["production_interval_schur_executed"]:
        raise RuntimeError("production interval scope overclaimed")

    smallest = pilot["rows"][-1]
    if smallest["sigma"] != 0.01:
        raise RuntimeError("smallest stored scale changed")
    if max(
        smallest[side]["source_packet_gram"]["coherence_upper"]
        for side in ("left", "right")
    ) >= 2.0:
        raise RuntimeError("unitary source-packet budget regressed")
    if max(
        smallest[side]["state_block_gram"]["coherence_upper"]
        for side in ("left", "right")
    ) >= 1.8:
        raise RuntimeError("unitary state-block budget regressed")
    if smallest["left"]["scalar_path_majorant"]["energy_upper"] <= 1000.0:
        raise RuntimeError("left absolute-path obstruction disappeared")
    if smallest["right"]["scalar_path_majorant"]["energy_upper"] <= 300.0:
        raise RuntimeError("right absolute-path obstruction disappeared")

    channels = [
        row[side]
        for row in pilot["rows"]
        for side in ("left", "right")
    ]
    if max(
        channel["scalar_path_majorant"]["maximum_terminal_power_norm"]
        for channel in channels
    ) >= 0.30:
        raise RuntimeError("eight-step diagonal contraction gate failed")
    if max(
        channel["cross_stein_recursion"]["maximum_empirical_gain"]
        for channel in channels
    ) >= 2.80:
        raise RuntimeError("empirical block-Stein gain gate failed")
    if max(
        channel["schur_partition"]["reconstruction_defect"]
        for channel in channels
    ) >= 1.0e-10:
        raise RuntimeError("Schur reconstruction residual too large")
    if max(
        channel["cross_stein_recursion"]["maximum_residual_norm"]
        for channel in channels
    ) >= 1.0e-10:
        raise RuntimeError("cross-Stein recursion residual too large")
    if max(
        channel["primal_dual_energy_squared_relative_defect"]
        for channel in channels
    ) >= 1.0e-10:
        raise RuntimeError("primal-dual residual too large")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "positive semidefinite",
        "cross-stein",
        "block-power",
        "absolute-path",
        "binary64",
        "stage a1",
        "stage a4",
        "hilbert--polya",
        "prime-power",
        "t\\log t",
        "riemann-hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    pilot = load("results/schur_fusion_pilot.json")
    arb = load("results/arb_schur_audit.json")
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
        ROOT / "time-ordered-schur-cross-gramian.pdf",
        ROOT / "figures" / "time_ordered_schur_fusion.pdf",
        ROOT / "figures" / "time_ordered_schur_fusion.png",
        ROOT / "results" / "schur_fusion_pilot.json",
        ROOT / "results" / "schur_fusion_pilot_smoke.json",
        ROOT / "results" / "arb_schur_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": (
            "all_archived_hashes_schur_packet_and_route_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "gates": {
            "dual_packet_identities": summary["theorem"][
                "dual_positive_packet_identities"
            ],
            "absolute_path_route_obstructed": True,
            "stage_A1_closed": summary["program_boundary"][
                "stage_A1_closed"
            ],
            "stage_A4_closed": summary["program_boundary"][
                "stage_A4_unconditional_closed"
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
