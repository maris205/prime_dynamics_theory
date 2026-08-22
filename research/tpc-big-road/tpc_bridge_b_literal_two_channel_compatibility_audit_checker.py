#!/usr/bin/env python3
"""Fail-closed release checker for TPC-224."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-224-literal-two-channel-compatibility-audit"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_literal_two_channel_compatibility_audit.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "5569492608f08f897a6c7eca28fe948fe185f8fdf39c08a7989c5ec92a29a603"


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
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, f"command failed: {' '.join(command)}")
    require(result.stderr == "", f"stderr from command: {' '.join(command)}")
    return result.stdout


def f(value: str) -> Fraction:
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
        "code/literal_compatibility.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/boundary_adversary.py",
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
        "TPC224_COMMON_LITERAL_HILBERT_INTERFACE = PROVED_EXACT",
        "TPC224_SHARP_ADDITIVE_CONSTANT = PROVED_EXACT",
        "TPC224_UNIT_INTERFACE = REFUTED_SCOPED",
        "TPC224_ARITHMETIC_ADVANCE = NO",
    ):
        require(anchor in proof_text, f"missing proof anchor: {anchor}")
    readme = (PROJECT / "README.md").read_text()
    require("Liang Wang" in readme, "author lock missing")
    require("Huazhong University of Science and Technology" in readme, "affiliation lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text())
    require(data.get("schema") == "tpc224-literal-two-channel-compatibility-audit-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level")
    require(data.get("author") == "Liang Wang", "author")
    require(data.get("affiliation") == "Huazhong University of Science and Technology", "affiliation")
    theorem = data.get("theorem")
    require(theorem.get("common_vector_interface") == "PROVED_EXACT", "common interface")
    require(theorem.get("sharp_additive_constant") == "PJ/(P+J)", "sharp constant")
    require(theorem.get("unit_constant_interface") == "REFUTED_SCOPED", "unit interface")
    firewall = data.get("firewall")
    require(firewall.get("arithmetic_advance") == "NO", "arithmetic firewall")
    require(firewall.get("fixed_atom_credit") == 0, "atom firewall")
    require(firewall.get("l2") == "NONE", "L2 firewall")
    require(firewall.get("full_gate_b") == "OPEN", "Gate B firewall")
    require(firewall.get("strict_1_over_400") == "UNPAID", "strict firewall")
    source = data.get("source_clock")
    stress = data.get("collision_stress_clock")
    require(source.get("clock") == "source_surrogate", "source clock")
    require(stress.get("clock") == "collision_stress", "stress clock")
    require(len(source.get("records")) == 9, "source record count")
    require(len(stress.get("records")) == 5, "stress record count")
    require(all(record.get("sharp_interface_holds") is True for record in source["records"]), "source sharp")
    require(all(record.get("sharp_interface_holds") is True for record in stress["records"]), "stress sharp")
    require(all(record.get("sharp_ratio") == "1" for record in stress["records"]), "stress equality")
    require(all(record.get("unit_interface_holds") is False for record in stress["records"]), "stress unit refutation")
    require(data.get("checks") and all(type(value) is bool and value for value in data["checks"].values()), "check flags")
    aligned = data.get("aligned_fixture")
    require(aligned[1].get("unit_interface_refuted") is True, "aligned adversary")
    require(aligned[1].get("sharp_equality") is True, "aligned sharpness")


def check_subchecks() -> None:
    producer = run([
        sys.executable,
        "-B",
        str(PROJECT / "experiments/run_certificate.py"),
        "--check",
    ])
    require("TPC224_CERTIFICATE=PASS" in producer, "producer check")
    outputs = [
        run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")]),
        run([sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")]),
    ]
    require(outputs[0] == outputs[1], "normal/optimized independent output differs")
    require("TPC224_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/boundary_adversary.py")])
    require("TPC224_BOUNDARY_ADVERSARY=PASS" in adversary, "boundary adversary")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           5" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in (
        "Literal Two-Channel Compatibility",
        "Liang Wang",
        "smallest universal coefficient",
        "unit-factor interface",
        "TPC-223",
        "References",
    ):
        require(phrase in text, f"missing PDF phrase: {phrase}")
    fonts = run(["pdffonts", str(pdf)])
    for line in fonts.splitlines()[2:]:
        if line.strip():
            fields = line.split()
            require(len(fields) >= 4 and fields[-4] == "yes", "unembedded font")


def main() -> int:
    try:
        check_layout()
        check_certificate()
        check_subchecks()
        check_pdf()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"TPC224_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC224_BRIDGE_CHECK=PASS")
    print("source_scales=9")
    print("stress_scales=5")
    print("sharp_constant=PJ/(P+J)")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
