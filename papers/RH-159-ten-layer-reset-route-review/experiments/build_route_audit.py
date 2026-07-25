from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from reset_route_review import classify_route, directional_to_native_lower, first_unresolved_gate  # noqa: E402


PAPER_NUMBERS = tuple(range(151, 159))
ROUTE_NAMES = ("recursive", "native", "contemporaneous", "lagged")


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def paper_directory(number: int) -> Path:
    matches = sorted(PAPERS.glob(f"RH-{number}-*"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one RH-{number} directory, found {len(matches)}")
    return matches[0]


def verify_paper(number: int) -> tuple[dict[str, object], list[tuple[int, int]]]:
    directory = paper_directory(number)
    summary = json.loads((directory / "results/summary.json").read_text())
    dependency = json.loads((directory / "results/dependency_manifest.json").read_text())
    verification = json.loads((directory / "results/archive_verification.json").read_text())
    checks = []

    def check(path: Path, expected: str, category: str) -> None:
        actual = sha(path)
        checks.append({
            "category": category,
            "path": str(path.relative_to(REPO)),
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
        })

    for path, expected in verification["files"].items():
        check(directory / path, expected, "archive_publication")
    for path, expected in summary["result_hashes"].items():
        check(directory / path, expected, "result")
    for path, expected in dependency["local_sources"].items():
        check(directory / path, expected, "local_source")
    for path, expected in dependency["publication_artifacts"].items():
        check(directory / path, expected, "manifest_publication")
    edges = []
    for record in dependency["external_inputs"].values():
        path = REPO / record["path"]
        check(path, record["sha256"], "external_input")
        match = re.search(r"papers/RH-(\d+)-", record["path"])
        if match and int(match.group(1)) in PAPER_NUMBERS:
            edges.append((int(match.group(1)), number))

    return ({
        "paper": number,
        "directory": directory.name,
        "summary_status": summary["status"],
        "archive_status": verification["status"],
        "check_count": len(checks),
        "match_count": sum(item["match"] for item in checks),
        "failure_count": sum(not item["match"] for item in checks),
        "publication_file_count": len(verification["files"]),
        "external_input_count": len(dependency["external_inputs"]),
        "local_source_count": len(dependency["local_sources"]),
        "checks": checks,
    }, edges)


def acyclic(nodes: set[int], edges: set[tuple[int, int]]) -> bool:
    incoming = {node: 0 for node in nodes}
    outgoing = {node: [] for node in nodes}
    for left, right in edges:
        if left in nodes and right in nodes:
            incoming[right] += 1
            outgoing[left].append(right)
    queue = [node for node, degree in incoming.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for right in outgoing[node]:
            incoming[right] -= 1
            if incoming[right] == 0:
                queue.append(right)
    return visited == len(nodes)


def main() -> None:
    paper_records = []
    dependency_edges: set[tuple[int, int]] = set()
    summaries = {}
    for number in PAPER_NUMBERS:
        record, edges = verify_paper(number)
        paper_records.append(record)
        dependency_edges.update(edges)
        summaries[number] = json.loads((paper_directory(number) / "results/summary.json").read_text())
        print(json.dumps({key: record[key] for key in (
            "paper", "check_count", "match_count", "failure_count", "publication_file_count"
        )}, sort_keys=True), flush=True)

    metrics = {
        "reset_snapshots_certified": summaries[151]["audit"]["direct_reset_certificate_count"],
        "reset_snapshot_count": summaries[151]["audit"]["snapshot_count"],
        "universal_recursive_informative_count": summaries[151]["audit"]["universal_branch_free_informative_count"],
        "transition_overlap_certified": summaries[152]["audit"]["invertible_transition_count"],
        "transition_count": summaries[152]["audit"]["transition_count"],
        "correlated_congruence_positive": summaries[153]["audit"]["correlated_positive_base_count"],
        "independent_congruence_positive": summaries[153]["audit"]["independent_positive_definite_count"],
        "independent_congruence_failures": summaries[153]["audit"]["independent_positive_definite_failure_count"],
        "delayed_half_count": summaries[154]["audit"]["half_suffix_transition_count"],
        "delayed_half_overlap_floor": summaries[154]["audit"]["half_suffix_common_overlap_floor"],
        "native_subunit_count": summaries[155]["audit"]["subunit_recent_tail_count"],
        "native_snapshot_count": summaries[155]["audit"]["snapshot_count"],
        "native_support_positive_count": summaries[156]["audit"]["positive_support_count"],
        "native_support_transition_count": summaries[156]["audit"]["transition_count"],
        "native_support_floor": summaries[156]["audit"]["minimum_support_lower"],
        "contemporaneous_exact_zero_count": summaries[157]["audit"]["tail_inactive_exact_zero_count"],
        "contemporaneous_active_four_mode_count": summaries[157]["audit"]["active_four_mode_coupling_certificate_count"],
        "contemporaneous_active_count": summaries[157]["audit"]["tail_active_snapshot_count"],
        "lagged_four_mode_count": summaries[158]["audit"]["adaptive_four_mode_certificate_count"],
        "lagged_target_count": summaries[158]["audit"]["target_count"],
        "lagged_cross_base_floor": summaries[158]["audit"]["minimum_selected_normalized_base_lower"],
        "lagged_fourth_cross_floor": summaries[158]["audit"]["minimum_selected_fourth_cross_lower"],
        "lagged_path_overlap_floor": summaries[158]["audit"]["minimum_selected_path_overlap_lower"],
    }
    lag_audit = json.loads((paper_directory(158) / "results/lag_audit.json").read_text())
    eta = float(lag_audit["eta"])
    depth = int(lag_audit["depth"])
    recent_norm_upper = (1.0 - eta**depth) / (1.0 - eta)
    metrics["universal_recent_norm_upper"] = recent_norm_upper
    metrics["lagged_cross_implied_native_fourth_floor"] = directional_to_native_lower(
        metrics["lagged_fourth_cross_floor"], recent_norm_upper
    )

    gates = [
        {"index": 1, "key": "packet_localization", "name": "packet localization / direct reset", "evidence": "RH-151", "global_status": "finite_certified"},
        {"index": 2, "key": "transition_coherence", "name": "reset transition coherence", "evidence": "RH-152", "global_status": "finite_certified"},
        {"index": 3, "key": "correlated_congruence", "name": "correlated congruence transport", "evidence": "RH-153", "global_status": "finite_certified"},
        {"index": 4, "key": "delayed_suffix", "name": "delayed terminal-half conditioning", "evidence": "RH-154", "global_status": "finite_certified"},
        {"index": 5, "key": "native_tail_gate", "name": "native recent/tail subunit gate", "evidence": "RH-155", "global_status": "finite_certified"},
        {"index": 6, "key": "native_support", "name": "native support floor", "evidence": "RH-156", "global_status": "finite_certified"},
        {"index": 7, "key": "contemporaneous_cross", "name": "contemporaneous directional cross", "evidence": "RH-157", "global_status": "exact_obstruction"},
        {"index": 8, "key": "lagged_cross", "name": "bounded-lag directional cross", "evidence": "RH-158", "global_status": "finite_certified"},
        {"index": 9, "key": "all_level_laws", "name": "uniform all-level endpoint laws", "evidence": "not proved", "global_status": "open"},
        {"index": 10, "key": "downstream_assembly", "name": "typed downstream outward assembly", "evidence": "not recomposed", "global_status": "open"},
    ]

    matrix = {
        "recursive": ["obstruction", "not_required", "not_required", "not_required", "not_required", "not_required", "not_required", "not_required", "open", "open"],
        "native": ["certified", "certified", "certified", "optional", "certified", "certified", "not_required", "not_required", "open", "open"],
        "contemporaneous": ["certified", "certified", "optional", "optional", "optional", "optional", "obstruction", "not_required", "open", "open"],
        "lagged": ["certified", "certified", "optional", "optional", "optional", "optional", "not_required", "certified", "open", "open"],
    }
    seed_requirements = {
        "recursive": [("recursive packet transport", "obstruction")],
        "native": [("packet localization", "certified"), ("transition coherence", "certified"), ("correlated congruence", "certified"), ("native tail gate", "certified"), ("native support", "certified")],
        "contemporaneous": [("packet localization", "certified"), ("transition coherence", "certified"), ("contemporaneous cross", "obstruction")],
        "lagged": [("packet localization", "certified"), ("transition coherence", "certified"), ("lagged cross", "certified")],
    }
    routes = []
    for name in ROUTE_NAMES:
        seed = seed_requirements[name]
        seed_state = classify_route(state for _, state in seed)
        program = [*seed, ("uniform all-level laws", "open"), ("downstream assembly", "open")]
        routes.append({
            "name": name,
            "finite_seed_state": seed_state,
            "program_state": classify_route(state for _, state in program),
            "first_seed_failure": first_unresolved_gate(seed),
            "first_program_unresolved": first_unresolved_gate(program),
            "seed_requirements": [{"gate": gate, "state": state} for gate, state in seed],
        })

    total_checks = sum(record["check_count"] for record in paper_records)
    failures = sum(record["failure_count"] for record in paper_records)
    summary = {
        "paper_count": len(paper_records),
        "archive_verified_paper_count": sum(record["failure_count"] == 0 for record in paper_records),
        "publication_file_count": sum(record["publication_file_count"] for record in paper_records),
        "hash_check_count": total_checks,
        "hash_failure_count": failures,
        "internal_dependency_edge_count": len(dependency_edges),
        "internal_dependency_graph_acyclic": acyclic(set(PAPER_NUMBERS), dependency_edges),
        "gate_count": len(gates),
        "finite_certified_gate_count": sum(gate["global_status"] == "finite_certified" for gate in gates),
        "exact_obstruction_gate_count": sum(gate["global_status"] == "exact_obstruction" for gate in gates),
        "open_gate_count": sum(gate["global_status"] == "open" for gate in gates),
        "finite_closed_route_count": sum(route["finite_seed_state"] == "finite_closed" for route in routes),
        "program_closed_route_count": sum(route["program_state"] == "finite_closed" for route in routes),
    }
    payload = {
        "status": "rh159_ten_layer_reset_route_review",
        "papers": paper_records,
        "dependency_edges": [{"from": left, "to": right} for left, right in sorted(dependency_edges)],
        "gates": gates,
        "route_matrix": matrix,
        "routes": routes,
        "metrics": metrics,
        "audit_summary": summary,
        "typed_route_conclusion": {
            "native_to_directional_implication": False,
            "directional_to_native_with_complement_upper": True,
            "native_finite_seed_closed": True,
            "lagged_directional_finite_seed_closed": True,
            "contemporaneous_directional_route_rejected": True,
            "recursive_branch_free_route_rejected_at_current_bounds": True,
            "any_program_route_closed": False,
            "minimal_open_frontier": ["uniform all-level endpoint laws", "typed downstream outward assembly"],
        },
        "theorem_boundary": {
            "positive_block_directional_to_native_theorem": True,
            "strict_nonimplication_native_to_directional": True,
            "eight_paper_archive_reverified": failures == 0,
            "finite_route_lattice_classified": True,
            "uniform_all_level_reset_theorem": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The route lattice has two finite survivors with different output types: a native compression-support seed and an adaptive-lag directional-cross seed. "
            "The contemporaneous directional route is exactly obstructed and the current branch-free recursive route is finitely noninformative. "
            "A directional cross lower implies a same-packet native eigenvalue lower when complement energy is bounded, whereas native positivity alone cannot recover cross rank. "
            "No route is program-complete because uniform all-level laws and typed downstream assembly remain open."
        ),
    }
    output = ROOT / "results/route_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary, **metrics}, sort_keys=True))


if __name__ == "__main__":
    main()
