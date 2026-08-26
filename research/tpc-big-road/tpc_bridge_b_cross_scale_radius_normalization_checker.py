#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-270 finite radius audit."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-270-cross-scale-radius-normalization"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_cross_scale_radius_normalization.md"
PRODUCER = PROJECT / "code/tpc270_cross_scale_radius_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc270_independent_checker.py"
STRESS = PROJECT / "experiments/tpc270_normalization_stress.py"
CERTIFICATE = PROJECT / "results/tpc270_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "e129f19b8290277e5afbc162c84b03d9a25e8640"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT"
BRIDGE_SHA256 = "2c58d4d040d187fff35f21fd02354bd4d5a334956daa9cedd91d86a6e4e1a0e1"

# These hashes freeze the last released upstream interface.  They deliberately
# use git objects at BASELINE_HEAD so later dynamic documentation cannot alter
# the meaning of this bridge.
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "c8f182995c5f7fce93b6eda7d0a10ffa2827714752423053549f038403780204",
    "papers/tpc-269-growing-cutoff-profile-transfer/README.md": "ed56f6403d1037c37a1ebe0960c515e6fef135d2c079ebb12e13b957099604df",
    "papers/tpc-269-growing-cutoff-profile-transfer/PROOF_PACKAGE.md": "4284ee1b1919851f3b7ab1f94b89cdbc8eadbcded7007c65c3aecb4767c56d1b",
    "papers/tpc-269-growing-cutoff-profile-transfer/notes/theorem_ledger.md": "45491ee91ae494044c48821f97781899fbeb3eaaf8f0192c80ffbbec5120cd08",
    "papers/tpc-269-growing-cutoff-profile-transfer/notes/route_evaluation.md": "214d593ff8260186b47e50e4d62241cd863828451708b4d94222e8726012ab58",
    "research/tpc-big-road/bridge_b_growing_cutoff_profile_transfer.md": "139f07492d1d27d0f2feeb81626f37c9820ffa9c14065489eca77190bd8f1e9d",
    "research/tpc-big-road/tpc_bridge_b_growing_cutoff_profile_transfer_checker.py": "a1df4ab209e2b7fa78880bd5f25c239b88df48e0178a28de4a1775236b592881",
}

PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "8af2e8cc1eca745b2f2fdf9268f1aba142c9318deeaf3ffe7fb5703f6ba1df00",
    "PAPER_PLAN.md": "405e75d765d238e4b9a648c4f17accc43b3238c147929289aa1a9293a7aba670",
    "PROOF_PACKAGE.md": "496bb49033007cab6aba66f4076112ad739d3ccc52627574e93c61dc85d8cd1d",
    "README.md": "349fc7fecc193f03a0eac98a5ca0ad0044fed5b2c59f60cfd751c990f90f0138",
    "code/tpc270_cross_scale_radius_certificate.py": "ffa82a23bf4592b7e5ecbeb4e97ff6def4ee61007f8e1c2bb31e388902d50ca1",
    "experiments/tpc270_independent_checker.py": "c75c457b7df16a97ddf1c427acb1bf1de2f01802b031e8df29f58104ad33eb90",
    "experiments/tpc270_normalization_stress.py": "13827e5c872c7861c19149bc567c62b09c5b665223455102b9501f6c3c234cd0",
    "notes/citation_verification.md": "70230e230c3b184270e4784b5287789100c654ad104d7bffb860d74e07405dff",
    "notes/claim_firewall.md": "f5ecb1e49abe333e2d97ce577a3ee997ecb3b0884dd16aadcb6a7c4413b9558e",
    "notes/computational_protocol.md": "3203fc02418aadadeaf2120584a4280de3369971805e13535e5b59730545ad35",
    "notes/route_evaluation.md": "44cc3d77fac5ed08e30f21f317ca9b8952a81b31640ca9371237622ff1d08ad6",
    "notes/theorem_ledger.md": "30707fc8c63ad50df96c2e49eac842e4b7da7d2ec98864c1544063aaa7305453",
    "paper/main.pdf": "11fded4628255bb675e8b17a9e3ca8c18961e2555948a00f621febb603ae2cfd",
    "paper/main.tex": "6056fecb17aad48ce203328283f11db469052d03c7cea51fc74a606235b8162a",
    "paper/paper.pdf": "11fded4628255bb675e8b17a9e3ca8c18961e2555948a00f621febb603ae2cfd",
    "paper/references.bib": "ccc44072e999e8f7e467b99ff58ff7351837af1bbec7bd5b1234a7f41780ba14",
    "results/tpc270_certificate.json": "3cdb6ca037c0a93c85ad2de225483e486db8da33893ec54ba9e274b0a5443e55",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest_bytes(data: bytes) -> str:
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def frozen(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + path], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "missing frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(expected != "PLACEHOLDER", "source hash placeholder: " + path)
        need(digest_bytes(frozen(path)) == expected,
             "frozen source hash: " + path)


def check_project() -> None:
    actual = {
        str(path.relative_to(PROJECT))
        for path in PROJECT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(digest(PROJECT / relative) == expected, "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH", "bridge hash placeholder")
    need(digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC270_MAXIMUM_CLAIM = " + STATUS,
        "TPC270_ROUTE_ADVANCE = YES_SCOPED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT",
        "TPC270_ENDPOINT_NORMALIZATION = PROVED_EXACT_FINITE_IDENTITY",
        "TPC270_CROSS_SCALE_VARIATION = NUMERICALLY_CERTIFIED_FINITE",
        "TPC270_PROFILE_CONTROL = NUMERICALLY_CERTIFIED_FINITE",
        "TPC270_FINITE_STABILITY = REFUTED_SCOPED",
        "TPC270_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC",
        "TPC270_SOURCE_LEVEL_PHASE = OPEN_ASYMPTOTIC",
        "TPC270_FIXED_POWER_CREDIT = 0",
        "TPC270_ARITHMETIC_ADVANCE = NO",
        "TPC270_L2 = NONE",
        "TPC270_FULL_GATE_B = OPEN",
        "TPC270_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC270_TWIN_PRIME_RESULT = NONE",
        "TPC270_STATUS = " + STATUS,
        "TPC270_ROUND2_CLUE = TEST_SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_NORMALIZATION",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    for phrase in ("DROP_RISE_RISE_DROP", "23.9597604587",
                   "0.231753859227", "1/2 < Xi"):
        need(phrase in text, "bridge result: " + phrase)


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command, cwd=ROOT, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == "",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    pairs = (
        (child(PRODUCER, "TPC270_CERTIFICATE=PASS"),
         child(PRODUCER, "TPC270_CERTIFICATE=PASS", True)),
        (child(INDEPENDENT, "TPC270_INDEPENDENT_CHECK=PASS"),
         child(INDEPENDENT, "TPC270_INDEPENDENT_CHECK=PASS", True)),
        (child(STRESS, "TPC270_NORMALIZATION_STRESS=PASS"),
         child(STRESS, "TPC270_NORMALIZATION_STRESS=PASS", True)),
    )
    for normal, optimized in pairs:
        need(normal == optimized, "normal/optimized mismatch")


def interval(values: object) -> tuple[float, float]:
    need(isinstance(values, list) and len(values) == 2,
         "bad interval")
    lo, hi = float(values[0]), float(values[1])
    need(0 < lo <= hi, "nonpositive interval")
    return lo, hi


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (
        json.dumps(parsed, ensure_ascii=True, sort_keys=True,
                   separators=(",", ":")) + "\n"
    ).encode("ascii")
    need(raw == canonical, "certificate is not canonical")
    need(parsed.get("certificate_version") == 1 and
         parsed.get("claim_status") == STATUS, "certificate header")
    payload = parsed.get("payload", {})
    need(payload.get("schema") ==
         "TPC270_CROSS_SCALE_RADIUS_NORMALIZATION_CERTIFICATE_V1",
         "certificate schema")
    payload_raw = (
        json.dumps(payload, ensure_ascii=True, sort_keys=True,
                   separators=(",", ":")) + "\n"
    ).encode("ascii")
    need(hashlib.sha256(payload_raw).hexdigest() == parsed.get("payload_sha256"),
         "payload digest")
    parameters = payload.get("parameters", {})
    need(parameters.get("registered_scales") == [64, 96, 128, 192, 256, 384],
         "registered scales")
    need(parameters.get("cutoff_rule") ==
         "z_N=floor(log(N)) on registered rows", "cutoff rule")
    need(parameters.get("normalization") ==
         "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6", "normalization")
    theorem = payload.get("finite_theorem", {})
    need((theorem.get("base_rows"), theorem.get("profile_control_rows"),
          theorem.get("dyadic_ratio_rows"), theorem.get("adjacent_ratio_rows"),
          theorem.get("profile_ratio_rows")) == (6, 3, 4, 5, 3),
         "theorem counts")
    need(theorem.get("dyadic_pattern") == "DROP_RISE_RISE_DROP",
         "dyadic pattern")
    need(theorem.get("normalized_radius_variation") ==
         "NUMERICALLY_CERTIFIED_FINITE", "variation status")
    need(len(payload.get("base_rows", [])) == 6 and
         len(payload.get("profile_rows", [])) == 3, "row counts")
    for row in payload["base_rows"] + payload["profile_rows"]:
        interval(row.get("radius_squared_interval"))
        interval(row.get("endpoint_normalized_sixth_interval"))
        need(row.get("exact_projection_identity") is True and
             row.get("positive_radius_certified") is True,
             "row certificate")
        need(row.get("normalization_identity") ==
             "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6", "row identity")
    expected_dyadic = (
        "DROP_BELOW_ONE_QUARTER", "RISE_ABOVE_SIXTEEN",
        "RISE_ABOVE_SEVEN", "DROP_BETWEEN_THREE_QUARTERS_AND_ONE",
    )
    dyadic = payload.get("dyadic_ratios", [])
    need(len(dyadic) == 4 and
         tuple(row.get("classification") for row in dyadic) == expected_dyadic,
         "dyadic classifications")
    for row in dyadic:
        interval(row.get("ratio_interval"))
        need(row.get("positive_denominator_certified") is True,
             "dyadic denominator")
    adjacent = payload.get("adjacent_ratios", [])
    need(len(adjacent) == 5, "adjacent count")
    for row in adjacent:
        interval(row.get("ratio_interval"))
    profiles = payload.get("profile_ratios", [])
    need(len(profiles) == 3, "profile count")
    for row in profiles:
        lo, hi = interval(row.get("ratio_interval"))
        need(0.5 < lo <= hi < 0.75, "profile band")
    firewall = payload.get("firewall", {})
    expected_firewall = {
        "TPC270_ENDPOINT_NORMALIZATION": "PROVED_EXACT_FINITE_IDENTITY",
        "TPC270_CROSS_SCALE_VARIATION": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC270_PROFILE_CONTROL": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC270_SOURCE_LEVEL_RADIUS": "OPEN_ASYMPTOTIC",
        "TPC270_SOURCE_LEVEL_PHASE": "OPEN_ASYMPTOTIC",
        "TPC270_FIXED_POWER_CREDIT": 0,
        "TPC270_ARITHMETIC_ADVANCE": "NO",
        "TPC270_L2": "NONE",
        "TPC270_FULL_GATE_B": "OPEN",
        "TPC270_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        "TPC270_TWIN_PRIME_RESULT": "NONE",
        "TPC270_STATUS": STATUS,
    }
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall: " + key)
    need(payload.get("round2_clue") ==
         "TEST_SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_NORMALIZATION",
         "round-two clue")


def check_pdf() -> None:
    text = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Cross-Scale", "Liang Wang", "endpoint-normalized",
                   "DROP", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(
        ["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(info.returncode == 0 and b"Pages:           4" in info.stdout,
         "PDF pages")
    fonts = subprocess.run(
        ["pdffonts", str(PDF)], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    rows = [row for row in fonts.stdout.decode("ascii", errors="replace").splitlines()[2:]
            if row.strip()]
    need(fonts.returncode == 0 and fonts.stderr == b"" and rows and
         all(row.split()[-5:-2] == ["yes", "yes", "yes"] for row in rows),
         "PDF fonts")
    if LOG.is_file():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        need("Warning:" not in log and "Overfull" not in log and
             "Underfull" not in log and "undefined references" not in log and
             "Citation `" not in log, "LaTeX log")


def check_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "assert syntax: " + path.name)
    need("tpc270_cross_scale_radius_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")
    need("tpc270_cross_scale_radius_certificate" not in
         STRESS.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError, ValueError) as exc:
        print("TPC270_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC270_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("cross_scale_radius_normalization=NUMERICALLY_CERTIFIED_FINITE")
    print("dyadic_pattern=DROP_RISE_RISE_DROP")
    print("source_level_radius=OPEN_ASYMPTOTIC")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
