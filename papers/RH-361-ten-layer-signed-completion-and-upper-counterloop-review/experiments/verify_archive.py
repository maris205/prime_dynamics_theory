"""Verify all individual manifests and write only RH-361 verification."""

from __future__ import annotations

import json

from build_archive import ROOT, digest, paper_directories, publication_files


def main() -> None:
    total_failures = 0
    summaries = []
    for directory in paper_directories():
        manifest = json.loads(
            (directory / "results/dependency_manifest.json").read_text(encoding="utf-8")
        )
        expected = manifest["files"]
        current = {
            str(path.relative_to(directory)): path for path in publication_files(directory)
        }
        failures = []
        if manifest.get("status") != f"{directory.name}_publication_manifest":
            failures.append({"file": "dependency_manifest.json", "reason": "status_mismatch"})
        if manifest.get("file_count") != len(expected):
            failures.append({"file": "dependency_manifest.json", "reason": "file_count_mismatch"})
        for relative in sorted(set(expected) - set(current)):
            failures.append({"file": relative, "reason": "missing"})
        for relative in sorted(set(current) - set(expected)):
            failures.append({"file": relative, "reason": "unexpected"})
        for relative in sorted(set(expected) & set(current)):
            if digest(current[relative]) != expected[relative]:
                failures.append({"file": relative, "reason": "sha256_mismatch"})
        payload = {
            "status": f"{directory.name}_archive_verified",
            "file_count": manifest["file_count"],
            "failure_count": len(failures),
            "failures": failures,
        }
        verification_path = directory / "results/archive_verification.json"
        if directory == ROOT:
            verification_path.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        else:
            existing = json.loads(verification_path.read_text(encoding="utf-8"))
            if existing != payload:
                failures.append(
                    {"file": "archive_verification.json", "reason": "upstream_verification_mismatch"}
                )
        total_failures += len(failures)
        summaries.append(
            {
                "paper": directory.name,
                "file_count": manifest["file_count"],
                "failure_count": len(failures),
            }
        )
    print(
        json.dumps(
            {"paper_count": len(summaries), "failure_count": total_failures, "papers": summaries},
            sort_keys=True,
        )
    )
    if total_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
