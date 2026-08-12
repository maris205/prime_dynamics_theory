from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT, ROOT / "experiments", ROOT / "src"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_archive, build_result, build_schema, source_locks, verify_archive  # noqa: E402
from lag_endpoint_extrema.core import exact_equal, loads_strict  # noqa: E402


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_manifest_is_exact_fresh_regeneration() -> None:
    stored_path = ROOT / "results" / "dependency_manifest.json"
    stored = loads_strict(stored_path.read_text(encoding="utf-8"))
    fresh = build_archive.build_payload()
    require(exact_equal(stored, fresh))
    require(stored_path.read_text(encoding="utf-8") == build_archive.serialized_payload(fresh))
    require(stored["publication_file_count"] == len(build_archive.LOCAL_MEMBERS) == 41)
    require(stored["release_stage_file_count"] == 43)
    require(stored["external_git_input_count"] == 184)
    require(stored["remote_logical_input_count"] == 4)
    require(stored["logical_input_total"] == 188)
    require(exact_equal(stored["git_group_sizes"], build_archive.SOURCE_GROUP_SIZES))
    require(exact_equal(stored["git_group_digests"], build_archive.SOURCE_GROUP_DIGESTS))
    require(stored["all_git_source_digest"] == build_archive.ALL_GIT_SOURCE_DIGEST)
    require(exact_equal(
        stored["remote_redistributable_in_release"],
        list(build_archive.REMOTE_REDISTRIBUTION),
    ))
    require(stored["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST)
    require(all(stored[key] is True for key in build_archive.BOOLEAN_KEYS))


def test_archive_report_is_exact_and_failure_free() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    fresh = verify_archive.verify_manifest(manifest)
    stored = loads_strict((ROOT / "results" / "archive_verification.json").read_text(encoding="utf-8"))
    require(exact_equal(stored, fresh))
    require(stored["status"] == "RH-398_archive_verified")
    require(type(stored["failure_count"]) is int and stored["failure_count"] == 0)
    require(stored["failures"] == [])


def test_six_external_payloads_are_excluded_from_members_and_tree() -> None:
    members = set(build_archive.LOCAL_MEMBERS)
    require(len(build_archive.REMOTE_PAYLOAD_HASHES) == 6)
    require({item for item in members if item.endswith(".pdf")} == build_archive.PUBLICATION_PDFS)
    member_hashes = {file_sha(ROOT / item) for item in members}
    tree_hashes = {
        file_sha(path) for path in ROOT.rglob("*") if path.is_file() and not path.is_symlink()
    }
    require(member_hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES))
    require(tree_hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES))
    require(build_archive.payload_hash_scan() == {
        "remote_payload_hash_count": 6,
        "publication_payload_hash_hit_count": 0,
        "tree_payload_hash_hit_count": 0,
    })
    require(build_archive.external_payload_exclusion() is True)


def test_four_offline_remote_replays_make_zero_requests() -> None:
    rows = list(build_archive.offline_remote_replay())
    require([row["source_key"] for row in rows] == list(build_archive.REMOTE_KEYS))
    require(len(rows) == 4)
    require(all(row["status"] == "NETWORK_DISABLED" for row in rows))
    require(all(
        row["network_opt_in"] is False
        and type(row["requests_made"]) is int
        and row["requests_made"] == 0
        for row in rows
    ))


def test_frozen_stage_digests_are_exact() -> None:
    require(len(build_archive.FROZEN_STAGE_DIGESTS) == 21)
    require(all(
        file_sha(ROOT / path) == expected
        for path, expected in build_archive.FROZEN_STAGE_DIGESTS.items()
    ))


def test_manifest_hash_membership_and_path_attacks_fail_closed() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["README.md"] = "0" * 64
    require(verify_archive.verify_manifest(attacked)["failure_count"] > 0)
    for relative in ("unexpected.pdf", "../outside", "x" * 5000):
        attacked = deepcopy(manifest)
        attacked["publication_artifacts"][relative] = "0" * 64
        attacked["publication_file_count"] += 1
        report = verify_archive.verify_manifest(attacked)
        require(report["status"] == "RH-398_archive_failed")
        require(report["failure_count"] > 0)


def test_manifest_nested_type_and_sha_attacks_fail_closed() -> None:
    manifest = build_archive.build_payload()
    attacks = []
    for key, value in (("publication_artifacts", []), ("external_git_inputs", None)):
        attacked = deepcopy(manifest)
        attacked[key] = value
        attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["README.md"] = True
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["extra"] = False
    attacks.append(attacked)
    for payload in attacks:
        require(verify_archive.verify_manifest(payload)["failure_count"] > 0)


def test_remote_order_logical_offline_and_rights_attacks_fail() -> None:
    manifest = build_archive.build_payload()
    attacks = []
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"].reverse()
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["logical_source_digest"] = "0" * 64
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["git_group_sizes"]["rh397_immutable_closure"] = 159
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["git_group_digests"]["rh397_standard8"] = "0" * 64
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["all_git_source_digest"] = "0" * 64
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["offline_remote_replay"][3]["requests_made"] = 1
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["remote_rights_nonvendor_pass"] = False
    attacks.append(attacked)
    for payload in attacks:
        require(verify_archive.verify_manifest(payload)["failure_count"] > 0)


def test_exact_integer_boolean_commit_and_hygiene_attacks_fail() -> None:
    manifest = build_archive.build_payload()
    attacks = []
    for key, value in (
        ("release_stage_file_count", True),
        ("remote_logical_input_count", True),
        ("logical_input_total", 120),
        ("tree_payload_hash_hit_count", 1),
        ("carriage_return_count", True),
        ("unlisted_regular_file_count", 1),
        ("semantic_pdf_match", 1),
    ):
        attacked = deepcopy(manifest)
        attacked[key] = value
        attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["source_commits"]["rh397_release"] = "0" * 40
    attacks.append(attacked)
    for payload in attacks:
        require(verify_archive.verify_manifest(payload)["failure_count"] > 0)


@pytest.mark.parametrize("value", [[], None, 1, "not-an-object"])
def test_nonobject_manifest_has_standard_failure(value: object) -> None:
    report = verify_archive.verify_manifest(value)
    require(report["status"] == "RH-398_archive_failed")
    require(report["failure_count"] == 1)
    require(report["failures"] == ["manifest:top_level_not_an_object"])
    require(report["release_stage_file_count"] == 0)
    require(report["logical_input_total"] == 0)
    require(all(report[key] is False for key in build_archive.BOOLEAN_KEYS))


def test_publication_pdfs_are_byte_identical() -> None:
    main_pdf = ROOT / "main.pdf"
    semantic = ROOT / build_archive.SEMANTIC_PDF
    require(main_pdf.read_bytes() == semantic.read_bytes())
    require(file_sha(main_pdf) == build_archive.FROZEN_STAGE_DIGESTS["main.pdf"])


def test_no_cache_symlink_sentinel_cr_unlisted_or_eof_defect() -> None:
    require(build_archive.tree_hygiene_scan() == {
        "tree_symlink_count": 0,
        "cache_path_count": 0,
        "pyc_file_count": 0,
        "sentinel_path_count": 0,
        "sentinel_content_hit_count": 0,
        "unlisted_regular_file_count": 0,
        "special_path_count": 0,
        "carriage_return_count": 0,
        "text_eof_defect_count": 0,
    })
    require(all(
        (ROOT / item).is_file() and not (ROOT / item).is_symlink()
        for item in build_archive.LOCAL_MEMBERS
    ))


def test_symlink_member_attack_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.write_bytes(b"regular\n")
    link = tmp_path / "link"
    link.symlink_to(target)
    with pytest.raises(FileNotFoundError):
        build_archive.hash_map(tmp_path, ["link"])
    failures: list[str] = []
    require(verify_archive._verify_map(tmp_path, {"link": file_sha(target)}, "attack", failures) == 1)
    require(failures == ["attack:link:missing_or_nonregular"])


def test_literal_sealing_sentinel_attack_is_detected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    probe = tmp_path / "probe.txt"
    probe.write_text("TO_" + "BE_" + "SEALED\n", encoding="utf-8")
    monkeypatch.setattr(build_archive, "ROOT", tmp_path)
    monkeypatch.setattr(build_archive, "LOCAL_MEMBERS", ("probe.txt",))
    scan = build_archive.tree_hygiene_scan()
    require(scan["sentinel_content_hit_count"] == 1)


def test_unlisted_pyc_carriage_return_and_eof_attacks_are_detected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    member = tmp_path / "member.txt"
    member.write_bytes(b"bad\r\n\n")
    (tmp_path / "extra.pyc").write_bytes(b"not-bytecode")
    monkeypatch.setattr(build_archive, "ROOT", tmp_path)
    monkeypatch.setattr(build_archive, "LOCAL_MEMBERS", ("member.txt",))
    scan = build_archive.tree_hygiene_scan()
    require(scan["pyc_file_count"] == 1)
    require(scan["unlisted_regular_file_count"] == 1)
    require(scan["carriage_return_count"] == 1)
    require(scan["text_eof_defect_count"] == 1)


def test_normal_and_optimized_four_objects_are_fresh_exact() -> None:
    names = ("result.json", "result.schema.json", "dependency_manifest.json", "archive_verification.json")
    stored_hashes = [file_sha(ROOT / "results" / name) for name in names]
    artifact_python = Path("/usr/bin/python3")
    require(artifact_python.is_file(), "official Python interpreter is unavailable")
    code = """
import hashlib, sys
sys.path[:0] = ['src', 'experiments', '.']
import build_result, build_schema, build_archive, verify_archive
def emit(raw):
    print(hashlib.sha256(raw).hexdigest(), flush=True)
fresh_result = build_result.build_payload()
stored_result = build_result.loads_strict(
    (build_archive.ROOT / 'results' / 'result.json').read_text(encoding='utf-8')
)
if not build_result.exact_equal(fresh_result, stored_result):
    raise RuntimeError('fresh result differs from stored result')
fresh_schema = build_schema.build_schema(compare_fresh_result=False)
emit(build_result.pretty_json_bytes(fresh_result))
emit(build_result.pretty_json_bytes(fresh_schema))
build_result.build_payload = lambda: fresh_result
build_schema.build_schema = lambda **kwargs: fresh_schema
build_archive.build_payload.cache_clear()
manifest = build_archive.build_payload()
emit(build_archive.serialized_payload(manifest).encode())
verify_archive.build_payload = lambda: manifest
report = verify_archive.verify_manifest(manifest)
emit(verify_archive.serialized_report(report).encode())
"""
    outputs: list[list[str]] = []
    inherited_pythonpath = os.environ.get("PYTHONPATH", "")
    subprocess_pythonpath = os.pathsep.join(
        part for part in ("src", "experiments", ".", inherited_pythonpath) if part
    )
    for optimized in (False, True):
        completed = subprocess.run(
            [str(artifact_python), *(["-OO"] if optimized else []), "-B", "-c", code],
            cwd=ROOT,
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPATH": subprocess_pythonpath,
            },
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        require(completed.returncode == 0, f"optimized={optimized}: {completed.stderr}")
        mode_hashes = completed.stdout.strip().splitlines()
        require(len(mode_hashes) == 4, "unexpected four-object hash output")
        outputs.append(mode_hashes)
    require(outputs == [stored_hashes, stored_hashes])


def test_official_schema_is_closed_and_accepts_result() -> None:
    script = (
        "import importlib.metadata,json,sys;"
        "from jsonschema import Draft202012Validator as V;"
        "p=json.load(open(sys.argv[1],encoding='utf-8'));"
        "s=json.load(open(sys.argv[2],encoding='utf-8'));"
        "V.check_schema(s);"
        "print(importlib.metadata.version('jsonschema'),len(list(V(s).iter_errors(p))))"
    )
    completed = subprocess.run(
        [
            "/usr/bin/python3",
            "-B",
            "-c",
            script,
            str(ROOT / "results" / "result.json"),
            str(ROOT / "results" / "result.schema.json"),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(completed.returncode == 0, completed.stderr)
    require(completed.stdout.strip() == "4.26.0 0")


def test_outer_verifier_replays_without_writing() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    report = verify_archive.verify_manifest(manifest)
    require(report["status"] == "RH-398_archive_verified")
    require(report["failure_count"] == 0)
    require(verify_archive.serialized_report(report) == (
        ROOT / "results" / "archive_verification.json"
    ).read_text(encoding="utf-8"))


def test_release_tests_have_no_bare_asserts() -> None:
    for relative in ("tests/test_archive.py", "tests/test_offline_sources.py"):
        tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), relative)
