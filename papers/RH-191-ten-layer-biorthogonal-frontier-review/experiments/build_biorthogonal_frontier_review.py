"""Assemble the RH-182--190 results into the next typed frontier."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from biorthogonal_frontier import current_frontier, macro_boundary, route_status  # noqa: E402


def directory(number: int) -> Path:
    matches = tuple(PAPERS.glob(f"RH-{number}-*"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one RH-{number} directory, found {len(matches)}")
    return matches[0]


def read(number: int, name: str) -> dict[str, object]:
    return json.loads((directory(number) / "results" / name).read_text(encoding="utf-8"))


def main() -> None:
    results = {
        182: read(182, "temporal_clock_audit.json"),
        183: read(183, "wrap_obstruction_audit.json"),
        184: read(184, "biorthogonal_identity_audit.json"),
        185: read(185, "bi_krylov_audit.json"),
        186: read(186, "oblique_conditioning_audit.json"),
        187: read(187, "regularization_audit.json"),
        188: read(188, "directional_balance_audit.json"),
        189: read(189, "feshbach_identity_audit.json"),
        190: read(190, "complement_budget_audit.json"),
    }
    statuses = {
        "orthogonal_finite_clock": "rejected_by_finite_two_sided_audit",
        "projective_wrap_obstruction": "proved_finite_lower_bound",
        "biorthogonal_temporal_algebra": "proved",
        "biorthogonal_local_candidate": (
            "local_floating_candidate"
            if results[185]["local_sigma_0_01_length_4_two_sided_gate_count"] > 0
            else "not_found"
        ),
        "cross_angle_uniformity": "open",
        "validated_physical_D": "open",
        "uniform_K_margin": "open",
        "shell_transport_H": "open",
        "cloud_ledger_Q": "open",
    }
    finite_case_count = sum([
        int(results[182]["window_count"]),
        int(results[183]["formula_case_count"]) + int(results[183]["physical_window_count"]),
        int(results[184]["case_count"]),
        int(results[185]["window_count"]),
        int(results[186]["window_count"]),
        int(results[187]["sweep_case_count"]) + int(results[187]["window_count"]),
        int(results[188]["window_count"]),
        int(results[189]["case_count"]),
        int(results[190]["window_count"]),
    ])
    output_payload = {
        "status": "rh191_ten_layer_biorthogonal_frontier_review",
        "paper_numbers": list(range(182, 191)),
        "aggregate_finite_case_count": finite_case_count,
        "formula_or_identity_failure_count": (
            int(results[182]["formula_failure_count"])
            + int(results[183]["formula_failure_count"])
            + int(results[184]["failure_count"])
            + int(results[189]["failure_count"])
        ),
        "orthogonal_clock_window_count": results[182]["window_count"],
        "orthogonal_clock_three_gate_success_count": results[182]["three_gate_success_count"],
        "projective_formula_case_count": results[183]["formula_case_count"],
        "biorthogonal_identity_case_count": results[184]["case_count"],
        "local_biorthogonal_gate_count": results[185]["local_sigma_0_01_length_4_two_sided_gate_count"],
        "conditioned_gate_count": results[186]["conditioned_contraction_success_count"],
        "regularized_strict_gate_count": results[187]["strict_regularized_contraction_count"],
        "directional_absolute_product_below_one_count": results[188]["absolute_coupling_product_below_1_count"],
        "feshbach_identity_case_count": results[189]["case_count"],
        "norm_only_resolvent_success_count": results[190]["norm_only_resolvent_success_count"],
        "statuses": statuses,
        "route_status": route_status(statuses),
        "current_frontier": current_frontier(statuses),
        "route_consequence": (
            "The orthogonal temporal clock is rejected by a finite two-sided audit. "
            "A balanced source/observation bi-Krylov clock has a local sigma=0.01, L=4 floating candidate, "
            "but its cross-angle conditioning is severe. Exact Feshbach factorization and scalar directional "
            "coupling balance are now available. The sharp elementary orthonormal-coordinate, one-factor "
            "norm-only complement resolvent bound fails "
            "on every audited window, so validated contour inverses are the next physical D wall."
        ),
        "macro_boundary": macro_boundary(),
        "component_results": results,
    }
    output = ROOT / "results/biorthogonal_frontier_review.json"
    output.write_text(json.dumps(output_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "aggregate_cases": finite_case_count,
        "route_status": output_payload["route_status"],
        "frontier": output_payload["current_frontier"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
