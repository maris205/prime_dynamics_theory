"""Replay Volume II hashes and enforce its claim firewall."""

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
    if audit["unique_numbers"] != list(range(161, 242)):
        raise RuntimeError("Volume II source range changed")
    if audit["review_anchor_numbers"] != [161, 171, 181, 191, 201, 211, 221, 231, 241]:
        raise RuntimeError("Volume II anchors changed")
    if not audit["typed_assembly"]["abstract_implication_proved"]:
        raise RuntimeError("typed assembly status changed")
    if any(audit["typed_assembly"]["physical_interfaces"].values()):
        raise RuntimeError("physical interface was promoted")
    if audit["fixed_order_trace_envelope_max_order"] != 12:
        raise RuntimeError("fixed-order boundary changed")
    if audit["moving_noisy_all_order_trace_envelope_proved"]:
        raise RuntimeError("all-order noisy envelope was promoted")
    if audit["no_over_extraction_coefficient_anchor_proved"]:
        raise RuntimeError("coefficient anchor was promoted")
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
        "typed assembly theorem",
        "finite-jet nonpromotion theorem",
        "moving noisy all-order trace envelope remains open",
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
        "physical-riesz-cloud-trace-envelope-synthesis.pdf",
        "results/volume_audit.json", "results/dependency_manifest.json",
        "results/summary.json", "results/atomic_index.tex",
    )
    missing = [relative for relative in required_archive if not (ROOT / relative).is_file()]
    if missing:
        raise RuntimeError(f"missing required archive files: {missing}")
    archived = {relative: sha(ROOT / relative) for relative in required_archive}
    output = ROOT / "results/archive_verification.json"
    output.write_text(json.dumps({
        "status": "rh_volume_ii_hashes_and_claim_boundary_verified",
        "file_count": len(archived),
        "files": archived,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"file_count": len(archived), "status": "verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
