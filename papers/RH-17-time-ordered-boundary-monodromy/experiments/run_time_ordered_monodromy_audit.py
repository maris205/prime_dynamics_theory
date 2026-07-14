"""Generate multiplier, cycle-determinant, conditioning, and cloud audits."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath
import numpy as np

from time_ordered_monodromy import (
    balancing_condition_number,
    balancing_diagonal,
    boundary_cycle,
    critical_constants,
    eigenvalue_condition_number,
    ideal_reciprocal_cloud,
    inverse_jacobian_weights,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
sys.path.insert(0, str(RH16 / "src"))

from endpoint_rank import (  # noqa: E402
    HALF_ENERGY_THRESHOLD,
    boundary_clearances,
    threshold_rank,
)


DECIMAL_DIGITS = 130
MAX_PERIOD = 100
ORBIT_PERIOD = 8


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def multiplier_rows() -> list[dict[str, object]]:
    constants = critical_constants(DECIMAL_DIGITS)
    with mpmath.workdps(DECIMAL_DIGITS):
        limiting_two_step = +(1 / constants.lambda_fixed)
        limiting_one_step = +constants.lambda_fixed ** (-mpmath.mpf("0.5"))
    rows: list[dict[str, object]] = []
    for period in range(1, MAX_PERIOD + 1):
        cycle = boundary_cycle(period, DECIMAL_DIGITS)
        condition = balancing_condition_number(cycle)
        rows.append(
            {
                "component_period": period,
                "original_period": 2 * period,
                "boundary_clearance": mpmath.nstr(cycle.clearance, 20),
                "multiplier": mpmath.nstr(cycle.multiplier, 20),
                "absolute_multiplier_over_lambda_k": mpmath.nstr(
                    cycle.scaled_multiplier, 20
                ),
                "two_step_inverse_jacobian_radius": mpmath.nstr(
                    cycle.inverse_jacobian_radius, 20
                ),
                "one_step_cycle_radius": mpmath.nstr(cycle.one_step_radius, 20),
                "limiting_two_step_radius": mpmath.nstr(
                    limiting_two_step, 20
                ),
                "limiting_one_step_radius": mpmath.nstr(
                    limiting_one_step, 20
                ),
                "balancing_condition_number": condition,
                "condition_over_lambda_k": condition
                / float(constants.lambda_fixed**period),
                "eigenvalue_condition_number": eigenvalue_condition_number(cycle),
            }
        )
    write_csv(RESULTS / "boundary_cycle_monodromy.csv", rows)
    return rows


def orbit_rows() -> list[dict[str, object]]:
    constants = critical_constants(DECIMAL_DIGITS)
    cycle = boundary_cycle(ORBIT_PERIOD, DECIMAL_DIGITS)
    weights = inverse_jacobian_weights(cycle)
    diagonal = balancing_diagonal(cycle)
    rows: list[dict[str, object]] = []
    for index, (point, derivative, weight, balance) in enumerate(
        zip(cycle.orbit, cycle.two_step_derivatives, weights, diagonal)
    ):
        rows.append(
            {
                "component_period": ORBIT_PERIOD,
                "time_index": index,
                "point": mpmath.nstr(point, 20),
                "distance_from_repelling_boundary": mpmath.nstr(
                    point - constants.r, 20
                ),
                "two_step_derivative": mpmath.nstr(derivative, 20),
                "inverse_jacobian_weight": weight,
                "balancing_diagonal": balance,
                "next_time_index": (index + 1) % ORBIT_PERIOD,
            }
        )
    write_csv(RESULTS / "time_ordered_orbit.csv", rows)
    return rows


def _row_degree(clearances: np.ndarray, sigma: float, *, power: float) -> int:
    return threshold_rank(
        clearances,
        sigma,
        threshold=HALF_ENERGY_THRESHOLD,
        power=power,
    )


def cloud_comparison_rows() -> list[dict[str, object]]:
    constants = critical_constants(DECIMAL_DIGITS)
    with mpmath.workdps(DECIMAL_DIGITS):
        limiting_radius = float(
            constants.lambda_fixed ** (-mpmath.mpf("0.5"))
        )
    clearances = boundary_clearances(70, decimal_digits=110)
    rows: list[dict[str, object]] = []
    for archived in read_csv(RH15 / "results" / "cloud_summary.csv"):
        sigma = float(archived["sigma"])
        hellinger_degree = _row_degree(clearances, sigma, power=0.5)
        linear_degree = _row_degree(clearances, sigma, power=1.0)
        cloud_degree = int(float(archived["effective_cloud_degree"]))
        hellinger_cycle = boundary_cycle(hellinger_degree + 1, DECIMAL_DIGITS)
        linear_cycle = boundary_cycle(linear_degree + 1, DECIMAL_DIGITS)
        cloud_cycle = boundary_cycle(cloud_degree + 1, DECIMAL_DIGITS)
        hellinger_radius = float(hellinger_cycle.one_step_radius)
        linear_radius = float(linear_cycle.one_step_radius)
        cloud_cycle_radius = float(cloud_cycle.one_step_radius)
        observed_radius = float(archived["cloud_radial_mean"])
        limiting_error = abs(observed_radius - limiting_radius)
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": int(float(archived["folded_dimension"])),
                "independent_hellinger_degree": hellinger_degree,
                "independent_linear_row_degree": linear_degree,
                "archived_cloud_degree": cloud_degree,
                "observed_cloud_radius": observed_radius,
                "hellinger_cycle_radius": hellinger_radius,
                "linear_cycle_radius": linear_radius,
                "cloud_degree_cycle_radius": cloud_cycle_radius,
                "limiting_radius": limiting_radius,
                "hellinger_cycle_absolute_error": abs(
                    observed_radius - hellinger_radius
                ),
                "linear_cycle_absolute_error": abs(observed_radius - linear_radius),
                "cloud_degree_cycle_absolute_error": abs(
                    observed_radius - cloud_cycle_radius
                ),
                "limiting_absolute_error": limiting_error,
                "hellinger_to_limiting_error_ratio": abs(
                    observed_radius - hellinger_radius
                )
                / limiting_error,
                "linear_to_limiting_error_ratio": abs(
                    observed_radius - linear_radius
                )
                / limiting_error,
                "archived_phase_rms": float(archived["cloud_phase_rms_error"]),
            }
        )
    write_csv(RESULTS / "cloud_cycle_comparison.csv", rows)
    return rows


def selected_archived_cloud(sigma: float) -> np.ndarray:
    values: list[complex] = []
    for row in read_csv(RH15 / "results" / "outer_resonance_cloud.csv"):
        if abs(float(row["sigma"]) - sigma) > 1.0e-15:
            continue
        if not row["expected_radius"]:
            continue
        value = complex(float(row["real"]), float(row["imag"]))
        values.extend((value, np.conjugate(value)))
    return np.asarray(values, dtype=np.complex128)


def plot_main_audit(
    multiplier: list[dict[str, object]],
    orbit: list[dict[str, object]],
    cloud: list[dict[str, object]],
) -> None:
    constants = critical_constants(DECIMAL_DIGITS)
    periods = np.asarray([int(row["component_period"]) for row in multiplier])
    scaled = np.asarray(
        [float(row["absolute_multiplier_over_lambda_k"]) for row in multiplier]
    )
    condition = np.asarray(
        [float(row["balancing_condition_number"]) for row in multiplier]
    )
    eigen_condition = np.asarray(
        [float(row["eigenvalue_condition_number"]) for row in multiplier]
    )
    lambda_values = float(constants.lambda_fixed) ** periods

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].plot(periods, scaled, "o-", ms=2.7, color="#2455a4")
    axes[0, 0].axhline(
        scaled[-1],
        color="#a0273f",
        ls="--",
        label=rf"$C_M\approx {scaled[-1]:.10f}$",
    )
    axes[0, 0].set(
        xlabel=r"component period $k$",
        ylabel=r"$|M_k|/\lambda^k$",
        title="Critical-return multiplier law",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].semilogy(periods, condition, color="#2455a4", label=r"$\kappa(D_k)$")
    axes[0, 1].semilogy(
        periods,
        eigen_condition,
        color="#a0273f",
        label="eigenvalue condition",
    )
    axes[0, 1].semilogy(
        periods,
        0.405 * lambda_values,
        "--",
        color="0.25",
        label=r"$0.405\,\lambda^k$",
    )
    axes[0, 1].set(
        xlabel=r"component period $k$",
        ylabel="Euclidean condition number",
        title="Balancing is not uniformly conditioned",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    sigma = np.asarray([float(row["sigma"]) for row in cloud])
    observed = np.asarray([float(row["observed_cloud_radius"]) for row in cloud])
    hellinger = np.asarray(
        [float(row["hellinger_cycle_radius"]) for row in cloud]
    )
    linear = np.asarray([float(row["linear_cycle_radius"]) for row in cloud])
    limiting = float(cloud[0]["limiting_radius"])
    order = np.argsort(sigma)[::-1]
    axes[1, 0].semilogx(
        sigma[order], observed[order], "o-", color="#2455a4", label="archived cloud"
    )
    axes[1, 0].semilogx(
        sigma[order],
        hellinger[order],
        "s--",
        color="#a0273f",
        label="Hellinger-rank cycle",
    )
    axes[1, 0].semilogx(
        sigma[order],
        linear[order],
        "^:",
        color="#25865f",
        label=r"linear-$L^2$-rank cycle",
    )
    axes[1, 0].axhline(
        limiting,
        color="0.25",
        ls=":",
        label=r"$\lambda^{-1/2}$",
    )
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="one-step radius",
        title="Two intrinsic finite-radius corrections",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    time = np.asarray([int(row["time_index"]) for row in orbit])
    distance = np.asarray(
        [float(row["distance_from_repelling_boundary"]) for row in orbit]
    )
    axes[1, 1].semilogy(time, distance, "o-", color="#2455a4")
    for index in range(time.size - 1):
        axes[1, 1].annotate(
            "",
            xy=(time[index + 1], distance[index + 1]),
            xytext=(time[index], distance[index]),
            arrowprops={"arrowstyle": "->", "color": "0.35", "lw": 0.7},
        )
    axes[1, 1].set(
        xlabel=r"two-step time $j$",
        ylabel=r"$x_{k,j}-r$",
        title=rf"Exact ordered return chain ($k={ORBIT_PERIOD}$)",
    )
    axes[1, 1].grid(alpha=0.22)

    fig.tight_layout()
    fig.savefig(FIGURES / "time_ordered_boundary_monodromy.pdf")
    fig.savefig(FIGURES / "time_ordered_boundary_monodromy.png", dpi=220)
    plt.close(fig)


def plot_cloud_overlay(cloud_rows: list[dict[str, object]]) -> None:
    row = min(cloud_rows, key=lambda value: float(value["sigma"]))
    sigma = float(row["sigma"])
    hellinger_degree = int(row["independent_hellinger_degree"])
    linear_degree = int(row["independent_linear_row_degree"])
    if hellinger_degree != linear_degree:
        raise RuntimeError("the two intrinsic degrees differ at the selected noise")
    degree = hellinger_degree
    cycle = boundary_cycle(degree + 1, DECIMAL_DIGITS)
    finite = ideal_reciprocal_cloud(cycle)
    observed = selected_archived_cloud(sigma)
    angles = np.arange(1, degree + 1) * np.pi / (degree + 1)
    limiting_radius = float(row["limiting_radius"])
    limiting_positive = limiting_radius * np.exp(1j * angles)
    limiting = np.concatenate((limiting_positive, np.conjugate(limiting_positive)))

    fig, axis = plt.subplots(figsize=(6.4, 6.0))
    theta = np.linspace(0.0, 2.0 * np.pi, 500)
    axis.plot(
        limiting_radius * np.cos(theta),
        limiting_radius * np.sin(theta),
        ":",
        color="0.55",
        label=r"limit $|\mu|=\lambda^{-1/2}$",
    )
    axis.scatter(
        observed.real,
        observed.imag,
        s=42,
        facecolors="none",
        edgecolors="#2455a4",
        label="archived noisy cloud",
    )
    axis.scatter(
        finite.real,
        finite.imag,
        marker="x",
        s=48,
        color="#a0273f",
        label="finite boundary cycle",
    )
    axis.scatter(
        limiting.real,
        limiting.imag,
        marker="+",
        s=36,
        color="0.35",
        label="limiting geometric grid",
    )
    axis.axhline(0.0, color="0.82", lw=0.7)
    axis.axvline(0.0, color="0.82", lw=0.7)
    axis.set_aspect("equal")
    axis.set(
        xlabel=r"$\operatorname{Re}\mu$",
        ylabel=r"$\operatorname{Im}\mu$",
        title=rf"Intrinsic $N={degree}$ cycle model at $\sigma={sigma:g}$",
    )
    axis.legend(frameon=False, fontsize=8, loc="lower left")
    axis.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(FIGURES / "finite_cycle_cloud_overlay.pdf")
    fig.savefig(FIGURES / "finite_cycle_cloud_overlay.png", dpi=220)
    plt.close(fig)


def write_summary(
    multiplier: list[dict[str, object]], cloud: list[dict[str, object]]
) -> None:
    hellinger_errors = np.asarray(
        [float(row["hellinger_cycle_absolute_error"]) for row in cloud]
    )
    linear_errors = np.asarray(
        [float(row["linear_cycle_absolute_error"]) for row in cloud]
    )
    conditional_errors = np.asarray(
        [float(row["cloud_degree_cycle_absolute_error"]) for row in cloud]
    )
    limiting_errors = np.asarray(
        [float(row["limiting_absolute_error"]) for row in cloud]
    )
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "mpmath": mpmath.__version__,
        "decimal_digits": DECIMAL_DIGITS,
        "maximum_component_period": MAX_PERIOD,
        "multiplier_constant_estimate": float(
            multiplier[-1]["absolute_multiplier_over_lambda_k"]
        ),
        "balancing_constant_estimate": float(
            multiplier[-1]["condition_over_lambda_k"]
        ),
        "hellinger_rank_match_count": sum(
            int(row["independent_hellinger_degree"])
            == int(row["archived_cloud_degree"])
            for row in cloud
        ),
        "linear_rank_match_count": sum(
            int(row["independent_linear_row_degree"])
            == int(row["archived_cloud_degree"])
            for row in cloud
        ),
        "noise_level_count": len(cloud),
        "hellinger_cycle_radius_rms_error": float(
            np.sqrt(np.mean(hellinger_errors**2))
        ),
        "linear_cycle_radius_rms_error": float(np.sqrt(np.mean(linear_errors**2))),
        "cloud_degree_cycle_radius_rms_error": float(
            np.sqrt(np.mean(conditional_errors**2))
        ),
        "limiting_radius_rms_error": float(
            np.sqrt(np.mean(limiting_errors**2))
        ),
        "hellinger_rms_error_ratio": float(
            np.sqrt(np.mean(hellinger_errors**2) / np.mean(limiting_errors**2))
        ),
        "linear_rms_error_ratio": float(
            np.sqrt(np.mean(linear_errors**2) / np.mean(limiting_errors**2))
        ),
        "cloud_degree_rms_error_ratio": float(
            np.sqrt(np.mean(conditional_errors**2) / np.mean(limiting_errors**2))
        ),
        "source_hashes": {
            "dynamics.py": source_hash(
                ROOT / "src" / "time_ordered_monodromy" / "dynamics.py"
            ),
            "monodromy.py": source_hash(
                ROOT / "src" / "time_ordered_monodromy" / "monodromy.py"
            ),
            "audit.py": source_hash(Path(__file__)),
            "rh15_cloud_summary.csv": source_hash(
                RH15 / "results" / "cloud_summary.csv"
            ),
            "rh16_hellinger.py": source_hash(
                RH16 / "src" / "endpoint_rank" / "hellinger.py"
            ),
        },
    }
    with (RESULTS / "time_ordered_monodromy_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    multiplier = multiplier_rows()
    orbit = orbit_rows()
    cloud = cloud_comparison_rows()
    plot_main_audit(multiplier, orbit, cloud)
    plot_cloud_overlay(cloud)
    write_summary(multiplier, cloud)
    print(
        "generated boundary monodromy, ordered orbit, cloud comparison, "
        "two figures, and summary",
        flush=True,
    )


if __name__ == "__main__":
    main()
