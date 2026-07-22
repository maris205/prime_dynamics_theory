"""Verify RH-70 hashes, interval gates, and claim boundaries."""

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


def verify_audit(summary, audit) -> None:
    if len(audit["rows"]) != 5:
        raise RuntimeError("five-scale audit is incomplete")
    channels = [
        channel for row in audit["rows"] for channel in row["channels"]
    ]
    if len(channels) != 10:
        raise RuntimeError("left/right channel audit is incomplete")
    for channel in channels:
        if not channel["certified_block_contraction"]:
            raise RuntimeError("block contraction gate failed")
        if not channel["frozen_matrix_green_at_one_percent"]:
            raise RuntimeError("one-percent frozen gate failed")
        if not channel["archived_energy_inside_interval"]:
            raise RuntimeError("archived energy escaped certificate")
        if channel["relative_enclosure_width_upper"] > 1.01:
            raise RuntimeError("completion factor exceeded budget")
    if not summary["audit"]["all_frozen_green"]:
        raise RuntimeError("summary lost frozen-green status")
    for key, value in summary["theorem"].items():
        if not value:
            raise RuntimeError(f"theorem gate missing: {key}")
    for key, value in summary["program_boundary"].items():
        if value:
            raise RuntimeError(f"overclaimed boundary: {key}")


def verify_text() -> None:
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "block-power hardy bound",
        "scalar sharpness",
        "exact-dyadic interval audit",
        "augmented difference bridge",
        "frozen green",
        "end-to-end amber",
        "stage a1",
        "stage a4",
        "hilbert--polya",
        "prime-power",
        "t\\log t",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing boundary phrase: {phrase}")


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/frozen_production_interval_audit.json")
    verify_hashes(summary, dependency)
    verify_audit(summary, audit)
    verify_text()
    archived = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "frozen-production-block-hardy-audit.pdf",
        ROOT / "figures" / "frozen_production_block_hardy_audit.pdf",
        ROOT / "figures" / "frozen_production_block_hardy_audit.png",
        ROOT / "results" / "frozen_production_interval_audit.json",
        ROOT / "results" / "frozen_production_interval_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived
    }
    payload = {
        "status": "all_archived_hashes_interval_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
        "gates": {
            "all_frozen_green": summary["audit"]["all_frozen_green"],
            "stage_A1_closed": summary["program_boundary"]["stage_A1_closed"],
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
