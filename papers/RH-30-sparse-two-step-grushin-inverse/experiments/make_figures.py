"""Aggregate RH-30 archives and render the manuscript figures."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def pilot_row(path: Path, *, auxiliary_scale: float = 1.0) -> dict[str, object]:
    data = load_json(path)
    selected = min(
        data["scales"],
        key=lambda row: abs(float(row["auxiliary_scale"]) - auxiliary_scale),
    )
    if abs(float(selected["auxiliary_scale"]) - auxiliary_scale) > 1.0e-14:
        raise ValueError(f"auxiliary scale {auxiliary_scale:g} missing from {path}")
    return {
        "sigma": float(data["sigma"]),
        "physical_dimension": int(selected["physical_dimension"]),
        "bordered_dimension": int(selected["bordered_dimension"]),
        "border_rank": int(selected["border_rank"]),
        "matrix_nnz": int(selected["matrix_nnz"]),
        "factor_nnz": int(selected["factor_nnz"]),
        "factor_fill_ratio": float(selected["factor_fill_ratio"]),
        "factor_seconds": float(selected["factor_seconds"]),
        "peak_memory_mb": float(selected["peak_memory_after_factor_mb"]),
        "physical_inverse_candidate": float(
            selected["physical_inverse"]["inverse_norm_candidate"]
        ),
        "physical_triplet_residual": float(
            selected["physical_inverse"]["triplet_residual"]
        ),
        "full_inverse_candidate": float(
            selected["full_inverse"]["inverse_norm_candidate"]
        ),
        "full_triplet_residual": float(selected["full_inverse"]["triplet_residual"]),
        "lifted_inverse_budget_lower": float(
            selected["lifted_inverse_budget_lower"]
        ),
        "physical_candidate_budget_margin": float(
            selected["physical_budget_margin"]
        ),
        "full_candidate_budget_margin": float(selected["full_budget_margin"]),
    }


def certificate_row(path: Path) -> dict[str, object]:
    data = load_json(path)
    return {
        "sigma": float(data["sigma"]),
        "physical_dimension": int(data["physical_dimension"]),
        "bordered_dimension": int(data["bordered_dimension"]),
        "border_rank": int(data["border_rank"]),
        "matrix_nnz": int(data["matrix_nnz"]),
        "factor_nnz": int(data["factor_nnz"]),
        "factor_fill_ratio": float(data["factor_fill_ratio"]),
        "factor_seconds": float(data["factor_seconds"]),
        "certificate_seconds": float(data["certificate_seconds"]),
        "approximate_inverse_frobenius_upper": float(
            data["approximate_inverse_frobenius_upper"]
        ),
        "residual_frobenius_upper": float(data["residual_frobenius_upper"]),
        "lifted_inverse_two_norm_upper": float(
            data["lifted_inverse_two_norm_upper"]
        ),
        "lifted_inverse_budget_lower": float(data["lifted_inverse_budget_lower"]),
        "certified_budget_margin": float(data["certified_budget_margin"]),
        "original_center_inverse_two_norm_upper": float(
            data["original_center_inverse_two_norm_upper"]
        ),
        "selected_arc_inverse_two_norm_upper": float(
            data["selected_arc_inverse_two_norm_upper"]
        ),
        "rh28_selected_arc_resolvent_budget_lower": float(
            data["rh28_selected_arc_resolvent_budget_lower"]
        ),
        "selected_arc_budget_margin": float(data["selected_arc_budget_margin"]),
        "status": str(data["status"]),
    }


def scaling_exponent(x: np.ndarray, y: np.ndarray) -> float:
    slope, _ = np.polyfit(np.log(x), np.log(y), 1)
    return float(slope)


def main() -> None:
    auxiliary_scan = load_json(RESULTS / "pilot_auxiliary_scan_sigma_1e-2.json")
    auxiliary_rows = [
        {
            "auxiliary_scale": float(row["auxiliary_scale"]),
            "matrix_one_norm": float(row["matrix_one_norm"]),
            "matrix_infinity_norm": float(row["matrix_infinity_norm"]),
            "factor_fill_ratio": float(row["factor_fill_ratio"]),
            "physical_inverse_candidate": float(
                row["physical_inverse"]["inverse_norm_candidate"]
            ),
            "full_inverse_candidate": float(
                row["full_inverse"]["inverse_norm_candidate"]
            ),
            "full_triplet_residual": float(row["full_inverse"]["triplet_residual"]),
            "full_candidate_budget_margin": float(row["full_budget_margin"]),
        }
        for row in auxiliary_scan["scales"]
    ]
    auxiliary_rows.sort(key=lambda row: float(row["auxiliary_scale"]))
    pilot_rows = [
        pilot_row(RESULTS / "pilot_auxiliary_scan_sigma_1e-2.json"),
        pilot_row(RESULTS / "pilot_sigma_4e-3_t1.json"),
        pilot_row(RESULTS / "pilot_sigma_2e-3_t1.json"),
    ]
    pilot_rows.sort(key=lambda row: int(row["physical_dimension"]))
    certificate_rows = [
        certificate_row(path)
        for path in RESULTS.glob("stored_inverse_certificate_sigma_*.json")
        if "chunk" not in path.stem
    ]
    certificate_rows.sort(key=lambda row: int(row["physical_dimension"]))
    write_csv(RESULTS / "sparse_lu_scale_summary.csv", pilot_rows)
    write_csv(RESULTS / "stored_certificate_summary.csv", certificate_rows)
    write_csv(RESULTS / "auxiliary_scale_summary.csv", auxiliary_rows)

    dimensions = np.asarray(
        [float(row["physical_dimension"]) for row in pilot_rows]
    )
    matrix_nnz = np.asarray([float(row["matrix_nnz"]) for row in pilot_rows])
    factor_nnz = np.asarray([float(row["factor_nnz"]) for row in pilot_rows])
    factor_seconds = np.asarray(
        [float(row["factor_seconds"]) for row in pilot_rows]
    )
    certificate_dimensions = np.asarray(
        [float(row["physical_dimension"]) for row in certificate_rows]
    )
    certificate_seconds = np.asarray(
        [float(row["certificate_seconds"]) for row in certificate_rows]
    )
    summary = {
        "status": "two_rigorous_selected_arc_closures",
        "rigorous_scale_count": len(certificate_rows),
        "floating_pilot_scale_count": len(pilot_rows),
        "matrix_nnz_scaling_exponent": scaling_exponent(dimensions, matrix_nnz),
        "factor_nnz_scaling_exponent": scaling_exponent(dimensions, factor_nnz),
        "factor_time_scaling_exponent": scaling_exponent(dimensions, factor_seconds),
        "certificate_time_two_point_exponent": scaling_exponent(
            certificate_dimensions, certificate_seconds
        ),
        "minimum_certified_lifted_budget_margin": min(
            float(row["certified_budget_margin"]) for row in certificate_rows
        ),
        "maximum_residual_frobenius_upper": max(
            float(row["residual_frobenius_upper"]) for row in certificate_rows
        ),
    }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.size": 9.0,
            "axes.labelsize": 9.5,
            "axes.titlesize": 10.0,
            "legend.fontsize": 8.0,
            "figure.dpi": 120,
        }
    )

    figure, axes = plt.subplots(1, 2, figsize=(9.0, 3.55))
    axes[0].loglog(dimensions, matrix_nnz, "o-", label="nnz(G)")
    axes[0].loglog(dimensions, factor_nnz, "s-", label="nnz(L) + nnz(U)")
    axes[0].set_xlabel("physical dimension $n$")
    axes[0].set_ylabel("stored nonzeros")
    axes[0].set_title("Sparse storage grows mildly on three pilot scales")
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend()

    physical = np.asarray(
        [float(row["physical_inverse_candidate"]) for row in pilot_rows]
    )
    full = np.asarray([float(row["full_inverse_candidate"]) for row in pilot_rows])
    budgets = np.asarray(
        [float(row["lifted_inverse_budget_lower"]) for row in pilot_rows]
    )
    axes[1].loglog(dimensions, physical, "o-", label="physical inverse candidate")
    axes[1].loglog(dimensions, full, "s-", label="full bordered inverse candidate")
    axes[1].loglog(dimensions, budgets, "^-", label="RH-29 lifted budget")
    axes[1].set_xlabel("physical dimension $n$")
    axes[1].set_ylabel("inverse norm / budget")
    axes[1].set_title("The full border retains a large candidate margin")
    axes[1].grid(True, which="both", alpha=0.25)
    axes[1].legend()
    figure.tight_layout()
    figure.savefig(FIGURES / "sparse_grushin_scaling.pdf")
    figure.savefig(FIGURES / "sparse_grushin_scaling.png", dpi=220)
    plt.close(figure)

    figure, axes = plt.subplots(1, 2, figsize=(9.0, 3.55))
    labels = [f"{float(row['sigma']):.0e}" for row in certificate_rows]
    x = np.arange(len(certificate_rows), dtype=np.float64)
    candidates = []
    for row in certificate_rows:
        matching = min(
            pilot_rows,
            key=lambda pilot: abs(float(pilot["sigma"]) - float(row["sigma"])),
        )
        candidates.append(float(matching["physical_inverse_candidate"]))
    certified = np.asarray(
        [float(row["lifted_inverse_two_norm_upper"]) for row in certificate_rows]
    )
    certified_budgets = np.asarray(
        [float(row["lifted_inverse_budget_lower"]) for row in certificate_rows]
    )
    axes[0].semilogy(x, candidates, "o", markersize=7, label="floating candidate")
    axes[0].semilogy(x, certified, "s", markersize=7, label="rigorous upper bound")
    axes[0].semilogy(x, certified_budgets, "^", markersize=8, label="required budget")
    for index in range(len(x)):
        axes[0].plot(
            [x[index], x[index]],
            [certified[index], certified_budgets[index]],
            color="0.7",
            linewidth=1.0,
        )
    axes[0].set_xticks(x, labels)
    axes[0].set_xlabel("noise scale σ")
    axes[0].set_ylabel("lifted inverse norm")
    axes[0].set_title("Two deterministic lifted-inverse closures")
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend()

    residuals = np.asarray(
        [float(row["residual_frobenius_upper"]) for row in certificate_rows]
    )
    times = np.asarray(
        [float(row["certificate_seconds"]) for row in certificate_rows]
    )
    axes[1].semilogy(x, residuals, "o-", color="tab:green", label="residual Frobenius bound")
    axes[1].axhline(1.0, color="black", linestyle="--", linewidth=1.0, label="Neumann threshold")
    time_axis = axes[1].twinx()
    time_axis.plot(x, times, "s--", color="tab:red", label="certificate seconds")
    axes[1].set_xticks(x, labels)
    axes[1].set_xlabel("noise scale σ")
    axes[1].set_ylabel("outward residual bound")
    time_axis.set_ylabel("wall time (s)")
    axes[1].set_title("Residuals are tiny; all-column cost grows")
    axes[1].grid(True, which="both", alpha=0.25)
    handles, legend_labels = axes[1].get_legend_handles_labels()
    handles2, legend_labels2 = time_axis.get_legend_handles_labels()
    axes[1].legend(handles + handles2, legend_labels + legend_labels2, loc="center left")
    figure.tight_layout()
    figure.savefig(FIGURES / "stored_inverse_closure.pdf")
    figure.savefig(FIGURES / "stored_inverse_closure.png", dpi=220)
    plt.close(figure)

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
