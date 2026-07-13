#!/usr/bin/env python3
"""Reproduce two-step blindness, directed traces, and logarithmic scaling."""

from __future__ import annotations

import argparse
import csv
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.linalg as la

from temporal_spectrum.operators import (
    gaussian_markov_family,
    gaussian_markov_matrix,
    nonperron_spectrum,
    stationary_distribution,
)
from temporal_spectrum.orientation import (
    commutator,
    matched_spectrum_error,
    matrix_infinity_norm,
    orientation_curvature,
    orientation_trace,
    parity_block_family,
    parity_orientation_curvature,
    vandermonde,
)


U_CRITICAL = 1.5436890127


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def curvature_values(d: int, u: float, sigma: float) -> tuple[float, float]:
    _, matrix, first, second = gaussian_markov_family(d, u, sigma)
    one_step = float(orientation_curvature(matrix, first, second).real)
    paired = float(parity_orientation_curvature(matrix, first, second).real)
    return one_step, paired


def stationary_commutator_response(
    matrix: np.ndarray,
    first: np.ndarray,
) -> np.ndarray:
    """Solve eta(I-K^2)=pi[K,K'] with eta 1=0."""
    block = matrix @ matrix
    stationary = stationary_distribution(matrix)
    rhs = stationary @ commutator(matrix, first)
    fundamental = np.eye(matrix.shape[0]) - block + np.ones((matrix.shape[0], 1)) @ stationary[None, :]
    return la.solve(fundamental.T, rhs, assume_a="gen")


def pair_order_scaling(
    d: int,
    u: float,
    sigma: float,
    epsilons: np.ndarray,
) -> tuple[list[dict[str, object]], dict[str, object], list[dict[str, object]]]:
    grid, matrix, first, _ = gaussian_markov_family(d, u, sigma)
    oriented_commutator = commutator(matrix, first)
    eta = stationary_commutator_response(matrix, first)
    observable = np.cos(np.pi * grid) + 0.3 * np.sin(2.0 * np.pi * grid)
    source_index = int(np.argmin(np.abs(grid - 0.8)))

    rows: list[dict[str, object]] = []
    for epsilon in epsilons:
        minus = gaussian_markov_matrix(d, u - float(epsilon), sigma)
        plus = gaussian_markov_matrix(d, u + float(epsilon), sigma)
        forward = minus @ plus
        reverse = plus @ minus
        difference = forward - reverse
        pi_forward = stationary_distribution(forward)
        pi_reverse = stationary_distribution(reverse)
        rows.append(
            {
                "epsilon": float(epsilon),
                "operator_infinity_difference": matrix_infinity_norm(difference),
                "stationary_total_variation": float(
                    0.5 * np.sum(np.abs(pi_forward - pi_reverse))
                ),
                "observable_difference": float(
                    abs((difference @ observable)[source_index])
                ),
                "normalized_commutator_error": matrix_infinity_norm(
                    difference / (2.0 * epsilon) - oriented_commutator
                ),
            }
        )

    fit_mask = epsilons <= 0.006
    fits: dict[str, float] = {}
    for key in (
        "operator_infinity_difference",
        "stationary_total_variation",
        "observable_difference",
        "normalized_commutator_error",
    ):
        values = np.array([float(row[key]) for row in rows])
        fits[key] = float(
            np.polyfit(np.log(epsilons[fit_mask]), np.log(values[fit_mask]), 1)[0]
        )

    selected_epsilon = 0.02
    minus = gaussian_markov_matrix(d, u - selected_epsilon, sigma)
    plus = gaussian_markov_matrix(d, u + selected_epsilon, sigma)
    forward = minus @ plus
    reverse = plus @ minus
    spectral_audit = matched_spectrum_error(forward, reverse, threshold=1.0e-7)
    pi_forward = stationary_distribution(forward)
    pi_reverse = stationary_distribution(reverse)
    transported = pi_forward @ minus
    spectral_audit.update(
        {
            "epsilon": selected_epsilon,
            "matrix_infinity_difference": matrix_infinity_norm(forward - reverse),
            "stationary_transport_error": float(np.max(np.abs(transported - pi_reverse))),
        }
    )

    spectrum_rows: list[dict[str, object]] = []
    for order, product in (("forward", forward), ("reverse", reverse)):
        values = nonperron_spectrum(product)
        values = values[np.argsort(-np.abs(values))]
        for rank, value in enumerate(values, start=1):
            spectrum_rows.append(
                {
                    "order": order,
                    "rank_by_modulus": rank,
                    "real": float(value.real),
                    "imag": float(value.imag),
                    "modulus": float(abs(value)),
                }
            )

    predictions = {
        "slopes": fits,
        "leading_coefficients": {
            "operator_difference_over_epsilon": 2.0
            * matrix_infinity_norm(oriented_commutator),
            "stationary_tv_over_epsilon": float(np.sum(np.abs(eta))),
            "observable_difference_over_epsilon": float(
                2.0 * abs((oriented_commutator @ observable)[source_index])
            ),
        },
        "spectral_audit": spectral_audit,
    }
    return rows, predictions, spectrum_rows


def curvature_atlas(
    d: int,
    u_values: np.ndarray,
    sigmas: list[float],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sigma in sigmas:
        for index, u in enumerate(u_values):
            one_step, paired = curvature_values(d, float(u), sigma)
            rows.append(
                {
                    "sigma": sigma,
                    "u": float(u),
                    "one_step_curvature": one_step,
                    "parity_block_curvature": paired,
                }
            )
            if index % 20 == 0:
                print(f"curvature sigma={sigma:g} {index + 1}/{len(u_values)}", flush=True)
    return rows


def curvature_convergence(
    dimensions: list[int],
    u: float,
    sigma: float,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    for d in dimensions:
        one_step, paired = curvature_values(d, u, sigma)
        rows.append(
            {
                "d": d,
                "h": 2.0 / d,
                "one_step_curvature": one_step,
                "parity_block_curvature": paired,
            }
        )
        print(f"curvature dimension {d}", flush=True)

    x = np.array([4.0 / d**2 for d in dimensions])
    fit_mask = np.array(dimensions) >= 384
    metadata: dict[str, object] = {"fits": {}}
    for key in ("one_step_curvature", "parity_block_curvature"):
        values = np.array([float(row[key]) for row in rows])
        coefficients = np.polyfit(x[fit_mask], values[fit_mask], 2)
        continuum = float(coefficients[-1])
        errors = np.abs(values - continuum)
        slope_mask = np.array(dimensions) >= 256
        slope = float(
            np.polyfit(
                np.log(np.array(dimensions)[slope_mask]),
                np.log(errors[slope_mask]),
                1,
            )[0]
        )
        for row, error in zip(rows, errors, strict=True):
            row[f"error_{key}"] = float(error)
        metadata["fits"][key] = {
            "continuum_extrapolation": continuum,
            "dimension_slope": slope,
            "quadratic_in_h2_coefficients": [float(value) for value in coefficients],
        }
    return rows, metadata


def vandermonde_scaling(
    d: int,
    u: float,
    sigma: float,
    epsilons: np.ndarray,
) -> tuple[list[dict[str, object]], dict[str, float]]:
    _, matrix, first, second = gaussian_markov_family(d, u, sigma)
    curvature = float(orientation_curvature(matrix, first, second).real)
    parity_curvature = float(
        parity_orientation_curvature(matrix, first, second).real
    )
    middle = matrix
    middle_block = middle @ middle
    rows: list[dict[str, object]] = []
    for epsilon in epsilons:
        minus = gaussian_markov_matrix(d, u - float(epsilon), sigma)
        plus = gaussian_markov_matrix(d, u + float(epsilon), sigma)
        factor = vandermonde(u - epsilon, u, u + epsilon)
        directed = float(orientation_trace(minus, middle, plus).real)
        minus_block = minus @ minus
        plus_block = plus @ plus
        directed_parity = float(
            orientation_trace(minus_block, middle_block, plus_block).real
        )
        rows.append(
            {
                "epsilon": float(epsilon),
                "vandermonde": factor,
                "one_step_trace": directed,
                "one_step_quotient": directed / factor,
                "one_step_relative_error": abs(directed / factor - curvature)
                / abs(curvature),
                "six_step_trace": directed_parity,
                "six_step_quotient": directed_parity / factor,
                "six_step_relative_error": abs(
                    directed_parity / factor - parity_curvature
                )
                / abs(parity_curvature),
            }
        )
    small = epsilons <= 0.006
    slopes = {
        "one_step_relative_error": float(
            np.polyfit(
                np.log(epsilons[small]),
                np.log([float(row["one_step_relative_error"]) for row in rows if float(row["epsilon"]) <= 0.006]),
                1,
            )[0]
        ),
        "six_step_relative_error": float(
            np.polyfit(
                np.log(epsilons[small]),
                np.log([float(row["six_step_relative_error"]) for row in rows if float(row["epsilon"]) <= 0.006]),
                1,
            )[0]
        ),
        "one_step_curvature": curvature,
        "parity_block_curvature": parity_curvature,
    }
    return rows, slopes


def alternating_pair_tail(
    start: int,
    kappa: float,
    p: float,
    shift: float,
    terms: int = 42,
) -> float:
    """Euler-transform the tail 1/2 sum_j (s_2j-s_(2j-1))."""
    indices = 2.0 * start - 1.0 + np.arange(terms + 1, dtype=float)
    values = kappa / np.log(indices + shift) ** p
    transformed = 0.5 * values[0]
    differences = values
    factor = 0.25
    for _ in range(1, terms):
        differences = differences[:-1] - differences[1:]
        transformed += factor * differences[0]
        factor *= 0.5
    return float(-0.5 * transformed)


def schedule_scaling(
    d: int,
    u: float,
    sigma: float,
    logarithms: np.ndarray,
    *,
    p: float = 2.0,
    kappa: float = 0.5,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, float]]:
    alphas = np.array([0.25, 0.5, 1.0])
    log_alphas = np.log(alphas)
    _, matrix, first, second = gaussian_markov_family(d, u, sigma)
    curvature = float(orientation_curvature(matrix, first, second).real)
    parity_curvature = float(
        parity_orientation_curvature(matrix, first, second).real
    )
    scalar_limit = -(kappa * p) ** 3 * vandermonde(*log_alphas)
    one_step_limit = curvature * scalar_limit
    parity_limit = parity_curvature * scalar_limit

    rows: list[dict[str, object]] = []
    for logarithm in logarithms:
        parameters = u + kappa / (logarithm + log_alphas) ** p
        matrices = [gaussian_markov_matrix(d, value, sigma) for value in parameters]
        factor = vandermonde(*parameters)
        one_step = float(orientation_trace(*matrices).real)
        blocks = [value @ value for value in matrices]
        parity = float(orientation_trace(*blocks).real)
        scale = logarithm ** (3.0 * p + 3.0)
        rows.append(
            {
                "log_T": float(logarithm),
                "scaled_vandermonde": scale * factor,
                "one_step_quotient": one_step / factor,
                "scaled_one_step_trace": scale * one_step,
                "six_step_quotient": parity / factor,
                "scaled_six_step_trace": scale * parity,
            }
        )

    tail_rows: list[dict[str, object]] = []
    for start in np.unique(np.rint(np.logspace(1.0, 7.0, 25)).astype(int)):
        tail = alternating_pair_tail(int(start), kappa, p, shift=10.0)
        log_start = np.log(2.0 * start + 10.0)
        odd = kappa / np.log(2.0 * start - 1.0 + 10.0) ** p
        even = kappa / np.log(2.0 * start + 10.0) ** p
        half_increment = 0.5 * (even - odd)
        tail_rows.append(
            {
                "start_pair": int(start),
                "half_increment": half_increment,
                "normalized_increment": half_increment
                * start
                * log_start ** (p + 1.0),
                "tail_sum": tail,
                "normalized_tail": tail * log_start**p,
            }
        )

    limits = {
        "scaled_vandermonde_limit": scalar_limit,
        "scaled_one_step_trace_limit": one_step_limit,
        "scaled_six_step_trace_limit": parity_limit,
        "normalized_half_increment_limit": -kappa * p / 4.0,
        "normalized_tail_limit": -kappa / 4.0,
    }
    return rows, tail_rows, limits


def make_pair_figure(
    rows: list[dict[str, object]],
    predictions: dict[str, object],
    spectrum_rows: list[dict[str, object]],
    path: Path,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.55))
    eps = np.array([float(row["epsilon"]) for row in rows])
    series = (
        ("operator_infinity_difference", "operator difference", "#3b4cc0"),
        ("stationary_total_variation", "stationary TV", "#1f968b"),
        ("observable_difference", "one observable", "#d1495b"),
    )
    for key, label, color in series:
        values = np.array([float(row[key]) for row in rows])
        slope = predictions["slopes"][key]
        axes[0].loglog(eps, values, "o-", color=color, label=f"{label}, slope {slope:.2f}")
    axes[0].set_xlabel(r"half separation $\varepsilon$")
    axes[0].set_ylabel("order-reversal difference")
    axes[0].set_title("Order survives outside eigenvalues")
    axes[0].legend(frameon=False, fontsize=7)

    colors = {"forward": "#3b4cc0", "reverse": "#d1495b"}
    markers = {"forward": "o", "reverse": "x"}
    for order in ("forward", "reverse"):
        selected = [row for row in spectrum_rows if row["order"] == order]
        values = np.array([complex(float(row["real"]), float(row["imag"])) for row in selected])
        visible = np.abs(values) > 1.0e-5
        if order == "forward":
            axes[1].scatter(
                values.real[visible],
                values.imag[visible],
                s=28,
                facecolors="none",
                edgecolors=colors[order],
                marker=markers[order],
                label=order,
            )
        else:
            axes[1].scatter(
                values.real[visible],
                values.imag[visible],
                s=28,
                color=colors[order],
                marker=markers[order],
                label=order,
            )
    axes[1].axhline(0.0, color="0.75", lw=0.7)
    axes[1].axvline(0.0, color="0.75", lw=0.7)
    all_visible = [
        row
        for row in spectrum_rows
        if float(row["modulus"]) > 1.0e-5
    ]
    imaginary_bound = max(
        0.04,
        1.25 * max(abs(float(row["imag"])) for row in all_visible),
    )
    axes[1].set_xlim(-0.45, 1.03)
    axes[1].set_ylim(-imaginary_bound, imaginary_bound)
    axes[1].set_title(r"$K_-K_+$ and $K_+K_-$ spectra")
    axes[1].set_xlabel(r"$\Re\lambda$")
    axes[1].set_ylabel(r"$\Im\lambda$")
    axes[1].legend(frameon=False, fontsize=8)

    remainder = np.array([float(row["normalized_commutator_error"]) for row in rows])
    slope = predictions["slopes"]["normalized_commutator_error"]
    axes[2].loglog(eps, remainder, "o-", color="#8f2d56", label=f"fit slope {slope:.2f}")
    axes[2].loglog(eps, remainder[0] * (eps / eps[0]) ** 2, "--", color="0.3", label=r"$\varepsilon^2$ guide")
    axes[2].set_xlabel(r"half separation $\varepsilon$")
    axes[2].set_ylabel(r"$\|(Q_+-Q_-)/(2\varepsilon)-[K,K']\|_\infty$")
    axes[2].set_title("Commutator expansion")
    axes[2].legend(frameon=False, fontsize=8)

    for axis in axes:
        axis.grid(alpha=0.23, which="both")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


def make_curvature_figure(
    atlas_rows: list[dict[str, object]],
    scaling_rows: list[dict[str, object]],
    scaling_meta: dict[str, float],
    path: Path,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.55))
    palette = {0.03: "#3b4cc0", 0.05: "#1f968b", 0.08: "#f0a202", 0.12: "#d1495b"}
    for sigma, color in palette.items():
        selected = [row for row in atlas_rows if float(row["sigma"]) == sigma]
        u = [float(row["u"]) for row in selected]
        axes[0].plot(u, [float(row["one_step_curvature"]) for row in selected], color=color, label=rf"$\sigma={sigma:g}$")
        axes[1].plot(u, [float(row["parity_block_curvature"]) for row in selected], color=color, label=rf"$\sigma={sigma:g}$")
    for axis in axes[:2]:
        axis.axhline(0.0, color="0.6", lw=0.7)
        axis.axvline(U_CRITICAL, color="0.5", ls="--", lw=0.8)
        axis.set_yscale("symlog", linthresh=1.0)
        axis.set_xlabel(r"quadratic parameter $u$")
        axis.grid(alpha=0.23)
    axes[0].set_title(r"One-step curvature $\chi_K$")
    axes[0].set_ylabel("orientation curvature")
    axes[0].legend(frameon=False, fontsize=7, ncol=2)
    axes[1].set_title(r"Parity-block curvature $\chi_Q$")

    eps = np.array([float(row["epsilon"]) for row in scaling_rows])
    for key, label, color in (
        ("one_step_relative_error", rf"$\chi_K$, slope {scaling_meta['one_step_relative_error']:.2f}", "#3b4cc0"),
        ("six_step_relative_error", rf"$\chi_Q$, slope {scaling_meta['six_step_relative_error']:.2f}", "#d1495b"),
    ):
        axes[2].loglog(eps, [float(row[key]) for row in scaling_rows], "o-", color=color, label=label)
    first_error = float(scaling_rows[0]["one_step_relative_error"])
    axes[2].loglog(eps, first_error * (eps / eps[0]) ** 2, "--", color="0.35", label=r"$\varepsilon^2$ guide")
    axes[2].set_xlabel(r"symmetric separation $\varepsilon$")
    axes[2].set_ylabel("relative quotient error")
    axes[2].set_title("Vandermonde cubic law")
    axes[2].grid(alpha=0.23, which="both")
    axes[2].legend(frameon=False, fontsize=7)

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


def make_schedule_figure(
    convergence_rows: list[dict[str, object]],
    convergence_meta: dict[str, object],
    schedule_rows: list[dict[str, object]],
    tail_rows: list[dict[str, object]],
    limits: dict[str, float],
    path: Path,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.55))
    dimensions = np.array([int(row["d"]) for row in convergence_rows])
    for key, label, color in (
        ("one_step_curvature", r"$\chi_K$", "#3b4cc0"),
        ("parity_block_curvature", r"$\chi_Q$", "#d1495b"),
    ):
        slope = convergence_meta["fits"][key]["dimension_slope"]
        errors = [float(row[f"error_{key}"]) for row in convergence_rows]
        axes[0].loglog(dimensions, errors, "o-", color=color, label=f"{label}, slope {slope:.2f}")
    guide = dimensions.astype(float) ** -2
    axes[0].loglog(dimensions, float(convergence_rows[0]["error_one_step_curvature"]) * guide / guide[0], "--", color="0.35", label=r"$d^{-2}$ guide")
    axes[0].set_xlabel(r"full dimension $d$")
    axes[0].set_ylabel("extrapolation error")
    axes[0].set_title("Curvature continuum limit")
    axes[0].legend(frameon=False, fontsize=8)

    logs = np.array([float(row["log_T"]) for row in schedule_rows])
    axes[1].plot(logs, [float(row["scaled_one_step_trace"]) for row in schedule_rows], "o-", color="#3b4cc0", label=r"$(\log T)^9\Omega_3$")
    axes[1].plot(logs, [float(row["scaled_six_step_trace"]) for row in schedule_rows], "o-", color="#d1495b", label=r"$(\log T)^9\Omega_6$")
    axes[1].axhline(limits["scaled_one_step_trace_limit"], color="#3b4cc0", ls="--")
    axes[1].axhline(limits["scaled_six_step_trace_limit"], color="#d1495b", ls="--")
    axes[1].set_xlabel(r"$\log T$")
    axes[1].set_ylabel("renormalized directed trace")
    axes[1].set_title(r"Macroscopic schedule, $p=2$")
    axes[1].legend(frameon=False, fontsize=8)

    starts = np.array([int(row["start_pair"]) for row in tail_rows])
    axes[2].semilogx(starts, [float(row["normalized_tail"]) for row in tail_rows], "o-", color="#1f968b", label=r"$(\log(2J))^p\sum_{j\geq J}\varepsilon_j$")
    axes[2].semilogx(starts, [float(row["normalized_increment"]) for row in tail_rows], "s-", color="#f0a202", label=r"$J(\log(2J))^{p+1}\varepsilon_J$")
    axes[2].axhline(limits["normalized_tail_limit"], color="#1f968b", ls="--")
    axes[2].axhline(limits["normalized_half_increment_limit"], color="#f0a202", ls="--")
    axes[2].set_xlabel(r"starting pair $J$")
    axes[2].set_ylabel("normalized scalar coefficient")
    axes[2].set_title("Summable pair-order tail")
    axes[2].legend(frameon=False, fontsize=7)

    for axis in axes:
        axis.grid(alpha=0.23, which="both")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--u", type=float, default=U_CRITICAL)
    parser.add_argument("--sigma", type=float, default=0.05)
    parser.add_argument("--pair-dimension", type=int, default=768)
    parser.add_argument("--atlas-dimension", type=int, default=384)
    parser.add_argument("--curvature-dimension", type=int, default=768)
    parser.add_argument("--schedule-dimension", type=int, default=512)
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--figures", type=Path, default=Path("figures"))
    args = parser.parse_args()

    epsilons = np.geomspace(2.0e-4, 3.0e-2, 11)
    pair_rows, pair_meta, spectrum_rows = pair_order_scaling(
        args.pair_dimension, args.u, args.sigma, epsilons
    )
    atlas_rows = curvature_atlas(
        args.atlas_dimension,
        np.linspace(1.35, 1.75, 81),
        [0.03, 0.05, 0.08, 0.12],
    )
    dimensions = [128, 192, 256, 384, 512, 768, 1024, 1536, 2048]
    convergence_rows, convergence_meta = curvature_convergence(
        dimensions, args.u, args.sigma
    )
    vandermonde_rows, vandermonde_meta = vandermonde_scaling(
        args.curvature_dimension,
        args.u,
        args.sigma,
        np.geomspace(5.0e-4, 3.0e-2, 11),
    )
    schedule_rows, tail_rows, schedule_limits = schedule_scaling(
        args.schedule_dimension,
        args.u,
        args.sigma,
        np.array([6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]),
    )

    write_csv(args.results / "pair_order_scaling.csv", pair_rows)
    write_csv(args.results / "two_step_spectra.csv", spectrum_rows)
    write_csv(args.results / "curvature_atlas.csv", atlas_rows)
    write_csv(args.results / "curvature_convergence.csv", convergence_rows)
    write_csv(args.results / "vandermonde_scaling.csv", vandermonde_rows)
    write_csv(args.results / "schedule_scaling.csv", schedule_rows)
    write_csv(args.results / "pair_tail_scaling.csv", tail_rows)

    metadata = {
        "parameters": {
            "u_critical": args.u,
            "sigma": args.sigma,
            "pair_dimension": args.pair_dimension,
            "atlas_dimension": args.atlas_dimension,
            "curvature_dimension": args.curvature_dimension,
            "schedule_dimension": args.schedule_dimension,
            "target_data_loaded": False,
        },
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "pair_order": pair_meta,
        "curvature_convergence": convergence_meta,
        "vandermonde_scaling": vandermonde_meta,
        "schedule_limits": schedule_limits,
    }
    args.results.mkdir(parents=True, exist_ok=True)
    with (args.results / "temporal_orientation_summary.json").open("w") as handle:
        json.dump(metadata, handle, indent=2)

    make_pair_figure(
        pair_rows,
        pair_meta,
        spectrum_rows,
        args.figures / "two_step_blindness.pdf",
    )
    make_curvature_figure(
        atlas_rows,
        vandermonde_rows,
        vandermonde_meta,
        args.figures / "orientation_curvature.pdf",
    )
    make_schedule_figure(
        convergence_rows,
        convergence_meta,
        schedule_rows,
        tail_rows,
        schedule_limits,
        args.figures / "resolution_schedule.pdf",
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
