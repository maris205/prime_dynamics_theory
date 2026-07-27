#!/usr/bin/env python3
"""Deterministic certificate-format audit for TPC-131."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


FORBIDDEN_PRIMITIVE_INPUTS = {
    "B_is_oX",
    "target_H3_packet_saving",
    "target_D_lower_bound",
    "target_Z_upper_bound",
}


def topo_order(graph: dict[str, tuple[str, ...]]) -> list[str]:
    indegree = {node: 0 for node in graph}
    children = {node: [] for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            if dep not in graph:
                raise ValueError(f"unknown dependency {dep}")
            indegree[node] += 1
            children[dep].append(node)
    queue = sorted(node for node, degree in indegree.items() if degree == 0)
    out: list[str] = []
    while queue:
        node = queue.pop(0)
        out.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(out) != len(graph):
        raise ValueError("cyclic proof graph")
    return out


def primitive_firewall(
    primitive_inputs: dict[str, tuple[str, ...]],
) -> bool:
    return all(
        not (set(inputs) & FORBIDDEN_PRIMITIVE_INPUTS)
        for inputs in primitive_inputs.values()
    )


@dataclass(frozen=True)
class Token:
    occurrence: str
    map_name: str
    scope: str
    scale: str
    exponent: Fraction
    source: str
    dependencies: tuple[str, ...] = ()

def canonical_registry(tokens: list[Token]) -> list[Token]:
    """Return maximal exact-cover tokens in a selected theorem registry.

    Occurrence identifiers are globally unique, independently of norm
    scale.  A joint token replaces the primitive leaves below its
    dependencies.  The maximal retained tokens must form a disjoint
    exact cover of all primitive occurrences.
    """

    selected: dict[str, Token] = {}
    for token in tokens:
        if token.occurrence in selected:
            raise ValueError("two sources selected for one occurrence")
        if token.scale not in {"amplitude", "energy"}:
            raise ValueError("unknown norm scale")
        if token.occurrence in token.dependencies:
            raise ValueError("self-dependent joint token")
        selected[token.occurrence] = token

    dependency_graph = {
        occurrence: token.dependencies
        for occurrence, token in selected.items()
    }
    topo_order(dependency_graph)

    leaves_cache: dict[str, frozenset[str]] = {}

    def primitive_leaves(occurrence: str) -> frozenset[str]:
        if occurrence in leaves_cache:
            return leaves_cache[occurrence]
        token = selected[occurrence]
        if not token.dependencies:
            leaves = frozenset({occurrence})
        else:
            leaves = frozenset().union(
                *(primitive_leaves(dep) for dep in token.dependencies)
            )
            if not leaves:
                raise ValueError("joint token has no primitive leaves")
        leaves_cache[occurrence] = leaves
        return leaves

    primitive_universe = {
        occurrence
        for occurrence, token in selected.items()
        if not token.dependencies
    }
    absorbed = {
        dependency
        for token in selected.values()
        for dependency in token.dependencies
    }
    retained = [
        token
        for occurrence, token in selected.items()
        if occurrence not in absorbed
    ]

    covered: set[str] = set()
    for token in retained:
        leaves = set(primitive_leaves(token.occurrence))
        if covered & leaves:
            raise ValueError("overlapping retained joint dependencies")
        covered |= leaves
    if covered != primitive_universe:
        raise ValueError("retained registry is not an exact primitive cover")
    return sorted(retained, key=lambda token: token.occurrence)


def amplitude_loss(token: Token) -> Fraction:
    if token.scale == "amplitude":
        return token.exponent
    if token.scale == "energy":
        return token.exponent / 2
    raise ValueError("unknown norm scale")


def phase_certificate(
    lambda_e: Fraction,
    lambda_phi: Fraction,
    gamma_r: Fraction,
) -> Fraction:
    return max(Fraction(0), lambda_e + 2 * lambda_phi - gamma_r)


def zero_certificate(
    delta_prefix: Fraction,
    ell_z: Fraction,
    eta_cont: Fraction,
) -> Fraction | None:
    if delta_prefix < ell_z:
        return None
    return min(delta_prefix - ell_z, eta_cont)


def endpoint_state(
    sigma_raw: Fraction,
    lambda_phys: Fraction | None,
) -> str:
    if lambda_phys is None:
        return "INCOMPLETE"
    if lambda_phys < sigma_raw:
        return "STRICT_PASS"
    if lambda_phys == sigma_raw:
        return "EQUALITY_STOP"
    return "STOP_ROUTE"


def audit() -> dict:
    graph = {
        "archive": (),
        "reassembly": ("archive",),
        "fixed_h0": ("reassembly",),
        "literal_block": ("fixed_h0",),
        "liouville_pullback": ("literal_block",),
        "squarefree_expansion": ("liouville_pullback",),
        "quantifier_firewall": ("squarefree_expansion",),
        "fejer_four_sign_reduction": ("quantifier_firewall",),
        "actual_H3_four_sign_bound": ("fejer_four_sign_reduction",),
        "squarefree_truncation_tail": ("squarefree_expansion",),
        "packet_census": ("archive", "reassembly"),
        "raw_packet_bound": (
            "actual_H3_four_sign_bound",
            "squarefree_truncation_tail",
            "packet_census",
        ),
        "h5_certificate": ("archive",),
        "complete_soft_remainder": ("archive",),
        "physical_H4_tail": ("archive",),
        "H6_cover": ("reassembly",),
        "H7_localization": ("fixed_h0",),
        "H8_reconnection": ("archive", "reassembly"),
        "occurrence_registry": ("reassembly",),
        "strict_endpoint_certificate": ("occurrence_registry",),
        "endpoint_synthesis": (
            "raw_packet_bound",
            "h5_certificate",
            "complete_soft_remainder",
            "physical_H4_tail",
            "H6_cover",
            "H7_localization",
            "H8_reconnection",
            "strict_endpoint_certificate",
        ),
    }
    order = topo_order(graph)
    acyclic_ok = order.index("archive") < order.index("endpoint_synthesis")
    deliberate_cycle_rejected = False
    try:
        topo_order({"a": ("b",), "b": ("a",)})
    except ValueError:
        deliberate_cycle_rejected = True

    primitive_inputs = {
        "archive": ("source_dictionary", "fixed_h0", "normalization"),
        "arithmetic": ("literal_coefficients", "uniform_quantifiers"),
    }
    firewall_ok = primitive_firewall(primitive_inputs)
    bad_firewall_rejected = not primitive_firewall(
        {"bad": ("literal_coefficients", "B_is_oX")}
    )

    tokens = [
        Token(
            "frame@stage1",
            "S",
            "fixed-h0",
            "amplitude",
            Fraction(1, 2000),
            "frame theorem",
        ),
        Token(
            "frame@stage2",
            "S",
            "fixed-h0",
            "energy",
            Fraction(1, 1000),
            "second occurrence energy theorem",
        ),
        Token(
            "group@stage3",
            "G",
            "fixed-h0",
            "amplitude",
            Fraction(1, 4000),
            "group theorem",
        ),
        Token(
            "joint@stage1-3",
            "G o S",
            "fixed-h0",
            "amplitude",
            Fraction(1, 3000),
            "joint theorem",
            ("frame@stage1", "group@stage3"),
        ),
        Token(
            "packet-census@outer",
            "ell-infinity packet synthesis",
            "fixed-h0",
            "amplitude",
            Fraction(1, 5000),
            "weighted packet census theorem",
        ),
    ]
    registry = canonical_registry(tokens)
    registry_ids = [token.occurrence for token in registry]
    occurrence_level_ok = (
        "frame@stage2" in registry_ids
        and "frame@stage1" not in registry_ids
        and "group@stage3" not in registry_ids
        and "joint@stage1-3" in registry_ids
        and "packet-census@outer" in registry_ids
    )
    lambda_phys = sum(
        (amplitude_loss(token) for token in registry),
        start=Fraction(0),
    )

    energy_exponent = Fraction(3, 100)
    amplitude_exponent = energy_exponent / 2
    norm_conversion_ok = amplitude_exponent == Fraction(3, 200)

    tail_coverage = [
        ("h3.squarefree_truncation_tail", "raw_packet_bound"),
        ("h5.zero_mode_content_remainder", "h5_certificate"),
        ("physical.high_ultra_boundary_tail", "physical_H4_tail"),
    ]
    expected_tails = {
        "h3.squarefree_truncation_tail",
        "h5.zero_mode_content_remainder",
        "physical.high_ultra_boundary_tail",
    }
    tail_ids = [tail for tail, _ in tail_coverage]
    tail_namespace_ok = (
        set(tail_ids) == expected_tails
        and len(tail_ids) == len(set(tail_ids))
        and all(destination in graph for _, destination in tail_coverage)
    )

    duplicate_occurrence_rejected = False
    try:
        canonical_registry(
            [
                Token(
                    "same@event", "S", "fixed-h0", "amplitude",
                    Fraction(1, 100), "source A"
                ),
                Token(
                    "same@event", "S", "fixed-h0", "energy",
                    Fraction(1, 100), "source E"
                ),
            ]
        )
    except ValueError:
        duplicate_occurrence_rejected = True

    overlapping_joints_rejected = False
    try:
        canonical_registry(
            [
                Token("a", "A", "s", "amplitude", Fraction(0), "a"),
                Token("b", "B", "s", "amplitude", Fraction(0), "b"),
                Token("c", "C", "s", "amplitude", Fraction(0), "c"),
                Token(
                    "j1", "AB", "s", "amplitude", Fraction(0), "j1",
                    ("a", "b")
                ),
                Token(
                    "j2", "BC", "s", "amplitude", Fraction(0), "j2",
                    ("b", "c")
                ),
            ]
        )
    except ValueError:
        overlapping_joints_rejected = True

    self_dependency_rejected = False
    try:
        canonical_registry(
            [
                Token(
                    "self", "S", "s", "amplitude", Fraction(0),
                    "self", ("self",)
                )
            ]
        )
    except ValueError:
        self_dependency_rejected = True

    lam_d = phase_certificate(
        Fraction(1), Fraction(1, 20), Fraction(3, 10)
    )
    eta_z = zero_certificate(
        Fraction(9, 20), Fraction(1, 20), Fraction(2, 5)
    )
    h5_compatible = eta_z is not None and lam_d <= 2 * eta_z
    determinant_reserve = (
        None if eta_z is None else 2 * eta_z - lam_d
    )

    endpoint_cases = {
        "strict": endpoint_state(Fraction(1, 400), Fraction(1, 500)),
        "equality": endpoint_state(Fraction(1, 400), Fraction(1, 400)),
        "above": endpoint_state(Fraction(1, 400), Fraction(3, 1000)),
        "unknown": endpoint_state(Fraction(1, 400), None),
    }
    endpoint_ok = endpoint_cases == {
        "strict": "STRICT_PASS",
        "equality": "EQUALITY_STOP",
        "above": "STOP_ROUTE",
        "unknown": "INCOMPLETE",
    }

    general_slack = Fraction(1, 80) - Fraction(1, 100)
    general_synthesis_ok = general_slack == Fraction(1, 400)

    evidence_labels = {
        "finite_dag_regression": "L0",
        "literal_archive_crosswalk": "L1",
        "conditional_synthesis": "L1_CONDITIONAL",
        "four_sign_reduction_without_estimate": "L1",
    }
    pseudo_l2_rejected = "L2" not in evidence_labels.values()

    status = all(
        [
            acyclic_ok,
            deliberate_cycle_rejected,
            firewall_ok,
            bad_firewall_rejected,
            occurrence_level_ok,
            norm_conversion_ok,
            tail_namespace_ok,
            duplicate_occurrence_rejected,
            overlapping_joints_rejected,
            self_dependency_rejected,
            h5_compatible,
            determinant_reserve is not None
            and determinant_reserve >= 0,
            endpoint_ok,
            general_synthesis_ok,
            pseudo_l2_rejected,
        ]
    )

    return {
        "schema": "tpc-131-end-to-end-typed-synthesis-v1",
        "status": "PASS" if status else "FAIL",
        "checks": {
            "acyclic_proof_dag": acyclic_ok,
            "deliberate_cycle_rejected": deliberate_cycle_rejected,
            "semantic_firewall": firewall_ok,
            "target_as_primitive_rejected": bad_firewall_rejected,
            "occurrence_level_registry": occurrence_level_ok,
            "energy_to_amplitude_conversion": norm_conversion_ok,
            "tail_occurrences_exactly_covered": tail_namespace_ok,
            "duplicate_occurrence_rejected": duplicate_occurrence_rejected,
            "overlapping_joints_rejected": overlapping_joints_rejected,
            "self_dependency_rejected": self_dependency_rejected,
            "h5_certificate_compatible": h5_compatible,
            "determinant_reserve_nonnegative": (
                determinant_reserve is not None
                and determinant_reserve >= 0
            ),
            "strict_endpoint_states": endpoint_ok,
            "general_sigma_minus_lambda_slack": general_synthesis_ok,
            "pseudo_L2_rejected": pseudo_l2_rejected,
        },
        "sample": {
            "topological_order": order,
            "retained_occurrences": registry_ids,
            "lambda_phys": str(lambda_phys),
            "lambda_phys_scale": "amplitude",
            "tail_coverage": [
                {"occurrence": tail, "destination": destination}
                for tail, destination in tail_coverage
            ],
            "lambda_D_cert": str(lam_d),
            "eta_Z_cert": str(eta_z),
            "rho_det": str(determinant_reserve),
            "general_final_slack": str(general_slack),
            "endpoint_cases": endpoint_cases,
        },
        "claim_boundary": {
            "actual_complete_archive": False,
            "actual_growing_H3_four_sign_saving": False,
            "actual_growing_H5_inputs": False,
            "actual_complete_physical_registry": False,
            "fixed_h0_L2_saving": False,
            "endpoint_GO": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed JSON instead of rewriting it",
    )
    args = parser.parse_args()
    payload = audit()
    out = Path(__file__).with_suffix(".json")
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != rendered:
            raise SystemExit("certificate mismatch")
    else:
        out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
