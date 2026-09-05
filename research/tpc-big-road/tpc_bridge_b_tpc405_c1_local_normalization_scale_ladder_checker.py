#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-405 exact scale ladder."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-405-c1-local-normalization-scale-ladder"
FILES = {
    "producer": PROJECT / "code/tpc405_c1_local_normalization_scale_ladder.py",
    "independent": PROJECT / "experiments/tpc405_independent_checker.py",
    "stress": PROJECT / "experiments/tpc405_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc405_certificate.json",
    "main_tex": PROJECT / "paper/main.tex",
    "main_pdf": PROJECT / "paper/main.pdf",
    "pdf": PROJECT / "paper/paper.pdf",
    "log": PROJECT / "paper/compile.log",
    "readme": PROJECT / "README.md",
    "plan": PROJECT / "PAPER_PLAN.md",
    "derivation": PROJECT / "DERIVATION_PACKAGE.md",
    "proof": PROJECT / "PROOF_PACKAGE.md",
    "claim": PROJECT / "notes/claim_firewall.md",
    "route": PROJECT / "notes/route_evaluation.md",
    "protocol": PROJECT / "notes/computational_protocol.md",
    "theorem": PROJECT / "notes/theorem_ledger.md",
    "ledger": ROOT / "research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md",
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc405_c1_local_normalization_scale_ladder.md",
}

# Filled from the finalized, LF-normalized release artifacts.
LOCKS = {
    "producer": "564de4fad656bc7be16a7ab20a985025a98fb678b5a33410e89a32a80acbe734",
    "independent": "dbedf3d1c6abd98980fcb56580cf6faaa7419d71b3120f0441329d098967e0a1",
    "stress": "db40dd54441a1a2596523ff76aa2b13c7407ca7a1fc10bd15e8583bfce54cc23",
    "certificate": "42ef38b28a713380e969db2c4c15a7330c0aa4a2de41d9a68048f717aae7f865",
    "main_tex": "b1b40518ea1714f301b23dd04ee1f893d9587982a2a2430fb8a747aad29f5656",
    "main_pdf": "7509086fa589bb49d04dfced1ec78d669e4c540917e761a8f86b4fee62b54c31",
    "pdf": "7509086fa589bb49d04dfced1ec78d669e4c540917e761a8f86b4fee62b54c31",
    "log": "fb12d7c5fa1f7eab6eca9b246b0aa9f81d5c425ae083ad7f06ab087d67f2b1bf",
    "readme": "aef74f13eff1b23485b285158a5d9034597b54fb6ca86541a9f2132b0ae4f84b",
    "plan": "3a52040df52c0a26076b5b88e844c4bcc7bbd2aaaeb24fb4187ee142c1e5f951",
    "derivation": "059204c24636fdf380b1835c4e3305318dc92de49e0f76297d4defa9acf42427",
    "proof": "28b61612ecaf6ee62338fbcbeb0ccc902c88ecc1647b5f08dc8b2dbefeac9b61",
    "claim": "05ca27275046e239e1d4e921c636e878f249a5ec48316df90af5e960a3f48d87",
    "route": "9ce6cfe3d436028fe26d3ef4081ad4315f0c0a93d6c6cab71f966470af9a440c",
    "protocol": "a81c40d01d6e475dd852bb38b344715c62b34cb0a6b095b013410f7547872056",
    "theorem": "a55a29989461e23c5f98257253a965dcd26ca57c67922ec4251cf2aaa8c13266",
    "ledger": "dc522eb543482f9cda603ea58bc29a39dce6aae38b966507db891cc4517d23ec",
    "bridge": "0265ff326b8aa8385db0a510df6cc1dbe5b04d5d6ce632896a7942c9372faa81",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def fail(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(path: Path, optimized: bool) -> str:
    command = [sys.executable] + (["-O"] if optimized else []) + ["-B", str(path), "--check"]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    fail(proc.returncode == 0, f"{path.name} failed: {proc.stderr}")
    fail(proc.stderr == "", f"{path.name} wrote stderr")
    return proc.stdout


def check() -> None:
    for name, path in FILES.items():
        fail(path.is_file(), f"missing {name}")
        fail(digest(path) == LOCKS[name], f"provenance {name}")
    document = json.loads(FILES["certificate"].read_bytes())
    payload = document["payload"]
    fail(document["claim_status"] == "PROVED_UNIFORM_FINITE_CRT_PROXY_ADJACENT_ENTRY_BOUND", "claim status")
    fail(payload["schema"] == "TPC405_C1_LOCAL_NORMALIZATION_SCALE_LADDER_V1", "schema")
    fail(payload["window_rule"] == "N=4H", "window rule")
    fail(payload["theorem_domain"]["H_and_N"] == "integers H,N with H>=1 and N>=H+2", "integer domain")
    fail(payload["theorem"]["coarse_uniform_bound"] == "z<=4/(a_min*H)<=4/H", "uniform bound")
    fail(payload["claim_firewall"]["FULL_OPERATOR_NORM"] == "OPEN", "full operator firewall")
    fail(len(payload["cases"]) == 20, "case census")
    normal = [run(FILES[key], False) for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True) for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC405_BRIDGE_CHECK=PASS cases=20 scale_ladder=PASS strict_firewall=PASS")


if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
