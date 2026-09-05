#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-404 finite local audit."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-404-c1-local-normalization-boundary"
FILES = {
    "producer": PROJECT / "code/tpc404_c1_local_normalization_boundary.py",
    "independent": PROJECT / "experiments/tpc404_independent_checker.py",
    "stress": PROJECT / "experiments/tpc404_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc404_certificate.json",
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
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc404_c1_local_normalization_boundary.md",
}
LOCKS = {
    "producer": "db06511130b791fb2a9fd8ee7fe2ecd2bd83efc10074a62174869de6d7d6d291",
    "independent": "462c625edfe156b377eba0375771f4c520b8c4d80ff5668f1d43df1d902ca682",
    "stress": "6eb15ea67bbfed931e3562455c524f9dcf1ed55c7c14d020a6198eb31435f9d9",
    "certificate": "e39bbf772f4fe647cc1ff3fcfeb9f87f915cb125b40f2da4c178c89594ebf50b",
    "main_tex": "17e93382e57dd23b9fe81092d7e3c25101f54ec6cb7d678453a5d77f51cc1079",
    "main_pdf": "0e04d3054753e9ea92a1c9c8e827a1a337928f123c085d712d5bb651c96ec185",
    "pdf": "0e04d3054753e9ea92a1c9c8e827a1a337928f123c085d712d5bb651c96ec185",
    "log": "10b70961436acd682fe02687a0d69b41680fc90b7fc19d33741bfb4a275c9672",
    "readme": "24554cb483e97d569ec9bc48b269403c5f59bc722a83fe88fd317114e4d922fc",
    "plan": "4ef07ae7c3a770fb4567958a46d1eba50c8c448e3b0aa178e3ce6a124897ddf8",
    "derivation": "a66b4f1f2f03ab78e594124da3c8220660bd1163d3276ce747d04f085afed9c3",
    "proof": "e9a6765f3783a9dc76ad396d9f167a631adb386189c54616fbd6ec52c3aa1e35",
    "claim": "605801a2be3482322b89b9e0c4fb76682c8a3ed68b5b905dab7182c3bdf6bca0",
    "route": "60e356a92a0746ed52ff3ecb6dddfed55bb256346f882431df68b9f5a0c57ba4",
    "protocol": "900e6bd3e20ecc448557ac62fccb8ea7012d20dc1e294b8c33f0915ea28162a8",
    "theorem": "946daed268abe0f4e74159cf2a4033eaeb202f2d76209aa5cef2462c4174c580",
    "bridge": "3704bcd8955d6f3af96c23c2eb2d350c983a468b317120579487eaf382f11735",
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
    fail(document["claim_status"] == "PROVED_EXACT_FINITE_LOCAL_NORMALIZATION_BOUNDARY_AUDIT", "claim status")
    fail(payload["schema"] == "TPC404_C1_LOCAL_NORMALIZATION_BOUNDARY_V1", "schema")
    fail(payload["normalization"] == "local_diagonal", "normalization")
    fail(len(payload["cases"]) == 4 and [c["m"] for c in payload["cases"]] == [1, 2, 3, 4], "case census")
    fail(payload["claim_firewall"]["NORMALIZED_GROWING_THEOREM"] == "OPEN", "claim firewall")
    normal = [run(FILES[key], False) for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True) for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC404_BRIDGE_CHECK=PASS cases=4 local_diagonal=PASS strict_firewall=PASS")


if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
