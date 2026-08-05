"""Independently verify the RH-363 fixed publication manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
MANIFEST = ROOT / "results" / "dependency_manifest.json"
OUTPUT = ROOT / "results" / "archive_verification.json"
SHA256 = re.compile(r"[0-9a-f]{64}")

EXPECTED_PUBLICATION_MEMBERS = {
    ".gitignore",
    "Makefile",
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "experiments/build_archive.py",
    "experiments/build_result.py",
    "experiments/verify_archive.py",
    "main.pdf",
    "main.tex",
    "prime-return-admissible-entropy-tower.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "src/return_entropy_tower/__init__.py",
    "src/return_entropy_tower/core.py",
    "tests/test_archive.py",
    "tests/test_results.py",
    "tests/test_theory.py",
}

EXPECTED_EXTERNAL_INPUTS = {
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "README.md",
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "main.tex",
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "results/result.json",
    "dyna_zeta_map/paper/sections/3_5_core.tex",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_manifest.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_verification.json",
}

EXPECTED_SOURCE_COMMITS = {
    "prime_dynamics_theory_rh362_release":
        "54709f1c0b30e7970ebca010973a24a1d2656c7e",
    "dyna_zeta_map": "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
}


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
        path.read_text(),
        object_pairs_hook=hook,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON constant: {value}")
        ),
    )


def safe_path(base: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise RuntimeError(f"invalid archive path: {relative!r}")
    base_resolved = base.resolve()
    path = (base_resolved / relative).resolve()
    try:
        path.relative_to(base_resolved)
    except ValueError as exc:
        raise RuntimeError(f"archive path escapes root: {relative}") from exc
    if path == base_resolved:
        raise RuntimeError("archive path names its root")
    return path


def validate_manifest(manifest: dict[str, object]) -> None:
    if manifest.get("status") != "RH-363_fixed_publication_manifest":
        raise RuntimeError("archive status changed")
    publication = manifest.get("publication_artifacts")
    external = manifest.get("external_inputs")
    if not isinstance(publication, dict) or set(publication) != EXPECTED_PUBLICATION_MEMBERS:
        raise RuntimeError("publication membership changed")
    if not isinstance(external, dict) or set(external) != EXPECTED_EXTERNAL_INPUTS:
        raise RuntimeError("external-input membership changed")
    if manifest.get("publication_file_count") != len(EXPECTED_PUBLICATION_MEMBERS):
        raise RuntimeError("publication file count changed")
    if manifest.get("external_input_count") != len(EXPECTED_EXTERNAL_INPUTS):
        raise RuntimeError("external input count changed")
    if manifest.get("source_commits") != EXPECTED_SOURCE_COMMITS:
        raise RuntimeError("source commit lock changed")


def verify_map(base: Path, rows: object, label: str) -> tuple[int, list[dict[str, str]]]:
    if not isinstance(rows, dict):
        raise TypeError(f"{label} must be an object")
    failures: list[dict[str, str]] = []
    for relative, expected in rows.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise TypeError(f"invalid {label} row")
        if not SHA256.fullmatch(expected):
            raise RuntimeError(f"invalid {label} SHA-256: {relative}")
        path = safe_path(base, relative)
        if not path.is_file():
            failures.append({"path": relative, "reason": "missing"})
        elif digest(path) != expected:
            failures.append({"path": relative, "reason": "sha256_mismatch"})
    return len(rows), failures


def verification_payload() -> dict[str, object]:
    manifest = strict_load(MANIFEST)
    validate_manifest(manifest)
    publication_count, publication_failures = verify_map(
        ROOT, manifest.get("publication_artifacts"), "publication_artifacts"
    )
    external_count, external_failures = verify_map(
        WORKSPACE, manifest.get("external_inputs"), "external_inputs"
    )
    failures = publication_failures + external_failures
    if manifest.get("publication_file_count") != publication_count:
        failures.append({"path": "publication_file_count", "reason": "count_mismatch"})
    if manifest.get("external_input_count") != external_count:
        failures.append({"path": "external_input_count", "reason": "count_mismatch"})
    return {
        "status": "RH-363_archive_verified",
        "publication_file_count": publication_count,
        "external_input_count": external_count,
        "failure_count": len(failures),
        "failures": failures,
    }


def main() -> None:
    payload = verification_payload()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if payload["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
