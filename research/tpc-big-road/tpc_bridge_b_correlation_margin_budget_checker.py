#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-272 budget compiler."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-272-correlation-margin-budget-compiler"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_correlation_margin_budget.md"
PRODUCER = PROJECT / "code/tpc272_correlation_margin_budget_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc272_independent_checker.py"
STRESS = PROJECT / "experiments/tpc272_margin_stress.py"
CERTIFICATE = PROJECT / "results/tpc272_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "dad299b0601f81238396862b9d587a3b2a4193c4"
STATUS = "PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER"
BRIDGE_SHA256 = "d792fff25603967021bc2bee9c83c66e89cb6eb4e2952947e249c7f0837af8a3"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "d9748b8ab275d8297558e0ba6025217ef13cc94519c1cdfe41bb99af0a481846",
    "papers/tpc-271-phase-radius-decoupling/README.md": "daa4883384539b2b407c71826fe4559cb8cf2e89c03792d9be2ea0432d58d0bd",
    "papers/tpc-271-phase-radius-decoupling/PROOF_PACKAGE.md": "af7b96dd282675010928933ed58a4e079e8a2343f3a16db8059e20425ae7b8c3",
    "papers/tpc-271-phase-radius-decoupling/notes/theorem_ledger.md": "5258f15d442a286605018cd450e85685aa80deb02c39b848a54608ef03497e53",
    "papers/tpc-271-phase-radius-decoupling/notes/route_evaluation.md": "5349084c51e9b34aa3a8689e2d40314e1fab8c5424c082ef443cd439a9e9d894",
    "papers/tpc-271-phase-radius-decoupling/results/tpc271_certificate.json": "fa981eeec9f0f618081af0fdc86fd3a1f29cf3d221916b3e3036a659ef676100",
    "research/tpc-big-road/bridge_b_phase_radius_decoupling.md": "fa0546e9dc8e817e59580f074b0996ffcea2c5a61ef823347f6a126a23408968",
    "research/tpc-big-road/tpc_bridge_b_phase_radius_decoupling_checker.py": "69cc657400ea4388ec7b09ec0ee0b1a4026f760fe194c0632d160c0ccefe3021",
}

PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "252c0ac1de0eae10140ea1b35d3f5daa4bd71c7f07a2311fe9bc42889a4c742b",
    "PAPER_PLAN.md": "e74b6d9442d2b230be0b6e60b0416331e2dc9971b6849a4aa4d7bd9b03c9ecc9",
    "PROOF_PACKAGE.md": "90f729e3132d0a9a810191454ac026c40ca62827dbeb2ca61bd777074f96d398",
    "README.md": "3e4b4b1efc2933f5b72bdd2b8c98855660767b30a96cff04fe833c98b8fa0c4d",
    "code/tpc272_correlation_margin_budget_certificate.py": "17f82b77c08002be733a698ed12a8c8bf036ef4042ca7646482509c7e11cc7aa",
    "experiments/tpc272_independent_checker.py": "652a4053633b0e6bce83cf6a5580311daedd9c84bae85ed169aa7dd58335e8e8",
    "experiments/tpc272_margin_stress.py": "774452df5468101cbd62389ec6f410421d75b630f8a29d4d0d356c6bc4f8c787",
    "notes/citation_verification.md": "2d365cbeb8556a57d0280241655c7514495393d94363db4c376de9203d66dc78",
    "notes/claim_firewall.md": "e7de44974e45d0281cc420debb56b99b645ab89058c55de3945a9d4323f5df88",
    "notes/computational_protocol.md": "c5d03426ad6d4466cb460ba401f0e7004e8d36d34bcf141b3838a45e52e180ea",
    "notes/route_evaluation.md": "11269363de1f81c7473c2eeb3c6f35895a8173550242f6d838a4871b512cb8ac",
    "notes/theorem_ledger.md": "7e1cba1a0e3975796f0aa8df40a50593d3388158e69ff267741018cec6d4e24a",
    "paper/main.pdf": "7c4c2179bf8c045593a29fbda7a4d2e4c7b6c9f59baee27dc0e1ce60396e93cb",
    "paper/main.tex": "1f803d9a145563c07e068fd15d5731a946d2419b564e45ead770d6a0f4604c71",
    "paper/paper.pdf": "7c4c2179bf8c045593a29fbda7a4d2e4c7b6c9f59baee27dc0e1ce60396e93cb",
    "paper/references.bib": "3aead739640ffe01c4224efafcac2cdff430a941c5722a1e0c4ce46e2c14549a",
    "results/tpc272_certificate.json": "f12b8f5a666593df4d14c5a36b261db1c8f323596d033013479fcce43540d4cb",
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
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "missing frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest_bytes(frozen(path)) == expected, "frozen source hash: " + path)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER" and digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH" and digest(BRIDGE) == BRIDGE_SHA256,
         "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC272_MAXIMUM_CLAIM = " + STATUS,
        "TPC272_ROUTE_ADVANCE = YES_SCOPED_CONDITIONAL_MARGIN_BUDGET_AND_FINITE_AUDIT",
        "TPC272_CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL",
        "TPC272_MARGIN_IDENTITY = PROVED_EXACT_FINITE",
        "TPC272_SHARP_CONVERSE = PROVED_EXACT",
        "TPC272_FINITE_MARGIN_AUDIT = NUMERICALLY_CERTIFIED",
        "TPC272_SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC",
        "TPC272_FIXED_POWER_CREDIT = 0",
        "TPC272_ARITHMETIC_ADVANCE = NO",
        "TPC272_L2 = NONE",
        "TPC272_FULL_GATE_B = OPEN",
        "TPC272_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC272_TWIN_PRIME_RESULT = NONE",
        "TPC272_STATUS = " + STATUS,
        "TPC272_ROUND2_CLUE = AUDIT_SOURCE_LEVEL_MARGIN_LOWER_BOUND_BEFORE_ANY_PHASE_PROMOTION",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    for phrase in ("m^6 = Xi_C/Xi", "sigma-eta>1/400", "96->192",
                   "(1/32)^6", "negative phase"):
        need(phrase in text, "bridge result: " + phrase)


def child(path: Path, marker: str, optimized: bool, args: list[str]) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), *args])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    triples = (
        (PRODUCER, "TPC272_CERTIFICATE=PASS", ["--check"]),
        (INDEPENDENT, "TPC272_INDEPENDENT_CHECK=PASS", []),
        (STRESS, "TPC272_MARGIN_STRESS=PASS", []),
    )
    for path, marker, args in triples:
        normal = child(path, marker, False, args)
        optimized = child(path, marker, True, args)
        need(normal == optimized, "normal/optimized mismatch: " + path.name)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = Fraction(str(value[0])), Fraction(str(value[1]))
    need(0 < lo <= hi, "positive interval")
    return lo, hi


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    canonical = (json.dumps(data, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "certificate canonicality")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "certificate header")
    payload = data["payload"]
    payload_raw = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                               separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(payload_raw).hexdigest() == data["payload_sha256"],
         "payload digest")
    need(payload["schema"] == "TPC272_CORRELATION_MARGIN_BUDGET_CERTIFICATE_V1",
         "schema")
    need(payload["finite_theorem"] == {
        "base_rows": 6, "collapse_pair": "96->192", "dyadic_rows": 4,
        "finite_margin_audit": "NUMERICALLY_CERTIFIED",
        "margin_identity": "PROVED_EXACT_FINITE", "phase_pattern": "ALL_NEGATIVE_REAL_AXIS",
        "profile_rows": 3, "rows": 9, "sharp_two_dimensional_converse": "PROVED_EXACT",
    }, "theorem ledger")
    rows = payload["rows"]
    need(len(rows) == 9, "row count")
    for row in rows:
        interval(row["margin_sixth_interval"])
        interval(row["amplification_interval"])
        need(row["phase"] == "NEGATIVE_REAL_AXIS" and row["phase_sign_locked"] is True,
             "row phase")
    dyadic = payload["dyadic_margin_ratios"]
    need(len(dyadic) == 4, "dyadic count")
    collapse = dyadic[1]
    need(collapse["label"] == "96->192" and
         interval(collapse["margin_sixth_ratio_interval"])[1] < Fraction(1, 32**6) and
         collapse["phase_sign_preserved"] is True and
         collapse["margin_ratio_classification"] ==
         "MARGIN_COLLAPSE_BELOW_ONE_THIRTY_SECOND", "collapse semantics")
    rise = dyadic[3]
    need(interval(rise["margin_sixth_ratio_interval"])[0] > 4**6 and
         rise["margin_ratio_classification"] == "MARGIN_RISE_ABOVE_FOUR",
         "rise semantics")
    firewall = payload["firewall"]
    need(firewall["TPC272_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC272_SOURCE_LEVEL_MARGIN"] == "OPEN_ASYMPTOTIC" and
         firewall["TPC272_FULL_GATE_B"] == "OPEN" and
         firewall["TPC272_TWIN_PRIME_RESULT"] == "NONE", "firewall")


def check_pdf() -> None:
    need(PDF.stat().st_size > 10000, "PDF too small")
    log = LOG.read_text(encoding="utf-8")
    for bad in ("Warning", "Undefined", "Overfull", "Underfull", "Fatal", "Error"):
        need(bad not in log, "LaTeX log contains " + bad)


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, KeyError, TypeError, ValueError) as error:
        print("TPC272_BRIDGE_CHECK=FAIL " + str(error))
        return 1
    print("TPC272_BRIDGE_CHECK=PASS rows=9 dyadic_rows=4 "
          "conditional_gate=SIGMA_MINUS_ETA_GREATER_THAN_1_OVER_400 "
          "collapse_pair=96->192 phase_preserved=TRUE fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
