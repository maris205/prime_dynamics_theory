"""Generate the Arb certificate, stability data, and audit figures."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path

import flint
from flint import arb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from validated_gap import (
    LAMBDA_FIXED,
    certify_reduced_gap,
    leading_eigenvalues,
    reduced_beta_one_matrix,
    sector_matrices,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

EXPECTED_EVEN_ONE_CENTERED = np.asarray(
    [
        2.3849119781623518e-1,
        4.3940546389003020e-2,
        9.0025259375838830e-3,
        1.8679794144809136e-3,
        3.8822358995527220e-4,
        8.0701562705787210e-5,
        1.6776198787038510e-5,
        3.4874394423400900e-6,
        7.2496990055626040e-7,
        1.5070696468555410e-7,
    ]
)
EXPECTED_ODD_TWO = np.asarray(
    [
        1.8292556703613560e-1,
        2.3976300252288668e-2,
        3.5670780045273798e-3,
        5.4174287194709570e-4,
        8.2569429808249100e-5,
        1.2592539976867545e-5,
        1.9206748640785560e-6,
        2.9295601688007070e-7,
        4.4684035463513766e-8,
        6.8155765471471230e-9,
    ]
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def arb_record(value: arb) -> dict[str, object]:
    return {
        "interval": str(value),
        "lower_float": float(value.lower()),
        "upper_float": float(value.upper()),
    }


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_primary_certificate() -> tuple[object, dict[str, object]]:
    result = certify_reduced_gap()
    values: dict[str, object] = {}
    for field in fields(result):
        value = getattr(result, field.name)
        values[field.name] = arb_record(value) if isinstance(value, arb) else value
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "python_flint": flint.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "source_sha256": {
            "certificate.py": source_hash(
                ROOT / "src" / "validated_gap" / "certificate.py"
            ),
            "taylor_operator.py": source_hash(
                ROOT / "src" / "validated_gap" / "taylor_operator.py"
            ),
        },
        "parameters_and_bounds": values,
        "theorem_checks": {
            "beta_one_cube_below_lambda_inverse_six": result.beta_one_certified,
            "beta_two_square_below_lambda_inverse_four": result.beta_two_certified,
            "conclusion": "r(T_1,0), r(T_2,-) < lambda^(-2)",
            "coefficient_rate": "q_n=1-lambda^(-n)+lambda^(-2n)+O(3^(-n))",
        },
    }
    with (RESULTS / "validated_spectral_gap_certificate.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return result, payload


def dimension_stability() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dimension in (30, 40, 50, 60, 70):
        print(f"validated dimension {dimension}", flush=True)
        result = certify_reduced_gap(
            decimal_precision=100,
            dimension=dimension,
            tail_degree=dimension + 50,
        )
        rows.append(
            {
                "dimension": dimension,
                "tail_degree": dimension + 50,
                "beta_one_cube_bound_upper": float(
                    result.beta_one_cube_bound.upper()
                ),
                "lambda_inverse_six_lower": float(
                    result.beta_one_threshold.lower()
                ),
                "beta_one_radius_bound_upper": float(
                    result.beta_one_radius_bound.upper()
                ),
                "beta_two_square_bound_upper": float(
                    result.beta_two_square_bound.upper()
                ),
                "lambda_inverse_four_lower": float(
                    result.beta_two_threshold.lower()
                ),
                "beta_two_radius_bound_upper": float(
                    result.beta_two_radius_bound.upper()
                ),
                "target_radius_lower": float(result.target_radius.lower()),
                "both_certified": result.beta_one_certified
                and result.beta_two_certified,
            }
        )
    write_csv(RESULTS / "dimension_stability.csv", rows)
    return rows


def trace_and_resonance_audit() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    degree = 100
    radius = 0.7
    beta_one = reduced_beta_one_matrix(degree, radius)
    _, beta_two = sector_matrices(degree, radius)
    power_one = np.eye(beta_one.shape[0])
    power_two = np.eye(beta_two.shape[0])
    trace_rows: list[dict[str, object]] = []
    for index in range(10):
        power_one = power_one @ beta_one
        power_two = power_two @ beta_two
        observed_one = float(np.trace(power_one))
        observed_two = float(np.trace(power_two))
        trace_rows.append(
            {
                "iterate": index + 1,
                "taylor_even_beta_one_centered_trace": observed_one,
                "circle_even_beta_one_centered_trace": EXPECTED_EVEN_ONE_CENTERED[index],
                "beta_one_trace_difference": observed_one
                - EXPECTED_EVEN_ONE_CENTERED[index],
                "taylor_odd_beta_two_trace": observed_two,
                "circle_odd_beta_two_trace": EXPECTED_ODD_TWO[index],
                "beta_two_trace_difference": observed_two - EXPECTED_ODD_TWO[index],
            }
        )
    write_csv(RESULTS / "sector_trace_crosscheck.csv", trace_rows)

    resonance_rows: list[dict[str, object]] = []
    for sector, matrix in (("reduced_beta_one", beta_one), ("odd_beta_two", beta_two)):
        for rank, value in enumerate(leading_eigenvalues(matrix, 6), start=1):
            resonance_rows.append(
                {
                    "sector": sector,
                    "rank": rank,
                    "real_part": value.real,
                    "imaginary_part": value.imag,
                    "modulus": abs(value),
                    "lambda_inverse_squared": LAMBDA_FIXED**-2,
                    "status": "floating-point diagnostic only",
                }
            )
    write_csv(RESULTS / "leading_resonances.csv", resonance_rows)
    return trace_rows, resonance_rows


def plot_certificate(
    primary: object,
    stability_rows: list[dict[str, object]],
    trace_rows: list[dict[str, object]],
) -> None:
    dimension = np.asarray([int(row["dimension"]) for row in stability_rows])
    one_cube = np.asarray(
        [float(row["beta_one_cube_bound_upper"]) for row in stability_rows]
    )
    two_square = np.asarray(
        [float(row["beta_two_square_bound_upper"]) for row in stability_rows]
    )
    one_radius = np.asarray(
        [float(row["beta_one_radius_bound_upper"]) for row in stability_rows]
    )
    two_radius = np.asarray(
        [float(row["beta_two_radius_bound_upper"]) for row in stability_rows]
    )
    target = float(primary.target_radius.lower())

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.2))
    axes[0, 0].plot(dimension, one_cube, "o-", color="#2455a4", label=r"$\|\mathcal{T}_{1,0}^3\|$ bound")
    axes[0, 0].axhline(float(primary.beta_one_threshold.lower()), color="#2455a4", ls="--", label=r"$\lambda^{-6}$")
    axes[0, 0].plot(dimension, two_square, "s-", color="#a0273f", label=r"$\|\mathcal{T}_{2,-}^2\|$ bound")
    axes[0, 0].axhline(float(primary.beta_two_threshold.lower()), color="#a0273f", ls="--", label=r"$\lambda^{-4}$")
    axes[0, 0].set(xlabel="Taylor dimension", ylabel="certified power norm", title="Validated power inequalities")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].plot(dimension, one_radius, "o-", color="#2455a4", label=r"$r(\mathcal{T}_{1,0})$ bound")
    axes[0, 1].plot(dimension, two_radius, "s-", color="#a0273f", label=r"$r(\mathcal{T}_{2,-})$ bound")
    axes[0, 1].axhline(target, color="black", ls="--", label=r"$\lambda^{-2}$")
    axes[0, 1].set(xlabel="Taylor dimension", ylabel="spectral-radius upper bound", title="Reduced-sector disk gap")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    labels = [r"finite $\beta=1$", r"tail $\beta=1$", r"finite $\beta=2$", r"tail $\beta=2$"]
    values = [
        float(primary.beta_one_matrix_cube_norm.upper()),
        float(primary.beta_one_cube_bound.upper() - primary.beta_one_matrix_cube_norm.lower()),
        float(primary.beta_two_matrix_square_norm.upper()),
        float(primary.beta_two_square_bound.upper() - primary.beta_two_matrix_square_norm.lower()),
    ]
    colors = ["#2455a4", "#7ea1d6", "#a0273f", "#d78a9a"]
    axes[1, 0].bar(np.arange(4), values, color=colors)
    axes[1, 0].set_xticks(np.arange(4), labels, rotation=18, ha="right")
    axes[1, 0].set(ylabel="contribution to certified bound", title="Finite matrix versus analytic tail")
    axes[1, 0].grid(axis="y", alpha=0.22)

    iterate = np.asarray([int(row["iterate"]) for row in trace_rows])
    error_one = np.maximum(
        np.abs([float(row["beta_one_trace_difference"]) for row in trace_rows]),
        1.0e-17,
    )
    error_two = np.maximum(
        np.abs([float(row["beta_two_trace_difference"]) for row in trace_rows]),
        1.0e-17,
    )
    axes[1, 1].semilogy(iterate, error_one, "o-", color="#2455a4", label=r"even $\beta=1$")
    axes[1, 1].semilogy(iterate, error_two, "s-", color="#a0273f", label=r"odd $\beta=2$")
    axes[1, 1].set(xlabel="iterate", ylabel="Taylor/circle trace difference", title="Independent representation cross-check")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"validated_reduced_sector_gap.{suffix}",
            dpi=220,
            bbox_inches="tight",
        )
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    primary, payload = write_primary_certificate()
    stability_rows = dimension_stability()
    trace_rows, _ = trace_and_resonance_audit()
    plot_certificate(primary, stability_rows, trace_rows)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
