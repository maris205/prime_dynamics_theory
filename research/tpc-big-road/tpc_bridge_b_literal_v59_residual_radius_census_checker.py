#!/usr/bin/env python3
"""Fail-closed release checker for TPC-267."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-267-literal-v59-residual-radius-census"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_literal_v59_residual_radius_census.md"
PRODUCER = PROJECT / "code/tpc267_literal_residual_radius_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc267_independent_checker.py"
STRESS = PROJECT / "experiments/tpc267_kernel_stress.py"
CERTIFICATE = PROJECT / "results/tpc267_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "5cec310465c9c8aac4af055f2eafa577ed4afb7f"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS"
BRIDGE_SHA256 = "ab0287a0aa90f5272899fe513ddb3b11c71335c7d83fb4e990403be9adc51527"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "7dd6d491dfaa2fbdb552223b6a9d1a0ee411d360a3a5f30975aaaeb9515f3ee8",
    "papers/tpc-266-end-to-end-claim-firewall/README.md":
        "40165bd0b8e47975ad97c14080e69180490c33258f234b4e27cc56c3f824a753",
    "papers/tpc-266-end-to-end-claim-firewall/PROOF_PACKAGE.md":
        "6220d5590a963d25c6fc063a4f33b484fd68c5645cbfffe9e05c467c9df7b52c",
    "papers/tpc-266-end-to-end-claim-firewall/notes/theorem_ledger.md":
        "6f137c516d42f85792f080602fe0bfbc8e3bc077db40dea9b1844795a66ff0c1",
    "papers/tpc-266-end-to-end-claim-firewall/notes/route_evaluation.md":
        "3cee9e6001b92f666ed908d7fd7662d2931bc7c6b4e939e61fbc857987691646",
    "research/tpc-big-road/bridge_b_typed_end_to_end_claim_firewall.md":
        "3f0a6787e8177e17207217f69f3fb89d8b50f97d8791cdd48be8e575dacce84a",
    "research/tpc-big-road/tpc_bridge_b_typed_end_to_end_claim_firewall_checker.py":
        "ede957ca2c4ddeb68160672ee7c5c8a5e6d54aa0f401c30643d9504a30d04ed6",
}

PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "9bce9830f34878471541c437629fef9a8158161225191d4a51b4c4cf19194825",
    "PAPER_PLAN.md": "e0cba99db6bf93a6841caeeaa1d121e33a96173d7d844f78a19ec28a7961df2d",
    "PROOF_PACKAGE.md": "d62d8580ed1a886f8b57edb88e51179c04a4ef82c9e2133f30e6a30b5e6f67ce",
    "README.md": "6001b3d5db82ca844a049f6e1fb110d42e2f87a1b5e4f6da3d69cfab15c38bd1",
    "code/tpc267_literal_residual_radius_certificate.py": "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750",
    "experiments/tpc267_independent_checker.py": "77c6ba5e94275a64355ebc921ccd23db546705269176077873513e8b04747cc1",
    "experiments/tpc267_kernel_stress.py": "6f28ca0844dc0dbba270cb35b37dff622ca2cc08a4f19f95109bfe8457a6ce43",
    "notes/citation_verification.md": "c7832907c11ba59f991f482ce5f2fd59d28095bbcb147cd389989a59d46ad18f",
    "notes/claim_firewall.md": "84b36dbd4bc4e10e15ce4144ed08ba455afc270f076f52b34185d9fd37faa9c4",
    "notes/computational_protocol.md": "79fc8dd3e865704e397c28b2a2f45fb0d0817994222d0a3854ad960817677a22",
    "notes/route_evaluation.md": "0ca421f4c28d5e9e896c983b4390b51cb2faf7f4f13534f8d1bc99ad0db06e62",
    "notes/theorem_ledger.md": "6a73208a5f7249f2605499563c01dddf2a5b258a1f36b52696c690962f2b6c72",
    "paper/main.pdf": "9ca695ca14b56bd300152a06e2eae6263fac3c9fa39555955b46d78307595332",
    "paper/main.tex": "99811e2c135168ce97fa9d9170c7e607dec3f089a1a45ac25c332e8d5ad29f41",
    "paper/paper.pdf": "9ca695ca14b56bd300152a06e2eae6263fac3c9fa39555955b46d78307595332",
    "paper/references.bib": "51710e70f53bfad776da380a133ce26f95763ef24ff6e5b3b36d03810cfe36ee",
    "results/tpc267_certificate.json": "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg", "paper/main.log",
    "paper/main.out",
}

MARKERS = (
    "TPC267_MAXIMUM_CLAIM = " + STATUS,
    "TPC267_ROUTE_ADVANCE = YES_SCOPED_FINITE_LITERAL_RESIDUAL_CENSUS",
    "TPC267_LITERAL_MASK_OPERATOR = PROVED_EXACT_FINITE",
    "TPC267_BETA_FORMULA = PROVED_EXACT_FINITE",
    "TPC267_HYBRID_EULER_ENCLOSURE = PROVED_INTERVAL_FINITE",
    "TPC267_PROJECTION_SPLIT = PROVED_EXACT_FINITE",
    "TPC267_FINITE_RESIDUAL_RADIUS = NUMERICALLY_CERTIFIED",
    "TPC267_FINITE_SIGNED_PHASE = NUMERICALLY_CERTIFIED",
    "TPC267_QUARTER_CONTRACTION = NUMERICALLY_CERTIFIED_ALL_12_ROWS",
    "TPC267_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC",
    "TPC267_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC",
    "TPC267_FIXED_POWER_CREDIT = 0",
    "TPC267_ARITHMETIC_ADVANCE = NO",
    "TPC267_L2 = NONE",
    "TPC267_FULL_GATE_B = OPEN",
    "TPC267_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC267_TWIN_PRIME_RESULT = NONE",
    "TPC267_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def normalized_digest(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        blob = frozen(path).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        need(hashlib.sha256(blob).hexdigest() == expected,
             "source hash: " + path)


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
    need("TPC267_ROUND2_CLUE = REPEAT_THE_CENSUS_WITH_GROWING_LOCAL_CUTOFF_AND_SMOOTH_PROFILE" in text,
         "round-two clue")


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    outputs = [
        (child(PRODUCER, "TPC267_CERTIFICATE=PASS"),
         child(PRODUCER, "TPC267_CERTIFICATE=PASS", True)),
        (child(INDEPENDENT, "TPC267_INDEPENDENT_CHECK=PASS"),
         child(INDEPENDENT, "TPC267_INDEPENDENT_CHECK=PASS", True)),
        (child(STRESS, "TPC267_KERNEL_STRESS=PASS"),
         child(STRESS, "TPC267_KERNEL_STRESS=PASS", True)),
    ]
    for normal, optimized in outputs:
        need(normal == optimized, "normal/optimized child mismatch")
    need("finite_phase=certified" in outputs[0][0] and
         "actual_asymptotic_radius=OPEN" in outputs[0][0],
         "producer fields")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("certificate_version") == 1 and
         parsed.get("claim_status") == STATUS,
         "certificate header")
    payload = parsed.get("payload", {})
    need(payload.get("schema") == "TPC267_LITERAL_V59_RESIDUAL_CENSUS_V1",
         "certificate schema")
    need(hashlib.sha256((json.dumps(payload, ensure_ascii=True,
                                    sort_keys=True, separators=(",", ":")) +
                         "\n").encode("ascii")).hexdigest() ==
         parsed.get("payload_sha256"), "payload digest")
    parameters = payload.get("parameters", {})
    need(parameters.get("tail_cutoff") == 50000 and
         parameters.get("profiles") == [1, 2], "certificate parameters")
    theorem = payload.get("finite_theorem", {})
    need(theorem.get("exact_operator_and_projection") is True and
         theorem.get("residual_identity") == "C_perp=C-C_3" and
         theorem.get("certified_cases") == 12 and
         theorem.get("rho_bound") ==
         "|C_perp|/R < 1/4 in every listed finite case" and
         theorem.get("phase_set") == ["NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS"],
         "finite theorem")
    cases = payload.get("cases", [])
    expected = [(64, 15, 4, 1), (64, 15, 4, 2),
                (96, 20, 5, 1), (96, 20, 5, 2),
                (128, 24, 5, 1), (128, 24, 5, 2),
                (192, 32, 6, 1), (192, 32, 6, 2),
                (256, 38, 6, 1), (256, 38, 6, 2),
                (384, 50, 7, 1), (384, 50, 7, 2)]
    need(len(cases) == len(expected), "case count")
    for case, (scale, height, q0, exponent) in zip(cases, expected):
        need((case.get("scale"), case.get("H"), case.get("Q"),
              case.get("kernel_exponent")) ==
             (scale, height, q0, exponent), "case parameters")
        need(case.get("comparison_cutoff_z") == 2 and
             case.get("euler_tail_cutoff") == 50000 and
             case.get("beta_exact_rational") is True and
             case.get("exact_projection_identity") is True and
             case.get("quarter_contraction") is True,
             "case exact flags")
        need(float(case.get("rho_upper", "1")) < 0.25 and
             float(case.get("rho_upper_squared", "1")) < 0.0625,
             "case contraction")
        interval = case.get("rho_squared_interval", [])
        need(len(interval) == 2 and 0.0 <= float(interval[0]) <=
             float(interval[1]) < 0.0625, "case interval")
        need(case.get("phase") in {"NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS"},
             "case phase")
        radius = case.get("radius_squared_interval", [])
        need(len(radius) == 2 and float(radius[0]) > 0, "case radius")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC267_FINITE_RESIDUAL_RADIUS") ==
         "NUMERICALLY_CERTIFIED" and
         firewall.get("TPC267_FINITE_SIGNED_PHASE") ==
         "NUMERICALLY_CERTIFIED" and
         firewall.get("TPC267_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC267_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC267_ACTUAL_V59_RADIUS") == "OPEN_ASYMPTOTIC" and
         firewall.get("TPC267_ACTUAL_V59_PHASE") == "OPEN_ASYMPTOTIC" and
         firewall.get("TPC267_L2") == "NONE" and
         firewall.get("TPC267_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC267_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Finite Literal V59 Residual-Radius", "Liang Wang",
                   "finite signed-phase", "1/4", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+4\s*$", info_text) is not None,
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
        bad = re.search(r"(?m)^(?:LaTeX Warning:|Package .* Warning:|"
                        r"Overfull \\|Underfull \\|"
                        r"There were undefined references)", log_text)
        need(bad is None, "LaTeX log")


def check_source_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "unsafe assertion syntax: " + path.name)
    need("tpc267_literal_residual_radius_certificate" not in
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
        print("TPC267_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC267_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("finite_residual_phase=NUMERICALLY_CERTIFIED")
    print("quarter_contraction=ALL_12_ROWS")
    print("actual_v59_radius=OPEN_ASYMPTOTIC")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
