"""Verify every RH-373 manifest hash and fixed membership count."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
MANIFEST = ROOT / "results" / "dependency_manifest.json"
OUTPUT = ROOT / "results" / "archive_verification.json"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.build_archive import EXTERNAL_INPUTS, LOCAL_MEMBERS  # noqa: E402


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _safe_relative(relative: object) -> bool:
    if not isinstance(relative, str):
        return False
    path = Path(relative)
    return not path.is_absolute() and ".." not in path.parts


def _verify_map(base: Path, entries: object, label: str, failures: list[str]) -> int:
    if not isinstance(entries, dict):
        failures.append(f"{label}:not_an_object")
        return 0
    count = 0
    for relative, expected in entries.items():
        count += 1
        if not _safe_relative(relative):
            failures.append(f"{label}:{relative}:unsafe_path")
            continue
        if not isinstance(expected, str) or not _SHA256.fullmatch(expected):
            failures.append(f"{label}:{relative}:invalid_sha256")
            continue
        path = base / relative
        if not path.is_file():
            failures.append(f"{label}:{relative}:missing")
            continue
        if digest(path) != expected:
            failures.append(f"{label}:{relative}:hash_mismatch")
    return count


def main() -> None:
    failures: list[str] = []
    manifest: dict[str, object] = {}
    if not MANIFEST.is_file():
        failures.append("manifest:missing")
    else:
        try:
            loaded = json.loads(MANIFEST.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"manifest:invalid_json:{type(exc).__name__}")
        else:
            if isinstance(loaded, dict):
                manifest = loaded
            else:
                failures.append("manifest:not_an_object")

    if manifest.get("status") != "RH-373_fixed_publication_manifest":
        failures.append("manifest:status")
    local_count = _verify_map(ROOT, manifest.get("publication_artifacts"), "local", failures)
    external_count = _verify_map(WORKSPACE, manifest.get("external_inputs"), "external", failures)
    local_entries = manifest.get("publication_artifacts")
    external_entries = manifest.get("external_inputs")
    if manifest.get("publication_file_count") != local_count:
        failures.append("manifest:publication_file_count")
    if manifest.get("external_input_count") != external_count:
        failures.append("manifest:external_input_count")
    if local_count != len(LOCAL_MEMBERS):
        failures.append("manifest:publication_membership_count")
    elif isinstance(local_entries, dict) and set(local_entries) != set(LOCAL_MEMBERS):
        failures.append("manifest:publication_membership_set")
    if external_count != len(EXTERNAL_INPUTS):
        failures.append("manifest:external_membership_count")
    elif isinstance(external_entries, dict) and set(external_entries) != set(EXTERNAL_INPUTS):
        failures.append("manifest:external_membership_set")

    payload = {
        "status": "RH-373_archive_verified" if not failures else "RH-373_archive_failed",
        "publication_file_count": local_count,
        "external_input_count": external_count,
        "failure_count": len(failures),
        "failures": failures,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
