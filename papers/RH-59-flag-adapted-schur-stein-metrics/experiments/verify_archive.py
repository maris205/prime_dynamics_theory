"""Verify RH-59 hashes, numerical gates, and theorem boundaries."""

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
    if len(pilot["rows"]) != 5:
        raise RuntimeError("five-scale pilot is incomplete")
    if pilot["evidence_level"].startswith("interval"):
        raise RuntimeError("binary64 pilot misclassified")

    smallest = pilot["rows"][-1]
    if smallest["sigma"] != 0.01:
        raise RuntimeError("smallest stored scale changed")
    left = smallest["left"]
    right = smallest["right"]
    if not 15.0 < left["metric_absolute_upper"] < 25.0:
        raise RuntimeError("left flag-metric endpoint gate regressed")
    if not 10.0 < right["metric_absolute_upper"] < 15.0:
        raise RuntimeError("right flag-metric endpoint gate regressed")
    if left["inherited_rh58"]["scalar_path_upper"] <= (
        90.0 * left["metric_absolute_upper"]
    ):
        raise RuntimeError("left path improvement gate regressed")
    if right["inherited_rh58"]["scalar_path_upper"] <= (
        30.0 * right["metric_absolute_upper"]
    ):
        raise RuntimeError("right path improvement gate regressed")

    channels = [
        row[side]
        for row in pilot["rows"]
        for side in ("left", "right")
    ]
    packets = [packet for channel in channels for packet in channel["packets"]]
    if min(
        packet["minimum_dissipation_eigenvalue"] for packet in packets
    ) <= 1.0e-8:
        raise RuntimeError("positive dissipation margin failed")
    if min(
        packet["minimum_supersolution_eigenvalue"] for packet in packets
    ) <= -1.0e-9:
        raise RuntimeError("Stein supersolution residual too negative")
    if any(
        packet["metric_energy_upper"]
        < packet["exact_packet_energy"] * (1.0 - 1.0e-9)
        for packet in packets
    ):
        raise RuntimeError("packet upper fell below exact packet energy")
    if any(not packet["optimizer"]["direct_success"] for packet in packets):
        raise RuntimeError("stored low-dimensional optimizer did not terminate")
    if max(
        channel["maximum_local_metric_residual"] for channel in channels
    ) >= 1.0e-10:
        raise RuntimeError("local Lyapunov residual too large")
    if max(
        channel["observability_stein_residual_relative"]
        for channel in channels
    ) >= 1.0e-10:
        raise RuntimeError("observability Stein residual too large")
    if max(
        channel["rh58_exact_relative_defect"] for channel in channels
    ) >= 1.0e-10:
        raise RuntimeError("RH-58 cross-check failed")

    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    for key in (
        "local_lyapunov_identities_certified",
        "dissipation_positive_definite_certified",
        "supersolution_positive_semidefinite_certified",
        "packet_upper_certified",
    ):
        if not arb[key]:
            raise RuntimeError(f"Arb gate failed: {key}")
    if arb["production_interval_schur_metric_executed"]:
        raise RuntimeError("production interval scope overclaimed")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "flag-compatible block metric",
        "stein supersolution",
        "endpoint coercivity",
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
    pilot = load("results/flag_metric_pilot.json")
    arb = load("results/arb_flag_metric_audit.json")
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
        ROOT / "flag-adapted-schur-stein-metrics.pdf",
        ROOT / "figures" / "flag_adapted_schur_stein.pdf",
        ROOT / "figures" / "flag_adapted_schur_stein.png",
        ROOT / "results" / "flag_metric_pilot.json",
        ROOT / "results" / "flag_metric_pilot_smoke.json",
        ROOT / "results" / "arb_flag_metric_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": (
            "all_archived_hashes_flag_metric_and_endpoint_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "gates": {
            "flag_metric_existence": summary["theorem"][
                "flag_block_diagonal_metric_existence"
            ],
            "exact_dissipation_supersolution": summary["theorem"][
                "packetwise_exact_dissipation_supersolution"
            ],
            "outer_packet_bottleneck_recorded": True,
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
