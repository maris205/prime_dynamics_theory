"""Verify RH-74 hashes, bridge gates, and claim boundaries."""

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


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/validated_upstream_bridge_audit.json")
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
            raise RuntimeError(f"external input hash mismatch: {path}")
    if len(audit["rows"]) != 5 or not audit["all_executed_channels_green"]:
        raise RuntimeError("five-scale bridge audit is incomplete")
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    if len(channels) != 10:
        raise RuntimeError("fine/coarse bridge channel count changed")
    for channel in channels:
        if not channel["finite_scale_one_percent_green"]:
            raise RuntimeError("one-percent composition failed")
        if not channel["robust_hardy_bridge"]["block_contraction_certified"]:
            raise RuntimeError("robust block contraction failed")
        if channel["factor_transfer"]["all_factor_transfers_green"] is not True:
            raise RuntimeError("analytic factor transfer failed")
    metrics = summary["audit"]
    if metrics["maximum_bridge"] >= 2.1e-6:
        raise RuntimeError("bridge upper exceeded archived budget")
    if metrics["maximum_bridge_to_slack_ratio"] >= 0.003:
        raise RuntimeError("bridge consumed too much headroom")
    if metrics["maximum_true_block_contraction"] >= 0.022:
        raise RuntimeError("true block contraction margin changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("a theorem gate is missing")
    boundary = summary["program_boundary"]
    if not boundary["finite_scale_end_to_end_hardy_closed"]:
        raise RuntimeError("finite-scale closure was lost")
    if any(value for key, value in boundary.items() if key != "finite_scale_end_to_end_hardy_closed"):
        raise RuntimeError("claim boundary was overrun")
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "normalized coupling perturbation",
        "volterra power perturbation",
        "robust four-block hardy bridge",
        "source/observation transfer",
        "finite-scale chain",
        "stage a1",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing boundary phrase: {phrase}")
    archived = [
        ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib",
        ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf",
        ROOT / "validated-upstream-hardy-bridge.pdf",
        ROOT / "figures" / "validated_upstream_hardy_bridge.pdf",
        ROOT / "figures" / "validated_upstream_hardy_bridge.png",
        ROOT / "results" / "validated_upstream_bridge_audit.json",
        ROOT / "results" / "validated_upstream_bridge_smoke.json",
        ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    payload = {
        "status": "all_archived_hashes_upstream_bridge_gates_and_boundaries_verified",
        "file_count": len(files), "files": files,
        "gates": {"all_channels_green": metrics["all_channels_green"], "finite_scale_end_to_end_hardy_closed": boundary["finite_scale_end_to_end_hardy_closed"], "uniform_small_noise_family_bound": boundary["uniform_small_noise_family_bound"]},
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
