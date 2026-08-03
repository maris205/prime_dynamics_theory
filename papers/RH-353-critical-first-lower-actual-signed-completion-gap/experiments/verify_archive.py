"""Verify the RH-353 individual publication manifest."""

from __future__ import annotations

import json

from build_archive import ROOT, digest, publication_files


def verification_payload() -> dict[str, object]:
    manifest = json.loads(
        (ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8")
    )
    expected = manifest["files"]
    current = {str(path.relative_to(ROOT)): path for path in publication_files()}
    failures = []
    if manifest.get("status") != f"{ROOT.name}_publication_manifest":
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
    return {
        "status": f"{ROOT.name}_archive_verified",
        "file_count": manifest["file_count"],
        "failure_count": len(failures),
        "failures": failures,
    }


def main() -> None:
    payload = verification_payload()
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, sort_keys=True))
    if payload["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
