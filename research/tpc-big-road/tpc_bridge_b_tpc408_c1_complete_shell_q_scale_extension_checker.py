#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-408."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-408-c1-complete-shell-q-scale-extension"
FILES = {
    "producer": PROJECT / "code/tpc408_c1_complete_shell_q_scale_extension.py",
    "independent": PROJECT / "experiments/tpc408_independent_checker.py",
    "stress": PROJECT / "experiments/tpc408_adversarial_certificate_stress.py",
    "certificate": PROJECT / "results/tpc408_certificate.json",
    "main_tex": PROJECT / "paper/main.tex", "main_pdf": PROJECT / "paper/main.pdf",
    "pdf": PROJECT / "paper/paper.pdf", "log": PROJECT / "paper/compile.log",
    "readme": PROJECT / "README.md", "plan": PROJECT / "PAPER_PLAN.md",
    "derivation": PROJECT / "DERIVATION_PACKAGE.md", "proof": PROJECT / "PROOF_PACKAGE.md",
    "claim": PROJECT / "notes/claim_firewall.md", "route": PROJECT / "notes/route_evaluation.md",
    "protocol": PROJECT / "notes/computational_protocol.md", "theorem": PROJECT / "notes/theorem_ledger.md",
    "ledger": ROOT / "research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md",
    "bridge": ROOT / "research/tpc-big-road/bridge_b_tpc408_c1_complete_shell_q_scale_extension.md",
}

# Filled after the release files are finalized.  Keeping this explicit makes
# any post-release edit fail closed instead of silently changing the package.
LOCKS = {
    "producer": "a863f75ebc35ded168a3740bc376ac663bfe06b9d49c6db83798d459ee5d8be5",
    "independent": "378530d604c058fffe494122e4dbaa91185daa8d73be1b73b474d25bbdaadd84",
    "stress": "58703123a167716368e98d887d80b04a61158bf0028cbb1168408340af68788d",
    "certificate": "8e84061f335e478025d5814f326c8c2a9e31d026007cadcf02186b0210763170",
    "main_tex": "dfa9755da88919c5162d214355ca6dd135f3823284e8f9c622ecb048007a027a",
    "main_pdf": "24d9c8eb53581ae196475cfbb42553b498b467ca4fc9332d4c503536b4c9f784",
    "pdf": "24d9c8eb53581ae196475cfbb42553b498b467ca4fc9332d4c503536b4c9f784",
    "log": "a34e29f7275a45a501efbc8bd457fb77c3025f360d6520142617a2ee62c2d1fe",
    "readme": "dd5fc211b496d32e546f8de7403c4ecfe8ab1394a2e93212eeb7fb8244e5d47d",
    "plan": "aabfba806621797403ab9919ca7b93aa9afc264e2e0692146835e01f2f7142a5",
    "derivation": "e6db15f78ba02b3046ab0628daa8e1228689a90766ffb936052d958e29fa3a04",
    "proof": "c4dee5de7af7dfe6661b8406bccc68ff9cfc6407f9a5faaabb28509284178561",
    "claim": "b5f929f602cef08785ffebca6d44b94e41dce5dffd64162cd7a559ce58b160eb",
    "route": "35b629e0cca7cbaa7997ee6eaf8ad5222bce394cc4162907db98b96a86456eb1",
    "protocol": "d52b5b911cf2a080ab7aac7fc777c51fcc9285f95b8da8b5bf1d15bd588bca22",
    "theorem": "23ead7f5f11a27e319fa0c29f31bb51875bfa6125453577fe4a714391bc20829",
    "ledger": "c03c54aa0b410bbf843d5557a559006e1cf67ac37656ccf9c2c2712f8ccf1b8e",
    "bridge": "032ba59fe92d7b2f37b635512e3c8ef08c3455fbef53b8877189e48773892be4",
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
        fail(LOCKS[name].startswith("__") is False and digest(path) == LOCKS[name],
             f"provenance {name}")
    document = json.loads(FILES["certificate"].read_bytes())
    payload = document["payload"]
    fail(document["claim_status"] == "PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_EXTENSION", "claim status")
    fail(payload["schema"] == "TPC408_C1_COMPLETE_SHELL_Q_SCALE_EXTENSION_V1", "schema")
    fail(payload["Q_scales"] == [65536, 131072] and payload["shell_counts"] == [5709, 10749], "scale census")
    fail(payload["window_rule"] == "N=264=4H", "window")
    fail(payload["theorem"]["coarse_uniform_bound"] == "z<=4/(a_min*H)<=4/H", "bound")
    fail(payload["theorem_domain"]["parity"].startswith("r may be odd"), "odd parity domain")
    fail(payload["claim_firewall"]["FULL_OPERATOR_NORM"] == "OPEN", "operator firewall")
    fail(len(payload["cases"]) == 2, "case census")
    normal = [run(FILES[key], False) for key in ("producer", "independent", "stress")]
    optimized = [run(FILES[key], True) for key in ("producer", "independent", "stress")]
    fail(normal == optimized, "normal/optimized mismatch")
    print("TPC408_BRIDGE_CHECK=PASS cases=2 q_scales=2 odd_shells=PASS strict_firewall=PASS")


if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    check()
