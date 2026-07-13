"""Generate the weighted-zeta and physical flat-trace completion audit."""

from __future__ import annotations

import csv
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy

from flat_trace_completion import (
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    audit_length,
    centered_component_zeta_series,
    component_critical_value_derivative,
    critical_value_derivative,
    critical_zero_deflated_coefficients,
    smallest_positive_real_root,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
MAXIMUM_LENGTH = 28
MAXIMUM_TWO_STEP_LENGTH = MAXIMUM_LENGTH // 2


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def trace_audit() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for length in range(1, MAXIMUM_LENGTH + 1):
        print(f"periodic trace {length}/{MAXIMUM_LENGTH}", flush=True)
        record = audit_length(length)
        rows.append(
            {
                "length": length,
                "parity": "even" if length % 2 == 0 else "odd",
                "fixed_point_count": record.fixed_point_count,
                "flat_trace": record.flat_trace,
                "weighted_trace": record.weighted_trace,
                "flat_minus_weighted": record.flat_minus_weighted,
                "parity_centered_flat": record.parity_centered_flat,
                "parity_centered_weighted": record.parity_centered_weighted,
                "central_component_weighted": ""
                if record.central_weighted is None
                else record.central_weighted,
                "high_component_weighted": ""
                if record.high_weighted is None
                else record.high_weighted,
                "component_difference": ""
                if record.component_difference is None
                else record.component_difference,
                "component_reconstruction_error": ""
                if record.component_reconstruction_error is None
                else record.component_reconstruction_error,
                "minimum_abs_multiplier": record.minimum_multiplier,
                "elementary_comparison_bound": record.elementary_comparison_bound,
            }
        )
    write_csv(RESULTS / "flat_weighted_trace_comparison.csv", rows)
    return rows


def zeta_audit(trace_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    even = [row for row in trace_rows if int(row["length"]) % 2 == 0]
    component = np.asarray([float(row["central_component_weighted"]) for row in even])
    deflated = critical_zero_deflated_coefficients(component)
    coefficient_rows: list[dict[str, object]] = []
    for index, (row, value, remainder) in enumerate(zip(even, component, deflated), start=1):
        length = int(row["length"])
        coefficient_rows.append(
            {
                "two_step_length": index,
                "original_length": length,
                "component_weighted_trace": value,
                "component_centered": value - 1.0,
                "component_centered_times_lambda_power": (value - 1.0)
                * LAMBDA_FIXED**index,
                "lambda_inverse_power": LAMBDA_FIXED ** (-index),
                "critical_zero_deflated": remainder,
                "deflated_times_lambda_squared_power": remainder * LAMBDA_FIXED ** (2 * index),
            }
        )
    write_csv(RESULTS / "component_weighted_zeta_coefficients.csv", coefficient_rows)

    root_rows: list[dict[str, object]] = []
    for degree in range(3, MAXIMUM_TWO_STEP_LENGTH + 1):
        series = centered_component_zeta_series(component[:degree])
        root = smallest_positive_real_root(series)
        root_rows.append(
            {
                "truncation_degree": degree,
                "smallest_positive_real_root": root,
                "lambda_fixed": LAMBDA_FIXED,
                "root_minus_lambda": root - LAMBDA_FIXED,
                "absolute_error": abs(root - LAMBDA_FIXED),
            }
        )
    write_csv(RESULTS / "centered_zeta_roots.csv", root_rows)
    return coefficient_rows, root_rows


def tail_slope(rows: list[dict[str, object]], field: str, minimum_length: int = 14) -> float:
    selected = [row for row in rows if int(row["length"]) >= minimum_length and int(row["length"]) % 2 == 0]
    length = np.asarray([float(row["length"]) for row in selected])
    values = np.asarray([abs(float(row[field])) for row in selected])
    return float(np.polyfit(length, np.log(values), 1)[0])


def plot_completion(rows: list[dict[str, object]]) -> None:
    length = np.asarray([int(row["length"]) for row in rows])
    even = length % 2 == 0
    even_rows = [row for row in rows if int(row["length"]) % 2 == 0]
    even_length = length[even]

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.2))
    n = np.arange(1, 11)
    axes[0, 0].semilogy(n, [critical_value_derivative(int(k)) for k in n], "o-", color="#2455a4", label=r"$|(f^n)'(1)|$")
    axes[0, 0].semilogy(n, [component_critical_value_derivative("central", int(k)) for k in n], "s-", color="#a0273f", label=r"$|(T^n)'(-r)|$")
    axes[0, 0].set(xlabel=r"iterate $n$", ylabel="critical-value derivative", title="Exact Collet--Eckmann growth")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].plot(even_length, [float(row["flat_trace"]) for row in even_rows], "o-", ms=3.5, color="#2455a4", label=r"physical $P_m$")
    axes[0, 1].plot(even_length, [float(row["weighted_trace"]) for row in even_rows], "s--", ms=3.2, color="#a0273f", label=r"Perron weight $Q_m$")
    axes[0, 1].axhline(2.0, color="black", lw=0.9, ls=":")
    axes[0, 1].set(xlabel=r"even length $m$", ylabel="periodic trace", title="Common unconditional parity limit")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    difference = np.asarray([abs(float(row["flat_minus_weighted"])) for row in even_rows])
    bound = np.asarray([float(row["elementary_comparison_bound"]) for row in even_rows])
    axes[1, 0].semilogy(even_length, difference, "o-", ms=3.5, color="#3a8f6b", label=r"$|P_m-Q_m|$")
    axes[1, 0].semilogy(even_length, bound, "--", color="#cf7b28", lw=1.1, label="elementary bound")
    anchor = difference[4]
    reference = anchor * np.exp(-1.5 * np.log(LAMBDA_FIXED) * (even_length - even_length[4]))
    axes[1, 0].semilogy(even_length, reference, ":", color="black", lw=1.1, label=r"reference $\lambda^{-3m/2}$")
    axes[1, 0].set(xlabel=r"even length $m$", ylabel="absolute difference", title="Physical versus standard weight")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    minimum = np.asarray([float(row["minimum_abs_multiplier"]) for row in even_rows])
    axes[1, 1].semilogy(even_length, minimum, "o-", ms=3.5, color="#7049a8", label="minimum periodic multiplier")
    reference = minimum[-1] * np.exp(0.5 * np.log(LAMBDA_FIXED) * (even_length - even_length[-1]))
    axes[1, 1].semilogy(even_length, reference, "--", color="black", lw=1.1, label=r"reference $\lambda^{m/2}$")
    axes[1, 1].set(xlabel=r"even length $m$", ylabel="minimum multiplier", title="Uniform periodic expansion audit")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"flat_trace_completion.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_zeta(
    coefficient_rows: list[dict[str, object]], root_rows: list[dict[str, object]]
) -> None:
    n = np.asarray([int(row["two_step_length"]) for row in coefficient_rows])
    component = np.asarray([float(row["component_weighted_trace"]) for row in coefficient_rows])
    roots = np.asarray([float(row["smallest_positive_real_root"]) for row in root_rows])
    degrees = np.asarray([int(row["truncation_degree"]) for row in root_rows])

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.55))
    axes[0].plot(n, (component - 1.0) * LAMBDA_FIXED**n, "o-", color="#2455a4", ms=4)
    axes[0].axhline(-1.0, color="black", ls="--", lw=1.0)
    axes[0].set(xlabel=r"two-step length $n$", ylabel=r"$(q_n-1)\lambda^n$", title="Leading centered coefficient")
    axes[0].grid(alpha=0.22)

    axes[1].semilogy(degrees, np.abs(roots - LAMBDA_FIXED), "o-", color="#a0273f", ms=4)
    axes[1].set(xlabel="zeta truncation degree", ylabel=r"$|z_N-\lambda|$", title="First centered-zeta zero")
    axes[1].grid(alpha=0.22)

    z = np.linspace(0.0, 2.05, 700)
    for degree, color in zip((6, 8, 10, 12, 14), plt.cm.viridis(np.linspace(0.12, 0.9, 5))):
        series = centered_component_zeta_series(component[:degree])
        values = np.polynomial.polynomial.polyval(z, series.real)
        axes[2].plot(z, values, color=color, lw=1.0, label=fr"$N={degree}$")
    axes[2].axhline(0.0, color="black", lw=0.8)
    axes[2].axvline(LAMBDA_FIXED, color="#a0273f", lw=1.1, ls="--", label=r"$\lambda$")
    axes[2].set(xlim=(1.35, 2.02), ylim=(-0.22, 0.25), xlabel=r"real $z$", ylabel=r"truncated $(1-z)Z(z)$", title="Zero stabilization")
    axes[2].legend(frameon=False, fontsize=7, ncol=2)
    axes[2].grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"centered_weighted_zeta.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_summary(
    trace_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    root_rows: list[dict[str, object]],
) -> dict[str, object]:
    even = [row for row in trace_rows if int(row["length"]) % 2 == 0]
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "constants": {
            "u_critical": U_CRITICAL,
            "r_fixed": R_FIXED,
            "lambda_fixed": LAMBDA_FIXED,
        },
        "theorem_completion": {
            "collet_eckmann_f": "abs((f^n)'(f(c))) = 2*u_c*lambda^(n-1)",
            "central_component_ce": "abs((T^n)'(T(c_C))) = lambda^(2n)",
            "high_component_ce": "abs((T^n)'(T(c_H))) = 2*u_c*lambda^(2n-1)",
            "weighted_parity_trace": "Q_m = 1+(-1)^m+O(theta^m)",
            "flat_weight_comparison": "P_m-Q_m = O(theta_1^m)",
            "unconditional_flat_trace": "P_m = 1+(-1)^m+O(theta_2^m)",
        },
        "numerical_audit": {
            "maximum_length": MAXIMUM_LENGTH,
            "physical_roots_at_maximum_length": int(trace_rows[-1]["fixed_point_count"]),
            "flat_trace_at_maximum_length": float(trace_rows[-1]["flat_trace"]),
            "weighted_trace_at_maximum_length": float(trace_rows[-1]["weighted_trace"]),
            "maximum_component_pairing_error": max(abs(float(row["component_difference"])) for row in even),
            "maximum_component_reconstruction_error": max(abs(float(row["component_reconstruction_error"])) for row in even),
            "flat_centered_tail_slope": tail_slope(trace_rows, "parity_centered_flat"),
            "weighted_centered_tail_slope": tail_slope(trace_rows, "parity_centered_weighted"),
            "flat_minus_weighted_tail_slope": tail_slope(trace_rows, "flat_minus_weighted"),
            "reference_half_log_lambda": -0.5 * float(np.log(LAMBDA_FIXED)),
            "reference_three_half_log_lambda": -1.5 * float(np.log(LAMBDA_FIXED)),
            "last_component_scaled_centered": float(coefficient_rows[-1]["component_centered_times_lambda_power"]),
            "last_zeta_root": float(root_rows[-1]["smallest_positive_real_root"]),
            "last_zeta_root_error": float(root_rows[-1]["absolute_error"]),
        },
        "scope": {
            "exponential_flat_trace_gap": "unconditional theorem via published Collet-Eckmann weighted-zeta and uniform-hyperbolicity results",
            "sharp_lambda_rate": "numerical evidence only",
            "centered_zeta_zero_at_lambda": "numerical conjecture only",
        },
    }
    with (RESULTS / "flat_trace_completion_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return summary


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    trace_rows = trace_audit()
    coefficient_rows, root_rows = zeta_audit(trace_rows)
    plot_completion(trace_rows)
    plot_zeta(coefficient_rows, root_rows)
    summary = write_summary(trace_rows, coefficient_rows, root_rows)
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
