"""Verify RH-66 hashes, Gram gates, and claim boundaries."""

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
    if len(pilot["models"]) != 3:
        raise RuntimeError("block Gram pilot is incomplete")
    for model in pilot["models"]:
        for record in model["depths"]:
            if record["directional_upper"] + 1.0e-10 < record[
                "exact_directional_energy"
            ]:
                raise RuntimeError("directional upper fell below exact")
            if record["gram_envelope_minimum_slack_eigenvalue"] < -1.0e-10:
                raise RuntimeError("PSD Gram envelope failed")
    cancelling = pilot["models"][0]["depths"][0]
    chain_one, chain_full = pilot["models"][1]["depths"]
    phase_one, phase_full = pilot["models"][2]["depths"]
    if cancelling["directional_gain"] >= 1.00001:
        raise RuntimeError("cancelling direction regressed")
    if cancelling["independent_column_gain"] <= 1.0e18:
        raise RuntimeError("columnwise cancellation witness disappeared")
    if cancelling["uniform_gram_gain"] <= 100.0:
        raise RuntimeError("uniform Gram stress witness disappeared")
    if not (chain_one["directional_gain"] < 4.0 < chain_one[
        "independent_column_gain"
    ]):
        raise RuntimeError("chain block improvement regressed")
    if chain_full["directional_gain"] >= 1.000001:
        raise RuntimeError("chain full block closure regressed")
    if not (phase_one["directional_gain"] < 1.3 < phase_one[
        "independent_column_gain"
    ]):
        raise RuntimeError("phase block improvement regressed")
    if phase_full["directional_gain"] >= 1.000001:
        raise RuntimeError("phase full block closure regressed")
    required_arb = (
        "fused_slow_and_fast_coordinates_cancel_certified",
        "block_residual_annihilates_fused_axis_certified",
        "exact_fused_energy_positive_certified",
        "columnwise_loss_exceeds_1e18_certified",
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
        "block galerkin power identity",
        "directional block center-radius certificate",
        "uniform psd gram envelope",
        "exact fused cancellation",
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
    pilot = load("results/block_gram_pilot.json")
    arb = load("results/arb_cancellation_audit.json")
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
        ROOT / "block-cross-column-krylov-gram.pdf",
        ROOT / "figures" / "block_cross_column_krylov_gram.pdf",
        ROOT / "figures" / "block_cross_column_krylov_gram.png",
        ROOT / "results" / "block_gram_pilot.json",
        ROOT / "results" / "block_gram_smoke.json",
        ROOT / "results" / "arb_cancellation_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_block_gram_and_boundary_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "uniform_psd_gram_envelope": summary["theorem"][
                "uniform_psd_gram_envelope"
            ],
            "uniform_physical_family_block_depth": summary[
                "program_boundary"
            ]["uniform_physical_family_block_depth"],
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
