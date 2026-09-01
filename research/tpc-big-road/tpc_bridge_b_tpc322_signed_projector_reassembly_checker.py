#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-322."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-322-signed-projector-reassembly"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc322_signed_projector_reassembly.md"
PRODUCER = PROJECT / "code/tpc322_signed_projector_reassembly.py"
INDEPENDENT = PROJECT / "experiments/tpc322_independent_checker.py"
STRESS = PROJECT / "experiments/tpc322_reassembly_stress.py"
CERTIFICATE = PROJECT / "results/tpc322_certificate.json"
PARENT = ROOT / "papers/tpc-321-cross-shell-profile-stability/results/tpc321_certificate.json"
PARENT_SHA256 = "f7048edce7260bceb14acc674311ce0268fb5ae4fdb9914edc0138a5cb7cc6be"

# Filled after every release artifact and bridge text is final.
PRODUCER_SHA256 = "d54ad81251a688edc9ddae0cec304ff01834dc61c8aebcf22b7edeb753e90429"
INDEPENDENT_SHA256 = "45677e50ca9e55d354cf7bb851300e4ee5fab3f3446bac257fa55d3e20b5e9c6"
STRESS_SHA256 = "0037da51981c1da7e442841d101ece6d0917009da0aad1d10497bc25bf43f548"
CERTIFICATE_SHA256 = "4961b34ebb755e8216d4fbc6d9d6d59781c9a8203c8687b5990385c7e0a57b0c"
BRIDGE_SHA256 = "dc33f3ed0d0fed5fc2c93b91208d3346e1fa9437defa4783d4e791e2b16989e9"

STATUS = "NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS"
SCHEMA = "TPC322_SIGNED_PROJECTOR_REASSEMBLY_V1"
REQUIRED = (
    ".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
    "PROOF_PACKAGE.md", "code/tpc322_signed_projector_reassembly.py",
    "experiments/tpc322_independent_checker.py",
    "experiments/tpc322_reassembly_stress.py",
    "results/tpc322_certificate.json", "notes/theorem_ledger.md",
    "notes/claim_firewall.md", "notes/computational_protocol.md",
    "notes/citation_verification.md", "notes/route_evaluation.md",
    "paper/main.tex", "paper/references.bib", "paper/main.pdf",
    "paper/paper.pdf", "paper/compile.log")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(script), "--check"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=PROJECT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed: " + script.name)
    return result.stdout


def check_files() -> None:
    for relative in REQUIRED:
        need((PROJECT / relative).is_file(), "missing artifact: " + relative)
    for path, expected, label in (
            (PRODUCER, PRODUCER_SHA256, "producer"),
            (INDEPENDENT, INDEPENDENT_SHA256, "independent"),
            (STRESS, STRESS_SHA256, "stress"),
            (CERTIFICATE, CERTIFICATE_SHA256, "certificate"),
            (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(not expected.startswith("__"), label + " hash is unsealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PARENT.read_bytes()) == PARENT_SHA256, "parent provenance")
    log = (PROJECT / "paper/compile.log").read_text(encoding="utf-8")
    for marker in ("LaTeX Warning", "undefined", "LaTeX Error",
                   "Overfull", "Underfull"):
        need(marker not in log, "compile diagnostic: " + marker)
    need((PROJECT / "paper/main.pdf").read_bytes() ==
         (PROJECT / "paper/paper.pdf").read_bytes(), "PDF alias")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document["payload"]
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload digest")
    need(payload["parent_lock"]["certificate_sha256"] == PARENT_SHA256,
         "payload parent lock")
    protocol = payload["protocol"]
    need(protocol["source_scales"] == [640, 1280, 2560] and
         protocol["Q_anchors"] == [24, 36, 54, 80] and
         protocol["kernel_exponents"] == [1, 2] and
         protocol["height"] == 66, "protocol")
    audit = payload["finite_audit"]
    need(audit["rows"] == 24 and audit["minimum_sign_below_one"] == 24 and
         audit["maximum_sign_above_one"] == 24 and
         audit["pattern_counts"]["all_plus"] ==
         {"below_one": 3, "above_one": 21} and
         audit["pattern_counts"]["alternating_index"] ==
         {"below_one": 21, "above_one": 3} and
         audit["fixed_power_credit"] == 0, "finite audit")
    firewall = payload["claim_firewall"]
    need(firewall["TPC322_SIGNED_PROJECTOR_IDENTITY"] ==
         "PROVED_EXACT_FINITE" and
         firewall["TPC322_OPERATOR_REASSEMBLY_ATLAS"] ==
         "NUMERICALLY_CERTIFIED_FINITE_24_ROWS" and
         firewall["TPC322_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC322_FULL_GATE_B"] == "OPEN" and
         firewall["TPC322_TWIN_PRIME_RESULT"] == "NONE", "firewall")


def main() -> int:
    try:
        check_files()
        check_certificate()
        outputs = []
        for optimized in (False, True):
            outputs.append((run(PRODUCER, optimized),
                            run(INDEPENDENT, optimized),
                            run(STRESS, optimized)))
        need(outputs[0] == outputs[1], "normal/optimized output mismatch")
        print("TPC322_BRIDGE_CHECK=PASS rows=24 min_sign=24/24 "
              "max_sign=24/24 all_plus=3/21 alternating=21/3")
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC322_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
