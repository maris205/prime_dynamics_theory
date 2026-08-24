#!/usr/bin/env python3
"""Fail-closed release checker for TPC-226."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-226-first-primitive-collision-transition"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_first_primitive_collision_transition.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "a07675154f0d78f1fab1541624d38f6e45715da38467d8fcbe0a3c0f0a8fa5bc"


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def run(command: list[str]) -> str:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
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
        "paper/sections/0_abstract.tex",
        "paper/sections/1_introduction.tex",
        "paper/sections/2_setup.tex",
        "paper/sections/3_collision_transition.tex",
        "paper/sections/4_signed_energy.tex",
        "paper/sections/5_certification.tex",
        "paper/sections/6_conclusion.tex",
        "paper/sections/A_case_table.tex",
        "code/primitive_collision_transition.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/nonprimitive_adversary.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing project file: {relative}")
    require(
        (PROJECT / "paper/main.pdf").read_bytes()
        == (PROJECT / "paper/paper.pdf").read_bytes(),
        "PDF copies differ",
    )
    require(PROOF_SHA256 != "TO_BE_FILLED", "proof hash not frozen")
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash mismatch")
    proof_text = PROOF.read_text()
    for anchor in (
        "TPC226_L_LE_3_DISJOINTNESS = PROVED_EXACT",
        "TPC226_L4_RESONANCE_CLASSIFICATION = PROVED_EXACT",
        "TPC226_UNIFORM_PROFILE_INDEPENDENT_SAVING = REFUTED_SCOPED",
        "TPC226_ARITHMETIC_ADVANCE = NO",
        "TPC226_ROUND2_CLUE = SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING",
    ):
        require(anchor in proof_text, f"missing proof anchor: {anchor}")
    readme = (PROJECT / "README.md").read_text()
    require("Liang Wang" in readme, "author lock missing")
    require(
        "Huazhong University of Science and Technology" in readme,
        "affiliation lock missing",
    )


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
    require(data.get("schema") == "tpc226-first-primitive-collision-transition-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level")
    require(data.get("author") == "Liang Wang", "author")
    require(
        data.get("affiliation") == "Huazhong University of Science and Technology",
        "affiliation",
    )

    theorem = data.get("theorem")
    require(type(theorem) is dict, "theorem object")
    require(theorem.get("clock_family") == "x=Q^3, H=4Q^2, h_L=4LQ", "clock")
    require(theorem.get("primitive_support") == "gcd(m,h_L)=1", "primitive support")
    require(theorem.get("L_le_3_disjointness") == "PROVED_EXACT", "small dilation theorem")
    require(theorem.get("first_primitive_collision_dilation") == 4, "first dilation")
    require(
        theorem.get("L4_resonance") == "7p+3r=16Q with multipliers +/-3 and -/+7",
        "resonance theorem",
    )
    require(
        theorem.get("uniform_profile_independent_saving") == "REFUTED_SCOPED",
        "uniform-saving obstruction",
    )

    boundary = data.get("boundary_scan")
    require(type(boundary) is dict, "boundary object")
    require(boundary.get("Q_min") == 8 and boundary.get("Q_max") == 512, "boundary range")
    require(boundary.get("scales_checked") == 505, "boundary count")
    require(
        [boundary.get(f"L{index}_collision_scales") for index in range(1, 4)]
        == [0, 0, 0],
        "small-dilation collision census",
    )
    require(boundary.get("L4_collision_scales") == 182, "L4 collision scales")
    require(boundary.get("L4_total_resonances") == 235, "L4 resonance total")
    require(boundary.get("L4_first_collision_Q") == 25, "first collision")
    require(boundary.get("L4_maximum_resonances") == 4, "maximum resonance count")
    require(boundary.get("L4_maximum_Q") == 502, "maximum-resonance scale")
    require(
        boundary.get("classification_sha256")
        == "fe678364061af5b70411105e05344e51fbc8bd0c2418172d67cedaa068c58d8d",
        "classification digest",
    )

    records = data.get("records")
    require(type(records) is dict, "record object")
    require(set(records) == {"aligned", "affine", "balanced_sign"}, "record modes")
    require(all(type(rows) is list and len(rows) == 10 for rows in records.values()), "record counts")
    for mode, rows in records.items():
        for row in rows:
            require(row.get("mode") == mode, "record mode")
            require(row.get("collision_pairs", 0) > 0, "empty witness record")
            correction = Fraction(row["AP_minus_diag"])
            if mode in {"aligned", "affine"}:
                require(correction > 0, "amplifying record sign")
            else:
                require(correction < 0, "balanced record sign")
                require(row.get("E_pol") == "0" and row.get("E_all") == "0", "packet cancellation")

    q25 = data.get("Q25_exact")
    require(type(q25) is dict, "Q25 object")
    require(q25.get("aligned_AP_over_diag") == "15/13", "Q25 aligned ratio")
    require(
        q25.get("affine_AP_over_diag")
        == "14610396266802411880605/12679409642889136447511",
        "Q25 affine ratio",
    )
    require(q25.get("balanced_sign_AP_over_diag") == "11/13", "Q25 sign ratio")
    require(q25.get("balanced_sign_E_pol") == "0", "Q25 polarized cancellation")
    require(q25.get("balanced_sign_E_all") == "0", "Q25 total cancellation")

    firewall = data.get("firewall")
    require(type(firewall) is dict, "firewall object")
    require(firewall.get("dilated_clock_family") == "MODELING_CHOICE", "clock firewall")
    require(firewall.get("V46_profile_transfer") == "OPEN", "transfer firewall")
    require(firewall.get("arithmetic_advance") == "NO", "arithmetic firewall")
    require(firewall.get("arithmetic_cancellation") == "NONE", "cancellation firewall")
    require(firewall.get("fixed_atom_credit") == 0, "atom firewall")
    require(firewall.get("L2") == "NONE", "L2 firewall")
    require(firewall.get("full_gate_b") == "OPEN", "Gate B firewall")
    require(firewall.get("strict_1_over_400") == "UNPAID", "strict firewall")
    checks = data.get("checks")
    require(checks and all(type(value) is bool and value for value in checks.values()), "check flags")


def check_subchecks() -> None:
    producer = run([
        sys.executable,
        "-B",
        str(PROJECT / "experiments/run_certificate.py"),
        "--check",
    ])
    require("TPC226_CERTIFICATE=PASS" in producer, "producer check")
    outputs = [
        run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")]),
        run([sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")]),
    ]
    require(outputs[0] == outputs[1], "normal/optimized independent output differs")
    require("TPC226_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check")
    adversary = run([
        sys.executable,
        "-B",
        str(PROJECT / "experiments/nonprimitive_adversary.py"),
    ])
    require("TPC226_NONPRIMITIVE_ADVERSARY=PASS" in adversary, "primitive adversary")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           5" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in (
        "First Primitive-Collision Transition",
        "Liang Wang",
        "7p + 3r = 16Q",
        "15/13",
        "11/13",
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
    except (
        CheckFailure,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
        KeyError,
        ValueError,
        ZeroDivisionError,
    ) as error:
        print(f"TPC226_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC226_BRIDGE_CHECK=PASS")
    print("classification_scales=505")
    print("profile_records=30")
    print("first_collision_Q=25")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
