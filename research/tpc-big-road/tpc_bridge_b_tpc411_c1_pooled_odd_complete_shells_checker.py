#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-411."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-411-c1-pooled-odd-complete-shells"
FILES = {
    "producer": PROJECT / "code/tpc411_c1_pooled_odd_complete_shells.py",
    "independent": PROJECT / "experiments/tpc411_independent_checker.py",
    "stress": PROJECT / "experiments/tpc411_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc411_certificate.json",
    "main_tex": PROJECT / "paper/main.tex", "main_pdf": PROJECT / "paper/main.pdf",
    "pdf": PROJECT / "paper/paper.pdf", "log": PROJECT / "paper/compile.log",
    "readme": PROJECT / "README.md", "plan": PROJECT / "PAPER_PLAN.md",
    "derivation": PROJECT / "DERIVATION_PACKAGE.md", "proof": PROJECT / "PROOF_PACKAGE.md",
    "claim": PROJECT / "notes/claim_firewall.md", "route": PROJECT / "notes/route_evaluation.md",
    "protocol": PROJECT / "notes/computational_protocol.md", "theorem": PROJECT / "notes/theorem_ledger.md",
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc411_c1_pooled_odd_complete_shells.md",
}
LOCKS = {
    "producer": "912deff0417f82f04633802f6f8031b07786e0b619811b5270e689043b133dce", "independent": "dde9f9616e360fc20b0c42161022fab85105c7807ff320a8bdc9100257d88cb0", "stress": "3258c61d4278654bde7bfa7e995667e8aa269c50e2e44d75ff5aa589534d6646",
    "certificate": "6f0f517afaf26c42db51681e6032e4a9e986d1ff3956d9da9eb38e7a3d5a6acf", "main_tex": "43403dc5ddc8eeec037bdd316725f5929dd7616bc7fcdc913acd347e127b46d0", "main_pdf": "bd8192d4a0dae4c22c15c2d29934b68e7628c9c3468f3d9edaa2f245f90ef7e5",
    "pdf": "bd8192d4a0dae4c22c15c2d29934b68e7628c9c3468f3d9edaa2f245f90ef7e5", "log": "bc789e24bcf5852ff2b6c1e0379297ddb9f38bc478827dbe2b115fe64bc56e3e", "readme": "028edb826c131613116fcd9a68badd32f969935f58079eb190485ad8ce434b48", "plan": "ac31cfa16c895685059d59126377558368cf006da9319249e74408971a8ab56e",
    "derivation": "d5a31ea0ed0f6350cf26dda10580f67aa2a94a437c16e2162410442a3fe4c7d0", "proof": "b7b8b2efd1b696743dde552107492fdea9f7847548f9c9c97a0beb1b0a6cd64a", "claim": "6f66b649f89e89605e7e7438204b33bec3b84b28df71c587640843d48971b64a",
    "route": "90c03ce31aab6dbbfb897143362add89c52e1b5f299993a3347f3da7cd758ee4", "protocol": "29ac986af4b37b805c24e33ffdbd3948f10d7318a30e9ac14755a1509b5cedf4", "theorem": "d02e1ddce3eab2225eae1247a0a5b6dd8d7cee0a4340fdebb68659ad8a4f7ec8",
    "bridge": "c497b405e6e4c659a68d144837fe2eb1c9f34152fb4e27037a7cf39651a6170b",
}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()

def fail(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def run(path: Path, optimized: bool) -> str:
    command = [sys.executable] + (["-O"] if optimized else []) + ["-B", str(path), "--check"]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    fail(result.returncode == 0, f"{path.name} failed: {result.stderr}")
    fail(result.stderr == "", f"{path.name} wrote stderr")
    return result.stdout

def check() -> None:
    for name, path in FILES.items():
        fail(path.is_file(), f"missing {name}")
        fail(not LOCKS[name].startswith("__") and digest(path) == LOCKS[name], f"provenance {name}")
    document = json.loads(FILES["certificate"].read_bytes())
    payload = document["payload"]
    fail(document["claim_status"] == "PROVED_EXACT_FINITE_POOLED_ODD_COMPLETE_SHELLS", "claim status")
    fail(payload["schema"] == "TPC411_C1_POOLED_ODD_COMPLETE_SHELLS_V1", "schema")
    fail(payload["Q_scales"] == [65536, 131072] and payload["H"] == 66 and payload["N"] == 264, "domain")
    fail(payload["shell_counts"] == [5709, 10749] and payload["window_rule"] == "N=264=4H", "shell census")
    fail(payload["theorem"]["coarse_uniform_bound"] == "z<=4/(a_min*H)<=4/H", "bound")
    fail(payload["theorem_domain"]["parity"].startswith("pooled cardinality r=16458 is even"), "parity")
    fail(payload["claim_firewall"]["FULL_OPERATOR_NORM"] == "OPEN", "operator firewall")
    fail(payload["claim_firewall"]["ARITHMETIC_ADVANCE"] == "NO" and payload["claim_firewall"]["FIXED_POWER_CREDIT"] == 0, "advance firewall")
    fail(len(payload["cases"]) == 1 and payload["cases"][0]["shell_count"] == 16458, "case census")
    normal = [run(FILES[key], False) for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True) for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC411_BRIDGE_CHECK=PASS cases=1 pooled_shells=2 literal_masks=PASS strict_firewall=PASS")

if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
