"""Verify RH-65 hashes, numerical gates, and claim boundaries."""

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
    if pilot["precision_decimal_digits"] != 140:
        raise RuntimeError("high-precision pilot changed")
    if len(pilot["cases"]) != 6:
        raise RuntimeError("family pilot is incomplete")
    for case in pilot["cases"]:
        if abs(
            case["fitted_condition_exponent"]
            - case["predicted_condition_exponent"]
        ) > 0.02:
            raise RuntimeError("condition exponent fit regressed")
        if abs(
            case["fitted_metric_gap_exponent"]
            - case["predicted_metric_gap_exponent"]
        ) > 0.02:
            raise RuntimeError("metric-gap exponent fit regressed")
    fixed_d4 = pilot["cases"][2]["endpoint"]
    matched_d4 = pilot["cases"][-1]["endpoint"]
    if fixed_d4["condition_number"] <= 1.0e40:
        raise RuntimeError("fixed-coupling obstruction disappeared")
    if matched_d4["condition_number"] >= 2.0:
        raise RuntimeError("matched-scale conditioning regressed")
    if matched_d4["generic_horizon_1e_minus_6"] <= 1_000_000_000:
        raise RuntimeError("generic slow horizon witness changed")
    required_arb = (
        "unmatched_identity_certified",
        "matched_identity_certified",
        "positive_metrics_certified",
        "fixed_coupling_condition_exceeds_1e7",
        "fixed_coupling_metric_gap_below_1e_minus_10",
        "matched_condition_below_2",
        "matched_metric_gap_over_gap_between_point_4_and_point_5",
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
        "exact contraction ledger",
        "matched-scale conditioning",
        "unmatched jordan obstruction",
        "growing-chain barrier",
        "high-precision",
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
    pilot = load("results/family_conditioning_pilot.json")
    arb = load("results/arb_two_step_audit.json")
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
        ROOT / "physical-family-metric-conditioning.pdf",
        ROOT / "figures" / "physical_family_metric_conditioning.pdf",
        ROOT / "figures" / "physical_family_metric_conditioning.png",
        ROOT / "results" / "family_conditioning_pilot.json",
        ROOT / "results" / "family_conditioning_smoke.json",
        ROOT / "results" / "arb_two_step_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_conditioning_and_route_gates_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "matched_scale_uniform_conditioning": summary["theorem"][
                "matched_scale_uniform_conditioning"
            ],
            "production_family_uniformity": summary["program_boundary"][
                "production_family_uniformity"
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
