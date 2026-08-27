#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-276 signed-gain budget paper."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-276-signed-gain-endpoint-budget"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_signed_gain_endpoint_budget.md"
PRODUCER = PROJECT / "code/tpc276_signed_gain_endpoint_budget_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc276_independent_checker.py"
STRESS = PROJECT / "experiments/tpc276_budget_stress.py"
CERTIFICATE = PROJECT / "results/tpc276_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "da6b34746a8a56466c6092d37c432ccdf518d25d"
STATUS = "PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER"
BRIDGE_SHA256 = "9957833a275a4a90f4660f71cbee040315ba3b175f07da37e0d0a84f5ff6564d"

# TPC-275 is the immediately preceding released parent.  The source locks are
# read from its release commit, not from a mutable worktree, so a later edit to
# the current handoff cannot silently change the parent of this paper.
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "bbb5e8db69e8a1e87ff27f895f9ee8d8934cbf33d65090c16408495a16803f95",
    "papers/tpc-275-signed-four-packet-reassembly/README.md": "2c213f10cb9a8155dd34d35b2b4841339b66fbdaa036a49bd226827acbb86e51",
    "papers/tpc-275-signed-four-packet-reassembly/PROOF_PACKAGE.md": "c1776a60481d45917a744b7aeb549e0990f7e44a7d22fd813717e1be01bac2f2",
    "papers/tpc-275-signed-four-packet-reassembly/notes/theorem_ledger.md": "5a962839aaf67f683b69325e0cb4e0d3bacfec0e77d8c3885591ed88dac676a3",
    "papers/tpc-275-signed-four-packet-reassembly/notes/route_evaluation.md": "55a1f00677a042e68acd3034f11955973e755d8c19d59b64e95c67f3698cc363",
    "papers/tpc-275-signed-four-packet-reassembly/results/tpc275_certificate.json": "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd",
    "research/tpc-big-road/bridge_b_signed_four_packet_reassembly.md": "7056bd897054d5876d6e16121f0c02ceced0395d992750303710398f732d91a1",
    "research/tpc-big-road/tpc_bridge_b_signed_four_packet_reassembly_checker.py": "8fbd3b2e5a6b5ef36b9a84ce2b9ac821e70e34281e9c681893a906a60098b130",
    "papers/tpc-274-projected-output-frobenius-envelope/results/tpc274_certificate.json": "01f9c37438b846c009fbb1650b1da57e87b875519510662178ad26c135bf517d",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py": "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json": "19b629425c4e64ec3e9638bb8e9f5baee304a7340d764fb32dfa2c31d49c907d",
}

# Filled only after every TPC-276 project artifact is final.
PROJECT_HASHES = {
    ".gitignore": "139dac3fcaa03b01ebff688c84d62e6b7ceb154384980f414976d1242aaf2612",
    "DERIVATION_PACKAGE.md": "a123ddc166f1777d480aa9cbd8be5a40d6e846476e6dabed82920225bda33ecd",
    "PAPER_PLAN.md": "b5d348b4977ac0930ad377014273ca102b4a6b33d2aabc5e6299494832f3fa3d",
    "PROOF_PACKAGE.md": "2324ec556c97b1c36b499b80d904fae8c2facff77f79a78e337211d0c943b8b6",
    "README.md": "a6845a94ca919f1401f95c641278f4033725c48d32a5e8b8a6362fd8c61bdebe",
    "code/tpc276_signed_gain_endpoint_budget_certificate.py": "aa5e5200309ffa36b0445de10a4d3274ddbada4b6202bb8067e63c37f6c7029e",
    "experiments/tpc276_independent_checker.py": "e75dc6e1ab455c88c37bf4d2fa72a8241737b3c0596f2d34d1ccd9a622d040fc",
    "experiments/tpc276_budget_stress.py": "131a3076813ee7c35c8745f0af37d8f9713739b53e391d4a7f7b73d325c0b6f8",
    "notes/citation_verification.md": "4216d78651552c0e567232c5dff4b7e0f131df1a9d09c789d636c6adbf4a2108",
    "notes/claim_firewall.md": "56fceab61e238de83b5e9fa55c8e5682489d1352c19c2e9f39de3d10e7a4e4a3",
    "notes/computational_protocol.md": "0df278f77805aa442e777848ac44973bb4cbbb76fa005ce3055912d18ca3167f",
    "notes/route_evaluation.md": "ebd00354943be3c659a984414d125febbc1844c2accefd71570e354150fcdc5c",
    "notes/theorem_ledger.md": "46a86d7fa1e08d7016a1198a30e49c3c3d7311ea8d268946bbc8e527d8acc6a1",
    "paper/main.pdf": "f6ff0ba6ae01d494aed1a08b4739e4bc6e46f1b5976d3f5177785f24c359e340",
    "paper/main.tex": "a200c968d1891682caf7c7b069177d4f7a40b634885e0d6234c3a07de68dc7df",
    "paper/paper.pdf": "f6ff0ba6ae01d494aed1a08b4739e4bc6e46f1b5976d3f5177785f24c359e340",
    "paper/references.bib": "af065680bec537b075a35ac149228d806adf926ab254ac3919362acc8bf310c4",
    "results/tpc276_certificate.json": "cf74fdb9fadc156c5b9043edf3c5463adf6c24260184ba94de99d24719713c0e",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}


class Failure(RuntimeError):
    """A release invariant failed."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest_bytes(data: bytes) -> str:
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "missing frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest_bytes(frozen(path)) == expected,
             "frozen source hash: " + path)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object, positive: bool = False) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi and (not positive or lo > 0), "interval order/sign")
    return lo, hi


def interval_text(value: tuple[Fraction, Fraction]) -> list[str]:
    return [f"{value[0].numerator}/{value[0].denominator}",
            f"{value[1].numerator}/{value[1].denominator}"]


def classify(value: tuple[Fraction, Fraction], threshold: Fraction) -> str:
    if value[0] > threshold:
        return "ABOVE_THRESHOLD"
    if value[1] < threshold:
        return "BELOW_THRESHOLD"
    return "CROSSES_THRESHOLD"


def load_parent() -> dict[str, Any]:
    parent_path = ROOT / "papers/tpc-275-signed-four-packet-reassembly/results/tpc275_certificate.json"
    raw = parent_path.read_bytes()
    parent_file_hash = "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
    parent_payload_hash = "6f72d561af7f6aec1626843cc0574afc74a1de5a10f57867b202a585a1cfc429"
    parent_schema = "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1"
    need(digest_bytes(raw) == parent_file_hash, "parent file provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT",
         "parent header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == parent_schema,
         "parent schema")
    need(data.get("payload_sha256") == parent_payload_hash and
         hashlib.sha256(canonical(payload)).hexdigest() == parent_payload_hash,
         "parent payload provenance")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent rows")
    return data


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER" and
             digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH" and
         digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC276_MAXIMUM_CLAIM = " + STATUS,
        "TPC276_ROUTE_ADVANCE = YES_SCOPED_SIGNED_GAIN_MARGIN_RECOVERY",
        "TPC276_SIGNED_GAIN_MARGIN_IDENTITY = PROVED_EXACT_FINITE",
        "TPC276_CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL_WITH_EFFECTIVE_LOSS_MAX_ZERO_ETA_D_MINUS_GAMMA_OVER_2",
        "TPC276_FINITE_SIGNED_MARGIN_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC276_SIGNED_QUARTER_CROSSING = NUMERICALLY_CERTIFIED_FINITE_THREE_ROWS",
        "TPC276_SIGNED_EIGHTH_CROSSING = NUMERICALLY_CERTIFIED_FINITE_FIVE_ROWS",
        "TPC276_GAIN_STRICTLY_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC276_FINITE_POWER_PROMOTION = REFUTED_SCOPED",
        "TPC276_FIXED_POWER_CREDIT = 0",
        "TPC276_SOURCE_LEVEL_SIGNED_GAIN = OPEN_ASYMPTOTIC",
        "TPC276_ARITHMETIC_ADVANCE = NO",
        "TPC276_L2 = NONE",
        "TPC276_FULL_GATE_B = OPEN",
        "TPC276_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC276_TWIN_PRIME_RESULT = NONE",
        "TPC276_STATUS = " + STATUS,
        "TPC276_ROUND2_CLUE = SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    flat = " ".join(text.split())
    for phrase in (
        "12 rows", "r>1", "m^2 = r m_D^2", "three rows lie above",
        "five lie above", "finite gain is not a fixed-power credit",
        "source-level theorem", "twin-prime proof", "propose.md",
    ):
        need(phrase in flat, "bridge result: " + phrase)


def child(path: Path, marker: str, optimized: bool,
          args: list[str]) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), *args])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    children = (
        (PRODUCER, "TPC276_CERTIFICATE=PASS", ["--check"]),
        (INDEPENDENT, "TPC276_INDEPENDENT_CHECK=PASS", []),
        (STRESS, "TPC276_BUDGET_STRESS=PASS", []),
    )
    for path, marker, args in children:
        normal = child(path, marker, False, args)
        optimized = child(path, marker, True, args)
        need(normal == optimized, "normal/optimized mismatch: " + path.name)


def check_certificate() -> None:
    parent = load_parent()
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() ==
         data["payload_sha256"] and
         payload.get("schema") ==
         "TPC276_SIGNED_GAIN_ENDPOINT_BUDGET_CERTIFICATE_V1",
         "certificate digest/schema")
    parent_file_hash = "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
    parent_payload_hash = "6f72d561af7f6aec1626843cc0574afc74a1de5a10f57867b202a585a1cfc429"
    parent_schema = "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1"
    need(payload["parameters"] == {
        "E0": "5/3",
        "E_star": "1997/1200",
        "conditional_gain_hypothesis": "D/G>=b*x^gamma",
        "conditional_margin_hypothesis": "m_D>=c*x^(-eta_D-epsilon)",
        "conditional_scalar_hypothesis": "|C|<=A*x^(E0-sigma+epsilon)",
        "diagonal_margin_threshold": "m_D^2=1/16",
        "eighth_margin_threshold": "m^2=1/64",
        "effective_margin_loss": "eta_eff=max(0,eta_D-gamma/2)",
        "signed_gain_definition": "r=D/G",
        "signed_margin_identity": "m^2=r*m_D^2",
        "signed_margin_threshold": "m^2=1/16",
        "strict_budget_condition": "sigma-eta_eff>1/400",
        "strict_endpoint_gap": "1/400",
        "parent_file_sha256": parent_file_hash,
        "parent_payload_sha256": parent_payload_hash,
        "parent_schema": parent_schema,
    }, "parameters")

    parent_rows = parent["payload"]["rows"]
    rows = payload["rows"]
    need(isinstance(rows, list) and len(rows) == 12, "row count")
    seen: set[tuple[int, int]] = set()
    quarter_count = 0
    eighth_count = 0
    crossing_count = 0
    for parent_row, output_row in zip(parent_rows, rows):
        need(isinstance(output_row, dict), "row type")
        key = (parent_row["scale"], parent_row["kernel_exponent"])
        need(key not in seen, "duplicate row")
        seen.add(key)
        need((output_row.get("scale"), output_row.get("kernel_exponent")) == key,
             "row key")
        gain = frac(parent_row["diagonal_to_signed_ratio"])
        diagonal = interval(parent_row["diagonal_margin_squared_interval"], True)
        signed = (gain * diagonal[0], gain * diagonal[1])
        actual = interval(parent_row["actual_margin_squared_interval"], True)
        need(gain > 1 and max(signed[0], actual[0]) <=
             min(signed[1], actual[1]), "signed transfer support")
        improvement = (signed[0] - diagonal[1], signed[1] - diagonal[0])
        need(output_row["diagonal_margin_squared_interval"] ==
             interval_text(diagonal) and
             output_row["signed_gain_factor"] ==
             f"{gain.numerator}/{gain.denominator}" and
             output_row["signed_margin_squared_interval"] ==
             interval_text(signed) and
             output_row["signed_margin_improvement_interval"] ==
             interval_text(improvement), "signed intervals")
        need(output_row["signed_gain_identity"] == "m^2=(D/G)m_D^2" and
             output_row["gain_classification"] == "STRICTLY_ABOVE_ONE" and
             output_row["diagonal_quarter_classification"] ==
             classify(diagonal, Fraction(1, 16)) and
             output_row["signed_quarter_classification"] ==
             classify(signed, Fraction(1, 16)) and
             output_row["signed_eighth_classification"] ==
             classify(signed, Fraction(1, 64)) and
             output_row["parent_actual_margin_reference"] ==
             interval_text(actual) and
             output_row["parent_reference_overlaps_signed_interval"] is True and
             output_row["finite_transfer_exact"] is True, "row metadata")
        need(output_row["diagonal_quarter_classification"] ==
             "BELOW_THRESHOLD", "diagonal threshold")
        quarter = output_row["signed_quarter_classification"]
        eighth = output_row["signed_eighth_classification"]
        quarter_count += quarter == "ABOVE_THRESHOLD"
        eighth_count += eighth == "ABOVE_THRESHOLD"
        crossing_count += quarter == "CROSSES_THRESHOLD" or \
            eighth == "CROSSES_THRESHOLD"
    need(seen == {(n, s) for n in (64, 96, 128, 192, 256, 384)
                  for s in (1, 2)}, "registered rows")

    need(payload["finite_theorem"] == {
        "claim": "signed gain recovers finite margin but finite gain is not power credit",
        "diagonal_below_quarter_rows": 12,
        "gain_strictly_above_one_rows": 12,
        "parent_rows": 12,
        "signed_above_eighth_rows": 5,
        "signed_above_quarter_rows": 3,
        "signed_gain_identity_rows": 12,
        "signed_quarter_crossing_rows": 0,
        "status": "NUMERICALLY_CERTIFIED_FINITE",
        "total_rows": 12,
    }, "finite theorem")
    need((quarter_count, eighth_count, crossing_count) == (3, 5, 0),
         "computed counts")
    need(payload["budget_compiler"] == {
        "diagonal_margin_loss": "eta_D",
        "effective_endpoint_saving": "sigma-eta_eff",
        "effective_margin_loss": "eta_eff=max(0,eta_D-gamma/2)",
        "endpoint_exponent": "E0-sigma+eta_eff+2*epsilon",
        "margin_gain_exponent": "gamma/2",
        "scalar_saving": "sigma",
        "signed_gain_exponent": "gamma",
        "status": "PROVED_CONDITIONAL",
        "strict_target_condition": "sigma-eta_eff>1/400",
    }, "budget compiler")
    need(payload["firewall"] == {
        "TPC276_ARITHMETIC_ADVANCE": "NO",
        "TPC276_CONDITIONAL_BUDGET_COMPILER": "PROVED_CONDITIONAL",
        "TPC276_FINITE_POWER_PROMOTION": "REFUTED_SCOPED",
        "TPC276_FINITE_SIGNED_MARGIN_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC276_FIXED_POWER_CREDIT": 0,
        "TPC276_FULL_GATE_B": "OPEN",
        "TPC276_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        "TPC276_GAIN_STRICTLY_ABOVE_ONE":
        "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC276_L2": "NONE",
        "TPC276_SIGNED_EIGHTH_CROSSING":
        "NUMERICALLY_CERTIFIED_FINITE_FIVE_ROWS",
        "TPC276_SIGNED_GAIN_MARGIN_IDENTITY": "PROVED_EXACT_FINITE",
        "TPC276_SIGNED_QUARTER_CROSSING":
        "NUMERICALLY_CERTIFIED_FINITE_THREE_ROWS",
        "TPC276_SOURCE_LEVEL_SIGNED_GAIN": "OPEN_ASYMPTOTIC",
        "TPC276_STATUS": STATUS,
        "TPC276_TWIN_PRIME_RESULT": "NONE",
    }, "claim firewall")
    need(payload["round2_clue"] ==
         "SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND", "round2 clue")


def check_pdf() -> None:
    need(PDF.stat().st_size > 10000, "PDF too small")
    extracted = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               check=False)
    need(extracted.returncode == 0 and extracted.stderr == b"",
         "PDF text extraction")
    decoded = extracted.stdout.decode("utf-8", errors="replace")
    for phrase in ("Signed-Gain Margin Recovery", "Liang Wang", "12 rows",
                   "PROVED_CONDITIONAL", "TPC276_FIXED_POWER_CREDIT",
                   "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    need(info.returncode == 0 and info.stderr == b"", "PDF info")
    info_text = info.stdout.decode("ascii", errors="replace")
    match = re.search(r"^Pages:\s+(\d+)$", info_text, re.MULTILINE)
    need(match is not None and match.group(1) == "3", "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    embedded = 0
    for line in fonts.stdout.decode("ascii", errors="replace").splitlines()[2:]:
        if not line.strip() or set(line.strip()) == {"-"}:
            continue
        fields = line.split()
        need(len(fields) >= 8 and fields[-5:-2] == ["yes", "yes", "yes"],
             "font embedding")
        embedded += 1
    need(embedded > 0, "no fonts")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "Overfull \\hbox", "Underfull \\hbox",
                "undefined references", "Fatal", "Error"):
        need(bad not in log, "LaTeX log: " + bad)


def check_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "assert syntax: " + path.name)
    need("tpc276_signed_gain_endpoint_budget_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError,
            KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        print("TPC276_BRIDGE_CHECK=FAIL " + str(error))
        return 1
    print("TPC276_BRIDGE_CHECK=PASS rows=12 gain_above_one=12 "
          "signed_quarter=3 signed_eighth=5 fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
