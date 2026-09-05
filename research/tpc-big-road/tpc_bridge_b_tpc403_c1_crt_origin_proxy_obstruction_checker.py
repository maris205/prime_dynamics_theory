#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-403 finite CRT obstruction."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-403-c1-crt-origin-proxy-obstruction"
FILES = {
    "producer": PROJECT / "code/tpc403_c1_crt_origin_proxy_obstruction.py",
    "independent": PROJECT / "experiments/tpc403_independent_checker.py",
    "stress": PROJECT / "experiments/tpc403_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc403_certificate.json",
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
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc403_c1_crt_origin_proxy_obstruction.md",
}
LOCKS = {
    "producer": "b46ac034f8aced8a4988b3224827773c5ad7f2db9b203f73d12c952ac38920e3",
    "independent": "0d0942ea4890c50154e4239e5837881f8f16225655f7f7f7a72d44357a098622",
    "stress": "df2ebf49e1bd5c1820e6af347073a488c0642cf8f0421bc6365a9a6e805a4f54",
    "certificate": "64a109c63d6237a9b02fbc1ed6d2e5fe8a041f403cf1eb2102609b75174056da",
    "main_tex": "64a412a9b1f0a3248addf7c4830ae9eb31d11e5c0d2a44159d03a7cf898b4379",
    "main_pdf": "38a77f91a2b0b0f72b3d37e14dcf4d567c4593791a94ed4e47b94ae05bdbfdee",
    "pdf": "38a77f91a2b0b0f72b3d37e14dcf4d567c4593791a94ed4e47b94ae05bdbfdee",
    "log": "845364a73c4551bf029da0a668137873954c6245ef389c058ac824dd2bcb5383",
    "readme": "eae4e6aaaa13ae14a4854d4f7e31a1d717df86c6ba0e68f95485c36ae72515eb",
    "plan": "7162666d8de4bc8fb86428ce232724243b932758ab6cc8fff313467b37fce961",
    "derivation": "8c6a3f30edaea06aee86d86ec7f9bbf70f089032583800b8444a7c11e54feb13",
    "proof": "22c3c5f0436752895691912326835953506a067eb28105eac1f49608569dde5c",
    "claim": "c5b5e85ea79bfba91220ff31e8d7ab7fa1c89416a6669a76e8f7bcc154043146",
    "route": "d339e82c974ac105471076dfeed6b87c9aa181c71b924098e8d3b76937b46d62",
    "protocol": "d390a9f7524d761bf050d3a73f7c1eb8db867215e843e54f1cfe29a73be11f32",
    "theorem": "606877331f701001dca67f8cbaf7521f62f0faa1d34a32376fa70782bc394391",
    "bridge": "a5d1a9f05d96045f0a0b94ad406e1fd53ba84f36e53407f2f8e117a424bde4c0",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def fail(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(path: Path, optimized: bool) -> tuple[str, str]:
    python = [sys.executable]
    if optimized:
        python.insert(1, "-O")
    command = python + ["-B", str(path), "--check"]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    fail(proc.returncode == 0, f"{path.name} failed: {proc.stderr}")
    fail(proc.stderr == "", f"{path.name} wrote stderr")
    return proc.stdout, proc.stderr


def check() -> None:
    for name, path in FILES.items():
        fail(path.is_file(), f"missing {name}")
        if LOCKS:
            fail(digest(path) == LOCKS[name], f"provenance {name}")
    document = json.loads(FILES["certificate"].read_bytes())
    payload = document["payload"]
    fail(document["claim_status"] == "PROVED_EXACT_FINITE_CRT_PROXY_OBSTRUCTION", "claim status")
    fail(payload["schema"] == "TPC403_C1_CRT_ORIGIN_PROXY_OBSTRUCTION_V1", "schema")
    fail(len(payload["cases"]) == 4 and payload["cases"][-1]["m"] == 4, "case census")
    fail(payload["negative_congruence"] == "o = -N (mod p_i) for odd i", "corrected congruence")
    fail(payload["claim_firewall"]["ARITHMETIC_ADVANCE"] == "NO", "claim firewall")
    normal = [run(FILES[key], False)[0] for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True)[0] for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC403_BRIDGE_CHECK=PASS cases=4 max_m=4 reverse_crt=PASS signed_obstruction=PASS")


if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
