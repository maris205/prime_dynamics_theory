#!/usr/bin/env python3
"""Fail-closed release checker for TPC-259."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-259-same-clock-null-coupling"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_same_clock_null_coupling.md"
PRODUCER = PROJECT / "code/tpc259_null_coupling_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc259_independent_checker.py"
STRESS = PROJECT / "experiments/tpc259_null_coupling_stress.py"
CERTIFICATE = PROJECT / "results/tpc259_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
BASELINE_HEAD = "dc1f6628cc4953eeaad015aac79e48e6ca546773"
STATUS = (
    "PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_"
    "FOR_LITERAL_V59_SIGNED_COUPLING"
)

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "de46b106bfdf26832e9fb9c1dfbe3066088d89bb4d299d1de2cbc4b24121ba2f",
    "papers/tpc-258-source-frozen-transverse-null-direction/README.md":
        "760687705f6e4f4edf83dc1753eab092d36bbefb7d74bd4a0f857dd719bf3083",
    "papers/tpc-258-source-frozen-transverse-null-direction/PROOF_PACKAGE.md":
        "9676295123b94cabc78a3e24b95475380557a5a3accc0b890ba33e18a5e09c19",
    "papers/tpc-258-source-frozen-transverse-null-direction/notes/theorem_ledger.md":
        "66f70e7d6594f01ce872d1b9d0ecfe83bd96d2549986a9bd456dc7f6d049618a",
    "papers/tpc-258-source-frozen-transverse-null-direction/notes/route_evaluation.md":
        "f45a8b300b8f1fc7aa02b76d58ab78a2186b53a744380c129b42eac724639b5f",
    "research/tpc-big-road/bridge_b_source_frozen_transverse_null_direction.md":
        "0f5d65ffc419ac07c47c282ce34f05800e6d7342b6ffd8588d06c102c4b4c75d",
    "research/tpc-big-road/tpc_bridge_b_source_frozen_transverse_null_direction_checker.py":
        "770e47e9495bee3ed5115a29f6b050c14a529f2b14814ab09fdfcdb8d4dc42c2",
    "papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/PROOF_PACKAGE.md":
        "bb23c4dfc5cced89b34db0d2741b570c07335ac9aa153ae123d056f29924b768",
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md":
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee",
    "research/tpc-big-road/fm_local_comparison_compiler.md":
        "4f7537ff5a10d53634638afff508ee6e3401364dab7970852b327470918c644f",
}

# Filled after all TPC-259 project sources and the final PDF are built.
PROJECT_HASHES = {
    ".gitignore": "877a508d3d5e64e6ed46e9d4e6f5bf913239ea84d48c5e551dee08616603f3ed",
    "DERIVATION_PACKAGE.md": "a3896342caf26766198d0f4a14867f1e348215d91676fbaf77da16fbdf8546bd",
    "PAPER_PLAN.md": "854fd812f078def4a1aee984bfa38fb3ca8ef2128cec0fa15aecb802e059d002",
    "PROOF_PACKAGE.md": "f4573edbd6d30045f0f476508d3bccf315fba42fb50603c6da8f54c3b466eb14",
    "README.md": "a54e3ade4a56aec2e79be049ff4db06d30b79356115691af3686c00a844d5f86",
    "code/tpc259_null_coupling_certificate.py": "053828e13ed92497593e360dc4bd2655f7b9f19a5845e1920ddd95a843f72b30",
    "experiments/tpc259_independent_checker.py": "057f67d69e39ebb206eed5d3d8066170e8931a98a9f7aec37d1954130b8001ff",
    "experiments/tpc259_null_coupling_stress.py": "3c6ccf0df7af7d73f8f7b8c04f255e217906c162efc034d6b06223bceb78b2bc",
    "notes/citation_verification.md": "f8828a12741fb7505b0c552071e52f3da0493d8990bac0a3f3a0fec74f676582",
    "notes/claim_firewall.md": "ba052b103c230c5a77dcb06f2e7287c4757469c27000e563e9ae275f1f9b5ca9",
    "notes/computational_protocol.md": "75fa35992dab8bfe349af7a890e19b596d65daf7e558e9b89753fc8e594f363a",
    "notes/route_evaluation.md": "e0d40481e4c745323be9618c72e127de14523118899c9c26b040c38407105431",
    "notes/theorem_ledger.md": "6ecbad2368776856aa7ed4c1c20987ab2df0422c86283c5ec691f5d9c379d1de",
    "paper/main.tex": "657c1a3b86ceaf978dd9d40dd6c4d5540da5e27aee745f72bb39fbe7550fef0f",
    "paper/paper.pdf": "50dee6b618644829c4b5c17e1f9b7f390021a092848b419c17a319743f051788",
    "paper/references.bib": "978467b31a799d112bb997d99423cbe144319b0b9a65da2f12dac774a34f2a42",
    "results/tpc259_certificate.json": "01687a34996ecc88c41c17dd12846b6ae08442c6096ddb7f5ff5de4becf088ab",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}

MARKERS = (
    "TPC259_MAXIMUM_CLAIM = " + STATUS,
    "TPC259_ROUTE_ADVANCE = YES_SCOPED_NULL_CHANNEL",
    "TPC259_ARITHMETIC_ADVANCE = YES_SCOPED_SIGNED_COUPLING_CHANNEL",
    "TPC259_W_NULL_MOMENT = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC259_NULL_CHANNEL = PROVED_SOURCE_BACKED_o_ONE",
    "TPC259_RESIDUAL_DECOMPOSITION = PROVED_EXACT",
    "TPC259_RESIDUAL_FULL_SCALAR = OPEN",
    "TPC259_FIXED_POWER_SAVING = NONE",
    "TPC259_L2 = NONE",
    "TPC259_FULL_GATE_B = OPEN",
    "TPC259_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC259_FIXED_ATOM_CREDIT = 0",
    "TPC259_TWIN_PRIME_RESULT = NONE",
    "TPC259_STATUS = " + STATUS,
)

REQUIRED_SEMANTIC = (
    "5/3", "79/48", "1/48", "w_perp", "zero-diagonal",
    "conjugate", "ROUND2_CLUE", "OPEN", "NONE",
)
EXPECTED_PDF_PAGES = 4
EXPECTED_PDF_FONTS = 25


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def baseline_bytes(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "baseline source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(digest(baseline_bytes(relative)) == expected,
             "source hash: " + relative)


def check_exponent_ledger() -> None:
    need(Fraction(1, 2) + Fraction(7, 6) == Fraction(5, 3),
         "null product exponent")
    need(Fraction(1, 2) + Fraction(55, 48) == Fraction(79, 48),
         "residual boundary exponent")
    need(Fraction(5, 3) - Fraction(79, 48) == Fraction(1, 48),
         "residual gap")
    need(Fraction(2, 3) + Fraction(1, 2) == Fraction(7, 6),
         "source diagonal exponent")


def check_project_manifest() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file()}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    need((actual & BUILD_INTERMEDIATES) in (set(), BUILD_INTERMEDIATES),
         "partial build manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(digest((PROJECT / relative).read_bytes()) == expected,
             "project hash: " + relative)


def run_child(path: Path, marker: bytes) -> bytes:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_pdf() -> None:
    tools = [shutil.which(name) for name in ("pdftotext", "pdffonts", "pdfinfo")]
    need(all(tool is not None for tool in tools), "PDF tools")
    pdftotext, pdffonts, pdfinfo = tools
    text = subprocess.run([pdftotext, "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    need(b"A Same-Clock Null-Channel Decomposition" in text.stdout,
         "PDF title")
    need(b"Literal V59 Signed Coupling" in text.stdout, "PDF title continuation")
    need(b"Source-backed null moment" in text.stdout, "PDF theorem")
    need(b"Exact synthetic non-promotion witness" in text.stdout,
         "PDF obstruction")
    info = subprocess.run([pdfinfo, str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+4\s*$", info_text) is not None,
         "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = [row for row in fonts.stdout.decode("ascii").splitlines()[2:]
            if row.strip()]
    need(len(rows) == EXPECTED_PDF_FONTS, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF fonts embedded")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=True) + "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") == "TPC259_CERTIFICATE_V1",
         "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD,
         "certificate baseline")
    need(parsed.get("null_constants", {}).get("weights")
         == ["0.579956823172377", "-0.814647213986401"],
         "certificate null weights")
    need(parsed.get("exponent_ledger") == {
        "gap": "1/48", "null_product": "5/3",
        "residual_boundary": "79/48", "source_diagonal": "7/6"},
         "certificate exponent ledger")
    statuses = parsed.get("epistemic_status", {})
    need(statuses.get("null_channel") == "PROVED_SOURCE_BACKED_o_ONE",
         "certificate null status")
    need(statuses.get("residual") == "OPEN", "certificate residual status")
    need(statuses.get("rate_refinement") == "CONDITIONAL_THEOREM",
         "certificate rate status")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC259_FIXED_POWER_SAVING") == "NONE" and
         firewall.get("TPC259_L2") == "NONE" and
         firewall.get("TPC259_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC259_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")
    witness = parsed.get("synthetic_witness", {})
    need(witness.get("status") == "PROVED_EXACT_SYNTHETIC_NOT_LITERAL" and
         witness.get("null_channel") == "0" and
         witness.get("residual") == "3/2" and
         witness.get("zero_diagonal") is True,
         "certificate witness")
    need(parsed.get("rate_diagnostic", {}).get("proof_credit") == "NONE",
         "numerical proof credit")


def run() -> None:
    check_project_manifest()
    check_sources()
    check_exponent_ledger()
    need(BRIDGE.is_file(), "bridge missing")
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    joined = bridge_text + "\n" + "\n".join(
        (PROJECT / relative).read_text(encoding="utf-8", errors="replace")
        for relative in ("README.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
                         "notes/route_evaluation.md", "paper/main.tex")
    )
    for marker in MARKERS:
        need(marker in joined, "marker: " + marker)
    for marker in REQUIRED_SEMANTIC:
        need(marker in joined, "semantic marker: " + marker)
    for script in (PRODUCER, INDEPENDENT, STRESS):
        need("as" + "sert " not in script.read_text(encoding="utf-8"),
             "unsafe assertion syntax")
    independent_text = INDEPENDENT.read_text(encoding="utf-8")
    need(("from " + "tpc259_null_coupling_certificate") not in independent_text,
         "independent producer import")
    check_certificate()
    log_path = PROJECT / "paper/paper.log"
    need(log_path.is_file(), "LaTeX log missing")
    log = log_path.read_text(encoding="utf-8", errors="replace")
    for forbidden in ("LaTeX Warning", "Undefined control sequence", "Overfull",
                      "Underfull"):
        need(forbidden not in log, "LaTeX log: " + forbidden)
    check_pdf()
    run_child(PRODUCER, b"TPC259_CERTIFICATE=PASS")
    run_child(INDEPENDENT, b"TPC259_INDEPENDENT_CHECK=PASS")
    run_child(STRESS, b"TPC259_STRESS=PASS")
    print("TPC259_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=" + str(EXPECTED_PDF_PAGES))
    print("pdf_fonts=" + str(EXPECTED_PDF_FONTS) +
          "_EMBEDDED_SUBSETTED_UNICODE")
    print("null_channel=PROVED_SOURCE_BACKED")
    print("w_null_bound=SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER")
    print("residual=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC259_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, OSError, UnicodeError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC259_BRIDGE_CHECK=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
