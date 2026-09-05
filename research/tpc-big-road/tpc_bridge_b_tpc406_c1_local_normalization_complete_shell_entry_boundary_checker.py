#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-406 complete-shell release."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary"
FILES = {
    "producer": PROJECT / "code/tpc406_c1_local_normalization_complete_shell_entry_boundary.py",
    "independent": PROJECT / "experiments/tpc406_independent_checker.py",
    "stress": PROJECT / "experiments/tpc406_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc406_certificate.json",
    "main_tex": PROJECT / "paper/main.tex", "main_pdf": PROJECT / "paper/main.pdf",
    "pdf": PROJECT / "paper/paper.pdf", "log": PROJECT / "paper/compile.log",
    "readme": PROJECT / "README.md", "plan": PROJECT / "PAPER_PLAN.md",
    "derivation": PROJECT / "DERIVATION_PACKAGE.md", "proof": PROJECT / "PROOF_PACKAGE.md",
    "claim": PROJECT / "notes/claim_firewall.md", "route": PROJECT / "notes/route_evaluation.md",
    "protocol": PROJECT / "notes/computational_protocol.md", "theorem": PROJECT / "notes/theorem_ledger.md",
    "ledger": ROOT / "research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md",
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc406_c1_local_normalization_complete_shell_entry_boundary.md",
}

# Filled from the finalized LF-normalized release artifacts.
LOCKS = {
    "producer": "c464c92c31b85375465f49e40574e1c182943303843dda4ef850052c904909b6",
    "independent": "63a25e62c95031d4f7655fdc169efeb0b5a1c605cc312a61aecf22d2bd602d14",
    "stress": "3f3d69023a2f35b4b9e111a51e939d40e8ce48376ba255226e6f83aefc817c53",
    "certificate": "fdfb60557954f39207076c909e2b17460da46fe8602a75eced270c3e49ae195e",
    "main_tex": "d56b866522f2d622a8aa9c96c6365ffcd3ece3504aa58fe04260f0f18c12c371",
    "main_pdf": "217eec03573812a584dc832cefdd10f29497fe1bb88b27d1f2a5263fb755b4cf",
    "pdf": "217eec03573812a584dc832cefdd10f29497fe1bb88b27d1f2a5263fb755b4cf",
    "log": "9a9ba645e8c3e7753c6d8a70f78ef30aa8bc332d2b8a36acf3fc5047738b69f1",
    "readme": "fb34a6ffa6556a4e14860d4e56ad43420145199a654180f1ffc90401b1a645f7",
    "plan": "731c968a5c8be2b30ba1bc4603c47abdfb475b6075f460055a26b1bad676263a",
    "derivation": "f5c1dbfb14c5f5c533f5861029ae392a464d02cc98b5b52899bc2d46d484bcdd",
    "proof": "7c0b39deb4af79095f168bd02b7b81fc044f7fbf7d6f22bf762181eb43f1a172",
    "claim": "6e9d99d044386476030c128f635725b71bedb76b116c4efb2637ced5f5efdba7",
    "route": "51797469328d9674d6da074d35317b699ce834d79a36757ead564f3a5796ab37",
    "protocol": "ffe13b72b6d46f5702846697f298a7d70cfcf7a44fc9bd2096e6fb1107d547ab",
    "theorem": "9532f4dc8710f3801a894aa568af3acd51555f435d69db3187b50d4234db6389",
    "ledger": "d9dc2dca7b738d22f78b009d7ea37707cd49a74288add939cbea8bcd8e965fd5",
    "bridge": "44cc34ad017d103357b8222ffc1314ca75acedd3ec877b6f8c7f6074beb4f8db",
}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()
def fail(condition: bool, message: str) -> None:
    if not condition: raise SystemExit(message)
def run(path: Path, optimized: bool) -> str:
    proc = subprocess.run([sys.executable] + (["-O"] if optimized else []) + ["-B", str(path), "--check"], cwd=ROOT, text=True, capture_output=True, check=False)
    fail(proc.returncode == 0, f"{path.name} failed: {proc.stderr}")
    fail(proc.stderr == "", f"{path.name} wrote stderr")
    return proc.stdout
def check() -> None:
    for name,path in FILES.items():
        fail(path.is_file(), f"missing {name}")
        fail(digest(path) == LOCKS[name], f"provenance {name}")
    d=json.loads(FILES["certificate"].read_bytes()); p=d["payload"]
    fail(d["claim_status"]=="PROVED_EXACT_FINITE_COMPLETE_SHELL_LOCAL_ENTRY_BOUNDARY", "claim status")
    fail(p["schema"]=="TPC406_C1_LOCAL_NORMALIZATION_COMPLETE_SHELL_ENTRY_BOUNDARY_V1", "schema")
    fail(p["shell_rule"]=="all primes Q<p<=2Q" and p["shell_count"]==872, "complete shell")
    fail(p["window_rule"]=="N=4H", "window rule")
    fail(p["theorem"]["coarse_uniform_bound"]=="z<=4/(a_min*H)<=4/H", "uniform bound")
    fail(p["claim_firewall"]["FULL_OPERATOR_NORM"]=="OPEN", "full operator firewall")
    fail(len(p["cases"])==5 and all(c["m"]==436 for c in p["cases"]), "case census")
    normal=[run(FILES[k],False) for k in ("producer","independent","stress")]
    optimized=[run(FILES[k],True) for k in ("producer","independent","stress")]
    fail(normal==optimized, "normal/optimized mismatch")
    print("TPC406_BRIDGE_CHECK=PASS cases=5 shell_primes=872 strict_firewall=PASS")
if __name__=="__main__":
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    check()
