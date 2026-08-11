"""Build the fixed RH-396 publication dependency manifest."""

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
from fixed_lag_centered_capacity.core import (  # noqa: E402
    canonical_json_bytes,
    exact_equal,
    loads_strict,
)


SEMANTIC_PDF = "euler-run-spectrum-for-fixed-lag-centered-mobius-capacity.pdf"
LOCAL_MEMBERS = (
    ".gitignore",
    "FORMAT_AUDIT.md",
    "GATE_AUDIT.md",
    "INTEGRITY_AUDIT.md",
    "Makefile",
    "README.md",
    "REMOTE_SOURCE_AUDIT.md",
    "REPRODUCIBILITY_AUDIT.md",
    "RESEARCH_AUDIT.md",
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
    "main.log",
    "main.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/external_source_lock.json",
    "results/maynard_external_source_lock.json",
    "results/result.json",
    "results/result.schema.json",
    "results/tao_external_source_lock.json",
    "results/tao_teravainen_external_source_lock.json",
    "src/fixed_lag_centered_capacity/__init__.py",
    "src/fixed_lag_centered_capacity/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_offline_sources.py",
    "tests/test_result.py",
    "tests/test_schema.py",
    "tests/test_source_locks.py",
)
PUBLICATION_PDFS = {"main.pdf", SEMANTIC_PDF}
REMOTE_PAYLOAD_HASHES = frozenset(source_locks.REMOTE_PAYLOAD_HASHES)
REMOTE_DIGESTS = (
    source_locks.JY_CANONICAL_SHA256,
    source_locks.MAYNARD_CANONICAL_SHA256,
    source_locks.TAO_CANONICAL_SHA256,
    source_locks.TAO_TERAVAINEN_CANONICAL_SHA256,
)
REMOTE_KEYS = (
    "johnston-yang-arxiv-2204.01980v2",
    "maynard-annals-2015-small-gaps",
    "tao-cambridge-2016-logarithmic-chowla",
    "tao-teravainen-arxiv-1708.02610v2",
)
SOURCE_COMMITS = {
    "rh395_release": source_locks.SOURCE_RELEASE,
    "rh394_release": source_locks.RH394_RELEASE,
    "rh375_release": source_locks.RH375_RELEASE,
}
SOURCE_GROUP_SIZES = dict(source_locks.EXPECTED_GROUP_SIZES)
SOURCE_GROUP_DIGESTS = dict(source_locks.EXPECTED_GROUP_DIGESTS)
ALL_GIT_SOURCE_DIGEST = source_locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
REMOTE_REDISTRIBUTION = (False, False, True, False)
FROZEN_STAGE_DIGESTS = {
    "experiments/build_result.py": "d7678d1098a61bdb6f7c5c2c96ee6588e840365b09fedd015f1800146372a376",
    "experiments/build_schema.py": "4c2edf1e16f09955aa64ea79dc452c0cdb3b77ed01b53eaef10fe898ff5c80ba",
    "experiments/source_locks.py": "4805acbe541d8e5e4f07d9fa4cd621b87b7551afeb02a0b9fcc0d8684dfa75f6",
    "main.log": "0cb4d57eb4c1f8ed0203a707fa8915258fb634c7499b69b21a232d731e061a25",
    "main.pdf": "590f472a38bbe652b4f3a2e1eac11a407d9c5ed8a076abb3419334106834db1d",
    "main.tex": "5d9a8c6c9a39436d07a94e082fffc003cfba91ece1d3859c11e2facbd5ffe99d",
    "pyproject.toml": "36d81cd867a9468aa9ad43035ed88dfe8a90600d7d3565359271a1ae21fd7f63",
    "references.bib": "2a5f201d51355bf0eb930484b4c9d3ad3d02bc145eed11809b0ab533956c599f",
    "requirements.txt": "914bc8e6f37d72e03fe795b0924fbe7c007438b5e5c8b71d2cb7ce857a5518ae",
    "results/external_source_lock.json": "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058",
    "results/maynard_external_source_lock.json": "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba",
    "results/result.json": "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4",
    "results/result.schema.json": "b78f958c60b1651446a3e0ac2af7a2e696cba2642a6414237877d997ff51691a",
    "results/tao_external_source_lock.json": "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f",
    "results/tao_teravainen_external_source_lock.json": "52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec",
    "src/fixed_lag_centered_capacity/__init__.py": "ea55858a1129532ff7f27dc9507924d7aa27a6f5f125ebc4d15e4c7a9a167056",
    "src/fixed_lag_centered_capacity/core.py": "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d",
    "tests/test_core.py": "a02e4716f753aa3882ab9999cefc6be125bb8586214b18c15f921de2f64eea74",
    "tests/test_result.py": "30691e20742bf7135c6960a90bf9f8b038af01b2595a4af85145a0ce87656075",
    "tests/test_schema.py": "14068d04629c86a1f243d31851cc69b575bc5922440e05ec35b7b9141f1567e4",
    "tests/test_source_locks.py": "ce61e6b9c9eef136013123ef0fb344a7f9d7f17f2f0507faf17900a997f02b43",
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
    locks = result.get("source_closure")
    if type(locks) is not dict or type(locks.get("git")) is not dict:
        raise RuntimeError("result Git source locks are absent")
    git_locks = locks["git"]
    entries = git_locks.get("entries")
    expected_groups = {
        "rh395_immutable_closure": 148,
        "rh395_standard8": 8,
        "rh395_prior_external_locks": 4,
    }
    if (
        type(entries) is not list
        or len(entries) != 160
        or type(git_locks.get("count")) is not int
        or git_locks.get("count") != 160
        or not exact_equal(git_locks.get("group_sizes"), expected_groups)
    ):
        raise RuntimeError("result Git closure is not 160=148+8+4")
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
    locks = result.get("source_closure")
    if type(locks) is not dict or type(locks.get("remote")) is not dict:
        raise RuntimeError("result remote locks are absent")
    remote = locks["remote"]
    if not exact_equal(remote, source_locks.build_remote_source_locks()):
        raise RuntimeError("stored remote locks differ from fresh exact locks")
    objects = remote.get("objects")
    if (
        type(remote.get("count")) is not int
        or remote.get("count") != 4
        or type(objects) is not list
        or len(objects) != 4
        or remote.get("network_fetch_performed") is not False
        or not exact_equal(remote.get("canonical_digests"), list(REMOTE_DIGESTS))
        or not exact_equal(remote.get("source_keys"), list(REMOTE_KEYS))
        or not exact_equal(remote.get("redistributable_in_release"), [False, False, True, False])
        or remote.get("external_payload_hash_hits") != []
    ):
        raise RuntimeError("remote lock order, count, rights, or network contract changed")
    for index, row in enumerate(objects):
        if type(row) is not dict or row.get("source_key") != REMOTE_KEYS[index]:
            raise RuntimeError("remote source row order changed")
        if row.get("pdf_vendored") is not False:
            raise RuntimeError("remote PDF vendoring boundary opened")
        if row.get("redistributable_in_release") is not [False, False, True, False][index]:
            raise RuntimeError("remote redistribution metadata changed")
    if objects[0].get("source_tar_vendored") is not False:
        raise RuntimeError("Johnston--Yang source-tar vendoring boundary opened")
    return remote


def payload_hash_scan() -> dict[str, int]:
    if len(REMOTE_PAYLOAD_HASHES) != 6:
        raise RuntimeError("remote payload hash membership changed")
    member_hits = sum(digest(ROOT / relative) in REMOTE_PAYLOAD_HASHES for relative in LOCAL_MEMBERS)
    tree_hits = sum(
        digest(path) in REMOTE_PAYLOAD_HASHES
        for path in ROOT.rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    return {
        "remote_payload_hash_count": 6,
        "publication_payload_hash_hit_count": member_hits,
        "tree_payload_hash_hit_count": tree_hits,
    }


def tree_hygiene_scan() -> dict[str, int]:
    cache_names = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    sentinel_names = {".DS_Store", ".gitkeep", "RH_HANDOFF.md"}
    sealing_sentinel = b"TO_" + b"BE_" + b"SEALED"
    tree_paths = list(ROOT.rglob("*"))
    symlinks = sum(path.is_symlink() for path in tree_paths)
    caches = sum(path.name in cache_names for path in tree_paths)
    pyc_files = sum(path.is_file() and path.suffix == ".pyc" for path in tree_paths)
    sentinels = sum(
        path.name in sentinel_names or path.name.endswith((".tmp", ".swp", "~"))
        for path in tree_paths
    )
    sentinel_content_hits = sum(
        sealing_sentinel in path.read_bytes()
        for path in tree_paths
        if path.is_file() and not path.is_symlink()
    )
    allowed_regular = set(LOCAL_MEMBERS) | {
        "results/dependency_manifest.json",
        "results/archive_verification.json",
    }
    unlisted_regular = sum(
        path.is_file()
        and not path.is_symlink()
        and path.relative_to(ROOT).as_posix() not in allowed_regular
        for path in tree_paths
    )
    special_paths = sum(
        not path.is_file() and not path.is_dir() and not path.is_symlink()
        for path in tree_paths
    )
    eof_defects = 0
    carriage_returns = 0
    for relative in LOCAL_MEMBERS:
        if relative.endswith(".pdf") or relative == "main.log":
            continue
        raw = (ROOT / relative).read_bytes()
        carriage_returns += raw.count(b"\r")
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
        "pyc_file_count": pyc_files,
        "sentinel_path_count": sentinels,
        "sentinel_content_hit_count": sentinel_content_hits,
        "unlisted_regular_file_count": unlisted_regular,
        "special_path_count": special_paths,
        "carriage_return_count": carriage_returns,
        "text_eof_defect_count": eof_defects,
    }


def external_payload_exclusion() -> bool:
    required = {
        "results/external_source_lock.json",
        "results/maynard_external_source_lock.json",
        "results/tao_external_source_lock.json",
        "results/tao_teravainen_external_source_lock.json",
        "experiments/source_locks.py",
        "experiments/verify_offline_sources.py",
    }
    return (
        required.issubset(LOCAL_MEMBERS)
        and {item for item in LOCAL_MEMBERS if item.endswith(".pdf")} == PUBLICATION_PDFS
        and payload_hash_scan() == {
            "remote_payload_hash_count": 6,
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
    fresh_result = build_result.build_payload()
    if not exact_equal(result, fresh_result):
        raise RuntimeError("stored result differs from fresh result")
    # The exact stored result has just matched a fresh reconstruction, so the
    # schema builder need not reconstruct that 290 kB object a second time.
    fresh_schema = build_schema.build_schema(compare_fresh_result=False)
    if not exact_equal(schema, fresh_schema):
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

    source_contract = result.get("source_closure")
    logical_digest = (
        source_contract.get("logical_source_digest")
        if type(source_contract) is dict
        else None
    )
    logical_pass = (
        type(source_contract) is dict
        and logical_digest == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_contract.get("git_count") == 160
        and source_contract.get("remote_count") == 4
        and source_contract.get("logical_count") == 164
        and source_contract.get("logical_digest_pass") is True
        and source_contract.get("pass") is True
        and type(source_contract.get("git")) is dict
        and exact_equal(source_contract["git"].get("group_sizes"), SOURCE_GROUP_SIZES)
        and exact_equal(source_contract["git"].get("group_digests"), SOURCE_GROUP_DIGESTS)
        and source_contract["git"].get("all_git_source_digest") == ALL_GIT_SOURCE_DIGEST
        and type(source_contract.get("remote")) is dict
        and exact_equal(
            source_contract["remote"].get("redistributable_in_release"),
            list(REMOTE_REDISTRIBUTION),
        )
    )
    if not logical_pass:
        raise RuntimeError("160+4=164 logical source closure is not sealed")
    role_pass = exact_equal(result.get("source_roles"), build_result.SOURCE_ROLES)
    if not role_pass:
        raise RuntimeError("source role contract changed")

    certificate = result.get("certificate")
    identities = result.get("identities")
    fixture = identities.get("certificate") if type(identities) is dict else None
    certificate_pass = (
        type(certificate) is dict
        and certificate.get("all_pass") is True
        and certificate.get("row_count") == 96
        and sha256(canonical_json_bytes(certificate)).hexdigest()
        == build_result.CERTIFICATE_FIXTURE_SHA256
        and type(fixture) is dict
        and fixture.get("canonical_bytes") == build_result.CERTIFICATE_FIXTURE_BYTES
        and fixture.get("canonical_sha256") == build_result.CERTIFICATE_FIXTURE_SHA256
        and fixture.get("rows") == 96
    )
    if not certificate_pass:
        raise RuntimeError("result certificate differs from sealed fixture")

    semantic_match = (ROOT / "main.pdf").read_bytes() == (ROOT / SEMANTIC_PDF).read_bytes()
    if not semantic_match:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
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
        "status": "RH-396_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2,
        "external_git_input_count": len(external_git),
        "external_git_inputs": external_git,
        "git_group_sizes": SOURCE_GROUP_SIZES,
        "git_group_digests": SOURCE_GROUP_DIGESTS,
        "all_git_source_digest": ALL_GIT_SOURCE_DIGEST,
        "remote_logical_input_count": 4,
        "logical_input_total": len(external_git) + 4,
        "remote_source_lock_sha256": list(REMOTE_DIGESTS),
        "remote_redistributable_in_release": list(REMOTE_REDISTRIBUTION),
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
        "offline_remote_zero_requests": len(offline_rows) == 4,
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
