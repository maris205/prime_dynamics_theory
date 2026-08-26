#!/usr/bin/env python3
"""Fail-closed release checker for TPC-262."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-262-literal-mode-zero-cross-gram"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_literal_mode_zero_cross_gram.md"
PRODUCER = PROJECT / "code/tpc262_literal_mode_zero_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc262_independent_checker.py"
STRESS = PROJECT / "experiments/tpc262_prime_fiber_stress.py"
CERTIFICATE = PROJECT / "results/tpc262_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "fbf95fe0ca19918c6f5fe182277d1ecc4068b449"
STATUS = (
    "PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL"
)
BRIDGE_SHA256 = "0b9adb8c6bc22e6ae68a7e48821696fd516830f81cf8a22193bffe061301f167"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "01828abe639226e4b8db07fc941547151ee70fefa648b25cbaac21dc3b25ad05",
    "papers/tpc-261-strict-endpoint-budget-compiler/README.md":
        "a3a3f1c33b48eaab75e503657290421b2d092c640c3a95bc0713bd7f6ba6b977",
    "papers/tpc-261-strict-endpoint-budget-compiler/PROOF_PACKAGE.md":
        "0bcecbebfb00609cb1f9a429f715e5ab493811225b8c2b4f337e48d571599dd8",
    "papers/tpc-261-strict-endpoint-budget-compiler/notes/theorem_ledger.md":
        "731928d3fddbc3014e52e0fec887fe6980787577b4945f2d5fc95d3116214ce8",
    "papers/tpc-261-strict-endpoint-budget-compiler/notes/route_evaluation.md":
        "7860c4a756ccf4002c7ed8d0fe14b346d439f9aa5244f462255f23677a7d51ee",
    "research/tpc-big-road/bridge_b_strict_endpoint_budget_compiler.md":
        "31081a1a0f92cce5c7b7175b27d9d3e250f3fd505002093719b8bb4ea8becb47",
    "research/tpc-big-road/tpc_bridge_b_strict_endpoint_budget_compiler_checker.py":
        "9feea6fad48b65af9e061b29114b5f6d509fab233d5a8d55fd16fd54d2b3bf39",
    "research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md":
        "74e42689e17efad75e9718a9d6ac3d8f3ec9c16239204a4915b0b7bdc17ae218",
    "research/tpc-big-road/bridge_b_phase_fourier_collision_separation.md":
        "3a6783dc1e5798e2876bd0cdd1eee230a457749738e0f4b05685ca32e4ad0dac",
    "research/tpc-big-road/bridge_b_zero_hole_additive_edge_frame.md":
        "6244c1045faf86f97334c3bf5154ff68f945d4dd9c33b8f00ddd8ee6032442dd",
}

PROJECT_HASHES = {
    ".gitignore": "b3c3b3177a5ed79072b60737ac96c92856ad4769ade6a1bf913a003db57256c9",
    "DERIVATION_PACKAGE.md": "5606c2151ac1f1ad2ccb19ec8552718e6894cdef0fb8a1cafde7a030fde28883",
    "PAPER_PLAN.md": "9768b1bac164d4df96327aded038528e8c2ce2bc7de52aabc27d81172271fad9",
    "PROOF_PACKAGE.md": "520f74acd0fc39f50c53d1cef31e2a9a599630384b4f888b190a8a64842364b1",
    "README.md": "d93b364a110103a81cdf3e766586da0f43af1f2b090aecb7514e875d4f8365d6",
    "code/tpc262_literal_mode_zero_certificate.py": "960bf4102ead406edefc6f9ac9e0f5dabfc3b6c2348d5ae75759a34f052d82b7",
    "experiments/tpc262_independent_checker.py": "bf0d0f951d4565d9d7ecd8a54ff30fe1326ac89ab60d56ab0640a18200b4a675",
    "experiments/tpc262_prime_fiber_stress.py": "10830b4629cc690b3bdcfb32fab7809753bc8964d3d96a9cbb663de2fd1f5edd",
    "notes/citation_verification.md": "97eba8d31c2b8ba41a06503cb402b66d401e7634aa6e5105c14c814a2134dfa5",
    "notes/claim_firewall.md": "1dda6045a22aa9c8625338094505de3be85d13fca3ad4db37485fd6f84729088",
    "notes/computational_protocol.md": "af3a339e1ae22b5ec3c09057614ea58df268f981a0df54f6fa05b090a3723353",
    "notes/route_evaluation.md": "4951487298f1cb5ec0062d75512d4d05b7de3893b26b98a148b70d2a311147cc",
    "notes/theorem_ledger.md": "ef8c6d834dfda217a412c99d9f70a93961ac7e501fa7a86c8b9286d92dcb8556",
    "paper/main.pdf": "786528690ebea837cbbbb125fa4a56c97f1f848f075ace6ab9e02756b7c52ac5",
    "paper/main.tex": "7bba63069ba675a841ece61e3fbf038826ad7900a6d53e9c2fc5460cef725db8",
    "paper/paper.pdf": "786528690ebea837cbbbb125fa4a56c97f1f848f075ace6ab9e02756b7c52ac5",
    "paper/references.bib": "fae2433e2aaadc4b5ff93f96fa3db923de95df1616d20848335bb4ceb20951cf",
    "results/tpc262_certificate.json": "7a8de8d4a1874ee83c63be808d792400502077d1b9334f87653975f2c0cf5d0e",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}
MARKERS = (
    "TPC262_MAXIMUM_CLAIM = " + STATUS,
    "TPC262_ROUTE_ADVANCE = YES_SCOPED_LITERAL_SIGNED_OPERATOR_INTERFACE",
    "TPC262_UNIT_CLASS_PROJECTION = PROVED_EXACT_FINITE",
    "TPC262_CROSS_GRAM_IDENTITY = PROVED_EXACT",
    "TPC262_SIGNED_REMAINDER_OPERATOR = PROVED_EXACT_FINITE_X",
    "TPC262_DELETED_DIAGONAL = PROVED_EXACT_Q_MINUS_2",
    "TPC262_ENDPOINT_THRESHOLD = PROVED_EXACT_ONE_OVER_400",
    "TPC262_OPERATOR_IMAGE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL",
    "TPC262_PHASE_CHARACTER_SEPARATION = PROVED_EXACT",
    "TPC262_POLARIZED_V59_CHARACTER = OPEN",
    "TPC262_GROWING_SHELL_COUNTEREXAMPLE = NONE",
    "TPC262_ARITHMETIC_ADVANCE = NO",
    "TPC262_FIXED_ATOM_CREDIT = 0",
    "TPC262_L2 = NONE",
    "TPC262_FULL_GATE_B = OPEN",
    "TPC262_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC262_TWIN_PRIME_RESULT = NONE",
    "TPC262_LITERAL_BETA_W_CROSS_GRAM = OPEN",
    "TPC262_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_digest(path: Path) -> str:
    return digest(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n"))


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest(frozen(path)) == expected, "source hash: " + path)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(normalized_digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH", "bridge hash placeholder")
    need(normalized_digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in text, "bridge marker: " + marker)
    need("TPC262_ROUND2_CLUE = CENSUS_THE_LITERAL_GROWING_PRIME_SHELL_CROSS_GRAM"
         in text, "round-two clue")


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    producer = child(PRODUCER, "TPC262_CERTIFICATE=PASS")
    independent = child(INDEPENDENT, "TPC262_INDEPENDENT_CHECK=PASS")
    independent_opt = child(INDEPENDENT, "TPC262_INDEPENDENT_CHECK=PASS", True)
    stress = child(STRESS, "TPC262_FIBER_STRESS=PASS")
    stress_opt = child(STRESS, "TPC262_FIBER_STRESS=PASS", True)
    need(independent == independent_opt, "independent stdout mismatch")
    need(stress == stress_opt, "stress stdout mismatch")
    need("threshold=1/400" in producer and "literal_growing=OPEN" in producer,
         "producer fields")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) +
                 "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") == "TPC262_LITERAL_MODE_ZERO_CROSS_GRAM_CERTIFICATE_V1",
         "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD,
         "certificate baseline")
    need(parsed.get("baseline", {}).get("source_count") == 11,
         "certificate source count")
    need(parsed.get("fiber_audit", {}).get("primes") == list((5, 7, 11, 13)),
         "prime shell")
    gram = parsed.get("gram_audit", {})
    need(gram.get("probe_norm") == "15/4", "probe norm")
    need(gram.get("records", {}).get("plus", {}).get("mode_zero") == "60",
         "plus mode zero")
    need(gram.get("records", {}).get("alternating", {}).get("mode_zero") == "0",
         "alternating mode zero")
    need(gram.get("records", {}).get("plus", {}).get("diagonal") == ["15/4"] * 4,
         "plus diagonal")
    need(gram.get("records", {}).get("alternating", {}).get("diagonal") == ["15/4"] * 4,
         "alternating diagonal")
    phase = parsed.get("phase_character_audit", {})
    need(phase.get("F0") == "15/2" and phase.get("F1") == "-5/4" and
         phase.get("F3") == "-5/4" and phase.get("F2") == "0",
         "phase characters")
    signed = parsed.get("signed_operator_audit", {})
    need(signed.get("additive_phase") == "v=0_FINITE_CERTIFICATE_ONLY" and
         signed.get("polarized_scalar") == "352/3" and
         signed.get("packet_quadratics") ==
         ["9523/6", "2705/2", "6707/6", "2705/2"],
         "signed operator audit")
    need(parsed.get("threshold_audit", {}).get("gap") == "1/400", "gap")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC262_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC262_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC262_L2") == "NONE" and
         firewall.get("TPC262_LITERAL_BETA_W_CROSS_GRAM") == "OPEN" and
         firewall.get("TPC262_TWIN_PRIME_RESULT") == "NONE", "firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("mode-zero", "cross-Gram", "Liang Wang", "1/400",
                   "operator-image", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+5\s*$", info_text) is not None,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = [row for row in fonts.stdout.decode("ascii").splitlines()[2:]
            if row.strip()]
    need(len(rows) >= 10, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF font embedding")
    if LOG.is_file():
        log_text = LOG.read_text(encoding="utf-8", errors="replace")
        bad = re.search(
            r"(?m)^(?:LaTeX Warning:|Package .* Warning:|Overfull \\\\|"
            r"Underfull \\\\|There were undefined references)",
            log_text,
        )
        need(bad is None, "LaTeX log")


def check_source_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "unsafe assertion syntax: " + path.name)
    need("tpc262_literal_mode_zero_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_source_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print("TPC262_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC262_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("cross_gram=PROVED_EXACT")
    print("operator_image=NUMERICALLY_CERTIFIED_STRUCTURAL")
    print("literal_growing_cross_gram=OPEN")
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
