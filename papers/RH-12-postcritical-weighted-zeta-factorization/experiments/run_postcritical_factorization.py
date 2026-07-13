"""Generate the exhaustive RH-12 postcritical-factorization audit."""

from __future__ import annotations

import csv
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
import scipy

from postcritical_zeta import (
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    centered_zeta_series,
    component_weighted_trace,
    component_weighted_trace_mp,
    flat_determinant_series,
    lift_derivative,
    lift_trace_audit,
    multiprecision_constants,
    partial_log_g,
    postcritical_model,
    smallest_positive_real_root,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
MAXIMUM_COMPONENT_LENGTH = 20
MAXIMUM_LIFT_LENGTH = 10
MAXIMUM_MULTIPRECISION_LENGTH = 6


def long_double_string(value: np.longdouble, precision: int = 20) -> str:
    """Serialize without NumPy's ``__format__`` float64 down-cast."""

    return np.format_float_scientific(
        np.longdouble(value),
        precision=precision,
        unique=False,
        trim="k",
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def component_trace_audit() -> tuple[np.ndarray, list[dict[str, object]]]:
    traces: list[np.longdouble] = []
    rows: list[dict[str, object]] = []
    previous_remainder: np.longdouble | None = None
    lam = np.longdouble(LAMBDA_FIXED)
    for length in range(1, MAXIMUM_COMPONENT_LENGTH + 1):
        print(
            f"component trace {length}/{MAXIMUM_COMPONENT_LENGTH}",
            flush=True,
        )
        audit = component_weighted_trace(length)
        trace = audit.weighted_trace
        model = np.longdouble(postcritical_model(length))
        remainder = trace - model
        ratio = ""
        if previous_remainder is not None:
            ratio = float(remainder / previous_remainder)
        rows.append(
            {
                "two_step_length": length,
                "fixed_point_count": audit.fixed_point_count,
                "component_weighted_trace": long_double_string(trace),
                "perron_postcritical_model": long_double_string(model),
                "postcritical_remainder": long_double_string(remainder),
                "successive_remainder_ratio": ratio,
                "remainder_nth_root": float(abs(remainder) ** (1 / length)),
                "remainder_times_lambda_cubed_power": float(
                    remainder * lam ** (3 * length)
                ),
                "maximum_inverse_residual": long_double_string(
                    audit.maximum_inverse_residual, 6
                ),
                "maximum_iterations": audit.maximum_iterations,
            }
        )
        traces.append(trace)
        previous_remainder = remainder
    write_csv(RESULTS / "component_postcritical_traces.csv", rows)
    return np.asarray(traces, dtype=np.longdouble), rows


def lift_factorization_audit(
    traces: np.ndarray,
) -> tuple[list[dict[str, object]], np.ndarray, np.ndarray]:
    rows: list[dict[str, object]] = []
    even_one: list[float] = []
    odd_two: list[float] = []
    lam = float(LAMBDA_FIXED)
    for length in range(1, MAXIMUM_LIFT_LENGTH + 1):
        print(f"circle-lift trace {length}/{MAXIMUM_LIFT_LENGTH}", flush=True)
        audit = lift_trace_audit(length)
        direct = float(traces[length - 1])
        error = audit.reconstructed_component_trace - direct
        rows.append(
            {
                "two_step_length": length,
                "fixed_F_count": audit.fixed_count,
                "expected_fixed_F_count": 2**length - 1,
                "fixed_iota_F_count": audit.twisted_fixed_count,
                "expected_fixed_iota_F_count": 2**length + 1,
                "even_beta_one_flat_trace": audit.even_beta_one_trace,
                "odd_beta_two_flat_trace": audit.odd_beta_two_trace,
                "orbifold_branch_weight": lam ** (-length),
                "interval_endpoint_weight": lam ** (-2 * length),
                "reconstructed_component_trace": audit.reconstructed_component_trace,
                "direct_component_trace": direct,
                "reconstruction_error": error,
            }
        )
        even_one.append(audit.even_beta_one_trace)
        odd_two.append(audit.odd_beta_two_trace)
    write_csv(RESULTS / "circle_lift_trace_factorization.csv", rows)
    return rows, np.asarray(even_one), np.asarray(odd_two)


def multiprecision_audit(traces: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    constants = multiprecision_constants(80)
    for length in range(1, MAXIMUM_MULTIPRECISION_LENGTH + 1):
        print(
            f"multiprecision trace {length}/{MAXIMUM_MULTIPRECISION_LENGTH}",
            flush=True,
        )
        value = component_weighted_trace_mp(length, decimal_places=80)
        long_double = traces[length - 1]
        difference = value - mp.mpf(str(long_double))
        rows.append(
            {
                "two_step_length": length,
                "long_double_trace": long_double_string(long_double),
                "multiprecision_trace": mp.nstr(value, 45),
                "long_double_minus_multiprecision": mp.nstr(-difference, 12),
            }
        )
    write_csv(RESULTS / "multiprecision_trace_check.csv", rows)
    with (RESULTS / "multiprecision_constants.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(
            {
                "decimal_places": 80,
                "u_critical": mp.nstr(constants.u, 80),
                "r_fixed": mp.nstr(constants.r, 80),
                "lambda_fixed": mp.nstr(constants.lam, 80),
            },
            handle,
            indent=2,
        )
        handle.write("\n")
    return rows


def load_multiprecision_tail() -> dict[
    int, tuple[np.longdouble, np.longdouble]
]:
    path = RESULTS / "multiprecision_postcritical_tail.csv"
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {
        int(row["two_step_length"]): (
            np.longdouble(row["multiprecision_trace"]),
            np.longdouble(row["postcritical_remainder"]),
        )
        for row in rows
    }


def zeta_audit(traces: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    lam = np.longdouble(LAMBDA_FIXED)
    remainder = traces - postcritical_model(
        np.arange(1, traces.size + 1, dtype=np.int64)
    )
    for degree in range(3, traces.size + 1):
        coefficients = centered_zeta_series(traces[:degree])
        root = smallest_positive_real_root(coefficients)
        log_g = partial_log_g(traces[:degree], lam)
        last_term = remainder[degree - 1] * lam**degree / degree
        rows.append(
            {
                "truncation_degree": degree,
                "centered_zeta_positive_root": root,
                "lambda_fixed": float(lam),
                "root_minus_lambda": root - float(lam),
                "absolute_root_error": abs(root - float(lam)),
                "partial_log_G_at_lambda": long_double_string(log_g),
                "partial_G_at_lambda": float(np.exp(log_g)),
                "last_log_G_term_at_lambda": long_double_string(last_term, 12),
            }
        )
    write_csv(RESULTS / "zeta_deflation_convergence.csv", rows)
    return rows


def fredholm_audit(
    even_one: np.ndarray,
    odd_two: np.ndarray,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for degree in range(3, even_one.size + 1):
        reduced_perron = flat_determinant_series(even_one[:degree] - 1.0)
        odd_second = flat_determinant_series(odd_two[:degree])
        perron_zero = smallest_positive_real_root(reduced_perron)
        second_zero = smallest_positive_real_root(odd_second)
        rows.append(
            {
                "truncation_degree": degree,
                "reduced_even_beta_one_first_zero": perron_zero,
                "inferred_even_beta_one_resonance": 1.0 / perron_zero,
                "odd_beta_two_first_zero": second_zero,
                "inferred_odd_beta_two_resonance": 1.0 / second_zero,
                "lambda": float(LAMBDA_FIXED),
                "lambda_inverse": float(1.0 / LAMBDA_FIXED),
            }
        )
    write_csv(RESULTS / "fredholm_zero_convergence.csv", rows)
    return rows


def plot_postcritical(
    trace_rows: list[dict[str, object]],
    zeta_rows: list[dict[str, object]],
    multiprecision_tail: dict[int, tuple[np.longdouble, np.longdouble]],
) -> None:
    length = np.asarray([int(row["two_step_length"]) for row in trace_rows])
    trace = np.asarray([float(row["component_weighted_trace"]) for row in trace_rows])
    model = np.asarray([float(row["perron_postcritical_model"]) for row in trace_rows])
    remainder = np.asarray([float(row["postcritical_remainder"]) for row in trace_rows])
    for index, current_length in enumerate(length):
        if int(current_length) in multiprecision_tail:
            trace_value, remainder_value = multiprecision_tail[int(current_length)]
            trace[index] = float(trace_value)
            remainder[index] = float(remainder_value)
    ratio = remainder[1:] / remainder[:-1]
    degrees = np.asarray([int(row["truncation_degree"]) for row in zeta_rows])
    root_error = np.asarray([float(row["absolute_root_error"]) for row in zeta_rows])
    partial_g = np.asarray([float(row["partial_G_at_lambda"]) for row in zeta_rows])

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.2))
    axes[0, 0].plot(length, trace, "o-", ms=3.8, color="#2455a4", label=r"exact $q_n$")
    axes[0, 0].plot(length, model, "--", color="#a0273f", label=r"$1-\lambda^{-n}+\lambda^{-2n}$")
    axes[0, 0].set(xlabel=r"two-step length $n$", ylabel="weighted trace", title="Exact postcritical model")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].semilogy(length, remainder, "o-", ms=3.8, color="#3a8f6b", label=r"$e_n$")
    reference = remainder[8] * (0.208 ** (length - length[8]))
    axes[0, 1].semilogy(length, reference, ":", color="black", label=r"reference $0.208^n$")
    axes[0, 1].set(xlabel=r"two-step length $n$", ylabel=r"$e_n$", title="Deflated remainder")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    axes[1, 0].plot(length[1:], ratio, "o-", ms=3.8, color="#7049a8")
    axes[1, 0].axhline(1.0 / float(LAMBDA_FIXED) ** 3, color="#a0273f", ls="--", lw=1.0, label=r"$\lambda^{-3}$")
    axes[1, 0].set(xlabel=r"two-step length $n$", ylabel=r"$e_n/e_{n-1}$", title="Remainder ratio")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    twin = axes[1, 1].twinx()
    axes[1, 1].semilogy(degrees, root_error, "o-", ms=3.8, color="#a0273f", label=r"$|z_N-\lambda|$")
    twin.plot(degrees, partial_g, "s--", ms=3.2, color="#2455a4", label=r"$G_N(\lambda)$")
    axes[1, 1].set(xlabel="truncation degree", ylabel=r"$|z_N-\lambda|$", title="Zero and deflated value")
    twin.set_ylabel(r"$G_N(\lambda)$")
    handles_a, labels_a = axes[1, 1].get_legend_handles_labels()
    handles_b, labels_b = twin.get_legend_handles_labels()
    axes[1, 1].legend(handles_a + handles_b, labels_a + labels_b, frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"postcritical_zeta_factorization.{suffix}",
            dpi=220,
            bbox_inches="tight",
        )
    plt.close(fig)


def plot_lift(
    lift_rows: list[dict[str, object]],
    fredholm_rows: list[dict[str, object]],
) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 1000)
    derivative = lift_derivative(theta)
    length = np.asarray([int(row["two_step_length"]) for row in lift_rows])
    reconstruction_error = np.asarray(
        [abs(float(row["reconstruction_error"])) for row in lift_rows]
    )
    reconstruction_error = np.maximum(
        reconstruction_error, 0.5 * np.finfo(np.float64).eps
    )
    even_centered = np.asarray(
        [float(row["even_beta_one_flat_trace"]) - 1.0 for row in lift_rows]
    )
    odd_second = np.asarray(
        [float(row["odd_beta_two_flat_trace"]) for row in lift_rows]
    )
    degrees = np.asarray([int(row["truncation_degree"]) for row in fredholm_rows])
    resonance_one = np.asarray(
        [float(row["inferred_even_beta_one_resonance"]) for row in fredholm_rows]
    )
    resonance_two = np.asarray(
        [float(row["inferred_odd_beta_two_resonance"]) for row in fredholm_rows]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.2))
    axes[0, 0].plot(theta, derivative, color="#2455a4")
    axes[0, 0].axhline(float(LAMBDA_FIXED), color="#a0273f", ls="--", label=r"$\min F'=\lambda$")
    axes[0, 0].set(xlabel=r"$\theta$", ylabel=r"$F'(\theta)$", title="Analytic expanding lift")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].semilogy(length, reconstruction_error, "o-", ms=3.8, color="#3a8f6b")
    axes[0, 1].set(xlabel=r"iterate $n$", ylabel="absolute error", title="Exact trace reconstruction audit")
    axes[0, 1].grid(alpha=0.22)

    axes[1, 0].semilogy(length, even_centered, "o-", ms=3.8, color="#2455a4", label=r"$E_{1,n}-1$")
    axes[1, 0].semilogy(length, odd_second, "s--", ms=3.4, color="#a0273f", label=r"$O_{2,n}$")
    axes[1, 0].set(xlabel=r"iterate $n$", ylabel="flat trace", title="Two Fredholm sectors")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    axes[1, 1].plot(degrees, resonance_one, "o-", ms=3.8, color="#2455a4", label=r"even $\beta=1$")
    axes[1, 1].plot(degrees, resonance_two, "s--", ms=3.4, color="#a0273f", label=r"odd $\beta=2$")
    axes[1, 1].axhline(float(1.0 / LAMBDA_FIXED), color="black", ls=":", label=r"$\lambda^{-1}$")
    axes[1, 1].set(xlabel="Fredholm truncation degree", ylabel="inferred leading resonance", title="Noncancellation margin")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"circle_lift_fredholm_audit.{suffix}",
            dpi=220,
            bbox_inches="tight",
        )
    plt.close(fig)


def write_summary(
    trace_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    zeta_rows: list[dict[str, object]],
    fredholm_rows: list[dict[str, object]],
    multiprecision_tail: dict[int, tuple[np.longdouble, np.longdouble]],
) -> dict[str, object]:
    if multiprecision_tail:
        tail_lengths = sorted(multiprecision_tail)
        tail_remainders = [
            multiprecision_tail[length][1]
            for length in tail_lengths
        ]
        last_ratios = [
            float(tail_remainders[index] / tail_remainders[index - 1])
            for index in range(1, len(tail_remainders))
        ][-5:]
        maximum_length = tail_lengths[-1]
        maximum_trace = multiprecision_tail[maximum_length][0]
        maximum_remainder = tail_remainders[-1]
        tail_arithmetic = "50-decimal-place exhaustive mpmath"
    else:
        last_ratios = [
            float(row["successive_remainder_ratio"])
            for row in trace_rows[-5:]
        ]
        maximum_length = int(trace_rows[-1]["two_step_length"])
        maximum_trace = np.longdouble(trace_rows[-1]["component_weighted_trace"])
        maximum_remainder = np.longdouble(trace_rows[-1]["postcritical_remainder"])
        tail_arithmetic = "long double"
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "mpmath": mp.__version__,
            "platform": platform.platform(),
        },
        "constants": {
            "u_critical_long_double": np.format_float_positional(
                U_CRITICAL, precision=21, unique=False, trim="k"
            ),
            "r_fixed_long_double": np.format_float_positional(
                R_FIXED, precision=21, unique=False, trim="k"
            ),
            "lambda_fixed_long_double": np.format_float_positional(
                LAMBDA_FIXED, precision=21, unique=False, trim="k"
            ),
            "lambda_inverse": float(1.0 / LAMBDA_FIXED),
            "lambda_inverse_squared": float(1.0 / LAMBDA_FIXED**2),
        },
        "exact_results": {
            "component_trace_identity": "q_n=E_{1,n}-O_{2,n}-lambda^{-n}+lambda^{-2n}",
            "zeta_factorization": "Z=(D_{2,-}/D_{1,+})*(1-z/lambda)/(1-z/lambda^2)",
            "lift_fixed_counts": "#Fix(F^n)=2^n-1 and #Fix(iota F^n)=2^n+1",
        },
        "logical_status": {
            "odd_beta_two_at_lambda": "proved nonzero by a strict pressure bound",
            "simple_zero_at_lambda": "equivalent to absence of the non-Perron eigenvalue lambda^{-1} in L_{1,+}",
            "spectral_noncancellation": "high-precision numerical evidence; not a theorem",
        },
        "numerical_audit": {
            "maximum_component_length": maximum_length,
            "fixed_points_at_maximum_length": int(
                1 << maximum_length
            ),
            "tail_arithmetic": tail_arithmetic,
            "component_trace_at_maximum_length": long_double_string(maximum_trace),
            "postcritical_remainder_at_maximum_length": long_double_string(
                maximum_remainder
            ),
            "median_last_five_remainder_ratios": float(np.median(last_ratios)),
            "maximum_lift_reconstruction_error": max(
                abs(float(row["reconstruction_error"])) for row in lift_rows
            ),
            "degree_20_centered_root": float(
                zeta_rows[-1]["centered_zeta_positive_root"]
            ),
            "degree_20_root_error": float(zeta_rows[-1]["absolute_root_error"]),
            "partial_G_at_lambda_degree_20": float(
                zeta_rows[-1]["partial_G_at_lambda"]
            ),
            "degree_10_even_beta_one_resonance": float(
                fredholm_rows[-1]["inferred_even_beta_one_resonance"]
            ),
            "degree_10_odd_beta_two_resonance": float(
                fredholm_rows[-1]["inferred_odd_beta_two_resonance"]
            ),
        },
    }
    with (RESULTS / "postcritical_factorization_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return summary


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    traces, trace_rows = component_trace_audit()
    lift_rows, even_one, odd_two = lift_factorization_audit(traces)
    multiprecision_audit(traces)
    multiprecision_tail = load_multiprecision_tail()
    analysis_traces = traces.copy()
    for length, (value, _) in multiprecision_tail.items():
        if length <= analysis_traces.size:
            analysis_traces[length - 1] = value
    zeta_rows = zeta_audit(analysis_traces)
    fredholm_rows = fredholm_audit(even_one, odd_two)
    plot_postcritical(trace_rows, zeta_rows, multiprecision_tail)
    plot_lift(lift_rows, fredholm_rows)
    summary = write_summary(
        trace_rows,
        lift_rows,
        zeta_rows,
        fredholm_rows,
        multiprecision_tail,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
