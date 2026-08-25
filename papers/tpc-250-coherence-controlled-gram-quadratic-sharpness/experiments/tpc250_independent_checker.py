#!/usr/bin/env python3
"""Independently validate the TPC-250 release certificate and mutations."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "TPC250_CERTIFICATE_V1"
CLAIM = "PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS"
HANDOFF_SHA256 = "75fe9219197b41a54271df2ce4d1f15d20cd5fccd500c0a4cf4527f43c8f7357"
FIREWALL = {
    "TPC250_ACTUAL_V59_COHERENCE_ASYMPTOTIC": "OPEN",
    "TPC250_ARITHMETIC_ADVANCE": "NO",
    "TPC250_FIXED_ATOM_CREDIT": "0",
    "TPC250_L2": "NONE",
    "TPC250_FULL_GATE_B": "OPEN",
    "TPC250_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC250_TWIN_PRIME_RESULT": "NONE",
}
REQUIRED_FIXTURES = {
    "upper_equicorrelated_mu_1_over_3",
    "signed_lower_mu_2_over_5",
    "floor_regular_simplex_three",
    "floor_rational_collinear_negative_raw",
    "same_marginals_aligned",
    "same_marginals_antialigned",
    "zero_data_empty_pair",
    "singleton_active_empty_pair",
}
FRACTION_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


class CertificateError(ValueError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _payload_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _fraction(value: Any, location: str) -> Fraction:
    if not isinstance(value, str) or FRACTION_PATTERN.fullmatch(value) is None:
        raise CertificateError(f"{location}: expected canonical rational string")
    parsed = Fraction(value)
    if str(parsed) != value:
        raise CertificateError(f"{location}: rational string is not reduced canonical form")
    return parsed


def _determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    total = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            1
            for left in range(size)
            for right in range(left + 1, size)
            if permutation[left] > permutation[right]
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def _check_psd(matrix: list[list[Fraction]], name: str) -> None:
    size = len(matrix)
    for count in range(1, size + 1):
        for indices in itertools.combinations(range(size), count):
            principal = [[matrix[i][j] for j in indices] for i in indices]
            if _determinant(principal) < 0:
                raise CertificateError(f"{name}: negative principal minor at {indices}")


def _check_fixture(record: Any) -> tuple[str, dict[str, Fraction | None]]:
    if not isinstance(record, dict):
        raise CertificateError("fixture must be an object")
    required = {"name", "purpose", "gram", "weights", "unit_norms", "expected", "equality"}
    allowed = required | {"marginal_profile"}
    if set(record) != required and set(record) != allowed:
        raise CertificateError("fixture has unexpected keys")
    name = record.get("name")
    if not isinstance(name, str) or name not in REQUIRED_FIXTURES:
        raise CertificateError("fixture name is unknown")
    if not isinstance(record.get("purpose"), str) or not isinstance(record.get("equality"), str):
        raise CertificateError(f"{name}: purpose and equality must be strings")
    if record.get("unit_norms") is not True:
        raise CertificateError(f"{name}: only exact unit-norm fixtures are permitted")

    raw_weights = record.get("weights")
    raw_gram = record.get("gram")
    if not isinstance(raw_weights, list) or not isinstance(raw_gram, list) or len(raw_weights) == 0:
        raise CertificateError(f"{name}: weights and Gram must be nonempty lists")
    size = len(raw_weights)
    if len(raw_gram) != size or any(not isinstance(row, list) or len(row) != size for row in raw_gram):
        raise CertificateError(f"{name}: matrix dimension mismatch")
    weights = [_fraction(value, f"{name}.weights[{index}]") for index, value in enumerate(raw_weights)]
    gram = [
        [_fraction(value, f"{name}.gram[{row_index}][{column_index}]") for column_index, value in enumerate(row)]
        for row_index, row in enumerate(raw_gram)
    ]
    for i in range(size):
        if gram[i][i] != 1:
            raise CertificateError(f"{name}: diagonal must be one")
        for j in range(size):
            if gram[i][j] != gram[j][i]:
                raise CertificateError(f"{name}: Gram matrix must be symmetric")
    _check_psd(gram, name)

    active = [index for index, weight in enumerate(weights) if weight != 0]
    mu = Fraction(0)
    if len(active) >= 2:
        mu = max(abs(gram[i][j]) for i in active for j in active if i != j)
    diagonal = sum(weight * weight for weight in weights)
    ell_one = sum(abs(weight) for weight in weights)
    off_mass = ell_one * ell_one - diagonal
    quadratic = sum(weights[i] * gram[i][j] * weights[j] for i in range(size) for j in range(size))
    signed_lower = diagonal - mu * off_mass
    floor_lower = max(signed_lower, Fraction(0))
    upper = diagonal + mu * off_mass
    kappa = None if diagonal == 0 else ell_one * ell_one / diagonal
    calculated: dict[str, Fraction | None] = {
        "mu": mu,
        "D": diagonal,
        "L": ell_one,
        "L2_minus_D": off_mass,
        "quadratic": quadratic,
        "signed_lower": signed_lower,
        "floor_lower": floor_lower,
        "upper": upper,
        "kappa": kappa,
    }
    expected = record.get("expected")
    expected_keys = {"active_size", *calculated.keys()}
    if not isinstance(expected, dict) or set(expected) != expected_keys:
        raise CertificateError(f"{name}: expected block has wrong keys")
    if not isinstance(expected.get("active_size"), int) or isinstance(expected.get("active_size"), bool):
        raise CertificateError(f"{name}: active_size must be an integer")
    if expected["active_size"] != len(active):
        raise CertificateError(f"{name}: active_size semantic mismatch")
    for key, value in calculated.items():
        encoded = expected.get(key)
        if value is None:
            if encoded is not None:
                raise CertificateError(f"{name}: {key} must be null")
        elif _fraction(encoded, f"{name}.expected.{key}") != value:
            raise CertificateError(f"{name}: {key} semantic mismatch")
    if abs(quadratic - diagonal) > mu * off_mass or quadratic < floor_lower or quadratic > upper:
        raise CertificateError(f"{name}: theorem inequality failed")
    if diagonal > 0:
        if kappa is None or kappa < 1 or kappa > len(active):
            raise CertificateError(f"{name}: kappa range failed")
    elif kappa is not None:
        raise CertificateError(f"{name}: kappa was formed at D=0")
    return name, calculated


def check_document(document: Any) -> None:
    if not isinstance(document, dict) or set(document) != {"schema", "payload", "digest"}:
        raise CertificateError("top-level shape mismatch")
    if document.get("schema") != SCHEMA:
        raise CertificateError("schema mismatch")
    payload = document.get("payload")
    digest = document.get("digest")
    if not isinstance(payload, dict) or not isinstance(digest, str):
        raise CertificateError("payload or digest type mismatch")
    if _payload_digest(payload) != digest:
        raise CertificateError("digest mismatch")
    required_payload = {
        "claim", "evidence_label", "source_lock", "definitions", "firewall", "fixtures", "universal_sharpness_scope"
    }
    if set(payload) != required_payload:
        raise CertificateError("payload keys mismatch")
    if payload.get("claim") != CLAIM or payload.get("evidence_label") != "EXACT_FINITE_CERTIFICATE":
        raise CertificateError("claim or evidence label mismatch")
    source_lock = payload.get("source_lock")
    if not isinstance(source_lock, dict) or source_lock.get("handoff_sha256") != HANDOFF_SHA256:
        raise CertificateError("source lock hash mismatch")
    if source_lock.get("actual_v59_asymptotic") != "OPEN":
        raise CertificateError("source lock promotes the V59 asymptotic")
    definitions = payload.get("definitions")
    if not isinstance(definitions, dict) or definitions != {
        "mu_empty_pair_rule": "mu=0 when active_size<=1",
        "kappa_domain": "kappa=L^2/D only when D>0",
        "inner_product_orientation": "conjugate-linear first",
    }:
        raise CertificateError("definition ledger mismatch")
    if payload.get("firewall") != FIREWALL:
        raise CertificateError("firewall mismatch")
    if payload.get("universal_sharpness_scope") != "constants and nonnegative floor; not every arbitrary parameter tuple":
        raise CertificateError("sharpness scope mismatch")
    fixtures = payload.get("fixtures")
    if not isinstance(fixtures, list):
        raise CertificateError("fixtures must be a list")
    checked: dict[str, dict[str, Fraction | None]] = {}
    for fixture in fixtures:
        name, calculated = _check_fixture(fixture)
        if name in checked:
            raise CertificateError(f"duplicate fixture {name}")
        checked[name] = calculated
    if set(checked) != REQUIRED_FIXTURES:
        raise CertificateError("fixture coverage mismatch")
    if checked["upper_equicorrelated_mu_1_over_3"]["quadratic"] != checked["upper_equicorrelated_mu_1_over_3"]["upper"]:
        raise CertificateError("upper sharpness fixture does not saturate")
    lower = checked["signed_lower_mu_2_over_5"]
    if lower["quadratic"] != lower["signed_lower"]:
        raise CertificateError("signed lower sharpness fixture does not saturate")
    negative_floor = checked["floor_rational_collinear_negative_raw"]
    if negative_floor["quadratic"] != 0 or negative_floor["signed_lower"] is None or negative_floor["signed_lower"] >= 0:
        raise CertificateError("negative raw floor fixture failed")
    aligned = checked["same_marginals_aligned"]
    antialigned = checked["same_marginals_antialigned"]
    if aligned["D"] != antialigned["D"] or aligned["L"] != antialigned["L"]:
        raise CertificateError("same-marginal fixtures do not share marginals")
    if aligned["quadratic"] != 4 or antialigned["quadratic"] != 0:
        raise CertificateError("same-marginal endpoint values failed")


def _rebind(document: dict[str, Any]) -> None:
    document["digest"] = _payload_digest(document["payload"])


def _expect_rejection(document: dict[str, Any], label: str) -> None:
    try:
        check_document(document)
    except CertificateError:
        return
    raise CertificateError(f"mutation accepted: {label}")


def run_mutation_suite(document: dict[str, Any]) -> int:
    count = 0
    typed = copy.deepcopy(document)
    typed["payload"]["fixtures"][0]["expected"]["mu"] = 1
    _rebind(typed)
    _expect_rejection(typed, "typed_rebound_mu")
    count += 1

    semantic = copy.deepcopy(document)
    semantic["payload"]["fixtures"][0]["expected"]["quadratic"] = "999"
    _rebind(semantic)
    _expect_rejection(semantic, "semantic_rebound_quadratic")
    count += 1

    rebound = copy.deepcopy(document)
    rebound["payload"]["firewall"]["TPC250_ARITHMETIC_ADVANCE"] = "YES"
    _rebind(rebound)
    _expect_rejection(rebound, "digest_rebound_firewall")
    count += 1

    stale = copy.deepcopy(document)
    stale["payload"]["claim"] = "ALTERED"
    _expect_rejection(stale, "stale_digest")
    count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=Path(__file__).resolve().parents[1] / "results" / "tpc250_certificate.json")
    args = parser.parse_args()
    if not args.check:
        print("FAIL use --check for release validation")
        return 2
    try:
        document = json.loads(args.certificate.read_text(encoding="utf-8"))
        check_document(document)
        mutations = run_mutation_suite(document)
    except (OSError, json.JSONDecodeError, CertificateError) as error:
        print(f"FAIL {error}")
        return 1
    print(f"PASS independent_checker fixtures={len(REQUIRED_FIXTURES)} rejected_mutations={mutations} digest={document['digest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
