"""Replay Volume IV hashes and enforce its claim firewall."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(records: dict[str, str], base: Path, label: str) -> None:
    for relative, expected in records.items():
        path = base / relative
        if not path.exists() or sha(path) != expected:
            raise RuntimeError(f"{label} hash mismatch: {relative}")


def main() -> None:
    audit = json.loads((ROOT / "results/volume_audit.json").read_text())
    dependency = json.loads((ROOT / "results/dependency_manifest.json").read_text())
    summary = json.loads((ROOT / "results/summary.json").read_text())

    if audit["unique_numbers"] != list(range(282, 362)):
        raise RuntimeError("Volume IV source range changed")
    if set(audit["legacy_alias_groups"]) != {"302", "303", "304", "306"}:
        raise RuntimeError("legacy alias inventory changed")
    if audit["review_anchor_numbers"] != [291, 301, 311, 321, 331, 341, 351, 361]:
        raise RuntimeError("review anchors changed")
    if audit["route_coordinate"] != "actual_same_clock_unnormalized_head_transport_open":
        raise RuntimeError("route coordinate was promoted")
    if audit["same_clock_bridge_proved"] or audit["physical_obstruction_proved"]:
        raise RuntimeError("unproved physical result was promoted")
    if audit["rh_362_activated"]:
        raise RuntimeError("synthesis activated RH-362")
    if any(audit["gates"].values()) or any(audit["forbidden_claims"].values()):
        raise RuntimeError("claim firewall overrun")

    verify(dependency["local_sources"], ROOT, "local source")
    verify(dependency["publication_artifacts"], ROOT, "publication")
    verify(dependency["external_inputs"], REPO, "external source")
    for relative, expected in summary["result_hashes"].items():
        if sha(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")

    manuscript = " ".join((ROOT / "main.tex").read_text().lower().split())
    for phrase in (
        "provenance theorem",
        "typed nonpromotion theorem",
        "d_{4k}(r)",
        "gates a--e remain false/open",
        "does not construct a hilbert--polya operator",
        "rh-362 is not activated",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript boundary phrase: {phrase}")

    required_archive = (
        ".gitignore",
        "Makefile",
        "README.md",
        "CROSSWALK.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "experiments/build_volume_audit.py",
        "experiments/build_archive.py",
        "experiments/verify_archive.py",
        "tests/test_volume.py",
        "pyproject.toml",
        "requirements.txt",
        "main.pdf",
        "noisy-head-annulus-signed-completion-synthesis.pdf",
        "results/volume_audit.json",
        "results/dependency_manifest.json",
        "results/summary.json",
        "results/atomic_index.tex",
    )
    missing = [relative for relative in required_archive if not (ROOT / relative).is_file()]
    if missing:
        raise RuntimeError(f"missing required archive files: {missing}")
    archived = {relative: sha(ROOT / relative) for relative in required_archive}
    output = ROOT / "results/archive_verification.json"
    output.write_text(json.dumps({
        "status": "rh_volume_iv_hashes_and_claim_boundary_verified",
        "file_count": len(archived),
        "files": archived,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"file_count": len(archived), "status": "verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
