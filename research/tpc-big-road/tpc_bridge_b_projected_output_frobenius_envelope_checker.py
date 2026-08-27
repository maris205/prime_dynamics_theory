#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-274 projected envelope."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-274-projected-output-frobenius-envelope"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_projected_output_frobenius_envelope.md"
PRODUCER = PROJECT / "code/tpc274_projected_output_envelope_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc274_independent_checker.py"
STRESS = PROJECT / "experiments/tpc274_envelope_stress.py"
CERTIFICATE = PROJECT / "results/tpc274_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "01916208a6c4ae7018017c8f19e25997bf03e75b"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP"
BRIDGE_SHA256 = "4819122c45caddfb3be93356413f5414bdbbaeb2dff90da5c4e88eadf6664af1"

# The preceding release is frozen so that a later documentation edit cannot
# change the physical object replayed by this paper.
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "b2bdc929f8f90db6bcd67298ec243492916711017867a858231081bd1d7fa3ba",
    "papers/tpc-273-margin-stability-matrix/README.md": "2d3aefdd3bf3ac608b992f662b7db660abb42d2284a7c3d24147887dbe5db733",
    "papers/tpc-273-margin-stability-matrix/PROOF_PACKAGE.md": "00bb6f0b10e627d639f7eef27c273c8e59b5990e794ddbd3211cf5554827a7fb",
    "papers/tpc-273-margin-stability-matrix/notes/theorem_ledger.md": "1b11e224be860c2f1c6ab91b2ad8604291f0c6746dacb138f81703eb7f6a8830",
    "papers/tpc-273-margin-stability-matrix/notes/route_evaluation.md": "1e1b35fe512e7cb14a1e182c893264c964351ae9b2cb9ea8bab565007691a8ac",
    "papers/tpc-273-margin-stability-matrix/results/tpc273_certificate.json": "e44287f82692d4be536665cb87a4092d45fa48381a809a7efbdf66d67c962d13",
    "research/tpc-big-road/bridge_b_margin_stability_matrix.md": "ee86089264c36dda2d9a41619ab85af0e04911640eb39d8a4e84fdb49938b597",
    "research/tpc-big-road/tpc_bridge_b_margin_stability_matrix_checker.py": "6b4fae1bf0995f5f72b0ae1228a1e21e647ee234b5f34609eafd0cc3ae7e0126",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py": "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json": "19b629425c4e64ec3e9638bb8e9f5baee304a7340d764fb32dfa2c31d49c907d",
}

# Filled after all TPC-274 artifacts are final.  The checker hashes every
# project artifact except this bridge checker itself.
PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "36413a8f513ee99614c8061171d9869a6dc794d58cb00a2f31fb2d14517deaf2",
    "PAPER_PLAN.md": "5bb02531c8fd854af7da0e0a9b7554de7aae1c9c7290711ea6a4cd1f4aedba2e",
    "PROOF_PACKAGE.md": "cedc7ec9d4bb15adff45a64a76cc5b38d52fbccb2624af06359f54b4b5204469",
    "README.md": "0ba2dff50b1bdd2639d11f6cd4df8205e6e9d7f7f100f62a327385a04c6f8720",
    "code/tpc274_projected_output_envelope_certificate.py": "778e0cd331e55e0f7db6641d3062c24e6b6f2e4e9888283140a52764efd71713",
    "experiments/tpc274_independent_checker.py": "b96d790b7c4d3b31504e318dbe78894dc7c885e2a3275d9f3123864953f24d47",
    "experiments/tpc274_envelope_stress.py": "346f8e5f483488f2be047ba63360d5de968c51d79a27f6de94fb2eaced4beae7",
    "notes/citation_verification.md": "1f3d779ff4ed30cc08c8ebeae0d02691f64cdf9b1193eb3153753c7fb6c39f43",
    "notes/claim_firewall.md": "d94060aa10018382d229dc28087906eab12f88d027d6b27bdb338b18e5581187",
    "notes/computational_protocol.md": "3a5fd31bf3b70d48530c2c19d6b7e6c35f6c74c97791dd23adc018d1ff123909",
    "notes/route_evaluation.md": "b2bdd950ccbcd476f5122fe2105791eb1f24726c6a23705de056e4a56d712427",
    "notes/theorem_ledger.md": "b8b62a9c667074252beb97e06281737bd8ab1dfabb1c0ecb716002eccbc989fc",
    "paper/main.pdf": "530149438ccf7fc1fb9d1b0412d3e497fb4de36119338572e57796f6ee65e5d3",
    "paper/main.tex": "7d5052b1429fbd34439ac243cfca5336bf7b3ec398e9d33a124aea7bf1564b95",
    "paper/paper.pdf": "530149438ccf7fc1fb9d1b0412d3e497fb4de36119338572e57796f6ee65e5d3",
    "paper/references.bib": "873efdd5b46d3f0d4ddf2a54623684a9dfec53e1926200830c3d333db335a595",
    "results/tpc274_certificate.json": "01f9c37438b846c009fbb1650b1da57e87b875519510662178ad26c135bf517d",
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
    need(result.returncode == 0 and result.stderr == b"",
         "missing frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest_bytes(frozen(path)) == expected,
             "frozen source hash: " + path)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER" and digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH" and
         digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC274_MAXIMUM_CLAIM = " + STATUS,
        "TPC274_ROUTE_ADVANCE = YES_SCOPED_PROJECTED_FROBENIUS_ENVELOPE_GAP",
        "TPC274_PROJECTED_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE_INEQUALITY",
        "TPC274_FINITE_GAP = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC274_CANCELLATION_FREE_ROUTE = INSUFFICIENT_SCOPED",
        "TPC274_ENVELOPE_MARGIN = NOT_AN_ACTUAL_MARGIN_UPPER_BOUND",
        "TPC274_SOURCE_LEVEL_OUTPUT_BOUND = OPEN_ASYMPTOTIC",
        "TPC274_SIGNED_OUTPUT_REASSEMBLY = OPEN",
        "TPC274_FIXED_POWER_CREDIT = 0",
        "TPC274_ARITHMETIC_ADVANCE = NO",
        "TPC274_L2 = NONE",
        "TPC274_FULL_GATE_B = OPEN",
        "TPC274_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC274_TWIN_PRIME_RESULT = NONE",
        "TPC274_STATUS = " + STATUS,
        "TPC274_ROUND2_CLUE = TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    flat = " ".join(text.split())
    for phrase in ("12 rows", "above 50", "below `1/64`",
                   "11 `NEGATIVE_REAL_AXIS`", "one `POSITIVE_REAL_AXIS`",
                   "not an upper bound on the actual margin"):
        need(phrase in flat, "bridge result: " + phrase)


def child(path: Path, marker: str, optimized: bool,
          args: list[str]) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), *args])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    children = (
        (PRODUCER, "TPC274_CERTIFICATE=PASS", ["--check"]),
        (INDEPENDENT, "TPC274_INDEPENDENT_CHECK=PASS", []),
        (STRESS, "TPC274_ENVELOPE_STRESS=PASS", []),
    )
    for path, marker, args in children:
        normal = child(path, marker, False, args)
        optimized = child(path, marker, True, args)
        need(normal == optimized, "normal/optimized mismatch: " + path.name)


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object, positive: bool = False) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi and (not positive or lo > 0), "interval order/sign")
    return lo, hi


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS, "certificate header")
    payload = data["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() ==
         data["payload_sha256"], "payload digest")
    need(payload["schema"] ==
         "TPC274_PROJECTED_OUTPUT_FROBENIUS_ENVELOPE_CERTIFICATE_V1",
         "certificate schema")
    parameters = payload["parameters"]
    need(parameters["upstream_schema"] ==
         "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1" and
         parameters["upstream_payload_sha256"] ==
         "890167856037b7c1c0356ffa40bfe5f98e3f6974ff14ca3ef7e248682d220f4a" and
         parameters["kernel_exponents"] == [1, 2] and
         parameters["growing_cutoff_schedule"] ==
         {"64": 4, "96": 4, "128": 4, "192": 5, "256": 5, "384": 5} and
         parameters["gap_threshold"] == "G_F/G_perp > 50" and
         parameters["margin_threshold"] == "m_F^2<1/64",
         "certificate parameters")
    rows = payload["rows"]
    need(len(rows) == 12, "row count")
    expected_scales = {64: (15, 4), 96: (20, 5), 128: (24, 5),
                       192: (32, 6), 256: (38, 6), 384: (50, 7)}
    keys: set[tuple[int, int]] = set()
    phases = {"NEGATIVE_REAL_AXIS": 0, "POSITIVE_REAL_AXIS": 0,
              "CROSSES_ZERO": 0}
    for row in rows:
        n = row["scale"]
        key = (n, row["kernel_exponent"])
        need(key not in keys, "duplicate row")
        keys.add(key)
        need(n in expected_scales and
             (row["H"], row["Q"]) == expected_scales[n] and
             row["comparison_cutoff_z"] == parameters["growing_cutoff_schedule"][str(n)] and
             row["role"] == "GROWING_CUTOFF_KERNEL_GRID" and
             row["matrix_entry_arithmetic"] == "EXACT_RATIONAL" and
             row["projected_operator"] == "A_perp=(I-P_3)A" and
             row["frobenius_envelope_valid"] is True and
             row["exact_projection_identity"] is True, "row metadata")
        f2, b2, env = (frac(row["projected_frobenius_squared"]),
                       frac(row["beta_norm_squared"]),
                       frac(row["output_envelope_squared"]))
        need(f2 > 0 and b2 > 0 and env == f2 * b2,
             "exact envelope product")
        gap_lo, gap_hi = interval(row["envelope_to_actual_ratio_interval"], True)
        margin_lo, margin_hi = interval(row["envelope_margin_squared_interval"], True)
        need(gap_lo > 50 and gap_hi >= gap_lo and
             margin_hi < Fraction(1, 64) and margin_lo <= margin_hi,
             "finite thresholds")
        need(row["envelope_gap_classification"] == "GAP_ABOVE_FIFTY" and
             row["envelope_margin_classification"] ==
             "ENVELOPE_MARGIN_BELOW_ONE_EIGHTH", "row classification")
        phases[row["phase"]] += 1
    need(phases == {"NEGATIVE_REAL_AXIS": 11,
                    "POSITIVE_REAL_AXIS": 1, "CROSSES_ZERO": 0},
         "phase census")
    pairs = payload["kernel_pairs"]
    need(len(pairs) == 6, "kernel pair count")
    need(all(item["exponent_transition"] == "1->2" and
             item["both_envelope_margins_below_one_eighth"] is True
             for item in pairs), "kernel pair semantics")
    theorem = payload["finite_theorem"]
    need(theorem == {
        "cancellation_free_route": "INSUFFICIENT_SCOPED",
        "claim": "projected Frobenius envelope is valid but too loose on registered rows",
        "envelope_margin_below_one_eighth_rows": 12,
        "gap_above_fifty_rows": 12,
        "kernel_pair_rows": 6,
        "operator_envelope": "PROVED_EXACT_FINITE_INEQUALITY",
        "phase_crossing_rows": 0,
        "phase_negative_rows": 11,
        "phase_positive_rows": 1,
        "scale_rows": 6,
        "status": "NUMERICALLY_CERTIFIED_FINITE",
        "total_rows": 12,
    }, "finite theorem ledger")
    firewall = payload["firewall"]
    need(firewall["TPC274_PROJECTED_FROBENIUS_ENVELOPE"] ==
         "PROVED_EXACT_FINITE_INEQUALITY" and
         firewall["TPC274_CANCELLATION_FREE_ROUTE"] == "INSUFFICIENT_SCOPED" and
         firewall["TPC274_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC274_SOURCE_LEVEL_OUTPUT_BOUND"] == "OPEN_ASYMPTOTIC" and
         firewall["TPC274_SIGNED_OUTPUT_REASSEMBLY"] == "OPEN" and
         firewall["TPC274_L2"] == "NONE" and
         firewall["TPC274_FULL_GATE_B"] == "OPEN" and
         firewall["TPC274_TWIN_PRIME_RESULT"] == "NONE",
         "claim firewall")
    need(payload["round2_clue"] ==
         "TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES",
         "round2 clue")


def check_pdf() -> None:
    need(PDF.stat().st_size > 10000, "PDF too small")
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text extraction")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Projected Frobenius Envelope Gap", "Liang Wang",
                   "12 rows", "INSUFFICIENT_SCOPED", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(info.returncode == 0 and b"Pages:           4" in info.stdout,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    for line in fonts.stdout.decode("ascii", errors="replace").splitlines()[2:]:
        if line.strip():
            fields = line.split()
            need(len(fields) >= 8 and fields[-5:-2] == ["yes", "yes", "yes"],
                 "font embedding")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "Overfull \\hbox", "Underfull \\hbox",
                "undefined references", "Fatal", "Error"):
        need(bad not in log, "LaTeX log: " + bad)


def check_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "assert syntax: " + path.name)
    need("tpc274_projected_output_envelope_certificate" not in
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
        print("TPC274_BRIDGE_CHECK=FAIL " + str(error))
        return 1
    print("TPC274_BRIDGE_CHECK=PASS rows=12 pairs=6 gap_above_fifty=12 "
          "envelope_margin_low=12 cancellation_free=INSUFFICIENT_SCOPED")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
