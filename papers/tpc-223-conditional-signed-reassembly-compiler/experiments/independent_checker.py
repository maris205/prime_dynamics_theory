#!/usr/bin/env python3
"""Independent exact checker for the TPC-223 ledger certificate."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "certificate.json"
THRESHOLD = Fraction(1, 400)


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def f(value: str) -> Fraction:
    return Fraction(value)


def recompute(record: dict[str, object]) -> dict[str, Fraction | str]:
    baseline = f(record["baseline"])
    ap = f(record["ap_saving"])
    polarized = f(record["polarized_saving"])
    loss = f(record["structural_loss"])
    weakest = min(ap, polarized)
    effective = weakest - loss
    ap_exponent = baseline - ap
    polarized_exponent = baseline - polarized
    compiled = max(ap_exponent, polarized_exponent) + loss
    target = baseline - THRESHOLD
    margin = effective - THRESHOLD
    status = "STRICT_PASS" if margin > 0 else "BORDERLINE" if margin == 0 else "NO_STRICT_SAVING"
    return {
        "weakest_channel_saving": weakest,
        "effective_saving": effective,
        "ap_exponent": ap_exponent,
        "polarized_exponent": polarized_exponent,
        "compiled_exponent": compiled,
        "target_exponent": target,
        "strict_margin": margin,
        "status": status,
    }


def main() -> int:
    try:
        data = json.loads(CERTIFICATE.read_text())
        require(data["schema"] == "tpc223-conditional-signed-reassembly-compiler-v1", "schema")
        require(data["status"] == "PASS", "status")
        require(data["claim_level"] == "CONDITIONAL_THEOREM", "claim level")
        require(data["strict_threshold"] == "1/400", "threshold")
        require(data["arithmetic_advance"] == "NO", "arithmetic firewall")
        require(data["fixed_atom_credit"] == 0, "atom firewall")
        require(data["l2"] == "NONE", "L2 firewall")
        require(data["full_gate_b"] == "OPEN", "Gate B firewall")
        require(data["strict_1_over_400"] == "UNPAID", "strict firewall")
        require(data["conditional_inputs"] == {
            "ap_dispersion": "OPEN",
            "polarized_cross_correlation": "OPEN",
            "literal_reassembly_interface": "OPEN",
        }, "conditional input status")
        records = data["records"]
        require(type(records) is list and len(records) == 5, "record count")
        expected_status = {
            "strict_endpoint": "STRICT_PASS",
            "borderline_endpoint": "BORDERLINE",
            "failed_endpoint": "NO_STRICT_SAVING",
            "missing_polarized_saving": "NO_STRICT_SAVING",
            "loss_dominates": "NO_STRICT_SAVING",
        }
        for record in records:
            require(record["name"] in expected_status, "unexpected record")
            values = recompute(record)
            for key, value in values.items():
                if key == "status":
                    require(record[key] == value, f"identity: {record['name']}:{key}")
                else:
                    require(f(record[key]) == value, f"identity: {record['name']}:{key}")
            require(record["status"] == expected_status[record["name"]], "status classification")
            require(record["conditional_inputs"] == {
                "ap_dispersion": "CONDITIONAL_ASSUMPTION",
                "polarized_cross_correlation": "CONDITIONAL_ASSUMPTION",
                "literal_reassembly_interface": "CONDITIONAL_ASSUMPTION",
            }, "record assumptions")
            require(record["assumptions_declared"] is True, "assumption declaration")
        require(all(value is True for value in data["checks"].values()), "certificate check")
        strict = next(item for item in records if item["name"] == "strict_endpoint")
        require(strict["strict_margin"] == "1/150", "strict margin")
        require(f(strict["compiled_exponent"]) == Fraction(1989, 1200), "compiled exponent")
        require(f(strict["target_exponent"]) == Fraction(1997, 1200), "target exponent")
    except (CheckFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"TPC223_INDEPENDENT_CHECK=FAIL: {error}")
        return 1
    print("TPC223_INDEPENDENT_CHECK=PASS")
    print("records=5")
    print("effective_saving=11/1200")
    print("strict_margin=1/150")
    print("conditional_inputs=3_OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
