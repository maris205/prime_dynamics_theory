#!/usr/bin/env python3
"""Fail-closed release checker for TPC-258."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-258-source-frozen-transverse-null-direction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_source_frozen_transverse_null_direction.md"
PRODUCER = PROJECT / "code/tpc258_null_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc258_independent_checker.py"
STRESS = PROJECT / "experiments/tpc258_null_stress.py"
CERTIFICATE = PROJECT / "results/tpc258_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
BASELINE_HEAD = "337fa65aca20122f241c30c67f1deb64b45e3c0b"
STATUS = (
    "PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_"
    "FOR_LITERAL_V59_ADJOINT"
)

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "c4c79b25fdbcdb7f8f26b1348263f159d5cd7f55c486c2653066c5519a1782a5",
    "research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md":
        "faaede82e2ebf84a994e3e9c945e42c321a8c81d0c0db9e0f8e2f9a88329e609",
    "research/tpc-big-road/tpc_bridge_b_four_block_haar_transverse_norm_floor_checker.py":
        "d2cf0321dfbc730850438badaadf6018e0555662010ea39b80bd12a175ded2e1",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md":
        "06b6f2e9842f68fc6f3d882f95d3b9c161980ceb429dd24b52bd98322e6f397f",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/theorem_ledger.md":
        "127bf4a07defd26a87f74e989a426500a3b50a18df03875805b9afeb71a5a3a6",
    "papers/tpc-257-four-block-haar-transverse-norm-floor/notes/route_evaluation.md":
        "b92bf14797013e4371a0d9c88d4dc7bdef39d76b1361d8cf73009165b41e1f3f",
    "research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md":
        "ccb87a64ddb36ed35af415dde2d9fcf0a3ed7f443934edf0a24c98f7bd3ab4da",
    "research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md":
        "093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906",
}

# Filled after the final project sources and PDF have been built.
PROJECT_HASHES = {
    ".gitignore": "d92f5c8f90059cd13dc2b16e79d88d4b4d7bfb936cb1ae88d90f407177332bb3",
    "DERIVATION_PACKAGE.md": "1cf47e88d1232c9797b486a6033b456f4e4022345a9e0251997a491fba19c4ff",
    "PAPER_PLAN.md": "0bd59e98a9688c33ae61f93f6a40e53b82dcbd7ba2e80900c2f74336e6932fa0",
    "PROOF_PACKAGE.md": "9676295123b94cabc78a3e24b95475380557a5a3accc0b890ba33e18a5e09c19",
    "README.md": "760687705f6e4f4edf83dc1753eab092d36bbefb7d74bd4a0f857dd719bf3083",
    "code/tpc258_null_certificate.py": "2d0d26a8fbf8780db86f08df2f0946b7f43d759b3bd580e3791c1cbb5f2b9832",
    "experiments/tpc258_independent_checker.py": "4323312d93cd8eefc37c5f19a36668a9a1acdf20db85132826d7e1c5af5b4ccb",
    "experiments/tpc258_null_stress.py": "bc197a4d725f54cfafacd26043649a3acd2d93ea27ccc0c54775633de63f2b7c",
    "notes/citation_verification.md": "3ac9dfb059e16b87bee7087e23ee6a9e2f58a3253bdd421ff774664358bed2a4",
    "notes/claim_firewall.md": "09ca2fd28b83dca93d1c19f3ac8704ea9863ea69a833f4592a5310308355ba63",
    "notes/computational_protocol.md": "2c98eb083f9ae9972bdc3e1a0b60c69fb5d209588e81e96ee1acb434cd1cd6ec",
    "notes/route_evaluation.md": "f45a8b300b8f1fc7aa02b76d58ab78a2186b53a744380c129b42eac724639b5f",
    "notes/theorem_ledger.md": "66f70e7d6594f01ce872d1b9d0ecfe83bd96d2549986a9bd456dc7f6d049618a",
    "paper/main.tex": "aee30ecfc8b05bd9dcc0918801374445c9e48229fc77783a24d42b51b6496281",
    "paper/paper.pdf": "8ef87cc715099b39dba45643a675f493256a1573a0cb974a6369692e1fd92527",
    "paper/references.bib": "ea8627dcdb1a79c023a633e90f59c809ea05c952a30577bb81aac3c3746983ac",
    "results/tpc258_certificate.json": "041bf8ff9fd21ae2dd94557c4edb92de6deb24d2641397197b4f7ec0631d4263",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/paper.aux", "paper/paper.bbl", "paper/paper.blg",
    "paper/paper.log", "paper/paper.out",
}
MARKERS = (
    "TPC258_MAXIMUM_CLAIM = " + STATUS,
    "TPC258_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_NULL",
    "TPC258_ARITHMETIC_ADVANCE = YES_SCOPED_LOG_CANCELLATION",
    "TPC258_NULL_DIRECTION = PROVED_SOURCE_FROZEN_UNIT_VECTOR",
    "TPC258_LEADING_DIAGONAL_CANCELLATION = PROVED_SOURCE_BACKED",
    "TPC258_RATE_REFINEMENT = CONDITIONAL_THEOREM_LOG_ONE_OVER_X",
    "TPC258_FIXED_POWER_SAVING = NONE",
    "TPC258_L2 = NONE",
    "TPC258_FULL_GATE_B = OPEN",
    "TPC258_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC258_FIXED_ATOM_CREDIT = 0",
    "TPC258_TWIN_PRIME_RESULT = NONE",
    "TPC258_STATUS = " + STATUS,
)
REQUIRED_SEMANTIC = (
    "3456/3125", "884736/823543", "o(S_x)", "CONDITIONAL_THEOREM",
    "1/sqrt(log x)", "1/48", "ROUND2_CLUE", "signed `w`",
)
EXPECTED_PDF_PAGES = 5
EXPECTED_PDF_FONTS = 26


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
    need(result.returncode == 0 and result.stderr == b"", "baseline source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(digest(baseline_bytes(relative)) == expected, "source hash: " + relative)


def check_exponent_ledger() -> None:
    need(Fraction(133, 400) - Fraction(1, 2) == Fraction(-67, 400),
         "divisor exponent")
    need(Fraction(1, 3) + 2 * Fraction(21, 32) - Fraction(1, 2)
         == Fraction(55, 48), "boundary exponent")
    need(Fraction(2, 3) + Fraction(1, 2) == Fraction(7, 6),
         "diagonal exponent")
    need(Fraction(7, 6) - Fraction(55, 48) == Fraction(1, 48),
         "boundary gap")


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
    need(result.returncode == 0 and result.stderr == b"", "child failed: " + path.name)
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
    need(b"A Source-Frozen Transverse Null Direction" in text.stdout,
         "PDF title")
    need(b"Literal V59 Adjoint" in text.stdout, "PDF title continuation")
    need(b"Source-frozen transverse diagonal cancellation" in text.stdout,
         "PDF theorem")
    info = subprocess.run([pdfinfo, str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    need(info.returncode == 0 and
         ("Pages:           " + str(EXPECTED_PDF_PAGES)).encode() in info.stdout,
         "PDF pages")
    fonts = subprocess.run([pdffonts, str(PDF)], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = fonts.stdout.decode("ascii").splitlines()[2:]
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
    need(parsed.get("schema") == "TPC258_CERTIFICATE_V1", "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD,
         "certificate baseline")
    need(parsed.get("constants", {}).get("symbolic_cancellation")
         == "L2*(L1/2)-L1*(L2/2)=0", "certificate cancellation")
    need(parsed.get("constants", {}).get("null_weights")
         == ["0.579956823172377", "-0.814647213986401"],
         "certificate weights")
    need(parsed.get("epistemic_status", {}).get("theorem")
         == "PROVED_SOURCE_BACKED", "certificate theorem status")
    need(parsed.get("epistemic_status", {}).get("rate_refinement")
         == "CONDITIONAL_THEOREM", "certificate rate status")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC258_FIXED_POWER_SAVING") == "NONE" and
         firewall.get("TPC258_L2") == "NONE" and
         firewall.get("TPC258_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC258_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")
    need(parsed.get("numerical_observation", {}).get("proof_credit") == "NONE",
         "numerical proof credit")
    need(parsed.get("adversarial_control", {}).get("proof_credit")
         == "QUANTIFIER_FIREWALL_ONLY", "adversarial proof credit")


def run() -> None:
    check_project_manifest()
    check_sources()
    check_exponent_ledger()
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
    need(("from " + "tpc258_null_certificate") not in independent_text,
         "independent producer import")
    check_certificate()
    log = PROJECT.joinpath("paper/paper.log").read_text(encoding="utf-8",
                                                         errors="replace")
    for forbidden in ("LaTeX Warning", "Undefined control sequence", "Overfull",
                      "Underfull"):
        need(forbidden not in log, "LaTeX log: " + forbidden)
    check_pdf()
    run_child(PRODUCER, b"TPC258_CERTIFICATE=PASS")
    run_child(INDEPENDENT, b"TPC258_INDEPENDENT_CHECK=PASS")
    run_child(STRESS, b"TPC258_STRESS=PASS")
    print("TPC258_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("pdf_pages=" + str(EXPECTED_PDF_PAGES))
    print("pdf_fonts=" + str(EXPECTED_PDF_FONTS) + "_EMBEDDED_SUBSETTED_UNICODE")
    print("null_direction=SOURCE_FROZEN")
    print("leading_cancellation=PROVED_SOURCE_BACKED")
    print("rate_refinement=CONDITIONAL_LOG_ONE_OVER_X")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC258_BRIDGE_CHECK=FAIL: use --check")
    try:
        run()
    except (Failure, OSError, UnicodeError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC258_BRIDGE_CHECK=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
