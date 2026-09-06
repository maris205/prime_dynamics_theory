#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-409."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-409-c1-odd-complete-shell-height-ladder"
FILES = {
    "producer": PROJECT / "code/tpc409_c1_odd_complete_shell_height_ladder.py",
    "independent": PROJECT / "experiments/tpc409_independent_checker.py",
    "stress": PROJECT / "experiments/tpc409_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc409_certificate.json",
    "main_tex": PROJECT / "paper/main.tex", "main_pdf": PROJECT / "paper/main.pdf",
    "pdf": PROJECT / "paper/paper.pdf", "log": PROJECT / "paper/compile.log",
    "readme": PROJECT / "README.md", "plan": PROJECT / "PAPER_PLAN.md",
    "derivation": PROJECT / "DERIVATION_PACKAGE.md", "proof": PROJECT / "PROOF_PACKAGE.md",
    "claim": PROJECT / "notes/claim_firewall.md", "route": PROJECT / "notes/route_evaluation.md",
    "protocol": PROJECT / "notes/computational_protocol.md", "theorem": PROJECT / "notes/theorem_ledger.md",
    "ledger": ROOT / "research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md",
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc409_c1_odd_complete_shell_height_ladder.md",
}
LOCKS = {
    "producer": "2453dfa25f490c37edb1b273e20add7a880f900c6bbc2f125437828c305f65c6",
    "independent": "965624a1705d36975654a7a37c03b3886d9a952a611c813f5afa418999dedceb",
    "stress": "9341fbf480adb63434c32e9b1d12b08a004d425319f8eeed551ab62769c047c1",
    "certificate": "d7e603eabd700ee508c8a122d16b3225195867f0b85359b6673722fca920e303",
    "main_tex": "a28d0391f7e521318511a612753a3c25f6ebdc5a9ce16829d7cb2a55e7af2f26",
    "main_pdf": "95dec283065f89e0a9c16a63f5fbd9520c4eaba91a7b3825f1fdb1e23cb9f94b",
    "pdf": "95dec283065f89e0a9c16a63f5fbd9520c4eaba91a7b3825f1fdb1e23cb9f94b",
    "log": "d0c1a203cf88fce094fa7752d1ca91e1f272cac3fbd53549378f2932bc9b2f92",
    "readme": "e9ea52d470f9f9f358e4bf383b2e8739b693a2a50458b7c1ec618c58220cd2e9",
    "plan": "da883c1a2de37bc09eaa6759de523f0b2a137d3b5daa2d930cb74b21a0bc809f",
    "derivation": "6a2e30f22dc49f38c9dcffe2d7f82c94007a693ebfb164d7eba29051bbf26146",
    "proof": "2d06aa2af0fb7075450bd697efe33f78e6b0a4b6f4d45390d0cae19a63e1dc4d",
    "claim": "a08aebf3fa40aee976279d951481ed5c180842b55b04ae677eb531346bdcd0e4",
    "route": "8135461ec1361bbcacecd8023b2497e97d1ce7adeb03b30dc04bcd2636a4d5ad",
    "protocol": "e3b28e54325428d5a3e4de1898ce1f84158dfbeb040349b61b65af13965592e7",
    "theorem": "2f3eadcfecb5dfcd34e92f9fb13edf19f304127e7874fb84043ec144c418626a",
    "ledger": "573b0ccfee33f94e7100f3e46890c2edfa3f5ab4bd218c841a211ed621d3cbba",
    "bridge": "d8f3783e14298b1118295e8d407a933b80e62cd981b126d30440d8de6b3e20e9",
}


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def fail(condition, message):
    if not condition:
        raise SystemExit(message)


def run(path, optimized):
    command = [sys.executable] + (["-O"] if optimized else []) + ["-B", str(path), "--check"]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    fail(result.returncode == 0, f"{path.name} failed: {result.stderr}")
    fail(result.stderr == "", f"{path.name} wrote stderr")
    return result.stdout


def check():
    for name, path in FILES.items():
        fail(path.is_file(), f"missing {name}")
        fail(LOCKS[name].startswith("__") is False and digest(path) == LOCKS[name], f"provenance {name}")
    document = json.loads(FILES["certificate"].read_bytes())
    payload = document["payload"]
    fail(document["claim_status"] == "PROVED_EXACT_FINITE_ODD_COMPLETE_SHELL_HEIGHT_LADDER", "claim status")
    fail(payload["schema"] == "TPC409_C1_ODD_COMPLETE_SHELL_HEIGHT_LADDER_V1", "schema")
    fail(payload["Q"] == 65536 and payload["heights"] == [16, 32, 66, 128], "height census")
    fail(payload["shell_count"] == 5709 and payload["window_rule"] == "N=4H", "shell/window")
    fail(payload["theorem"]["coarse_uniform_bound"] == "z<=4/(a_min*H)<=4/H", "bound")
    fail(payload["theorem_domain"]["parity"].startswith("r odd"), "odd parity domain")
    fail(payload["claim_firewall"]["FULL_OPERATOR_NORM"] == "OPEN", "operator firewall")
    fail(len(payload["cases"]) == 4, "case census")
    normal = [run(FILES[key], False) for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True) for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC409_BRIDGE_CHECK=PASS cases=4 heights=4 odd_shell=PASS strict_firewall=PASS")


if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
