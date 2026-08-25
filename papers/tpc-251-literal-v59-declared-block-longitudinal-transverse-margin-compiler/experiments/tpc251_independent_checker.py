#!/usr/bin/env python3
"""Independent validator and mutation suite for the TPC-251 certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any


SCHEMA = "TPC251_MARGIN_CERTIFICATE_V1"
CLAIM = "PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER"
HANDOFF_SHA256 = "c0460de36fb09655078b6040f501539a63515eebe4667b65e666995b7810912f"
LABEL = "SYNTHETIC_EXACT_FINITE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_ARITHMETIC_INSTANCE"
FRACTION_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
FIREWALL = {
    "TPC251_HARD_PARTITION": "MODELING_CHOICE_EXHAUSTIVE_NONEMPTY",
    "TPC251_BLOCK_FLAT_DIRECTION": "MODELING_CHOICE_RELATIVE_TO_DECLARED_BLOCK",
    "TPC251_TPC243_EXTERNAL_ERROR": "CONDITIONAL_INPUT_NOT_AUTOMATIC",
    "TPC251_ACTUAL_V59_PROJECTED_COHERENCE_ASYMPTOTIC": "OPEN",
    "TPC251_PAYABLE_LONGITUDINAL_DOMINANCE": "OPEN",
    "TPC251_ARITHMETIC_ADVANCE": "NO",
    "TPC251_FIXED_ATOM_CREDIT": "0",
    "TPC251_L2": "NONE",
    "TPC251_FULL_GATE_B": "OPEN",
    "TPC251_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC251_TWIN_PRIME_RESULT": "NONE",
}


class CertificateError(ValueError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _fraction(value: Any, location: str) -> Fraction:
    if not isinstance(value, str) or FRACTION_PATTERN.fullmatch(value) is None:
        raise CertificateError(f"{location}: expected canonical rational string")
    result = Fraction(value)
    if str(result) != value:
        raise CertificateError(f"{location}: noncanonical rational string")
    return result


def _vector(value: Any, length: int, location: str) -> list[Fraction]:
    if not isinstance(value, list) or len(value) != length:
        raise CertificateError(f"{location}: vector shape mismatch")
    return [_fraction(entry, f"{location}[{index}]") for index, entry in enumerate(value)]


def _dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def _add(*vectors: list[Fraction]) -> list[Fraction]:
    return [sum(entries, Fraction(0)) for entries in zip(*vectors)]


def _sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [x - y for x, y in zip(left, right)]


def _scale(scalar: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [scalar * entry for entry in vector]


def _norm2(vector: list[Fraction]) -> Fraction:
    return _dot(vector, vector)


def _sqrt_fraction(value: Fraction, location: str) -> Fraction:
    if value < 0:
        raise CertificateError(f"{location}: negative square")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise CertificateError(f"{location}: expected rational norm")
    return Fraction(numerator, denominator)


def _matrix(value: Any, size: int, location: str) -> list[list[Fraction]]:
    if not isinstance(value, list) or len(value) != size:
        raise CertificateError(f"{location}: matrix row count mismatch")
    return [_vector(row, size, f"{location}[{index}]") for index, row in enumerate(value)]


def _matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [_dot(row, vector) for row in matrix]


def _encoded(vector: list[Fraction]) -> list[str]:
    return [str(entry) for entry in vector]


def _check_partition(blocks: Any, dimension: int) -> list[list[int]]:
    if not isinstance(blocks, list) or len(blocks) == 0:
        raise CertificateError("blocks must be a nonempty list")
    seen: list[int] = []
    checked: list[list[int]] = []
    for block in blocks:
        if not isinstance(block, list) or len(block) == 0:
            raise CertificateError("every declared block must be nonempty")
        if any(type(index) is not int for index in block):
            raise CertificateError("block indices must be exact integers")
        checked.append(block)
        seen.extend(block)
    if sorted(seen) != list(range(dimension)) or len(set(seen)) != dimension:
        raise CertificateError("declared blocks must be disjoint and exhaustive")
    return checked


def _check_operator_replay(record: Any) -> None:
    required = {"label", "dimension", "blocks", "beta", "A", "w", "external", "derived"}
    if not isinstance(record, dict) or set(record) != required:
        raise CertificateError("operator replay shape mismatch")
    if record.get("label") != LABEL:
        raise CertificateError("operator replay evidence label mismatch")
    dimension = record.get("dimension")
    if type(dimension) is not int or dimension != 8:
        raise CertificateError("operator replay dimension mismatch")
    blocks = _check_partition(record.get("blocks"), dimension)
    if len(blocks) != 2 or any(len(block) != 4 for block in blocks):
        raise CertificateError("release replay must have two four-coordinate blocks")
    beta = _vector(record.get("beta"), dimension, "operator.beta")
    matrix = _matrix(record.get("A"), dimension, "operator.A")
    w = _vector(record.get("w"), dimension, "operator.w")
    external = record.get("external")
    if not isinstance(external, dict) or set(external) != {"F", "E"}:
        raise CertificateError("external input shape mismatch")
    ext_f = _fraction(external.get("F"), "external.F")
    ext_e = _fraction(external.get("E"), "external.E")
    if ext_e < 0:
        raise CertificateError("external error must be nonnegative")
    derived = record.get("derived")
    required_derived = {
        "probes", "groups", "C_long", "Q_trans", "C_x", "R_trans", "R_coh",
        "external_distance", "external_upper", "lower_margin", "strict_nonzero",
    }
    if not isinstance(derived, dict) or set(derived) != required_derived:
        raise CertificateError("derived replay shape mismatch")

    image = _matvec(matrix, beta)
    expected_probes: list[dict[str, Any]] = []
    expected_groups: list[dict[str, Any]] = []
    probes: dict[tuple[int, int], list[Fraction]] = {}
    transverse: dict[tuple[int, int], list[Fraction]] = {}
    c_long = Fraction(0)
    q_trans = Fraction(0)
    r_trans = Fraction(0)
    r_coh = Fraction(0)
    for c, output_block in enumerate(blocks):
        u = [Fraction(1, 2)] * 4
        w_c = [w[index] for index in output_block]
        a_c = _dot(u, w_c)
        w_perp = _sub(w_c, _scale(a_c, u))
        for b, input_block in enumerate(blocks):
            beta_b = [beta[index] if index in input_block else Fraction(0) for index in range(dimension)]
            full_probe = _matvec(matrix, beta_b)
            probe = [full_probe[index] for index in output_block]
            moment = _dot(u, probe)
            probe_perp = _sub(probe, _scale(moment, u))
            probes[c, b] = probe
            transverse[c, b] = probe_perp
            expected_probes.append({
                "c": c,
                "b": b,
                "v": _encoded(probe),
                "m": str(moment),
                "v_perp": _encoded(probe_perp),
                "d": str(_sqrt_fraction(_norm2(probe_perp), "probe norm")),
            })
        g_c = _add(probes[c, 0], probes[c, 1])
        b_c = _dot(u, g_c)
        g_perp = _add(transverse[c, 0], transverse[c, 1])
        gram = [[_dot(probes[c, b], probes[c, bp]) for bp in range(2)] for b in range(2)]
        gram_perp = [[_dot(transverse[c, b], transverse[c, bp]) for bp in range(2)] for b in range(2)]
        for b in range(2):
            for bp in range(2):
                m_b = _dot(u, probes[c, b])
                m_bp = _dot(u, probes[c, bp])
                if gram_perp[b][bp] != gram[b][bp] - m_b * m_bp:
                    raise CertificateError("projected Gram subtraction failed")
        distances = [_sqrt_fraction(_norm2(transverse[c, b]), "projected norm") for b in range(2)]
        active = [b for b, distance in enumerate(distances) if distance != 0]
        mu = Fraction(0)
        if len(active) >= 2:
            mu = max(
                abs(gram_perp[b][bp]) / (distances[b] * distances[bp])
                for b in active for bp in active if b != bp
            )
        diagonal = sum((distance * distance for distance in distances), Fraction(0))
        ell_one = sum(distances, Fraction(0))
        upper = _sqrt_fraction(diagonal + mu * (ell_one * ell_one - diagonal), "coherence upper")
        transverse_norm = _sqrt_fraction(_norm2(g_perp), "group transverse norm")
        w_perp_norm = _sqrt_fraction(_norm2(w_perp), "lane transverse norm")
        c_long += a_c * b_c
        q_trans += _dot(w_perp, g_perp)
        r_trans += w_perp_norm * transverse_norm
        r_coh += w_perp_norm * upper
        expected_groups.append({
            "c": c,
            "u": _encoded(u),
            "w": _encoded(w_c),
            "a": str(a_c),
            "w_perp": _encoded(w_perp),
            "g": _encoded(g_c),
            "b_long": str(b_c),
            "g_perp": _encoded(g_perp),
            "gram": [[str(entry) for entry in row] for row in gram],
            "gram_perp": [[str(entry) for entry in row] for row in gram_perp],
            "D": str(diagonal),
            "L": str(ell_one),
            "mu": str(mu),
            "U": str(upper),
            "transverse_norm": str(transverse_norm),
            "w_perp_norm": str(w_perp_norm),
        })
    scalar = _dot(w, image)
    expected_derived = {
        "probes": expected_probes,
        "groups": expected_groups,
        "C_long": str(c_long),
        "Q_trans": str(q_trans),
        "C_x": str(scalar),
        "R_trans": str(r_trans),
        "R_coh": str(r_coh),
        "external_distance": str(abs(ext_f - c_long)),
        "external_upper": str(r_coh + ext_e),
        "lower_margin": str(max(abs(c_long) - r_coh - ext_e, Fraction(0))),
        "strict_nonzero": abs(c_long) > r_coh + ext_e,
    }
    if derived != expected_derived:
        raise CertificateError("derived operator replay semantic mismatch")
    if scalar != c_long + q_trans:
        raise CertificateError("longitudinal-transverse identity failed")
    if not (abs(q_trans) <= r_trans <= r_coh):
        raise CertificateError("transverse radius chain failed")
    if abs(ext_f - scalar) > ext_e:
        raise CertificateError("external certificate failed")
    if (c_long, q_trans, scalar, r_trans, r_coh) != (
        Fraction(11, 2), Fraction(-1), Fraction(9, 2), Fraction(1), Fraction(1)
    ):
        raise CertificateError("recommended exact replay values changed")
    if expected_derived["lower_margin"] != "4" or expected_derived["external_distance"] != "3/2":
        raise CertificateError("external equality or strict margin changed")


def _complex(value: Any, location: str) -> complex:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{location}: Gaussian rational shape mismatch")
    return complex(float(_fraction(value[0], location + ".re")), float(_fraction(value[1], location + ".im")))


def _gaussian(value: Any, location: str) -> tuple[Fraction, Fraction]:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{location}: Gaussian rational shape mismatch")
    return (_fraction(value[0], location + ".re"), _fraction(value[1], location + ".im"))


def _cadd(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (left[0] + right[0], left[1] + right[1])


def _cmul(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0])


def _cconj(value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (value[0], -value[1])


def _csub(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (left[0] - right[0], left[1] - right[1])


def _cdot(left: list[tuple[Fraction, Fraction]], right: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    total = (Fraction(0), Fraction(0))
    for x, y in zip(left, right):
        total = _cadd(total, _cmul(_cconj(x), y))
    return total


def _check_orientation(record: Any) -> None:
    required = {"encoding", "u", "w", "g", "v1", "v2", "expected"}
    if not isinstance(record, dict) or set(record) != required:
        raise CertificateError("complex orientation shape mismatch")
    vectors: dict[str, list[tuple[Fraction, Fraction]]] = {}
    for name in ("u", "w", "g", "v1", "v2"):
        raw = record.get(name)
        if not isinstance(raw, list) or len(raw) != 2:
            raise CertificateError(f"orientation.{name}: vector shape mismatch")
        vectors[name] = [_gaussian(entry, f"orientation.{name}") for entry in raw]
    expected = record.get("expected")
    if not isinstance(expected, dict) or set(expected) != {"a", "b", "C_long", "m1", "m2", "G12", "Gperp12"}:
        raise CertificateError("orientation expected shape mismatch")
    a = _cdot(vectors["u"], vectors["w"])
    b = _cdot(vectors["u"], vectors["g"])
    m1 = _cdot(vectors["u"], vectors["v1"])
    m2 = _cdot(vectors["u"], vectors["v2"])
    g12 = _cdot(vectors["v1"], vectors["v2"])
    calculated = {
        "a": a,
        "b": b,
        "C_long": _cmul(_cconj(a), b),
        "m1": m1,
        "m2": m2,
        "G12": g12,
        "Gperp12": _csub(g12, _cmul(_cconj(m1), m2)),
    }
    for key, value in calculated.items():
        if _gaussian(expected.get(key), f"orientation.expected.{key}") != value:
            raise CertificateError(f"complex conjugation semantic mismatch at {key}")
    if calculated["C_long"] == _cmul(a, b) or calculated["Gperp12"] == _csub(g12, _cmul(m1, m2)):
        raise CertificateError("orientation fixture does not distinguish missing conjugation")


def _check_obstruction(record: Any) -> None:
    if not isinstance(record, dict) or set(record) != {"label", "u", "t", "w", "g", "expected"}:
        raise CertificateError("equality obstruction shape mismatch")
    if record.get("label") != "EXACT_EQUALITY_OBSTRUCTION_NOT_NONVANISHING":
        raise CertificateError("equality obstruction label mismatch")
    u = _vector(record.get("u"), 4, "obstruction.u")
    t = _vector(record.get("t"), 4, "obstruction.t")
    w = _vector(record.get("w"), 4, "obstruction.w")
    g = _vector(record.get("g"), 4, "obstruction.g")
    a = _dot(u, w)
    b = _dot(u, g)
    w_perp = _sub(w, _scale(a, u))
    g_perp = _sub(g, _scale(b, u))
    values = {
        "C_long": a * b,
        "Q_trans": _dot(w_perp, g_perp),
        "R_trans": _sqrt_fraction(_norm2(w_perp), "obstruction w") * _sqrt_fraction(_norm2(g_perp), "obstruction g"),
        "C": _dot(w, g),
    }
    expected = record.get("expected")
    if not isinstance(expected, dict) or set(expected) != set(values):
        raise CertificateError("obstruction expected shape mismatch")
    for key, value in values.items():
        if _fraction(expected.get(key), "obstruction." + key) != value:
            raise CertificateError(f"equality obstruction mismatch at {key}")
    if values != {"C_long": Fraction(1), "Q_trans": Fraction(-1), "R_trans": Fraction(1), "C": Fraction(0)}:
        raise CertificateError("equality obstruction no longer cancels")
    if _dot(u, t) != 0 or _norm2(u) != 1 or _norm2(t) != 1:
        raise CertificateError("obstruction pair is not block-flat adapted orthonormal")


def _check_edges(records: Any) -> None:
    if not isinstance(records, list) or len(records) != 2:
        raise CertificateError("edge-case coverage mismatch")
    expected = {
        "singleton_declared_block": (1, [Fraction(0)], Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        "one_active_projected_probe": (4, [Fraction(3, 5), Fraction(0)], Fraction(9, 25), Fraction(3, 5), Fraction(0), Fraction(3, 5)),
    }
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or set(record) != {
            "name", "block_size", "projected_probe_norms", "D", "L", "mu", "U", "reason"
        }:
            raise CertificateError("edge-case shape mismatch")
        name = record.get("name")
        if not isinstance(name, str) or name not in expected or name in seen:
            raise CertificateError("edge-case name mismatch")
        seen.add(name)
        if type(record.get("block_size")) is not int or not isinstance(record.get("reason"), str):
            raise CertificateError("edge-case typed field mismatch")
        norms_raw = record.get("projected_probe_norms")
        if not isinstance(norms_raw, list):
            raise CertificateError("edge-case norms must be a list")
        values = (
            record["block_size"],
            [_fraction(value, name + ".norm") for value in norms_raw],
            _fraction(record.get("D"), name + ".D"),
            _fraction(record.get("L"), name + ".L"),
            _fraction(record.get("mu"), name + ".mu"),
            _fraction(record.get("U"), name + ".U"),
        )
        if values != expected[name]:
            raise CertificateError("edge-case semantic mismatch")


def check_document(document: Any) -> None:
    if not isinstance(document, dict) or set(document) != {"schema", "payload", "digest"}:
        raise CertificateError("top-level shape mismatch")
    if document.get("schema") != SCHEMA:
        raise CertificateError("schema mismatch")
    payload = document.get("payload")
    digest = document.get("digest")
    if not isinstance(payload, dict) or not isinstance(digest, str) or _digest(payload) != digest:
        raise CertificateError("payload digest mismatch")
    required = {
        "claim", "evidence_label", "source_lock", "definitions", "firewall", "operator_replay",
        "complex_orientation", "equality_obstruction", "edge_cases", "counts",
    }
    if set(payload) != required:
        raise CertificateError("payload shape mismatch")
    if payload.get("claim") != CLAIM or payload.get("evidence_label") != "EXACT_RATIONAL_STRUCTURAL_CERTIFICATE":
        raise CertificateError("claim or evidence label mismatch")
    source = payload.get("source_lock")
    if not isinstance(source, dict) or source != {
        "handoff_sha256": HANDOFF_SHA256,
        "literal_weight": "lambda_cb=1",
        "partition_status": "declared exhaustive nonempty modeling choice",
        "fixed_source_disk_image": "NOT_CLAIMED",
    }:
        raise CertificateError("source lock mismatch")
    definitions = payload.get("definitions")
    if not isinstance(definitions, dict) or definitions != {
        "inner_product": "conjugate-linear first",
        "projected_gram": "Gperp_c(bb')=G_c(bb')-conjugate(m_cb)m_cb'",
        "mu_empty_pair_rule": "mu=0 when fewer than two projected probes are active",
        "R_trans": "sum_c ||w_c_perp|| ||g_c_perp||",
        "R_coh": "sum_c ||w_c_perp|| U_c",
        "external_error": "independently certified conditional input",
    }:
        raise CertificateError("definition ledger mismatch")
    if payload.get("firewall") != FIREWALL:
        raise CertificateError("firewall mismatch")
    if payload.get("counts") != {
        "operator_replays": 1,
        "complex_orientation_fixtures": 1,
        "equality_obstructions": 1,
        "edge_cases": 2,
    }:
        raise CertificateError("certificate count mismatch")
    _check_operator_replay(payload.get("operator_replay"))
    _check_orientation(payload.get("complex_orientation"))
    _check_obstruction(payload.get("equality_obstruction"))
    _check_edges(payload.get("edge_cases"))


def _rebind(document: dict[str, Any]) -> None:
    document["digest"] = _digest(document["payload"])


def _reject(document: dict[str, Any], label: str) -> None:
    try:
        check_document(document)
    except CertificateError:
        return
    raise CertificateError(f"mutation accepted: {label}")


def run_mutations(document: dict[str, Any], raw_text: str) -> int:
    mutations: list[tuple[str, list[Any]]] = []
    cases: list[tuple[str, dict[str, Any], bool]] = []

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["dimension"] = True
    cases.append(("typed_bool_dimension", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["blocks"][1] = []
    cases.append(("empty_block", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["blocks"][1][-1] = 6
    cases.append(("nonexhaustive_duplicate_partition", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["beta"][0] = "2"
    cases.append(("operator_probe_semantics", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["derived"]["groups"][0]["gram_perp"][0][1] = "1/10"
    cases.append(("projected_gram_subtraction", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["derived"]["C_long"] = 5
    cases.append(("typed_longitudinal", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["operator_replay"]["derived"]["groups"][0]["U"] = "6/5"
    cases.append(("coherence_upper", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["complex_orientation"]["expected"]["C_long"] = ["-1", "1"]
    cases.append(("missing_longitudinal_conjugation", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["complex_orientation"]["expected"]["Gperp12"] = ["-2", "-3"]
    cases.append(("missing_gram_conjugation", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["equality_obstruction"]["expected"]["C"] = "1"
    cases.append(("equality_implies_nonzero", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["firewall"]["TPC251_ARITHMETIC_ADVANCE"] = "YES"
    cases.append(("arithmetic_promotion", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["source_lock"]["handoff_sha256"] = "0" * 64
    cases.append(("source_hash_rebound", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["edge_cases"][1]["mu"] = "1"
    cases.append(("empty_pair_mu", mutated, True))

    for label, mutated, rebind in cases:
        if rebind:
            _rebind(mutated)
        _reject(mutated, label)

    stale = copy.deepcopy(document)
    stale["payload"]["operator_replay"]["external"]["E"] = "3/5"
    _reject(stale, "stale_digest")

    duplicate_text = raw_text.replace('"schema":', '"schema":"DUPLICATE",\n  "schema":', 1)
    try:
        _strict_loads(duplicate_text)
    except CertificateError:
        pass
    else:
        raise CertificateError("mutation accepted: duplicate_json_key")
    return len(cases) + 2


def _strict_loads(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CertificateError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        return json.loads(text, object_pairs_hook=hook, parse_constant=lambda value: (_ for _ in ()).throw(CertificateError(f"nonfinite JSON: {value}")))
    except json.JSONDecodeError as error:
        raise CertificateError(f"invalid JSON: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate release and run mutation suite")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "tpc251_certificate.json",
    )
    args = parser.parse_args()
    if not args.check:
        parser.error("the independent checker is read-only; pass --check")
    try:
        raw_text = args.input.read_text(encoding="utf-8")
        document = _strict_loads(raw_text)
        check_document(document)
        mutation_count = run_mutations(document, raw_text)
    except (OSError, CertificateError) as error:
        print(f"FAIL {error}")
        return 1
    print(
        f"PASS {SCHEMA} digest={document['digest']} mutations_rejected={mutation_count} "
        "operator_replays=1 orientation=1 obstructions=1 edge_cases=2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
