#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-273 finite margin matrix."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-273-margin-stability-matrix"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_margin_stability_matrix.md"
PRODUCER = PROJECT / "code/tpc273_margin_stability_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc273_independent_checker.py"
STRESS = PROJECT / "experiments/tpc273_margin_stress.py"
CERTIFICATE = PROJECT / "results/tpc273_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "8a4bd82f86ac9acd0a8e82768904418cb811bdb8"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION"
BRIDGE_SHA256 = "ee86089264c36dda2d9a41619ab85af0e04911640eb39d8a4e84fdb49938b597"

# These hashes freeze the immediately preceding release.  They prevent a
# later documentation edit from silently changing what TPC-273 replays.
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "fb8049b8bbdf16baf9ea40692df08e55b83716f974fb8999b019a4b16c4f05bb",
    "papers/tpc-272-correlation-margin-budget-compiler/README.md": "3e4b4b1efc2933f5b72bdd2b8c98855660767b30a96cff04fe833c98b8fa0c4d",
    "papers/tpc-272-correlation-margin-budget-compiler/PROOF_PACKAGE.md": "90f729e3132d0a9a810191454ac026c40ca62827dbeb2ca61bd777074f96d398",
    "papers/tpc-272-correlation-margin-budget-compiler/notes/theorem_ledger.md": "7e1cba1a0e3975796f0aa8df40a50593d3388158e69ff267741018cec6d4e24a",
    "papers/tpc-272-correlation-margin-budget-compiler/notes/route_evaluation.md": "11269363de1f81c7473c2eeb3c6f35895a8173550242f6d838a4871b512cb8ac",
    "papers/tpc-272-correlation-margin-budget-compiler/results/tpc272_certificate.json": "f12b8f5a666593df4d14c5a36b261db1c8f323596d033013479fcce43540d4cb",
    "research/tpc-big-road/bridge_b_correlation_margin_budget.md": "d792fff25603967021bc2bee9c83c66e89cb6eb4e2952947e249c7f0837af8a3",
    "research/tpc-big-road/tpc_bridge_b_correlation_margin_budget_checker.py": "2abb0af7faef68217eeb732caa9d7d9623ce9e80a47afd428b1bd64e112d6ac0",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py": "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json": "19b629425c4e64ec3e9638bb8e9f5baee304a7340d764fb32dfa2c31d49c907d",
}

# Filled once the project and bridge text are final.  The checker deliberately
# hashes every release artifact except its own bridge checker.
PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "ca709835020d76057bdc989cf1fc1b8eb16b056eb3a4918c95c5bf10fadc8843",
    "PAPER_PLAN.md": "d490d813b8e167ce7c7c270b1658bdac3a9781b239ea257937aa83b5891223b8",
    "PROOF_PACKAGE.md": "00bb6f0b10e627d639f7eef27c273c8e59b5990e794ddbd3211cf5554827a7fb",
    "README.md": "2d3aefdd3bf3ac608b992f662b7db660abb42d2284a7c3d24147887dbe5db733",
    "code/tpc273_margin_stability_certificate.py": "9898d54a8c36c1c9576961a0f246ab6201c1a88997e9537a667e0537c27ff7a9",
    "experiments/tpc273_independent_checker.py": "8776fb9fc502bd2ec2001b2d12dbb130f7b159e91db56792c67350c3dffa47e5",
    "experiments/tpc273_margin_stress.py": "09bc6927ef28612a887316c1843db40000866f45fbbfea417444903f1290356e",
    "notes/citation_verification.md": "aaddcc1cd1a1055a0a70954a147fea02cbead4382f34a44965ca6af64635c574",
    "notes/claim_firewall.md": "f49056d026bc4460f020522ebb3c7c229c92930585f602e70100465823e031b6",
    "notes/computational_protocol.md": "92985f2cb81afa51f3a54887317142b891a3603eb1d37c29e1f7e43da9a5e04b",
    "notes/route_evaluation.md": "1e1b35fe512e7cb14a1e182c893264c964351ae9b2cb9ea8bab565007691a8ac",
    "notes/theorem_ledger.md": "1b11e224be860c2f1c6ab91b2ad8604291f0c6746dacb138f81703eb7f6a8830",
    "paper/main.pdf": "2cd104be4f669b8ffd123bbcd6971002bf6747a513dd12843330dbeb8b6db1f9",
    "paper/main.tex": "13a27783522489bc584c4733a361d58811a75d350b22dda9ddf6f8d02c09d62a",
    "paper/paper.pdf": "2cd104be4f669b8ffd123bbcd6971002bf6747a513dd12843330dbeb8b6db1f9",
    "paper/references.bib": "af266a9654aad4f25d364275e7b3d0f38053ab2edef29b970b18b098f249889c",
    "results/tpc273_certificate.json": "e44287f82692d4be536665cb87a4092d45fa48381a809a7efbdf66d67c962d13",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def frozen(path: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "missing frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest_bytes(frozen(path)) == expected, "frozen source hash: " + path)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER" and digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH" and digest(BRIDGE) == BRIDGE_SHA256,
         "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC273_MAXIMUM_CLAIM = " + STATUS,
        "TPC273_ROUTE_ADVANCE = YES_SCOPED_FINITE_MARGIN_STABILITY_OBSTRUCTION",
        "TPC273_MARGIN_STABILITY_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE",
        "TPC273_CUTOFF_FLIPS = NUMERICALLY_CERTIFIED",
        "TPC273_PHASE_FLIP = NUMERICALLY_CERTIFIED_FINITE_TWO_ROWS",
        "TPC273_SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC",
        "TPC273_GROWING_UNIFORMITY = OPEN_ASYMPTOTIC",
        "TPC273_FIXED_POWER_CREDIT = 0",
        "TPC273_ARITHMETIC_ADVANCE = NO",
        "TPC273_L2 = NONE",
        "TPC273_FULL_GATE_B = OPEN",
        "TPC273_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC273_TWIN_PRIME_RESULT = NONE",
        "TPC273_STATUS = " + STATUS,
        "TPC273_ROUND2_CLUE = TEST_SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    flat = " ".join(text.split())
    for phrase in ("32 rows", "12 rows", "11 middle-band rows", "9 rows",
                   "z=2 -> 5", "z=2 -> 3", "30 are `NEGATIVE_REAL_AXIS`",
                   "two are `POSITIVE_REAL_AXIS`", "m^2 = rho^2"):
        need(phrase in flat, "bridge result: " + phrase)


def child(path: Path, marker: str, optimized: bool, args: list[str]) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), *args])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    triples = (
        (PRODUCER, "TPC273_CERTIFICATE=PASS", ["--check"]),
        (INDEPENDENT, "TPC273_INDEPENDENT_CHECK=PASS", []),
        (STRESS, "TPC273_MARGIN_STRESS=PASS", []),
    )
    for path, marker, args in triples:
        normal = child(path, marker, False, args)
        optimized = child(path, marker, True, args)
        need(normal == optimized, "normal/optimized mismatch: " + path.name)


def fraction_interval(value: object, positive: bool = True) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = Fraction(str(value[0])), Fraction(str(value[1]))
    need(lo <= hi and (not positive or lo > 0), "interval order/sign")
    return lo, hi


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "certificate header")
    payload = data["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() == data["payload_sha256"],
         "payload digest")
    need(payload["schema"] == "TPC273_MARGIN_STABILITY_CERTIFICATE_V1",
         "certificate schema")
    parameters = payload["parameters"]
    need(parameters["registered_scales"] == [64, 96, 128, 192] and
         parameters["cutoff_grid"] == [2, 3, 4, 5] and
         parameters["kernel_exponents"] == [1, 2] and
         parameters["margin_squared_thresholds"] == {"low": "1/64", "high": "1/16"},
         "registered grid")
    cases = payload["cases"]
    need(len(cases) == 32, "case count")
    counts = {name: 0 for name in ("MARGIN_BELOW_ONE_EIGHTH",
                                   "MARGIN_MIDDLE_BAND",
                                   "MARGIN_ABOVE_ONE_QUARTER")}
    phases = {name: 0 for name in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS",
                                   "CROSSES_ZERO")}
    keys = set()
    for row in cases:
        key = (row["scale"], row["comparison_cutoff_z"], row["kernel_exponent"])
        need(key not in keys, "duplicate case")
        keys.add(key)
        m2 = fraction_interval(row["margin_squared_interval"])
        m6 = fraction_interval(row["margin_sixth_interval"])
        need(m6 == (m2[0] ** 3, m2[1] ** 3), "sixth-power transfer")
        expected = ("MARGIN_BELOW_ONE_EIGHTH" if m2[1] < Fraction(1, 64)
                    else "MARGIN_ABOVE_ONE_QUARTER" if m2[0] > Fraction(1, 16)
                    else "MARGIN_MIDDLE_BAND")
        need(row["classification"] == expected, "classification")
        need(row["phase"] in phases and row["positive_residual_lanes"] is True and
             row["exact_projection_identity"] is True, "row semantics")
        need(fraction_interval(row["radius_squared_interval"]) [0] > 0,
             "radius positivity")
        counts[row["classification"]] += 1
        phases[row["phase"]] += 1
    need(counts == {"MARGIN_BELOW_ONE_EIGHTH": 12,
                    "MARGIN_MIDDLE_BAND": 11,
                    "MARGIN_ABOVE_ONE_QUARTER": 9}, "classification counts")
    need(phases == {"NEGATIVE_REAL_AXIS": 30, "POSITIVE_REAL_AXIS": 2,
                    "CROSSES_ZERO": 0}, "phase counts")
    transitions = payload["transitions"]
    need(len(transitions) == 3, "transition count")
    expected_transitions = {
        "N64_E1_Z2_TO_Z5": ("MARGIN_MIDDLE_BAND", "MARGIN_ABOVE_ONE_QUARTER"),
        "N128_E1_Z2_TO_Z3": ("MARGIN_MIDDLE_BAND", "MARGIN_BELOW_ONE_EIGHTH"),
        "N96_Z3_E1_TO_E2": ("MARGIN_ABOVE_ONE_QUARTER", "MARGIN_ABOVE_ONE_QUARTER"),
    }
    for item in transitions:
        need(item["label"] in expected_transitions and
             (item["low_classification"], item["high_classification"]) ==
             expected_transitions[item["label"]], "transition semantics")
        ratio = fraction_interval(item["margin_squared_ratio_interval"])
        need(ratio[0] > 0 and item["phase_low"] in phases and
             item["phase_high"] in phases, "transition interval")
    theorem = payload["finite_theorem"]
    need(theorem == {
        "claim": "declared finite perturbations cross quantitative margin bands",
        "cutoff_flip_transitions": 2,
        "high_margin_cases": 9,
        "kernel_transition_records": 1,
        "low_margin_cases": 12,
        "middle_margin_cases": 11,
        "negative_phase_cases": 30,
        "positive_phase_cases": 2,
        "status": "NUMERICALLY_CERTIFIED_FINITE",
        "total_cases": 32,
    }, "finite theorem ledger")
    firewall = payload["firewall"]
    need(firewall["TPC273_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC273_SOURCE_LEVEL_MARGIN"] == "OPEN_ASYMPTOTIC" and
         firewall["TPC273_FULL_GATE_B"] == "OPEN" and
         firewall["TPC273_TWIN_PRIME_RESULT"] == "NONE", "claim firewall")


def check_pdf() -> None:
    need(PDF.stat().st_size > 10000, "PDF too small")
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text extraction")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Finite Margin-Stability Matrix", "Liang Wang",
                   "32-row matrix", "REFUTED_SCOPED", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(info.returncode == 0 and b"Pages:           4" in info.stdout,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    for row in fonts.stdout.decode("ascii", errors="replace").splitlines()[2:]:
        if row.strip():
            need(row.split()[-5:-2] == ["yes", "yes", "yes"], "font embedding")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "Overfull \\hbox", "Underfull \\hbox",
                "undefined references", "Fatal", "Error"):
        need(bad not in log, "LaTeX log: " + bad)


def check_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "assert syntax: " + path.name)
    need("tpc273_margin_stability_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError,
            KeyError, TypeError, ValueError) as error:
        print("TPC273_BRIDGE_CHECK=FAIL " + str(error))
        return 1
    print("TPC273_BRIDGE_CHECK=PASS cases=32 low=12 middle=11 high=9 "
          "cutoff_flips=2 phase_positive_rows=2 finite_stability=REFUTED_SCOPED")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
