"""Compose the RH-51 theorem and numerical evidence ledger."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
ROADMAP = PAPERS / "RH-ROADMAP-after-RH50.md"
PILOT = ROOT / "results" / "structured_stein_pilot.json"
OUTPUT = ROOT / "results" / "structured_stein_certificate.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path, *, local: bool = False) -> dict[str, str]:
    base = ROOT if local else REPOSITORY
    return {
        "path": str(path.relative_to(base)),
        "sha256": sha256_file(path),
    }


def linear_fit(x, y) -> dict[str, float | int]:
    abscissa = np.asarray(x, dtype=np.float64)
    ordinate = np.asarray(y, dtype=np.float64)
    slope, intercept = np.polyfit(abscissa, ordinate, 1)
    residual = ordinate - (slope * abscissa + intercept)
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "maximum_absolute_residual": float(np.max(np.abs(residual))),
        "levels": len(ordinate),
    }


def power_fit(x, y) -> dict[str, float | int]:
    fit = linear_fit(np.log(np.asarray(x)), np.log(np.asarray(y)))
    return {
        "power": fit["slope"],
        "log_intercept": fit["intercept"],
        "maximum_log_residual": fit["maximum_absolute_residual"],
        "levels": fit["levels"],
    }


def main() -> None:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = pilot["rows"]
    merged = []
    for row in rows:
        left_block = row["left_block_completion"]
        right_block = row["right_block_completion"]
        left_energy = float(row["left_exact_hardy_energy"])
        right_energy = float(row["right_exact_hardy_energy"])
        merged.append(
            {
                "sigma": float(row["sigma"]),
                "fine_dimension": int(row["fine_dimension"]),
                "left_exact_hardy_energy": left_energy,
                "right_exact_hardy_energy": right_energy,
                "left_participation_rank": float(
                    row["left_gramian"]["participation_rank"]
                ),
                "right_participation_rank": float(
                    row["right_gramian"]["participation_rank"]
                ),
                "left_rank_for_99_percent_trace": int(
                    row["left_gramian"]["rank_for_99_percent_trace"]
                ),
                "right_rank_for_99_percent_trace": int(
                    row["right_gramian"]["rank_for_99_percent_trace"]
                ),
                "left_source_numerical_rank": int(
                    row["left_cyclic_rank_profile"][0]["numerical_rank"]
                ),
                "left_cyclic_numerical_rank": int(
                    row["left_cyclic_rank_profile"][-1]["numerical_rank"]
                ),
                "left_cyclic_rank_fraction": float(
                    row["left_cyclic_rank_profile"][-1]["rank_fraction"]
                ),
                "identity_unforced_defect_minimum": float(
                    row["identity_metric"][
                        "minimum_unforced_defect_eigenvalue"
                    ]
                ),
                "identity_cone_obstructed": bool(
                    row["identity_metric"][
                        "scalar_identity_cone_obstructed"
                    ]
                ),
                "diagonal_extraction_is_supersolution": bool(
                    row["diagonal_of_exact_gramian"][
                        "is_a_supersolution"
                    ]
                ),
                "diagonal_extraction_defect_minimum": float(
                    row["diagonal_of_exact_gramian"][
                        "minimum_stein_defect_eigenvalue"
                    ]
                ),
                "left_selected_block_horizon": int(
                    left_block["selected_horizon"]
                ),
                "right_selected_block_horizon": int(
                    right_block["selected_horizon"]
                ),
                "left_selected_power_norm": float(
                    left_block["selected_power_norm"]
                ),
                "right_selected_power_norm": float(
                    right_block["selected_power_norm"]
                ),
                "left_block_energy_upper": float(
                    left_block["energy_upper"]
                ),
                "right_block_energy_upper": float(
                    right_block["energy_upper"]
                ),
                "left_block_relative_excess": float(
                    left_block["energy_upper"] / left_energy - 1.0
                ),
                "right_block_relative_excess": float(
                    right_block["energy_upper"] / right_energy - 1.0
                ),
                "left_block_defect_minimum": float(
                    left_block["block_defect_minimum_eigenvalue"]
                ),
                "right_block_defect_minimum": float(
                    right_block["block_defect_minimum_eigenvalue"]
                ),
            }
        )

    dimensions = [row["fine_dimension"] for row in merged]
    payload = {
        "status": (
            "rigorous_minimal_gramian_cyclic_rank_obstruction_and_growing_horizon_block_stein_route"
        ),
        "scope": (
            "structured positive Stein certificates for the two-pole Hilbert-Schmidt Hardy energies of RH-50"
        ),
        "evidence_level": {
            "analytic": (
                "exact finite-dimensional minimal-Gramian theorem, cyclic-support rank obstruction, low-rank-plus-floor lower bound, block-Stein domination theorem, isotropic and anisotropic residual completions, and conic dual no-go witnesses"
            ),
            "numerical": (
                "binary64 five-scale dense exact-Gramian and block-completion audit through dimension 512; not interval validated"
            ),
        },
        "minimal_gramian": {
            "definition": "G=sum_(m>=0) A^m X X^* (A^*)^m",
            "equation": "G-A G A^*=X X^*",
            "minimality": (
                "H>=0 and H-A H A^*>=X X^* imply H>=G"
            ),
            "cyclic_support": (
                "Ran(G)=span{A^m Ran(X):m>=0} in finite dimensions"
            ),
        },
        "cyclic_rank_obstruction": {
            "invariance": (
                "every positive supersolution has A-invariant range containing Ran(X)"
            ),
            "rank_lower": (
                "rank(H)>=dim span{A^m Ran(X):m>=0}=rank(G)"
            ),
            "consequence": (
                "a fixed-rank exact supersolution family is impossible whenever the directional cyclic dimension diverges"
            ),
            "physical_divergence_proved_analytically_here": False,
        },
        "low_rank_plus_floor": {
            "statement": (
                "if H=Z Z^*+alpha I>=G and rank(Z)<=k, then alpha>=lambda_(k+1)(G)"
            ),
            "interpretation": (
                "low-rank factors can be retained only by paying a full-dimensional positive background floor"
            ),
        },
        "block_stein": {
            "finite_sum": (
                "S_M=sum_(j=0)^(M-1) A^j X X^* (A^*)^j"
            ),
            "certificate": (
                "H-A^M H(A^*)^M>=S_M implies H>=G"
            ),
            "one_step_implies_every_block": True,
            "block_certificate_need_not_be_one_step": True,
            "fixed_rank_obstruction_removed": False,
            "fixed_step_global_contraction_required": False,
            "horizon_may_grow_with_noise_or_dimension": True,
        },
        "isotropic_block_completion": {
            "condition": "q_M=||A^M||_2<1",
            "candidate": "H_M=S_M+alpha_M I",
            "floor": (
                "alpha_M=||A^M S_M(A^*)^M||_2/(1-q_M^2)"
            ),
            "energy_upper": (
                "tr(Y G Y^*)<=tr(Y S_M Y^*)+alpha_M||Y||_S2^2"
            ),
            "meaning": (
                "RH-50's fixed-step no-go is compatible with M=M(sigma,n) increasing"
            ),
        },
        "anisotropic_residual_completion": {
            "statement": (
                "if D_M(W)>=mu I and R_M=S_M-D_M(Hhat), then Hhat+alpha W is a block supersolution for alpha>=max(0,lambda_max(R_M))/mu"
            ),
            "purpose": (
                "replace the dimension-costly identity floor by localized, banded, or multilevel positive backgrounds"
            ),
        },
        "conic_dual_no_go": {
            "statement": (
                "Z>=0, tr[Z(W_j-AW_jA^*)]<=0 for every generator, and tr(ZXX^*)>0 rule out every nonnegative conic combination of the W_j"
            ),
            "rank_one_specialization": "Z=v v^*",
        },
        "floating_five_scale_audit": {
            "rows": merged,
            "noise_levels": len(merged),
            "largest_dimension": max(dimensions),
            "resolution": pilot["fine_resolution"],
            "hardy_radius": pilot["hardy_radius"],
            "cyclic_relative_singular_tolerance": pilot[
                "cyclic_relative_singular_tolerance"
            ],
            "left_cyclic_rank_power_fit": power_fit(
                dimensions,
                [row["left_cyclic_numerical_rank"] for row in merged],
            ),
            "left_rank99_power_fit": power_fit(
                dimensions,
                [row["left_rank_for_99_percent_trace"] for row in merged],
            ),
            "right_rank99_power_fit": power_fit(
                dimensions,
                [row["right_rank_for_99_percent_trace"] for row in merged],
            ),
            "selected_horizon_log2_fit": linear_fit(
                [math.log2(value) for value in dimensions],
                [row["left_selected_block_horizon"] for row in merged],
            ),
            "maximum_left_block_relative_excess": max(
                row["left_block_relative_excess"] for row in merged
            ),
            "maximum_right_block_relative_excess": max(
                row["right_block_relative_excess"] for row in merged
            ),
            "identity_cone_obstructed_levels": sum(
                row["identity_cone_obstructed"] for row in merged
            ),
            "diagonal_extraction_failed_levels": sum(
                not row["diagonal_extraction_is_supersolution"]
                for row in merged
            ),
            "interval_validated": False,
        },
        "program_conclusion": {
            "fixed_rank_shortcut": "structurally closed unless cyclic dimension stays uniformly bounded",
            "scalar_identity_shortcut": "fails by explicit floating dual witnesses at the four finest stored scales",
            "diagonal_extraction_shortcut": "fails at all five stored scales",
            "growing_horizon_route": (
                "survives and gives near-exact finite-matrix uppers at horizons 4,8,16,24,32"
            ),
            "stage_A1_closed": False,
            "remaining_A1_gate": (
                "prove a dyadically uniform analytic trace budget for anisotropic or multilevel growing-horizon completions"
            ),
        },
        "dependencies": {
            "rh49_quarter_power_manuscript": entry(RH49 / "main.tex"),
            "rh50_hardy_stein_manuscript": entry(RH50 / "main.tex"),
            "post_rh50_roadmap": entry(ROADMAP),
            "local_pilot": entry(PILOT, local=True),
        },
        "limitations": [
            "The physical folded-Gaussian family is not proved here to have a cyclic dimension diverging as sigma tends to zero; the stored ranks are threshold-dependent binary64 evidence.",
            "The five-scale dense audit uses N sigma=5.12 and is not an interval or production-resolution validation.",
            "The logarithmic-looking selected horizons are finite evidence, not a uniform asymptotic mixing theorem.",
            "The isotropic completion pays alpha times the observation Hilbert-Schmidt dimension; an analytic anisotropic trace budget remains open.",
            "Failure of the identity cone and of one extracted diagonal does not rule out all diagonal, banded, localized, hierarchical, or multilevel positive metrics.",
            "No small-noise intrinsic Riesz identification theorem, renormalized determinant limit, arithmetic trace formula, prime-power identity, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, Riemann-hypothesis proof, or twin-prime conclusion is claimed.",
            "The independent TPC program may be referenced for techniques but is not an assumption or completed arithmetic interface in this RH result.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "horizon_fit": payload["floating_five_scale_audit"][
                    "selected_horizon_log2_fit"
                ],
                "cyclic_fit": payload["floating_five_scale_audit"][
                    "left_cyclic_rank_power_fit"
                ],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
