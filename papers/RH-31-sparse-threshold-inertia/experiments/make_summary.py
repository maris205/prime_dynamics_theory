"""Build the RH-31 summary table, plot, and machine-readable metadata."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
SOURCES = (
    RESULTS / "exact_target_inertia_sigma_1e-2_op24.json",
    RESULTS / "exact_target_inertia_sigma_4e-3_op24.json",
    RESULTS / "exact_target_inertia_sigma_2e-3.json",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def row(path: Path) -> dict[str, object]:
    data = load(path)
    bracket = data["inertia_bracket"]
    factors = {item["label"]: item for item in data["shifted_factorizations"]}
    minus = factors["minus"]
    plus = factors["plus"]
    alpha = float(data["threshold"])
    certified_inverse_upper = float(np.nextafter(1.0 / alpha, np.inf))
    budget_lower = 2.0 / alpha
    return {
        "sigma": float(data["sigma"]),
        "physical_dimension": int(data["physical_dimension"]),
        "grushin_dimension": int(data["grushin_dimension"]),
        "threshold_dimension": int(data["threshold_dimension"]),
        "threshold_matrix_nnz": int(data["threshold_matrix_nnz"]),
        "factor_nnz_per_side": int(minus["factor_nnz"]),
        "lower_shift": float(bracket["lower_shift"]),
        "upper_shift": float(bracket["upper_shift"]),
        "lower_error_upper": float(bracket["lower_shift_error_upper"]),
        "upper_error_upper": float(bracket["upper_shift_error_upper"]),
        "lower_utilization": float(bracket["lower_shift_error_upper"])
        / float(bracket["lower_shift"]),
        "upper_utilization": float(bracket["upper_shift_error_upper"])
        / float(bracket["upper_shift"]),
        "threshold": alpha,
        "lifted_inverse_budget_lower_recovered": budget_lower,
        "certified_full_grushin_inverse_upper": certified_inverse_upper,
        "budget_margin_lower": budget_lower / certified_inverse_upper,
        "grushin_matrix_error_frobenius_upper": float(
            data["grushin_matrix_error_frobenius_upper"]
        ),
        "threshold_transform_error_frobenius_upper": float(
            data["threshold_transform_error_frobenius_upper"]
        ),
        "minus_factor_seconds": float(minus["factor_seconds"]),
        "plus_factor_seconds": float(plus["factor_seconds"]),
        "factor_seconds_total": float(minus["factor_seconds"])
        + float(plus["factor_seconds"]),
        "peak_memory_mb": float(
            data.get(
                "peak_memory_mb_upper_across_runs", data.get("peak_memory_mb")
            )
        ),
        "positive_count": int(bracket["positive_count"]),
        "negative_count": int(bracket["negative_count"]),
        "operation_factor": int(
            minus["backward_error"]["elimination_operation_factor"]
        ),
        "source_file": str(path.relative_to(ROOT)),
        "source_sha256": digest(path),
    }


def empirical_exponent(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.polyfit(np.log(x), np.log(y), 1)[0])


def main() -> None:
    rows = [row(path) for path in SOURCES]
    fieldnames = list(rows[0])
    with (RESULTS / "threshold_inertia_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    dimension = np.asarray([item["physical_dimension"] for item in rows])
    factor_nnz = np.asarray([item["factor_nnz_per_side"] for item in rows])
    factor_time = np.asarray([item["minus_factor_seconds"] for item in rows])
    memory = np.asarray([item["peak_memory_mb"] for item in rows])
    summary = {
        "status": "three_exact_target_threshold_inertia_certificates",
        "certified_scales": [item["sigma"] for item in rows],
        "minimum_budget_margin_lower": min(
            item["budget_margin_lower"] for item in rows
        ),
        "maximum_shift_utilization": max(
            max(item["lower_utilization"], item["upper_utilization"])
            for item in rows
        ),
        "maximum_threshold_transform_error": max(
            item["threshold_transform_error_frobenius_upper"] for item in rows
        ),
        "empirical_exponents": {
            "factor_nnz_vs_physical_dimension": empirical_exponent(
                dimension, factor_nnz
            ),
            "one_side_factor_seconds_vs_physical_dimension": empirical_exponent(
                dimension, factor_time
            ),
            "peak_memory_vs_physical_dimension": empirical_exponent(
                dimension, memory
            ),
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): digest(path) for path in SOURCES
        },
    }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    FIGURES.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))
    axes[0].loglog(dimension, factor_nnz, "o-", label="factor nnz / side")
    axes[0].loglog(
        dimension,
        1.0e5 * factor_time,
        "s--",
        label=r"$10^5\times$ factor seconds",
    )
    axes[0].set_xlabel("physical dimension $n$")
    axes[0].set_ylabel("finite-scale cost indicator")
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend(frameon=False)

    positions = np.arange(len(rows))
    width = 0.34
    axes[1].bar(
        positions - width / 2,
        [item["lower_utilization"] for item in rows],
        width,
        label=r"lower $\varepsilon_-/\delta_-$",
    )
    axes[1].bar(
        positions + width / 2,
        [item["upper_utilization"] for item in rows],
        width,
        label=r"upper $\varepsilon_+/\delta_+$",
    )
    axes[1].axhline(1.0, color="black", linewidth=1.0, linestyle=":")
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels([r"$10^{-2}$", r"$4\cdot10^{-3}$", r"$2\cdot10^{-3}$"])
    axes[1].set_xlabel(r"noise scale $\sigma$")
    axes[1].set_ylabel("certified shift utilization")
    axes[1].set_ylim(0.0, 1.08)
    axes[1].grid(True, axis="y", alpha=0.25)
    axes[1].legend(frameon=False, fontsize=8)
    figure.tight_layout()
    figure.savefig(FIGURES / "threshold_inertia_scaling.pdf")
    figure.savefig(FIGURES / "threshold_inertia_scaling.png", dpi=180)
    plt.close(figure)


if __name__ == "__main__":
    main()
