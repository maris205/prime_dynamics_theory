#!/usr/bin/env python3
"""Independent replay for the TPC-304 overlap-label crosswalk.

This checker deliberately does not import the TPC-304 producer.  It reads the
two locked parent certificates, reconstructs the overlap products and the
TPC-303 transition census, and compares the resulting canonical rows with the
published TPC-304 certificate.
"""

from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-304-overlapping-shell-label-transport"
P302 = ROOT / "papers/tpc-302-growing-shell-budget-gap-audit"
P303 = ROOT / "papers/tpc-303-cardinality-monotonicity-obstruction"
RESULT = PROJECT / "results/tpc304_certificate.json"

P302_CODE_HASH = "1edd94f87af501e59ddaa07a6f2c9a5d458d7cb28e0623064f51bfb3d10ae517"
P302_RESULT_HASH = "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6"
P303_CODE_HASH = "8f6112aa89899dfd5f6f5fdd90307ed9bf56ab2264d66158b064d76623b21c4c"
P303_RESULT_HASH = "4d282a8a32ac1e916ac328a2579bb25744d8a00cfca4911f14b908387391255a"
STATUS = (
    "PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_"
    "DESCENT_LOCALIZATION")
SCHEMA = "TPC304_OVERLAPPING_SHELL_LABEL_TRANSPORT_V1"
Q = (50, 60, 70, 90)
PAIRS = tuple(zip(Q[:-1], Q[1:]))
EXPONENTS = (1, 2)
getcontext().prec = 80


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def canon(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load(path: Path, expected_hash: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " hash")
    data = json.loads(raw)
    need(raw == canon(data), path.name + " canonical")
    need(data.get("certificate_version") == 1, path.name + " version")
    need(data.get("payload_sha256") == hashlib.sha256(
        canon(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "fraction": (str(value.numerator) if value.denominator == 1 else
                      f"{value.numerator}/{value.denominator}"),
        "decimal": format(
            Decimal(value.numerator) / Decimal(value.denominator), ".28g"),
    }


def rows302(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    out: dict[tuple[int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512 and
                row.get("H") == 58 and row.get("comparison_cutoff_z") == 5 and
                row.get("Q") in Q and row.get("kernel_exponent") in EXPONENTS):
            key = (int(row["Q"]), int(row["kernel_exponent"]))
            need(key not in out, "duplicate parent row")
            shell = row["shell"]
            labels = row["weighted_target_label"]
            need(shell == sorted(shell) and len(shell) == len(labels),
                 "parent shell shape")
            need(labels[0] == 1 and all(x in (-1, 1) for x in labels),
                 "parent label shape")
            out[key] = row
    need(len(out) == 8, "parent fixed-source rows")
    return out


def transport(left: dict[str, Any], right: dict[str, Any], exponent: int) -> dict[str, Any]:
    lm = dict(zip(left["shell"], left["weighted_target_label"]))
    rm = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(lm) & set(rm))
    need(len(overlap) > 0, "empty overlap")
    a = [int(lm[p]) for p in overlap]
    b = [int(rm[p]) for p in overlap]
    raw = sum(x * y for x, y in zip(a, b))
    sign = 1 if raw >= 0 else -1
    aligned = [sign * y for y in b]
    mismatches = [p for p, x, y in zip(overlap, a, aligned) if x != y]
    matches = len(overlap) - len(mismatches)
    need(matches >= len(mismatches), "nonoptimal alignment")
    rho = Fraction(abs(raw), len(overlap))
    defect = Fraction(len(mismatches), len(overlap))
    need(defect == (1 - rho) / 2, "finite identity")
    return {
        "kernel_exponent": exponent,
        "from_Q": int(left["Q"]), "to_Q": int(right["Q"]),
        "from_shell_cardinality": int(left["shell_cardinality"]),
        "to_shell_cardinality": int(right["shell_cardinality"]),
        "overlap_primes": overlap,
        "overlap_cardinality": len(overlap),
        "left_overlap_labels": a,
        "right_overlap_labels": b,
        "optimal_alignment_sign": sign,
        "aligned_right_overlap_labels": aligned,
        "raw_inner_product": raw,
        "aligned_inner_product": abs(raw),
        "aligned_matches": matches,
        "aligned_mismatches": len(mismatches),
        "mismatch_primes": mismatches,
        "aligned_correlation": fraction_record(rho),
        "aligned_disagreement_fraction": fraction_record(defect),
        "fracture_at_correlation_one_third": rho <= Fraction(1, 3),
    }


def budget_census(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, int]]:
    out = {}
    for pair in PAIRS:
        transitions = []
        for series in data["payload"]["series"]:
            hit = [x for x in series["transitions"]
                   if (x["from_Q"], x["to_Q"]) == pair]
            need(len(hit) == 1, "missing parent transition")
            transitions.append((hit[0]["classification"],
                                bool(hit[0]["same_prefix"])))
        need(len(transitions) == 18, "transition group size")
        desc = sum(c == "DESCENT_CERTIFIED" for c, _ in transitions)
        asc = sum(c == "ASCENT_CERTIFIED" for c, _ in transitions)
        same = sum(c == "DESCENT_CERTIFIED" and sp
                   for c, sp in transitions)
        out[pair] = {"desc": desc, "asc": asc,
                     "unresolved": 18 - desc - asc, "same": same}
    return out


def main() -> int:
    p302_code = P302 / "code/tpc302_growing_shell_budget_gap_audit.py"
    p303_code = P303 / "code/tpc303_cardinality_monotonicity_obstruction.py"
    need(digest(p302_code.read_bytes()) == P302_CODE_HASH, "TPC-302 code hash")
    need(digest(p303_code.read_bytes()) == P303_CODE_HASH, "TPC-303 code hash")
    d302 = load(P302 / "results/tpc302_certificate.json", P302_RESULT_HASH)
    d303 = load(P303 / "results/tpc303_certificate.json", P303_RESULT_HASH)
    need(d302["payload"]["schema"] == "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1",
         "TPC-302 schema")
    need(d303["payload"]["schema"] == "TPC303_CARDINALITY_MONOTONICITY_OBSTRUCTION_V1",
         "TPC-303 schema")
    parent = rows302(d302)
    expected_rows = []
    for exponent in EXPONENTS:
        for left_q, right_q in PAIRS:
            expected_rows.append(transport(
                parent[(left_q, exponent)], parent[(right_q, exponent)], exponent))
    data = load(RESULT, digest(RESULT.read_bytes()))
    need(data["claim_status"] == STATUS and
         data["payload"]["schema"] == SCHEMA, "TPC-304 header")
    payload = data["payload"]
    need(payload["transport_rows"] == expected_rows, "transport replay")
    need(payload["parent_lock"]["tpc302_code_sha256"] == P302_CODE_HASH and
         payload["parent_lock"]["tpc302_result_sha256"] == P302_RESULT_HASH and
         payload["parent_lock"]["tpc303_code_sha256"] == P303_CODE_HASH and
         payload["parent_lock"]["tpc303_result_sha256"] == P303_RESULT_HASH,
         "parent lock")
    census = budget_census(d303)
    wanted = [(50, 60, Fraction(1, 2), 0, 3, 15, 0),
              (60, 70, Fraction(1, 11), 2, 15, 3, 9),
              (70, 90, Fraction(1, 2), 0, 3, 15, 0)]
    cross = payload["spine_crosswalk"]
    need(len(cross) == 3, "crosswalk group count")
    for item, (lq, rq, mean, fractures, desc, asc, same) in zip(cross, wanted):
        got = census[(lq, rq)]
        mean_record = item["mean_aligned_correlation"]
        need(item["from_Q"] == lq and item["to_Q"] == rq and
             mean_record["fraction"] == fraction_record(mean)["fraction"] and
             item["fracture_rows"] == fractures and
             got == {"desc": desc, "asc": asc,
                     "unresolved": 0, "same": same},
             "crosswalk summary")
        b = item["budget_transition_census"]
        need(b["certified_descents"] == desc and
             b["certified_ascents"] == asc and
             b["unresolved"] == 0 and
             b["same_prefix_descents"] == same,
             "embedded budget census")
    audit = payload["finite_audit"]
    need(audit["transport_rows"] == 6 and
         audit["fracture_rows_at_one_third"] == 2 and
         audit["unique_fracture_transition"] == [60, 70] and
         audit["budget_descents_by_Q_group"] == [3, 15, 3] and
         audit["same_prefix_descents_by_Q_group"] == [0, 9, 0] and
         audit["minimum_correlation_and_maximum_descent_coincide"] is True and
         audit["all_same_prefix_descents_localized_at_fracture"] is True,
         "finite audit")
    print("TPC304_INDEPENDENT_CHECK=PASS transport_rows=6 fracture_rows=2 "
          "mean_correlations=1/2,1/11,1/2 budget_descents=3,15,3 "
          "same_prefix_descents=0,9,0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, json.JSONDecodeError) as error:
        print("TPC304_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
