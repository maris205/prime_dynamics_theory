#!/usr/bin/env python3
"""Exact scale, floor, profile, and polarization checks for TPC-235."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction


class CrosswalkFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CrosswalkFailure(message)


def physical_depth(h: int, Q: int, H: int) -> Fraction:
    require(all(type(v) is int and v > 0 for v in (h, Q, H)), "positive scale integers")
    return Fraction(h * Q, H)


def physical_cutoff(h: int, q: int, H: int) -> int:
    return h * q // H


def depth_cutoff(lam: Fraction, q: int, Q: int) -> int:
    value = lam * q / Q
    return value.numerator // value.denominator


def physical_profile_argument(h: int, q: int, H: int, m: int) -> Fraction:
    return Fraction(H * m, h * q)


def depth_profile_argument(lam: Fraction, q: int, Q: int, m: int) -> Fraction:
    return Fraction(m * Q, 1) / (lam * q)


def floor_profile_fixture() -> dict[str, object]:
    Q, H, h, q, m = 10, 63, 21, 17, 5
    lam = physical_depth(h, Q, H)
    first_cutoff = physical_cutoff(h, q, H)
    second_cutoff = depth_cutoff(lam, q, Q)
    first_profile = physical_profile_argument(h, q, H, m)
    second_profile = depth_profile_argument(lam, q, Q, m)
    require(lam == Fraction(10, 3), "physical depth fixture")
    require(first_cutoff == second_cutoff == 5, "cutoff crosswalk")
    require(first_profile == second_profile == Fraction(15, 17), "profile crosswalk")
    modulus_matched_depth = Fraction(h, 4 * Q)
    model_cutoff = depth_cutoff(modulus_matched_depth, q, Q)
    require(model_cutoff == 0, "modulus-matched model should miss the physical cutoff")
    return {
        "Q": Q,
        "H": H,
        "h": h,
        "q": q,
        "m": m,
        "lambda": str(lam),
        "physical_cutoff": first_cutoff,
        "depth_cutoff": second_cutoff,
        "profile_argument": str(first_profile),
        "modulus_matched_model_depth": str(modulus_matched_depth),
        "modulus_matched_model_cutoff": model_cutoff,
    }


def surrogate_fixture() -> dict[str, object]:
    Q, L, H, h = 25, 4, 2500, 400
    rows = []
    for q in (37, 47):
        physical = physical_cutoff(h, q, H)
        modeled = L * q // Q
        require(physical == modeled, "surrogate cutoff")
        rows.append({"q": q, "cutoff": physical})
    require(H == 4 * Q * Q and h == 4 * L * Q, "surrogate compatibility")
    return {"Q": Q, "L": L, "H": H, "h": h, "rows": rows, "compatible": True}


def exponent_ledger() -> dict[str, str]:
    Q = Fraction(1, 3)
    H = Fraction(21, 32)
    U = Fraction(133, 400)
    ledger = {
        "Q": Q,
        "H": H,
        "U": U,
        "Q2_over_H": 2 * Q - H,
        "H_over_Q": H - Q,
        "UQ_over_H": U + Q - H,
    }
    require(ledger["Q2_over_H"] == Fraction(1, 96), "clock gap")
    require(ledger["H_over_Q"] == Fraction(31, 96), "denominator multiplicity")
    require(ledger["UQ_over_H"] == Fraction(23, 2400), "maximum physical depth")
    return {key: str(value) for key, value in ledger.items()}


def polarization_fixture() -> dict[str, object]:
    # beta=1, w=2; squared packet magnitudes for j=0,1,2,3.
    raw_squares = (9, 5, 1, 5)
    raw_real = Fraction(raw_squares[0] - raw_squares[2], 4)
    raw_imag = Fraction(raw_squares[1] - raw_squares[3], 4)
    normalized_squares = (1, 1, 1, 1)
    normalized_real = Fraction(normalized_squares[0] - normalized_squares[2], 4)
    normalized_imag = Fraction(normalized_squares[1] - normalized_squares[3], 4)
    require((raw_real, raw_imag) == (2, 0), "raw polarization")
    require((normalized_real, normalized_imag) == (0, 0), "normalized polarization")
    return {
        "beta": 1,
        "w": 2,
        "raw_packet_squared_norms": list(raw_squares),
        "raw_polarized_value": [str(raw_real), str(raw_imag)],
        "unit_output_squared_norms": list(normalized_squares),
        "unit_output_polarized_value": [str(normalized_real), str(normalized_imag)],
        "target_cross_term": ["2", "0"],
    }


def build_certificate() -> dict[str, object]:
    floor_record = floor_profile_fixture()
    surrogate = surrogate_fixture()
    exponents = exponent_ledger()
    polarization = polarization_fixture()
    records = {"floor_profile": floor_record, "surrogate": surrogate, "exponents": exponents, "polarization": polarization}
    digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {
        "schema": "tpc235-v59-physical-depth-crosswalk-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "theorem": {
            "physical_depth": "lambda_h=hQ/H",
            "physical_row": "modulus h, cutoff floor(lambda_h q/Q), profile mQ/(lambda_h q)",
            "single_clock_iff": "exact TPC226 compatibility iff H=4Q^2 and h=4LQ",
            "v59_mismatch": "4Q^2/H=4x^(1/96)",
            "output_normalization": "REFUTED_SCOPED_FOR_V59_POLARIZATION",
        },
        "finite_reproduction": {"records": records, "digest": digest},
        "source_lock": {
            "divisor_weight_C_h": "REQUIRED",
            "full_h_sum": "REQUIRED",
            "common_packet_transform": "REQUIRED",
            "physical_h_fiber": "REQUIRED",
        },
        "firewall": {
            "tpc226_exact_single_clock_attachment": "REFUTED_SCOPED",
            "source_valid_normalization": "OPEN_WEIGHTED_LINEAR_ONLY",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
        },
    }
