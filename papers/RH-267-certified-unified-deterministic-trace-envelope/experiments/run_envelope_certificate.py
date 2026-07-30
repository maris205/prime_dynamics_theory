"""Certify the clean all-order deterministic trace envelope."""

from __future__ import annotations
import json
from pathlib import Path
import sys
from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH13 = PAPERS / "RH-13-validated-reduced-sector-spectral-gap"
RH253 = PAPERS / "RH-253-extended-deterministic-anchor-atlas"
RH262 = PAPERS / "RH-262-certified-deterministic-numerator-boundary-budget"
sys.path[:0] = [str(ROOT / "src"), str(RH262 / "src"), str(RH13 / "src")]

from coefficient_envelope import certify_envelope  # noqa: E402
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


def record(value: arb) -> dict[str, object]:
    return {"interval": str(value), "float_midpoint": float(value)}


def replay(precision: int) -> dict[str, object]:
    ctx.dps = precision
    reduced = certify_reduced_gap(decimal_precision=precision, dimension=50, tail_degree=100)
    cert = certify_envelope(reduced)
    comparisons = {
        "q_star_lt_0_700876": cert.q_star < arb("0.700876"),
        "nu1_lt_4_623248864": cert.nu1 < arb("4.623248864"),
        "nu2_lt_2_930978": cert.nu2 < arb("2.930978"),
        "nu3_lt_0_806064": cert.nu3 < arb("0.806064"),
        "scaled_cube_lt_0_801254": cert.scaled_cube < arb("0.801254"),
        "residue_1_lt_27_054": cert.residue_constants[0] < arb("27.054"),
        "residue_2_lt_47_538": cert.residue_constants[1] < arb("47.538"),
        "residue_3_lt_37_062": cert.residue_constants[2] < arb("37.062"),
        "clean_constant_lt_48": cert.envelope_constant < arb(48),
    }
    if not all(comparisons.values()):
        raise RuntimeError(f"envelope comparison failed at {precision} dps")
    return {
        "decimal_precision": precision,
        "q_star": record(cert.q_star),
        "nu": [record(cert.nu1), record(cert.nu2), record(cert.nu3)],
        "scaled_cube": record(cert.scaled_cube),
        "residue_constants": [record(value) for value in cert.residue_constants],
        "comparisons": comparisons,
    }


def run() -> dict[str, object]:
    atlas = json.loads((RH253 / "results/extended_anchor_atlas.json").read_text())
    replays = [replay(precision) for precision in (100, 150, 200)]
    q_star = replays[-1]["q_star"]["float_midpoint"]
    finite_ratios = [
        abs(row["hardy_scaled_anchor"]) / q_star ** row["order"]
        for row in atlas["coefficient_rows"]
    ]
    return {
        "status": "rh267_certified_unified_deterministic_trace_envelope",
        "theorem": "For every n>=2, |a_n| < 48 q_star^n.",
        "q_star_definition": "1/(r_H*lambda)",
        "clean_envelope_constant": 48,
        "replays": replays,
        "finite_order_2_to_28_ratio_diagnostic": {
            "row_count": len(finite_ratios),
            "minimum": min(finite_ratios),
            "maximum": max(finite_ratios),
        },
        "obligation_vector": {
            "legal_anchored_head": False,
            "coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "analytic_target_tail": True,
            "certified_target_boundary_constant": True,
            "satisfied_count": 2,
            "complete": False,
        },
        "theorem_boundary": {
            "deterministic_target_all_order_envelope": True,
            "moving_cloud_uniform_trace_envelope": False,
            "cloud_coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "finite_fit_used_as_proof": False,
            "gate_A": False, "gate_B": False, "gate_C": False,
            "gate_D": False, "gate_E": False,
            "hilbert_polya_operator": False,
            "riemann_zero_identification": False,
            "zeta_divisor_equality": False,
            "riemann_hypothesis_implication": False,
        },
        "route_coordinate": "deterministic_all_order_envelope_certified_cloud_uniformity_open",
    }


def main() -> None:
    payload = run(); output = ROOT / "results/coefficient_envelope.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "constant": 48, "replays": 3}, sort_keys=True))
if __name__ == "__main__": main()
