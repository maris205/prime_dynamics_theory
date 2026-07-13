#!/usr/bin/env python3
"""Generate the target-independent resonance, trace, and contraction audit."""

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

from cycle_spectrum.invariants import (
    centered_trace_derivatives,
    centered_trace_moments,
    exact_dobrushin_coefficient,
    multistep_dobrushin_roots,
    regularized_logabs,
)
from cycle_spectrum.operators import (
    conditioned_eigenvalues,
    fold_matrix,
    gaussian_markov_family,
    nonperron_spectrum,
)


U_CRITICAL = 1.5436890127


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def without_perron(
    eigenvalues: np.ndarray,
    companions: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray | None]:
    index = int(np.argmin(np.abs(eigenvalues - 1.0)))
    values = np.delete(eigenvalues, index)
    if companions is None:
        return values, None
    return values, np.delete(companions, index)


def atlas_scan(
    dimension: int,
    sigma: float,
    u_values: np.ndarray,
    retain: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    eigen_rows: list[dict[str, object]] = []
    trace_rows: list[dict[str, object]] = []
    for index, u in enumerate(u_values):
        _, full, full_prime = gaussian_markov_family(dimension, float(u), sigma)
        folded = fold_matrix(full)
        folded_prime = fold_matrix(full_prime)
        eigenvalues, conditions = conditioned_eigenvalues(folded)
        eigenvalues, conditions = without_perron(eigenvalues, conditions)
        assert conditions is not None
        ordering = np.argsort(-np.abs(eigenvalues))
        for rank, position in enumerate(ordering[:retain], start=1):
            value = eigenvalues[position]
            eigen_rows.append(
                {
                    "u": float(u),
                    "rank_by_modulus": rank,
                    "real": float(value.real),
                    "imag": float(value.imag),
                    "modulus": float(abs(value)),
                    "condition_number": float(conditions[position]),
                }
            )
        moments = centered_trace_moments(folded, (2, 3, 4, 5, 6))
        derivatives = centered_trace_derivatives(
            folded, folded_prime, (2, 3, 4, 5, 6)
        )
        row: dict[str, object] = {"u": float(u)}
        for order in moments:
            row[f"c{order}"] = float(moments[order].real)
            row[f"dc{order}_du"] = float(derivatives[order].real)
        row["largest_condition_top8"] = float(
            np.max(conditions[ordering[: min(8, len(ordering))]])
        )
        trace_rows.append(row)
        if index % 10 == 0 or index + 1 == len(u_values):
            print(f"atlas {index + 1}/{len(u_values)} u={u:.6f}", flush=True)
    return eigen_rows, trace_rows


def spectrum_snapshots(
    dimension: int,
    u: float,
    sigmas: list[float],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sigma in sigmas:
        _, full, _ = gaussian_markov_family(dimension, u, sigma)
        eigenvalues = nonperron_spectrum(fold_matrix(full))
        ordering = np.argsort(-np.abs(eigenvalues))
        for rank, position in enumerate(ordering, start=1):
            value = eigenvalues[position]
            rows.append(
                {
                    "sigma": sigma,
                    "rank_by_modulus": rank,
                    "real": float(value.real),
                    "imag": float(value.imag),
                    "modulus": float(abs(value)),
                }
            )
    return rows


def trace_convergence(
    dimensions: list[int],
    u: float,
    sigma: float,
    orders: tuple[int, ...],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    for d in dimensions:
        _, full, full_prime = gaussian_markov_family(d, u, sigma)
        folded = fold_matrix(full)
        folded_prime = fold_matrix(full_prime)
        moments = centered_trace_moments(folded, orders)
        derivatives = centered_trace_derivatives(folded, folded_prime, orders)
        row: dict[str, object] = {"d": d, "h": 2.0 / d}
        for order in orders:
            row[f"c{order}"] = float(moments[order].real)
            row[f"dc{order}_du"] = float(derivatives[order].real)
        rows.append(row)
        print(f"trace dimension {d}", flush=True)

    fit_mask = np.array(dimensions) >= 384
    x = np.array([4.0 / (d * d) for d in dimensions], dtype=float)
    metadata: dict[str, object] = {"fits": {}}
    for prefix in ("c", "dc"):
        for order in orders:
            key = f"c{order}" if prefix == "c" else f"dc{order}_du"
            values = np.array([float(row[key]) for row in rows])
            coefficients = np.polyfit(x[fit_mask], values[fit_mask], 2)
            continuum = float(coefficients[-1])
            errors = np.abs(values - continuum)
            slope_mask = (np.array(dimensions) >= 256) & (errors > 1.0e-14)
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


def dobrushin_audit(
    dimension: int,
    u: float,
    sigmas: list[float],
    steps: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    metadata: dict[str, object] = {"continuum_one_step": {}}
    for sigma in sigmas:
        _, full, _ = gaussian_markov_family(dimension, u, sigma)
        folded = fold_matrix(full)
        spectral_radius = float(np.max(np.abs(nonperron_spectrum(folded))))
        records = multistep_dobrushin_roots(
            full, steps, unique_rows=slice(dimension // 2, None)
        )
        for record in records:
            rows.append(
                {
                    "sigma": sigma,
                    "step": record["step"],
                    "delta": record["delta"],
                    "root": record["root"],
                    "nonperron_spectral_radius": spectral_radius,
                }
            )
        metadata["continuum_one_step"][str(sigma)] = exact_dobrushin_coefficient(
            u, sigma
        )
        print(f"dobrushin sigma {sigma:g}", flush=True)
    return rows, metadata


def folding_audit(dimension: int, u: float, sigma: float) -> dict[str, object]:
    _, full, _ = gaussian_markov_family(dimension, u, sigma)
    folded = fold_matrix(full)
    full_values = np.linalg.eigvals(full)
    folded_values = np.linalg.eigvals(folded)
    retained = folded_values[np.abs(folded_values) > 1.0e-4]
    matching_errors = [float(np.min(np.abs(full_values - value))) for value in retained]
    return {
        "dimension": dimension,
        "folded_dimension": dimension // 2,
        "maximum_row_reflection_error": float(
            np.max(np.abs(full[: dimension // 2] - full[: dimension // 2 - 1 : -1]))
        ),
        "significant_folded_eigenvalues": len(retained),
        "maximum_match_error_above_1e-4": max(matching_errors),
        "full_eigenvalues_below_1e-10": int(np.sum(np.abs(full_values) < 1.0e-10)),
    }


def make_atlas_figure(
    eigen_rows: list[dict[str, object]],
    trace_rows: list[dict[str, object]],
    snapshot_rows: list[dict[str, object]],
    path: Path,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8.0))
    colors = {0.03: "#3b4cc0", 0.05: "#1f968b", 0.08: "#f0a202", 0.12: "#d1495b"}
    for sigma, color in colors.items():
        selected = [row for row in snapshot_rows if float(row["sigma"]) == sigma]
        values = np.array([complex(float(row["real"]), float(row["imag"])) for row in selected])
        visible = np.abs(values) > 2.0e-4
        axes[0, 0].scatter(
            values.real[visible], values.imag[visible], s=16, alpha=0.75, color=color, label=rf"$\sigma={sigma:g}$"
        )
    angle = np.linspace(0.0, 2.0 * np.pi, 400)
    axes[0, 0].plot(np.cos(angle), np.sin(angle), color="0.65", lw=0.8, ls="--")
    axes[0, 0].axhline(0.0, color="0.8", lw=0.6)
    axes[0, 0].axvline(0.0, color="0.8", lw=0.6)
    axes[0, 0].set_aspect("equal")
    axes[0, 0].set_xlim(-1.04, 0.75)
    axes[0, 0].set_ylim(-0.78, 0.78)
    axes[0, 0].set_title(r"Non-Perron spectrum at $u_{\rm c}$")
    axes[0, 0].legend(frameon=False, fontsize=8)

    u_values = sorted({float(row["u"]) for row in eigen_rows})
    for rank, color in zip(range(1, 6), ("#222222", "#3b4cc0", "#1f968b", "#f0a202", "#d1495b"), strict=True):
        selected = [row for row in eigen_rows if int(row["rank_by_modulus"]) == rank]
        axes[0, 1].plot(
            [float(row["u"]) for row in selected],
            [float(row["modulus"]) for row in selected],
            color=color,
            label=rf"rank {rank}",
        )
    axes[0, 1].axvline(U_CRITICAL, color="0.5", ls="--", lw=0.9)
    axes[0, 1].set_ylim(0.0, 1.03)
    axes[0, 1].set_title(r"Ordered resonance moduli, $\sigma=0.05$")
    axes[0, 1].set_xlabel(r"quadratic parameter $u$")
    axes[0, 1].set_ylabel(r"$|\lambda|$")
    axes[0, 1].legend(frameon=False, fontsize=8, ncol=2)

    trace_u = np.array([float(row["u"]) for row in trace_rows])
    for order, color in zip((2, 3, 4, 5), ("#3b4cc0", "#1f968b", "#f0a202", "#d1495b"), strict=True):
        axes[1, 0].plot(trace_u, [float(row[f"c{order}"]) for row in trace_rows], color=color, label=rf"$c_{order}$")
    axes[1, 0].axvline(U_CRITICAL, color="0.5", ls="--", lw=0.9)
    axes[1, 0].set_title("Centered cycle traces remain smooth")
    axes[1, 0].set_xlabel(r"quadratic parameter $u$")
    axes[1, 0].set_ylabel(r"$c_n=\operatorname{tr}K^n-1$")
    axes[1, 0].legend(frameon=False, fontsize=8, ncol=2)

    conditions = np.array([float(row["largest_condition_top8"]) for row in trace_rows])
    axes[1, 1].semilogy(trace_u, conditions, color="#8f2d56")
    axes[1, 1].axvline(U_CRITICAL, color="0.5", ls="--", lw=0.9)
    axes[1, 1].set_title("Leading eigenvalue conditioning")
    axes[1, 1].set_xlabel(r"quadratic parameter $u$")
    axes[1, 1].set_ylabel(r"$\max_{1\leq j\leq 8}\kappa(\lambda_j)$")

    for axis in axes.flat:
        axis.grid(alpha=0.22)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


def make_trace_figure(
    rows: list[dict[str, object]],
    metadata: dict[str, object],
    path: Path,
) -> None:
    dimensions = np.array([int(row["d"]) for row in rows])
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))
    colors = ("#3b4cc0", "#1f968b", "#f0a202")
    for order, color in zip((2, 3, 4), colors, strict=True):
        key = f"c{order}"
        slope = metadata["fits"][key]["dimension_slope"]
        axes[0].loglog(dimensions, [float(row[f"error_{key}"]) for row in rows], "o-", color=color, label=rf"$c_{order}$, slope {slope:.2f}")
        dkey = f"dc{order}_du"
        dslope = metadata["fits"][dkey]["dimension_slope"]
        axes[1].loglog(dimensions, [float(row[f"error_{dkey}"]) for row in rows], "o-", color=color, label=rf"$c_{order}'$, slope {dslope:.2f}")
    guide = dimensions.astype(float) ** -2
    for axis in axes:
        y0 = axis.lines[0].get_ydata()[0]
        axis.loglog(dimensions, y0 * guide / guide[0], "--", color="0.35", label=r"$d^{-2}$ guide")
        axis.set_xlabel(r"full dimension $d$")
        axis.grid(alpha=0.25, which="both")
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("absolute extrapolation error")
    axes[0].set_title("Centered trace moments")
    axes[1].set_title("Parameter derivatives")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


def make_determinant_figure(
    dobrushin_rows: list[dict[str, object]],
    snapshot_rows: list[dict[str, object]],
    path: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    for sigma, color in ((0.05, "#3b4cc0"), (0.12, "#d1495b")):
        selected = [row for row in dobrushin_rows if float(row["sigma"]) == sigma]
        axes[0].plot(
            [int(row["step"]) for row in selected],
            [float(row["root"]) for row in selected],
            "o-",
            color=color,
            label=rf"$\delta_n^{{1/n}}$, $\sigma={sigma:g}$",
        )
        radius = float(selected[0]["nonperron_spectral_radius"])
        axes[0].axhline(radius, color=color, ls="--", lw=1.0, label=rf"$r_\perp={radius:.4f}$")
    axes[0].set_xlabel(r"step $n$")
    axes[0].set_ylabel("contraction root")
    axes[0].set_ylim(0.82, 1.005)
    axes[0].set_title("Convergent Dobrushin enclosures")
    axes[0].grid(alpha=0.25)
    axes[0].legend(frameon=False, fontsize=8)

    selected = [row for row in snapshot_rows if float(row["sigma"]) == 0.05]
    eigenvalues = np.array([complex(float(row["real"]), float(row["imag"])) for row in selected])
    real = np.linspace(-2.35, 2.35, 360)
    imag = np.linspace(-2.35, 2.35, 360)
    xx, yy = np.meshgrid(real, imag)
    zz = xx + 1j * yy
    logabs = regularized_logabs(zz, eigenvalues)
    clipped = np.clip(logabs, -5.0, 5.0)
    contour = axes[1].contourf(xx, yy, clipped, levels=40, cmap="viridis")
    reciprocal = 1.0 / eigenvalues[np.abs(eigenvalues) > 0.10]
    axes[1].scatter(reciprocal.real, reciprocal.imag, marker="x", s=35, color="white", linewidth=1.0, label=r"$1/\lambda_j$")
    axes[1].axhline(0.0, color="white", alpha=0.35, lw=0.6)
    axes[1].axvline(0.0, color="white", alpha=0.35, lw=0.6)
    axes[1].set_aspect("equal")
    axes[1].set_xlim(real[0], real[-1])
    axes[1].set_ylim(imag[0], imag[-1])
    axes[1].set_title(r"$\log|\det_2(I-zN)|$, $\sigma=0.05$")
    axes[1].set_xlabel(r"$\Re z$")
    axes[1].set_ylabel(r"$\Im z$")
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")
    fig.colorbar(contour, ax=axes[1], shrink=0.84, pad=0.03)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas-dimension", type=int, default=512)
    parser.add_argument("--snapshot-dimension", type=int, default=768)
    parser.add_argument("--dobrushin-dimension", type=int, default=512)
    parser.add_argument("--atlas-points", type=int, default=81)
    parser.add_argument("--dobrushin-steps", type=int, default=30)
    parser.add_argument("--sigma", type=float, default=0.05)
    parser.add_argument("--u", type=float, default=U_CRITICAL)
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--figures", type=Path, default=Path("figures"))
    args = parser.parse_args()

    u_values = np.linspace(1.35, 1.75, args.atlas_points)
    snapshot_sigmas = [0.03, 0.05, 0.08, 0.12]
    trace_dimensions = [128, 192, 256, 384, 512, 768, 1024, 1536, 2048]
    orders = (2, 3, 4, 5, 6)

    atlas_rows, response_rows = atlas_scan(
        args.atlas_dimension, args.sigma, u_values, retain=12
    )
    snapshots = spectrum_snapshots(
        args.snapshot_dimension, args.u, snapshot_sigmas
    )
    trace_rows, trace_metadata = trace_convergence(
        trace_dimensions, args.u, args.sigma, orders
    )
    dobrushin_rows, dobrushin_metadata = dobrushin_audit(
        args.dobrushin_dimension,
        args.u,
        [0.05, 0.12],
        args.dobrushin_steps,
    )
    folding = folding_audit(192, args.u, 0.12)

    write_csv(args.results / "resonance_atlas.csv", atlas_rows)
    write_csv(args.results / "centered_trace_response.csv", response_rows)
    write_csv(args.results / "spectrum_snapshots.csv", snapshots)
    write_csv(args.results / "trace_convergence.csv", trace_rows)
    write_csv(args.results / "dobrushin_enclosures.csv", dobrushin_rows)

    metadata = {
        "parameters": {
            "u_critical": args.u,
            "atlas_sigma": args.sigma,
            "atlas_dimension": args.atlas_dimension,
            "snapshot_dimension": args.snapshot_dimension,
            "dobrushin_dimension": args.dobrushin_dimension,
            "atlas_points": args.atlas_points,
            "trace_dimensions": trace_dimensions,
            "target_data_loaded": False,
        },
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "folding_audit": folding,
        "trace_convergence": trace_metadata,
        "dobrushin": dobrushin_metadata,
    }
    args.results.mkdir(parents=True, exist_ok=True)
    with (args.results / "intrinsic_spectrum_summary.json").open("w") as handle:
        json.dump(metadata, handle, indent=2)

    make_atlas_figure(
        atlas_rows,
        response_rows,
        snapshots,
        args.figures / "resonance_atlas.pdf",
    )
    make_trace_figure(
        trace_rows,
        trace_metadata,
        args.figures / "trace_convergence.pdf",
    )
    make_determinant_figure(
        dobrushin_rows,
        snapshots,
        args.figures / "dobrushin_determinant.pdf",
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
