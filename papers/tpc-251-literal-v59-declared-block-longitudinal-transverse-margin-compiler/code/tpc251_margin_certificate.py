#!/usr/bin/env python3
"""Produce the exact TPC-251 declared-block margin certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any


SCHEMA = "TPC251_MARGIN_CERTIFICATE_V1"
CLAIM = "PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER"
HANDOFF_SHA256 = "c0460de36fb09655078b6040f501539a63515eebe4667b65e666995b7810912f"
FIREWALL = {
    "TPC251_HARD_PARTITION": "MODELING_CHOICE_EXHAUSTIVE_NONEMPTY",
    "TPC251_BLOCK_FLAT_DIRECTION": "MODELING_CHOICE_RELATIVE_TO_DECLARED_BLOCK",
    "TPC251_TPC243_EXTERNAL_ERROR": "CONDITIONAL_INPUT_NOT_AUTOMATIC",
    "TPC251_ACTUAL_V59_PROJECTED_COHERENCE_ASYMPTOTIC": "OPEN",
    "TPC251_PAYABLE_LONGITUDINAL_DOMINANCE": "OPEN",
    "TPC251_ARITHMETIC_ADVANCE": "NO",
    "TPC251_FIXED_ATOM_CREDIT": "0",
    "TPC251_L2": "NONE",
    "TPC251_FULL_GATE_B": "OPEN",
    "TPC251_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC251_TWIN_PRIME_RESULT": "NONE",
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _q(value: int | str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _s(value: Fraction) -> str:
    return str(value)


def _vec(values: list[int | str | Fraction]) -> list[Fraction]:
    return [_q(value) for value in values]


def _dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def _add(*vectors: list[Fraction]) -> list[Fraction]:
    return [sum(entries, Fraction(0)) for entries in zip(*vectors)]


def _sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [x - y for x, y in zip(left, right)]


def _scale(scalar: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [scalar * entry for entry in vector]


def _norm2(vector: list[Fraction]) -> Fraction:
    return _dot(vector, vector)


def _sqrt_fraction(value: Fraction) -> Fraction:
    if value < 0:
        raise ValueError("negative rational square root")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError(f"non-rational square root requested: {value}")
    return Fraction(numerator, denominator)


def _encoded_vector(vector: list[Fraction]) -> list[str]:
    return [_s(entry) for entry in vector]


def _matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [_dot(row, vector) for row in matrix]


def _project(vector: list[Fraction], block: list[int]) -> list[Fraction]:
    return [vector[index] for index in block]


def _operator_fixture() -> dict[str, Any]:
    blocks = [[0, 1, 2, 3], [4, 5, 6, 7]]
    beta = _vec([1, 0, 0, 0, 1, 0, 0, 0])
    zero = Fraction(0)
    matrix = [[zero for _ in range(8)] for _ in range(8)]
    v00 = _vec(["4/5", "1/5", "4/5", "1/5"])
    v01 = _vec(["13/20", "13/20", "-3/20", "-3/20"])
    v10 = _vec(["5/6", "-1/6", "5/6", "-1/6"])
    v11 = _vec(["1/6", "7/6", "1/6", "7/6"])
    for row, value in enumerate(v00 + v10):
        matrix[row][0] = value
    for row, value in enumerate(v01 + v11):
        matrix[row][4] = value
    w = _vec(["-1/5", "2/5", "3/5", "6/5", 1, 1, 1, 1])
    image = _matvec(matrix, beta)

    probes: dict[tuple[int, int], list[Fraction]] = {}
    projected: dict[tuple[int, int], list[Fraction]] = {}
    moments: dict[tuple[int, int], Fraction] = {}
    probe_records: list[dict[str, Any]] = []
    group_records: list[dict[str, Any]] = []
    c_long = Fraction(0)
    q_trans = Fraction(0)
    r_trans = Fraction(0)
    r_coh = Fraction(0)

    for c, output_block in enumerate(blocks):
        u = [Fraction(1, 2)] * 4
        w_c = _project(w, output_block)
        a_c = _dot(u, w_c)
        w_perp = _sub(w_c, _scale(a_c, u))
        for b, input_block in enumerate(blocks):
            beta_b = [beta[index] if index in input_block else zero for index in range(8)]
            full_probe = _matvec(matrix, beta_b)
            probe = _project(full_probe, output_block)
            moment = _dot(u, probe)
            transverse = _sub(probe, _scale(moment, u))
            probes[c, b] = probe
            projected[c, b] = transverse
            moments[c, b] = moment
            probe_records.append({
                "c": c,
                "b": b,
                "v": _encoded_vector(probe),
                "m": _s(moment),
                "v_perp": _encoded_vector(transverse),
                "d": _s(_sqrt_fraction(_norm2(transverse))),
            })
        g_c = _add(probes[c, 0], probes[c, 1])
        b_c = _dot(u, g_c)
        g_perp = _add(projected[c, 0], projected[c, 1])
        gram = [[_dot(probes[c, b], probes[c, bp]) for bp in range(2)] for b in range(2)]
        gram_perp = [[_dot(projected[c, b], projected[c, bp]) for bp in range(2)] for b in range(2)]
        distances = [_sqrt_fraction(_norm2(projected[c, b])) for b in range(2)]
        active = [b for b, distance in enumerate(distances) if distance != 0]
        mu = Fraction(0)
        if len(active) >= 2:
            mu = max(
                abs(gram_perp[b][bp]) / (distances[b] * distances[bp])
                for b in active for bp in active if b != bp
            )
        diagonal = sum((distance * distance for distance in distances), Fraction(0))
        ell_one = sum(distances, Fraction(0))
        upper2 = diagonal + mu * (ell_one * ell_one - diagonal)
        upper = _sqrt_fraction(upper2)
        transverse_norm = _sqrt_fraction(_norm2(g_perp))
        w_perp_norm = _sqrt_fraction(_norm2(w_perp))
        c_long += a_c * b_c
        q_trans += _dot(w_perp, g_perp)
        r_trans += w_perp_norm * transverse_norm
        r_coh += w_perp_norm * upper
        group_records.append({
            "c": c,
            "u": _encoded_vector(u),
            "w": _encoded_vector(w_c),
            "a": _s(a_c),
            "w_perp": _encoded_vector(w_perp),
            "g": _encoded_vector(g_c),
            "b_long": _s(b_c),
            "g_perp": _encoded_vector(g_perp),
            "gram": [[_s(entry) for entry in row] for row in gram],
            "gram_perp": [[_s(entry) for entry in row] for row in gram_perp],
            "D": _s(diagonal),
            "L": _s(ell_one),
            "mu": _s(mu),
            "U": _s(upper),
            "transverse_norm": _s(transverse_norm),
            "w_perp_norm": _s(w_perp_norm),
        })

    scalar = _dot(w, image)
    external_f = Fraction(4)
    external_e = Fraction(1, 2)
    lower_margin = max(abs(c_long) - r_coh - external_e, Fraction(0))
    if scalar != c_long + q_trans:
        raise ValueError("operator replay decomposition failed")
    if not (abs(q_trans) <= r_trans <= r_coh):
        raise ValueError("operator replay transverse bounds failed")
    if abs(external_f - scalar) > external_e:
        raise ValueError("external input is not certified")

    return {
        "label": "SYNTHETIC_EXACT_FINITE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_ARITHMETIC_INSTANCE",
        "dimension": 8,
        "blocks": blocks,
        "beta": _encoded_vector(beta),
        "A": [[_s(entry) for entry in row] for row in matrix],
        "w": _encoded_vector(w),
        "external": {"F": _s(external_f), "E": _s(external_e)},
        "derived": {
            "probes": probe_records,
            "groups": group_records,
            "C_long": _s(c_long),
            "Q_trans": _s(q_trans),
            "C_x": _s(scalar),
            "R_trans": _s(r_trans),
            "R_coh": _s(r_coh),
            "external_distance": _s(abs(external_f - c_long)),
            "external_upper": _s(r_coh + external_e),
            "lower_margin": _s(lower_margin),
            "strict_nonzero": abs(c_long) > r_coh + external_e,
        },
    }


def _complex_orientation_fixture() -> dict[str, Any]:
    return {
        "encoding": "each scalar is [real,imag] with canonical rational strings",
        "u": [["1", "0"], ["0", "0"]],
        "w": [["0", "1"], ["1", "0"]],
        "g": [["1", "1"], ["1", "0"]],
        "v1": [["1", "1"], ["1", "0"]],
        "v2": [["2", "-1"], ["0", "1"]],
        "expected": {
            "a": ["0", "1"],
            "b": ["1", "1"],
            "C_long": ["1", "-1"],
            "m1": ["1", "1"],
            "m2": ["2", "-1"],
            "G12": ["1", "-2"],
            "Gperp12": ["0", "1"],
        },
    }


def _obstruction_fixture() -> dict[str, Any]:
    return {
        "label": "EXACT_EQUALITY_OBSTRUCTION_NOT_NONVANISHING",
        "u": ["1/2", "1/2", "1/2", "1/2"],
        "t": ["1/2", "-1/2", "1/2", "-1/2"],
        "w": ["1", "0", "1", "0"],
        "g": ["0", "1", "0", "1"],
        "expected": {"C_long": "1", "Q_trans": "-1", "R_trans": "1", "C": "0"},
    }


def _edge_cases() -> list[dict[str, Any]]:
    return [
        {
            "name": "singleton_declared_block",
            "block_size": 1,
            "projected_probe_norms": ["0"],
            "D": "0",
            "L": "0",
            "mu": "0",
            "U": "0",
            "reason": "the transverse space is zero",
        },
        {
            "name": "one_active_projected_probe",
            "block_size": 4,
            "projected_probe_norms": ["3/5", "0"],
            "D": "9/25",
            "L": "3/5",
            "mu": "0",
            "U": "3/5",
            "reason": "TPC-250 empty-pair convention",
        },
    ]


def build_document() -> dict[str, Any]:
    payload = {
        "claim": CLAIM,
        "evidence_label": "EXACT_RATIONAL_STRUCTURAL_CERTIFICATE",
        "source_lock": {
            "handoff_sha256": HANDOFF_SHA256,
            "literal_weight": "lambda_cb=1",
            "partition_status": "declared exhaustive nonempty modeling choice",
            "fixed_source_disk_image": "NOT_CLAIMED",
        },
        "definitions": {
            "inner_product": "conjugate-linear first",
            "projected_gram": "Gperp_c(bb')=G_c(bb')-conjugate(m_cb)m_cb'",
            "mu_empty_pair_rule": "mu=0 when fewer than two projected probes are active",
            "R_trans": "sum_c ||w_c_perp|| ||g_c_perp||",
            "R_coh": "sum_c ||w_c_perp|| U_c",
            "external_error": "independently certified conditional input",
        },
        "firewall": FIREWALL,
        "operator_replay": _operator_fixture(),
        "complex_orientation": _complex_orientation_fixture(),
        "equality_obstruction": _obstruction_fixture(),
        "edge_cases": _edge_cases(),
        "counts": {
            "operator_replays": 1,
            "complex_orientation_fixtures": 1,
            "equality_obstructions": 1,
            "edge_cases": 2,
        },
    }
    return {"schema": SCHEMA, "payload": payload, "digest": _digest(payload)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare against the released JSON")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "tpc251_certificate.json",
    )
    args = parser.parse_args()
    document = build_document()
    if args.check:
        if not args.output.is_file():
            print(f"FAIL missing certificate: {args.output}")
            return 1
        try:
            existing = json.loads(args.output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"FAIL unreadable certificate: {error}")
            return 1
        if existing != document:
            print("FAIL released certificate differs from exact regenerated document")
            return 1
        print(
            f"PASS {SCHEMA} digest={document['digest']} "
            "operator_replays=1 orientation=1 obstructions=1 edge_cases=2"
        )
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"WROTE {args.output} digest={document['digest']} "
        "operator_replays=1 orientation=1 obstructions=1 edge_cases=2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
