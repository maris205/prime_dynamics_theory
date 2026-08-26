#!/usr/bin/env python3
"""Independent exact checker for the TPC-260 completion obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


BASELINE = "aa129b88ea2af47bcbf3473601bcb33f9b78380b"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc260_certificate.json"
CLAIM = "PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION"

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


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def frozen(relative: str) -> bytes:
    result = subprocess.run(["git", "show", BASELINE + ":" + relative],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"",
         "frozen source: " + relative)
    return result.stdout


def source_audit() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(hashlib.sha256(frozen(relative)).hexdigest() == expected,
             "source hash: " + relative)


def frame(sizes: tuple[int, int, int, int]):
    s0, s1, s2, s3 = sizes
    left, right = s0 + s1, s2 + s3
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


def dot(left, right, sizes):
    return sum((Fraction(size) * a * b
                for size, a, b in zip(sizes, left, right)), Fraction(0))


def independent_frame_audit() -> dict[str, int]:
    families = []
    for i in range(48):
        families.append((5 + 2 * i, 7 + 3 * i, 11 + 4 * i, 13 + 5 * i))
    for i in range(48):
        families.append((8 + 3 * i + (i % 2), 10 + 2 * i,
                         14 + 5 * i, 16 + 3 * i + (i % 3)))
    norms = dots = scaling = null_scaling = 0
    for sizes in families:
        specs = frame(sizes)
        scale = (Fraction(1),) * 4
        for rho2, vector in specs:
            need(dot(vector, vector, sizes) * rho2 == 1, "norm")
            need(dot(scale, vector, sizes) == 0, "scale complement")
            norms += 1
            scaling += 1
        for i in range(3):
            for j in range(i + 1, 3):
                need(dot(specs[i][1], specs[j][1], sizes) == 0,
                     "orthogonality")
                dots += 1
        need(dot(scale, specs[1][1], sizes) == 0 and
             dot(scale, specs[2][1], sizes) == 0,
             "null complement")
        null_scaling += 1
    return {"families": len(families), "norms": norms, "dots": dots,
            "scaling": scaling, "null_scaling": null_scaling}


def dft_coefficients(phases: list[tuple[int, int]]) -> list[tuple[Fraction, Fraction]]:
    roots = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    output = []
    for k in range(4):
        real = Fraction(0)
        imag = Fraction(0)
        for j, (a, b) in enumerate(phases):
            r, q = roots[(-j * k) % 4]
            real += r * a - q * b
            imag += r * b + q * a
        output.append((real / 2, imag / 2))
    return output


def gaussian_norm(value: tuple[Fraction, Fraction]) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def mode_audit() -> dict[str, tuple[str, list[str], str]]:
    families = {
        "plus": [(1, 0)] * 4,
        "alternating": [(1, 0), (-1, 0), (1, 0), (-1, 0)],
        "rotating": [(1, 0), (0, 1), (-1, 0), (0, -1)],
    }
    answer = {}
    for name, phases in families.items():
        modes = dft_coefficients(phases)
        energy = [gaussian_norm(mode) for mode in modes]
        packet_energy = sum((Fraction(a * a + b * b) for a, b in phases),
                            Fraction(0))
        aggregate = (sum(Fraction(a) for a, _ in phases),
                     sum(Fraction(b) for _, b in phases))
        full = gaussian_norm(aggregate)
        need(sum(energy, Fraction(0)) == packet_energy, "Parseval")
        need(full == 4 * energy[0], "mode zero")
        answer[name] = (str(packet_energy), [str(value) for value in energy],
                        str(full))
    need(answer["plus"][1] == ["4", "0", "0", "0"], "plus mode")
    need(answer["alternating"][1] == ["0", "0", "4", "0"],
         "alternating mode")
    return answer


def semantic(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        firewall = data["firewall"]
        modes = data["mode_audit"]
        return (
            data["schema"] == "TPC260_CERTIFICATE_V1"
            and data["claim"] == CLAIM
            and data["baseline"]["head"] == BASELINE
            and data["source_hashes"] == SOURCE_HASHES
            and firewall["TPC260_ARITHMETIC_ADVANCE"] == "NO"
            and firewall["TPC260_FULL_GATE_B"] == "OPEN"
            and firewall["TPC260_L2"] == "NONE"
            and firewall["TPC260_FIXED_ATOM_CREDIT"] == 0
            and firewall["TPC260_FULL_RESIDUAL_IDENTIFIABILITY"] == "REFUTED_SCOPED"
            and firewall["TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE"] == "NONE"
            and firewall["TPC260_TWIN_PRIME_RESULT"] == "NONE"
            and data["polygon_audit"]["equal_lengths"]["energy_min"] == "0"
            and data["polygon_audit"]["equal_lengths"]["energy_max"] == "16"
            and modes["plus"]["full_energy"] == "16"
            and modes["alternating"]["full_energy"] == "0"
            and modes["plus"]["mode_energy"] != modes["alternating"]["mode_energy"]
        )
    except (KeyError, TypeError):
        return False


def mutation_audit(data: dict[str, Any]) -> int:
    candidates = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        item = deepcopy(data)
        cursor: Any = item
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        candidates.append(item)

    mutate(("schema",), "TPC260_CERTIFICATE_V0")
    mutate(("claim",), "PROVED")
    mutate(("baseline", "head"), "0" * 40)
    mutate(("source_hashes",), {})
    mutate(("firewall", "TPC260_ARITHMETIC_ADVANCE"), "YES")
    mutate(("firewall", "TPC260_FULL_GATE_B"), "PAID")
    mutate(("firewall", "TPC260_L2"), "PAID")
    mutate(("firewall", "TPC260_FIXED_ATOM_CREDIT"), 1)
    mutate(("firewall", "TPC260_FULL_RESIDUAL_IDENTIFIABILITY"), "PROVED")
    mutate(("mode_audit", "plus", "full_energy"), "0")
    mutate(("polygon_audit", "equal_lengths", "energy_max"), "4")
    need(all(not semantic(candidate) for candidate in candidates),
         "mutation accepted")
    return len(candidates)


def run() -> None:
    source_audit()
    counts = independent_frame_audit()
    modes = mode_audit()
    need(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_text(encoding="utf-8")
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonical")
    need(semantic(data), "certificate semantics")
    need(data["mode_audit"]["plus"]["mode_energy"] == modes["plus"][1],
         "plus certificate")
    rejected = mutation_audit(data)
    print("TPC260_INDEPENDENT_CHECK=PASS "
          f"families={counts['families']} norms={counts['norms']} "
          f"dots={counts['dots']} scaling={counts['scaling']} "
          f"null_scaling={counts['null_scaling']} "
          f"modes={len(modes)} mutations_rejected={rejected} "
          "producer_imported=NO")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC260_INDEPENDENT_CHECK=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
