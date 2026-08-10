"""Build the fixed RH-391 publication and dependency manifest."""

from __future__ import annotations

from functools import lru_cache
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

for directory in (ROOT, ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_result, build_schema, source_locks  # noqa: E402
from moving_rank_necessity.core import exact_equal, loads_strict, payload_sha256  # noqa: E402


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
    "linear-scale-moving-rank-prime-tail-retention-necessity.pdf",
    "main.log",
    "main.pdf",
    "main.tex",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/external_source_lock.json",
    "results/maynard_external_source_lock.json",
    "results/result.json",
    "results/result.schema.json",
    "src/moving_rank_necessity/__init__.py",
    "src/moving_rank_necessity/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_results.py",
    "tests/test_source_locks.py",
)
PUBLICATION_PDFS = {
    "main.pdf",
    "linear-scale-moving-rank-prime-tail-retention-necessity.pdf",
}
REMOTE_PAYLOAD_HASHES = set(source_locks.REMOTE_PAYLOAD_HASHES)
SOURCE_COMMITS = {"rh390_release": source_locks.RH390_RELEASE}
REMOTE_DIGESTS = [source_locks.JY_CANONICAL_SHA256, source_locks.MAYNARD_CANONICAL_SHA256]
REMOTE_OFFLINE_COMMANDS = (
    (
        "johnston-yang-arxiv-2204.01980v2",
        ROOT.parent / "RH-387-all-order-prime-tail-integral-resummation" / "experiments" / "verify_remote_source.py",
    ),
    (
        "maynard-annals-2015-small-gaps",
        ROOT.parent / "RH-388-rank-one-p2-tail-resummation" / "experiments" / "verify_remote_source.py",
    ),
)
FROZEN_STAGE_DIGESTS = {
    "experiments/source_locks.py": "6f35655b66993633d6af4c02bfac94085a90347868f187b93ff96b91c0d03f97",
    "main.log": "4df66e0d74de6b8b5950b26d93a4ceb372ee5bfa9a436ebfda6128fbafe8b16d",
    "main.pdf": "90275847d4e07c9c6fb8a7fdf8ea291abf1b044bb74c70cd59740c2baef0d9d1",
    "main.tex": "27d58b4745fe0ce8e61ed788d67f76f47ac72774e5e808d952bb51cc9cb83061",
    "references.bib": "63cd8b8859b46fc10b9364557f64220c63f62b1f308bdcecd7ab52cf37abdd5a",
    "results/result.json": "023aa55c4a4e3795994eed866cc9d1412aef90bc0df9b27831f3718c069c1046",
    "results/result.schema.json": "f5fd98019eefdf600432ca59c6546a6c6d5c7c832a4f8da0603512d20ee40f54",
    "src/moving_rank_necessity/core.py": "82eb4d132d73daca7b136e3f5568513ee915d35d2a1e1513ac4ee014192faf40",
}


def digest(path: Path) -> str:
    if not isinstance(path, Path):
        raise TypeError("digest path must be pathlib.Path")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_members(members: tuple[str, ...] | list[str]) -> None:
    if type(members) not in (tuple, list):
        raise TypeError("manifest members must be a tuple or list")
    if len(members) != len(set(members)):
        raise ValueError("manifest member list contains duplicates")
    for relative in members:
        if type(relative) is not str or not relative:
            raise TypeError("manifest member is not nonempty text")
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
    if (
        type(entries) is not list
        or len(entries) != 97
        or type(git_locks.get("count")) is not int
        or git_locks.get("count") != 97
        or git_locks.get("group_sizes") != {"rh390_immutable_closure": 87, "rh390_standard8": 8, "rh390_prior_external_locks": 2}
    ):
        raise RuntimeError("result Git source-lock count or groups are not 97=87+8+2")
    output: dict[str, str] = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise RuntimeError("invalid result Git source-lock row")
        path, source_sha = entry["path"], entry["sha256"]
        if type(path) is not str or type(source_sha) is not str or path in output:
            raise RuntimeError("invalid or duplicate result Git source-lock path")
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
    fresh = source_locks.build_remote_source_locks()
    if not exact_equal(remote, fresh):
        raise RuntimeError("stored remote locks differ from fresh exact locks")
    objects = remote.get("objects")
    if (
        type(remote.get("count")) is not int
        or remote.get("count") != 2
        or type(objects) is not list
        or len(objects) != 2
        or remote.get("network_fetch_performed") is not False
        or remote.get("redistributable_in_release") is not False
        or not exact_equal(remote.get("canonical_digests"), REMOTE_DIGESTS)
    ):
        raise RuntimeError("remote lock count, order, network, or rights contract changed")
    for row in objects:
        if type(row) is not dict or row.get("redistributable_in_release") is not False:
            raise RuntimeError("remote redistribution boundary opened")
        if row.get("pdf_vendored") is not False:
            raise RuntimeError("remote PDF vendoring boundary opened")
        if row.get("source_key") == "johnston-yang-arxiv-2204.01980v2" and row.get("source_tar_vendored") is not False:
            raise RuntimeError("remote source-tar vendoring boundary opened")
    return remote


def payload_hash_scan() -> dict[str, int]:
    if len(REMOTE_PAYLOAD_HASHES) != 4:
        raise RuntimeError("remote payload hash membership changed")
    member_hits = sum(digest(ROOT / relative) in REMOTE_PAYLOAD_HASHES for relative in LOCAL_MEMBERS)
    tree_hits = 0
    for path in ROOT.rglob("*"):
        if path.is_file() and not path.is_symlink() and digest(path) in REMOTE_PAYLOAD_HASHES:
            tree_hits += 1
    return {
        "remote_payload_hash_count": 4,
        "publication_payload_hash_hit_count": member_hits,
        "tree_payload_hash_hit_count": tree_hits,
    }


def external_payload_exclusion() -> bool:
    required = {
        "results/external_source_lock.json",
        "results/maynard_external_source_lock.json",
        "experiments/source_locks.py",
    }
    if not required.issubset(LOCAL_MEMBERS):
        return False
    if {relative for relative in LOCAL_MEMBERS if relative.endswith(".pdf")} != PUBLICATION_PDFS:
        return False
    scan = payload_hash_scan()
    return scan == {
        "remote_payload_hash_count": 4,
        "publication_payload_hash_hit_count": 0,
        "tree_payload_hash_hit_count": 0,
    }


@lru_cache(maxsize=1)
def offline_remote_replay() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    for source_key, verifier in REMOTE_OFFLINE_COMMANDS:
        if not verifier.is_file():
            raise RuntimeError(f"offline verifier is absent: {source_key}")
        completed = subprocess.run(
            [sys.executable, "-B", str(verifier)],
            cwd=verifier.parent.parent,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0 or completed.stderr:
            raise RuntimeError(f"offline verifier failed: {source_key}")
        payload = loads_strict(completed.stdout)
        row = {
            "network_opt_in": payload.get("network_opt_in"),
            "requests_made": payload.get("requests_made"),
            "source_key": source_key,
            "status": payload.get("status"),
        }
        expected = {
            "network_opt_in": False,
            "requests_made": 0,
            "source_key": source_key,
            "status": "NETWORK_DISABLED",
        }
        if not exact_equal(row, expected):
            raise RuntimeError(f"offline verifier touched the network or changed status: {source_key}")
        rows.append(row)
    return tuple(rows)


def build_payload() -> dict[str, object]:
    publication = hash_map(ROOT, LOCAL_MEMBERS)
    result = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
    if not exact_equal(result, build_result.build_payload()):
        raise RuntimeError("stored result differs from fresh result")
    if not exact_equal(schema, build_schema.build_schema()):
        raise RuntimeError("stored schema differs from fresh schema")

    frozen_stage_pass = all(publication.get(path) == expected for path, expected in FROZEN_STAGE_DIGESTS.items())
    if not frozen_stage_pass:
        raise RuntimeError("frozen Stage 1 or manuscript artifact changed")
    result_git = validated_result_git_source_map(result)
    external_git = hash_map(WORKSPACE, list(result_git))
    if not exact_equal(external_git, result_git):
        raise RuntimeError("result Git locks do not match live external inputs")
    remote = validated_remote_locks(result)

    source_contract = result.get("source_locks")
    if type(source_contract) is not dict:
        raise RuntimeError("result source aggregate is absent")
    logical_digest = source_contract.get("logical_source_digest")
    logical_pass = (
        type(logical_digest) is str
        and logical_digest == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_contract.get("git_count") == 97
        and source_contract.get("remote_count") == 2
        and source_contract.get("logical_count") == 99
        and source_contract.get("logical_digest_pass") is True
        and source_contract.get("pass") is True
    )
    if not logical_pass:
        raise RuntimeError("97+2=99 logical source closure is not sealed")

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
    semantic_match = publication["main.pdf"] == publication["linear-scale-moving-rank-prime-tail-retention-necessity.pdf"]
    if not semantic_match:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
    scan = payload_hash_scan()
    payload_excluded = external_payload_exclusion()
    if not payload_excluded:
        raise RuntimeError("an external source payload is present")
    offline_rows = list(offline_remote_replay())

    return {
        "status": "RH-391_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2,
        "external_git_input_count": len(external_git),
        "external_git_inputs": external_git,
        "remote_logical_input_count": 2,
        "logical_input_total": len(external_git) + 2,
        "remote_source_lock_sha256": remote["canonical_digests"],
        "logical_source_digest": logical_digest,
        "source_commits": SOURCE_COMMITS,
        "offline_remote_replay": offline_rows,
        **scan,
        "result_rebuild_match": True,
        "schema_rebuild_match": True,
        "result_source_lock_match": True,
        "release_blob_identity_pass": True,
        "source_digest_contract_pass": True,
        "logical_source_digest_pass": logical_pass,
        "exact_certificate_digest_pass": certificate_pass,
        "remote_lock_exact_pass": True,
        "remote_rights_nonvendor_pass": True,
        "offline_remote_zero_requests": len(offline_rows) == 2,
        "remote_payload_excluded": payload_excluded,
        "semantic_pdf_match": semantic_match,
        "frozen_stage_digest_pass": frozen_stage_pass,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    if type(payload) is not dict:
        raise TypeError("manifest payload must be an exact object")
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(serialized_payload(payload), encoding="utf-8")
    boolean_keys = (
        "result_rebuild_match", "schema_rebuild_match", "result_source_lock_match",
        "release_blob_identity_pass", "source_digest_contract_pass",
        "logical_source_digest_pass", "exact_certificate_digest_pass",
        "remote_lock_exact_pass", "remote_rights_nonvendor_pass",
        "offline_remote_zero_requests", "remote_payload_excluded",
        "semantic_pdf_match", "frozen_stage_digest_pass",
    )
    print(json.dumps({
        "status": payload["status"],
        "publication_file_count": payload["publication_file_count"],
        "release_stage_file_count": payload["release_stage_file_count"],
        "external_git_input_count": payload["external_git_input_count"],
        "remote_logical_input_count": payload["remote_logical_input_count"],
        "logical_input_total": payload["logical_input_total"],
        "all_pass": all(payload[key] is True for key in boolean_keys),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
