#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-271 phase--radius audit."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-271-phase-radius-decoupling"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_phase_radius_decoupling.md"
PRODUCER = PROJECT / "code/tpc271_phase_radius_decoupling_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc271_independent_checker.py"
STRESS = PROJECT / "experiments/tpc271_phase_radius_stress.py"
CERTIFICATE = PROJECT / "results/tpc271_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "90689dfa7fead6747f184687e6c2148e7ef63810"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT"
BRIDGE_SHA256 = "fa0546e9dc8e817e59580f074b0996ffcea2c5a61ef823347f6a126a23408968"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "a8e227bba61413c7b5249f6a11a55b7115ffd7a8b657fcab2d6cb4c65e46a201",
    "papers/tpc-270-cross-scale-radius-normalization/README.md": "349fc7fecc193f03a0eac98a5ca0ad0044fed5b2c59f60cfd751c990f90f0138",
    "papers/tpc-270-cross-scale-radius-normalization/PROOF_PACKAGE.md": "496bb49033007cab6aba66f4076112ad739d3ccc52627574e93c61dc85d8cd1d",
    "papers/tpc-270-cross-scale-radius-normalization/notes/theorem_ledger.md": "30707fc8c63ad50df96c2e49eac842e4b7da7d2ec98864c1544063aaa7305453",
    "papers/tpc-270-cross-scale-radius-normalization/notes/route_evaluation.md": "44cc3d77fac5ed08e30f21f317ca9b8952a81b31640ca9371237622ff1d08ad6",
    "research/tpc-big-road/bridge_b_cross_scale_radius_normalization.md": "2c58d4d040d187fff35f21fd02354bd4d5a334956daa9cedd91d86a6e4e1a0e1",
    "research/tpc-big-road/tpc_bridge_b_cross_scale_radius_normalization_checker.py": "67215161d67d11cb8c837fe0815e984d5fa48bd0611cc5e4b3a355ac93b2e32f",
}

PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "a1fa53c2b428be161d0978dd695363a44d321f3831d2a92647ff0178c94ebdc2",
    "PAPER_PLAN.md": "d233cb52db2739897eede89bc1fc1ec90d94193cb8f22970d2e89aee5b49d083",
    "PROOF_PACKAGE.md": "af7b96dd282675010928933ed58a4e079e8a2343f3a16db8059e20425ae7b8c3",
    "README.md": "daa4883384539b2b407c71826fe4559cb8cf2e89c03792d9be2ea0432d58d0bd",
    "code/tpc271_phase_radius_decoupling_certificate.py": "60660b56fd17d9c956612081f07e990b661a6411bb6adb08eb6a3995d369b7d9",
    "experiments/tpc271_independent_checker.py": "bc4f60802fb55e3981b378348e26484db74b8aecedae48e1ee384ca307a7ff4e",
    "experiments/tpc271_phase_radius_stress.py": "a581fe10be788b3d7f6cab1e1ed0729f15db96873b5784074d118ce80e0618f0",
    "notes/citation_verification.md": "112721230f85de7416b0ef3a5c0be462372f6f2e8461291b129c7c034b844c85",
    "notes/claim_firewall.md": "350a07c2a521f4c501f0a5caeef72c40473d2bbc4c96ec6b0ac54a178a9c92c5",
    "notes/computational_protocol.md": "9c62d8709cda30f206b6cfcfa1563e086943a1a5ba7a3693130f7cc173707dc2",
    "notes/route_evaluation.md": "5349084c51e9b34aa3a8689e2d40314e1fab8c5424c082ef443cd439a9e9d894",
    "notes/theorem_ledger.md": "5258f15d442a286605018cd450e85685aa80deb02c39b848a54608ef03497e53",
    "paper/main.pdf": "788b225203604c42fb8996d8e8aff47c1c9db91bd39d69c243838185c52c4b9f",
    "paper/main.tex": "7bfe4df4bb1975e48638164628ff4fd86cad52d83734e110095a21ad40cbf417",
    "paper/paper.pdf": "788b225203604c42fb8996d8e8aff47c1c9db91bd39d69c243838185c52c4b9f",
    "paper/references.bib": "61cba97e1612aa1a55875883d37c91f6f267a45427bd05c843a230cbec6eb83b",
    "results/tpc271_certificate.json": "fa981eeec9f0f618081af0fdc86fd3a1f29cf3d221916b3e3036a659ef676100",
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
        "TPC271_MAXIMUM_CLAIM = " + STATUS,
        "TPC271_ROUTE_ADVANCE = YES_SCOPED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT",
        "TPC271_LANE_FACTORIZATION = PROVED_EXACT_FINITE",
        "TPC271_PHASE_SIGN_CENSUS = NUMERICALLY_CERTIFIED_FINITE",
        "TPC271_PHASE_RADIUS_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE",
        "TPC271_SOURCE_LANE_PROFILE_INVARIANCE = PROVED_EXACT_FINITE",
        "TPC271_OUTPUT_LANE_SPIKE = NUMERICALLY_CERTIFIED_FINITE",
        "TPC271_SOURCE_LEVEL_SIGNED_PHASE = OPEN_ASYMPTOTIC",
        "TPC271_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC",
        "TPC271_FIXED_POWER_CREDIT = 0",
        "TPC271_ARITHMETIC_ADVANCE = NO",
        "TPC271_L2 = NONE",
        "TPC271_FULL_GATE_B = OPEN",
        "TPC271_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC271_TWIN_PRIME_RESULT = NONE",
        "TPC271_STATUS = " + STATUS,
        "TPC271_ROUND2_CLUE = TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    for phrase in ("Xi=Xi_W*Xi_G", "Xi/Xi_C=|kappa|^(-6)",
                   "96->192", "Xi_G > 230", "ALL_NEGATIVE_REAL_AXIS"):
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
        (child(PRODUCER, "TPC271_CERTIFICATE=PASS"),
         child(PRODUCER, "TPC271_CERTIFICATE=PASS", True)),
        (child(INDEPENDENT, "TPC271_INDEPENDENT_CHECK=PASS"),
         child(INDEPENDENT, "TPC271_INDEPENDENT_CHECK=PASS", True)),
        (child(STRESS, "TPC271_PHASE_RADIUS_STRESS=PASS"),
         child(STRESS, "TPC271_PHASE_RADIUS_STRESS=PASS", True)),
    )
    for normal, optimized in pairs:
        need(normal == optimized, "normal/optimized mismatch")


def bounds(values: object) -> tuple[Fraction, Fraction]:
    need(isinstance(values, list) and len(values) == 2, "interval shape")
    lo, hi = Fraction(str(values[0])), Fraction(str(values[1]))
    need(0 < lo <= hi, "positive interval")
    return lo, hi


def signed_bounds(values: object) -> tuple[Fraction, Fraction]:
    need(isinstance(values, list) and len(values) == 2, "interval shape")
    lo, hi = Fraction(str(values[0])), Fraction(str(values[1]))
    need(lo <= hi, "ordered interval")
    return lo, hi


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "certificate is not canonical")
    need(parsed.get("certificate_version") == 1 and
         parsed.get("claim_status") == STATUS, "certificate header")
    payload = parsed.get("payload", {})
    need(payload.get("schema") ==
         "TPC271_PHASE_RADIUS_DECOUPLING_CERTIFICATE_V1", "certificate schema")
    payload_raw = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                               separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(payload_raw).hexdigest() == parsed.get("payload_sha256"),
         "payload digest")
    parameters = payload.get("parameters", {})
    need(parameters.get("registered_scales") == [64, 96, 128, 192, 256, 384],
         "registered scales")
    need(parameters.get("endpoint_normalization") ==
         "Xi=(R_squared)^3/N^10" and
         parameters.get("source_lane_normalization") == "Xi_W=W_perp^3/N^5" and
         parameters.get("output_lane_normalization") == "Xi_G=G_perp^3/N^5" and
         parameters.get("signed_scalar_normalization") == "Xi_C=|C_perp|^6/N^10",
         "lane normalization")
    theorem = payload.get("finite_theorem", {})
    need((theorem.get("base_rows"), theorem.get("profile_control_rows"),
          theorem.get("dyadic_lane_rows"), theorem.get("profile_lane_rows"),
          theorem.get("phase_rows")) == (6, 3, 4, 3, 9), "theorem counts")
    need(theorem.get("dyadic_radius_pattern") == "DROP_RISE_RISE_DROP" and
         theorem.get("phase_sign_pattern") == "ALL_NEGATIVE_REAL_AXIS" and
         theorem.get("lane_factorization") == "PROVED_EXACT_FINITE",
         "theorem labels")
    rows = payload.get("base_rows", []) + payload.get("profile_rows", [])
    need(len(rows) == 9, "row count")
    for row in rows:
        signed_bounds(row.get("residual_scalar_interval"))
        bounds(row.get("residual_w_norm_interval"))
        bounds(row.get("residual_g_norm_interval"))
        bounds(row.get("radius_squared_interval"))
        bounds(row.get("rho_squared_interval"))
        bounds(row.get("endpoint_normalized_sixth_interval"))
        bounds(row.get("source_lane_normalized_interval"))
        bounds(row.get("output_lane_normalized_interval"))
        bounds(row.get("signed_scalar_normalized_interval"))
        bounds(row.get("phase_amplification_interval"))
        need(row.get("phase") == "NEGATIVE_REAL_AXIS" and
             signed_bounds(row["residual_scalar_interval"])[1] < 0 and
             row.get("positive_residual_lanes_certified") is True and
             row.get("exact_projection_identity") is True and
             row.get("lane_product_encloses_radius") is True,
             "phase or row certificate")
    dyadic = payload.get("dyadic_lane_ratios", [])
    need(len(dyadic) == 4, "dyadic count")
    expected = (
        ("SOURCE_DROP_BELOW_ONE_HALF", "OUTPUT_DROP_BELOW_THREE_QUARTERS",
         "RADIUS_DROP_BELOW_ONE_QUARTER"),
        ("SOURCE_DROP_BELOW_ONE_EIGHTH", "OUTPUT_RISE_ABOVE_230",
         "RADIUS_RISE_ABOVE_23"),
        ("SOURCE_DROP_BELOW_ONE_HALF", "OUTPUT_RISE_ABOVE_15",
         "RADIUS_RISE_ABOVE_SEVEN"),
        ("SOURCE_RISE_ABOVE_ONE", "OUTPUT_DROP_BELOW_THREE_QUARTERS",
         "RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE"),
    )
    for item, classes in zip(dyadic, expected):
        need((item.get("source_classification"), item.get("output_classification"),
              item.get("radius_classification")) == classes,
             "dyadic classes")
        bounds(item.get("source_lane_ratio_interval"))
        bounds(item.get("output_lane_ratio_interval"))
        bounds(item.get("radius_ratio_interval"))
        bounds(item.get("signed_scalar_normalized_ratio_interval"))
        need(item.get("phase_sign_low") == item.get("phase_sign_high") ==
             "NEGATIVE_REAL_AXIS" and item.get("phase_sign_preserved") is True and
             item.get("exact_lane_product_identity") is True,
             "dyadic phase metadata")
    profiles = payload.get("profile_lane_ratios", [])
    need(len(profiles) == 3, "profile count")
    for item in profiles:
        need(item.get("source_lane_is_profile_invariant") is True and
             item.get("output_lane_classification") ==
             "OUTPUT_PROFILE_DROP_BELOW_NINE_TENTHS" and
             item.get("radius_classification") ==
             "RADIUS_PROFILE_RATIO_BETWEEN_ONE_HALF_AND_THREE_QUARTERS" and
             item.get("phase_sign_preserved") is True,
             "profile control")
        bounds(item.get("source_lane_ratio_interval"))
        bounds(item.get("output_lane_ratio_interval"))
        bounds(item.get("radius_ratio_interval"))
    firewall = payload.get("firewall", {})
    expected_firewall = {
        "TPC271_LANE_FACTORIZATION": "PROVED_EXACT_FINITE",
        "TPC271_PHASE_SIGN_CENSUS": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC271_PHASE_RADIUS_DECOUPLING": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC271_SOURCE_LANE_PROFILE_INVARIANCE": "PROVED_EXACT_FINITE",
        "TPC271_OUTPUT_LANE_SPIKE": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC271_SOURCE_LEVEL_SIGNED_PHASE": "OPEN_ASYMPTOTIC",
        "TPC271_SOURCE_LEVEL_RADIUS": "OPEN_ASYMPTOTIC",
        "TPC271_FIXED_POWER_CREDIT": 0,
        "TPC271_ARITHMETIC_ADVANCE": "NO",
        "TPC271_L2": "NONE",
        "TPC271_FULL_GATE_B": "OPEN",
        "TPC271_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        "TPC271_TWIN_PRIME_RESULT": "NONE",
        "TPC271_STATUS": STATUS,
    }
    for key, value in expected_firewall.items():
        need(firewall.get(key) == value, "firewall: " + key)
    need(payload.get("round2_clue") ==
         "TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL",
         "round-two clue")


def check_pdf() -> None:
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Phase", "Radius", "Liang Wang", "DROP", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(info.returncode == 0 and b"Pages:           3" in info.stdout,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    rows = [row for row in fonts.stdout.decode("ascii", errors="replace")
            .splitlines()[2:] if row.strip()]
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
    for path in (INDEPENDENT, STRESS):
        need("tpc271_phase_radius_decoupling_certificate" not in
             path.read_text(encoding="utf-8"), "producer import: " + path.name)


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
        print("TPC271_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC271_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("phase_sign=ALL_NEGATIVE_REAL_AXIS")
    print("output_lane_spike=96->192")
    print("source_level_phase=OPEN_ASYMPTOTIC")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
