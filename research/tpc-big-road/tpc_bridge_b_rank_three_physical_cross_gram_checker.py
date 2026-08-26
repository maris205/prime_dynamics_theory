#!/usr/bin/env python3
"""Fail-closed release checker for TPC-263."""

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
PROJECT = ROOT / "papers/tpc-263-rank-three-physical-cross-gram"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_rank_three_physical_cross_gram.md"
PRODUCER = PROJECT / "code/tpc263_rank_three_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc263_independent_checker.py"
STRESS = PROJECT / "experiments/tpc263_rank_three_stress.py"
CERTIFICATE = PROJECT / "results/tpc263_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "6c32d179c7225add34dfcc3a4d43a0c59da14424"
STATUS = "PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL"
BRIDGE_SHA256 = "c974eefc33e5832539632740b5da77d21ed84d658b6705d9d4adfc5341a89df9"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "344c75a6c41730703b04d5474e385986f8c66dcf5639531848da99c3bec574f4",
    "papers/tpc-262-literal-mode-zero-cross-gram/README.md":
        "d93b364a110103a81cdf3e766586da0f43af1f2b090aecb7514e875d4f8365d6",
    "papers/tpc-262-literal-mode-zero-cross-gram/PROOF_PACKAGE.md":
        "520f74acd0fc39f50c53d1cef31e2a9a599630384b4f888b190a8a64842364b1",
    "papers/tpc-262-literal-mode-zero-cross-gram/notes/theorem_ledger.md":
        "ef8c6d834dfda217a412c99d9f70a93961ac7e501fa7a86c8b9286d92dcb8556",
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md":
        "faaede82e2ebf84a994e3e9c945e42c321a8c81d0c0db9e0f8e2f9a88329e609",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md":
        "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md":
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee",
    "papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/notes/theorem_ledger.md":
        "ea138a0cd5839bdb62633a38389f82a4e6f4346641757b05729722daec89aa2b",
}

PROJECT_HASHES = {
    ".gitignore": "a495087842e7bc327a9be7a7a5077c474b10e8ed6266185de2cb27e463afd73f",
    "DERIVATION_PACKAGE.md": "b91e986a724a5878158c37d4380fe58c3139e321602a1985f7a2d7ff0c24ca77",
    "PAPER_PLAN.md": "039d73d0264ee585a892f5632724f5e1b83c623b7cc8ccaa26378deb9c99b166",
    "PROOF_PACKAGE.md": "d5519dc30335611eae313e220e0bd7a64c1d29b06932a65469c03d3e6a33d2dc",
    "README.md": "5cede7c57bd2c410d189e46e869232a21fabb840285513fdd001ea74d2485f54",
    "code/tpc263_rank_three_certificate.py": "b6a6bb2e1c07b3f03585680f83055d11269920fef15c1adf72e1b55bb30e6891",
    "experiments/tpc263_independent_checker.py": "f4b2584ae760df2dcca4f1398ea4c112bd4bff55f0bb4754e25120737396446e",
    "experiments/tpc263_rank_three_stress.py": "276957b94e53f2e76f5fda25abd08269f3b1614b04517de52f111b1f53c7db12",
    "notes/citation_verification.md": "9d5cda180d2a9d9721684272308a1c30f0d3071fba78577865e871061d279c0c",
    "notes/claim_firewall.md": "048e30ade8c52d2e094d73573a7d616099a1037c2406931cb9d33a15d455eb51",
    "notes/computational_protocol.md": "428cd917a3245baa5f171b8ed87033be5f545b7684dff38179add33988e7ce9a",
    "notes/route_evaluation.md": "91f66894d12359ec73fb2ffb8089a7876510073db97062d1560fd2233a3298a5",
    "notes/theorem_ledger.md": "895d614fe3564a706cb7fb4bf9056e181a8f78b07315092109b2a143e1620570",
    "paper/main.pdf": "983022dbbd751f2466a671e8b8639fb30532d86508e030905f0f6707f52ed0fc",
    "paper/main.tex": "d5e4403dd84d5a428364e125f1ba0b655a091f2c539900d4e4b786f2fac79709",
    "paper/paper.pdf": "983022dbbd751f2466a671e8b8639fb30532d86508e030905f0f6707f52ed0fc",
    "paper/references.bib": "e5f60bc2cf49aa5338b4f895569cb19ded826ba6d962e5c9449753d34145d52a",
    "results/tpc263_certificate.json": "70b76eade01f5616737266098dffd7400f2906786da68e21cc0815bd38297ff9",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.log", "paper/main.out",
}

MARKERS = (
    "TPC263_MAXIMUM_CLAIM = " + STATUS,
    "TPC263_ROUTE_ADVANCE = YES_SCOPED_RANK_THREE_LOG_CHANNEL",
    "TPC263_W_FRAME_MOMENTS = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC263_ADJOINT_FRAME_COEFFICIENTS = PROVED_SOURCE_BACKED_TPC257",
    "TPC263_PROJECTION_SPLIT = PROVED_EXACT",
    "TPC263_RANK_THREE_CHANNEL = PROVED_SOURCE_BACKED_X_5_OVER_3_LOG_M_PLUS_3",
    "TPC263_ORTHOGONAL_RESIDUAL = OPEN",
    "TPC263_FIXED_POWER_CREDIT = 0",
    "TPC263_ARITHMETIC_ADVANCE = YES_SCOPED_FIXED_LOG_ONLY",
    "TPC263_L2 = NONE",
    "TPC263_FULL_GATE_B = OPEN",
    "TPC263_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC263_TWIN_PRIME_RESULT = NONE",
    "TPC263_STATUS = " + STATUS,
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
    need("ROUND2_CLUE = ATTACK_THE_ORTHOGONAL_COMPLEMENT" in text,
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
    producer = child(PRODUCER, "TPC263_CERTIFICATE=PASS")
    independent = child(INDEPENDENT, "TPC263_INDEPENDENT_CHECK=PASS")
    independent_opt = child(INDEPENDENT, "TPC263_INDEPENDENT_CHECK=PASS", True)
    stress = child(STRESS, "TPC263_RANK_THREE_STRESS=PASS")
    stress_opt = child(STRESS, "TPC263_RANK_THREE_STRESS=PASS", True)
    need(independent == independent_opt, "independent stdout mismatch")
    need(stress == stress_opt, "stress stdout mismatch")
    need("channel=x^(5/3)/log^(M+3)" in producer,
         "producer channel field")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) +
                 "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") ==
         "TPC263_RANK_THREE_PHYSICAL_CROSS_GRAM_CERTIFICATE_V1",
         "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD and
         parsed.get("baseline", {}).get("source_count") == 11,
         "certificate baseline")
    constants = parsed.get("constants_and_exponents", {})
    need(constants.get("channel_exponent") == "5/3" and
         constants.get("channel_log_power") == "M+3" and
         constants.get("endpoint_gap") == "1/400" and
         constants.get("fixed_power_credit") == 0,
         "exponent ledger")
    projection = parsed.get("projection_audit", {})
    need(projection.get("projection_rank") == 3 and
         projection.get("residual_nonzero") is True and
         projection.get("projected_cross_gram") == ["-5", "14"],
         "projection audit")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC263_ORTHOGONAL_RESIDUAL") == "OPEN" and
         firewall.get("TPC263_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC263_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC263_L2") == "NONE" and
         firewall.get("TPC263_TWIN_PRIME_RESULT") == "NONE",
         "firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Rank-Three", "Physical Cross-Gram", "Liang Wang",
                   "x^(5/3)", "orthogonal residual", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+4\s*$", info_text) is not None,
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
    need("tpc263_rank_three_certificate" not in
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
        print("TPC263_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC263_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("rank_three_channel=PROVED_SOURCE_BACKED_LOG_ONLY")
    print("orthogonal_residual=OPEN")
    print("fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
