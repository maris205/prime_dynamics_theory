"""Verify RH-69 hashes, portfolio decisions, and boundaries."""

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


def verify_theory(summary, portfolio, arb) -> None:
    for key, value in summary["theorem"].items():
        if not value:
            raise RuntimeError(f"theorem gate missing: {key}")
    for key, value in summary["program_boundary"].items():
        if value:
            raise RuntimeError(f"overclaimed boundary: {key}")
    phase = portfolio["phase_horizon_portfolio"]
    if len(phase) != 10:
        raise RuntimeError("physical phase portfolio is incomplete")
    expected = {
        0.16: 4.0,
        0.08: 8.0,
        0.04: 16.0,
        0.02: 32.0,
        0.01: 32.0,
    }
    for row in phase:
        if row["selected"] is None:
            raise RuntimeError("physical phase row did not select")
        if row["selected"]["costs"]["horizon"] != expected[row["sigma"]]:
            raise RuntimeError("physical phase selector changed")
        if row["geometric_over_selected_horizon"] <= 1.0:
            raise RuntimeError("geometric comparison no longer saves")
    covariance = {
        row["name"]: row for row in portfolio["covariance_portfolio"]
    }
    cancellation = covariance["exact_diagonal_cancellation"]["selected"]
    if cancellation["costs"]["focus_exponent"] != 24.0:
        raise RuntimeError("cancellation covariance selection changed")
    for name in (
        "nonnormal_three_packet_chain",
        "six_mode_complex_phase_packets",
    ):
        if covariance[name]["selected"]["costs"]["focus_exponent"] != 0.0:
            raise RuntimeError("generic covariance unnecessarily focused")
    triage = portfolio["depth_triage"]
    if any(row["status"] != "red" for row in triage["exact_rings"]):
        raise RuntimeError("exact ring triage changed")
    if any(row["status"] != "red" for row in triage["jittered_rings"]):
        raise RuntimeError("jittered ring triage changed")
    arc_statuses = [row["status"] for row in triage["phase_arcs"]]
    if arc_statuses != ["green", "green", "green", "green", "amber", "amber", "amber"]:
        raise RuntimeError("phase arc triage changed")
    required_arb = (
        "geometric_first_horizon_certified",
        "focused_covariance_meets_physical_and_global_budgets_certified",
        "fourier_lower_gate_rejects_ten_percent_budget_certified",
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
        "safe pareto pruning",
        "three-way triage",
        "triage soundness",
        "adaptive composition",
        "conditional polylogarithmic ledger",
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
    portfolio = load("results/certificate_portfolio.json")
    arb = load("results/arb_portfolio_audit.json")
    verify_hashes(summary, dependency)
    verify_theory(summary, portfolio, arb)
    verify_text()
    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "adaptive-certificate-portfolio.pdf",
        ROOT / "figures" / "adaptive_certificate_portfolio.pdf",
        ROOT / "figures" / "adaptive_certificate_portfolio.png",
        ROOT / "results" / "certificate_portfolio.json",
        ROOT / "results" / "certificate_portfolio_smoke.json",
        ROOT / "results" / "arb_portfolio_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_portfolio_and_boundary_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "three_way_triage_soundness": summary["theorem"][
                "three_way_triage_soundness"
            ],
            "production_interval_upper_portfolio": summary[
                "program_boundary"
            ]["production_interval_upper_portfolio"],
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
