#!/usr/bin/env python3
"""Fail-closed release checker for TPC-228."""

from __future__ import annotations

import hashlib, json, os, subprocess, sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-228-source-native-polarized-collision-compiler"
PROOF = ROOT / "research/tpc-big-road/bridge_b_source_native_polarized_collision_compiler.md"
CERTIFICATE = PROJECT / "results/certificate.json"
PROOF_SHA256 = "99aab518c2d659e9cb20c50b24fdc6f80f7983876d6b176bc078bbaa12bfeae6"


class CheckFailure(RuntimeError): pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition: raise CheckFailure(message)


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def run(command: list[str]) -> str:
    env = os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0, f"command failed: {' '.join(command)}")
    require(result.stderr == "", f"stderr: {' '.join(command)}")
    return result.stdout


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result: raise CheckFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_layout() -> None:
    required = (
        "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
        "paper/main.tex", "paper/references.bib", "paper/main.pdf", "paper/paper.pdf",
        "paper/sections/0_abstract.tex", "paper/sections/1_introduction.tex",
        "paper/sections/2_common_profile.tex", "paper/sections/3_compiler.tex",
        "paper/sections/4_q25_block.tex", "paper/sections/5_certification.tex",
        "paper/sections/6_conclusion.tex", "code/source_native_compiler.py",
        "experiments/run_certificate.py", "experiments/independent_checker.py",
        "experiments/compiler_adversary.py", "results/certificate.json",
        "notes/theorem_ledger.md", "notes/source_lock.md", "notes/route_evaluation.md",
    )
    for relative in required: require((PROJECT / relative).is_file(), f"missing: {relative}")
    require((PROJECT / "paper/main.pdf").read_bytes() == (PROJECT / "paper/paper.pdf").read_bytes(), "PDF mismatch")
    require(PROOF_SHA256 != "TO_BE_FILLED" and normalized_sha256(PROOF) == PROOF_SHA256, "proof hash")
    proof = PROOF.read_text()
    for anchor in (
        "TPC228_POLARIZED_AP_MINUS_DIAGONAL_COMPILER = PROVED_EXACT",
        "TPC228_Q25_3_7_SOURCE_BLOCK = PROVED_EXACT_FINITE",
        "TPC228_ARITHMETIC_ADVANCE = NO",
        "TPC228_ROUND2_CLUE = ANALYZE_THE_SOURCE_NATIVE_3_7_COLLISION_GRAPH_AS_EXACT_TWO_BY_TWO_BLOCKS",
    ): require(anchor in proof, f"proof anchor: {anchor}")
    readme = (PROJECT / "README.md").read_text()
    require("Liang Wang" in readme and "Huazhong University of Science and Technology" in readme, "author")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(), object_pairs_hook=no_duplicates)
    require(data.get("schema") == "tpc228-source-native-polarized-collision-compiler-v1", "schema")
    require(data.get("status") == "PASS" and data.get("claim_level") == "PROVED_STRUCTURAL_L1", "status")
    theorem = data.get("theorem"); require(type(theorem) is dict, "theorem")
    require(theorem.get("phase_axis") == "SOURCE_SEQUENCE", "phase axis")
    require(theorem.get("profile_axis") == "COMMON_TRANSFORM", "profile axis")
    fixtures = data.get("fixtures"); require(type(fixtures) is dict and len(fixtures) == 5, "fixtures")
    expected = {"positive": Fraction(1,40000), "negative": Fraction(-1,40000), "row_cancellation": Fraction(0), "directed": Fraction(1,80000), "one_coordinate": Fraction(1,160000)}
    for name, value in expected.items():
        require(Fraction(fixtures[name]["four_phase_value"]) == value, f"fixture {name}")
        require(fixtures[name]["four_phase_value"] == fixtures[name]["direct_collision_value"], f"compiler {name}")
    firewall = data.get("firewall"); require(type(firewall) is dict, "firewall")
    require(firewall.get("arithmetic_advance") == "NO" and firewall.get("fixed_atom_credit") == 0, "claim firewall")
    require(firewall.get("L2") == "NONE" and firewall.get("strict_1_over_400") == "UNPAID", "endpoint firewall")


def check_subchecks() -> None:
    producer = run([sys.executable, "-B", str(PROJECT / "experiments/run_certificate.py"), "--check"])
    require("TPC228_CERTIFICATE=PASS" in producer, "producer")
    normal = run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")])
    optimized = run([sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")])
    require(normal == optimized and "TPC228_INDEPENDENT_CHECK=PASS" in normal, "independent")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/compiler_adversary.py")])
    require("TPC228_COMPILER_ADVERSARY=PASS" in adversary, "adversary")


def main() -> int:
    try: check_layout(); check_certificate(); check_subchecks()
    except (OSError, ValueError, json.JSONDecodeError, CheckFailure) as error:
        print(f"TPC228_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr); return 1
    print("TPC228_BRIDGE_CHECK=PASS")
    print("claim_level=PROVED_STRUCTURAL_L1")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__": raise SystemExit(main())
