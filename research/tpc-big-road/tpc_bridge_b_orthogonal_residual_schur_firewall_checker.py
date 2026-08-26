#!/usr/bin/env python3
"""Fail-closed release checker for TPC-264."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-264-orthogonal-residual-schur-firewall"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_orthogonal_residual_schur_firewall.md"
PRODUCER = PROJECT / "code/tpc264_schur_firewall_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc264_independent_checker.py"
STRESS = PROJECT / "experiments/tpc264_schur_stress.py"
CERTIFICATE = PROJECT / "results/tpc264_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "e0966c5a4c3b82d260bd774d1debbbb742c799e2"
STATUS = "PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL"
BRIDGE_SHA256 = "66ed9f4b9558ea086ed5f1952f614f78238c1d0ad0cecd49baaf887091a6d0bd"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "c783920d04ac1a58adb26bd6bcaee61fbc28335acc78f5abed3fd5dfc64161e4",
    "papers/tpc-263-rank-three-physical-cross-gram/README.md":
        "5cede7c57bd2c410d189e46e869232a21fabb840285513fdd001ea74d2485f54",
    "papers/tpc-263-rank-three-physical-cross-gram/PROOF_PACKAGE.md":
        "d5519dc30335611eae313e220e0bd7a64c1d29b06932a65469c03d3e6a33d2dc",
    "papers/tpc-263-rank-three-physical-cross-gram/notes/theorem_ledger.md":
        "895d614fe3564a706cb7fb4bf9056e181a8f78b07315092109b2a143e1620570",
    "papers/tpc-263-rank-three-physical-cross-gram/notes/route_evaluation.md":
        "91f66894d12359ec73fb2ffb8089a7876510073db97062d1560fd2233a3298a5",
    "research/tpc-big-road/bridge_b_rank_three_physical_cross_gram.md":
        "c974eefc33e5832539632740b5da77d21ed84d658b6705d9d4adfc5341a89df9",
    "research/tpc-big-road/tpc_bridge_b_rank_three_physical_cross_gram_checker.py":
        "b989fe071149e8c31d8b0d490aefc132d1da20b65ce344127cae3014cf0f333b",
}

PROJECT_HASHES = {
    ".gitignore": "f3c9a03240b1b7cdea120c494e482533729564039d037516225371f5aba8214c",
    "DERIVATION_PACKAGE.md": "699bbe04a1c1f181bd7ab9c2fac88fd39f715e737d5656b9c541799830cdf691",
    "PAPER_PLAN.md": "b37615b4c142b9139e9a93ff1983e0ecbb2de0a3f132af8b2a0c0191c64bf5ff",
    "PROOF_PACKAGE.md": "f3da6e2fcf0f992e4782f10c83936f5dc8f9c88e2a3ec9b2ff16bfb94c5422fa",
    "README.md": "8bd012ed8adab042a279dc4e48a6165f8baf139578d03a1b499fd34531d74a03",
    "code/tpc264_schur_firewall_certificate.py": "09d7fad2beb289b0b43567d38352c63c5aaa61bfd7dbb8fa3ffb3c072849e8ea",
    "experiments/tpc264_independent_checker.py": "35f59670a522a576e38e0b9dc0ad28c6e8e582113715eae557322571f9c78205",
    "experiments/tpc264_schur_stress.py": "fa26058f9fb9c7655fb1e61bb8dde2c03980b0d63962c30614144a10ca19f712",
    "notes/citation_verification.md": "c4027a9a5322bc8cd096bd3e2d04641e88224368081fb994b95905671a86f93d",
    "notes/claim_firewall.md": "3af700bcecd13eace0cf9f2d499e6c8e21782cd77b9b482a24f50352446bf623",
    "notes/computational_protocol.md": "32d02e767e5cd1ffdc0fb0350daf2e4accef8fe91fb61863e4f7bd40d2e5961c",
    "notes/route_evaluation.md": "08bdf96437fb4cd335c499eae2a1f495b89da4dbc2685e333d2f1e691221151b",
    "notes/theorem_ledger.md": "f4d01f5a5e759a04b046394dd7f41dd6df021ed0fd7dd388fdd79a29b1eec0bb",
    "paper/main.pdf": "99629fe5bdc4cc87e1e64b70038956c1a2645c6f5285cd0f16ddc357bb41727f",
    "paper/main.tex": "a2c6796189554a33cb6b97ad18c94f0389379fadbfca1143c5621eff6768be19",
    "paper/paper.pdf": "99629fe5bdc4cc87e1e64b70038956c1a2645c6f5285cd0f16ddc357bb41727f",
    "paper/references.bib": "70279dce3e9fa7910691ff5927268105728186bb7b3de7928d95706f0d138d75",
    "results/tpc264_certificate.json": "dfa152c2f96d2b31cfc73acd27bebcfbce2ff0c69e56014a3d5be4781d90e0bc",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg", "paper/main.log",
    "paper/main.out",
}

MARKERS = (
    "TPC264_MAXIMUM_CLAIM = " + STATUS,
    "TPC264_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_SCHUR_FIREWALL",
    "TPC264_PROJECTION_DATA = PROVED_EXACT",
    "TPC264_RESIDUAL_GRAM_FEASIBLE_SET = PROVED_EXACT",
    "TPC264_COMPLEMENT_DIMENSION_SPLIT = PROVED_EXACT",
    "TPC264_FULL_SCALAR_FEASIBLE_SET = PROVED_EXACT",
    "TPC264_ENDPOINT_SCALE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL",
    "TPC264_FIXED_POWER_CREDIT = 0",
    "TPC264_ARITHMETIC_ADVANCE = NO",
    "TPC264_ACTUAL_V59_RESIDUAL = OPEN",
    "TPC264_L2 = NONE",
    "TPC264_FULL_GATE_B = OPEN",
    "TPC264_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC264_TWIN_PRIME_RESULT = NONE",
    "TPC264_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE",
    "TPC264_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def normalized_digest(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(path)).hexdigest() == expected,
             "source hash: " + path)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(normalized_digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH", "bridge hash placeholder")
    need(normalized_digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in text, "bridge marker: " + marker)
    need("ROUND2_CLUE = TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE" in text,
         "round-two clue")


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    producer = child(PRODUCER, "TPC264_CERTIFICATE=PASS")
    independent = child(INDEPENDENT, "TPC264_INDEPENDENT_CHECK=PASS")
    independent_opt = child(INDEPENDENT, "TPC264_INDEPENDENT_CHECK=PASS", True)
    stress = child(STRESS, "TPC264_SCHUR_STRESS=PASS")
    stress_opt = child(STRESS, "TPC264_SCHUR_STRESS=PASS", True)
    need(independent == independent_opt, "independent stdout mismatch")
    need(stress == stress_opt, "stress stdout mismatch")
    need("schur=EXACT" in producer and "fixed_power_credit=0" in producer,
         "producer fields")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) +
                 "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") == "TPC264_SCHUR_FIREWALL_CERTIFICATE_V1",
         "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD and
         parsed.get("baseline", {}).get("source_count") == 8,
         "certificate baseline")
    projection = parsed.get("projection_fixture", {})
    need(projection.get("center") == ["2", "1"] and
         projection.get("radius") == "3" and
         projection.get("complement_dimension") == 2,
         "projection fixture")
    records = projection.get("records", {})
    need(records.get("plus", {}).get("residual_inner_product") == ["3", "0"] and
         records.get("minus", {}).get("residual_inner_product") == ["-3", "0"] and
         records.get("zero", {}).get("residual_inner_product") == ["0", "0"] and
         records.get("quarter_turn", {}).get("residual_inner_product") == ["0", "3"],
         "residual endpoints")
    dimensions = parsed.get("dimension_audit", {})
    need(dimensions.get("disk_feasible") is True and
         dimensions.get("circle_positive_modulus") is True and
         dimensions.get("circle_zero_rejected") is True,
         "dimension audit")
    budget = parsed.get("endpoint_budget_audit", {})
    need(budget.get("synthetic_radius_exponent") == "5/3" and
         budget.get("required_strict_saving") == "1/400" and
         budget.get("fixed_power_credit") == 0 and
         budget.get("synthetic_only") is True,
         "budget audit")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC264_ACTUAL_V59_RESIDUAL") == "OPEN" and
         firewall.get("TPC264_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC264_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC264_L2") == "NONE" and
         firewall.get("TPC264_TWIN_PRIME_RESULT") == "NONE",
         "firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Orthogonal-Residual Schur Firewall", "Liang Wang",
                   "Schur feasible", "closed disk", "dimension", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+5\s*$", info_text) is not None,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = [row for row in fonts.stdout.decode("ascii").splitlines()[2:]
            if row.strip()]
    need(len(rows) >= 10, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF font embedding")
    if LOG.is_file():
        log_text = LOG.read_text(encoding="utf-8", errors="replace")
        bad = re.search(r"(?m)^(?:LaTeX Warning:|Package .* Warning:|"
                        r"Overfull \\\\|Underfull \\\\|"
                        r"There were undefined references)", log_text)
        need(bad is None, "LaTeX log")


def check_source_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "unsafe assertion syntax: " + path.name)
    need("tpc264_schur_firewall_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_source_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print("TPC264_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC264_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("schur_feasible_set=PROVED_EXACT")
    print("full_scalar_set=PROVED_EXACT_CONDITIONAL")
    print("actual_v59_residual=OPEN")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
