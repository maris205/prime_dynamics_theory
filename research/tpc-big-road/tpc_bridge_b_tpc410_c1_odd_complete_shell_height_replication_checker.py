#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-410."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-410-c1-odd-complete-shell-height-replication"
FILES = {
    "producer": PROJECT / "code/tpc410_c1_odd_complete_shell_height_replication.py",
    "independent": PROJECT / "experiments/tpc410_independent_checker.py",
    "stress": PROJECT / "experiments/tpc410_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc410_certificate.json",
    "main_tex": PROJECT / "paper/main.tex", "main_pdf": PROJECT / "paper/main.pdf",
    "pdf": PROJECT / "paper/paper.pdf", "log": PROJECT / "paper/compile.log",
    "readme": PROJECT / "README.md", "plan": PROJECT / "PAPER_PLAN.md",
    "derivation": PROJECT / "DERIVATION_PACKAGE.md", "proof": PROJECT / "PROOF_PACKAGE.md",
    "claim": PROJECT / "notes/claim_firewall.md", "route": PROJECT / "notes/route_evaluation.md",
    "protocol": PROJECT / "notes/computational_protocol.md", "theorem": PROJECT / "notes/theorem_ledger.md",
    "ledger": ROOT / "research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md",
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc410_c1_odd_complete_shell_height_replication.md",
}
LOCKS = {
    "producer": "dd6baa870bbb14f85e041a72c287ba7329f01a013e8e996f2dce96ae2bf06a22",
    "independent": "22efa037150ca05ca959cb52bf7050ffcecb4502bfd929c39728a7565748a9a4",
    "stress": "10706f1943a21f276a0bbcab2cb4e10a3c466cbccd9acf2a3e166513b6dfeedb",
    "certificate": "d830efae2172923320aad3d5953fc092eccb63b7b3334a524572ea4eaaf37d9e",
    "main_tex": "fa7f97c0f019b6f1e111db66b0a24982c37870ab7fd975fefee10610201d286f",
    "main_pdf": "19ea5b80524567668b20c089a5832164592fe74d4e9c08ea5386cebf846a6f57",
    "pdf": "19ea5b80524567668b20c089a5832164592fe74d4e9c08ea5386cebf846a6f57",
    "log": "73738c6cc9dab0645174c9978824ad4e611f3c26720ab59fc88d33a0547db960",
    "readme": "5b36381f1825e5dedb6985e918f0f8a42d59a7f64e7d2206e906deb316f0a299",
    "plan": "4a70354d715e82b427cd871582072905743c486dfe5effa33ad93d1757e54844",
    "derivation": "851d859c36db4e15110baf6d396909691fb897f9158186fb332fecaabf600350",
    "proof": "ab897f42061681acef82741e407efa3c8efdc44f39077ff53597183049db239b",
    "claim": "61eed05b5066421c2a6edd7e31df130eb2910bfac1463ee557a6045202775329",
    "route": "03b2ca5d4fa530b36a1d01decdb627e1bfb6247290a0435508a8c618e0bcc930",
    "protocol": "3b3301cadd370f1bbd7ec68f3570a5417415fb1e1ed277050bfc1bab25faf837",
    "theorem": "f4c893d9abc72badc94625819265dd98099cf1093303f20f01203007d65a992a",
    "ledger": "96dde09a56374b48c08124fa287bb1f2bff0769bd7e5a9f1dffb21183e43c3d0",
    "bridge": "14a5cbc824db78d1b3b5b4d7a9ffd022d6174ddcfed6374bc2c287f9a238a04e",
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
    fail(document["claim_status"] == "PROVED_EXACT_FINITE_ODD_COMPLETE_SHELL_HEIGHT_REPLICATION", "claim status")
    fail(payload["schema"] == "TPC410_C1_ODD_COMPLETE_SHELL_HEIGHT_REPLICATION_V1", "schema")
    fail(payload["Q"] == 131072 and payload["heights"] == [16, 32, 66, 128], "height census")
    fail(payload["shell_count"] == 10749 and payload["window_rule"] == "N=4H", "shell/window")
    fail(payload["theorem"]["coarse_uniform_bound"] == "z<=4/(a_min*H)<=4/H", "bound")
    fail(payload["theorem_domain"]["parity"].startswith("r odd"), "odd parity domain")
    fail(payload["claim_firewall"]["FULL_OPERATOR_NORM"] == "OPEN", "operator firewall")
    fail(len(payload["cases"]) == 4, "case census")
    normal = [run(FILES[key], False) for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True) for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC410_BRIDGE_CHECK=PASS cases=4 heights=4 odd_shell=PASS strict_firewall=PASS")


if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
