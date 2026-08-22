#!/usr/bin/env python3
"""Fail-closed release checker for TPC-225."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-225-cutoff-one-shared-clock-obstruction"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_cutoff_one_shared_clock_obstruction.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "651cd1028ccdb1554aef5da635d65b3fb069cf0e34857637c8f7a80614691830"


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


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CheckFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


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
        "code/cutoff_one_obstruction.py",
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
        "TPC225_CUTOFF_ONE = PROVED_EXACT",
        "TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT",
        "TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED",
        "TPC225_ARITHMETIC_ADVANCE = NO",
    ):
        require(anchor in proof_text, f"missing proof anchor: {anchor}")
    readme = (PROJECT / "README.md").read_text()
    require("Liang Wang" in readme, "author lock missing")
    require("Huazhong University of Science and Technology" in readme, "affiliation lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
    require(data.get("schema") == "tpc225-cutoff-one-shared-clock-obstruction-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level")
    require(data.get("author") == "Liang Wang", "author")
    require(data.get("affiliation") == "Huazhong University of Science and Technology", "affiliation")
    theorem = data.get("theorem")
    require(theorem.get("clock") == "x=Q^3, H=4Q^2, h=4Q", "clock")
    require(theorem.get("cutoff") == "floor(hq/H)=1", "cutoff")
    require(theorem.get("support_disjointness") == "PROVED_EXACT", "support")
    require(theorem.get("ap_equals_diagonal") == "PROVED_EXACT", "AP identity")
    require(theorem.get("all_equals_polarized") == "PROVED_EXACT", "full identity")
    require(theorem.get("positive_ap_saving_on_clock") == "REFUTED_SCOPED", "AP obstruction")
    firewall = data.get("firewall")
    require(firewall.get("arithmetic_advance") == "NO", "arithmetic firewall")
    require(firewall.get("fixed_atom_credit") == 0, "atom firewall")
    require(firewall.get("l2") == "NONE", "L2 firewall")
    require(firewall.get("full_gate_b") == "OPEN", "Gate B firewall")
    require(firewall.get("strict_1_over_400") == "UNPAID", "strict firewall")
    affine = data["affine_clock"]["records"]
    aligned = data["boundary_profiles"]["aligned_records"]
    balanced = data["boundary_profiles"]["balanced_records"]
    require(len(affine) == 9, "affine record count")
    require(len(aligned) == 7 and len(balanced) == 7, "boundary record counts")
    all_records = affine + aligned + balanced
    require(all(record.get("cutoff_one") is True for record in all_records), "cutoff records")
    require(all(record.get("support_disjoint") is True for record in all_records), "support records")
    require(all(record.get("AP_over_diag") == "1" for record in all_records), "AP records")
    require(all(record.get("all_over_pol") in ("1", "UNDEFINED") for record in all_records), "full records")
    require(all(record.get("E_pol") == "0" for record in balanced), "balanced cancellation")
    require(all(record.get("E_diag") != "0" for record in balanced), "balanced diagonal")
    checks = data.get("checks")
    require(checks and all(type(value) is bool and value for value in checks.values()), "check flags")


def check_subchecks() -> None:
    producer = run([
        sys.executable,
        "-B",
        str(PROJECT / "experiments/run_certificate.py"),
        "--check",
    ])
    require("TPC225_CERTIFICATE=PASS" in producer, "producer check")
    outputs = [
        run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")]),
        run([sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")]),
    ]
    require(outputs[0] == outputs[1], "normal/optimized independent output differs")
    require("TPC225_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/boundary_adversary.py")])
    require("TPC225_BOUNDARY_ADVERSARY=PASS" in adversary, "boundary adversary")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           5" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in (
        "Cutoff-One Shared-Clock Obstruction",
        "Liang Wang",
        "E_AP = E_diag",
        "E_all = E_pol",
        "REFUTED_SCOPED",
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
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError, KeyError) as error:
        print(f"TPC225_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC225_BRIDGE_CHECK=PASS")
    print("affine_scales=9")
    print("boundary_profile_scales=14")
    print("ap_identity=E_AP_EQUALS_E_DIAG")
    print("full_identity=E_ALL_EQUALS_E_POL")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
