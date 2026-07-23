"""Verify RH-106 hashes, price audit, stopped safety, and boundaries."""

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


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/uniform_quotient_audit.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external hash mismatch: {path}")

    values = audit["audit_summary"]
    if len(audit["thresholds"]) != 3:
        raise RuntimeError("threshold count changed")
    if values["candidate_count"] != 38 or values["accepted_count"] != 35 or values["rejected_count"] != 3:
        raise RuntimeError("candidate/acceptance counts changed")
    if not values["all_local_gap_certificates_green"]:
        raise RuntimeError("local gap certificate failed")
    if not values["primary_all_candidates_fit_stopped_budget"]:
        raise RuntimeError("primary no-stop price fit failed")
    if values["maximum_replay_multiplier"] >= 1.0:
        raise RuntimeError("replay multiplier changed")
    if values["maximum_stopped_endpoint_ratio"] >= 1.007:
        raise RuntimeError("stopped endpoint gate changed")
    if values["maximum_unrestricted_endpoint_ratio"] <= 1.024:
        raise RuntimeError("unrestricted stress branch disappeared")
    if values["ratio_collapse_good_price_power"] != 1.5 or values["ratio_collapse_bad_price_power"] != 0.0:
        raise RuntimeError("ratio-collapse boundary changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "uniform_gap_aware_physical_supply_proved",
        "replay_free_uniform_debit_envelope_proved",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "local gap-weighted quotient price",
        "uniform gap-aware quotient law",
        "power-priced quotient criterion",
        "gap collapse is not the invariant",
        "stopped prefix",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")

    archived = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "uniform-gap-aware-quotient-law.pdf",
        ROOT / "figures" / "uniform_gap_aware_quotient.pdf",
        ROOT / "figures" / "uniform_gap_aware_quotient.png",
        ROOT / "results" / "uniform_quotient_audit.json",
        ROOT / "results" / "uniform_quotient_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_uniform_price_stopped_safety_ratio_boundary_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
