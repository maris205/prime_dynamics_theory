"""Compose the RH-53 theorem, validation, and numerical evidence ledger."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH51 = PAPERS / "RH-51-cyclic-rank-growing-horizon-stein"
RH52 = PAPERS / "RH-52-intrinsic-peripheral-residue-transfer"
ROADMAP = PAPERS / "RH-ROADMAP-after-RH50.md"
PILOT = ROOT / "results" / "deterministic_tail_pilot.json"
ARB_AUDIT = ROOT / "results" / "arb_tail_audit.json"
ARB_CUTOFF = ROOT / "results" / "arb_production_cutoff_ledger.json"
OUTPUT = ROOT / "results" / "hardy_tail_cutoff_certificate.json"
sys.path.insert(0, str(ROOT / "src"))

from hardy_tail import adaptive_cutoff_multiple, cutoff_bound  # noqa: E402


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def main() -> None:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    arb_audit = json.loads(ARB_AUDIT.read_text(encoding="utf-8"))
    arb_cutoff = json.loads(ARB_CUTOFF.read_text(encoding="utf-8"))
    rows = pilot["rows"]
    production_scales = []
    rh50 = json.loads(
        (RH50 / "results" / "two_pole_hardy_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    for row in rh50["rows"]:
        sigma = float(row["sigma"])
        dimension = int(row["fine_dimension"])
        fixed = cutoff_bound(dimension, sigma, 8.0)
        adaptive_multiple = adaptive_cutoff_multiple(1.0 / dimension)
        adaptive = cutoff_bound(dimension, sigma, adaptive_multiple)
        production_scales.append(
            {
                "sigma": sigma,
                "fine_dimension": dimension,
                "maximum_power_in_RH50": int(row["maximum_power"]),
                "fixed_eight_effective_multiple": fixed.effective_multiple,
                "fixed_eight_analytic_two_norm_upper": fixed.two_norm_upper,
                "adaptive_multiple": adaptive_multiple,
                "adaptive_analytic_two_norm_upper": adaptive.two_norm_upper,
            }
        )

    maximum_excess = max(
        row[side]["relative_energy_excess"]
        for row in rows
        for side in ("left", "right")
    )
    maximum_tail = max(
        row[side]["selected_infinite_tail_upper"]
        for row in rows
        for side in ("left", "right")
    )
    payload = {
        "status": (
            "rigorous_deterministic_block_tail_and_adaptive_exact_real_cutoff_route_"
            "with_production_interval_gap"
        ),
        "scope": (
            "finite-dimensional two-pole directional Hardy energies and transfer "
            "between exact-real sparse and canonical full folded-Gaussian matrices"
        ),
        "evidence_level": {
            "analytic": (
                "exact deterministic finite-horizon trace identity, block-contraction "
                "infinite-tail theorem, finite-horizon perturbation theorem, fixed-window "
                "no-go, and adaptive cutoff route"
            ),
            "validated": (
                "256-bit Arb outward-rounded execution on a small abstract matrix and "
                "the inherited RH-39 closed cutoff bounds"
            ),
            "numerical": (
                "binary64 five-scale dense all-column audit through dimension 512 and "
                "analytic cutoff ledgers on the RH-50 production dimensions through 40960"
            ),
        },
        "deterministic_main_sum": {
            "identity": "sum_(m=0)^(M-1) ||Y A^m X||_S2^2=tr(Y S_M Y^*)",
            "algorithm": (
                "propagate every source column and accumulate Frobenius squares; no "
                "Hutchinson probes and no full Gramian storage are required"
            ),
            "rounding_boundary": (
                "the identity is exact algebraically; a validated numerical upper requires "
                "outward-rounded matrix actions or certified local error budgets"
            ),
        },
        "infinite_tail_theorem": {
            "finite_gramian": "S_M=sum_(j=0)^(M-1) A^j X X^* (A^*)^j",
            "condition": "q_M=||A^M||_2<1",
            "stein_tail": (
                "tail<=||A^M S_M (A^*)^M||_2 ||Y||_S2^2/(1-q_M^2)"
            ),
            "simple_tail": (
                "tail<=||Y||_2^2 q_M^2 tr(S_M)/(1-q_M^2)"
            ),
            "consequence": (
                "the fitted time-64 decay base in RH-50 is unnecessary once one "
                "contracting block power is certified"
            ),
        },
        "perturbation_transfer": {
            "power_identity": (
                "A^m-B^m=sum_(j=0)^(m-1) A^(m-1-j)(A-B)B^j"
            ),
            "finite_horizon": (
                "operator, source, and observation defects give an explicit l2-in-time "
                "difference upper for the first M directional outputs"
            ),
            "block_contraction": (
                "finite-time semigroup norm ledgers transfer q_M<1 whenever the "
                "telescoping defect leaves positive margin"
            ),
            "infinite_energy": (
                "add the two available certified tails to the finite-horizon comparison"
            ),
        },
        "cutoff_result": {
            "fixed_window_no_go": (
                "for fixed L and sigma, rows approaching a zero of the map retain a "
                "strictly positive continuum omitted mass; fixed L does not define the "
                "canonical full-Gaussian all-grid limit"
            ),
            "stored_eight_sigma": (
                "L=8 is smaller than binary64 relevance on the stored scales but this "
                "finite-scale fact is not an asymptotic theorem"
            ),
            "adaptive_schedule": "L(h)=max(5,2 sqrt(log(1/h)))",
            "adaptive_two_norm_rate": "O(h^2/(log(1/h))^(1/4))",
            "hardy_transfer_condition": (
                "combine the adaptive matrix defect with finite-time semigroup ledgers, "
                "factor perturbation bounds, and a transferred block contraction"
            ),
            "fixed_eight_crossover_dimension": math.exp(16.0),
        },
        "arb_audit": arb_audit,
        "arb_production_cutoff_ledger": arb_cutoff,
        "floating_five_scale_audit": {
            "rows": rows,
            "noise_levels": len(rows),
            "largest_dimension": max(row["fine_dimension"] for row in rows),
            "maximum_relative_energy_excess": maximum_excess,
            "maximum_selected_tail_energy_squared_upper": maximum_tail,
            "all_column_deterministic": True,
            "hutchinson_probes_used": False,
            "interval_validated": False,
        },
        "rh50_production_cutoff_ledger": {
            "rows": production_scales,
            "largest_dimension": max(
                row["fine_dimension"] for row in production_scales
            ),
            "maximum_fixed_eight_two_norm_upper": max(
                row["fixed_eight_analytic_two_norm_upper"]
                for row in production_scales
            ),
            "all_stored_multiples_above_adaptive_requirement": all(
                row["adaptive_multiple"] <= 8.0 for row in production_scales
            ),
        },
        "program_conclusion": {
            "deterministic_finite_matrix_tail_mechanism_closed": True,
            "adaptive_exact_real_cutoff_route_closed": True,
            "fixed_eight_is_canonical_joint_limit": False,
            "small_arb_algorithm_executed": True,
            "production_scale_interval_trace_executed": False,
            "intrinsic_factor_cutoff_transfer_executed": False,
            "stage_A3_fully_closed": False,
            "stage_A1_uniform_trace_budget_closed": False,
            "stage_A4_intrinsic_identification_closed": False,
        },
        "dependencies": {
            "rh39_cutoff_manuscript": entry(RH39 / "main.tex"),
            "rh39_cutoff_bounds": entry(RH39 / "src" / "cutoff_bridge" / "bounds.py"),
            "rh50_hardy_manuscript": entry(RH50 / "main.tex"),
            "rh50_hardy_pilot": entry(RH50 / "results" / "two_pole_hardy_pilot.json"),
            "rh51_stein_manuscript": entry(RH51 / "main.tex"),
            "rh51_stein_pilot": entry(RH51 / "results" / "structured_stein_pilot.json"),
            "rh52_factor_manuscript": entry(RH52 / "main.tex"),
            "roadmap": entry(ROADMAP),
        },
        "limitations": [
            "The five-scale deterministic trace audit is binary64, not an interval enclosure.",
            "The 256-bit Arb run validates the algorithm on a small abstract matrix, not the N=40960 folded-Gaussian production matrix.",
            "RH-39 controls the exact-real Markov matrix cutoff before intrinsic Perron/parity factors and normalized coupling ranges are recomputed; that complete factor-aware transfer is not executed here.",
            "The theorem gives a certificate architecture for each finite matrix but does not prove a uniform or polylogarithmic small-noise Hardy trace budget; Stage A1 remains open.",
            "Consequently Stage A3 is analytically routed but not fully closed, and Stage A4 intrinsic Riesz identification is not proved.",
            "No arithmetic trace formula, prime-power identity, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, or Riemann-hypothesis conclusion is claimed.",
            "The independent TPC twin-prime program is neither assumed nor closed by this result.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "maximum_relative_energy_excess": maximum_excess,
                "maximum_production_cutoff_upper": payload[
                    "rh50_production_cutoff_ledger"
                ]["maximum_fixed_eight_two_norm_upper"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
