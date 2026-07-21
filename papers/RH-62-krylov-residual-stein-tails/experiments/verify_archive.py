"""Verify RH-62 hashes, numerical gates, and theorem boundaries."""

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
        raise RuntimeError("model pilot is incomplete")
    for model in pilot["models"]:
        for horizon in pilot["horizons"]:
            for record in model["horizons"][str(horizon)].values():
                if record["krylov_upper"] + 1.0e-11 < record["exact_norm"]:
                    raise RuntimeError("Krylov upper fell below exact power")
                if record["geometric_upper"] + 1.0e-11 < record["exact_norm"]:
                    raise RuntimeError("geometric upper fell below exact power")
    calibrated = pilot["models"][0]
    if calibrated["endpoint_geometric_gain"] < 1000.0:
        raise RuntimeError("calibrated norm-gap gate regressed")
    if calibrated["endpoint_krylov_gain_k1"] >= 1.01:
        raise RuntimeError("calibrated Krylov gain gate regressed")
    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    for key in (
        "one_step_upper_certified",
        "full_breakdown_exact_certified",
    ):
        if not arb[key]:
            raise RuntimeError(f"Arb gate failed: {key}")
    if arb["production_interval_audit_executed"]:
        raise RuntimeError("production interval scope overclaimed")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "arnoldi power identity",
        "directional power certificate",
        "stein tail",
        "breakdown",
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
    pilot = load("results/krylov_tail_pilot.json")
    arb = load("results/arb_krylov_audit.json")
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
        ROOT / "krylov-residual-stein-tails.pdf",
        ROOT / "figures" / "krylov_residual_tail.pdf",
        ROOT / "figures" / "krylov_residual_tail.png",
        ROOT / "results" / "krylov_tail_pilot.json",
        ROOT / "results" / "krylov_tail_smoke.json",
        ROOT / "results" / "arb_krylov_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_krylov_identity_and_tail_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "arnoldi_identity": summary["theorem"]["arnoldi_power_identity"],
            "directional_certificate": summary["theorem"][
                "directional_power_certificate"
            ],
            "production_physical_family": summary["program_boundary"][
                "production_physical_family"
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
