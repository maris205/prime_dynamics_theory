#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-275 signed packet audit."""

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
PROJECT = ROOT / "papers/tpc-275-signed-four-packet-reassembly"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_signed_four_packet_reassembly.md"
PRODUCER = PROJECT / "code/tpc275_signed_four_packet_reassembly_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc275_independent_checker.py"
STRESS = PROJECT / "experiments/tpc275_reassembly_stress.py"
CERTIFICATE = PROJECT / "results/tpc275_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "752e309ae2cc58a3575b28510c91c79bd1f6fd8c"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT"
BRIDGE_SHA256 = "7056bd897054d5876d6e16121f0c02ceced0395d992750303710398f732d91a1"

# The immediately preceding release is frozen.  These source hashes make the
# parent operator, source, and route context immutable for this paper.
SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "9f3a50bc7f68ed199a92ff25fc0fbd68fe9901fc5792b3476f1de6990a54fb2f",
    "papers/tpc-274-projected-output-frobenius-envelope/README.md": "0ba2dff50b1bdd2639d11f6cd4df8205e6e9d7f7f100f62a327385a04c6f8720",
    "papers/tpc-274-projected-output-frobenius-envelope/PROOF_PACKAGE.md": "cedc7ec9d4bb15adff45a64a76cc5b38d52fbccb2624af06359f54b4b5204469",
    "papers/tpc-274-projected-output-frobenius-envelope/notes/theorem_ledger.md": "b8b62a9c667074252beb97e06281737bd8ab1dfabb1c0ecb716002eccbc989fc",
    "papers/tpc-274-projected-output-frobenius-envelope/notes/route_evaluation.md": "b2bdd950ccbcd476f5122fe2105791eb1f24726c6a23705de056e4a56d712427",
    "papers/tpc-274-projected-output-frobenius-envelope/results/tpc274_certificate.json": "01f9c37438b846c009fbb1650b1da57e87b875519510662178ad26c135bf517d",
    "research/tpc-big-road/bridge_b_projected_output_frobenius_envelope.md": "4819122c45caddfb3be93356413f5414bdbbaeb2dff90da5c4e88eadf6664af1",
    "research/tpc-big-road/tpc_bridge_b_projected_output_frobenius_envelope_checker.py": "0e1a89c77ce7c8ba820bd0c490c3e139422c900263e23e291cf299d29a61f36a",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py": "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json": "19b629425c4e64ec3e9638bb8e9f5baee304a7340d764fb32dfa2c31d49c907d",
}

# Filled after all TPC-275 artifacts and the bridge text are final.
PROJECT_HASHES = {
    ".gitignore": "139dac3fcaa03b01ebff688c84d62e6b7ceb154384980f414976d1242aaf2612",
    "DERIVATION_PACKAGE.md": "b03726fc79ad45bd7e021603e975de0333d2988725ae21e836009a1075c8ffb3",
    "PAPER_PLAN.md": "391dd875fe017fc241887db1e1e74e630c77faf2115db1afc0826048a2537ad6",
    "PROOF_PACKAGE.md": "c1776a60481d45917a744b7aeb549e0990f7e44a7d22fd813717e1be01bac2f2",
    "README.md": "2c213f10cb9a8155dd34d35b2b4841339b66fbdaa036a49bd226827acbb86e51",
    "code/tpc275_signed_four_packet_reassembly_certificate.py": "abceae5328b5f454cabc06c2e95811224217f15d050f1672ce4e60fc154ad405",
    "experiments/tpc275_independent_checker.py": "67e0d665dbcc7f509084632817b6882d33b9a538965e263b9e47ff64c0609a81",
    "experiments/tpc275_reassembly_stress.py": "367f2c32c84200b996c4b005f7259c67de9c44ca6300a38a8b610adea898ec35",
    "notes/citation_verification.md": "bf2240b7b25292a499404830c5fd67a1ca676500df00c03656cf537590aa6c22",
    "notes/claim_firewall.md": "a3c94bc2aa5938572e87d13ed86133523f15ab1d2a5cc90dae57a4aa53f955f5",
    "notes/computational_protocol.md": "79f7bae6b0d8089441cea94aaf4ef1e18cd2b95e49bedbef46af8236c4249a25",
    "notes/route_evaluation.md": "55a1f00677a042e68acd3034f11955973e755d8c19d59b64e95c67f3698cc363",
    "notes/theorem_ledger.md": "5a962839aaf67f683b69325e0cb4e0d3bacfec0e77d8c3885591ed88dac676a3",
    "paper/main.pdf": "35e26acfcb6deb41a2d843d5be527b62d11063407551bc4014226357e0350590",
    "paper/main.tex": "f7b3b9a17dfc26f16f6b6e58a13e7794f387e5e056fde633e4d7dcc212d094d7",
    "paper/paper.pdf": "35e26acfcb6deb41a2d843d5be527b62d11063407551bc4014226357e0350590",
    "paper/references.bib": "5f6fe02adbd74f32a64da9f89bbfccdb861c8a7024662cb19cb97e91354d6090",
    "results/tpc275_certificate.json": "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd",
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
        need(expected != "PLACEHOLDER" and
             digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH" and
         digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC275_MAXIMUM_CLAIM = " + STATUS,
        "TPC275_ROUTE_ADVANCE = YES_SCOPED_LITERAL_SIGNED_FOUR_PACKET_REASSEMBLY",
        "TPC275_SIGNED_GRAM_IDENTITY = PROVED_EXACT_FINITE",
        "TPC275_DFT_LEDGER = PROVED_EXACT_FINITE",
        "TPC275_POLARIZATION = PROVED_EXACT_FINITE",
        "TPC275_LITERAL_PACKET_REPLAY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC275_NET_CROSS_TERM = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_ALL_12_ROWS",
        "TPC275_DIAGONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_BETWEEN_1_AND_12_OVER_5",
        "TPC275_FROBENIUS_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_ABOVE_50",
        "TPC275_DIAGONAL_MARGIN = NUMERICALLY_CERTIFIED_FINITE_BELOW_QUARTER",
        "TPC275_DIAGONAL_ROUTE = INSUFFICIENT_SCOPED",
        "TPC275_SOURCE_LEVEL_SIGNED_CROSS_GRAM = OPEN_ASYMPTOTIC",
        "TPC275_FIXED_POWER_CREDIT = 0",
        "TPC275_ARITHMETIC_ADVANCE = NO",
        "TPC275_L2 = NONE",
        "TPC275_FULL_GATE_B = OPEN",
        "TPC275_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC275_TWIN_PRIME_RESULT = NONE",
        "TPC275_STATUS = " + STATUS,
        "TPC275_ROUND2_CLUE = COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    flat = " ".join(text.split())
    for phrase in ("12 rows", "G-D < 0", "1 < D/G < 12/5",
                   "F/G > 50", "m_D^2<1/16", "actual source-block",
                   "twin-prime proof", "not being reused as a literal"):
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
        (PRODUCER, "TPC275_CERTIFICATE=PASS", ["--check"]),
        (INDEPENDENT, "TPC275_INDEPENDENT_CHECK=PASS", []),
        (STRESS, "TPC275_REASSEMBLY_STRESS=PASS", []),
    )
    for path, marker, args in children:
        normal = child(path, marker, False, args)
        optimized = child(path, marker, True, args)
        need(normal == optimized, "normal/optimized mismatch: " + path.name)


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object, positive: bool = False) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = fraction(value[0]), fraction(value[1])
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
         "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1",
         "certificate schema")
    parameters = payload["parameters"]
    need(parameters == {
        "diagonal_envelope": "D=sum_j ||V_j||_2^2",
        "diagonal_margin_threshold": "m_D^2<1/16",
        "diagonal_ratio_threshold": "1 < D/G < 12/5",
        "frobenius_ratio_threshold": "F/G > 50",
        "growing_cutoff_schedule": {"128": 4, "192": 5, "256": 5,
                                     "384": 5, "64": 4, "96": 4},
        "kernel_exponents": [1, 2],
        "packet_split": "four consecutive source blocks",
        "projection": "three declared four-block Haar contrasts",
        "upstream_payload_sha256":
        "ce03d5c47cd242732b21f8f71d58e009a8dc8b0521d58fdf1a587ba1a9f2affc",
        "upstream_schema":
        "TPC274_PROJECTED_OUTPUT_FROBENIUS_ENVELOPE_CERTIFICATE_V1",
    }, "certificate parameters")
    rows = payload["rows"]
    need(len(rows) == 12, "row count")
    expected_scales = {64: (15, 4), 96: (20, 5), 128: (24, 5),
                       192: (32, 6), 256: (38, 6), 384: (50, 7)}
    expected_cutoffs = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    phases = {"NEGATIVE_REAL_AXIS": 0, "POSITIVE_REAL_AXIS": 0,
              "CROSSES_ZERO": 0}
    seen: set[tuple[int, int]] = set()
    for row in rows:
        n, exponent = row["scale"], row["kernel_exponent"]
        key = (n, exponent)
        need(key not in seen, "duplicate row")
        seen.add(key)
        need(n in expected_scales and exponent in (1, 2) and
             (row["H"], row["Q"]) == expected_scales[n] and
             row["comparison_cutoff_z"] == expected_cutoffs[n] and
             row["role"] == "GROWING_CUTOFF_LITERAL_SIGNED_PACKET_REPLAY" and
             row["index_count"] == n // 2 and
             row["block_size"] == n // 8 and
             row["projected_operator"] == "A_perp=(I-P_3)A" and
             row["matrix_entry_arithmetic"] == "EXACT_RATIONAL" and
             row["packet_definition"] == "V_j=A_perp beta^(j)" and
             row["exact_signed_output_replay"] is True, "row metadata")
        packet_norms = [fraction(value) for value in row["packet_norm_squared"]]
        need(len(packet_norms) == 4 and all(value > 0 for value in packet_norms),
             "packet norms")
        gram = [[fraction(value) for value in line] for line in row["gram"]]
        need(len(gram) == 4 and all(len(line) == 4 for line in gram),
             "Gram shape")
        need(all(gram[j][k] == gram[k][j]
                 for j in range(4) for k in range(4)), "Gram symmetry")
        need(packet_norms == [gram[j][j] for j in range(4)],
             "Gram diagonal")
        diagonal = fraction(row["diagonal_packet_energy"])
        signed = fraction(row["signed_output_energy"])
        cross = fraction(row["signed_cross_sum"])
        need(diagonal == sum(packet_norms) and
             signed == sum(gram[j][k] for j in range(4) for k in range(4)) and
             cross == signed - diagonal and cross < 0 and signed > 0,
             "signed Gram expansion")
        frob = fraction(row["projected_frobenius_squared"])
        beta_norm = fraction(row["beta_norm_squared"])
        f_env = fraction(row["frobenius_envelope_energy"])
        need(frob > 0 and beta_norm > 0 and f_env == frob * beta_norm,
             "Frobenius envelope")
        ratio = fraction(row["diagonal_to_signed_ratio"])
        f_ratio = fraction(row["frobenius_to_signed_ratio"])
        need(ratio == diagonal / signed and f_ratio == f_env / signed and
             Fraction(1) < ratio < Fraction(12, 5) and f_ratio > 50,
             "energy ratios")
        margin_lo, margin_hi = interval(
            row["diagonal_margin_squared_interval"], True)
        actual_lo, actual_hi = interval(
            row["actual_output_residual_norm_squared_interval"], True)
        need(margin_lo <= margin_hi and margin_hi < Fraction(1, 16) and
             actual_lo <= actual_hi, "margin/reference intervals")
        modes = [fraction(row["dft_mode_energy"][str(k)])
                 for k in range(4)]
        need(all(value >= 0 for value in modes) and
             sum(modes) == diagonal and modes[0] * 4 == signed and
             row["dft_parseval_identity"] is True and
             row["dft_mode_zero_identity"] is True, "DFT ledger")
        probes = row["polarization"]
        need(len(probes) == 6, "polarization count")
        cursor = 0
        for j in range(4):
            for k in range(j + 1, 4):
                probe = probes[cursor]
                cursor += 1
                need((probe["left"], probe["right"]) == (j, k),
                     "polarization indices")
                plus = fraction(probe["plus_energy"])
                minus = fraction(probe["minus_energy"])
                recovered = fraction(probe["recovered_cross_term"])
                need(plus >= 0 and minus >= 0 and
                     (plus - minus) == 4 * recovered and
                     recovered == fraction(probe["gram_cross_term"]) and
                     probe["identity_holds"] is True and recovered == gram[j][k],
                     "polarization identity")
        need(row["net_cross_term_classification"] ==
             "NEGATIVE_NET_CROSS_TERM" and
             row["diagonal_gain_classification"] ==
             "BETWEEN_1_AND_12_OVER_5" and
             row["frobenius_comparison_classification"] == "ABOVE_FIFTY" and
             row["diagonal_margin_classification"] ==
             "BELOW_QUARTER_MARGIN" and
             row["phase"] in phases, "row firewall")
        phases[row["phase"]] += 1
    need(seen == {(n, exponent) for n in expected_scales for exponent in (1, 2)},
         "registered rows")
    need(phases == {"NEGATIVE_REAL_AXIS": 11,
                    "POSITIVE_REAL_AXIS": 1, "CROSSES_ZERO": 0},
         "phase census")
    theorem = payload["finite_theorem"]
    need(theorem == {
        "claim": "literal signed packet cross terms sharpen but do not close the margin route",
        "diagonal_margin_below_quarter_rows": 12,
        "diagonal_ratio_between_rows": 12,
        "dft_parseval_rows": 12,
        "frobenius_above_fifty_rows": 12,
        "kernel_pair_rows": 6,
        "net_cross_negative_rows": 12,
        "polarization_probe_rows": 72,
        "scale_rows": 6,
        "status": "NUMERICALLY_CERTIFIED_FINITE",
        "total_rows": 12,
    }, "finite theorem ledger")
    firewall = payload["firewall"]
    need(firewall == {
        "TPC275_ARITHMETIC_ADVANCE": "NO",
        "TPC275_DIAGONAL_GAIN": "NUMERICALLY_CERTIFIED_FINITE_BETWEEN_1_AND_12_OVER_5",
        "TPC275_DIAGONAL_MARGIN": "NUMERICALLY_CERTIFIED_FINITE_BELOW_QUARTER",
        "TPC275_DIAGONAL_ROUTE": "INSUFFICIENT_SCOPED",
        "TPC275_DFT_LEDGER": "PROVED_EXACT_FINITE",
        "TPC275_FIXED_POWER_CREDIT": 0,
        "TPC275_FROBENIUS_COMPARISON": "NUMERICALLY_CERTIFIED_FINITE_ABOVE_50",
        "TPC275_FULL_GATE_B": "OPEN",
        "TPC275_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        "TPC275_L2": "NONE",
        "TPC275_LITERAL_PACKET_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC275_NET_CROSS_TERM": "NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_ALL_12_ROWS",
        "TPC275_POLARIZATION": "PROVED_EXACT_FINITE",
        "TPC275_SIGNED_GRAM_IDENTITY": "PROVED_EXACT_FINITE",
        "TPC275_SOURCE_LEVEL_SIGNED_CROSS_GRAM": "OPEN_ASYMPTOTIC",
        "TPC275_STATUS": STATUS,
        "TPC275_TWIN_PRIME_RESULT": "NONE",
    }, "claim firewall")
    need(payload["round2_clue"] ==
         "COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET",
         "round2 clue")


def check_pdf() -> None:
    need(PDF.stat().st_size > 10000, "PDF too small")
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text extraction")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Signed Four-Packet Reassembly", "Liang Wang", "12 rows",
                   "INSUFFICIENT_SCOPED", "References"):
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
    need("tpc275_signed_four_packet_reassembly_certificate" not in
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
            KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        print("TPC275_BRIDGE_CHECK=FAIL " + str(error))
        return 1
    print("TPC275_BRIDGE_CHECK=PASS rows=12 cross_negative=12 "
          "diagonal_gain=12 diagonal_margin_low=12 dft_parseval=12 "
          "source_signed_cross_gram=OPEN")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
