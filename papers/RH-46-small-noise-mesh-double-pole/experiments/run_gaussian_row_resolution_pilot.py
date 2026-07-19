"""Exact floating projection pilot for a normalized Gaussian row on R."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.special import ndtr


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from small_noise_two_step import gaussian_row_asymptotic_constant  # noqa: E402


OUTPUT = ROOT / "results" / "gaussian_row_projection_pilot.json"
CELL_RATIOS = tuple(2.0 ** (-power) for power in range(1, 10))
PHASES = (0.0, 0.25, 0.5, 0.75)


def projection_error(cell_ratio: float, phase: float) -> float:
    """Return the sigma=1 error; scale invariance handles general sigma."""

    width = float(cell_ratio)
    offset = float(phase)
    cutoff = 12.0
    lower_index = math.floor(-cutoff / width - offset) - 1
    upper_index = math.ceil(cutoff / width - offset) + 1
    indices = np.arange(lower_index, upper_index + 1, dtype=np.float64)
    lower = (indices + offset) * width
    upper = lower + width
    masses = ndtr(upper) - ndtr(lower)
    projection_energy = float(np.sum(masses * masses) / width)
    exact_energy = 1.0 / (2.0 * math.sqrt(math.pi))
    return math.sqrt(max(0.0, exact_energy - projection_energy))


def main() -> None:
    constant = gaussian_row_asymptotic_constant()
    rows = []
    for ratio in CELL_RATIOS:
        errors = [projection_error(ratio, phase) for phase in PHASES]
        mean_error = float(np.mean(errors))
        rows.append(
            {
                "cell_to_sigma_ratio": ratio,
                "phase_errors": errors,
                "mean_scaled_error": mean_error,
                "mean_error_divided_by_cell_ratio": mean_error / ratio,
                "relative_error_to_asymptotic_constant": abs(
                    mean_error / ratio - constant
                )
                / constant,
            }
        )
    payload = {
        "status": "floating_exact_gaussian_row_cell_projection_pilot",
        "evidence_level": "closed_normal_cdf_cell_masses_binary64",
        "scaling_identity": (
            "error(sigma,h)=sigma^(-1/2) error(1,h/sigma)"
        ),
        "asymptotic_law": (
            "error(sigma,h)~C h sigma^(-3/2) when h/sigma->0"
        ),
        "asymptotic_constant": constant,
        "phases": list(PHASES),
        "rows": rows,
        "finest_relative_error": rows[-1][
            "relative_error_to_asymptotic_constant"
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
