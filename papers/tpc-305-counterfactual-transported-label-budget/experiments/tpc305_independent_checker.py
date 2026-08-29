#!/usr/bin/env python3
"""Independent structural replay for the TPC-305 certificate.

This file deliberately does not import the TPC-305 producer.  It reconstructs
the parent labels, overlap alignment, native off-overlap extension, parent
case census, and every stored interval/order/orientation decision.  The
high-precision quadratic-program solve is performed by the producer; this
checker verifies that its published atlas is attached to the correct finite
protocol and is internally fail-closed.
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
PROJECT = ROOT / "papers/tpc-305-counterfactual-transported-label-budget"
P302 = ROOT / "papers/tpc-302-growing-shell-budget-gap-audit"
P303 = ROOT / "papers/tpc-303-cardinality-monotonicity-obstruction"
RESULT = PROJECT / "results/tpc305_certificate.json"

P302_CODE_HASH = "1edd94f87af501e59ddaa07a6f2c9a5d458d7cb28e0623064f51bfb3d10ae517"
P302_RESULT_HASH = "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6"
P303_CODE_HASH = "8f6112aa89899dfd5f6f5fdd90307ed9bf56ab2264d66158b064d76623b21c4c"
P303_RESULT_HASH = "4d282a8a32ac1e916ac328a2579bb25744d8a00cfca4911f14b908387391255a"
RESULT_HASH = "e2f243ed86132af0cd4a6de169723246f3e2fdc0e4fa595fa3b1ffafe657cad3"
STATUS = (
    "PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_"
    "NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS")
SCHEMA = "TPC305_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGET_V1"
Q = (50, 60, 70, 90)
PAIRS = tuple(zip(Q[:-1], Q[1:]))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
getcontext().prec = 90


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


def parent_rows(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    out: dict[tuple[int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512 and
                row.get("H") == 58 and row.get("comparison_cutoff_z") == 5 and
                row.get("Q") in Q and row.get("kernel_exponent") in EXPONENTS):
            key = (int(row["Q"]), int(row["kernel_exponent"]))
            need(key not in out, "duplicate parent row")
            shell = row["shell"]
            labels = row["weighted_target_label"]
            need(shell == sorted(shell) and len(shell) == len(labels) and
                 all(x in (-1, 1) for x in labels), "parent row shape")
            out[key] = row
    need(len(out) == 8, "parent row census")
    return out


def parent_budget_cases(data: dict[str, Any]) -> dict[tuple[int, int, int, str], dict[str, Any]]:
    out: dict[tuple[int, int, int, str], dict[str, Any]] = {}
    for series in data["payload"]["series"]:
        e = int(series["kernel_exponent"])
        tau = series["tau"]
        normalizer = series["normalizer"]
        for left_q, right_q in PAIRS:
            hit = [x for x in series["transitions"]
                   if x["from_Q"] == left_q and x["to_Q"] == right_q]
            need(len(hit) == 1, "parent transition")
            key = (left_q, right_q, e, tau)
            item = out.setdefault(key, {"by_normalizer": []})
            item["by_normalizer"].append({
                "normalizer": normalizer,
                "classification": hit[0]["classification"],
                "same_prefix": bool(hit[0]["same_prefix"]),
            })
    need(len(out) == 18, "parent case count")
    for item in out.values():
        entries = item["by_normalizer"]
        need(len(entries) == 3 and
             {x["normalizer"] for x in entries} == set(NORMALIZERS),
             "parent normalizers")
        desc = sum(x["classification"] == "DESCENT_CERTIFIED" for x in entries)
        asc = sum(x["classification"] == "ASCENT_CERTIFIED" for x in entries)
        item.update({
            "descents": desc,
            "ascents": asc,
            "unresolved": len(entries) - desc - asc,
            "same_prefix_descents": sum(
                x["classification"] == "DESCENT_CERTIFIED" and
                x["same_prefix"] for x in entries),
        })
    return out


def interval(value: Any) -> tuple[Decimal, Decimal]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = Decimal(str(value[0])), Decimal(str(value[1]))
    need(lo <= hi, "interval order")
    return lo, hi


def status(value: Any) -> str:
    lo, hi = interval(value)
    if hi < 1:
        return "BELOW_ONE_CERTIFIED"
    if lo > 1:
        return "ABOVE_ONE_CERTIFIED"
    return "ONE_INTERVAL_UNRESOLVED"


def orientation(left: str, right: str) -> str:
    if left == "BELOW_ONE_CERTIFIED" and right == "ABOVE_ONE_CERTIFIED":
        return "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    if left == "ABOVE_ONE_CERTIFIED" and right == "BELOW_ONE_CERTIFIED":
        return "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    if left == "ABOVE_ONE_CERTIFIED" and right == "ABOVE_ONE_CERTIFIED":
        return "HOME_OPERATOR_FAVORED"
    if left == "BELOW_ONE_CERTIFIED" and right == "BELOW_ONE_CERTIFIED":
        return "CROSS_TARGET_FAVORED"
    return "ORIENTATION_UNRESOLVED"


def transport(left: dict[str, Any], right: dict[str, Any]) -> tuple[list[int], list[int], list[int], int, int]:
    lm = dict(zip(left["shell"], left["weighted_target_label"]))
    rm = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(lm) & set(rm))
    need(bool(overlap), "empty overlap")
    raw = sum(lm[p] * rm[p] for p in overlap)
    sign = 1 if raw >= 0 else -1
    tl = [sign * rm[p] if p in rm else lm[p] for p in left["shell"]]
    tr = [sign * lm[p] if p in lm else rm[p] for p in right["shell"]]
    return overlap, tl, tr, raw, sign


def check_operator(record: dict[str, Any], shell: list[int]) -> None:
    need(record["shell"] == shell and
         record["shell_cardinality"] == len(shell), "operator shell")
    # The record itself uses a common native/transported schema; labels are
    # checked by the caller because the compact record stores the vectors at
    # case level.
    nk, tk, k = (record["native_threshold_k"],
                 record["transported_threshold_k"],
                 record["comparison_prefix_k"])
    need(1 <= nk <= len(PROFILE_CUTOFFS) and
         1 <= tk <= len(PROFILE_CUTOFFS) and k == max(nk, tk),
         "operator prefix")
    need(record["comparison_cutoff"] == PROFILE_CUTOFFS[k - 1],
         "operator cutoff")
    for name in NORMALIZERS:
        nb = record["native_budget_over_normalizer"][name]
        tb = record["transported_budget_over_normalizer"][name]
        ratio = record["transported_over_native_interval"][name]
        nlo, nhi = interval(nb)
        tlo, thi = interval(tb)
        rlo, rhi = interval(ratio)
        need(nlo > 0 and tlo > 0 and rlo > 0 and rlo <= rhi,
             "positive budget interval")
        # The ratio enclosure must overlap the conservative quotient interval
        # induced by the two published budget enclosures.  Decimal arithmetic
        # is sufficient because the certificate intervals are deliberately
        # much wider than their printed-rounding error.
        qlo, qhi = tlo / nhi, thi / nlo
        need(rlo <= qhi and rhi >= qlo, "ratio enclosure")
        need(record["transported_over_native_status"][name] == status(ratio),
             "ratio status")


def main() -> int:
    try:
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
        rows = parent_rows(d302)
        parent = parent_budget_cases(d303)
        data = load(RESULT, RESULT_HASH)
        need(data["claim_status"] == STATUS and
             data["payload"]["schema"] == SCHEMA, "TPC-305 header")
        payload = data["payload"]
        need(payload["parent_lock"]["tpc302_code_sha256"] == P302_CODE_HASH and
             payload["parent_lock"]["tpc302_result_sha256"] == P302_RESULT_HASH and
             payload["parent_lock"]["tpc303_code_sha256"] == P303_CODE_HASH and
             payload["parent_lock"]["tpc303_result_sha256"] == P303_RESULT_HASH,
             "parent lock")
        cases = payload["cases"]
        need(len(cases) == 18, "case count")
        expected_cases = []
        for e in EXPONENTS:
            for left_q, right_q in PAIRS:
                for tau in TAUS:
                    left, right = rows[(left_q, e)], rows[(right_q, e)]
                    overlap, tl, tr, raw, sign = transport(left, right)
                    expected_cases.append((left_q, right_q, e, tau,
                                           overlap, tl, tr, raw, sign))
        pair_counts = {pair: {} for pair in PAIRS}
        pair_same = {pair: {} for pair in PAIRS}
        for case, expected in zip(cases, expected_cases):
            left_q, right_q, e, tau, overlap, tl, tr, raw, sign = expected
            need((case["from_Q"], case["to_Q"], case["kernel_exponent"],
                  case["tau"]) == (left_q, right_q, e, tau), "case key")
            need(case["overlap_primes"] == overlap and
                 case["overlap_cardinality"] == len(overlap) and
                 case["raw_overlap_inner_product"] == raw and
                 case["optimal_alignment_sign"] == sign and
                 case["native_left_label"] == rows[(left_q, e)]["weighted_target_label"] and
                 case["native_right_label"] == rows[(right_q, e)]["weighted_target_label"] and
                 case["transported_left_label"] == tl and
                 case["transported_right_label"] == tr, "transport replay")
            pcase = parent[(left_q, right_q, e, tau)]
            need(case["parent_budget_case_census"] == pcase,
                 "parent case attachment")
            lo = case["left_operator"]
            ro = case["right_operator"]
            check_operator(lo, rows[(left_q, e)]["shell"])
            check_operator(ro, rows[(right_q, e)]["shell"])
            need(lo["operator"] == "left" and ro["operator"] == "right",
                 "operator names")
            # Native/transported vectors are not duplicated inside the compact
            # operator records; their exact copies were checked above.
            ls = lo["transported_over_native_status"]
            rs = ro["transported_over_native_status"]
            need(len(set(ls.values())) == 1 and len(set(rs.values())) == 1,
                 "normalizer invariant status")
            expected_orientation = orientation(
                ls[NORMALIZERS[0]], rs[NORMALIZERS[0]])
            need(case["target_orientation"] == expected_orientation and
                 all(value == expected_orientation for value in
                     case["target_orientation_by_normalizer"].values()),
                 "orientation replay")
            pair = (left_q, right_q)
            orient = case["target_orientation"]
            pair_counts[pair][orient] = pair_counts[pair].get(orient, 0) + 1
            if pcase["same_prefix_descents"]:
                pair_same[pair][orient] = pair_same[pair].get(orient, 0) + 1
        wanted = {
            (50, 60): {"LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 4,
                       "CROSS_TARGET_FAVORED": 2},
            (60, 70): {"RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 5,
                       "HOME_OPERATOR_FAVORED": 1},
            (70, 90): {"LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS": 3,
                       "CROSS_TARGET_FAVORED": 1,
                       "HOME_OPERATOR_FAVORED": 2},
        }
        for pair, expected_counts in wanted.items():
            got = pair_counts[pair]
            need(got == expected_counts, "pair orientation census")
            expected_summary = next(x for x in payload["pair_summary"]
                                    if (x["from_Q"], x["to_Q"]) == pair)
            need(expected_summary["orientation_counts"] == {
                name: got.get(name, 0) for name in (
                    "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
                    "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
                    "HOME_OPERATOR_FAVORED", "CROSS_TARGET_FAVORED",
                    "ORIENTATION_UNRESOLVED")}, "pair summary")
        audit = payload["finite_audit"]
        need(audit["cases"] == 18 and audit["operator_budget_tables"] == 36 and
             audit["middle_right_label_cheaper_cases"] == 5 and
             audit["middle_same_prefix_cases"] == 3 and
             audit["middle_same_prefix_right_label_cheaper_cases"] == 3 and
             audit["fixed_power_credit"] == 0, "finite audit")
        print("TPC305_INDEPENDENT_CHECK=PASS cases=18 operator_tables=36 "
              "middle_right_label_cheaper=5/6 middle_same_prefix=3/3")
        return 0
    except (Failure, OSError, json.JSONDecodeError, ArithmeticError) as error:
        print("TPC305_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
