#!/usr/bin/env python3
"""Fail-closed release checker for TPC-231."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-231-finite-resonance-sieve-obstruction"
PROOF = ROOT / "research/tpc-big-road/bridge_b_finite_resonance_sieve_obstruction.md"
CERTIFICATE = PROJECT / "results/certificate.json"
PROOF_SHA256 = "24213e7258472d94f9e904a10b26b9ff675da3756f33cc08e2b5baf78fcc2582"


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
        check=False,
    )
    require(result.returncode == 0, f"command failed: {command}")
    require(result.stderr == "", f"unexpected stderr: {command}")
    return result.stdout


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key")
        output[key] = value
    return output


def check_layout() -> None:
    required = (
        ".gitignore",
        "README.md",
        "PAPER_PLAN.md",
        "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md",
        "code/finite_resonance_sieve.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/sieve_adversary.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
        "paper/main.tex",
        "paper/references.bib",
        "paper/main.pdf",
        "paper/paper.pdf",
        "paper/sections/0_abstract.tex",
        "paper/sections/1_introduction.tex",
        "paper/sections/2_local_arithmetic.tex",
        "paper/sections/3_selberg_bound.tex",
        "paper/sections/4_finite_families.tex",
        "paper/sections/5_certificate.tex",
        "paper/sections/6_conclusion.tex",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing {relative}")
    require((PROJECT / "paper/main.pdf").read_bytes() == (PROJECT / "paper/paper.pdf").read_bytes(), "PDF mismatch")
    require(PROOF_SHA256 != "TO_BE_FILLED" and normalized_sha256(PROOF) == PROOF_SHA256, "proof hash")
    proof_text = PROOF.read_text(encoding="utf-8")
    for claim in (
        "TPC231_3716_SELBERG_UPPER_BOUND = PROVED_SOURCE_BACKED",
        "TPC231_3716_EDGE_DENSITY_ZERO = PROVED_ASYMPTOTIC",
        "TPC231_FIRST_PRIMITIVE_3_7_FIXED_SAVING = STOP_SCOPED",
        "TPC231_ARITHMETIC_ADVANCE = NO",
        "TPC231_L2 = NONE",
        "TPC231_ROUND2_CLUE = TEST_GROWING_RESONANCE_DEPTH_OR_RETURN_TO_THE_ACTUAL_V59_SOURCE_MASS_CROSSWALK",
    ):
        require(claim in proof_text, f"missing proof claim: {claim}")
    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    require("Liang Wang" in readme and "Huazhong University of Science and Technology" in readme, "author metadata")
    source_lock = (PROJECT / "notes/source_lock.md").read_text(encoding="utf-8")
    require("Halberstam" in source_lock and "Iwaniec" in source_lock and "Selberg" in source_lock, "source lock")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    require(data["schema"] == "tpc231-finite-resonance-sieve-obstruction-v1", "schema")
    require(data["status"] == "PASS" and data["claim_level"] == "PROVED_ARITHMETIC_OBSTRUCTION_L1", "status")
    theorem = data["theorem"]
    require(theorem["prime_shell_density"].endswith("-> 0"), "density theorem")
    require(theorem["finite_family_extension"].startswith("every fixed finite"), "finite family")
    local = data["local_density"]
    require(local["q25"]["determinant"] == 400, "Q25 determinant")
    require(local["q25_exceptional_correction"] == "4/3", "Q25 correction")
    scan = data["finite_scan"]
    require(scan["Q_max"] == 32768 and scan["scales_checked"] == 32761, "scan domain")
    require(scan["total_edges"] == 568308 and scan["total_prime_rows"] == 52199509, "scan totals")
    require(scan["scan_sha256"] == "b6ca54f2d09c0403fe0f44371f8c600c67f7f9709062a22c120503e0277836e0", "scan digest")
    checks = data["checks"]
    require(type(checks) is dict and all(type(value) is bool and value for value in checks.values()), "certificate checks")
    firewall = data["firewall"]
    require(firewall["first_primitive_3_7_fixed_saving"] == "STOP_SCOPED", "scoped stop")
    require(firewall["arithmetic_advance"] == "NO" and firewall["arithmetic_cancellation"] == "NONE", "arithmetic firewall")
    require(type(firewall["fixed_atom_credit"]) is int and firewall["fixed_atom_credit"] == 0, "atom credit")
    require(firewall["L2"] == "NONE" and firewall["full_gate_b"] == "OPEN", "gate firewall")


def check_subprocesses() -> None:
    producer = run([sys.executable, "-B", str(PROJECT / "experiments/run_certificate.py"), "--check"])
    require("TPC231_CERTIFICATE=PASS" in producer, "producer")
    normal = run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")])
    optimized = run([sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")])
    require(normal == optimized and "TPC231_INDEPENDENT_CHECK=PASS" in normal, "independent optimized parity")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/sieve_adversary.py")])
    require("TPC231_SIEVE_ADVERSARY=PASS" in adversary, "adversary")


def main() -> int:
    try:
        check_layout()
        check_certificate()
        check_subprocesses()
    except (OSError, ValueError, json.JSONDecodeError, CheckFailure) as error:
        print(f"TPC231_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC231_BRIDGE_CHECK=PASS")
    print("claim_level=PROVED_ARITHMETIC_OBSTRUCTION_L1")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
