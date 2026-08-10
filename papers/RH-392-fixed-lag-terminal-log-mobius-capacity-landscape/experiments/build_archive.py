"""Build the fixed RH-392 publication dependency manifest."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"
for directory in (ROOT, ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_result, build_schema, source_locks  # noqa: E402
from fixed_lag_capacity.core import exact_equal, loads_strict, payload_sha256  # noqa: E402


SEMANTIC_PDF = "fixed-lag-terminal-log-mobius-diagonalization-and-square-divisor-capacity-landscape.pdf"
LOCAL_MEMBERS = (
    ".gitignore",
    "FORMAT_AUDIT.md",
    "INTEGRITY_AUDIT.md",
    "Makefile",
    "README.md",
    "REMOTE_SOURCE_AUDIT.md",
    "REPLAY_AUDIT.md",
    "REVIEW_AUDIT.md",
    "TABLE_TRACE.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "VISUAL_QA.md",
    "experiments/build_archive.py",
    "experiments/build_result.py",
    "experiments/build_schema.py",
    "experiments/source_locks.py",
    "experiments/verify_archive.py",
    "experiments/verify_offline_sources.py",
    SEMANTIC_PDF,
    "main.tex",
    "outputs/main.log",
    "outputs/main.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/external_source_lock.json",
    "results/maynard_external_source_lock.json",
    "results/result.json",
    "results/result.schema.json",
    "results/tao_external_source_lock.json",
    "src/fixed_lag_capacity/__init__.py",
    "src/fixed_lag_capacity/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_offline_sources.py",
    "tests/test_result.py",
    "tests/test_schema.py",
    "tests/test_source_locks.py",
)
PUBLICATION_PDFS = {"outputs/main.pdf", SEMANTIC_PDF}
REMOTE_PAYLOAD_HASHES = frozenset(source_locks.REMOTE_PAYLOAD_HASHES)
REMOTE_DIGESTS = (
    source_locks.JY_CANONICAL_SHA256,
    source_locks.MAYNARD_CANONICAL_SHA256,
    source_locks.TAO_CANONICAL_SHA256,
)
REMOTE_KEYS = (
    "johnston-yang-arxiv-2204.01980v2",
    "maynard-annals-2015-small-gaps",
    "tao-cambridge-2016-logarithmic-chowla",
)
SOURCE_COMMITS = {"rh389_release": source_locks.SOURCE_RELEASE}
FROZEN_STAGE_DIGESTS = {
    "experiments/build_result.py": "2d33ee9284524a328ab902a6dfadf8ae31078c6391c83914a0dad41d11fb6cf4",
    "experiments/build_schema.py": "66edfaec4bb4395516ad489ef59b1de85b7fdbd6e51c678a69086ac1c8f3b479",
    "experiments/source_locks.py": "189fa0a7630925f18cf299f0805a997fc77a7edc28e9df198ce05d332ad3b568",
    "main.tex": "693f38a69b7f6c35d3a89e98191d0dd27789fd9d14e4057684c942f14bf18112",
    "outputs/main.log": "060e40171624e9c7571e18a01a0025dc3e9f7ccf2aa1ab0e82f3337bc76358c1",
    "outputs/main.pdf": "c8a90aadb7c1f86373e094124cf5e9b279cd764daeab8f014784f0b35345b056",
    "references.bib": "5b3073a8381da87a30615e18f0b4ae09f1165acb28ed01bf457058489d9a8bb7",
    "results/result.json": "83bab4eb57f1d4d2d31c646946df16203b155d49d78942f74a40df239e404bc0",
    "results/result.schema.json": "606d0ae74b4da9e4a97e6a951e89dfd4237108028c9b2436030e2d6861ec8f5d",
    "src/fixed_lag_capacity/core.py": "a4e297f4c324ba1fce1829e5c1caf1b8a7e451a9b90c1f78be5f00d44cd97397",
}
BOOLEAN_KEYS = (
    "result_rebuild_match",
    "schema_rebuild_match",
    "official_schema_validation_pass",
    "result_source_lock_match",
    "release_blob_identity_pass",
    "source_digest_contract_pass",
    "logical_source_digest_pass",
    "source_role_contract_pass",
    "exact_certificate_digest_pass",
    "remote_lock_exact_pass",
    "remote_rights_nonvendor_pass",
    "offline_remote_zero_requests",
    "remote_payload_excluded",
    "semantic_pdf_match",
    "frozen_stage_digest_pass",
    "tree_hygiene_pass",
)


def digest(path: Path) -> str:
    if not isinstance(path, Path):
        raise TypeError("digest path must be pathlib.Path")
    hasher = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_members(members: tuple[str, ...] | list[str]) -> None:
    if type(members) not in (tuple, list) or len(members) != len(set(members)):
        raise TypeError("manifest members must be a unique tuple or list")
    for relative in members:
        if type(relative) is not str or not relative:
            raise TypeError("manifest member must be nonempty exact text")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"manifest member escapes its base: {relative}")


def hash_map(base: Path, members: tuple[str, ...] | list[str]) -> dict[str, str]:
    if not isinstance(base, Path):
        raise TypeError("manifest base must be pathlib.Path")
    _check_members(members)
    output: dict[str, str] = {}
    for relative in members:
        path = base / relative
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(path)
        output[relative] = digest(path)
    return output


def validated_result_git_source_map(result: dict[str, object]) -> dict[str, str]:
    if type(result) is not dict:
        raise TypeError("result must be an exact object")
    locks = result.get("source_locks")
    if type(locks) is not dict or type(locks.get("git")) is not dict:
        raise RuntimeError("result Git source locks are absent")
    git_locks = locks["git"]
    entries = git_locks.get("entries")
    expected_groups = {
        "rh389_immutable_closure": 95,
        "rh389_standard8": 8,
        "rh389_prior_external_locks": 3,
    }
    if (
        type(entries) is not list
        or len(entries) != 106
        or type(git_locks.get("count")) is not int
        or git_locks.get("count") != 106
        or not exact_equal(git_locks.get("group_sizes"), expected_groups)
    ):
        raise RuntimeError("result Git closure is not 106=95+8+3")
    output: dict[str, str] = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise RuntimeError("invalid result Git source-lock row")
        path, source_sha = entry["path"], entry["sha256"]
        if type(path) is not str or type(source_sha) is not str or path in output:
            raise RuntimeError("invalid or duplicate result Git source-lock path")
        safe = Path(path)
        if safe.is_absolute() or ".." in safe.parts:
            raise RuntimeError("unsafe result Git source-lock path")
        output[path] = source_sha
    if not exact_equal(git_locks, source_locks.build_git_source_locks()):
        raise RuntimeError("stored Git locks differ from fresh release-blob locks")
    return output


def validated_remote_locks(result: dict[str, object]) -> dict[str, object]:
    if type(result) is not dict:
        raise TypeError("result must be an exact object")
    locks = result.get("source_locks")
    if type(locks) is not dict or type(locks.get("remote")) is not dict:
        raise RuntimeError("result remote locks are absent")
    remote = locks["remote"]
    if not exact_equal(remote, source_locks.build_remote_source_locks()):
        raise RuntimeError("stored remote locks differ from fresh exact locks")
    objects = remote.get("objects")
    if (
        type(remote.get("count")) is not int
        or remote.get("count") != 3
        or type(objects) is not list
        or len(objects) != 3
        or remote.get("network_fetch_performed") is not False
        or not exact_equal(remote.get("canonical_digests"), list(REMOTE_DIGESTS))
        or not exact_equal(remote.get("source_keys"), list(REMOTE_KEYS))
        or not exact_equal(remote.get("redistributable_in_release"), [False, False, True])
        or remote.get("external_payload_hash_hits") != []
    ):
        raise RuntimeError("remote lock order, count, rights, or network contract changed")
    for index, row in enumerate(objects):
        if type(row) is not dict or row.get("source_key") != REMOTE_KEYS[index]:
            raise RuntimeError("remote source row order changed")
        if row.get("pdf_vendored") is not False:
            raise RuntimeError("remote PDF vendoring boundary opened")
        if row.get("redistributable_in_release") is not [False, False, True][index]:
            raise RuntimeError("remote redistribution metadata changed")
    if objects[0].get("source_tar_vendored") is not False:
        raise RuntimeError("Johnston--Yang source-tar vendoring boundary opened")
    return remote


def payload_hash_scan() -> dict[str, int]:
    if len(REMOTE_PAYLOAD_HASHES) != 5:
        raise RuntimeError("remote payload hash membership changed")
    member_hits = sum(digest(ROOT / relative) in REMOTE_PAYLOAD_HASHES for relative in LOCAL_MEMBERS)
    tree_hits = sum(
        digest(path) in REMOTE_PAYLOAD_HASHES
        for path in ROOT.rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    return {
        "remote_payload_hash_count": 5,
        "publication_payload_hash_hit_count": member_hits,
        "tree_payload_hash_hit_count": tree_hits,
    }


def tree_hygiene_scan() -> dict[str, int]:
    cache_names = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    sentinel_names = {".DS_Store", ".gitkeep", "RH_HANDOFF.md"}
    tree_paths = list(ROOT.rglob("*"))
    symlinks = sum(path.is_symlink() for path in tree_paths)
    caches = sum(path.name in cache_names for path in tree_paths)
    sentinels = sum(
        path.name in sentinel_names or path.name.endswith((".tmp", ".swp", "~"))
        for path in tree_paths
    )
    eof_defects = 0
    for relative in LOCAL_MEMBERS:
        if relative.endswith(".pdf") or relative == "outputs/main.log":
            continue
        raw = (ROOT / relative).read_bytes()
        try:
            raw.decode("utf-8")
        except UnicodeError:
            eof_defects += 1
        else:
            if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
                eof_defects += 1
    return {
        "tree_symlink_count": symlinks,
        "cache_path_count": caches,
        "sentinel_path_count": sentinels,
        "text_eof_defect_count": eof_defects,
    }


def external_payload_exclusion() -> bool:
    required = {
        "results/external_source_lock.json",
        "results/maynard_external_source_lock.json",
        "results/tao_external_source_lock.json",
        "experiments/source_locks.py",
        "experiments/verify_offline_sources.py",
    }
    return (
        required.issubset(LOCAL_MEMBERS)
        and {item for item in LOCAL_MEMBERS if item.endswith(".pdf")} == PUBLICATION_PDFS
        and payload_hash_scan() == {
            "remote_payload_hash_count": 5,
            "publication_payload_hash_hit_count": 0,
            "tree_payload_hash_hit_count": 0,
        }
    )


@lru_cache(maxsize=1)
def offline_remote_replay() -> tuple[dict[str, object], ...]:
    verifier = ROOT / "experiments" / "verify_offline_sources.py"
    rows: list[dict[str, object]] = []
    for source_key in REMOTE_KEYS:
        completed = subprocess.run(
            [sys.executable, "-B", str(verifier), "--source", source_key],
            cwd=ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode or completed.stderr:
            raise RuntimeError(f"offline verifier failed: {source_key}")
        payload = loads_strict(completed.stdout)
        if type(payload) is not dict:
            raise RuntimeError("offline verifier returned a nonobject")
        row = {
            "network_opt_in": payload.get("network_opt_in"),
            "requests_made": payload.get("requests_made"),
            "source_key": payload.get("source_key"),
            "status": payload.get("status"),
        }
        expected = {
            "network_opt_in": False,
            "requests_made": 0,
            "source_key": source_key,
            "status": "NETWORK_DISABLED",
        }
        if not exact_equal(row, expected):
            raise RuntimeError(f"offline verifier changed status: {source_key}")
        rows.append(row)
    return tuple(rows)


def _official_schema_pass(result: dict[str, object], schema: dict[str, object]) -> bool:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise RuntimeError("official jsonschema dependency is unavailable") from exc
    Draft202012Validator.check_schema(schema)
    return list(Draft202012Validator(schema).iter_errors(result)) == []


@lru_cache(maxsize=1)
def build_payload() -> dict[str, object]:
    publication = hash_map(ROOT, LOCAL_MEMBERS)
    result = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
    if type(result) is not dict or type(schema) is not dict:
        raise RuntimeError("stored result or schema is not an object")
    if not exact_equal(result, build_result.build_payload()):
        raise RuntimeError("stored result differs from fresh result")
    if not exact_equal(schema, build_schema.build_schema()):
        raise RuntimeError("stored schema differs from fresh schema")
    build_schema.validate_exact_instance(result, schema)
    if not _official_schema_pass(result, schema):
        raise RuntimeError("official Draft 2020-12 validation failed")

    frozen_pass = all(publication.get(path) == expected for path, expected in FROZEN_STAGE_DIGESTS.items())
    if not frozen_pass:
        raise RuntimeError("frozen Stage 1 or manuscript artifact changed")
    result_git = validated_result_git_source_map(result)
    external_git = hash_map(WORKSPACE, list(result_git))
    if not exact_equal(external_git, result_git):
        raise RuntimeError("result Git locks do not match live external inputs")
    remote = validated_remote_locks(result)

    source_contract = result.get("source_locks")
    logical_digest = source_contract.get("logical_source_digest") if type(source_contract) is dict else None
    logical_pass = (
        type(source_contract) is dict
        and logical_digest == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_contract.get("git_count") == 106
        and source_contract.get("remote_count") == 3
        and source_contract.get("logical_count") == 109
        and source_contract.get("logical_digest_pass") is True
        and source_contract.get("pass") is True
    )
    if not logical_pass:
        raise RuntimeError("106+3=109 logical source closure is not sealed")
    role_pass = exact_equal(result.get("source_roles"), build_result.SOURCE_ROLES)
    if not role_pass:
        raise RuntimeError("source role contract changed")

    certificate = result.get("certificate")
    fixture = result.get("certificate_fixture")
    certificate_pass = (
        type(certificate) is dict
        and payload_sha256(certificate) == build_result.CERTIFICATE_FIXTURE_SHA256
        and type(fixture) is dict
        and fixture.get("canonical_bytes") == build_result.CERTIFICATE_FIXTURE_BYTES
        and fixture.get("sha256") == build_result.CERTIFICATE_FIXTURE_SHA256
        and fixture.get("pass") is True
    )
    if not certificate_pass:
        raise RuntimeError("result certificate differs from sealed fixture")

    semantic_match = (ROOT / "outputs" / "main.pdf").read_bytes() == (ROOT / SEMANTIC_PDF).read_bytes()
    if not semantic_match:
        raise RuntimeError("semantic PDF is not byte-identical to outputs/main.pdf")
    scan = payload_hash_scan()
    payload_excluded = external_payload_exclusion()
    if not payload_excluded:
        raise RuntimeError("an external source payload is present")
    hygiene = tree_hygiene_scan()
    hygiene_pass = all(type(value) is int and value == 0 for value in hygiene.values())
    if not hygiene_pass:
        raise RuntimeError("tree hygiene gate failed")
    offline_rows = list(offline_remote_replay())

    return {
        "status": "RH-392_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2,
        "external_git_input_count": len(external_git),
        "external_git_inputs": external_git,
        "remote_logical_input_count": 3,
        "logical_input_total": len(external_git) + 3,
        "remote_source_lock_sha256": list(REMOTE_DIGESTS),
        "logical_source_digest": logical_digest,
        "source_commits": SOURCE_COMMITS,
        "offline_remote_replay": offline_rows,
        **scan,
        **hygiene,
        "result_rebuild_match": True,
        "schema_rebuild_match": True,
        "official_schema_validation_pass": True,
        "result_source_lock_match": True,
        "release_blob_identity_pass": True,
        "source_digest_contract_pass": True,
        "logical_source_digest_pass": logical_pass,
        "source_role_contract_pass": role_pass,
        "exact_certificate_digest_pass": certificate_pass,
        "remote_lock_exact_pass": True,
        "remote_rights_nonvendor_pass": True,
        "offline_remote_zero_requests": len(offline_rows) == 3,
        "remote_payload_excluded": payload_excluded,
        "semantic_pdf_match": semantic_match,
        "frozen_stage_digest_pass": frozen_pass,
        "tree_hygiene_pass": hygiene_pass,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    if type(payload) is not dict:
        raise TypeError("manifest payload must be an exact object")
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(serialized_payload(payload), encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "publication_file_count": payload["publication_file_count"],
        "release_stage_file_count": payload["release_stage_file_count"],
        "external_git_input_count": payload["external_git_input_count"],
        "remote_logical_input_count": payload["remote_logical_input_count"],
        "logical_input_total": payload["logical_input_total"],
        "all_pass": all(payload[key] is True for key in BOOLEAN_KEYS),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
