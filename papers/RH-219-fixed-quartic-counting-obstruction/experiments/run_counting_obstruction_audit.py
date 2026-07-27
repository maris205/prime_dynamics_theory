"""Illustrate the exact fixed-degree and repeated-support obstructions."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from fixed_quartic import (  # noqa: E402
    canonical_shape_roots,
    distinct_support_count,
    normalized_power_values,
    repeated_profile,
)


def run() -> dict[str, object]:
    source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    finest_sigma = min(float(row["sigma"]) for row in source["shape_rows"])
    finest = next(
        row for row in source["shape_rows"]
        if float(row["sigma"]) == finest_sigma and str(row["side"]) == "left"
    )
    roots = canonical_shape_roots(float(finest["u"]), float(finest["eta"]))
    heights = np.linspace(0.0, 1.2, 13)
    exponents = (1, 2, 4, 8, 16, 32, 64)
    profiles = repeated_profile(roots, exponents, heights)
    sample_points = np.asarray([0.0, 0.25j, 0.75j, 1.5j, 0.5 + 0.5j])
    power_rows = []
    for exponent in exponents:
        values = normalized_power_values(roots, exponent, sample_points, 2.0 + 0.0j)
        power_rows.append({
            "exponent": exponent,
            "sample_moduli": [float(abs(value)) for value in values],
            "minimum_sample_modulus": float(np.min(np.abs(values))),
            "maximum_sample_modulus": float(np.max(np.abs(values))),
        })
    # A degree-m growing synthetic cloud is included only as a structural
    # contrast: its distinct support grows because new roots are added.
    growing_rows = []
    for rank in exponents:
        synthetic = 1j * np.arange(1, rank + 1, dtype=float)
        growing_rows.append({
            "rank": rank,
            "degree": rank,
            "distinct_support_count": distinct_support_count(synthetic),
        })
    return {
        "status": "rh219_fixed_quartic_counting_obstruction",
        "source_sigma": finest_sigma,
        "source_u": float(finest["u"]),
        "source_eta": float(finest["eta"]),
        "source_root_imaginary_heights": sorted(float(abs(value.imag)) for value in roots),
        "height_grid": [float(value) for value in heights],
        "repeated_divisor_rows": profiles,
        "normalized_power_rows": power_rows,
        "growing_cloud_contrast_rows": growing_rows,
        "fixed_quartic_distinct_support": distinct_support_count(roots),
        "maximum_repeated_distinct_support": max(row["distinct_support_count"] for row in profiles),
        "maximum_repeated_degree": max(row["degree_counting_multiplicity"] for row in profiles),
        "theorem_boundary": {
            "bounded_degree_zero_count_exact": True,
            "repeated_factor_support_obstruction_exact": True,
            "diverging_compact_multiplicity_not_locally_finite": True,
            "growing_divisor_required_for_spectral_count": True,
            "growing_physical_divisor_constructed": False,
            "T_log_T_counting_law": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/counting_obstruction_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "fixed_support": payload["fixed_quartic_distinct_support"],
        "maximum_degree": payload["maximum_repeated_degree"],
        "maximum_support": payload["maximum_repeated_distinct_support"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
