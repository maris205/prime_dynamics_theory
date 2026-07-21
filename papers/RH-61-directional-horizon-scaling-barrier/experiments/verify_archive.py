"""Verify RH-61 hashes, numerical gates, and claim boundaries."""

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


def verify_theory(summary, audit, arb) -> None:
    for key, value in summary["theorem"].items():
        if not value:
            raise RuntimeError(f"theorem gate missing: {key}")
    for key, value in summary["program_boundary"].items():
        if value:
            raise RuntimeError(f"overclaimed boundary: {key}")
    if len(audit["rows"]) != 5:
        raise RuntimeError("five-scale archive is incomplete")
    if audit["evidence_level"].startswith("interval"):
        raise RuntimeError("archived binary64 audit misclassified")

    for row in audit["rows"]:
        for side in ("left", "right"):
            channel = row[side]
            if not 0.0 < channel["maximum_contraction"] < 1.0:
                raise RuntimeError("packet contraction is not strict")
            for record in channel["horizons"].values():
                if record["geometric_tail_envelope"] < -1.0e-14:
                    raise RuntimeError("negative geometric envelope")
                if record["phase_tail_sum"] < -1.0e-14:
                    raise RuntimeError("negative phase tail")
                if record["geometric_tail_envelope"] + 1.0e-12 < (
                    record["phase_tail_sum"]
                ):
                    raise RuntimeError("geometric envelope is below stored tail")

    endpoint = audit["rows"][-1]
    if endpoint["sigma"] != 0.01:
        raise RuntimeError("endpoint scale changed")
    if endpoint["left"]["geometric_horizons"]["0.05"] < 800:
        raise RuntimeError("left geometric barrier gate regressed")
    if endpoint["right"]["geometric_horizons"]["0.05"] < 200:
        raise RuntimeError("right geometric barrier gate regressed")
    if endpoint["left"]["horizons"]["32"]["phase_upper_over_exact"] >= 1.01:
        raise RuntimeError("left phase completion gate regressed")
    if endpoint["right"]["horizons"]["32"]["phase_upper_over_exact"] >= 1.01:
        raise RuntimeError("right phase completion gate regressed")

    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    for key in (
        "slow_mode_upper_at_horizon_certified",
        "slow_mode_failure_before_horizon_certified",
        "geometric_upper_at_horizon_certified",
        "geometric_failure_before_horizon_certified",
        "stein_tail_equality_case_certified",
    ):
        if not arb[key]:
            raise RuntimeError(f"Arb gate failed: {key}")
    if arb["production_interval_audit_executed"]:
        raise RuntimeError("production interval scope overclaimed")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "packetwise geometric envelope",
        "reducing slow-mode lower bound",
        "power-gap implication",
        "phase-aware",
        "binary64",
        "stage a1",
        "stage a4",
        "hilbert--polya",
        "prime-power",
        "t\\log t",
        "riemann-hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing claim-boundary phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/horizon_scaling_audit.json")
    arb = load("results/arb_horizon_audit.json")
    verify_hashes(summary, dependency)
    verify_theory(summary, audit, arb)
    verify_text()

    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "directional-horizon-scaling-barrier.pdf",
        ROOT / "figures" / "directional_horizon_scaling.pdf",
        ROOT / "figures" / "directional_horizon_scaling.png",
        ROOT / "results" / "horizon_scaling_audit.json",
        ROOT / "results" / "horizon_scaling_smoke.json",
        ROOT / "results" / "arb_horizon_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_horizon_and_barrier_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "geometric_envelope": summary["theorem"][
                "packetwise_geometric_envelope"
            ],
            "slow_mode_lower_bound": summary["theorem"][
                "reducing_slow_mode_lower_bound"
            ],
            "stage_A1_closed": summary["program_boundary"]["stage_A1_closed"],
            "directional_tail_certificate": summary["program_boundary"][
                "directional_tail_certificate"
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
