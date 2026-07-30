"""Verify publication manifests for RH-272 through RH-281."""

from __future__ import annotations

import json

from build_archive import digest, paper_directories, publication_files


def main() -> None:
    total_failures = 0
    summaries = []
    for directory in paper_directories():
        manifest = json.loads(
            (directory / "results/dependency_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        expected = manifest["files"]
        current = {
            str(path.relative_to(directory)): path
            for path in publication_files(directory)
        }
        failures = []
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
        (directory / "results/archive_verification.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
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
            {
                "paper_count": len(summaries),
                "failure_count": total_failures,
                "papers": summaries,
            },
            sort_keys=True,
        )
    )
    if total_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
