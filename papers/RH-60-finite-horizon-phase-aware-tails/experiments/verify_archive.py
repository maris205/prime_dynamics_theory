"""Verify RH-60 hashes, numerical gates, and theorem boundaries."""

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
    if pilot["selected_horizon"] != 32:
        raise RuntimeError("selected horizon changed")
    if pilot["evidence_level"].startswith("interval"):
        raise RuntimeError("binary64 pilot misclassified")

    for row in pilot["rows"]:
        for side in ("left", "right"):
            channel = row[side]
            for horizon in pilot["horizons"]:
                record = channel["horizons"][str(horizon)]
                if record["finite_gram_minimum_eigenvalue"] < -1.0e-9:
                    raise RuntimeError("finite Gram positivity gate failed")
                if record["tail_sum"] < 0.0:
                    raise RuntimeError("negative tail sum")
            if channel["selected_phase_aware_upper"] < (
                channel["exact_hardy_energy"] * (1.0 - 1.0e-9)
            ):
                raise RuntimeError("completion fell below exact energy")
            zero = channel["horizons"]["0"]["phase_aware_upper"]
            if zero < channel["selected_phase_aware_upper"] * (1.0 - 1.0e-9):
                raise RuntimeError("L=0 route comparison regressed")

    smallest = pilot["rows"][-1]
    if smallest["sigma"] != 0.01:
        raise RuntimeError("smallest stored scale changed")
    if smallest["left"]["selected_phase_aware_upper"] >= 1.6:
        raise RuntimeError("left phase-aware endpoint gate regressed")
    if smallest["right"]["selected_phase_aware_upper"] >= 1.9:
        raise RuntimeError("right phase-aware endpoint gate regressed")
    if smallest["left"]["selected_phase_aware_upper_over_exact"] >= 1.01:
        raise RuntimeError("left completion ratio gate regressed")
    if smallest["right"]["selected_phase_aware_upper_over_exact"] >= 1.01:
        raise RuntimeError("right completion ratio gate regressed")
    if not 0.15 < pilot["fits"]["left_phase_aware"]["growth_exponent"] < 0.19:
        raise RuntimeError("left fitted growth gate regressed")
    if not 0.18 < pilot["fits"]["right_phase_aware"]["growth_exponent"] < 0.22:
        raise RuntimeError("right fitted growth gate regressed")

    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    for key in (
        "local_lyapunov_identities_certified",
        "dissipation_positive_definite_certified",
        "supersolution_positive_definite_certified",
        "tail_upper_certified",
        "completion_upper_certified",
    ):
        if not arb[key]:
            raise RuntimeError(f"Arb gate failed: {key}")
    if arb["production_interval_audit_executed"]:
        raise RuntimeError("production interval scope overclaimed")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "finite-horizon stein completion",
        "phase-aware global completion",
        "finite gram",
        "stein tail",
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
    pilot = load("results/phase_tail_pilot.json")
    arb = load("results/arb_phase_tail_audit.json")
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
        ROOT / "finite-horizon-phase-aware-tails.pdf",
        ROOT / "figures" / "finite_horizon_phase_tail.pdf",
        ROOT / "figures" / "finite_horizon_phase_tail.png",
        ROOT / "results" / "phase_tail_pilot.json",
        ROOT / "results" / "phase_tail_pilot_smoke.json",
        ROOT / "results" / "arb_phase_tail_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": (
            "all_archived_hashes_phase_completion_and_tail_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "gates": {
            "loewner_completion": summary["theorem"][
                "loewner_finite_horizon_stein_completion"
            ],
            "phase_aware_completion": summary["theorem"][
                "phase_aware_global_completion"
            ],
            "fixed_horizon_observed": True,
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
