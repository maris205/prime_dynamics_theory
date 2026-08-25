#!/usr/bin/env python3
"""Independent exact replay for TPC-247; imports no producer code."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc247_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_LITERAL_V59_SOURCE_OPERATOR_ATTACHMENT_WITH_NORM_OBSTRUCTION"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise Failure("duplicate key")
            output[key] = value
        return output
    return json.loads(text, object_pairs_hook=hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("nonfinite token: " + token)))


def rat(value: Any) -> Fraction:
    need(type(value) is str and value.count("/") == 1, "rational type")
    left, right = value.split("/")
    result = Fraction(int(left), int(right))
    need(f"{result.numerator}/{result.denominator}" == value, "rational canonical")
    return result


def replay(document: Any) -> None:
    need(type(document) is dict and set(document) == {
        "certificate_version", "claim_status", "payload", "payload_sha256"
    }, "document schema")
    need(type(document["certificate_version"]) is int and
         document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "status")
    payload = document["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() == document["payload_sha256"],
         "payload digest")
    fixture = payload["source_fixture"]
    indices = tuple(fixture["indices"])
    primes = tuple(fixture["primes"])
    blocks = tuple(tuple(block) for block in fixture["blocks"])
    beta = {int(key): value for key, value in fixture["beta"].items()}
    w = {int(key): value for key, value in fixture["w"].items()}
    need(indices == (2, 3, 4, 6, 8, 9) and primes == (5, 7), "frozen fixture")
    need(blocks == ((2, 3), (4, 6), (8, 9)), "blocks")

    def entry(u: int, t: int) -> Fraction:
        if u == t:
            return Fraction(0)
        output = Fraction(0)
        for prime in primes:
            if u % prime == 0 or t % prime == 0:
                continue
            output += (prime * Fraction(1, 1 + abs(u - t)) *
                       (Fraction(int(u % prime == t % prime)) -
                        Fraction(1, prime - 1)))
        return output

    direct = sum((Fraction(w[u] * beta[t]) * entry(u, t)
                  for u in indices for t in indices), Fraction(0))
    rows = fixture["block_rows"]
    need(type(rows) is list and len(rows) == 9, "block rows")
    total = Fraction(0)
    count = 0
    seen: set[tuple[int, int]] = set()
    for row in rows:
        c = row["c"]
        b = row["b"]
        need(type(c) is int and type(b) is int and (c, b) not in seen, "block label")
        seen.add((c, b))
        value = sum((Fraction(w[u] * beta[t]) * entry(u, t)
                     for u in blocks[c] for t in blocks[b]), Fraction(0))
        triples = sum((1 for u in blocks[c] for t in blocks[b] for prime in primes
                       if u != t and u % prime != 0 and t % prime != 0))
        need(rat(row["scalar"]) == value, "block scalar")
        need(type(row["admissible_triples"]) is int and
             row["admissible_triples"] == triples, "triple count")
        total += value
        count += triples
    need(total == direct == rat(fixture["direct_scalar"]) == rat(fixture["block_scalar"]),
         "scalar identity")
    need(count == fixture["admissible_triples"] and fixture["exactly_once"] is True,
         "exactly once")
    wnorm = sum((Fraction(value * value) for value in w.values()), Fraction(0))
    need(rat(fixture["w_norm2"]) == wnorm, "w norm")
    need(rat(fixture["w_external_norm2"]) == len(blocks) * wnorm,
         "w external norm")
    need(rat(fixture["counterexample_full_output_norm2"]) == 0 and
         rat(fixture["counterexample_external_norm2"]) == 2,
         "B norm counterexample")
    orientation = payload["complex_orientation_firewall"]
    need(orientation["unconjugated_physical_scalar"] == {"im": "-1/1", "re": "5/1"},
         "complex physical scalar")
    need(orientation["inner_product_with_w"] == {"im": "1/1", "re": "5/1"} and
         orientation["inner_product_with_conjugate_w"] == {"im": "-1/1", "re": "5/1"},
         "complex orientation")
    firewall = payload["scope_firewall"]
    need(firewall["ARITHMETIC_ADVANCE"] == "NO" and
         firewall["ARITHMETIC_L2"] == "NONE" and
         type(firewall["FIXED_ATOM_CREDIT"]) is int and
         firewall["FIXED_ATOM_CREDIT"] == 0, "arithmetic firewall")


def rejected(mutator: Callable[[dict[str, Any]], None], document: dict[str, Any]) -> bool:
    candidate = deepcopy(document)
    mutator(candidate)
    try:
        replay(candidate)
    except (Failure, KeyError, TypeError, ValueError, ZeroDivisionError):
        return True
    return False


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = strict(raw.decode("ascii"))
    need(raw == canonical(document) + b"\n", "canonical bytes")
    replay(document)
    attacks: list[Callable[[dict[str, Any]], None]] = [
        lambda d: d.__setitem__("certificate_version", True),
        lambda d: d.__setitem__("claim_status", "PROVED_ARITHMETIC_L2"),
        lambda d: d["payload"]["source_fixture"].__setitem__("exactly_once", False),
        lambda d: d["payload"]["source_fixture"].__setitem__("direct_scalar", "0/1"),
        lambda d: d["payload"]["source_fixture"].__setitem__("admissible_triples", 0),
        lambda d: d["payload"]["source_fixture"].__setitem__("w_external_norm2", "0/1"),
        lambda d: d["payload"]["scope_firewall"].__setitem__("ARITHMETIC_L2", "PASS"),
        lambda d: d.__setitem__("payload_sha256", "0" * 64),
    ]
    need(all(rejected(attack, document) for attack in attacks), "mutation accepted")
    digest_rebound = deepcopy(document)
    digest_rebound["payload"]["source_fixture"]["exactly_once"] = False
    digest_rebound["payload_sha256"] = hashlib.sha256(
        canonical(digest_rebound["payload"])).hexdigest()
    need(rejected(lambda d: d.update(digest_rebound), document),
         "digest-rebound mutation accepted")
    print("TPC247_INDEPENDENT_CHECK=PASS")
    print("mutations_rejected=9/9")
    print("admissible_triples=" + str(document["payload"]["source_fixture"]["admissible_triples"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC247_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        check()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, ZeroDivisionError) as error:
        raise SystemExit("TPC247_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
