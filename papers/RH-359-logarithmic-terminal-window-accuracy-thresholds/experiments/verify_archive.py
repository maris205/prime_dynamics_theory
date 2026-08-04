"""Verify the RH-359 individual publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def strict_load(path: Path) -> dict[str, object]:
    def hook(pairs):
        output = {}
        for key, value in pairs:
            if key in output:
                raise ValueError(f"duplicate JSON key: {key}")
            output[key] = value
        return output

    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=hook,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON constant: {value}")
        ),
    )


def verification_payload() -> dict[str, object]:
    manifest = strict_load(ROOT / "results" / "dependency_manifest.json")
    failures = []
    files = manifest.get("files", {})
    if not isinstance(files, dict):
        raise TypeError("manifest files field must be an object")
    for relative, expected in files.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append({"path": relative, "reason": "missing"})
        elif digest(path) != expected:
            failures.append({"path": relative, "reason": "sha256_mismatch"})
    return {
        "status": f"{ROOT.name}_archive_verified",
        "file_count": len(files),
        "failure_count": len(failures),
        "failures": failures,
    }


def main() -> None:
    output = ROOT / "results" / "archive_verification.json"
    payload = verification_payload()
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, sort_keys=True))
    if payload["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
