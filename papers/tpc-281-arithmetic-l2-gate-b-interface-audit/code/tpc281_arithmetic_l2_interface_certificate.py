#!/usr/bin/env python3
"""Typed arithmetic-L2 interface theorem and attachment obstruction certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_PROJECT = ROOT / "papers/tpc-280-leakage-aware-endpoint-compiler"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc280_leakage_aware_endpoint_certificate.py"
)
PARENT_RESULT = PARENT_PROJECT / "results/tpc280_certificate.json"
RESULT = PROJECT / "results/tpc281_certificate.json"

PARENT_CODE_SHA256 = "f5f3848df397d49fcfe6ca56704c23d925ec6cfb4f02654221cffdb12389e12d"
PARENT_RESULT_SHA256 = "8ddf560b00133dbd2aa2132b40b714749aa94c342caf55f2a446d09c263e8228"
PARENT_SCHEMA = "TPC280_LEAKAGE_AWARE_ENDPOINT_COMPILER_CERTIFICATE_V1"
PARENT_STATUS = (
    "PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_"
    "NUMERICALLY_CERTIFIED_TRANSFER"
)
SCHEMA = "TPC281_ARITHMETIC_L2_GATE_B_INTERFACE_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_"
    "NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT"
)
ROUND2_CLUE = "REQUIRE_LITERAL_SOURCE_ARITHMETIC_L2_AND_TYPED_ATTACHMENT_NONDEGENERACY"


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def ftext(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval_text(value: tuple[Fraction, Fraction]) -> list[str]:
    return [ftext(value[0]), ftext(value[1])]


def parse_interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = parse_fraction(value[0]), parse_fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def normalized_hash(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def load_parent() -> dict[str, Any]:
    need(normalized_hash(PARENT_CODE) == PARENT_CODE_SHA256,
         "parent code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest_bytes(raw) == PARENT_RESULT_SHA256,
         "parent result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == PARENT_STATUS, "parent header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == PARENT_SCHEMA, "parent schema")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent rows")
    return data


Vector = tuple[Fraction, Fraction]


PACKETS: tuple[dict[str, Any], ...] = (
    {
        "name": "balanced_plane",
        "vectors": ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
                    (Fraction(1), Fraction(1)), (Fraction(-1), Fraction(0))),
    },
    {
        "name": "near_cancel_plane",
        "vectors": ((Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)),
                    (Fraction(1), Fraction(0)), (Fraction(-29, 10), Fraction(0))),
    },
    {
        "name": "aligned_plane",
        "vectors": ((Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)),
                    (Fraction(1), Fraction(0)), (Fraction(1), Fraction(0))),
    },
    {
        "name": "mixed_plane",
        "vectors": ((Fraction(2), Fraction(1)), (Fraction(-1), Fraction(2)),
                    (Fraction(1), Fraction(-1)), (Fraction(-1), Fraction(-1))),
    },
)


INTERFACE_CASES: tuple[dict[str, Any], ...] = (
    {
        "name": "balanced_typed_readout", "packet": 0, "X": 8, "a": 2,
        "d_upper": Fraction(1), "K": Fraction(32), "sigma": 1,
        "B": Fraction(1), "ell_over_d": Fraction(0), "gamma": 0, "delta": 2,
    },
    {
        "name": "near_cancel_power_lane", "packet": 1, "X": 16, "a": 2,
        "d_upper": Fraction(1), "K": Fraction(4), "sigma": 1,
        "B": Fraction(1), "ell_over_d": Fraction(0), "gamma": 1, "delta": 3,
    },
    {
        "name": "aligned_universal_floor", "packet": 2, "X": 8, "a": 2,
        "d_upper": Fraction(1), "K": Fraction(64), "sigma": 1,
        "B": Fraction(4), "ell_over_d": Fraction(0), "gamma": 0, "delta": 1,
    },
    {
        "name": "mixed_leakage_budget", "packet": 3, "X": 16, "a": 2,
        "d_upper": Fraction(1), "K": Fraction(32), "sigma": 1,
        "B": Fraction(3), "ell_over_d": Fraction(1), "gamma": 1, "delta": 2,
    },
)


def dot(u: Vector, v: Vector) -> Fraction:
    return u[0] * v[0] + u[1] * v[1]


def norm_sq(v: Vector) -> Fraction:
    return dot(v, v)


def add_vectors(vectors: tuple[Vector, ...]) -> Vector:
    return (sum((v[0] for v in vectors), Fraction(0)),
            sum((v[1] for v in vectors), Fraction(0)))


def inverse_power(x: int, exponent: int) -> Fraction:
    need(x >= 1 and exponent >= 0, "power domain")
    return Fraction(1, x ** exponent)


def packet_record(spec: dict[str, Any]) -> dict[str, Any]:
    vectors = tuple(spec["vectors"])
    source = add_vectors(vectors)
    D = sum((norm_sq(v) for v in vectors), Fraction(0))
    G = norm_sq(source)
    need(D > 0 and G > 0, "nonzero packet fixture")
    parallel = source
    perpendicular = (-source[1], source[0])
    parallel_value = dot(parallel, source)
    perpendicular_value = dot(perpendicular, source)
    need(parallel_value == G and perpendicular_value == 0,
         "attachment identities")
    need(norm_sq(parallel) == norm_sq(perpendicular) == G,
         "same operator norm")
    return {
        "name": spec["name"],
        "vectors": [[ftext(v[0]), ftext(v[1])] for v in vectors],
        "sum_vector": [ftext(source[0]), ftext(source[1])],
        "D": ftext(D), "G": ftext(G),
        "q": ftext(G / D), "r": ftext(D / G),
        "parallel_functional_norm_squared": ftext(norm_sq(parallel)),
        "perpendicular_functional_norm_squared": ftext(norm_sq(perpendicular)),
        "parallel_attachment": ftext(parallel_value),
        "perpendicular_attachment": ftext(perpendicular_value),
        "parallel_attachment_squared": ftext(parallel_value ** 2),
        "perpendicular_attachment_squared": ftext(perpendicular_value ** 2),
        "same_operator_norm": True,
        "attachment_ratio_parallel": ftext(parallel_value ** 2 / (G * G)),
        "attachment_ratio_perpendicular": ftext(Fraction(0)),
    }


def interface_record(spec: dict[str, Any], packets: list[dict[str, Any]]) -> dict[str, Any]:
    packet = packets[int(spec["packet"])]
    x, a = int(spec["X"]), int(spec["a"])
    d_upper = Fraction(spec["d_upper"])
    K = Fraction(spec["K"])
    sigma = int(spec["sigma"])
    B = Fraction(spec["B"])
    leak = Fraction(spec["ell_over_d"])
    gamma, delta = int(spec["gamma"]), int(spec["delta"])
    D, G = parse_fraction(packet["D"]), parse_fraction(packet["G"])
    q = G / D
    source_upper = d_upper * (x ** a)
    need(D <= source_upper, "source upper envelope")
    kappa = min(gamma, delta)
    q_two = B * inverse_power(x, gamma) + leak * inverse_power(x, delta)
    q_collapsed = (B + leak) * inverse_power(x, kappa)
    need(q <= q_two and q_two <= q_collapsed and q_two > 0,
         "packet gain envelope")
    operator_norm_sq = G
    operator_bound_sq = K * K * inverse_power(x, 2 * sigma)
    need(operator_norm_sq <= operator_bound_sq, "typed operator bound")
    parallel_sq = G * G
    perpendicular_sq = Fraction(0)
    two_bound_sq = operator_bound_sq * q_two * source_upper
    collapsed_bound_sq = operator_bound_sq * q_collapsed * source_upper
    need(parallel_sq <= two_bound_sq <= collapsed_bound_sq,
         "typed output envelope")
    return {
        "name": spec["name"], "packet": packet["name"], "X": x, "a": a,
        "d_upper": ftext(d_upper), "source_upper": ftext(source_upper),
        "D": ftext(D), "G": ftext(G), "q": ftext(q),
        "K": ftext(K), "sigma": sigma,
        "B": ftext(B), "ell_over_d": ftext(leak),
        "gamma": gamma, "delta": delta, "kappa": kappa,
        "q_two_term": ftext(q_two), "q_collapsed": ftext(q_collapsed),
        "operator_norm_squared": ftext(operator_norm_sq),
        "operator_bound_squared": ftext(operator_bound_sq),
        "parallel_attachment_squared": ftext(parallel_sq),
        "perpendicular_attachment_squared": ftext(perpendicular_sq),
        "two_term_output_bound_squared": ftext(two_bound_sq),
        "collapsed_output_bound_squared": ftext(collapsed_bound_sq),
        "source_upper_condition": True,
        "typed_operator_condition": True,
        "two_term_output_condition": True,
        "collapsed_output_condition": True,
    }


def transfer_parent_rows(parent: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in parent["payload"]["rows"]:
        q = parse_interval(source["q_interval"] if "q_interval" in source
                           else source["normalized_output_ratio_interval"])
        delta = parse_interval(source["deficit_interval"])
        need(Fraction(0) <= q[0] <= q[1] <= Fraction(4),
             "parent q domain")
        need(delta[0] < 1, "parent deficit domain")
        sign = source.get("parent_deficit_sign", source.get("deficit_sign"))
        digest = source.get("source_exact_digest", source.get("source_exact_digest"))
        rows.append({
            "scale": int(source["scale"]), "H": int(source["H"]),
            "Q": int(source["Q"]),
            "comparison_cutoff_z": int(source["comparison_cutoff_z"]),
            "kernel_exponent": int(source["kernel_exponent"]),
            "role": source["role"], "q_interval": interval_text(q),
            "deficit_interval": interval_text(delta),
            "parent_deficit_sign": sign,
            "source_exact_digest": digest,
            "arithmetic": "EXACT_FINITE_COORDINATE_TRANSFER_FROM_TPC280",
        })
    return rows


def theorem_payload(parent: dict[str, Any]) -> dict[str, Any]:
    packets = [packet_record(spec) for spec in PACKETS]
    interfaces = [interface_record(spec, packets) for spec in INTERFACE_CASES]
    rows = transfer_parent_rows(parent)
    need(len(packets) == 4 and len(interfaces) == 4 and len(rows) == 12,
         "certificate census")
    need(sum(row["parent_deficit_sign"] == "POSITIVE_DEFICIT" for row in rows) == 8,
         "positive parent census")
    need(sum(row["parent_deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows) == 4,
         "negative parent census")
    return {
        "schema": SCHEMA,
        "parameters": {
            "packet_space": "R^2 exact witness space; theorem is Hilbert-space typed",
            "arithmetic_operator": "A_X:H_X -> ell^2(I_X)",
            "operator_L2_hypothesis": "||A_X||_{2->2}<=K X^(-sigma)",
            "source_upper_hypothesis": "D<=d_+ X^a",
            "packet_gain_hypothesis": "G/D<=Q_X",
            "two_term_Q": "Q_X=B X^(-gamma)+(ell/d)X^(-delta)",
            "collapsed_Q": "Q_X<=(B+ell/d)X^(-kappa)",
            "kappa": "min(gamma,delta)",
        },
        "exact_theorem": {
            "typed_two_term_L2": "||A_X S||_2^2<=K^2 X^(-2sigma) Q_X D",
            "typed_collapsed_L2": "||A_X S||_2^2<=(K^2 d_+ (B+ell/d)) X^(a-2sigma-kappa)",
            "scalar_readout": "|lambda(A_X S)|<=||lambda|| ||A_X S||_2",
            "endpoint_saving": "arithmetic sigma plus packet kappa/2",
            "conditional_scope": "requires a literal arithmetic L2 operator bound and source upper bound",
        },
        "attachment_obstruction": {
            "same_geometry": "fixed packet tuple fixes D,G,q,r",
            "same_operator_norm": "u_parallel=S and u_perp=(-S_2,S_1) have equal norm",
            "parallel_output": "<u_parallel,S>=G",
            "perpendicular_output": "<u_perp,S>=0",
            "lower_attachment_identifiability": "REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL",
            "interpretation": "packet geometry and an L2 norm do not identify arithmetic attachment",
        },
        "packets": packets,
        "interface_cases": interfaces,
        "finite_transfer": {
            "parent_schema": PARENT_SCHEMA,
            "parent_result_sha256": PARENT_RESULT_SHA256,
            "total_rows": len(rows),
            "positive_deficit_rows": sum(
                row["parent_deficit_sign"] == "POSITIVE_DEFICIT" for row in rows),
            "negative_deficit_rows": sum(
                row["parent_deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows),
            "fixed_power_credit": 0,
            "asymptotic_promotion": "REFUTED_SCOPED",
        },
        "rows": rows,
        "firewall": {
            "TPC281_TYPED_ARITHMETIC_L2": "PROVED_CONDITIONAL_INTERFACE_ONLY",
            "TPC281_ATTACHMENT_IDENTIFIABILITY": "REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL",
            "TPC281_FINITE_ATTACHMENT_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_4_PACKET_FIXTURES",
            "TPC281_FINITE_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC281_ARITHMETIC_ADVANCE": "NO",
            "TPC281_L2": "OPEN_LITERAL_SOURCE",
            "TPC281_FIXED_POWER_CREDIT": 0,
            "TPC281_FULL_GATE_B": "OPEN",
            "TPC281_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC281_TWIN_PRIME_RESULT": "NONE",
            "TPC281_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    parent = load_parent()
    payload = theorem_payload(parent)
    return {
        "certificate_version": 1, "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def validate(data: dict[str, Any]) -> None:
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(data.get("payload_sha256") ==
         hashlib.sha256(canonical(payload)).hexdigest(), "payload hash")
    exact = payload["exact_theorem"]
    need(exact["typed_two_term_L2"] ==
         "||A_X S||_2^2<=K^2 X^(-2sigma) Q_X D" and
         exact["typed_collapsed_L2"] ==
         "||A_X S||_2^2<=(K^2 d_+ (B+ell/d)) X^(a-2sigma-kappa)",
         "theorem fields")
    packets = [packet_record(spec) for spec in PACKETS]
    need(payload["packets"] == packets, "packet witnesses")
    need(payload["interface_cases"] ==
         [interface_record(spec, packets) for spec in INTERFACE_CASES],
         "interface cases")
    transfer = payload["finite_transfer"]
    need(transfer == {
        "parent_schema": PARENT_SCHEMA,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "total_rows": 12, "positive_deficit_rows": 8,
        "negative_deficit_rows": 4, "fixed_power_credit": 0,
        "asymptotic_promotion": "REFUTED_SCOPED",
    }, "transfer fields")
    need(payload["rows"] == transfer_parent_rows(load_parent()),
         "parent transfer")
    firewall = payload["firewall"]
    need(firewall["TPC281_ATTACHMENT_IDENTIFIABILITY"] ==
         "REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL" and
         firewall["TPC281_L2"] == "OPEN_LITERAL_SOURCE" and
         firewall["TPC281_FIXED_POWER_CREDIT"] == 0, "firewall")


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    validate(data)
    need(data == document(), "certificate is not reproducible from parent")
    print("TPC281_CERTIFICATE=PASS theorem=TYPED_L2_INTERFACE "
          "attachment=EXACTLY_NONIDENTIFIABLE packet_fixtures=4 "
          "transfer_rows=12 fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC281_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
