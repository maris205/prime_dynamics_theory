"""Stored-factor certificates for one-channel complement-resolvent deflation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import flint
import numpy as np
import scipy


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
TRIPLETS = RESULTS / "triplets"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
sys.path[:0] = [
    str(ROOT / "src"),
    str(ROOT / "experiments"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from deflated_resolvent import (  # noqa: E402
    arb_vector_norm_interval,
    arc_center_threshold_lower,
    candidate_arc_inverse,
    lifted_full_inverse_upper,
    lifted_inverse_budget_lower,
    normalized_residual_bounds,
)
from outward_residuals import (  # noqa: E402
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
    componentwise_scalar_multiply,
    componentwise_subtract,
)
from run_resolvent_pilot import _gmres_solve, tightest_arc  # noqa: E402


DEFAULT_TOLERANCES = {
    1.0e-2: 1.0e-11,
    4.0e-3: 1.0e-10,
    2.0e-3: 1.0e-10,
    1.0e-3: 3.0e-10,
    5.0e-4: 1.0e-9,
    2.0e-4: 3.0e-9,
    1.0e-4: 1.0e-8,
}
DEFAULT_ITERATIONS = {
    1.0e-2: 4,
    4.0e-3: 4,
    2.0e-3: 4,
    1.0e-3: 3,
    5.0e-4: 3,
    2.0e-4: 3,
    1.0e-4: 3,
}
LIFT_RESULT_FILES = {
    1.0e-2: "rank_one_lift_sigma_1e-2.json",
    4.0e-3: "rank_one_lift_sigma_4e-3.json",
    2.0e-3: "rank_one_lift_sigma_2e-3.json",
    1.0e-3: "rank_one_lift_sigma_1e-3.json",
    5.0e-4: "rank_one_lift_sigma_5e-4.json",
    2.0e-4: "rank_one_lift_sigma_2e-4.json",
    1.0e-4: "rank_one_lift_sigma_1e-4.json",
}


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("at least one result row is required")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def inverse_triplet(operator, tolerance: float, iterations: int):
    dimension = int(operator.shape[0])
    vector = rh25_global.deterministic_start(dimension, 0.413)
    history = []
    for iteration in range(int(iterations)):
        begun = time.time()
        dual, dual_iterations, dual_residual = _gmres_solve(
            operator.H, vector, tolerance
        )
        updated, primal_iterations, primal_residual = _gmres_solve(
            operator, dual, tolerance
        )
        vector = updated / np.linalg.norm(updated)
        image = operator @ vector
        singular = float(np.linalg.norm(image))
        left = image / singular
        triplet_residual = float(
            np.linalg.norm(operator.H @ left - singular * vector)
        )
        row = {
            "iteration": iteration + 1,
            "singular_candidate": singular,
            "triplet_residual": triplet_residual,
            "dual_gmres_iterations": dual_iterations,
            "primal_gmres_iterations": primal_iterations,
            "dual_relative_residual": dual_residual,
            "primal_relative_residual": primal_residual,
            "seconds": time.time() - begun,
        }
        history.append(row)
        print(
            f"  inverse iteration {iteration + 1}/{iterations}: "
            f"s={singular:.8e}, residual={triplet_residual:.3e}, "
            f"gmres={dual_iterations}+{primal_iterations}",
            flush=True,
        )
    return singular, np.asarray(left), np.asarray(vector), history


def stored_residual_bounds(environment, spectral_parameter, singular, left, right):
    spectrum = environment["spectrum"]
    graph = ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )
    right_ball = ComponentwiseBall.exact(right)
    left_ball = ComponentwiseBall.exact(left)
    right_shifted = componentwise_subtract(
        componentwise_scalar_multiply(spectral_parameter, right_ball),
        graph.action(right_ball),
    )
    left_shifted = componentwise_subtract(
        componentwise_scalar_multiply(np.conj(spectral_parameter), left_ball),
        graph.action_adjoint(left_ball),
    )
    raw_right = componentwise_subtract(
        right_shifted,
        componentwise_scalar_multiply(singular, left_ball),
    )
    raw_left = componentwise_subtract(
        left_shifted,
        componentwise_scalar_multiply(singular, right_ball),
    )
    return raw_right.norm_upper, raw_left.norm_upper


def lift_diagnostic(sigma: float) -> tuple[float, float, float]:
    filename = LIFT_RESULT_FILES.get(float(sigma))
    if filename is None:
        return float("nan"), float("nan"), float("nan")
    path = RESULTS / filename
    if not path.exists():
        return float("nan"), float("nan"), float("nan")
    data = json.loads(path.read_text(encoding="utf-8"))
    singular = float(data["lifted_smallest_singular_candidate"])
    return (
        singular,
        1.0 / singular,
        float(data["lifted_triplet_residual"]),
    )


def audit_scale(sigma: float, tolerance: float, iterations: int) -> dict[str, object]:
    setting = rh24.physical_settings()[float(sigma)]
    arc = tightest_arc(float(sigma))
    point = complex(float(arc["center_real"]), float(arc["center_imag"]))
    print(
        f"deflated certificate sigma={sigma:g}, n={setting['dimension']}, "
        f"arc={arc['arc']}",
        flush=True,
    )
    begun = time.time()
    environment = rh25_global.add_adjoint_actions(
        rh25_global.build_environment(float(sigma), setting)
    )
    build_seconds = time.time() - begun
    operator = rh25_global.shifted_operator(environment, point)
    singular, left, right, history = inverse_triplet(
        operator, float(tolerance), int(iterations)
    )
    TRIPLETS.mkdir(parents=True, exist_ok=True)
    triplet_path = TRIPLETS / f"dangerous_triplet_sigma_{sigma:.0e}.npz"
    np.savez_compressed(
        triplet_path,
        singular_value=np.asarray([singular], dtype=np.float64),
        left=left,
        right=right,
    )
    right_norm = arb_vector_norm_interval(right)
    left_norm = arb_vector_norm_interval(left)
    raw_right, raw_left = stored_residual_bounds(
        environment, point, singular, left, right
    )
    normalized = normalized_residual_bounds(
        raw_right,
        raw_left,
        right_norm,
        left_norm,
        singular,
    )
    arc_budget = float(arc["resolvent_budget_lower"])
    arc_radius = float(arc["disc_radius"])
    center_budget = arc_center_threshold_lower(arc_budget, arc_radius)
    bulk_budget = lifted_inverse_budget_lower(
        center_budget,
        singular,
        normalized.right,
        normalized.left,
    )
    center_candidate = 1.0 / singular
    arc_candidate = candidate_arc_inverse(center_candidate, arc_radius)
    bulk_singular, bulk_inverse, bulk_residual = lift_diagnostic(float(sigma))
    if np.isfinite(bulk_inverse):
        conditional_full = lifted_full_inverse_upper(
            bulk_inverse,
            singular,
            normalized.right,
            normalized.left,
        ).full_inverse_upper
        conditional_arc = candidate_arc_inverse(conditional_full, arc_radius)
        bulk_budget_margin = bulk_budget / bulk_inverse
    else:
        conditional_full = float("nan")
        conditional_arc = float("nan")
        bulk_budget_margin = float("nan")
    return {
        "sigma": sigma,
        "folded_dimension": int(setting["dimension"]),
        "packet_rank": int(environment["analysis"].shape[0]),
        "tightest_arc": int(arc["arc"]),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "arc_disc_radius": arc_radius,
        "rh28_arc_resolvent_budget_lower": arc_budget,
        "center_inverse_budget_lower": center_budget,
        "stored_singular_scalar": singular,
        "floating_center_inverse_candidate": center_candidate,
        "floating_arc_inverse_candidate": arc_candidate,
        "floating_arc_budget_margin": arc_budget / arc_candidate,
        "right_vector_norm_lower": right_norm.lower,
        "right_vector_norm_upper": right_norm.upper,
        "left_vector_norm_lower": left_norm.lower,
        "left_vector_norm_upper": left_norm.upper,
        "raw_right_residual_norm_upper": raw_right,
        "raw_left_residual_norm_upper": raw_left,
        "normalized_right_residual_norm_upper": normalized.right,
        "normalized_left_residual_norm_upper": normalized.left,
        "normalization_norm_mismatch_upper": normalized.norm_mismatch,
        "lift": 1.0,
        "lifted_inverse_budget_lower": bulk_budget,
        "required_lifted_singular_lower": 1.0 / bulk_budget if bulk_budget > 0.0 else float("inf"),
        "lifted_bulk_singular_candidate": bulk_singular,
        "lifted_bulk_inverse_candidate": bulk_inverse,
        "lifted_bulk_triplet_residual": bulk_residual,
        "lifted_bulk_budget_margin": bulk_budget_margin,
        "conditional_full_inverse_candidate_bound": conditional_full,
        "conditional_arc_inverse_candidate_bound": conditional_arc,
        "final_floating_triplet_residual": float(history[-1]["triplet_residual"]),
        "maximum_primal_gmres_iterations": max(
            int(row["primal_gmres_iterations"]) for row in history
        ),
        "maximum_dual_gmres_iterations": max(
            int(row["dual_gmres_iterations"]) for row in history
        ),
        "build_seconds": build_seconds,
        "inverse_iteration_seconds": sum(float(row["seconds"]) for row in history),
        "scale_seconds": time.time() - begun,
        "triplet_file": str(triplet_path.relative_to(ROOT)),
        "triplet_sha256": source_hash(triplet_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, required=True)
    parser.add_argument("--tolerance", type=float)
    parser.add_argument("--iterations", type=int)
    parser.add_argument("--replace", action="store_true")
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    if sigma not in DEFAULT_TOLERANCES:
        raise ValueError(f"unsupported sigma={sigma:g}")
    tolerance = (
        DEFAULT_TOLERANCES[sigma]
        if arguments.tolerance is None
        else float(arguments.tolerance)
    )
    iterations = (
        DEFAULT_ITERATIONS[sigma]
        if arguments.iterations is None
        else int(arguments.iterations)
    )
    summary_path = RESULTS / "deflated_scale_summary.csv"
    rows: list[dict[str, object]] = list(read_csv(summary_path))
    if any(float(row["sigma"]) == sigma for row in rows) and not arguments.replace:
        print(f"reuse completed sigma={sigma:g}", flush=True)
        return
    rows = [row for row in rows if float(row["sigma"]) != sigma]
    rows.append(audit_scale(sigma, tolerance, iterations))
    order = {value: index for index, value in enumerate(DEFAULT_TOLERANCES)}
    rows.sort(key=lambda row: order[float(row["sigma"])])
    write_csv(summary_path, rows)
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "python_flint": flint.__version__,
        "completed_sigmas": [float(row["sigma"]) for row in rows],
        "source_hashes": {
            "run_deflated_certificate.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(ROOT / "src" / "deflated_resolvent" / "algebra.py"),
            "norms.py": source_hash(ROOT / "src" / "deflated_resolvent" / "norms.py"),
        },
        "input_hashes": {
            "rh28_arcwise_contour_arcs.csv": source_hash(
                RH28 / "results" / "arcwise_contour_arcs.csv"
            ),
        },
        "result_hashes": {
            "deflated_scale_summary.csv": source_hash(summary_path),
        },
    }
    (RESULTS / "deflated_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    row = next(row for row in rows if float(row["sigma"]) == sigma)
    print(
        f"completed sigma={sigma:g}: M_candidate={float(row['floating_arc_inverse_candidate']):.6e}, "
        f"K_lift^-={float(row['lifted_inverse_budget_lower']):.6e}",
        flush=True,
    )


if __name__ == "__main__":
    main()
