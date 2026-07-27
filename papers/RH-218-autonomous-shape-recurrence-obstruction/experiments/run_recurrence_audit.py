"""Test simple autonomous maps on an equal-log-step dyadic subsequence."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from shape_recurrence import (  # noqa: E402
    SCALAR_MODELS,
    error_metrics,
    evaluate_polynomial_shape_map,
    fit_affine_shape_map,
    fit_scalar_recurrence,
    lagrange_autonomous_map,
)


DYADIC_SIGMAS = (0.04, 0.02, 0.01, 0.005, 0.0025, 0.00125)


def run() -> dict[str, object]:
    source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    endpoint = {(float(row["sigma"]), str(row["side"])): row for row in source["shape_rows"]}
    channel_rows = []
    all_train_current = []
    all_train_following = []
    all_holdout_current = []
    all_holdout_following = []
    for side in ("left", "right"):
        states = np.asarray([[endpoint[(sigma, side)]["u"], endpoint[(sigma, side)]["eta"]] for sigma in DYADIC_SIGMAS])
        train_current = states[:3]
        train_following = states[1:4]
        holdout_current = states[3:5]
        holdout_following = states[4:6]
        scalar_rows = []
        for model in SCALAR_MODELS:
            recurrence = fit_scalar_recurrence(model, train_current[:, 0], train_following[:, 0])
            scalar_rows.append({
                "model": model,
                "slope": recurrence.slope,
                "intercept": recurrence.intercept,
                "training_metrics": error_metrics(train_following[:, 0], recurrence(train_current[:, 0])),
                "holdout_metrics": error_metrics(holdout_following[:, 0], recurrence(holdout_current[:, 0])),
                "holdout_predictions": [float(value) for value in recurrence(holdout_current[:, 0])],
                "holdout_actual": [float(value) for value in holdout_following[:, 0]],
            })
        affine = fit_affine_shape_map(train_current, train_following)
        polynomial = lagrange_autonomous_map(states)
        polynomial_fit = evaluate_polynomial_shape_map(polynomial, states[:-1])
        channel_rows.append({
            "side": side,
            "states": [[float(value) for value in row] for row in states],
            "scalar_rows": scalar_rows,
            "best_scalar_holdout_model": min(scalar_rows, key=lambda row: row["holdout_metrics"]["rms_error"])["model"],
            "affine_matrix": affine.matrix.tolist(),
            "affine_offset": affine.offset.tolist(),
            "affine_training_metrics": error_metrics(train_following, affine(train_current)),
            "affine_holdout_metrics": error_metrics(holdout_following, affine(holdout_current)),
            "interpolating_polynomial_degree": len(polynomial[0]) - 1,
            "interpolating_polynomial_in_sample_error": error_metrics(states[1:], polynomial_fit),
        })
        all_train_current.append(train_current)
        all_train_following.append(train_following)
        all_holdout_current.append(holdout_current)
        all_holdout_following.append(holdout_following)
    pooled_affine = fit_affine_shape_map(np.vstack(all_train_current), np.vstack(all_train_following))
    pooled_training = error_metrics(np.vstack(all_train_following), pooled_affine(np.vstack(all_train_current)))
    pooled_holdout = error_metrics(np.vstack(all_holdout_following), pooled_affine(np.vstack(all_holdout_current)))
    return {
        "status": "rh218_autonomous_shape_recurrence_obstruction",
        "dyadic_sigmas": list(DYADIC_SIGMAS),
        "training_transition_count_per_channel": 3,
        "holdout_transition_count_per_channel": 2,
        "channel_rows": channel_rows,
        "pooled_affine_matrix": pooled_affine.matrix.tolist(),
        "pooled_affine_offset": pooled_affine.offset.tolist(),
        "pooled_affine_training_metrics": pooled_training,
        "pooled_affine_holdout_metrics": pooled_holdout,
        "theorem_boundary": {
            "finite_orbit_polynomial_interpolation_exact": True,
            "simple_recurrences_audited": True,
            "scale_independent_semigroup_identified": False,
            "continuous_generator_identified": False,
            "all_scale_shape_law": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/recurrence_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "left_best": payload["channel_rows"][0]["best_scalar_holdout_model"],
        "right_best": payload["channel_rows"][1]["best_scalar_holdout_model"],
        "pooled_affine_holdout": payload["pooled_affine_holdout_metrics"]["maximum_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
