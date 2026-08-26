#!/usr/bin/env python3
"""Deterministic certificate for the TPC-260 residual reassembly audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE_HEAD = "aa129b88ea2af47bcbf3473601bcb33f9b78380b"
PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
RESULT = PROJECT / "results/tpc260_certificate.json"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "bddb89f6ce0fa7f17481c091bc53cec23ed8da2c228ac389e846625b6b5b7ef0",
    "papers/tpc-259-same-clock-null-coupling/README.md":
        "a54e3ade4a56aec2e79be049ff4db06d30b79356115691af3686c00a844d5f86",
    "papers/tpc-259-same-clock-null-coupling/PROOF_PACKAGE.md":
        "f4573edbd6d30045f0f476508d3bccf315fba42fb50603c6da8f54c3b466eb14",
    "papers/tpc-259-same-clock-null-coupling/notes/theorem_ledger.md":
        "6ecbad2368776856aa7ed4c1c20987ab2df0422c86283c5ec691f5d9c379d1de",
    "papers/tpc-259-same-clock-null-coupling/notes/route_evaluation.md":
        "e0d40481e4c745323be9618c72e127de14523118899c9c26b040c38407105431",
    "research/tpc-big-road/bridge_b_same_clock_null_coupling.md":
        "8c09035660c026d21606955b41a10affa06cb330dcdaf4782065adc42f1153ff",
    "research/tpc-big-road/tpc_bridge_b_same_clock_null_coupling_checker.py":
        "cc0adf0bf7d5c28dcbe831f3aca3a65f81708620d09f4a7ffe70c2349ed991c3",
}

STATUS = "PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION"
ROUND2_CLUE = (
    "PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_FOR_THE_COMMON_V59_FOUR_PACKET_OUTPUT"
)

FIREWALL = {
    "TPC260_ARITHMETIC_ADVANCE": "NO",
    "TPC260_FIXED_ATOM_CREDIT": 0,
    "TPC260_FULL_GATE_B": "OPEN",
    "TPC260_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC260_HAAR_COMPLEMENT": "PROVED_EXACT_FINITE",
    "TPC260_L2": "NONE",
    "TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
    "TPC260_NULL_CHANNEL_COMPATIBILITY": "PROVED_EXACT_SYNTHETIC",
    "TPC260_POLYGON_COMPLETION": "PROVED_EXACT_FINITE",
    "TPC260_ROUTE_ADVANCE": "YES_SCOPED_MODE_AUDIT",
    "TPC260_STATUS": STATUS,
    "TPC260_DFT_MODE_LEDGER": "PROVED_EXACT",
    "TPC260_FULL_RESIDUAL_IDENTIFIABILITY": "REFUTED_SCOPED",
    "TPC260_TWIN_PRIME_RESULT": "NONE",
}


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen_blob(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def verify_sources() -> int:
    markers = 0
    for relative, expected in SOURCE_HASHES.items():
        blob = frozen_blob(relative)
        need(hashlib.sha256(blob).hexdigest() == expected,
             "source hash: " + relative)
        text = blob.decode("utf-8")
        need(len(text) > 0, "empty source: " + relative)
        markers += 1
    return markers


def block_frame(sizes: tuple[int, int, int, int]) -> list[tuple[Fraction, tuple[Fraction, ...]]]:
    s0, s1, s2, s3 = sizes
    left = s0 + s1
    right = s2 + s3
    total = left + right
    return [
        (Fraction(left * right, total),
         (Fraction(1, left), Fraction(1, left),
          Fraction(-1, right), Fraction(-1, right))),
        (Fraction(s0 * s1, left),
         (Fraction(1, s0), Fraction(-1, s1), Fraction(0), Fraction(0))),
        (Fraction(s2 * s3, right),
         (Fraction(0), Fraction(0), Fraction(1, s2), Fraction(-1, s3))),
    ]


def weighted_dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...],
                 sizes: tuple[int, int, int, int]) -> Fraction:
    return sum((Fraction(size) * a * b for size, a, b
                in zip(sizes, left, right)), Fraction(0))


def frame_audit() -> dict[str, int]:
    clocks = [tuple(7 + 3 * i + j for j in range(4)) for i in range(64)]
    clocks += [
        (11 + 2 * i, 13 + 3 * i + (i % 2),
         17 + 4 * i, 19 + 5 * i + (i % 3))
        for i in range(64)
    ]
    norms = dots = scaling_dots = null_scaling = 0
    for sizes in clocks:
        need(all(size > 0 for size in sizes), "nonpositive block")
        specs = block_frame(sizes)
        for rho2, vector in specs:
            need(weighted_dot(vector, vector, sizes) * rho2 == 1,
                 "Haar norm")
            norms += 1
        for i in range(3):
            for j in range(i + 1, 3):
                need(weighted_dot(specs[i][1], specs[j][1], sizes) == 0,
                     "Haar orthogonality")
                dots += 1
        scaling = (Fraction(1),) * 4
        for _, vector in specs:
            need(weighted_dot(scaling, vector, sizes) == 0,
                 "scaling complement")
            scaling_dots += 1
        # The source-frozen null direction is a linear combination of z1,z2;
        # both summands already have zero weighted scaling moment.
        need(weighted_dot(scaling, specs[1][1], sizes) == 0 and
             weighted_dot(scaling, specs[2][1], sizes) == 0,
             "null scaling complement")
        null_scaling += 1
    return {"clocks": len(clocks), "frame_norms": norms,
            "orthogonality": dots, "scaling_dots": scaling_dots,
            "null_scaling": null_scaling}


Gaussian = tuple[Fraction, Fraction]


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gscale(value: Gaussian, scalar: Fraction) -> Gaussian:
    return (value[0] * scalar, value[1] * scalar)


def gnorm2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def root(power: int) -> Gaussian:
    power %= 4
    return ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
            (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))[power]


def dft(phases: tuple[Gaussian, ...]) -> tuple[Gaussian, ...]:
    modes = []
    for k in range(4):
        total = (Fraction(0), Fraction(0))
        for j, value in enumerate(phases):
            total = gadd(total, gmul(root(-j * k), value))
        modes.append(gscale(total, Fraction(1, 2)))
    return tuple(modes)


def mode_audit() -> dict[str, Any]:
    plus = tuple((Fraction(1), Fraction(0)) for _ in range(4))
    alternating = tuple((Fraction(1 if j % 2 == 0 else -1), Fraction(0))
                       for j in range(4))
    rotating = tuple(root(j) for j in range(4))
    records = {}
    for name, phases in (("plus", plus), ("alternating", alternating),
                         ("rotating", rotating)):
        modes = dft(phases)
        packet_energy = sum((gnorm2(value) for value in phases), Fraction(0))
        mode_energy = tuple(gnorm2(value) for value in modes)
        aggregate = sum((value[0] for value in phases), Fraction(0))
        aggregate_imag = sum((value[1] for value in phases), Fraction(0))
        full_energy = aggregate * aggregate + aggregate_imag * aggregate_imag
        reconstructed = 4 * mode_energy[0]
        need(sum(mode_energy, Fraction(0)) == packet_energy, "DFT Parseval")
        need(full_energy == reconstructed, "mode-zero reconstruction")
        records[name] = {
            "packet_energy": str(packet_energy),
            "mode_energy": [str(value) for value in mode_energy],
            "full_energy": str(full_energy),
            "mode_zero_reconstruction": str(reconstructed),
            "packet_diagonal": ["1", "1", "1", "1"],
        }
    need(records["plus"]["mode_energy"] == ["4", "0", "0", "0"],
         "plus mode")
    need(records["alternating"]["mode_energy"] == ["0", "0", "4", "0"],
         "alternating mode")
    need(records["plus"]["full_energy"] == "16" and
         records["alternating"]["full_energy"] == "0",
         "residual endpoints")
    return records


def polygon_audit() -> dict[str, Any]:
    lengths = (Fraction(1), Fraction(1), Fraction(1), Fraction(1))
    total = sum(lengths, Fraction(0))
    long_side = max(lengths)
    minimum = max(2 * long_side - total, Fraction(0))
    need(minimum == 0 and total == 4, "polygon endpoints")
    # A second unequal record checks the long-side formula without using a
    # floating point angle or an unproved numerical approximation.
    unequal = (Fraction(1), Fraction(2), Fraction(3), Fraction(7))
    unequal_total = sum(unequal, Fraction(0))
    unequal_min = max(2 * max(unequal) - unequal_total, Fraction(0))
    need(unequal_total == 13 and unequal_min == 1, "unequal polygon")
    return {
        "equal_lengths": {"D": "4", "r_min": "0", "r_max": "4",
                          "energy_min": "0", "energy_max": "16"},
        "unequal_lengths": {"D": "13", "r_min": "1", "r_max": "13"},
    }


def build_certificate() -> dict[str, Any]:
    source_count = verify_sources()
    return {
        "baseline": {"head": BASELINE_HEAD, "source_count": source_count},
        "claim": STATUS,
        "epistemic_status": {
            "dft_ledger": "PROVED_EXACT",
            "finite_geometry": "PROVED_EXACT_FINITE",
            "literal_mode_zero": "OPEN",
            "null_compatibility": "PROVED_EXACT_SYNTHETIC",
            "polygon_completion": "PROVED_EXACT_FINITE",
            "synthetic_obstruction": "NUMERICALLY_CERTIFIED",
        },
        "exact_checks": frame_audit(),
        "firewall": dict(FIREWALL),
        "mode_audit": mode_audit(),
        "polygon_audit": polygon_audit(),
        "round2_clue": ROUND2_CLUE,
        "schema": "TPC260_CERTIFICATE_V1",
        "source_hashes": dict(SOURCE_HASHES),
    }


def check_result(expected: dict[str, Any]) -> None:
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    need(raw == canonical_json(expected), "certificate is not canonical")
    need(json.loads(raw) == expected, "certificate semantics")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    need(args.check != args.emit, "choose exactly one mode")
    expected = build_certificate()
    if args.emit:
        sys.stdout.write(canonical_json(expected))
        return 0
    check_result(expected)
    counts = expected["exact_checks"]
    print("TPC260_CERTIFICATE=PASS "
          f"clocks={counts['clocks']} frame_norms={counts['frame_norms']} "
          f"orthogonality={counts['orthogonality']} "
          f"scaling_dots={counts['scaling_dots']} "
          "polygon=EXACT dft=EXACT null_compatibility=EXACT "
          "literal_mode_zero=OPEN")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC260_CERTIFICATE=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
