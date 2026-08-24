#!/usr/bin/env python3
"""Fail-closed release checker for TPC-227."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-227-packet-profile-axis-separation"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_packet_profile_axis_separation.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "e7cf1f145332c37901d5937a10aef4be51f70c697a77079df7619a74d2c28131"


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
        "paper/sections/2_source_typing.tex",
        "paper/sections/3_gram_criterion.tex",
        "paper/sections/4_collision_witness.tex",
        "paper/sections/5_certification.tex",
        "paper/sections/6_conclusion.tex",
        "code/axis_separation.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/axis_mutation_adversary.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing project file: {relative}")
    require((PROJECT / "paper/main.pdf").read_bytes() == (PROJECT / "paper/paper.pdf").read_bytes(), "PDF copies differ")
    require(PROOF_SHA256 != "TO_BE_FILLED", "proof hash not frozen")
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash mismatch")
    proof = PROOF.read_text()
    for anchor in (
        "TPC227_FOUR_GRAM_CRITERION = PROVED_EXACT",
        "TPC227_Q25_ROW_SIGN_GRAM_MISMATCH = PROVED_EXACT",
        "TPC227_TPC226_AUTOMATIC_SOURCE_TRANSFER = REFUTED_SCOPED",
        "TPC227_ARITHMETIC_ADVANCE = NO",
        "TPC227_ROUND2_CLUE = KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON",
    ):
        require(anchor in proof, f"missing proof anchor: {anchor}")
    readme = (PROJECT / "README.md").read_text()
    require("Liang Wang" in readme, "author lock")
    require("Huazhong University of Science and Technology" in readme, "affiliation lock")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
    require(data.get("schema") == "tpc227-packet-profile-axis-separation-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level")
    require(data.get("author") == "Liang Wang", "author")
    require(data.get("affiliation") == "Huazhong University of Science and Technology", "affiliation")
    theorem = data.get("theorem")
    require(type(theorem) is dict, "theorem")
    require(theorem.get("physical_V59_packet_axis") == "a^(j)=beta+i^j w", "packet axis")
    require(theorem.get("physical_V59_profile_axis") == "one common psi_+(v)", "profile axis")
    require(theorem.get("global_packet_phase") == "GRAM_INVISIBLE", "phase")
    block = data.get("q25_resonance_block")
    require(type(block) is dict, "block")
    require(block.get("off_diagonal_difference") == "-1/80000", "witness difference")
    require(Fraction(block["off_diagonal_difference"]) == Fraction(-1, 80000), "fraction witness")
    fixtures = data.get("fixtures")
    require(type(fixtures) is dict and len(fixtures) == 6, "fixtures")
    require(fixtures["common_physical"]["compatible_with_target"] is True, "positive control")
    require(fixtures["packet_global_signs"]["compatible_with_target"] is True, "sign control")
    for key in ("row_dependent_odd_sign", "alternating_scale", "fully_unequal_scale", "mixed_row_profile"):
        require(fixtures[key]["compatible_with_target"] is False, f"negative control: {key}")
    firewall = data.get("firewall")
    require(type(firewall) is dict, "firewall")
    require(firewall.get("arithmetic_advance") == "NO", "arithmetic")
    require(firewall.get("fixed_atom_credit") == 0, "atom")
    require(firewall.get("L2") == "NONE", "L2")
    require(firewall.get("strict_1_over_400") == "UNPAID", "strict")
    checks = data.get("checks")
    require(type(checks) is dict and all(type(value) is bool and value for value in checks.values()), "checks")


def check_subchecks() -> None:
    producer = run([sys.executable, "-B", str(PROJECT / "experiments/run_certificate.py"), "--check"])
    require("TPC227_CERTIFICATE=PASS" in producer, "producer")
    normal = run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")])
    optimized = run([sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")])
    require(normal == optimized, "normal/optimized checker mismatch")
    require("TPC227_INDEPENDENT_CHECK=PASS" in normal, "independent")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/axis_mutation_adversary.py")])
    require("TPC227_AXIS_ADVERSARY=PASS" in adversary, "adversary")


def main() -> int:
    try:
        check_layout()
        check_certificate()
        check_subchecks()
    except (OSError, ValueError, CheckFailure, json.JSONDecodeError) as error:
        print(f"TPC227_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC227_BRIDGE_CHECK=PASS")
    print("claim_level=PROVED_STRUCTURAL_L1")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
