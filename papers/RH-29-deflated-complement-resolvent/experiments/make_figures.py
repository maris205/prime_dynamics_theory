"""Figures and final metadata for RH-29."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import flint
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_figure(figure: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight")
    figure.savefig(FIGURES / f"{stem}.png", dpi=220, bbox_inches="tight")
    plt.close(figure)


def budget_figure(rows: list[dict[str, str]]) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    position = -np.log10(sigma)
    arc_budget = np.asarray(
        [float(row["rh28_arc_resolvent_budget_lower"]) for row in rows]
    )
    raw_arc = np.asarray(
        [float(row["floating_arc_inverse_candidate"]) for row in rows]
    )
    deflated_arc = np.asarray(
        [float(row["conditional_arc_inverse_candidate_bound"]) for row in rows]
    )
    bulk_budget = np.asarray(
        [float(row["lifted_inverse_budget_lower"]) for row in rows]
    )
    bulk_candidate = np.asarray(
        [float(row["lifted_bulk_inverse_candidate"]) for row in rows]
    )

    figure, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    axes[0].semilogy(position, arc_budget, "o-", label=r"RH-28 $M_{*,a}^-$")
    axes[0].semilogy(position, raw_arc, "s-", label="inverse-iteration candidate")
    axes[0].semilogy(
        position,
        deflated_arc,
        "^-",
        label="one-channel conditional bound",
    )
    axes[0].set_xlabel(r"noise scale $-\log_{10}\sigma$")
    axes[0].set_ylabel("arc resolvent scale")
    axes[0].set_title("Original RH-28 gate")
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend(fontsize=8)

    axes[1].semilogy(position, bulk_budget, "o-", label=r"lifted budget $K_*^-$")
    axes[1].semilogy(position, bulk_candidate, "s-", label="lifted inverse candidate")
    axes[1].set_xlabel(r"noise scale $-\log_{10}\sigma$")
    axes[1].set_ylabel("lifted inverse scale")
    axes[1].set_title("Deflated bulk gate")
    axes[1].grid(True, which="both", alpha=0.25)
    axes[1].legend(fontsize=8)
    save_figure(figure, "deflated_budget_summary")


def gap_figure(rows: list[dict[str, str]]) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    position = -np.log10(sigma)
    first = np.asarray([float(row["stored_singular_scalar"]) for row in rows])
    bulk = np.asarray(
        [float(row["lifted_bulk_singular_candidate"]) for row in rows]
    )
    required = np.asarray(
        [float(row["required_lifted_singular_lower"]) for row in rows]
    )
    gap = bulk / first
    margin = np.asarray(
        [float(row["lifted_bulk_budget_margin"]) for row in rows]
    )
    right_residual = np.asarray(
        [float(row["normalized_right_residual_norm_upper"]) for row in rows]
    )
    left_residual = np.asarray(
        [float(row["normalized_left_residual_norm_upper"]) for row in rows]
    )

    figure, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    axes[0].semilogy(position, first, "o-", label=r"dangerous $\widehat s$")
    axes[0].semilogy(position, bulk, "s-", label="lifted bulk candidate")
    axes[0].semilogy(position, required, "^-", label="required bulk lower bound")
    axes[0].set_xlabel(r"noise scale $-\log_{10}\sigma$")
    axes[0].set_ylabel("singular-value scale")
    axes[0].set_title("One-channel singular separation")
    axes[0].grid(True, which="both", alpha=0.25)
    axes[0].legend(fontsize=8)

    axes[1].semilogy(position, gap, "o-", label="bulk / dangerous gap")
    axes[1].semilogy(position, margin, "s-", label="bulk budget margin")
    axes[1].semilogy(position, right_residual / np.min(right_residual), "--", alpha=0.5, label="right residual / min")
    axes[1].semilogy(position, left_residual / np.min(left_residual), ":", alpha=0.7, label="left residual / min")
    axes[1].set_xlabel(r"noise scale $-\log_{10}\sigma$")
    axes[1].set_ylabel("dimensionless ratio")
    axes[1].set_title("Gap and certification margins")
    axes[1].grid(True, which="both", alpha=0.25)
    axes[1].legend(fontsize=8)
    save_figure(figure, "deflated_gap_summary")


def numerical_range_figure() -> None:
    witness = json.loads(
        (RESULTS / "certified_numerical_range_witness.json").read_text(
            encoding="utf-8"
        )
    )
    scan = json.loads(
        (RESULTS / "deflated_accretivity_sigma_1e-2.json").read_text(
            encoding="utf-8"
        )
    )
    centers = np.asarray(
        [
            0.5 * (row["real_lower"] + row["real_upper"])
            + 0.5j * (row["imag_lower"] + row["imag_upper"])
            for row in witness["point_intervals"]
        ]
    )
    closed = np.concatenate([centers, centers[:1]])
    figure, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    axes[0].plot(closed.real, closed.imag, "o-", color="tab:blue")
    axes[0].plot(0.0, 0.0, "r*", markersize=11, label="origin")
    for index, value in enumerate(centers):
        axes[0].annotate(f"$w_{index + 1}$", (value.real, value.imag), xytext=(4, 4), textcoords="offset points")
    axes[0].axhline(0.0, color="black", linewidth=0.6, alpha=0.4)
    axes[0].axvline(0.0, color="black", linewidth=0.6, alpha=0.4)
    axes[0].set_aspect("equal", adjustable="datalim")
    axes[0].set_xlabel("real part")
    axes[0].set_ylabel("imaginary part")
    axes[0].set_title("Certified compressed numerical-range witness")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.2)

    for lift in sorted({float(row["lift"]) for row in scan["rows"]}):
        selected = [row for row in scan["rows"] if float(row["lift"]) == lift]
        phase = np.asarray([float(row["phase"]) / np.pi for row in selected])
        values = np.asarray(
            [float(row["minimum_hermitian_candidate"]) for row in selected]
        )
        axes[1].plot(phase, values, "o-", label=fr"lift $\tau={lift:g}$")
    axes[1].axhline(0.0, color="red", linewidth=0.8)
    axes[1].set_xlabel(r"rotation phase $\phi/\pi$")
    axes[1].set_ylabel(r"candidate $\lambda_{\min}\Re(e^{-i\phi}\widetilde A)$")
    axes[1].set_title("Accretivity scan remains negative")
    axes[1].grid(True, alpha=0.25)
    axes[1].legend(fontsize=8)
    save_figure(figure, "numerical_range_no_go")


def write_metadata(rows: list[dict[str, str]]) -> None:
    summary = {
        "minimum_original_arc_budget_margin": min(
            float(row["floating_arc_budget_margin"]) for row in rows
        ),
        "minimum_lifted_bulk_budget_margin": min(
            float(row["lifted_bulk_budget_margin"]) for row in rows
        ),
        "minimum_singular_gap_ratio": min(
            float(row["lifted_bulk_singular_candidate"])
            / float(row["stored_singular_scalar"])
            for row in rows
        ),
        "maximum_normalized_right_residual_upper": max(
            float(row["normalized_right_residual_norm_upper"]) for row in rows
        ),
        "maximum_normalized_left_residual_upper": max(
            float(row["normalized_left_residual_norm_upper"]) for row in rows
        ),
        "finest_conditional_arc_candidate_bound": float(
            rows[-1]["conditional_arc_inverse_candidate_bound"]
        ),
        "finest_rh28_arc_budget_lower": float(
            rows[-1]["rh28_arc_resolvent_budget_lower"]
        ),
        "certified_numerical_range_no_go": 1,
    }
    (RESULTS / "deflated_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    source_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "src" / "deflated_resolvent" / "algebra.py",
        ROOT / "src" / "deflated_resolvent" / "norms.py",
        ROOT / "experiments" / "run_resolvent_pilot.py",
        ROOT / "experiments" / "run_rank_one_lift_pilot.py",
        ROOT / "experiments" / "run_deflated_certificate.py",
        ROOT / "experiments" / "run_certified_numerical_range_witness.py",
        ROOT / "experiments" / "refresh_lift_diagnostics.py",
        ROOT / "tests" / "test_deflated_resolvent.py",
        Path(__file__),
    ]
    result_paths = [
        ROOT / "one-channel-grushin-deflation.pdf",
        RESULTS / "deflated_scale_summary.csv",
        RESULTS / "deflated_summary.json",
        RESULTS / "certified_numerical_range_witness.json",
        RESULTS / "compressed_numerical_range_witness.json",
        RESULTS / "deflated_accretivity_sigma_1e-2.json",
    ]
    triplet_paths = sorted((RESULTS / "triplets").glob("*.npz"))
    diagnostic_paths = sorted(RESULTS.glob("rank_one_lift_sigma_*.json"))
    figure_paths = sorted(FIGURES.glob("*.pdf")) + sorted(FIGURES.glob("*.png"))
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "python_flint": flint.__version__,
        "sigmas": [float(row["sigma"]) for row in rows],
        "source_hashes": {
            str(path.relative_to(ROOT)): source_hash(path) for path in source_paths
        },
        "input_hashes": {
            "rh28_arcwise_contour_arcs.csv": source_hash(
                RH28 / "results" / "arcwise_contour_arcs.csv"
            )
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): source_hash(path)
            for path in result_paths + triplet_paths + diagnostic_paths + figure_paths
        },
    }
    (RESULTS / "deflated_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-only", action="store_true")
    arguments = parser.parse_args()
    rows = read_csv(RESULTS / "deflated_scale_summary.csv")
    if not arguments.metadata_only:
        budget_figure(rows)
        gap_figure(rows)
        numerical_range_figure()
    write_metadata(rows)


if __name__ == "__main__":
    main()
