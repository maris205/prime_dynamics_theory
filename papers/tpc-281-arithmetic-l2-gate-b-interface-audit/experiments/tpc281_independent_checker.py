#!/usr/bin/env python3
"""Independent exact replay for the TPC-281 typed-interface certificate.

This checker intentionally reconstructs the packet and interface records
without importing the release producer.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(__import__("sys"), "set_int_max_str_digits"):
    __import__("sys").set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-281-arithmetic-l2-gate-b-interface-audit"
PARENT_PROJECT = ROOT / "papers/tpc-280-leakage-aware-endpoint-compiler"
PARENT_CODE = PARENT_PROJECT / "code/tpc280_leakage_aware_endpoint_certificate.py"
PARENT = PARENT_PROJECT / "results/tpc280_certificate.json"
RESULT = PROJECT / "results/tpc281_certificate.json"
PARENT_CODE_SHA256 = "f5f3848df397d49fcfe6ca56704c23d925ec6cfb4f02654221cffdb12389e12d"
PARENT_SHA256 = "8ddf560b00133dbd2aa2132b40b714749aa94c342caf55f2a446d09c263e8228"
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


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def ftext(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def itext(value: tuple[Fraction, Fraction]) -> list[str]:
    return [ftext(value[0]), ftext(value[1])]


def inv(x: int, exponent: int) -> Fraction:
    need(x >= 1 and exponent >= 0, "power domain")
    return Fraction(1, x ** exponent)


VECTORS = (
    ("balanced_plane", ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
                         (Fraction(1), Fraction(1)), (Fraction(-1), Fraction(0)))),
    ("near_cancel_plane", ((Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)),
                            (Fraction(1), Fraction(0)), (Fraction(-29, 10), Fraction(0)))),
    ("aligned_plane", ((Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)),
                        (Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)))),
    ("mixed_plane", ((Fraction(2), Fraction(1)), (Fraction(-1), Fraction(2)),
                     (Fraction(1), Fraction(-1)), (Fraction(-1), Fraction(-1)))),
)


def dot(u: tuple[Fraction, Fraction], v: tuple[Fraction, Fraction]) -> Fraction:
    return u[0] * v[0] + u[1] * v[1]


def packet_expected(name: str, vectors: tuple[tuple[Fraction, Fraction], ...]) -> dict[str, Any]:
    source = (sum((v[0] for v in vectors), Fraction(0)),
              sum((v[1] for v in vectors), Fraction(0)))
    D = sum((dot(v, v) for v in vectors), Fraction(0))
    G = dot(source, source)
    need(D > 0 and G > 0, "fixture domain")
    parallel = source
    perpendicular = (-source[1], source[0])
    parallel_value = dot(parallel, source)
    perpendicular_value = dot(perpendicular, source)
    need(parallel_value == G and perpendicular_value == 0, "attachment")
    need(dot(parallel, parallel) == dot(perpendicular, perpendicular) == G,
         "equal norm")
    return {
        "name": name,
        "vectors": [[ftext(v[0]), ftext(v[1])] for v in vectors],
        "sum_vector": [ftext(source[0]), ftext(source[1])],
        "D": ftext(D), "G": ftext(G), "q": ftext(G / D), "r": ftext(D / G),
        "parallel_functional_norm_squared": ftext(dot(parallel, parallel)),
        "perpendicular_functional_norm_squared": ftext(dot(perpendicular, perpendicular)),
        "parallel_attachment": ftext(parallel_value),
        "perpendicular_attachment": ftext(perpendicular_value),
        "parallel_attachment_squared": ftext(parallel_value ** 2),
        "perpendicular_attachment_squared": ftext(perpendicular_value ** 2),
        "same_operator_norm": True,
        "attachment_ratio_parallel": ftext(parallel_value ** 2 / (G * G)),
        "attachment_ratio_perpendicular": ftext(Fraction(0)),
    }


def interface_expected(name: str, packet_index: int, x: int, a: int,
                       d_upper: Fraction, K: Fraction, sigma: int,
                       B: Fraction, leak: Fraction, gamma: int,
                       delta: int, packets: list[dict[str, Any]]) -> dict[str, Any]:
    packet = packets[packet_index]
    D, G = frac(packet["D"]), frac(packet["G"])
    q = G / D
    source_upper = d_upper * x ** a
    kappa = min(gamma, delta)
    q_two = B * inv(x, gamma) + leak * inv(x, delta)
    q_collapsed = (B + leak) * inv(x, kappa)
    operator_bound_sq = K * K * inv(x, 2 * sigma)
    need(D <= source_upper and q <= q_two <= q_collapsed,
         "interface budget")
    need(G <= operator_bound_sq, "operator budget")
    two_bound = operator_bound_sq * q_two * source_upper
    collapsed_bound = operator_bound_sq * q_collapsed * source_upper
    need(G * G <= two_bound <= collapsed_bound, "output budget")
    return {
        "name": name, "packet": packet["name"], "X": x, "a": a,
        "d_upper": ftext(d_upper), "source_upper": ftext(source_upper),
        "D": ftext(D), "G": ftext(G), "q": ftext(q), "K": ftext(K),
        "sigma": sigma, "B": ftext(B), "ell_over_d": ftext(leak),
        "gamma": gamma, "delta": delta, "kappa": kappa,
        "q_two_term": ftext(q_two), "q_collapsed": ftext(q_collapsed),
        "operator_norm_squared": ftext(G),
        "operator_bound_squared": ftext(operator_bound_sq),
        "parallel_attachment_squared": ftext(G * G),
        "perpendicular_attachment_squared": ftext(Fraction(0)),
        "two_term_output_bound_squared": ftext(two_bound),
        "collapsed_output_bound_squared": ftext(collapsed_bound),
        "source_upper_condition": True, "typed_operator_condition": True,
        "two_term_output_condition": True, "collapsed_output_condition": True,
    }


def load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical JSON: " + str(path))
    return data


def check() -> None:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    parent_raw = PARENT.read_bytes()
    parent = load(PARENT)
    need(digest(parent_raw) == PARENT_SHA256, "parent result provenance")
    need(parent["certificate_version"] == 1 and
         parent["claim_status"] == PARENT_STATUS, "parent header")
    need(parent["payload"]["schema"] == PARENT_SCHEMA and
         len(parent["payload"]["rows"]) == 12, "parent schema")

    raw = RESULT.read_bytes()
    data = load(RESULT)
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "certificate header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA, "certificate schema")
    need(data["payload_sha256"] == digest(canonical(payload)), "payload hash")
    exact = payload["exact_theorem"]
    need(exact == {
        "typed_two_term_L2": "||A_X S||_2^2<=K^2 X^(-2sigma) Q_X D",
        "typed_collapsed_L2": "||A_X S||_2^2<=(K^2 d_+ (B+ell/d)) X^(a-2sigma-kappa)",
        "scalar_readout": "|lambda(A_X S)|<=||lambda|| ||A_X S||_2",
        "endpoint_saving": "arithmetic sigma plus packet kappa/2",
        "conditional_scope": "requires a literal arithmetic L2 operator bound and source upper bound",
    }, "theorem fields")

    expected_packets = [packet_expected(name, vectors) for name, vectors in VECTORS]
    need(payload["packets"] == expected_packets, "packet records")
    specs = (
        ("balanced_typed_readout", 0, 8, 2, Fraction(1), Fraction(32), 1,
         Fraction(1), Fraction(0), 0, 2),
        ("near_cancel_power_lane", 1, 16, 2, Fraction(1), Fraction(4), 1,
         Fraction(1), Fraction(0), 1, 3),
        ("aligned_universal_floor", 2, 8, 2, Fraction(1), Fraction(64), 1,
         Fraction(4), Fraction(0), 0, 1),
        ("mixed_leakage_budget", 3, 16, 2, Fraction(1), Fraction(32), 1,
         Fraction(3), Fraction(1), 1, 2),
    )
    expected_interfaces = [interface_expected(*spec, expected_packets)
                           for spec in specs]
    need(payload["interface_cases"] == expected_interfaces, "interface records")

    rows = []
    for source in parent["payload"]["rows"]:
        q = interval(source["q_interval"])
        deficit = interval(source["deficit_interval"])
        sign = source["parent_deficit_sign"]
        need(0 <= q[0] <= q[1] <= 4 and deficit[0] < 1,
             "parent row domain")
        rows.append({
            "scale": int(source["scale"]), "H": int(source["H"]),
            "Q": int(source["Q"]),
            "comparison_cutoff_z": int(source["comparison_cutoff_z"]),
            "kernel_exponent": int(source["kernel_exponent"]),
            "role": source["role"], "q_interval": itext(q),
            "deficit_interval": itext(deficit),
            "parent_deficit_sign": sign,
            "source_exact_digest": source["source_exact_digest"],
            "arithmetic": "EXACT_FINITE_COORDINATE_TRANSFER_FROM_TPC280",
        })
    need(payload["rows"] == rows and len(rows) == 12, "transfer rows")
    need(sum(row["parent_deficit_sign"] == "POSITIVE_DEFICIT" for row in rows) == 8 and
         sum(row["parent_deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows) == 4,
         "transfer census")
    need(payload["finite_transfer"] == {
        "parent_schema": PARENT_SCHEMA, "parent_result_sha256": PARENT_SHA256,
        "total_rows": 12, "positive_deficit_rows": 8,
        "negative_deficit_rows": 4, "fixed_power_credit": 0,
        "asymptotic_promotion": "REFUTED_SCOPED",
    }, "transfer metadata")
    firewall = payload["firewall"]
    need(firewall == {
        "TPC281_TYPED_ARITHMETIC_L2": "PROVED_CONDITIONAL_INTERFACE_ONLY",
        "TPC281_ATTACHMENT_IDENTIFIABILITY": "REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL",
        "TPC281_FINITE_ATTACHMENT_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_4_PACKET_FIXTURES",
        "TPC281_FINITE_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC281_ARITHMETIC_ADVANCE": "NO", "TPC281_L2": "OPEN_LITERAL_SOURCE",
        "TPC281_FIXED_POWER_CREDIT": 0, "TPC281_FULL_GATE_B": "OPEN",
        "TPC281_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        "TPC281_TWIN_PRIME_RESULT": "NONE", "TPC281_STATUS": STATUS,
    }, "firewall")
    need(payload["round2_clue"] ==
         "REQUIRE_LITERAL_SOURCE_ARITHMETIC_L2_AND_TYPED_ATTACHMENT_NONDEGENERACY",
         "round2 clue")
    need(raw == canonical(data), "canonical result")
    print("TPC281_INDEPENDENT_CHECK=PASS packet_fixtures=4 interface_cases=4 "
          "transfer_rows=12 parallel_zero_pairs=4")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC281_INDEPENDENT_CHECK=FAIL: " + str(error))
