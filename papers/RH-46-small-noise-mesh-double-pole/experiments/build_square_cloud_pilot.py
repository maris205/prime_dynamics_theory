"""Convert the archived one-step resonance clouds into two-step scattering."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
sys.path.insert(0, str(ROOT / "src"))

from small_noise_two_step import (  # noqa: E402
    edge_scaled_square_section,
    ideal_cloud,
    ideal_square_section,
    square_cloud_determinant,
    universal_squared_profile,
)


SOURCE = RH15 / "results" / "outer_resonance_cloud.csv"
OUTPUT = ROOT / "results" / "two_step_square_cloud_pilot.json"
COORDINATES = (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    source_rows = read_rows(SOURCE)
    sigmas = sorted({float(row["sigma"]) for row in source_rows}, reverse=True)
    levels = {}
    ideal_identity_error = 0.0
    for sigma in sigmas:
        selected_rows = [
            row
            for row in source_rows
            if float(row["sigma"]) == sigma
            and row["positive_order"] == "selected"
        ]
        values = np.asarray(
            [
                complex(float(row["real"]), float(row["imag"]))
                for row in selected_rows
            ],
            dtype=np.complex128,
        )
        degree = values.size // 2
        if values.size != 2 * degree or degree < 1:
            raise RuntimeError(f"invalid selected cloud at sigma={sigma}")
        radial_mean = float(np.mean(np.abs(values)))
        base_w = radial_mean ** -2
        base = square_cloud_determinant(values, base_w)
        rows = []
        for coordinate in COORDINATES:
            q = np.exp(coordinate / (degree + 1))
            w = base_w * q
            observed = square_cloud_determinant(values, w) / base
            finite = edge_scaled_square_section(degree, coordinate)
            universal = universal_squared_profile(coordinate)
            rows.append(
                {
                    "coordinate": coordinate,
                    "w": float(w),
                    "observed_real": float(observed.real),
                    "observed_imag": float(observed.imag),
                    "finite_geometric_real": float(finite.real),
                    "finite_geometric_imag": float(finite.imag),
                    "universal_real": float(universal.real),
                    "universal_imag": float(universal.imag),
                    "observed_to_finite_error": float(abs(observed - finite)),
                    "observed_to_universal_error": float(
                        abs(observed - universal)
                    ),
                }
            )

        ideal = ideal_cloud(degree)
        for w in (0.1, 0.5, 1.0):
            identity_error = abs(
                square_cloud_determinant(ideal, w)
                - ideal_square_section(degree, w)
            )
            ideal_identity_error = max(ideal_identity_error, identity_error)
        levels[str(sigma)] = {
            "sigma": sigma,
            "dimension": int(selected_rows[0]["folded_dimension"]),
            "effective_degree": degree,
            "one_step_cloud_size": int(values.size),
            "radial_mean": radial_mean,
            "two_step_edge_center": base_w,
            "maximum_observed_to_finite_error": max(
                row["observed_to_finite_error"] for row in rows
            ),
            "mean_observed_to_finite_error": float(
                np.mean([row["observed_to_finite_error"] for row in rows])
            ),
            "rows": rows,
        }

    payload = {
        "status": "floating_two_step_squared_resonance_cloud_scattering_pilot",
        "evidence_level": "archived_binary64_one_step_clouds_reprocessed_exactly",
        "source": {
            "path": str(SOURCE.relative_to(REPOSITORY)),
            "sha256": sha256_file(SOURCE),
        },
        "coordinates": list(COORDINATES),
        "model": {
            "finite": "[Pi_N(exp(s/(N+1)))/(N+1)]^2",
            "universal": "[(exp(s)-1)/s]^2",
            "two_step_zero_multiplicity": 2,
        },
        "maximum_ideal_cloud_polynomial_identity_error": float(
            ideal_identity_error
        ),
        "levels": levels,
        "limitations": [
            "The source clouds are floating eigensolver selections from RH-15.",
            "Radial centering uses the arithmetic mean radius at each noise.",
            "Agreement with the squared geometric section is diagnostic and does not prove residual normality.",
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
