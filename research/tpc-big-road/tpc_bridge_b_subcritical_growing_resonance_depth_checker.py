#!/usr/bin/env python3
"""Fail-closed release checker for TPC-232."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-232-subcritical-growing-resonance-depth"
PROOF = ROOT / "research/tpc-big-road/bridge_b_subcritical_growing_resonance_depth.md"
CERTIFICATE = PROJECT / "results/certificate.json"
PROOF_SHA256 = "8ab0c890a4533bcfa8bb787011f31a329be933895e1fbf579e2bff2e7ec69838"


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
    output: dict[str, object] = {}
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
        "code/growing_resonance_depth.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/depth_adversary.py",
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
        "paper/sections/2_collision_geometry.tex",
        "paper/sections/3_uniform_sieve.tex",
        "paper/sections/4_depth_threshold.tex",
        "paper/sections/5_certificate.tex",
        "paper/sections/6_conclusion.tex",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing {relative}")
    require(
        (PROJECT / "paper/main.pdf").read_bytes()
        == (PROJECT / "paper/paper.pdf").read_bytes(),
        "PDF mismatch",
    )
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash")
    proof_text = PROOF.read_text(encoding="utf-8")
    for claim in (
        "TPC232_UNIFORM_POLYLOG_DEPTH_SIEVE = PROVED_SOURCE_BACKED",
        "TPC232_SUBCRITICAL_DEPTH_DENSITY_ZERO = PROVED_ASYMPTOTIC",
        "TPC232_SUBCRITICAL_FIXED_SAVING = STOP_SCOPED",
        "TPC232_DILATED_CLOCK = MODELING_CHOICE",
        "TPC232_ARITHMETIC_ADVANCE = NO",
        "TPC232_L2 = NONE",
        "TPC232_ROUND2_CLUE = TEST_CRITICAL_DEPTH_CLOCK_MASS_AND_DEGREE_BEFORE_V59_ATTACHMENT",
    ):
        require(claim in proof_text, f"missing proof claim: {claim}")
    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    require(
        "Liang Wang" in readme
        and "Huazhong University of Science and Technology" in readme,
        "author metadata",
    )
    source = (PROJECT / "notes/source_lock.md").read_text(encoding="utf-8")
    require("Selberg" in source and "MODELING_CHOICE" in source, "source firewall")


def check_certificate() -> None:
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
    require(data["schema"] == "tpc232-subcritical-growing-resonance-depth-v1", "schema")
    require(
        data["status"] == "PASS"
        and data["claim_level"] == "PROVED_ARITHMETIC_OBSTRUCTION_L1",
        "status",
    )
    theorem = data["theorem"]
    require(theorem["incidence_bound"].startswith("C_L(Q) <<_A"), "incidence theorem")
    require(theorem["subcritical_stop"].endswith("C_L(Q)/P(Q)->0"), "depth theorem")
    scan = data["finite_scan"]
    require(
        type(scan["record_count"]) is int and scan["record_count"] == 19,
        "record count",
    )
    require(
        scan["scan_sha256"]
        == "fd4023281dc31c15c23d15ad66e49629565a9918ea36962a7705492bcff8dd5c",
        "scan digest",
    )
    first = scan["records"][0]
    last = scan["records"][-1]
    require(
        first["Q"] == 25
        and first["L"] == 4
        and first["resonance_channels"] == 1,
        "Q25 anchor",
    )
    require(
        last["Q"] == 3203
        and last["L"] == 512
        and last["resonance_channels"] == 1623
        and last["incident_rows"] == 338
        and last["max_degree"] == 28,
        "terminal scan anchor",
    )
    checks = data["checks"]
    require(
        type(checks) is dict
        and all(type(value) is bool and value for value in checks.values()),
        "certificate checks",
    )
    firewall = data["firewall"]
    require(firewall["dilated_clock"] == "MODELING_CHOICE", "clock firewall")
    require(firewall["critical_depth_sufficiency"] == "OPEN", "critical firewall")
    require(
        firewall["arithmetic_advance"] == "NO"
        and firewall["arithmetic_cancellation"] == "NONE",
        "arithmetic firewall",
    )
    require(
        type(firewall["fixed_atom_credit"]) is int
        and firewall["fixed_atom_credit"] == 0,
        "fixed atom",
    )
    require(firewall["L2"] == "NONE" and firewall["full_gate_b"] == "OPEN", "gate")


def check_subprocesses() -> None:
    producer = run(
        [sys.executable, "-B", str(PROJECT / "experiments/run_certificate.py"), "--check"]
    )
    require("TPC232_CERTIFICATE=PASS" in producer, "producer")
    normal = run([sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py")])
    optimized = run(
        [sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py")]
    )
    require(
        normal == optimized and "TPC232_INDEPENDENT_CHECK=PASS" in normal,
        "independent optimized parity",
    )
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/depth_adversary.py")])
    require("TPC232_DEPTH_ADVERSARY=PASS" in adversary, "adversary")


def main() -> int:
    try:
        check_layout()
        check_certificate()
        check_subprocesses()
    except (OSError, ValueError, KeyError, json.JSONDecodeError, CheckFailure) as error:
        print(f"TPC232_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC232_BRIDGE_CHECK=PASS")
    print("claim_level=PROVED_ARITHMETIC_OBSTRUCTION_L1")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
