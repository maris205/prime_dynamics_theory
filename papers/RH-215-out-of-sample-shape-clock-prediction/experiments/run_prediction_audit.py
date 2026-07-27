"""Blindly score three predeclared axial-clock extrapolants."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from shape_prediction import MODEL_NAMES, constant_prediction, fit_clock, prediction_metrics  # noqa: E402


TRAIN_SIGMAS = np.asarray((0.008, 0.00625, 0.005, 0.004, 0.0032, 0.0025, 0.002))
HOLDOUT_SIGMAS = np.asarray((0.0016, 0.00125))


def run() -> dict[str, object]:
    source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    endpoint = {(float(row["sigma"]), str(row["side"])): row for row in source["shape_rows"]}
    channel_rows = []
    for side in ("left", "right"):
        train_u = np.asarray([endpoint[(float(sigma), side)]["u"] for sigma in TRAIN_SIGMAS])
        holdout_u = np.asarray([endpoint[(float(sigma), side)]["u"] for sigma in HOLDOUT_SIGMAS])
        train_eta = np.asarray([endpoint[(float(sigma), side)]["eta"] for sigma in TRAIN_SIGMAS])
        holdout_eta = np.asarray([endpoint[(float(sigma), side)]["eta"] for sigma in HOLDOUT_SIGMAS])
        model_rows = []
        for model in MODEL_NAMES:
            fit = fit_clock(model, TRAIN_SIGMAS, train_u)
            train_prediction = fit.predict(TRAIN_SIGMAS)
            holdout_prediction = fit.predict(HOLDOUT_SIGMAS)
            model_rows.append({
                "model": model,
                "slope": fit.slope,
                "intercept": fit.intercept,
                "training_metrics": prediction_metrics(train_u, train_prediction),
                "holdout_metrics": prediction_metrics(holdout_u, holdout_prediction),
                "holdout_predictions": [float(value) for value in holdout_prediction],
                "holdout_actual": [float(value) for value in holdout_u],
                "pointwise_holdout_absolute_errors": [float(value) for value in np.abs(holdout_prediction - holdout_u)],
            })
        eta_prediction = constant_prediction(train_eta)
        channel_rows.append({
            "side": side,
            "training_u": [float(value) for value in train_u],
            "holdout_u": [float(value) for value in holdout_u],
            "model_rows": model_rows,
            "best_model_at_sigma_0_0016": min(model_rows, key=lambda row: row["pointwise_holdout_absolute_errors"][0])["model"],
            "best_model_at_sigma_0_00125": min(model_rows, key=lambda row: row["pointwise_holdout_absolute_errors"][1])["model"],
            "best_two_point_holdout_model": min(model_rows, key=lambda row: row["holdout_metrics"]["root_mean_square_error"])["model"],
            "constant_eta_prediction": eta_prediction,
            "holdout_eta": [float(value) for value in holdout_eta],
            "constant_eta_maximum_absolute_error": float(np.max(np.abs(holdout_eta - eta_prediction))),
        })
    return {
        "status": "rh215_out_of_sample_shape_clock_prediction",
        "training_sigmas": [float(value) for value in TRAIN_SIGMAS],
        "holdout_sigmas": [float(value) for value in HOLDOUT_SIGMAS],
        "channel_rows": channel_rows,
        "same_winner_both_channels": (
            channel_rows[0]["best_two_point_holdout_model"] == channel_rows[1]["best_two_point_holdout_model"]
        ),
        "theorem_boundary": {
            "models_predeclared": True,
            "two_point_out_of_sample_audit": True,
            "power_gap_wins_finite_holdout": all(
                row["best_two_point_holdout_model"] == "power_gap" for row in channel_rows
            ),
            "asymptotic_law_identified": False,
            "limit_u_equals_one": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/prediction_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "left_winner": payload["channel_rows"][0]["best_two_point_holdout_model"],
        "right_winner": payload["channel_rows"][1]["best_two_point_holdout_model"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
