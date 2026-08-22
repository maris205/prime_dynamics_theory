#!/usr/bin/env python3
"""Fail-closed release checker for TPC-223."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-223-conditional-signed-reassembly-compiler"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_conditional_signed_reassembly_compiler.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "d4cd11a5cef966f2df4f62fbc13f1179bccbc236f5c20f7d0355b4b847d376a2"


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(
        command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    require(result.returncode == 0, f"command failed: {' '.join(command)}")
    require(result.stderr == "", f"stderr from command: {' '.join(command)}")
    return result.stdout


def fraction(value: str):
    from fractions import Fraction

    return Fraction(value)


def check_layout() -> None:
    required = (
        "README.md",
        "PAPER_PLAN.md",
        "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md",
        "paper/main.tex",
        "paper/references.bib",
        "paper/main.pdf",
        "paper/paper.pdf",
        "code/reassembly_compiler.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/borderline_adversary.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing project file: {relative}")
    require(
        (PROJECT / "paper/main.pdf").read_bytes() == (PROJECT / "paper/paper.pdf").read_bytes(),
        "PDF copies differ",
    )
    require(PROOF_SHA256 != "TO_BE_FILLED", "proof hash not frozen")
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash mismatch")
    proof_text = PROOF.read_text()
    for anchor in (
        "TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA",
        "TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT",
        "TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT",
        "TPC223_ARITHMETIC_ADVANCE = NO",
    ):
        require(anchor in proof_text, f"missing proof anchor: {anchor}")
    require("Liang Wang" in (PROJECT / "README.md").read_text(), "author lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text())
    require(data.get("schema") == "tpc223-conditional-signed-reassembly-compiler-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "CONDITIONAL_THEOREM", "claim level")
    require(data.get("baseline_exponent") == "5/3", "baseline")
    require(data.get("strict_threshold") == "1/400", "threshold")
    require(data.get("arithmetic_advance") == "NO", "arithmetic firewall")
    require(data.get("fixed_atom_credit") == 0, "atom firewall")
    require(data.get("l2") == "NONE", "L2 firewall")
    require(data.get("full_gate_b") == "OPEN", "Gate B firewall")
    require(data.get("strict_1_over_400") == "UNPAID", "strict firewall")
    require(data.get("conditional_inputs") == {
        "ap_dispersion": "OPEN",
        "literal_reassembly_interface": "OPEN",
        "polarized_cross_correlation": "OPEN",
    }, "conditional inputs")
    records = data.get("records")
    require(type(records) is list and len(records) == 5, "record count")
    names = [record.get("name") for record in records]
    require(names == [
        "strict_endpoint",
        "borderline_endpoint",
        "failed_endpoint",
        "missing_polarized_saving",
        "loss_dominates",
    ], "record order")
    require(records[0]["status"] == "STRICT_PASS", "strict fixture")
    require(records[0]["effective_saving"] == "11/1200", "effective saving")
    require(fraction(records[0]["strict_margin"]) == fraction("1/150"), "strict margin")
    require(fraction(records[0]["compiled_exponent"]) == fraction("663/400"), "compiled exponent")
    require(fraction(records[0]["target_exponent"]) == fraction("1997/1200"), "target exponent")
    require(records[1]["status"] == "BORDERLINE", "borderline status")
    require(records[2]["status"] == "NO_STRICT_SAVING", "failed status")
    require(records[3]["status"] == "NO_STRICT_SAVING", "missing-channel status")
    require(records[4]["status"] == "NO_STRICT_SAVING", "loss status")
    require(all(value is True for value in data["checks"].values()), "certificate checks")


def check_subchecks() -> None:
    commands = [
        [sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")],
        [sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")],
    ]
    outputs = [run(command) for command in commands]
    require(outputs[0] == outputs[1], "normal/optimized output differs")
    require("TPC223_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check failed")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/borderline_adversary.py")])
    require("TPC223_BOUNDARY_ADVERSARY=PASS" in adversary, "adversary failed")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           3" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in (
        "Conditional Signed-Reassembly Compiler",
        "Liang Wang",
        "1/400",
        "borderline",
        "References",
    ):
        require(phrase in text, f"missing PDF phrase: {phrase}")
    fonts = run(["pdffonts", str(pdf)])
    for line in fonts.splitlines()[2:]:
        if line.strip():
            require(line.split()[-4] == "yes", "unembedded font")


def main() -> int:
    try:
        check_layout()
        check_certificate()
        check_subchecks()
        check_pdf()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"TPC223_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC223_BRIDGE_CHECK=PASS")
    print("records=5")
    print("effective_saving=11/1200")
    print("strict_margin=1/150")
    print("claim_level=CONDITIONAL_THEOREM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
