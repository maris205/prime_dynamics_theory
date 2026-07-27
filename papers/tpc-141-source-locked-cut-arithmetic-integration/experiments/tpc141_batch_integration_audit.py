#!/usr/bin/env python3
"""Deterministic source-lock and integration audit for TPC-141.

Default mode writes the frozen batch manifest and the derived audit JSON.
``--check`` performs no writes and compares both committed artifacts byte
for byte.  The program checks certificate syntax and exact finite
bookkeeping only; it does not estimate an arithmetic correlation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
SCHEMA_PATH = HERE / "tpc141_batch_manifest.schema.json"
MANIFEST_PATH = HERE / "tpc141_batch_manifest.json"
AUDIT_PATH = HERE / "tpc141_batch_integration_audit.json"

SCHEMA_NAME = "tpc-141-source-locked-batch-manifest-v1"
VALID_STATUSES = {
    "PROVED",
    "CONDITIONAL",
    "OPEN",
    "NOT_TESTABLE",
    "REFUTED",
}
VALID_LEVELS = {
    "L0",
    "L1",
    "L1_CONDITIONAL",
    "L2_TARGET_POSITIVE",
    "L2_NEGATIVE",
}
VALID_DIRECTIONS = {"POSITIVE", "NEGATIVE", "NEUTRAL"}
FORBIDDEN_PRIMITIVE_INPUTS = {
    "B_h0_delta_is_oX",
    "target_H3_packet_saving",
    "target_D_lower_bound",
    "target_Z_upper_bound",
}

SOURCE_TITLES = {
    133: "executable native entrance",
    134: "boundary-complete dyadic prefix-tail archive",
    135: "eligible/frontier domain cover",
    136: "complete cut archive",
    137: "fixed-data affine logarithmic closure",
    138: "shift-one firewall and restricted affine corridor",
    139: "small-polylog corridor and growing-data phase diagram",
    140: "exceptional-scale selector and power-ledger interface",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def fraction_record(value: Fraction) -> dict[str, int]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


def parse_fraction(record: dict[str, int]) -> Fraction:
    denominator = record["denominator"]
    if denominator <= 0:
        raise ValueError("fraction denominator must be positive")
    return Fraction(record["numerator"], denominator)


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def find_source_dir(number: int) -> Path:
    matches = sorted(
        path
        for path in PAPERS_DIR.glob(f"tpc-{number}-*")
        if path.is_dir()
    )
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one TPC-{number} directory, found {len(matches)}"
        )
    return matches[0]


def source_bundle(number: int) -> dict[str, Any]:
    directory = find_source_dir(number)
    required = ["main.tex", "README.md", "references.bib"]
    for name in required:
        if not (directory / name).is_file():
            raise FileNotFoundError(f"TPC-{number} lacks required file {name}")

    files: list[Path] = [directory / name for name in required]
    experiments = directory / "experiments"
    if experiments.is_dir():
        files.extend(
            path
            for path in experiments.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix in {".py", ".json"}
        )
    files = sorted(set(files), key=lambda path: path.as_posix())
    file_hashes = {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in files
    }
    bundle_hash = sha256_bytes(
        canonical_json(file_hashes).encode("utf-8")
    )
    return {
        "paper": f"TPC-{number}",
        "directory": directory.name,
        "title_role": SOURCE_TITLES[number],
        "files": file_hashes,
        "bundle_sha256": bundle_hash,
    }


def topo_order(graph: dict[str, tuple[str, ...]]) -> list[str]:
    indegree = {node: 0 for node in graph}
    children = {node: [] for node in graph}
    for node, parents in graph.items():
        for parent in parents:
            if parent not in graph:
                raise ValueError(f"unknown DAG parent {parent}")
            indegree[node] += 1
            children[parent].append(node)
    queue = sorted(node for node, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(order) != len(graph):
        raise ValueError("cyclic proof DAG")
    return order


def validate_order(
    graph: dict[str, tuple[str, ...]],
    order: list[str],
) -> None:
    if len(order) != len(set(order)) or set(order) != set(graph):
        raise ValueError("topological order does not exactly cover DAG")
    position = {node: index for index, node in enumerate(order)}
    for node, parents in graph.items():
        if any(position[parent] >= position[node] for parent in parents):
            raise ValueError("declared order is not topological")


def ancestor_closure(
    graph: dict[str, tuple[str, ...]],
    node_id: str,
) -> set[str]:
    """Return every direct or indirect parent of ``node_id``."""

    seen: set[str] = set()
    stack = list(graph[node_id])
    while stack:
        parent = stack.pop()
        if parent in seen:
            continue
        seen.add(parent)
        stack.extend(graph[parent])
    return seen


def primitive_leaves(
    token_id: str,
    tokens: dict[str, dict[str, Any]],
    cache: dict[str, frozenset[str]],
) -> frozenset[str]:
    if token_id in cache:
        return cache[token_id]
    token = tokens[token_id]
    dependencies = token["dependencies"]
    if not dependencies:
        leaves = frozenset({token_id})
    else:
        if token_id in dependencies:
            raise ValueError("self-dependent occurrence token")
        leaves = frozenset().union(
            *(
                primitive_leaves(dependency, tokens, cache)
                for dependency in dependencies
            )
        )
        if not leaves:
            raise ValueError("joint occurrence token has no leaves")
    cache[token_id] = leaves
    return leaves


def canonical_occurrence_registry(
    primitive: list[dict[str, Any]],
    joints: list[dict[str, Any]],
) -> tuple[list[str], set[str], bool]:
    tokens: dict[str, dict[str, Any]] = {}
    for token in primitive + joints:
        token_id = token["occurrence_id"]
        if token_id in tokens:
            raise ValueError("duplicate occurrence identifier")
        if token["scale"] not in {"AMPLITUDE", "ENERGY"}:
            raise ValueError("unknown occurrence norm scale")
        tokens[token_id] = token

    graph = {
        token_id: tuple(token["dependencies"])
        for token_id, token in tokens.items()
    }
    topo_order(graph)

    primitive_universe = {
        token["occurrence_id"]
        for token in primitive
        if not token["dependencies"]
    }
    absorbed = {
        dependency
        for token in joints
        for dependency in token["dependencies"]
    }
    retained = sorted(
        token_id for token_id in tokens if token_id not in absorbed
    )

    covered: set[str] = set()
    cache: dict[str, frozenset[str]] = {}
    for token_id in retained:
        leaves = set(primitive_leaves(token_id, tokens, cache))
        if covered & leaves:
            raise ValueError("overlapping retained joint covers")
        covered |= leaves
    if covered != primitive_universe:
        raise ValueError("retained occurrences do not exactly cover primitives")

    complete = all(tokens[token_id]["exponent"] is not None for token_id in retained)
    return retained, covered, complete


def endpoint_state(
    threshold: Fraction,
    upper: Fraction | None,
    lower: Fraction | None,
    registry_complete: bool,
) -> str:
    if not registry_complete or upper is None:
        return "INCOMPLETE"
    if lower is not None and lower > upper:
        raise ValueError("endpoint lower certificate exceeds upper certificate")
    if upper < threshold:
        return "STRICT_PASS"
    if lower is not None and lower >= threshold:
        if lower == threshold:
            return "EQUALITY_STOP"
        return "STOP_ROUTE"
    return "NO_PASS_CERTIFICATE"


def scopes() -> dict[str, dict[str, Any]]:
    return {
        "scope.physical_cut": {
            "h0": 2,
            "delta": "fixed-rational",
            "weight": "fixed-smooth-W-effective-support-envelope",
            "support_semantics": "COMPLETE_ENVELOPE_NOT_MINIMAL_ACTIVE_SET",
            "X_quantifier": "all-sufficiently-large-X",
            "coefficient_height": "literal-TPC-growing-family",
            "cutoff_modulus": "literal-TPC-schedule",
            "scale_quantifier": "all-X",
            "prefix_quantifier": "all-archived-prefixes",
            "sum_weight": "ordinary-physical",
            "carrier_id": "tpc15-native-cut-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
        "scope.frozen_affine_log": {
            "h0": 2,
            "delta": "not-used",
            "weight": "terminal-reciprocal",
            "support_semantics": "FIXED_AFFINE_FIXED_PERIODIC",
            "X_quantifier": "asymptotic-with-fixed-data",
            "coefficient_height": "fixed",
            "cutoff_modulus": "fixed-before-limit",
            "scale_quantifier": "logarithmic-terminal",
            "prefix_quantifier": "terminal-only",
            "sum_weight": "logarithmic",
            "carrier_id": "fixed-affine-squarefree-periodic-v1",
            "normalization_id": "reciprocal-log-mass",
        },
        "scope.quant_shift1": {
            "h0": 1,
            "delta": "not-used",
            "weight": "reciprocal-or-almost-scale-Cesaro",
            "support_semantics": "SHIFT_ONE",
            "X_quantifier": "quantitative-log-and-almost-scale",
            "coefficient_height": "fixed-shift-one",
            "cutoff_modulus": "none",
            "scale_quantifier": "logarithmic-or-almost-all-scales",
            "prefix_quantifier": "not-actual-all-prefix",
            "sum_weight": "logarithmic-or-Cesaro",
            "carrier_id": "liouville-shift-one-v1",
            "normalization_id": "shift-one-theorem-normalization",
        },
        "scope.small_polylog_affine_almost_scale": {
            "h0": "nonparallel-positive-affine-includes-determinant-two",
            "delta": "not-used",
            "weight": "unweighted-Cesaro",
            "support_semantics": "REDUCED_AFFINE_COMPONENT_ONLY",
            "X_quantifier": "outside-small-log-density-exceptional-set",
            "coefficient_height": "at-most-log-N-to-small-absolute-c",
            "cutoff_modulus": "only-if-encoded-in-small-polylog-height",
            "scale_quantifier": "almost-all-scales-log-density",
            "prefix_quantifier": "not-deterministic-actual-prefixes",
            "sum_weight": "ordinary-Cesaro",
            "carrier_id": "small-polylog-affine-liouville-v1",
            "normalization_id": "cesaro-N",
        },
        "scope.actual_h3": {
            "h0": 2,
            "delta": "fixed-rational",
            "weight": "literal-physical-weight-and-phase",
            "support_semantics": "ACTUAL_ELIGIBLE_TAIL",
            "X_quantifier": "uniform-growing-family",
            "coefficient_height": "growing-with-X",
            "cutoff_modulus": "actual-R-X-and-asR4",
            "scale_quantifier": "all-actual-scales",
            "prefix_quantifier": "all-actual-prefixes",
            "sum_weight": "ordinary-physical",
            "carrier_id": "tpc126-130-eligible-tail-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
    }


def export_record(
    *,
    export_id: str,
    paper: int,
    statement: str,
    status: str,
    level: str,
    direction: str,
    scope_id: str,
    carrier_id: str,
    normalization_id: str,
    coverage: str,
    promotion_eligible: bool,
    bundles: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "export_id": export_id,
        "paper": f"TPC-{paper}",
        "statement": statement,
        "statement_sha256": sha256_bytes(statement.encode("utf-8")),
        "source_bundle_sha256": bundles[f"TPC-{paper}"]["bundle_sha256"],
        "status": status,
        "program_level": level,
        "direction": direction,
        "proof_mode": "THEOREM" if status == "PROVED" else "TARGET_OR_INTERFACE",
        "coverage": coverage,
        "promotion_eligible": promotion_eligible,
        "scope_id": scope_id,
        "carrier_id": carrier_id,
        "normalization_id": normalization_id,
    }


def build_exports(
    bundles: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        export_record(
            export_id="E133.native_entrance",
            paper=133,
            statement=(
                "canonical tuple enumeration equals the opened TPC-15 packet "
                "on the effective support envelope"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="NATIVE_ENTRANCE",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="E134.dyadic_prefix_tail",
            paper=134,
            statement=(
                "boundary-complete dyadic prefix-tail path archive is "
                "coefficientwise conservative"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="DYADIC_PATHS",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="E135.domain_partition",
            paper=135,
            statement=(
                "eligible prefix, eligible tail, and frontier form an exact "
                "native-domain partition"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="CUT_DOMAIN",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="N135.eligible_only_cover",
            paper=135,
            statement=(
                "the eligible-only TPC-17/18 compiler is not a "
                "coefficientwise complete cover"
            ),
            status="PROVED",
            level="L1",
            direction="NEGATIVE",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ELIGIBLE_ONLY_SUBROUTE",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="E136.cut_reconnection",
            paper=136,
            statement=(
                "the three terminal cut classes reconnect exactly to the "
                "opened hard packet"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="CUT_RECONNECTION",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="E136.soft_prefix",
            paper=136,
            statement=(
                "the complete eligible-prefix outer sum is imported as o(X)"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ELIGIBLE_PREFIX_SOFT",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="G136.frontier_totalization",
            paper=136,
            statement=(
                "every frontier leaf has downstream physical maps or one "
                "complete original-scale o(X) theorem"
            ),
            status="NOT_TESTABLE",
            level="L1",
            direction="NEUTRAL",
            scope_id="scope.physical_cut",
            carrier_id="tpc15-native-cut-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="FRONTIER",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="A137.full_mu_fixed_log",
            paper=137,
            statement=(
                "fixed affine full-squarefree fixed-periodic qualitative "
                "logarithmic cancellation"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.frozen_affine_log",
            carrier_id="fixed-affine-squarefree-periodic-v1",
            normalization_id="reciprocal-log-mass",
            coverage="FROZEN_LOG_SHADOW",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="A139.small_polylog_affine_almost_scale",
            paper=139,
            statement=(
                "power-of-log Liouville cancellation for positive "
                "nonparallel affine data of sufficiently small "
                "polylogarithmic height outside a small "
                "logarithmic-density exceptional set"
            ),
            status="PROVED",
            level="L1",
            direction="POSITIVE",
            scope_id="scope.small_polylog_affine_almost_scale",
            carrier_id="small-polylog-affine-liouville-v1",
            normalization_id="cesaro-N",
            coverage="RESTRICTED_ALMOST_SCALE_ARITHMETIC_SHADOW",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="A138.quant_shift1",
            paper=138,
            statement=(
                "quantitative logarithmic and almost-scale estimates in the "
                "stated shift-one scope"
            ),
            status="PROVED",
            level="L0",
            direction="POSITIVE",
            scope_id="scope.quant_shift1",
            carrier_id="liouville-shift-one-v1",
            normalization_id="shift-one-theorem-normalization",
            coverage="SHIFT_ONE_SHADOW",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="N138.shift1_reparam_block",
            paper=138,
            statement=(
                "direct shift-one reparameterization is blocked on the "
                "active odd determinant-two carrier"
            ),
            status="PROVED",
            level="L1",
            direction="NEGATIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="SHIFT_ONE_REPARAM_SUBROUTE",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="G138.quant_affine",
            paper=138,
            statement=(
                "quantitative determinant-two affine estimate in the actual "
                "growing carrier"
            ),
            status="OPEN",
            level="L2_TARGET_POSITIVE",
            direction="POSITIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ACTUAL_H3",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="G139.growing_affine_uniformity",
            paper=139,
            statement=(
                "uniform growing coefficient, cutoff, modulus, phase, "
                "weight, origin, and all-prefix envelope"
            ),
            status="OPEN",
            level="L2_TARGET_POSITIVE",
            direction="POSITIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ACTUAL_H3",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="S140.selector_firewall",
            paper=140,
            statement=(
                "almost-scale control alone does not control a prescribed "
                "sequence of actual prefixes"
            ),
            status="PROVED",
            level="L1",
            direction="NEGATIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="SELECTOR_NONIMPLICATION",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="N140.global_density_window_firewall",
            paper=140,
            statement=(
                "a cumulative logarithmic-density exceptional-set bound "
                "does not automatically give the same normalized bound "
                "on an arbitrary terminal window"
            ),
            status="PROVED",
            level="L1",
            direction="NEGATIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="WINDOW_DENSITY_NONIMPLICATION",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="G140.local_exceptional_window_return",
            paper=140,
            statement=(
                "actual union of pulled-back exceptional sets has a "
                "positive normalized terminal-window logarithmic exponent"
            ),
            status="OPEN",
            level="L2_TARGET_POSITIVE",
            direction="POSITIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ACTUAL_H3",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="G140.pointwise_or_selector",
            paper=140,
            statement=(
                "actual all-prefix pointwise theorem or independent selector "
                "domination"
            ),
            status="OPEN",
            level="L2_TARGET_POSITIVE",
            direction="POSITIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ACTUAL_H3",
            promotion_eligible=False,
            bundles=bundles,
        ),
        export_record(
            export_id="H140.raw_sigma_formula",
            paper=140,
            statement=(
                "conditional raw power ledger after uniformity, truncation, "
                "census, and selector costs"
            ),
            status="CONDITIONAL",
            level="L1_CONDITIONAL",
            direction="POSITIVE",
            scope_id="scope.actual_h3",
            carrier_id="tpc126-130-eligible-tail-v1",
            normalization_id="tpc15-physical-nuX",
            coverage="ACTUAL_H3",
            promotion_eligible=False,
            bundles=bundles,
        ),
    ]


def build_imports() -> list[dict[str, Any]]:
    return [
        {
            "import_id": "I134.native_entrance",
            "consumer": "TPC-134",
            "export_id": "E133.native_entrance",
            "purpose": "PROOF",
            "scope_id": "scope.physical_cut",
            "carrier_id": "tpc15-native-cut-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
        {
            "import_id": "I135.dyadic_paths",
            "consumer": "TPC-135",
            "export_id": "E134.dyadic_prefix_tail",
            "purpose": "PROOF",
            "scope_id": "scope.physical_cut",
            "carrier_id": "tpc15-native-cut-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
        {
            "import_id": "I136.domain_partition",
            "consumer": "TPC-136",
            "export_id": "E135.domain_partition",
            "purpose": "PROOF",
            "scope_id": "scope.physical_cut",
            "carrier_id": "tpc15-native-cut-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
        {
            "import_id": "I139.fixed_log_shadow",
            "consumer": "TPC-139",
            "export_id": "A137.full_mu_fixed_log",
            "purpose": "SHADOW_ONLY",
            "scope_id": "scope.frozen_affine_log",
            "carrier_id": "fixed-affine-squarefree-periodic-v1",
            "normalization_id": "reciprocal-log-mass",
        },
        {
            "import_id": "I139.shift1_shadow",
            "consumer": "TPC-139",
            "export_id": "A138.quant_shift1",
            "purpose": "SHADOW_ONLY",
            "scope_id": "scope.quant_shift1",
            "carrier_id": "liouville-shift-one-v1",
            "normalization_id": "shift-one-theorem-normalization",
        },
        {
            "import_id": "I141.small_polylog_affine_shadow",
            "consumer": "TPC-141",
            "export_id": "A139.small_polylog_affine_almost_scale",
            "purpose": "SHADOW_ONLY",
            "scope_id": "scope.small_polylog_affine_almost_scale",
            "carrier_id": "small-polylog-affine-liouville-v1",
            "normalization_id": "cesaro-N",
        },
        {
            "import_id": "I140.uniformity_target",
            "consumer": "TPC-140",
            "export_id": "G139.growing_affine_uniformity",
            "purpose": "TARGET_DEFINITION",
            "scope_id": "scope.actual_h3",
            "carrier_id": "tpc126-130-eligible-tail-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
        {
            "import_id": "I141.selector_firewall",
            "consumer": "TPC-141",
            "export_id": "S140.selector_firewall",
            "purpose": "PROOF",
            "scope_id": "scope.actual_h3",
            "carrier_id": "tpc126-130-eligible-tail-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
        {
            "import_id": "I141.window_density_firewall",
            "consumer": "TPC-141",
            "export_id": "N140.global_density_window_firewall",
            "purpose": "PROOF",
            "scope_id": "scope.actual_h3",
            "carrier_id": "tpc126-130-eligible-tail-v1",
            "normalization_id": "tpc15-physical-nuX",
        },
    ]


def validate_imports(
    exports: list[dict[str, Any]],
    imports: list[dict[str, Any]],
) -> None:
    by_id = {record["export_id"]: record for record in exports}
    if len(by_id) != len(exports):
        raise ValueError("duplicate export id")
    for record in imports:
        source = by_id.get(record["export_id"])
        if source is None:
            raise ValueError("import references unknown export")
        for field in ("scope_id", "carrier_id", "normalization_id"):
            if record[field] != source[field]:
                raise ValueError(f"source lock mismatch in {field}")
        purpose = record["purpose"]
        if purpose == "PROOF" and source["status"] != "PROVED":
            raise ValueError("proof import does not reference a proved export")
        if purpose == "SHADOW_ONLY":
            if source["promotion_eligible"]:
                raise ValueError("shadow-only source cannot be promotion eligible")
        elif purpose not in {"PROOF", "TARGET_DEFINITION"}:
            raise ValueError("unknown import purpose")


def node(
    node_id: str,
    gate: str,
    status: str,
    level: str,
    direction: str,
    structural: bool,
    required: bool,
    scope_id: str,
    source_export: str | None,
    required_artifact: str,
    parents: tuple[str, ...],
    primitive_inputs: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "gate": gate,
        "status": status,
        "program_level": level,
        "direction": direction,
        "structural": structural,
        "required_for_selected_route": required,
        "scope_id": scope_id,
        "source_export": source_export,
        "required_artifact": required_artifact,
        "parents": list(parents),
        "primitive_inputs": list(primitive_inputs),
        "scope_match": True,
    }


def build_nodes() -> list[dict[str, Any]]:
    return [
        node(
            "S133.native_entrance", "H1.native", "PROVED", "L1",
            "POSITIVE", True, True, "scope.physical_cut",
            "E133.native_entrance", "", (),
            ("native_tuple_dictionary", "fixed_h0", "physical_normalization"),
        ),
        node(
            "S134.dyadic_cut", "H1.cut", "PROVED", "L1",
            "POSITIVE", True, True, "scope.physical_cut",
            "E134.dyadic_prefix_tail", "", ("S133.native_entrance",),
        ),
        node(
            "S135.domain_partition", "H1.cut", "PROVED", "L1",
            "POSITIVE", True, True, "scope.physical_cut",
            "E135.domain_partition", "", ("S134.dyadic_cut",),
        ),
        node(
            "S136.cut_reconnection", "H8.cut", "PROVED", "L1",
            "POSITIVE", True, True, "scope.physical_cut",
            "E136.cut_reconnection", "", ("S135.domain_partition",),
        ),
        node(
            "S136.soft_prefix", "H4.soft", "PROVED", "L1",
            "POSITIVE", False, True, "scope.physical_cut",
            "E136.soft_prefix", "", ("S136.cut_reconnection",),
        ),
        node(
            "H1.frontier_totalization", "H1", "NOT_TESTABLE", "L1",
            "NEUTRAL", True, True, "scope.physical_cut",
            "G136.frontier_totalization",
            (
                "total Q_D, Q_Z, G and fixed-h0 maps for every frontier "
                "leaf, or one complete original-scale o(X) frontier theorem"
            ),
            ("S136.cut_reconnection",),
        ),
        node(
            "H1.actual_carrier", "H1", "NOT_TESTABLE", "L1",
            "NEUTRAL", True, True, "scope.physical_cut", None,
            "complete frontier-augmented actual carrier",
            ("S136.cut_reconnection", "H1.frontier_totalization"),
        ),
        node(
            "A137.fixed_log_shadow", "H3.shadow", "PROVED", "L1",
            "POSITIVE", False, False, "scope.frozen_affine_log",
            "A137.full_mu_fixed_log", "", (),
            ("fixed_affine_forms", "fixed_periodic_masks", "log_weight"),
        ),
        node(
            "A139.polylog_almost_scale_shadow", "H3.shadow",
            "PROVED", "L1", "POSITIVE", False, False,
            "scope.small_polylog_affine_almost_scale",
            "A139.small_polylog_affine_almost_scale", "",
            (),
            (
                "small_polylog_positive_affine_data",
                "nonexceptional_scale",
                "unweighted_Cesaro_normalization",
            ),
        ),
        node(
            "N138.shift1_nontransfer", "H3.shadow", "PROVED", "L1",
            "NEGATIVE", False, False, "scope.actual_h3",
            "N138.shift1_reparam_block", "", (),
            ("odd_determinant_two_support", "shift_one_statement"),
        ),
        node(
            "G138.quant_affine", "H3", "OPEN", "L2_TARGET_POSITIVE",
            "POSITIVE", False, False, "scope.actual_h3",
            "G138.quant_affine",
            "quantitative determinant-two affine theorem", (),
        ),
        node(
            "G139.growing_uniformity", "H3", "OPEN",
            "L2_TARGET_POSITIVE", "POSITIVE", False, True,
            "scope.actual_h3", "G139.growing_affine_uniformity",
            (
                "uniform coefficient-height, cutoff, modulus, masks, "
                "weights, phases, origins and all-prefix theorem"
            ),
            (
                "A137.fixed_log_shadow",
                "A139.polylog_almost_scale_shadow",
                "N138.shift1_nontransfer",
            ),
        ),
        node(
            "N140.window_density_firewall", "H3.shadow", "PROVED",
            "L1", "NEGATIVE", False, False, "scope.actual_h3",
            "N140.global_density_window_firewall", "", (),
            (
                "global_exceptional_density",
                "arbitrary_terminal_window",
            ),
        ),
        node(
            "G140.local_exceptional_window", "H3", "OPEN",
            "L2_TARGET_POSITIVE", "POSITIVE", False, True,
            "scope.actual_h3", "G140.local_exceptional_window_return",
            (
                "positive local logarithmic exponent for the union of "
                "all pulled-back exceptional sets on every actual "
                "terminal window"
            ),
            (
                "A139.polylog_almost_scale_shadow",
                "N140.window_density_firewall",
            ),
        ),
        node(
            "G140.selector", "H3", "OPEN", "L2_TARGET_POSITIVE",
            "POSITIVE", False, True, "scope.actual_h3",
            "G140.pointwise_or_selector",
            "pointwise all-prefix theorem or independent selector domination",
            (
                "G139.growing_uniformity",
                "G140.local_exceptional_window",
            ),
        ),
        node(
            "H140.raw_sigma_formula", "H3", "CONDITIONAL",
            "L1_CONDITIONAL", "POSITIVE", False, True,
            "scope.actual_h3", "H140.raw_sigma_formula",
            "positive actual raw exponent after every declared loss",
            ("G139.growing_uniformity", "G140.selector"),
        ),
        node(
            "H2.signed_resonance", "H2", "OPEN",
            "L2_TARGET_POSITIVE", "POSITIVE", False, True,
            "scope.actual_h3", None,
            "literal signed replacement for the unresolved resonance sector",
            ("H1.actual_carrier",),
        ),
        node(
            "H3.actual_packet_saving", "H3", "OPEN",
            "L2_TARGET_POSITIVE", "POSITIVE", False, True,
            "scope.actual_h3", None,
            "uniform actual-family amplitude saving at least 1/400",
            ("H140.raw_sigma_formula",),
        ),
        node(
            "H4.complete_tail", "H4", "OPEN",
            "L2_TARGET_POSITIVE", "POSITIVE", False, True,
            "scope.physical_cut", None,
            "complete original-scale physical high/ultra/boundary return",
            ("H1.actual_carrier",),
        ),
        node(
            "H5.det_zero", "H5", "NOT_TESTABLE",
            "L2_TARGET_POSITIVE", "POSITIVE", False, True,
            "scope.physical_cut", None,
            "actual compatible determinant and zero-mode exponent pair",
            ("H1.actual_carrier",),
        ),
        node(
            "H6.physical_cover", "H6", "NOT_TESTABLE", "L1",
            "POSITIVE", True, True, "scope.physical_cut", None,
            "complete physical cover including every frontier leaf",
            ("H1.actual_carrier",),
        ),
        node(
            "H7.fixed_h0_totality", "H7", "NOT_TESTABLE", "L1",
            "POSITIVE", True, True, "scope.physical_cut", None,
            "total fixed-h0 map on every terminal leaf",
            ("H1.actual_carrier",),
        ),
        node(
            "H8.final_reconnection", "H8", "NOT_TESTABLE", "L1",
            "POSITIVE", True, True, "scope.physical_cut", None,
            "complete exact hard-packet intertwining after frontier handling",
            (
                "H1.actual_carrier",
                "H6.physical_cover",
                "H7.fixed_h0_totality",
            ),
        ),
        node(
            "H9.physical_registry", "H9", "NOT_TESTABLE", "L1",
            "POSITIVE", True, True, "scope.physical_cut", None,
            (
                "complete theorem-backed physical occurrence registry and "
                "strict 1/400 primal certificate"
            ),
            (
                "H1.actual_carrier",
                "H6.physical_cover",
                "H7.fixed_h0_totality",
                "H8.final_reconnection",
            ),
        ),
        node(
            "ROOT.endpoint_synthesis", "ROOT", "CONDITIONAL",
            "L1_CONDITIONAL", "POSITIVE", False, True,
            "scope.physical_cut", None,
            "proved H1--H9 active-route conjunction with strict slack",
            (
                "H1.actual_carrier",
                "H2.signed_resonance",
                "H3.actual_packet_saving",
                "H4.complete_tail",
                "H5.det_zero",
                "H6.physical_cover",
                "H7.fixed_h0_totality",
                "H8.final_reconnection",
                "H9.physical_registry",
                "S136.soft_prefix",
            ),
        ),
    ]


def validate_nodes(
    nodes: list[dict[str, Any]],
    scope_registry: dict[str, dict[str, Any]],
    exports: list[dict[str, Any]],
) -> tuple[dict[str, tuple[str, ...]], list[str]]:
    by_id = {record["node_id"]: record for record in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("duplicate proof node id")
    export_ids = {record["export_id"] for record in exports}
    for record in nodes:
        if record["status"] not in VALID_STATUSES:
            raise ValueError("unknown node status")
        if record["program_level"] not in VALID_LEVELS:
            raise ValueError("unknown evidence level")
        if record["direction"] not in VALID_DIRECTIONS:
            raise ValueError("unknown evidence direction")
        if record["scope_id"] not in scope_registry:
            raise ValueError("unknown node scope")
        if (
            record["source_export"] is not None
            and record["source_export"] not in export_ids
        ):
            raise ValueError("node references unknown source export")
        if set(record["primitive_inputs"]) & FORBIDDEN_PRIMITIVE_INPUTS:
            raise ValueError("semantic target firewall violation")
        if (
            record["status"] == "PROVED"
            and record["program_level"] == "L2_TARGET_POSITIVE"
        ):
            raise ValueError("target-only label cannot be a proved L2 result")

    graph = {
        node_id: tuple(record["parents"])
        for node_id, record in by_id.items()
    }
    order = topo_order(graph)
    validate_order(graph, order)

    h9_ancestors = ancestor_closure(graph, "H9.physical_registry")
    forbidden_h9_gates = {"H2", "H3", "H4", "H5"}
    if any(
        by_id[ancestor]["gate"].split(".", 1)[0] in forbidden_h9_gates
        for ancestor in h9_ancestors
    ):
        raise ValueError(
            "H9 physical registry has a direct or indirect arithmetic dependency"
        )
    return graph, order


def terminal_coverage() -> list[dict[str, Any]]:
    return [
        {
            "terminal_id": "eligible-prefix-soft",
            "source_node": "S136.soft_prefix",
            "disposition": "SOFT_PROVED",
            "destination": "R_soft",
        },
        {
            "terminal_id": "eligible-tail-open",
            "source_node": "S136.cut_reconnection",
            "disposition": "NONSOFT_MAPPED",
            "destination": "H3.actual_packet_saving",
        },
        {
            "terminal_id": "frontier-unmapped",
            "source_node": "S136.cut_reconnection",
            "disposition": "UNMAPPED",
            "destination": "H1.frontier_totalization",
        },
    ]


def validate_terminal_coverage(
    records: list[dict[str, Any]],
    node_ids: set[str],
) -> None:
    expected = {
        "eligible-prefix-soft",
        "eligible-tail-open",
        "frontier-unmapped",
    }
    ids = [record["terminal_id"] for record in records]
    if set(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError("terminal roles are not an exact cover")
    for record in records:
        if record["source_node"] not in node_ids:
            raise ValueError("terminal source node missing")
        if (
            record["terminal_id"] == "frontier-unmapped"
            and record["disposition"] != "UNMAPPED"
        ):
            raise ValueError("frontier cannot be silently promoted")


def tail_namespaces() -> list[dict[str, str]]:
    return [
        {
            "occurrence_id": "H3.squarefree_tail",
            "namespace": "H3",
            "destination": "H3.actual_packet_saving",
        },
        {
            "occurrence_id": "H5.content_remainder",
            "namespace": "H5",
            "destination": "H5.det_zero",
        },
        {
            "occurrence_id": "Phys.high_ultra_boundary",
            "namespace": "PHYSICAL",
            "destination": "H4.complete_tail",
        },
        {
            "occurrence_id": "Archive.frontier_totalization",
            "namespace": "ARCHIVE",
            "destination": "H1.frontier_totalization",
        },
    ]


def validate_tails(
    records: list[dict[str, str]],
    node_ids: set[str],
) -> None:
    expected = {
        "H3.squarefree_tail",
        "H5.content_remainder",
        "Phys.high_ultra_boundary",
        "Archive.frontier_totalization",
    }
    ids = [record["occurrence_id"] for record in records]
    namespaces = [record["namespace"] for record in records]
    if set(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError("tail occurrences are omitted or duplicated")
    if len(namespaces) != len(set(namespaces)):
        raise ValueError("tail namespaces were merged")
    if any(record["destination"] not in node_ids for record in records):
        raise ValueError("tail destination is not a proof node")


def occurrence_token(
    occurrence_id: str,
    map_name: str,
    scale: str,
    exponent: Fraction | None,
    source: str,
    dependencies: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "occurrence_id": occurrence_id,
        "map_name": map_name,
        "domain": f"domain:{occurrence_id}",
        "codomain": f"codomain:{occurrence_id}",
        "scope_id": "scope.physical_cut",
        "scale": scale,
        "exponent": None if exponent is None else fraction_record(exponent),
        "source": source,
        "dependencies": list(dependencies),
        "ledger_namespace": "PHYSICAL_SYNTHESIS",
    }


def build_occurrence_registry() -> dict[str, Any]:
    primitive = [
        occurrence_token(
            "native-entrance@133", "native entrance", "AMPLITUDE",
            Fraction(0), "TPC-133 exact theorem"
        ),
        occurrence_token(
            "dyadic-split@134", "dyadic split", "AMPLITUDE",
            Fraction(0), "TPC-134 exact theorem"
        ),
        occurrence_token(
            "domain-partition@135", "domain partition", "AMPLITUDE",
            Fraction(0), "TPC-135 exact theorem"
        ),
        occurrence_token(
            "cut-reconnection@136", "cut reconnection", "AMPLITUDE",
            Fraction(0), "TPC-136 exact theorem"
        ),
        occurrence_token(
            "frontier-totalization@after136", "frontier totalization",
            "AMPLITUDE", None, "missing frontier theorem"
        ),
        occurrence_token(
            "physical-cover@H6", "physical cover", "AMPLITUDE",
            None, "missing H6 theorem"
        ),
        occurrence_token(
            "fixed-h0-totality@H7", "fixed-h0 totality", "AMPLITUDE",
            None, "missing H7 theorem"
        ),
        occurrence_token(
            "final-reconnection@H8", "final reconnection", "AMPLITUDE",
            None, "missing H8 theorem"
        ),
        occurrence_token(
            "packet-census@outer", "weighted packet census", "AMPLITUDE",
            None, "missing complete synthesis theorem"
        ),
    ]
    joints = [
        occurrence_token(
            "joint-cut@133-136",
            "cut archive composite",
            "AMPLITUDE",
            Fraction(0),
            "TPC-133--136 joint exact composition",
            (
                "native-entrance@133",
                "dyadic-split@134",
                "domain-partition@135",
                "cut-reconnection@136",
            ),
        )
    ]
    retained, covered, complete = canonical_occurrence_registry(
        primitive, joints
    )
    unknown = sorted(
        token["occurrence_id"]
        for token in primitive + joints
        if token["occurrence_id"] in retained and token["exponent"] is None
    )
    return {
        "primitive_occurrences": primitive,
        "joint_tokens": joints,
        "retained_occurrences": retained,
        "covered_primitive_occurrences": sorted(covered),
        "unknown_retained_occurrences": unknown,
        "complete": complete,
        "determinant_reserve_is_physical_token": False,
    }


def gate_projection() -> dict[str, dict[str, Any]]:
    return {
        "H1": {
            "status": "NOT_TESTABLE",
            "evidence": "L1_TARGET",
            "structural": True,
            "source_node": "H1.actual_carrier",
        },
        "H2": {
            "status": "OPEN",
            "evidence": "L2_TARGET_POSITIVE",
            "structural": False,
            "source_node": "H2.signed_resonance",
        },
        "H3": {
            "status": "OPEN",
            "evidence": "L2_TARGET_POSITIVE",
            "structural": False,
            "source_node": "H3.actual_packet_saving",
        },
        "H4": {
            "status": "OPEN",
            "evidence": "L2_TARGET_POSITIVE",
            "structural": False,
            "source_node": "H4.complete_tail",
        },
        "H5": {
            "status": "NOT_TESTABLE",
            "evidence": "L2_TARGET_POSITIVE",
            "structural": False,
            "source_node": "H5.det_zero",
        },
        "H6": {
            "status": "NOT_TESTABLE",
            "evidence": "L1_TARGET",
            "structural": True,
            "source_node": "H6.physical_cover",
        },
        "H7": {
            "status": "NOT_TESTABLE",
            "evidence": "L1_TARGET",
            "structural": True,
            "source_node": "H7.fixed_h0_totality",
        },
        "H8": {
            "status": "NOT_TESTABLE",
            "evidence": "L1_TARGET",
            "structural": True,
            "source_node": "H8.final_reconnection",
        },
        "H9": {
            "status": "NOT_TESTABLE",
            "evidence": "L1_TARGET",
            "structural": True,
            "source_node": "H9.physical_registry",
        },
    }


def route_universe() -> dict[str, Any]:
    return {
        "routes": [
            "eligible_only_tpc17_18_compiler",
            "quantitative_shift1_reparameterization",
            "signed_native_frontier_augmented",
        ],
        "selected_route": "signed_native_frontier_augmented",
        "typed_alternative": None,
        "stops": {
            "eligible_only_tpc17_18_compiler": {
                "stopped": True,
                "source_export": "N135.eligible_only_cover",
                "scope_id": "scope.physical_cut",
                "carrier_id": "tpc15-native-cut-v1",
            },
            "quantitative_shift1_reparameterization": {
                "stopped": True,
                "source_export": "N138.shift1_reparam_block",
                "scope_id": "scope.actual_h3",
                "carrier_id": "tpc126-130-eligible-tail-v1",
            },
            "signed_native_frontier_augmented": {
                "stopped": False,
                "source_export": None,
                "scope_id": "scope.physical_cut",
                "carrier_id": "tpc15-native-cut-v1",
            },
        },
    }


def validate_routes(
    routes: dict[str, Any],
    export_ids: set[str],
) -> None:
    universe = set(routes["routes"])
    if not universe or routes["selected_route"] not in universe:
        raise ValueError("selected route is outside route universe")
    if set(routes["stops"]) != universe:
        raise ValueError("route stop map is not an exact universe cover")
    for route, record in routes["stops"].items():
        if record["stopped"]:
            if (
                record["source_export"] not in export_ids
                or not record["scope_id"]
                or not record["carrier_id"]
            ):
                raise ValueError(f"stop record for {route} lacks metadata")
    alternative = routes["typed_alternative"]
    if alternative is not None:
        if alternative not in universe or alternative == routes["selected_route"]:
            raise ValueError("invalid typed alternative")
        if not routes["stops"][routes["selected_route"]]["stopped"]:
            raise ValueError("reroute lacks selected-route stop")
        if routes["stops"][alternative]["stopped"]:
            raise ValueError("typed alternative is already stopped")


def first_missing(
    nodes: list[dict[str, Any]],
    order: list[str],
) -> dict[str, Any] | None:
    by_id = {record["node_id"]: record for record in nodes}
    for node_id in order:
        record = by_id[node_id]
        if record["required_for_selected_route"] and (
            record["status"] == "NOT_TESTABLE"
            or not record["scope_match"]
        ):
            return {
                "node_id": node_id,
                "gate": record["gate"],
                "status": record["status"],
                "program_level": record["program_level"],
                "required_artifact": record["required_artifact"],
            }
    return None


def build_manifest() -> dict[str, Any]:
    bundles = {
        f"TPC-{number}": source_bundle(number)
        for number in range(133, 141)
    }
    scope_registry = scopes()
    exports = build_exports(bundles)
    imports = build_imports()
    validate_imports(exports, imports)
    nodes = build_nodes()
    graph, order = validate_nodes(nodes, scope_registry, exports)
    terminals = terminal_coverage()
    validate_terminal_coverage(terminals, set(graph))
    tails = tail_namespaces()
    validate_tails(tails, set(graph))
    registry = build_occurrence_registry()

    threshold = Fraction(1, 400)
    state = endpoint_state(
        threshold,
        upper=None,
        lower=None,
        registry_complete=registry["complete"],
    )
    endpoint = {
        "contract": "MVP1-physical-amplitude-v1",
        "scale": "AMPLITUDE",
        "comparison": "STRICT_LT",
        "sigma_target": fraction_record(threshold),
        "sigma_shadow_power": fraction_record(Fraction(0)),
        "sigma_actual_certified": None,
        "lambda_phys_upper": None,
        "lambda_phys_lower": None,
        "strict_slack": None,
        "state": state,
        "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
        "upper_at_or_above_is_stop_without_lower": False,
        "determinant_reserve_reusable": False,
    }

    routes = route_universe()
    validate_routes(routes, {record["export_id"] for record in exports})
    missing = first_missing(nodes, order)
    if missing is None or missing["node_id"] != "H1.frontier_totalization":
        raise ValueError("unexpected first missing record")

    return {
        "schema": SCHEMA_NAME,
        "snapshot": {
            "date": "2026-07-27",
            "source_range": "TPC-133--140",
            "selected_route": routes["selected_route"],
            "schema_sha256": sha256_file(SCHEMA_PATH),
            "identity_rule": "canonical-content-no-self-hash",
            "source_hash_semantics": "INTEGRITY_ONLY",
            "restricted_positive_arithmetic_shadow": (
                "SMALL_POLYLOG_AFFINE_ALMOST_SCALE"
            ),
            "exceptional_window_state": (
                "GLOBAL_DENSITY_PROVED_LOCAL_ACTUAL_WINDOW_OPEN"
            ),
        },
        "source_bundles": bundles,
        "scope_registry": scope_registry,
        "exports": exports,
        "imports": imports,
        "nodes": nodes,
        "proof_dag": {
            "parents": {
                node_id: list(parents)
                for node_id, parents in graph.items()
            },
            "topological_order": order,
            "root": "ROOT.endpoint_synthesis",
            "H9_arithmetic_independent": True,
        },
        "terminal_leaf_coverage": terminals,
        "tail_namespaces": tails,
        "occurrence_registry": registry,
        "endpoint_ledger": endpoint,
        "route_universe": routes,
        "gate_projection": gate_projection(),
        "first_missing": missing,
        "cut_aware_bound": {
            "identity": "B=S_soft+S_eligible+S_frontier",
            "soft": "o(X)",
            "bound": (
                "|B| <= o(X)+|S_frontier|"
                "+X^(1-sigma_eligible+Lambda_eligible+o(1))"
            ),
            "frontier_explicit": True,
            "coverage": "DECLARED_THREE_WAY_CUT_ONLY",
            "full_carrier_totalized": False,
        },
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "cut_complete_is_full_carrier": False,
            "arithmetic_frontier": False,
            "positive_L2": False,
            "strict_endpoint": False,
            "endpoint_pass": False,
            "hard_packet_oX": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
            "certificate_PASS_is_route_GO": False,
        },
    }


def validate_manifest(manifest: dict[str, Any]) -> dict[str, bool]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    required = set(schema["required"])
    if set(manifest) != required:
        raise ValueError("manifest top-level fields differ from schema contract")
    if manifest["schema"] != SCHEMA_NAME:
        raise ValueError("manifest schema name mismatch")
    if schema["properties"]["schema"]["const"] != SCHEMA_NAME:
        raise ValueError("JSON schema and generator schema differ")
    if len(manifest["source_bundles"]) != 8:
        raise ValueError("source bundle count is not eight")
    for number in range(133, 141):
        bundle = manifest["source_bundles"].get(f"TPC-{number}")
        if bundle is None or len(bundle["bundle_sha256"]) != 64:
            raise ValueError("source bundle is absent or unhashed")
    if manifest["snapshot"].get("source_hash_semantics") != "INTEGRITY_ONLY":
        raise ValueError("source hashes were assigned proof semantics")
    if manifest["snapshot"].get(
        "restricted_positive_arithmetic_shadow"
    ) != "SMALL_POLYLOG_AFFINE_ALMOST_SCALE":
        raise ValueError("restricted positive arithmetic shadow is absent")
    if manifest["snapshot"].get("exceptional_window_state") != (
        "GLOBAL_DENSITY_PROVED_LOCAL_ACTUAL_WINDOW_OPEN"
    ):
        raise ValueError("exceptional-window firewall is absent")
    validate_imports(manifest["exports"], manifest["imports"])
    graph, order = validate_nodes(
        manifest["nodes"],
        manifest["scope_registry"],
        manifest["exports"],
    )
    if manifest["proof_dag"]["parents"] != {
        node_id: list(parents) for node_id, parents in graph.items()
    }:
        raise ValueError("manifest DAG differs from node parents")
    validate_order(graph, manifest["proof_dag"]["topological_order"])
    if order != manifest["proof_dag"]["topological_order"]:
        raise ValueError("manifest topological order is not canonical")
    validate_terminal_coverage(
        manifest["terminal_leaf_coverage"],
        set(graph),
    )
    validate_tails(manifest["tail_namespaces"], set(graph))
    registry = manifest["occurrence_registry"]
    retained, covered, complete = canonical_occurrence_registry(
        registry["primitive_occurrences"],
        registry["joint_tokens"],
    )
    if retained != registry["retained_occurrences"]:
        raise ValueError("retained occurrence list is stale")
    if covered != set(registry["covered_primitive_occurrences"]):
        raise ValueError("primitive occurrence cover is stale")
    if complete != registry["complete"]:
        raise ValueError("registry completeness flag is stale")
    validate_routes(
        manifest["route_universe"],
        {record["export_id"] for record in manifest["exports"]},
    )
    threshold = parse_fraction(manifest["endpoint_ledger"]["sigma_target"])
    if threshold != Fraction(1, 400):
        raise ValueError("endpoint threshold changed")
    current_endpoint = endpoint_state(
        threshold, None, None, registry_complete=complete
    )
    if current_endpoint != manifest["endpoint_ledger"]["state"]:
        raise ValueError("endpoint state is stale")
    missing = first_missing(
        manifest["nodes"],
        manifest["proof_dag"]["topological_order"],
    )
    if missing != manifest["first_missing"]:
        raise ValueError("first-missing record is stale")
    if missing is None or missing["node_id"] != "H1.frontier_totalization":
        raise ValueError("frontier is not the first missing record")
    cut = manifest["cut_aware_bound"]
    expected_bound = (
        "|B| <= o(X)+|S_frontier|"
        "+X^(1-sigma_eligible+Lambda_eligible+o(1))"
    )
    if (
        cut["identity"] != "B=S_soft+S_eligible+S_frontier"
        or cut["soft"] != "o(X)"
        or cut["bound"] != expected_bound
        or not cut["frontier_explicit"]
        or cut.get("coverage") != "DECLARED_THREE_WAY_CUT_ONLY"
        or cut.get("full_carrier_totalized") is not False
    ):
        raise ValueError("cut scope, identity, or explicit frontier drifted")
    terminal_by_id = {
        record["terminal_id"]: record
        for record in manifest["terminal_leaf_coverage"]
    }
    if terminal_by_id["frontier-unmapped"] != {
        "terminal_id": "frontier-unmapped",
        "source_node": "S136.cut_reconnection",
        "disposition": "UNMAPPED",
        "destination": "H1.frontier_totalization",
    }:
        raise ValueError("frontier terminal was softened or redirected")
    if manifest["gate_projection"]["H1"]["status"] != "NOT_TESTABLE":
        raise ValueError("cut completeness was promoted to full-carrier H1")
    exports_by_id = {
        record["export_id"]: record for record in manifest["exports"]
    }
    restricted = exports_by_id.get(
        "A139.small_polylog_affine_almost_scale"
    )
    if (
        restricted is None
        or restricted["status"] != "PROVED"
        or restricted["program_level"] != "L1"
        or restricted["scope_id"]
        != "scope.small_polylog_affine_almost_scale"
        or restricted["coverage"]
        != "RESTRICTED_ALMOST_SCALE_ARITHMETIC_SHADOW"
        or restricted["promotion_eligible"]
    ):
        raise ValueError("restricted affine shadow was promoted or mistyped")
    window_firewall = exports_by_id.get(
        "N140.global_density_window_firewall"
    )
    window_target = exports_by_id.get(
        "G140.local_exceptional_window_return"
    )
    if (
        window_firewall is None
        or window_firewall["status"] != "PROVED"
        or window_firewall["direction"] != "NEGATIVE"
        or window_target is None
        or window_target["status"] != "OPEN"
        or window_target["program_level"] != "L2_TARGET_POSITIVE"
    ):
        raise ValueError("global-to-window firewall or local target drifted")
    if manifest["claim_boundary"]["positive_L2"]:
        raise ValueError("snapshot falsely claims positive L2")
    if any(
        manifest["claim_boundary"][field]
        for field in (
            "source_hashes_prove_theorems",
            "cut_complete_is_full_carrier",
            "arithmetic_frontier",
            "strict_endpoint",
            "endpoint_pass",
        )
    ):
        raise ValueError("claim boundary contains an unsupported promotion")
    return {
        "schema_fields": True,
        "eight_source_bundles_hashed": True,
        "source_hashes_integrity_only": True,
        "restricted_small_polylog_affine_shadow_scoped": True,
        "global_density_not_promoted_to_terminal_window": True,
        "source_scope_carrier_normalization_locks": True,
        "acyclic_exact_node_DAG": True,
        "H9_transitively_independent_of_arithmetic": True,
        "terminal_roles_exactly_covered": True,
        "tail_namespaces_exactly_covered": True,
        "occurrence_registry_nonduplicated": True,
        "unknown_costs_not_zero": True,
        "strict_one_over_400_contract": True,
        "cut_complete_not_full_carrier": True,
        "frontier_remains_explicit": True,
        "no_positive_L2": True,
        "first_missing_frontier_totalization": True,
    }


def mutation_regressions(manifest: dict[str, Any]) -> dict[str, bool]:
    results: dict[str, bool] = {}

    bad_imports = copy.deepcopy(manifest["imports"])
    bad_imports[0]["normalization_id"] = "wrong-normalization"
    try:
        validate_imports(manifest["exports"], bad_imports)
    except ValueError:
        results["normalization_mismatch_rejected"] = True
    else:
        results["normalization_mismatch_rejected"] = False

    duplicate_terminal = copy.deepcopy(manifest["terminal_leaf_coverage"])
    duplicate_terminal[-1]["terminal_id"] = "eligible-tail-open"
    try:
        validate_terminal_coverage(
            duplicate_terminal,
            {record["node_id"] for record in manifest["nodes"]},
        )
    except ValueError:
        results["duplicate_terminal_rejected"] = True
    else:
        results["duplicate_terminal_rejected"] = False

    soft_frontier = copy.deepcopy(manifest["terminal_leaf_coverage"])
    for record in soft_frontier:
        if record["terminal_id"] == "frontier-unmapped":
            record["disposition"] = "SOFT_PROVED"
    try:
        validate_terminal_coverage(
            soft_frontier,
            {record["node_id"] for record in manifest["nodes"]},
        )
    except ValueError:
        results["frontier_soft_promotion_rejected"] = True
    else:
        results["frontier_soft_promotion_rejected"] = False

    merged_tails = copy.deepcopy(manifest["tail_namespaces"])
    merged_tails[-1]["namespace"] = merged_tails[-2]["namespace"]
    try:
        validate_tails(
            merged_tails,
            {record["node_id"] for record in manifest["nodes"]},
        )
    except ValueError:
        results["tail_namespace_merge_rejected"] = True
    else:
        results["tail_namespace_merge_rejected"] = False

    primitive = copy.deepcopy(
        manifest["occurrence_registry"]["primitive_occurrences"]
    )
    duplicate_occurrence = primitive + [copy.deepcopy(primitive[0])]
    try:
        canonical_occurrence_registry(
            duplicate_occurrence,
            manifest["occurrence_registry"]["joint_tokens"],
        )
    except ValueError:
        results["duplicate_occurrence_rejected"] = True
    else:
        results["duplicate_occurrence_rejected"] = False

    self_joint = [
        occurrence_token(
            "self", "self", "AMPLITUDE", Fraction(0), "bad", ("self",)
        )
    ]
    try:
        canonical_occurrence_registry([], self_joint)
    except ValueError:
        results["self_joint_rejected"] = True
    else:
        results["self_joint_rejected"] = False

    overlap_primitive = [
        occurrence_token("a", "a", "AMPLITUDE", Fraction(0), "a"),
        occurrence_token("b", "b", "AMPLITUDE", Fraction(0), "b"),
        occurrence_token("c", "c", "AMPLITUDE", Fraction(0), "c"),
    ]
    overlap_joints = [
        occurrence_token(
            "j1", "j1", "AMPLITUDE", Fraction(0), "j1", ("a", "b")
        ),
        occurrence_token(
            "j2", "j2", "AMPLITUDE", Fraction(0), "j2", ("b", "c")
        ),
    ]
    try:
        canonical_occurrence_registry(overlap_primitive, overlap_joints)
    except ValueError:
        results["overlapping_joints_rejected"] = True
    else:
        results["overlapping_joints_rejected"] = False

    threshold = Fraction(1, 400)
    results["endpoint_strict_case"] = (
        endpoint_state(
            threshold, Fraction(1, 500), None, True
        ) == "STRICT_PASS"
    )
    results["endpoint_upper_failure_not_stop"] = (
        endpoint_state(
            threshold, Fraction(1, 300), None, True
        ) == "NO_PASS_CERTIFICATE"
    )
    results["endpoint_equality_lower_stop"] = (
        endpoint_state(
            threshold, Fraction(1, 400), Fraction(1, 400), True
        ) == "EQUALITY_STOP"
    )
    results["endpoint_unknown_not_zero"] = (
        endpoint_state(threshold, None, None, False) == "INCOMPLETE"
    )

    bad_nodes = copy.deepcopy(manifest["nodes"])
    for record in bad_nodes:
        if record["node_id"] == "A137.fixed_log_shadow":
            record["status"] = "PROVED"
            record["program_level"] = "L2_TARGET_POSITIVE"
    try:
        validate_nodes(
            bad_nodes,
            manifest["scope_registry"],
            manifest["exports"],
        )
    except ValueError:
        results["fixed_log_pseudo_L2_rejected"] = True
    else:
        results["fixed_log_pseudo_L2_rejected"] = False

    bad_h9 = copy.deepcopy(manifest["nodes"])
    for record in bad_h9:
        if record["node_id"] == "H8.final_reconnection":
            record["parents"].append("H3.actual_packet_saving")
    try:
        validate_nodes(
            bad_h9,
            manifest["scope_registry"],
            manifest["exports"],
        )
    except ValueError:
        results["H9_indirect_arithmetic_dependency_rejected"] = True
    else:
        results["H9_indirect_arithmetic_dependency_rejected"] = False

    results["determinant_reserve_not_physical"] = not manifest[
        "occurrence_registry"
    ]["determinant_reserve_is_physical_token"]
    return results


def build_audit(
    manifest: dict[str, Any],
    manifest_rendered: str,
) -> dict[str, Any]:
    checks = validate_manifest(manifest)
    mutations = mutation_regressions(manifest)
    status = all(checks.values()) and all(mutations.values())
    return {
        "schema": "tpc-141-batch-integration-audit-v1",
        "status": "PASS" if status else "FAIL",
        "manifest_sha256": sha256_bytes(manifest_rendered.encode("utf-8")),
        "checks": checks,
        "mutation_regressions": mutations,
        "integration_state": "ASSEMBLED_WITH_GAPS",
        "first_missing": manifest["first_missing"],
        "endpoint_state": manifest["endpoint_ledger"]["state"],
        "route_status": {
            "selected_route": manifest["route_universe"]["selected_route"],
            "eligible_only_compiler": "STOPPED_SCOPED",
            "shift1_reparameterization": "STOPPED_SCOPED",
            "frontier_augmented_signed_route": "NOT_TESTABLE",
        },
        "claim_boundary": manifest["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare both committed JSON artifacts without writing",
    )
    args = parser.parse_args()

    manifest = build_manifest()
    manifest_rendered = canonical_json(manifest)
    audit = build_audit(manifest, manifest_rendered)
    audit_rendered = canonical_json(audit)

    if args.check:
        expected = {
            MANIFEST_PATH: manifest_rendered,
            AUDIT_PATH: audit_rendered,
        }
        for path, rendered in expected.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
                raise SystemExit(f"certificate mismatch: {path.name}")
    else:
        MANIFEST_PATH.write_text(manifest_rendered, encoding="utf-8")
        AUDIT_PATH.write_text(audit_rendered, encoding="utf-8")

    print(audit_rendered, end="")
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
