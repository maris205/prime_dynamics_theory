"""Replay Volume III hashes and enforce its claim firewall."""

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
    if audit["unique_numbers"] != list(range(242, 282)):
        raise RuntimeError("Volume III source range changed")
    if audit["review_anchor_numbers"] != [251, 261, 271, 281]:
        raise RuntimeError("Volume III review anchors changed")
    if not audit["deterministic_envelope"]["proved"]:
        raise RuntimeError("deterministic envelope status changed")
    if not audit["deterministic_counterloop_bridge_proved"]:
        raise RuntimeError("counterloop status changed")
    if audit["actual_cloud_coefficient_bridge_proved"]:
        raise RuntimeError("actual coefficient bridge was promoted")
    if audit["aggregate_noisy_cloud_transport_proved"]:
        raise RuntimeError("noisy cloud transport was promoted")
    if audit["variable_rank_quotient_instantiated"]:
        raise RuntimeError("variable-rank quotient was promoted")
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
        "deterministic closure theorem",
        "finite-head separation theorem",
        "actual cloud identification remains open",
        "gates a--e remain false/open",
        "does not construct a hilbert--polya operator",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript boundary phrase: {phrase}")

    required_archive = (
        ".gitignore", "Makefile", "README.md", "CROSSWALK.md",
        "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
        "experiments/build_volume_audit.py", "experiments/build_archive.py",
        "experiments/verify_archive.py", "tests/test_volume.py",
        "pyproject.toml", "requirements.txt", "main.pdf",
        "deterministic-numerator-anchor-counterloop-synthesis.pdf",
        "results/volume_audit.json", "results/dependency_manifest.json",
        "results/summary.json", "results/atomic_index.tex",
    )
    missing = [relative for relative in required_archive if not (ROOT / relative).is_file()]
    if missing:
        raise RuntimeError(f"missing required archive files: {missing}")
    archived = {relative: sha(ROOT / relative) for relative in required_archive}
    output = ROOT / "results/archive_verification.json"
    output.write_text(json.dumps({
        "status": "rh_volume_iii_hashes_and_claim_boundary_verified",
        "file_count": len(archived),
        "files": archived,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"file_count": len(archived), "status": "verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
