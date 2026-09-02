#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-336."""

from __future__ import annotations
import hashlib, json, os, subprocess, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-336-masked-signed-gram-response"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_tpc336_masked_signed_gram_response.md"
PRODUCER = PROJECT / "code/tpc336_masked_signed_gram_response.py"
INDEPENDENT = PROJECT / "experiments/tpc336_independent_checker.py"
STRESS = PROJECT / "experiments/tpc336_response_stress.py"
CERTIFICATE = PROJECT / "results/tpc336_certificate.json"
MAIN_PDF = PROJECT / "paper/main.pdf"; PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
PARENT_CODE = ROOT / "papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py"
PARENT_CERT = ROOT / "papers/tpc-335-twin-isolated-source-norm/results/tpc335_certificate.json"
PARENT_CODE_SHA256 = "e6d66a3963f974c9d3f03b20441b327a34dd9e684fabb72e0777d31082c4e608"
PARENT_CERT_SHA256 = "cee2aee00208cbfe8331abc80e066c7a736824414f4d8208a73e4c545bfa4934"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE"
SCHEMA = "TPC336_MASKED_SIGNED_GRAM_RESPONSE_V1"
PRODUCER_SHA256 = "0c2febd76d6bfdc5af4b58145739bcc04b435303f15c66b31e2d0b2e63497442"; INDEPENDENT_SHA256 = "cfb30da3e8bb24d9771743597ea40156421ded0647886e3fb44e8b7971b90cb9"
STRESS_SHA256 = "c33fec2d0a2a5c37b78bb57691b1d674fca899ac0d10b46be23ebf262d3f5bfb"; CERTIFICATE_SHA256 = "926859be38cc601ef728363328899d4e9ab2001f77e7e1106ab028d64cf2814a"
BRIDGE_SHA256 = "163c07ae53772774c2ac032c4d3bcbc3aebbe7510f7a908d29007582f86ae9ab"

class Failure(RuntimeError): pass
def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition: raise Failure(message)
def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")
def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()
def run(script: Path, optimized: bool) -> bytes:
    cmd = [sys.executable] + (["-O"] if optimized else []) + ["-B", str(script), "--check"]
    env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["OMP_NUM_THREADS"] = "8"; env["OPENBLAS_NUM_THREADS"] = "8"; env["MKL_NUM_THREADS"] = "8"
    result = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"", "subcheck failed: " + script.name)
    return result.stdout
def check_files() -> None:
    required = (".gitignore", "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md",
        "PROOF_PACKAGE.md", "code/tpc336_masked_signed_gram_response.py",
        "experiments/tpc336_independent_checker.py", "experiments/tpc336_response_stress.py",
        "results/tpc336_certificate.json", "notes/theorem_ledger.md", "notes/claim_firewall.md",
        "notes/computational_protocol.md", "notes/route_evaluation.md",
        "notes/citation_verification.md", "paper/main.tex", "paper/main.pdf",
        "paper/paper.pdf", "paper/compile.log")
    for item in required: need((PROJECT / item).is_file(), "missing artifact: " + item)
    for path, expected, label in ((PRODUCER, PRODUCER_SHA256, "producer"),
        (INDEPENDENT, INDEPENDENT_SHA256, "independent"), (STRESS, STRESS_SHA256, "stress"),
        (CERTIFICATE, CERTIFICATE_SHA256, "certificate"), (BRIDGE, BRIDGE_SHA256, "bridge")):
        need(len(expected) == 64 and not expected.startswith("__"), label + " hash not sealed")
        need(digest(path.read_bytes()) == expected, label + " provenance")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent provenance")
    raw = CERTIFICATE.read_bytes(); document = json.loads(raw)
    need(raw == canonical(document) and document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(canonical(payload)).hexdigest(), "payload")
    need(payload.get("finite_audit") == {"rows": 6, "operator_rows": 6, "categories": 4,
         "response_identity_observations": 6, "gain_ordering_census": 6,
         "arithmetic_advance": "NO", "fixed_power_credit": 0}, "audit")
    need(len(payload.get("rows", [])) == 6 and
         payload.get("summary", {}).get("destructive_interaction_rows") == 6, "summary")
    fw = payload.get("claim_firewall", {})
    need(fw.get("TPC336_ARITHMETIC_ADVANCE") == "NO" and
         fw.get("TPC336_SOURCE_UNIFORM_L2") == "OPEN" and
         fw.get("TPC336_FIXED_POWER_CREDIT") == 0, "firewall")
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and PDF.read_bytes().startswith(b"%PDF-")
         and PDF.stat().st_size > 100000, "PDF")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox", "Underfull \\hbox",
                "LaTeX Error", "Fatal error"): need(bad not in log, "LaTeX diagnostic: " + bad)
def check_bridge_text() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in ("TPC336_MASK_RESPONSE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC336_FIXED_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS",
        "TPC336_GAIN_ORDERING = NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
        "TPC336_DESTRUCTIVE_OUTPUT_INTERACTION = NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
        "TPC336_TWIN_RESPONSE_DOMINANCE = REFUTED_SCOPED_FINITE_PANEL",
        "TPC336_ARITHMETIC_ADVANCE = NO", "TPC336_FIXED_POWER_CREDIT = 0",
        "TPC336_SOURCE_UNIFORM_L2 = OPEN", "TPC336_FULL_GATE_B = OPEN",
        "TPC336_TWIN_PRIME_RESULT = NONE", "TPC336_STATUS = " + STATUS,
        "TPC336_ROUND2_CLUE = RETURN_TO_CONTROL_COVARIANCE_OR_SEEK_UNIFORM_MASKED_OPERATOR_BOUND"):
        need(marker in text, "bridge marker missing")
def main() -> int:
    if "--check" not in sys.argv[1:]: raise SystemExit("explicit --check is required")
    try:
        check_files(); check_bridge_text()
        normal = tuple(run(s, False) for s in (PRODUCER, INDEPENDENT, STRESS))
        optimized = tuple(run(s, True) for s in (PRODUCER, INDEPENDENT, STRESS))
        need(normal == optimized, "normal/optimized stdout mismatch")
        print("TPC336_BRIDGE_CHECK=PASS rows=6 categories=4 gain_ordering=6 destructive_interaction=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print("TPC336_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
