"""Build the analytic and finite-grid cutoff bridge certificate for RH-39."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH5 = PAPERS / "RH-5-renormalized-gaussian-response"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
sys.path.insert(0, str(ROOT / "src"))

from cutoff_bridge import (  # noqa: E402
    adaptive_cutoff_multiple,
    cutoff_bound,
    haar_cutoff_defect,
    support_half_width,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def upper_float(value: arb) -> float:
    return float(np.nextafter(float(value.upper()), np.inf))


def lower_float(value: arb) -> float:
    return float(np.nextafter(float(value.lower()), -np.inf))


def arb_fixed_bound(dimension: int) -> dict[str, object]:
    n = int(dimension)
    h = arb(1) / n
    sigma = arb(1) / 100
    multiple = arb(8)
    half_width = support_half_width(n, 0.01, 8.0)
    effective = arb(half_width) * h / sigma
    exp_half = (-(effective * effective) / 2).exp()
    omitted_mass = (
        2
        * arb(1).exp().sqrt()
        * exp_half
        * (h + sigma / effective)
        / (sigma - h)
    )
    alpha = omitted_mass / (1 - omitted_mass)
    exp_square = exp_half * exp_half
    denominator_square = (sigma - h) ** 2
    omitted_square = (
        4
        * arb(1).exp()
        * exp_square
        * (h + sigma / (2 * effective))
        / denominator_square
    )
    renormalization_square = (
        alpha**2
        * arb(1).exp()
        * (4 * h + 2 * arb.pi().sqrt() * sigma)
        / denominator_square
    )
    two_norm = (omitted_square + renormalization_square).sqrt()
    return {
        "dimension": n,
        "mesh": 1.0 / n,
        "support_half_width": half_width,
        "effective_support_multiple": upper_float(effective),
        "omitted_mass_upper": upper_float(omitted_mass),
        "infinity_norm_upper": upper_float(2 * omitted_mass),
        "omitted_frobenius_square_upper": upper_float(omitted_square),
        "renormalization_frobenius_square_upper": upper_float(
            renormalization_square
        ),
        "two_norm_upper": upper_float(two_norm),
        "arb_two_norm_ball": str(two_norm),
    }


def main() -> None:
    previous_precision = ctx.prec
    ctx.prec = 256
    try:
        fixed_levels = {
            str(dimension): arb_fixed_bound(dimension)
            for dimension in (2048, 4096, 8192)
        }
        sigma = arb(1) / 100
        multiple = arb(8)
        sqrt_two = arb(2).sqrt()
        finite_tail = (
            (multiple / sqrt_two).erfc()
            - (1 / (sqrt_two * sigma)).erfc()
        ) / (1 / (sqrt_two * sigma)).erf()
        nonvanishing = {
            "mean_zero_continuum_omitted_mass_lower": lower_float(finite_tail),
            "mean_zero_continuum_omitted_mass_upper": upper_float(finite_tail),
            "mean_zero_continuum_row_error_lower": lower_float(2 * finite_tail),
            "arb_omitted_mass_ball": str(finite_tail),
        }
    finally:
        ctx.prec = previous_precision

    coarse_first = cutoff_bound(2048, 0.01, 8.0)
    fine_first = cutoff_bound(4096, 0.01, 8.0)
    fine_second = cutoff_bound(8192, 0.01, 8.0)
    first_haar = haar_cutoff_defect(coarse_first, fine_first)
    second_haar = haar_cutoff_defect(fine_first, fine_second)
    pilot_path = ROOT / "results" / "cutoff_pilot_sigma_1e-02.json"
    component_path = (
        RH38 / "results" / "component_scaling_pilot_sigma_1e-02.json"
    )
    pilot = load(pilot_path)
    component = load(component_path)
    markov_levels = {
        "2048_to_4096": component["levels"]["2048_to_4096"]["components"][
            "markov"
        ],
        "4096_to_8192": component["levels"]["4096_to_8192"]["components"][
            "markov"
        ],
    }
    haar_levels = {
        "2048_to_4096": first_haar,
        "4096_to_8192": second_haar,
    }
    relative_diagnostics = {}
    for level, defect in haar_levels.items():
        relative_diagnostics[level] = {}
        for name in (
            "coarse_consistency",
            "coarse_to_detail",
            "detail_to_coarse",
            "detail_block",
        ):
            relative_diagnostics[level][name] = (
                getattr(defect, name)
                / float(markov_levels[level][name]["largest_singular_value"])
            )
    maximum_relative = max(
        value
        for rows in relative_diagnostics.values()
        for value in rows.values()
    )
    schedule_rows = []
    for dimension in (2048, 4096, 8192, 1048576):
        h = 1.0 / dimension
        adaptive = adaptive_cutoff_multiple(h)
        schedule_rows.append(
            {
                "dimension": dimension,
                "adaptive_multiple": adaptive,
                "fixed_eight_exceeds_adaptive": 8.0 >= adaptive,
            }
        )

    payload = {
        "status": "analytic_uniform_cutoff_bridge_with_arb_finite_grid_enclosures",
        "scope": (
            "exact-real full versus hard-cutoff folded Gaussian midpoint Markov "
            "matrices using the archived support rule on [0,1] at fixed sigma=1e-2"
        ),
        "evidence_levels": {
            "analytic_theorem": "exact support, tail, Frobenius, Haar, and schedule inequalities",
            "finite_grid_constants": "256-bit Arb interval enclosures",
            "stored_grid_mechanism": "floating full-versus-cutoff diagnostic",
        },
        "analytic_statements": {
            "support_buffer": (
                "every omitted midpoint has distance at least H_h h from |f(x)|, "
                "where H_h=ceil(L sigma/h)+2"
            ),
            "row_identity": "infinity-row error equals twice the omitted full-row mass",
            "fixed_multiple": (
                "a fixed L has a positive continuum row defect and does not "
                "converge to the full kernel in the row-operator norm"
            ),
            "adaptive_schedule": "L(h)=max(5,sqrt(4 log(1/h))) gives two-norm cutoff defect O(h^2)",
            "haar_bridge": (
                "cutoff contributions are epsilon_h+epsilon_h/2 for E and "
                "epsilon_h/2 for C,B,D"
            ),
        },
        "arb_precision_bits": 256,
        "fixed_eight_sigma_levels": fixed_levels,
        "fixed_eight_sigma_nonvanishing_limit": nonvanishing,
        "haar_cutoff_defect_uppers": {
            "2048_to_4096": first_haar.__dict__,
            "4096_to_8192": second_haar.__dict__,
        },
        "floating_markov_relative_diagnostics": relative_diagnostics,
        "maximum_cutoff_upper_over_floating_markov_block": maximum_relative,
        "schedule": {
            "formula": "max(5,sqrt(4 log(1/h)))",
            "eight_sigma_crossover_dimension_floor": int(math.floor(math.exp(16.0))),
            "rows": schedule_rows,
        },
        "floating_pilot": {
            "path": str(pilot_path.relative_to(ROOT)),
            "sha256": sha256_file(pilot_path),
            "maximum_actual_omitted_mass": max(
                float(row["maximum_omitted_mass"])
                for row in pilot["dimensions"]
            ),
            "maximum_actual_frobenius_norm": max(
                float(row["frobenius_norm"]) for row in pilot["dimensions"]
            ),
        },
        "dependencies": {
            "rh5_twice_tail_manuscript": {
                "path": str((RH5 / "main.tex").relative_to(REPOSITORY)),
                "sha256": sha256_file(RH5 / "main.tex"),
            },
            "rh18_archived_sparse_builder": {
                "path": str(
                    (RH18 / "src" / "gaussian_return" / "operators.py").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH18 / "src" / "gaussian_return" / "operators.py"
                ),
            },
            "rh38_component_pilot": {
                "path": str(component_path.relative_to(REPOSITORY)),
                "sha256": sha256_file(component_path),
            },
            "rh38_decay_certificate": {
                "path": str(
                    (
                        RH38
                        / "results"
                        / "dyadic_haar_block_decay_certificate.json"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH38
                    / "results"
                    / "dyadic_haar_block_decay_certificate.json"
                ),
            },
        },
        "limitations": [
            "The theorem closes only the hard-cutoff gate for the Markov component.",
            "It does not enclose every binary64 transcendental and normalization operation used to build the stored sparse arrays.",
            "It does not validate convergence of the computed Perron/parity projectors.",
            "The fixed eight-sigma family has a tiny but mathematically nonzero full-kernel defect.",
            "The adaptive schedule is a sufficient bound, not an optimal cutoff law.",
            "The floating pilot is diagnostic and is not used as an interval enclosure.",
            "No zero-noise, zeta-zero, Hilbert-Polya, or Riemann-hypothesis claim is made.",
        ],
    }
    output = ROOT / "results" / "uniform_gaussian_cutoff_bridge_certificate.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
