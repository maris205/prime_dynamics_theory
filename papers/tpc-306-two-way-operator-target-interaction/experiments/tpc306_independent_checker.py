#!/usr/bin/env python3
"""Independent replay of the TPC-306 two-way decomposition.

The checker does not import the TPC-306 producer.  It uses Decimal logarithms
to reconstruct the derived intervals from the locked TPC-305 ratio intervals,
then verifies the cell ordering, dominance identity, scaling invariance, and
the published finite census.
"""

from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-306-two-way-operator-target-interaction"
P305 = ROOT / "papers/tpc-305-counterfactual-transported-label-budget"
RESULT = PROJECT / "results/tpc306_certificate.json"
P305_CODE_HASH = "fa43b82a3a7a7adf8821cf8ebacbfadad80759b917787d00ce365e43adfd4c5d"
P305_RESULT_HASH = "e2f243ed86132af0cd4a6de169723246f3e2fdc0e4fa595fa3b1ffafe657cad3"
RESULT_HASH = "ab9eba3317e4e22d4955c15cb7a0c22e55fd0495696f34be1476985f2232a34b"
P305_STATUS = (
    "PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_"
    "NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS")
STATUS = (
    "PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS")
SCHEMA = "TPC306_TWO_WAY_OPERATOR_TARGET_INTERACTION_V1"
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")
PAIRS = ((50, 60), (60, 70), (70, 90))
SLACK = Decimal("1e-25")
getcontext().prec = 100


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


def interval(value: Any) -> tuple[Decimal, Decimal]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = Decimal(str(value[0])), Decimal(str(value[1]))
    need(lo <= hi, "interval order")
    return lo, hi


def log_interval(value: Any) -> tuple[Decimal, Decimal]:
    lo, hi = interval(value)
    need(lo > 0, "log domain")
    return lo.ln(), hi.ln()


def add(a: tuple[Decimal, Decimal], b: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[Decimal, Decimal], b: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    return a[0] - b[1], a[1] - b[0]


def neg(a: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    return -a[1], -a[0]


def half(a: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    return a[0] / 2, a[1] / 2


def mul(a: tuple[Decimal, Decimal], b: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    values = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(values), max(values)


def absolute(a: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    if a[0] >= 0:
        return a
    if a[1] <= 0:
        return -a[1], -a[0]
    return Decimal(0), max(-a[0], a[1])


def div_positive(a: tuple[Decimal, Decimal], b: tuple[Decimal, Decimal]
                ) -> tuple[Decimal, Decimal]:
    need(b[0] > 0, "positive denominator")
    return a[0] / b[1], a[1] / b[0]


def contains(stored: Any, expected: tuple[Decimal, Decimal], label: str) -> None:
    lo, hi = interval(stored)
    need(lo <= expected[0] + SLACK and hi >= expected[1] - SLACK,
         label + " does not enclose replay")


def target_preference(dl: tuple[Decimal, Decimal],
                      dr: tuple[Decimal, Decimal]) -> str:
    if dl[1] < 0 and dr[1] < 0:
        return "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    if dl[0] > 0 and dr[0] > 0:
        return "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    return "MIXED_OPERATOR_PREFERENCE"


def dominance(product: tuple[Decimal, Decimal]) -> str:
    if product[0] > 0:
        return "TARGET_MAIN_DOMINATES"
    if product[1] < 0:
        return "OPERATOR_INTERACTION_DOMINATES"
    return "DOMINANCE_UNRESOLVED"


def main() -> int:
    try:
        p305_code = P305 / "code/tpc305_counterfactual_transported_label_budget.py"
        need(digest(p305_code.read_bytes()) == P305_CODE_HASH, "TPC-305 code hash")
        p305 = load(P305 / "results/tpc305_certificate.json", P305_RESULT_HASH)
        need(p305["claim_status"] == P305_STATUS and
             p305["payload"]["schema"] ==
             "TPC305_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGET_V1",
             "TPC-305 header")
        data = load(RESULT, RESULT_HASH)
        need(data["claim_status"] == STATUS and
             data["payload"]["schema"] == SCHEMA, "TPC-306 header")
        payload = data["payload"]
        parent_cases = p305["payload"]["cases"]
        cases = payload["cases"]
        need(len(parent_cases) == 18 and len(cases) == 18, "case census")
        main_count = interaction_count = unresolved_count = 0
        pair_counts = {(50, 60): [0, 0], (60, 70): [0, 0], (70, 90): [0, 0]}
        same_prefix_main = 0
        all_main_ratios = []
        all_interaction_ratios = []
        middle_same_ratios = []
        for parent_case, case in zip(parent_cases, cases):
            key = (parent_case["from_Q"], parent_case["to_Q"],
                   parent_case["kernel_exponent"], parent_case["tau"])
            need((case["from_Q"], case["to_Q"], case["kernel_exponent"],
                  case["tau"]) == key, "case key")
            decompositions = case["decomposition_by_normalizer"]
            need(set(decompositions) == set(NORMALIZERS), "normalizer census")
            local_statuses = set()
            for name in NORMALIZERS:
                left = parent_case["left_operator"][
                    "transported_over_native_interval"][name]
                right = parent_case["right_operator"][
                    "transported_over_native_interval"][name]
                dl = log_interval(left)
                dr = neg(log_interval(right))
                main_effect = half(add(dl, dr))
                interaction = half(sub(dl, dr))
                product = mul(dl, dr)
                ratio = div_positive(absolute(interaction), absolute(main_effect))
                record = decompositions[name]
                contains(record["left_log_target_effect"], dl, "left effect")
                contains(record["right_log_target_effect"], dr, "right effect")
                contains(record["target_main_contrast"], main_effect, "main contrast")
                contains(record["operator_interaction_contrast"], interaction,
                         "interaction contrast")
                contains(record["squared_dominance_gap"], product, "dominance gap")
                contains(record["interaction_to_main_abs_ratio"], ratio,
                         "interaction/main ratio")
                # Check the exact algebra on printed interval centres as an
                # additional independent replay of m^2-i^2=d_L*d_R.
                cm = sum(interval(record["target_main_contrast"])) / 2
                ci = sum(interval(record["operator_interaction_contrast"])) / 2
                cdl = sum(interval(record["left_log_target_effect"])) / 2
                cdr = sum(interval(record["right_log_target_effect"])) / 2
                need(abs(cm * cm - ci * ci - cdl * cdr) < Decimal("1e-20"),
                     "squared dominance identity")
                pref = target_preference(dl, dr)
                dom = dominance(product)
                need(record["target_preference"] == pref and
                     record["dominance_status"] == dom, "case classification")
                local_statuses.add((pref, dom))
                bounds = interval(record["interaction_to_main_abs_ratio"])
                if dom == "TARGET_MAIN_DOMINATES":
                    all_main_ratios.append(bounds)
                elif dom == "OPERATOR_INTERACTION_DOMINATES":
                    all_interaction_ratios.append(bounds)
                if ((case["from_Q"], case["to_Q"]) == (60, 70) and
                        case["same_prefix_parent_descent"]):
                    middle_same_ratios.append(bounds)
            need(len(local_statuses) == 1, "normalizer invariant case")
            dom = case["dominance_status"]
            pair = (case["from_Q"], case["to_Q"])
            if dom == "TARGET_MAIN_DOMINATES":
                main_count += 1
                pair_counts[pair][0] += 1
                if case["same_prefix_parent_descent"]:
                    same_prefix_main += 1
            elif dom == "OPERATOR_INTERACTION_DOMINATES":
                interaction_count += 1
                pair_counts[pair][1] += 1
            else:
                unresolved_count += 1
        need((main_count, interaction_count, unresolved_count) == (12, 6, 0),
             "global dominance census")
        need(pair_counts == {(50, 60): [4, 2], (60, 70): [5, 1],
                             (70, 90): [3, 3]}, "pair dominance census")
        need(same_prefix_main == 3, "same-prefix census")
        audit = payload["finite_audit"]
        need(audit["cases"] == 18 and audit["decomposition_rows"] == 54 and
             audit["target_main_dominates_cases"] == 12 and
             audit["operator_interaction_dominates_cases"] == 6 and
             audit["unresolved_cases"] == 0 and
             audit["middle_target_main_dominates"] == 5 and
             audit["middle_same_prefix_target_main_dominates"] == 3,
             "published audit")
        need(interval(audit["max_main_ratio_interval"])[1] < Decimal("0.88") and
             interval(audit["min_interaction_ratio_interval"])[0] > Decimal("1.2") and
             interval(audit["middle_same_prefix_max_ratio_interval"])[1] < Decimal("0.64"),
             "published ratio margins")
        print("TPC306_INDEPENDENT_CHECK=PASS cases=18 decomposition_rows=54 "
              "target_main=12/18 interaction=6/18 middle=5/6 same_prefix=3/3")
        return 0
    except (Failure, OSError, json.JSONDecodeError, ArithmeticError) as error:
        print("TPC306_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
