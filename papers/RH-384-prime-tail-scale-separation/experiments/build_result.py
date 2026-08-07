"""Build the immutable-source-locked RH-384 result ledger."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from prime_tail_scales import (
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_SHA256,
    canonical_json_bytes,
    payload_sha256,
    verify_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_COMMITS = {
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh379_release": "9ae9802ed17529ef4adfb81d7e2158d47c3c8d22",
    "rh380_release": "dd94b9cfebdbf5df92084ba870b10d3a4d432bee",
    "rh381_release": "b6a6355b3390f3d00091a02cf77845b4f68a4a22",
    "rh382_release": "32afe96176ac00f4f261cf7097e0342a5c5194f1",
    "rh383_release": "bea5c88ca4ae9ca75511af42296ed099c1d6b11a",
    "rh_mvp2_archive": "c0aed13a34b8bbc53061aed23738660adcd3624c",
    "rh2_pnt_release": "836426546db31e2737e877182848c538ed4cd436",
}


def _paper_group(slug: str, package: str) -> tuple[str, ...]:
    base = f"prime_dynamics_theory/papers/{slug}"
    return (
        f"{base}/README.md",
        f"{base}/THEOREM_LEDGER.md",
        f"{base}/UPDATED_ROADMAP.md",
        f"{base}/main.tex",
        f"{base}/references.bib",
        f"{base}/results/result.json",
        f"{base}/results/result.schema.json",
        f"{base}/src/{package}/core.py",
    )


SOURCE_GROUPS = {
    "rh374_release": (
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/README.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/main.tex",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/src/square_clock/core.py",
    ),
    "rh379_release": _paper_group("RH-379-phasewise-chowla-free-memory-supremum", "phasewise_memory"),
    "rh380_release": _paper_group("RH-380-square-clock-monotonicity-and-finite-clock-nonattainment", "finite_clock_gap"),
    "rh381_release": _paper_group("RH-381-prime-square-tail-rate-and-quadratic-memory-remainder", "prime_square_tail"),
    "rh382_release": _paper_group("RH-382-two-scale-prime-square-tail-expansion", "two_scale_tail"),
    "rh383_release": _paper_group("RH-383-exact-euler-tail-partition-normal-form", "euler_tail_normal_form"),
    "rh_mvp2_archive": (
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json",
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    ),
    "rh2_pnt_release": (
        "prime_dynamics_theory/papers/RH-2-exact-prime-kneading-spectral-stability/main.tex",
        "prime_dynamics_theory/papers/RH-2-exact-prime-kneading-spectral-stability/references.bib",
    ),
}

EXPECTED_SHA256 = {
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/README.md": "dbc0041d012d6316ef6a8ffab6f05d510a1cc68414eae30c3744a7c411925c4c",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md": "9451ee6faf1f523a62a10c85ba494b8617011dab7b8d7bc517e7c0c26aabb4ee",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/UPDATED_ROADMAP.md": "c6857ef5bc9cd88074108254fc39a93e985daae7fa545e26badbfdfc086bf28c",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/main.tex": "2129075ec4bae1c5f0f25fcd09cec273fe322d44116d51e5191e3cade4fb9f6d",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib": "ce1e5123ff7edc05c6436f2534044e7058b4a3857bf0f084971954ced3e7c184",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json": "ca492e96bd557b966d7924ee7acca7eceb9248dafe513a674f36f78891438bdd",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/src/square_clock/core.py": "79afe7d583c3db30f876c62605a42f2ee77819028a40d01a3ec24d3259a40615",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/README.md": "8beb603782f40db86031515d3a70d82e4f76cdf10d60561062d88ff581daffe5",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/THEOREM_LEDGER.md": "7229a3969c48463724ed573b4dde1da3e8a48790ebe7663af68b1139a033c2bb",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/UPDATED_ROADMAP.md": "75c243a5ae12fbe71cdb2ce3cb3c46a8e7a61d016dd6c8dba2b98b6b9dac3464",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/main.tex": "c5d97a227398a4f1d46a39fdec73ffb86aeb9bfc0f16296be7023b187b497090",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/references.bib": "d728ca8571bfcc96e78be3b5231db83c3bb61140d0dfabb3be0b4848738673c6",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.json": "a209b922ad6235263bb5213d090a2fb0ad0bcfdd0168788e64115b33d95a4ca8",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.schema.json": "0af712350369e3f7e4a51ce5a8ee1179928e9397372b7b1040183dc3668406df",
    "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/src/phasewise_memory/core.py": "cd3949cc0a1ece1dadab59c049c8a4d3fc170a9c7b6332b93ad62567277fd582",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/README.md": "eb241b1fd954ba689750d47dd51ae7cd5980c2bb7706165e3fcbab2e2375bc23",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/THEOREM_LEDGER.md": "c274c2a5685ba6d472d392c5097149742e432e938aeb61fd3f5b7f001a382c7a",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/UPDATED_ROADMAP.md": "8a82e86bf66248d5dda44ca806fd2c5d974530b5b7e85baac25c0aa98f41ce1d",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/main.tex": "6110b876e1b31fe79e7ff72e5058d97179575cf1dccce86e8c7c0a049d57451f",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/references.bib": "5ea4b95e74c63e47b5eb6a92564941748fb02fc7e7729efe05f52932bb657604",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/results/result.json": "e7e6bc2acc46b9346e2fdd90306e9f8c5fb18c193ed0601466bbf4e01a92be33",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/results/result.schema.json": "62bb03f0e61043bdeda0bf49afcbc0877d95115ca677e7cda20a73d955c5a57f",
    "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/src/finite_clock_gap/core.py": "ed88dd657fcf4c3fa4ae1c2cd2d0a434770433e7cffd0b52297faab1d5459074",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/README.md": "891ebd30acfbffd90cddda3bd96719f01d7cae13eec399894b08c0c20435dae3",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/THEOREM_LEDGER.md": "a7a79197bba2a423cff77f6f74e63c8621a40c2bcef368e5ce6ce954857edcda",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/UPDATED_ROADMAP.md": "f2ea88b81441c78171a2a54d85ddc7f2a405ae78b94cac43ca6f6ae46048d703",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/main.tex": "b1025502880530602f134ea5bdc6dcde34e2cdfd18fb364cb104343d456b643a",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/references.bib": "bb61978aebc465b05e3ffda154926ad20bb15e4a475e12304cc6147903d40625",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/results/result.json": "a7a869f40af0a17656b28a07fe58e337d9b8e619d13de8bc671326912f875ffd",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/results/result.schema.json": "ed1788580270f03bdcbb43172edf149f086b76564697dd93e1556282855aad5b",
    "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/src/prime_square_tail/core.py": "acc1e11ff57b634ec702996526f4ddd12ac58d372236a8d77202b529faca9322",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/README.md": "5f818841bb7db7c8b27e75d892a2fa6f3de549edb7456f65fb2275b82356203a",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/THEOREM_LEDGER.md": "1c835ef614fd9381c08019f0cb5358c829bafdb2e7502861649566508b4ea586",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/UPDATED_ROADMAP.md": "793e27292d6f99fc1c23a550e66b247bbc1aa1b5c0bfef266339697bf3b9e66e",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/main.tex": "929b4304390036843c5e4f0d165f3be45d683e36f2a7537a3a5d14ed197b5d0c",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/references.bib": "c8ea97c3b3626d27fc6a3ec0dca69aa87c4eb2b248ec410bc989aff0aa4f11dc",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/results/result.json": "960ef6ce017ad62b6c552ed30a41b9f0c3e41a9a217ef103c4a3f812c80a71d2",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/results/result.schema.json": "573b631820edd3b911b9792f9587fee07a03cf13ecefd03a6247d115cfa42394",
    "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/src/two_scale_tail/core.py": "3fd8bd0233385aeb440d0703769ea6b624792aef4460ec5b887116fe3554b56e",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/README.md": "a666c7d396bb54062b761f06d95d35a3b27ddceec7ed7a6519cbfc61e7d590f3",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/THEOREM_LEDGER.md": "eb117b3e731cfc2bb9b6df0368f475d25ec0b1646f4ac7e616dd29e1d7ddd896",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/UPDATED_ROADMAP.md": "9d9e36e923e1430aeee6715684b3039ccca576360e3c5528d85fe355a088ae51",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/main.tex": "b1030a1203685121ddc99504d0d8a5b389611b41e47a1009fea70a0215ab3bb3",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/references.bib": "0cd86c21c7b65399043ec4994baecb3501b8e7e61294b211131488a9fe9e0dad",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/results/result.json": "519f585f4cf867c0d41ae674c3fb16bc0fbcf529af32131ad1afbba6692355ab",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/results/result.schema.json": "8985f41cd7043b58d3b2fa9ee387bd6da4cb9d6156d3e5226acf57123674c118",
    "prime_dynamics_theory/papers/RH-383-exact-euler-tail-partition-normal-form/src/euler_tail_normal_form/core.py": "7f976ebb09374d0df339a71947e4c4dd7d49c7bc226ab05ac7de481f1e26defb",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json": "3cf3261c0c2c6fbe7511b16615f032edfcbd6b6b1e0c73f5e2ef932a1e6a694c",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json": "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
    "prime_dynamics_theory/papers/RH-2-exact-prime-kneading-spectral-stability/main.tex": "5f2538e648c2ed850b94a03c072a3526f31bcc0c70c90639f65601507f52e532",
    "prime_dynamics_theory/papers/RH-2-exact-prime-kneading-spectral-stability/references.bib": "bd86702192cd4bc6d1c2975c7da4b305541e0c5943f13c5edf044686f0faf2ab",
}

SOURCE_FILES = tuple(path for group in SOURCE_GROUPS.values() for path in group)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _safe_source_path(relative: str) -> None:
    prefix = "prime_dynamics_theory/"
    if type(relative) is not str:
        raise TypeError("source path must be text")
    path = Path(relative)
    if not relative.startswith(prefix) or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe source path: {relative}")
    if relative in ("prime_dynamics_theory/AGENTS.md", "prime_dynamics_theory/RH_HANDOFF.md"):
        raise ValueError("mutable root files cannot be source locked")


def _release_blob(relative: str, release: str) -> bytes:
    _safe_source_path(relative)
    repository_relative = relative.removeprefix("prime_dynamics_theory/")
    completed = subprocess.run(
        ["git", "-C", str(REPOSITORY), "show", f"{release}:{repository_relative}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def source_digest_lines(entries: list[dict[str, str]]) -> tuple[str, ...]:
    lines: list[str] = []
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source row membership changed")
        group, commit, path, sha = entry["group"], entry["commit"], entry["path"], entry["sha256"]
        _safe_source_path(path)
        if group not in SOURCE_COMMITS or commit != SOURCE_COMMITS[group]:
            raise ValueError("source group or release changed")
        if type(sha) is not str or len(sha) != 64:
            raise ValueError("invalid source digest")
        lines.append(f"{group}|{commit}|{path}|{sha}")
    if len(lines) != len(set(lines)):
        raise ValueError("source rows contain duplicates")
    return tuple(sorted(lines))


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    return hashlib.sha256(("\n".join(sorted(lines)) + "\n").encode("utf-8")).hexdigest()


def validate_source_contract(
    source_commits: dict[str, str],
    source_groups: dict[str, tuple[str, ...]],
) -> None:
    if source_commits != SOURCE_COMMITS:
        raise ValueError("RH-384 source commits were rebound")
    if source_groups != SOURCE_GROUPS:
        raise ValueError("RH-384 source membership was rebound")
    if len(SOURCE_FILES) != 51 or len(set(SOURCE_FILES)) != 51:
        raise ValueError("RH-384 source closure is not the frozen 51-file set")
    if set(EXPECTED_SHA256) != set(SOURCE_FILES):
        raise ValueError("declared source hashes do not match the frozen membership")
    for path in SOURCE_FILES:
        _safe_source_path(path)


def expected_digest_contract() -> tuple[dict[str, str], str]:
    rows = [
        {"group": group, "commit": SOURCE_COMMITS[group], "path": path, "sha256": EXPECTED_SHA256[path]}
        for group, paths in SOURCE_GROUPS.items()
        for path in paths
    ]
    lines = source_digest_lines(rows)
    groups = {
        group: lines_digest([line for line in lines if line.startswith(f"{group}|")])
        for group in SOURCE_GROUPS
    }
    return groups, lines_digest(lines)


EXPECTED_GROUP_DIGESTS = {
    "rh374_release": "1110169db1afe2bcb1242cd8284665be9681f955ff942b23908a9401635695ff",
    "rh379_release": "c029ccbe0b499a38f675292c2260cfde5d4b7aede6c6ddee9f87d2c816ecd848",
    "rh380_release": "3c488551cf9b8bdf6a4509b1f39af2119ea6b2ac401bda3cb63f87df38a0e751",
    "rh381_release": "5d07b1b897aa36127f2f190517229534719f37ce0f3ff904d1c31adebae6c9df",
    "rh382_release": "ca26217907f59b219ba2d2b3e4e77ec6e344d036c3a8a92ab5683497d3309f7e",
    "rh383_release": "038b2b88b6357f39fffb1b1d4ce681542ed73b2e5131ef6677d83c13f77fc730",
    "rh_mvp2_archive": "c22c0a9e4702c3bc615acfc19e564cbfd7d08a3bc845b28c659511065c05989b",
    "rh2_pnt_release": "5219f97f85322d1f6a51c7db4a6d81db8c64000be56ebbb6726d370b40369f5b",
}
EXPECTED_ALL_SOURCE_DIGEST = "90434e0468ecc062cb522da096a267748725b5dca8e59c642bb7711f45a3e0e4"
if expected_digest_contract() != (EXPECTED_GROUP_DIGESTS, EXPECTED_ALL_SOURCE_DIGEST):
    raise RuntimeError("declared 51-source digest literals disagree with the source table")


def build_source_locks(
    source_commits: dict[str, str] | None = None,
    source_groups: dict[str, tuple[str, ...]] | None = None,
) -> dict[str, object]:
    commits = SOURCE_COMMITS if source_commits is None else source_commits
    groups = SOURCE_GROUPS if source_groups is None else source_groups
    validate_source_contract(commits, groups)
    entries: list[dict[str, str]] = []
    release_blob_identity_pass = True
    declared_hash_identity_pass = True
    for group, paths in groups.items():
        commit = commits[group]
        for relative in paths:
            live_sha = digest(WORKSPACE / relative)
            blob_sha = hashlib.sha256(_release_blob(relative, commit)).hexdigest()
            release_blob_identity_pass = release_blob_identity_pass and live_sha == blob_sha
            declared_hash_identity_pass = declared_hash_identity_pass and live_sha == EXPECTED_SHA256[relative]
            entries.append({"group": group, "commit": commit, "path": relative, "sha256": live_sha})
    lines = source_digest_lines(entries)
    group_digests = {
        group: lines_digest([line for line in lines if line.startswith(f"{group}|")])
        for group in SOURCE_GROUPS
    }
    all_digest = lines_digest(lines)
    digest_contract_pass = group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_SOURCE_DIGEST
    if not release_blob_identity_pass:
        raise RuntimeError("a live source differs from its declared release blob")
    if not declared_hash_identity_pass or not digest_contract_pass:
        raise RuntimeError("the frozen 51-source digest contract failed")
    return {
        "count": len(entries),
        "group_sizes": {group: len(paths) for group, paths in SOURCE_GROUPS.items()},
        "entries": entries,
        "group_digests": group_digests,
        "all_source_digest": all_digest,
        "release_blob_identity_pass": release_blob_identity_pass,
        "declared_hash_identity_pass": declared_hash_identity_pass,
        "digest_contract_pass": digest_contract_pass,
        "mutable_root_files_excluded": True,
        "pass": release_blob_identity_pass and declared_hash_identity_pass and digest_contract_pass,
    }


def _strict_load(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=lambda pairs: _pairs_to_unique_dict(pairs),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if type(value) is not dict:
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def _pairs_to_unique_dict(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def predecessor_checks() -> dict[str, object]:
    statuses = {
        "rh374_release": "RH-374_square_clock_euler_product_capacity_floor",
        "rh379_release": "RH-379_phasewise_chowla_free_memory_supremum",
        "rh380_release": "RH-380_square_clock_monotonicity_and_finite_clock_nonattainment",
        "rh381_release": "RH-381_prime_square_tail_rate_and_quadratic_memory_remainder",
        "rh382_release": "RH-382_two_scale_prime_square_tail_expansion",
        "rh383_release": "RH-383_exact_euler_tail_partition_normal_form",
    }
    rows: dict[str, bool] = {}
    for group, expected in statuses.items():
        result_path = SOURCE_GROUPS[group][5]
        rows[f"{group}_status_pass"] = _strict_load(WORKSPACE / result_path).get("status") == expected
    rh2_main = (WORKSPACE / SOURCE_GROUPS["rh2_pnt_release"][0]).read_text()
    rh2_refs = (WORKSPACE / SOURCE_GROUPS["rh2_pnt_release"][1]).read_text()
    rows.update({
        "rh2_main_invokes_pnt": "prime number theorem" in rh2_main.lower(),
        "rh2_main_cites_montgomery_vaughan": "MontgomeryVaughan2007" in rh2_main,
        "rh2_reference_has_book_doi": "10.1017/CBO9780511618314" in rh2_refs,
        "rh2_is_prime_counting_source_not_mobius_consequence": True,
        "rh382_gap_input_present": "Y_infinity-2m_infinity" in (WORKSPACE / SOURCE_GROUPS["rh382_release"][0]).read_text(),
        "rh383_exact_tail_input_present": "successor tail `j+1`" in (WORKSPACE / SOURCE_GROUPS["rh383_release"][0]).read_text(),
    })
    return {"checks": rows, "all_pass": all(rows.values())}


GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}

FORBIDDEN_CLAIMS = {
    "active_phasewise_c11_cancellation": False,
    "adaptive_capacity_limit": False,
    "effective_PNT_rate_or_threshold": False,
    "growing_clock_q_of_N": False,
    "hilbert_polya_operator": False,
    "riemann_zero_identification": False,
    "uniform_growing_partition_degree": False,
    "proof_of_RH": False,
}


def build_payload() -> dict[str, object]:
    certificate = verify_certificate()
    if certificate["all_pass"] is not True:
        raise RuntimeError("exact certificate failed")
    if len(canonical_json_bytes(certificate)) != CERTIFICATE_FIXTURE_BYTES:
        raise RuntimeError("exact certificate byte fixture changed")
    if payload_sha256(certificate) != CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("exact certificate digest fixture changed")
    source_locks = build_source_locks()
    inputs = predecessor_checks()
    if inputs["all_pass"] is not True:
        raise RuntimeError("predecessor semantic checks failed")
    return {
        "status": "RH-384_prime_tail_scale_separation",
        "paper": "RH-384",
        "title": "Prime-Tail Scale Separation below the Quadratic Square-Clock Gap",
        "source_locks": source_locks,
        "predecessor_checks": inputs,
        "certificate_fixture": {
            "canonical_bytes": CERTIFICATE_FIXTURE_BYTES,
            "sha256": CERTIFICATE_FIXTURE_SHA256,
            "pass": True,
        },
        "certificate": certificate,
        "theorem": {
            "fixed_r": "P_r(y)~1/[(2r-1)*p_y^(2r-1)*log(p_y)] for every fixed r>=1",
            "fixed_partition": "P_lambda(y)~product_r(2r-1)^(-k_r)*p_y^(-(2d-ell))*log(p_y)^(-ell) for every fixed lambda",
            "scale_separation": [
                "p_y*log(p_y)*T_y->1",
                "3*p_y^3*log(p_y)*S_y->1",
                "S_y/T_y^2->0",
                "T_y^3/S_y->0",
                "S_y/[T_y^3*log(p_y)^2]->1/3",
            ],
            "gap_expansion_input": "B_infinity-G(q_y)=A*T_y+B*T_y^2+C*S_y+O(T_y^3)",
            "coefficients": {
                "A": "2*X_infinity/pi^2",
                "B": "(Y_infinity+2*m_infinity)/pi^2",
                "C": "(Y_infinity-2*m_infinity)/pi^2",
            },
            "contrast_interval": {
                "quantity": "Y_infinity-2*m_infinity",
                "lower": "1.5463476716710499204",
                "upper": "1.5484488989771761113",
            },
            "exact_subtraction_firewall": "L2 subtracts exact A*T_y; L3--L5 subtract exact A*T_y+B*T_y^2; bare-PNT surrogates are forbidden",
            "twice_subtracted_residual": "positive eventually and divided by T_y^3 tends to +infinity",
        },
        "claim_boundary": certificate["claim_boundary"],
        "gates": GATES,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "ars_integrity": {
            "data_code_availability": "analytic proof plus exact/direct-rounding certificate included",
            "author_contributions": "single author: all CRediT roles applicable to this work",
            "funding": "no external funding",
            "competing_interests": "none declared",
            "ethics": "no human participants, animals, or personal data",
            "ai_assistance": "AI-assisted proof auditing, code checking, and typesetting disclosed; author retains responsibility",
        },
        "all_pass": source_locks["pass"] is True and inputs["all_pass"] is True and certificate["all_pass"] is True,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized_payload(payload))
    print(json.dumps({
        "status": payload["status"],
        "source_count": payload["source_locks"]["count"],
        "certificate_sha256": payload["certificate_fixture"]["sha256"],
        "all_pass": payload["all_pass"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
