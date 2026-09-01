#!/usr/bin/env python3
"""TPC-325: a pre-registered source-scale ladder for signed profiles.

TPC-324 replicated the TPC-323 profile census at new source locations.  This
release keeps one fresh source origin fixed and changes only the nested source
cardinality, testing the ladder 160, 320, 640, 1280.  The literal block engine
is imported from the locked TPC-324 implementation; all scale-specific
expectations and the certificate are owned here.  No asymptotic or arithmetic
claim is made.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC325 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc325_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-324-source-profile-holdout"
PARENT_CERT = PARENT_PROJECT / "results/tpc324_certificate.json"
PARENT_ENGINE = PARENT_PROJECT / "code/tpc324_source_profile_holdout.py"
PARENT_CERT_SHA256 = (
    "b92b119118bd0888463aa609de7d9c0cd5289dd1dedf267b9ab215034bf22e3c")
PARENT_ENGINE_SHA256 = (
    "bd487c60aedab124603be6308f80f852bc53e7c24ac44d3e78a497e182332faa")

SCHEMA = "TPC325_SCALE_LADDER_PROFILE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT"
ROUND2_CLUE = "TEST_SCALE_LADDER_SOURCE_REPLICATION_OR_SOURCE_NATIVE_ARITHMETIC_L2"

HEIGHT = 66
SOURCE_ORIGIN = 12001
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")
EXPECTED_LABELS_BY_SCALE = {
    320: {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 8, "MIXED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 4, "MIXED": 4},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 5, "MIXED": 3},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 5, "MIXED": 3},
    },
    640: {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 8, "MIXED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 5, "MIXED": 3},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 7, "MIXED": 1},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 6, "MIXED": 2},
    },
    1280: {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 8, "MIXED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 6, "MIXED": 2},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 7, "MIXED": 1},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 6, "MIXED": 2},
    },
    2560: {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 8, "MIXED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 6, "MIXED": 2},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 7, "MIXED": 1},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 6, "MIXED": 2},
    },
}
EXPECTED_ENERGY_BY_SCALE = {
    scale: {
        "all_plus": {"below_one": 1, "above_one": 7},
        "alternating_index": {"below_one": 7, "above_one": 1},
        "mod4_character": ({"below_one": 7, "above_one": 1}
                            if scale < 1280 else {"below_one": 6, "above_one": 2}),
        "half_split": {"below_one": 7, "above_one": 1},
    }
    for scale in SCALES
}

PROFILE_TOL = 1.0e-10
NUMERICAL_GUARD = 1.0e-12
EXACT_INTERVAL = (12001, 12016)
EXACT_Q = 4
EXACT_EXPONENT = 1
EXACT_DIRECT_DIGEST = (
    "b21611beb065685432544b4ee8a103e17b3b4193930fe6e4e307916f29982990")
EXACT_SIGNED_DIGEST = (
    "6dd9a73a2269de9e4c50cc5af735da81c251533307dcaf850d75607be6d4a5d6")


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def display(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def load_engine() -> Any:
    need(PARENT_ENGINE.is_file(), "TPC324 parent engine missing")
    need(digest(PARENT_ENGINE.read_bytes()) == PARENT_ENGINE_SHA256,
         "TPC324 parent engine provenance")
    spec = importlib.util.spec_from_file_location("tpc324_locked_engine",
                                                  PARENT_ENGINE)
    need(spec is not None and spec.loader is not None,
         "cannot load locked engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PANEL_INTERVALS = {
        "nested_ladder": {
            scale: (SOURCE_ORIGIN, SOURCE_ORIGIN + scale // 2 - 1)
            for scale in SCALES
        }
    }
    module.PANEL_NAMES = ("nested_ladder",)
    module.SCALES = SCALES
    return module


def exact_small_audit(engine: Any) -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = engine.shell_for(EXACT_Q)
    blocks = [[[engine.exact_entry(prime, u, t, EXACT_EXPONENT)
                for t in values] for u in values] for prime in primes]
    gram = [[sum((blocks[i][u][t] * blocks[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signs = [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    signed = sum((signs[i] * signs[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))

    def fraction_digest(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()

    need(direct > 0 and signed > 0, "exact anchor positivity")
    direct_digest = fraction_digest(direct)
    signed_digest = fraction_digest(signed)
    need(direct_digest == EXACT_DIRECT_DIGEST and
         signed_digest == EXACT_SIGNED_DIGEST, "exact anchor digest")
    return {
        "interval": list(EXACT_INTERVAL),
        "Q": EXACT_Q,
        "shell": primes,
        "exponent": EXACT_EXPONENT,
        "direct_energy_digest": direct_digest,
        "signed_energy_digest": signed_digest,
        "direct_energy_decimal": display(float(direct), 16),
        "signed_energy_decimal": display(float(signed), 16),
        "signed_over_direct_decimal": display(float(signed / direct), 16),
        "identity_exact": True,
    }


def expected_labels() -> dict[str, dict[str, int]]:
    result = {}
    for name in LAW_NAMES:
        result[name] = {label: sum(
            EXPECTED_LABELS_BY_SCALE[scale][name].get(label, 0)
            for scale in SCALES) for label in LABELS}
    return result


def expected_energy() -> dict[str, dict[str, int]]:
    result = {}
    for name in LAW_NAMES:
        result[name] = {
            side: sum(EXPECTED_ENERGY_BY_SCALE[scale][name][side]
                      for scale in SCALES)
            for side in ("below_one", "above_one")
        }
    return result


def scale_summary(rows: list[dict[str, Any]], scale: int) -> dict[str, Any]:
    selected = [row for row in rows if row["scale"] == scale]
    need(len(selected) == 8, "scale row count")
    all_plus = [row["laws"]["all_plus"] for row in selected]
    tv_lowers = [float(item["profile_tv_interval"][0]) for item in all_plus]
    energy = [float(item["energy_ratio_estimate"]) for item in all_plus]
    return {
        "scale": scale,
        "source_count": scale // 2,
        "source_interval": [SOURCE_ORIGIN, SOURCE_ORIGIN + scale // 2 - 1],
        "rows": len(selected),
        "all_plus_majorization_rows": sum(
            item["majorization"] == "SIGNED_MAJORISES_DIRECT"
            for item in all_plus),
        "all_plus_minimum_prefix_lower": display(min(
            float(item["minimum_prefix_interval"][0]) for item in all_plus), 16),
        "all_plus_tv_lower_envelope": display(min(tv_lowers), 16),
        "all_plus_energy_ratio_min": display(min(energy), 16),
        "all_plus_energy_ratio_max": display(max(energy), 16),
    }


def build_payload(engine: Any) -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC324 parent certificate lock")
    rows = [engine.row_record("nested_ladder", scale, q0, exponent)
            for scale in SCALES for q0 in engine.Q_ANCHORS
            for exponent in engine.EXPONENTS]
    need(len(rows) == 32, "row census")
    class_counts = {
        name: {label: sum(row["laws"][name]["majorization"] == label
                          for row in rows) for label in LABELS}
        for name in LAW_NAMES
    }
    energy_counts = {
        name: {
            "below_one": sum(float(row["laws"][name]["energy_ratio_estimate"]) < 1
                              for row in rows),
            "above_one": sum(float(row["laws"][name]["energy_ratio_estimate"]) > 1
                              for row in rows),
        }
        for name in LAW_NAMES
    }
    need(class_counts == expected_labels(), "profile census")
    need(energy_counts == expected_energy(), "energy census")
    summaries = [scale_summary(rows, scale) for scale in SCALES]
    tv_envelopes = [float(item["all_plus_tv_lower_envelope"])
                    for item in summaries]
    energy_maxima = [float(item["all_plus_energy_ratio_max"])
                     for item in summaries]
    need(all(item["all_plus_majorization_rows"] == 8 for item in summaries),
         "all-plus ladder majorization")
    need(all(item["all_plus_minimum_prefix_lower"] and
             float(item["all_plus_minimum_prefix_lower"]) > 0
             for item in summaries), "all-plus strict prefix")
    need(all(left > right for left, right in zip(tv_envelopes, tv_envelopes[1:])),
         "TV lower envelope is not strictly descending")
    need(all(left > right for left, right in zip(energy_maxima, energy_maxima[1:])),
         "energy upper envelope is not strictly descending")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-324 source profile holdout",
            "certificate_sha256": PARENT_CERT_SHA256,
            "engine_sha256": PARENT_ENGINE_SHA256,
        },
        "protocol": {
            "source_origin": SOURCE_ORIGIN,
            "source_scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "nested_rule": "I_N=[12001,12000+N/2] with N in {320,640,1280,2560}",
            "height": HEIGHT,
            "Q_anchors": list(engine.Q_ANCHORS),
            "kernel_exponents": list(engine.EXPONENTS),
            "domain": "ell^2(I_N)",
            "direct_gram": "G_direct=sum_p B_p^T B_p",
            "signed_gram": "G_e=C_e^T C_e, C_e=sum_p e_p B_p",
            "profile": "pi_j(G)=lambda_j(G)/tr(G), descending",
            "paths": list(engine.PATHS),
            "majorization_rule": (
                "signed cumulative-minus-direct cumulative is nonnegative "
                "at every interior rank"),
            "canonical_sign_laws": list(LAW_NAMES),
            "scale_ladder_rule": (
                "same source origin and nested cardinalities; no claim that "
                "the four rows form an asymptotic sequence"),
        },
        "exact_small_audit": exact_small_audit(engine),
        "scale_ladder": summaries,
        "finite_audit": {
            "rows": len(rows),
            "rows_per_scale": {str(scale): 8 for scale in SCALES},
            "profile_majorization_counts": class_counts,
            "energy_ratio_counts": energy_counts,
            "all_plus_strict_majorization_rows": 32,
            "all_plus_minimum_prefix_lower": display(min(
                float(row["laws"]["all_plus"]["minimum_prefix_interval"][0])
                for row in rows), 16),
            "all_plus_tv_lower_envelope_strictly_descends": True,
            "all_plus_energy_upper_envelope_strictly_descends": True,
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC325_SCALE_LADDER": "NUMERICALLY_CERTIFIED_FINITE_32_ROWS_4_SCALES",
            "TPC325_ALL_PLUS_SCALE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
            "TPC325_ALL_PLUS_PROFILE_MAJORISATION": "NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
            "TPC325_TV_ENVELOPE": "NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES",
            "TPC325_ENERGY_ENVELOPE": "NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES",
            "TPC325_ARITHMETIC_ADVANCE": "NO",
            "TPC325_FIXED_POWER_CREDIT": 0,
            "TPC325_FULL_GATE_B": "OPEN",
            "TPC325_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
    }


def build_document(engine: Any) -> dict[str, Any]:
    payload = build_payload(engine)
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate(engine: Any) -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document(engine)))


def check_certificate(engine: Any) -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored == build_document(engine), "certificate does not replay")
    print("TPC325_CERTIFICATE=PASS rows=32 scales=4 "
          "all_plus=32/32 tv_envelope=descending energy_envelope=descending")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        engine = load_engine()
        if args.write:
            write_certificate(engine)
            print("TPC325_CERTIFICATE=WRITTEN")
        else:
            check_certificate(engine)
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC325_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
