from __future__ import annotations

import json
from math import pi
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from typed_assembly import (  # noqa: E402
    assembly_frontier,
    det2_error_bound,
    determinant_error_bound,
    marked_trace_error_bound,
    neumann_packet_riesz_bound,
)


def main() -> None:
    current_statuses = {
        "S_native": "conditional",
        "S_lagged": "conditional",
        "R": "open",
        "Q": "open",
        "U": "open",
        "Z": "open",
        "T": "open",
    }
    interface_names = {
        "S_native": "eventual native O/E/S reset seed",
        "S_lagged": "eventual native plus bounded-lag directional seed",
        "R": "packet-to-Riesz spectral isolation",
        "Q": "cloud coefficient and deterministic pole ledger",
        "U": "common-space complementary Schatten-norm limit for p=1 or p=2",
        "Z": "target-independent normalization and schedule independence",
        "T": "directed marked-trace convergence",
    }
    frontier = assembly_frontier(current_statuses)

    couplings = (0.02, 0.05, 0.10, 0.20, 0.25, 0.30)
    packet_examples = []
    for coupling in couplings:
        row = neumann_packet_riesz_bound(2.0 * pi, 2.0, coupling)
        packet_examples.append({"coupling_upper": coupling, **row})

    determinant_examples = []
    for error in (0.1, 0.05, 0.02, 0.01, 0.005):
        determinant_examples.append({
            "trace_norm_error_upper": error,
            "determinant_error_upper": determinant_error_bound(0.5, 1.0, 1.2, error),
            "hilbert_schmidt_error_upper": error,
            "regularized_determinant_error_upper": det2_error_bound(0.5, 1.0, 1.2, error),
        })

    marked_examples = []
    for length in (2, 3, 6):
        marked_examples.append({
            "word_length": length,
            "marked_trace_error_upper": marked_trace_error_bound(length, 1.1, 0.01, 1.0),
        })

    omission_witnesses = [
        {
            "missing": "S",
            "witness": "take a fixed isolated operator but let the reset packet become orthogonal to its Riesz subspace",
            "surviving_failure": "no packet-selected cloud",
        },
        {
            "missing": "R",
            "witness": "A=diag(-1,2) and the packet projection onto (1,1), whose native compression is positive but is not invariant",
            "surviving_failure": "native support does not imply a reducing Riesz cloud",
        },
        {
            "missing": "Q",
            "witness": "attach either 1-z/a or 1-z/b as the deterministic pole ledger to the same finite relative determinants",
            "surviving_failure": "the finite cloud quotient alone does not identify the deterministic pole divisor",
        },
        {
            "missing": "U",
            "witness": "append rank-one complement blocks whose eigenvalues tend to infinity",
            "surviving_failure": "Schatten norms diverge and residual det_p families need not be locally bounded",
        },
        {
            "missing": "Z",
            "witness": "multiply every residual determinant by exp(c_n z) with schedule-dependent c_n",
            "surviving_failure": "zero divisors agree but no canonical determinant exists",
        },
        {
            "missing": "T",
            "witness": "for A=[[0,1],[0,0]], B=[[0,0],[1,0]], and J=diag(1,0), AB and BA have the same determinant while Tr(JAB)=1 and Tr(JBA)=0",
            "surviving_failure": "ordinary determinant data erase temporal orientation",
        },
    ]

    boundary = {
        "abstract_typed_assembly_theorem": True,
        "trace_class_fredholm_branch": True,
        "hilbert_schmidt_regularized_branch": True,
        "one_step_two_step_limits_identified": False,
        "packet_riesz_bound": True,
        "interface_omission_witnesses": True,
        "eventual_reset_interfaces_proved": False,
        "physical_packet_to_riesz_bridge_proved": False,
        "cloud_coefficient_bridge_proved": False,
        "uniform_complement_limit_proved": False,
        "canonical_intrinsic_determinant_constructed": False,
        "gate_A_closed": False,
        "hilbert_polya_operator": False,
        "riemann_hypothesis": False,
    }
    payload = {
        "status": "rh161_packet_riesz_relative_determinant_assembly",
        "current_statuses": current_statuses,
        "interface_names": interface_names,
        "minimal_completion_bundles": [sorted(bundle) for bundle in frontier],
        "packet_riesz_examples": packet_examples,
        "determinant_examples": determinant_examples,
        "marked_trace_examples": marked_examples,
        "omission_witnesses": omission_witnesses,
        "audit_summary": {
            "typed_interface_count": len(current_statuses),
            "minimal_completion_bundle_count": len(frontier),
            "open_interface_count": sum(status == "open" for status in current_statuses.values()),
            "conditional_seed_count": sum(status == "conditional" for status in current_statuses.values()),
            "packet_riesz_example_count": len(packet_examples),
            "spectral_rank_certified_example_count": sum(row["spectral_rank_certified"] for row in packet_examples),
            "packet_bridge_certified_example_count": sum(row["packet_bridge_certified"] for row in packet_examples),
            "packet_bridge_uncertified_example_count": sum(not row["packet_bridge_certified"] for row in packet_examples),
            "omission_witness_count": len(omission_witnesses),
            "current_first_missing_interface": "S_native",
        },
        "theorem_boundary": boundary,
        "route_consequence": (
            "RH-161 turns Gate A's typed assembly from a phrase into six explicit obligations after one of two conditional reset seeds. "
            "A quantitative packet-to-Riesz theorem supplies equal cloud rank under a contour-resolvent/coupling threshold; exact moving-cloud factorization, complementary Schatten-norm convergence for p=1 or p=2, normalization canonicity, and directed marked traces then yield a canonical relative determinant of the selected type. "
            "None of those physical all-level interfaces is proved for prime dynamics, so Gate A remains open with a sharper completion frontier."
        ),
    }
    output = ROOT / "results/typed_assembly_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
