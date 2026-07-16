"""Merge completed rank-one-lift diagnostics into the certificate table."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "experiments")]

from deflated_resolvent import candidate_arc_inverse, lifted_full_inverse_upper  # noqa: E402
from run_deflated_certificate import lift_diagnostic, read_csv, write_csv  # noqa: E402


def main() -> None:
    path = ROOT / "results" / "deflated_scale_summary.csv"
    rows = read_csv(path)
    if not rows:
        raise RuntimeError("the deflated scale summary is absent")
    for row in rows:
        sigma = float(row["sigma"])
        bulk_singular, bulk_inverse, bulk_residual = lift_diagnostic(sigma)
        bulk_budget = float(row["lifted_inverse_budget_lower"])
        full = lifted_full_inverse_upper(
            bulk_inverse,
            float(row["stored_singular_scalar"]),
            float(row["normalized_right_residual_norm_upper"]),
            float(row["normalized_left_residual_norm_upper"]),
        ).full_inverse_upper
        arc = candidate_arc_inverse(full, float(row["arc_disc_radius"]))
        row["lifted_bulk_singular_candidate"] = bulk_singular
        row["lifted_bulk_inverse_candidate"] = bulk_inverse
        row["lifted_bulk_triplet_residual"] = bulk_residual
        row["lifted_bulk_budget_margin"] = bulk_budget / bulk_inverse
        row["conditional_full_inverse_candidate_bound"] = full
        row["conditional_arc_inverse_candidate_bound"] = arc
    write_csv(path, rows)


if __name__ == "__main__":
    main()
