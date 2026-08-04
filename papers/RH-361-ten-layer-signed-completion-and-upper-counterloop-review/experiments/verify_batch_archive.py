"""Verify the RH-352--RH-361 batch publication manifest."""

from __future__ import annotations

import json

from build_archive import NUMBERS, PAPERS, ROOT, digest, paper_directories, publication_files


def main() -> None:
    manifest = json.loads(
        (ROOT / "results/batch_dependency_manifest.json").read_text(encoding="utf-8")
    )
    paths = []
    for directory in paper_directories():
        paths.extend(publication_files(directory))
    current = {str(path.relative_to(PAPERS)): path for path in sorted(paths)}
    expected = manifest["files"]
    failures = []
    if manifest.get("status") != "rh352_361_batch_publication_manifest":
        failures.append({"file": "batch_dependency_manifest.json", "reason": "status_mismatch"})
    if manifest.get("paper_numbers") != list(NUMBERS):
        failures.append({"file": "batch_dependency_manifest.json", "reason": "paper_numbers_mismatch"})
    if manifest.get("file_count") != len(expected):
        failures.append({"file": "batch_dependency_manifest.json", "reason": "file_count_mismatch"})
    for relative in sorted(set(expected) - set(current)):
        failures.append({"file": relative, "reason": "missing"})
    for relative in sorted(set(current) - set(expected)):
        failures.append({"file": relative, "reason": "unexpected"})
    for relative in sorted(set(expected) & set(current)):
        if digest(current[relative]) != expected[relative]:
            failures.append({"file": relative, "reason": "sha256_mismatch"})
    payload = {
        "status": "rh352_361_batch_archive_verified",
        "paper_numbers": list(NUMBERS),
        "file_count": manifest["file_count"],
        "failure_count": len(failures),
        "failures": failures,
    }
    (ROOT / "results/batch_archive_verification.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
