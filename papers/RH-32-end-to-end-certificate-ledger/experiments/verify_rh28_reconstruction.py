"""Verify that the RH-28 construction exactly reproduces its arc archive."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH26 = PAPERS / "RH-26-primal-dual-directional-certificate"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
sys.path[:0] = [
    str(ROOT / "src"),
    str(ROOT / "experiments"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH26 / "src"),
    str(RH26 / "experiments"),
    str(RH27 / "src"),
    str(RH28 / "src"),
    str(RH28 / "experiments"),
]

import run_arcwise_enclosure as rh28_run  # noqa: E402
import run_contour_feshbach_audit as rh24_builder  # noqa: E402
import run_directional_closure_audit as rh25_builder  # noqa: E402
from certificate_ledger import sha256_file  # noqa: E402


MODEL_STEMS = {1.0e-2: "1e-02", 4.0e-3: "4e-03", 2.0e-3: "2e-03"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def compare_snapshot(sigma: float) -> tuple[bool, list[str]]:
    data = rh25_builder.build_physical_extended_model(
        sigma, rh24_builder.physical_settings()[sigma]
    )
    model = data["model"]
    depth = int(data["base_depth"])
    snapshot = (
        ROOT
        / "results"
        / "models"
        / f"rh28_base_model_sigma_{MODEL_STEMS[sigma]}.npz"
    )
    failures = []
    with np.load(snapshot, allow_pickle=False) as archive:
        if not np.array_equal(model.reduced, archive["reduced"]):
            failures.append("reduced")
        if not np.array_equal(model.forcing_norms, archive["forcing_norms"]):
            failures.append("forcing_norms")
        for column in range(model.packet_rank):
            if not np.array_equal(
                np.asarray(model.hessenbergs[column])[: depth + 1, :depth],
                archive[f"hessenberg_{column}"],
            ):
                failures.append(f"hessenberg_{column}")
            if not np.array_equal(
                np.asarray(model.output_couplings[column])[:, :depth],
                archive[f"coupling_{column}"],
            ):
                failures.append(f"coupling_{column}")
    return not failures, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, required=True)
    parser.add_argument("--workers", type=int, default=16)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    if sigma not in MODEL_STEMS:
        raise ValueError(f"sigma={sigma:g} is not one of the RH-32 scales")

    archived_arcs = read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
    archived_scales = {
        float(row["sigma"]): row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
    }
    snapshot_equal, snapshot_failures = compare_snapshot(sigma)
    summary, rows = rh28_run.audit_scale(
        sigma,
        rh24_builder.physical_settings()[sigma],
        arc_count=64,
        maximum_refinement=14,
        workers=int(arguments.workers),
    )
    expected_rows = [row for row in archived_arcs if float(row["sigma"]) == sigma]
    deterministic_arc_fields = [
        field for field in expected_rows[0] if field != "arc_seconds"
    ]
    arc_mismatches = []
    if len(rows) != len(expected_rows):
        arc_mismatches.append(
            {
                "kind": "row_count",
                "generated": len(rows),
                "archived": len(expected_rows),
            }
        )
    for index, (generated, archived) in enumerate(zip(rows, expected_rows)):
        for field in deterministic_arc_fields:
            if str(generated[field]) != archived[field]:
                arc_mismatches.append(
                    {
                        "kind": "arc_field",
                        "row": index,
                        "field": field,
                        "generated": str(generated[field]),
                        "archived": archived[field],
                    }
                )
                if len(arc_mismatches) >= 20:
                    break
        if len(arc_mismatches) >= 20:
            break

    archived_summary = archived_scales[sigma]
    deterministic_summary_fields = [
        field for field in archived_summary if not field.endswith("seconds")
    ]
    summary_mismatches = []
    for field in deterministic_summary_fields:
        if str(summary[field]) != archived_summary[field]:
            summary_mismatches.append(
                {
                    "field": field,
                    "generated": str(summary[field]),
                    "archived": archived_summary[field],
                }
            )
    record = {
        "sigma": sigma,
        "archived_arc_count": len(expected_rows),
        "deterministic_arc_field_count": len(deterministic_arc_fields),
        "arc_mismatch_count": len(arc_mismatches),
        "arc_mismatch_examples": arc_mismatches,
        "summary_mismatch_count": len(summary_mismatches),
        "summary_mismatches": summary_mismatches,
        "snapshot_matches_fresh_rebuild_bitwise": snapshot_equal,
        "snapshot_mismatch_fields": snapshot_failures,
        "status": (
            "exact_archive_reproduction"
            if not arc_mismatches and not summary_mismatches and snapshot_equal
            else "reconstruction_mismatch"
        ),
    }
    output = ROOT / "results" / "rh28_reconstruction_verification.json"
    existing = []
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8")).get("scales", [])
    scale_records = [row for row in existing if float(row["sigma"]) != sigma]
    scale_records.append(record)
    scale_records.sort(key=lambda row: list(MODEL_STEMS).index(float(row["sigma"])))
    complete = {float(row["sigma"]) for row in scale_records} == set(MODEL_STEMS)
    passed = all(row["status"] == "exact_archive_reproduction" for row in scale_records)
    payload = {
        "status": (
            "all_deterministic_rh28_fields_exactly_reproduced"
            if complete and passed
            else (
                "partial_exact_rh28_reconstruction"
                if passed
                else "rh28_reconstruction_mismatch"
            )
        ),
        "excluded_nondeterministic_fields": [
            "arc_seconds",
            "static_certificate_seconds",
            "primal_arnoldi_seconds",
            "dual_arnoldi_seconds",
            "scale_seconds",
        ],
        "arc_archive_sha256": sha256_file(
            RH28 / "results" / "arcwise_contour_arcs.csv"
        ),
        "scale_archive_sha256": sha256_file(
            RH28 / "results" / "arcwise_scale_summary.csv"
        ),
        "scales": scale_records,
    }
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if record["status"] != "exact_archive_reproduction":
        raise RuntimeError("RH-28 reconstruction did not match the archive")


if __name__ == "__main__":
    main()
