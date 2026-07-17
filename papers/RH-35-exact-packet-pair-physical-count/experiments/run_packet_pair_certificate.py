"""Run the rigorous RH-35 exact packet-pair count-transfer certificate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
RH34 = PAPERS / "RH-34-interior-complement-pole-count"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from outward_residuals import (  # noqa: E402
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
)
from packet_pair import (  # noqa: E402
    certify_leaf_transfer,
    exact_real_gram,
    pair_correction_majorant,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def combine_frobenius_bounds(bounds: list[float]) -> float:
    total = 0.0
    for bound in bounds:
        square = np.nextafter(float(bound) * float(bound), np.inf)
        total = np.nextafter(total + square, np.inf)
    return float(np.nextafter(np.sqrt(total), np.inf))


def graph_from_environment(environment: dict[str, object]):
    spectrum = environment["spectrum"]
    return ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )


def physical_on_external_upper(
    graph: ComponentwiseStoredFactorGraph,
    *,
    chunk_size: int,
) -> tuple[float, float]:
    dimension = int(graph.matrix.shape[0])
    bounds: list[float] = []
    begun = time.perf_counter()
    for start in range(0, dimension, int(chunk_size)):
        stop = min(start + int(chunk_size), dimension)
        width = stop - start
        identity = np.zeros((dimension, width), dtype=np.float64)
        identity[np.arange(start, stop), np.arange(width)] = 1.0
        external = graph.external(ComponentwiseBall.exact(identity))
        returned = graph.two_step(external)
        bounds.append(returned.norm_upper)
        print(
            f"  certified U^2 Q columns {stop}/{dimension}: "
            f"block_F={bounds[-1]:.3e}",
            flush=True,
        )
    return combine_frobenius_bounds(bounds), time.perf_counter() - begun


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--precision", type=int, default=256)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    if sigma != 1.0e-2:
        raise ValueError("RH-35 currently certifies the sigma=1e-2 archive")
    precision = int(arguments.precision)
    settings = rh24.physical_settings()[sigma]

    total_started = time.perf_counter()
    begun = time.perf_counter()
    environment = rh25_global.build_environment(sigma, settings)
    environment_seconds = time.perf_counter() - begun
    graph = graph_from_environment(environment)
    synthesis = np.asarray(environment["synthesis"])
    analysis = np.asarray(environment["analysis"])
    dimension = int(environment["matrix"].shape[0])
    packet_rank = int(analysis.shape[0])
    print(
        f"built stored environment n={dimension}, m={packet_rank} "
        f"in {environment_seconds:.2f}s",
        flush=True,
    )

    begun = time.perf_counter()
    pair_defect = exact_real_gram(
        analysis,
        synthesis,
        subtract_identity=True,
        precision=precision,
    )
    synthesis_gram = exact_real_gram(
        synthesis.T,
        synthesis,
        precision=precision,
    )
    analysis_gram = exact_real_gram(
        analysis,
        analysis.T,
        precision=precision,
    )
    exact_gram_seconds = time.perf_counter() - begun

    begun = time.perf_counter()
    blocks = graph.build_blocks()
    physical_on_packet = graph.two_step(
        ComponentwiseBall.exact(synthesis)
    )
    small_block_seconds = time.perf_counter() - begun
    physical_external_upper, external_seconds = physical_on_external_upper(
        graph, chunk_size=int(arguments.chunk_size)
    )

    majorant = pair_correction_majorant(
        pair_defect_upper=pair_defect.frobenius_upper,
        synthesis_upper=synthesis_gram.factor_spectral_upper,
        analysis_upper=analysis_gram.factor_spectral_upper,
        physical_on_packet_upper=physical_on_packet.norm_upper,
        physical_on_external_upper=physical_external_upper,
        stored_direct_upper=blocks.direct.norm_upper,
        stored_forcing_upper=blocks.forcing.norm_upper,
        stored_observation_upper=blocks.observation.norm_upper,
        precision=precision,
    )

    parent_rows = {
        int(row["arc"]): row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == sigma
    }
    leaf_path = RH33 / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    leaf_rows = read_csv(leaf_path)
    scale_row = next(
        row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(row["sigma"]) == sigma
    )
    center_real = Fraction.from_float(
        float(scale_row["contour_center_real"])
    )
    center_imag = Fraction.from_float(
        float(scale_row["contour_center_imag"])
    )
    radius = Fraction.from_float(float(scale_row["contour_radius"]))
    zero_circle_margin = (
        center_real * center_real
        + center_imag * center_imag
        - radius * radius
    )
    zero_outside_circle = bool(zero_circle_margin > 0)
    transfer_rows: list[dict[str, object]] = []
    for leaf in leaf_rows:
        parent_arc = int(leaf["parent_arc"])
        parent = parent_rows[parent_arc]
        certificate = certify_leaf_transfer(
            majorant,
            stored_complement_inverse_upper=float(
                leaf["transported_inverse_upper"]
            ),
            projected_feshbach_inverse_upper=float(
                parent["projected_inverse_norm_upper"]
            ),
            stored_feshbach_computed_ratio_upper=float(
                parent["correction_ratio_upper"]
            ),
            stored_feshbach_remainder_coefficient_upper=float(
                parent["remainder_coefficient_upper"]
            ),
            precision=precision,
        )
        transfer_rows.append(
            {
                "parent_arc": parent_arc,
                "start_numerator": int(leaf["start_numerator"]),
                "end_numerator": int(leaf["end_numerator"]),
                "turn_denominator": int(leaf["turn_denominator"]),
                "theta_midpoint": float(leaf["theta_midpoint"]),
                "center_id": leaf["center_id"],
                **asdict(certificate),
            }
        )
    ledger_path = (
        ROOT / "results" / f"packet_pair_transfer_sigma_{sigma:.0e}.csv"
    )
    write_csv(ledger_path, transfer_rows)

    all_complement = all(
        bool(row["complement_homotopy_certified"]) for row in transfer_rows
    )
    all_feshbach = all(
        bool(row["feshbach_homotopy_certified"]) for row in transfer_rows
    )
    worst_complement = max(
        transfer_rows,
        key=lambda row: float(row["complement_neumann_product_upper"]),
    )
    worst_feshbach = max(
        transfer_rows,
        key=lambda row: float(row["feshbach_rouche_product_upper"]),
    )

    rh34_summary_path = RH34 / "results" / "summary.json"
    rh34_summary = load_json(rh34_summary_path)
    inherited = bool(
        rh34_summary["interior_complement_pole_count_certified"]
        and int(rh34_summary["interior_complement_pole_count"]) == 0
        and rh34_summary["ordinary_feshbach_zero_count_certified"]
        and int(rh34_summary["ordinary_feshbach_zero_count"]) == 1
    )
    physical_count_certified = bool(
        inherited
        and all_complement
        and all_feshbach
        and zero_outside_circle
    )
    physical_count = 1 if physical_count_certified else None
    status = (
        "rigorous_exact_packet_pair_correction_physical_count_one"
        if physical_count_certified
        else "exact_packet_pair_transfer_incomplete"
    )
    exact_pair_path = (
        ROOT / "results" / f"exact_packet_defect_sigma_{sigma:.0e}.json"
    )
    exact_pair_payload = {
        "status": "exact_dyadic_packet_gram_defect",
        "sigma": sigma,
        "packet_rank": packet_rank,
        "precision_bits_for_reported_roots": precision,
        "pair_defect_frobenius_upper": pair_defect.frobenius_upper,
        "pair_defect_spectral_upper": pair_defect.spectral_upper,
        "pair_defect_entries": pair_defect.serializable_entries(),
        "synthesis_gram_spectral_upper": synthesis_gram.spectral_upper,
        "analysis_gram_spectral_upper": analysis_gram.spectral_upper,
        "synthesis_two_norm_upper": synthesis_gram.factor_spectral_upper,
        "analysis_two_norm_upper": analysis_gram.factor_spectral_upper,
    }
    exact_pair_path.parent.mkdir(parents=True, exist_ok=True)
    exact_pair_path.write_text(
        json.dumps(exact_pair_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payload = {
        "status": status,
        "scope": (
            "exact stored Perron/parity-extracted physical two-step matrix "
            "defined by binary64 factors"
        ),
        "evidence_level": "rigorous_computer_assisted_stored_model_certificate",
        "sigma": sigma,
        "dimension": dimension,
        "packet_rank": packet_rank,
        "exact_pair_defect": exact_pair_payload,
        "majorant": asdict(majorant),
        "leaf_count": len(transfer_rows),
        "all_corrected_complement_homotopies_certified": all_complement,
        "all_corrected_feshbach_homotopies_certified": all_feshbach,
        "maximum_complement_neumann_product_upper": float(
            worst_complement["complement_neumann_product_upper"]
        ),
        "minimum_complement_homotopy_denominator_lower": min(
            float(row["complement_homotopy_denominator_lower"])
            for row in transfer_rows
        ),
        "maximum_feshbach_rouche_product_upper": float(
            worst_feshbach["feshbach_rouche_product_upper"]
        ),
        "minimum_feshbach_homotopy_denominator_lower": min(
            float(row["feshbach_homotopy_denominator_lower"])
            for row in transfer_rows
        ),
        "worst_complement_leaf": worst_complement,
        "worst_feshbach_leaf": worst_feshbach,
        "inherited_stored_complement_count": int(
            rh34_summary["interior_complement_pole_count"]
        ),
        "inherited_stored_feshbach_zero_count": int(
            rh34_summary["ordinary_feshbach_zero_count"]
        ),
        "corrected_complement_count": 0 if physical_count_certified else None,
        "corrected_feshbach_winding": 1 if physical_count_certified else None,
        "physical_two_step_inside_count_certified": physical_count_certified,
        "physical_two_step_inside_count": physical_count,
        "zero_outside_counting_circle_exact": zero_outside_circle,
        "zero_circle_squared_margin_numerator": (
            zero_circle_margin.numerator
        ),
        "zero_circle_squared_margin_denominator": (
            zero_circle_margin.denominator
        ),
        "exact_pair_defect_path": str(exact_pair_path.relative_to(ROOT)),
        "exact_pair_defect_sha256": sha256_file(exact_pair_path),
        "transfer_ledger": str(ledger_path.relative_to(ROOT)),
        "transfer_ledger_sha256": sha256_file(ledger_path),
        "rh33_leaf_ledger_sha256": sha256_file(leaf_path),
        "rh34_summary_sha256": sha256_file(rh34_summary_path),
        "environment_seconds": environment_seconds,
        "exact_gram_seconds": exact_gram_seconds,
        "small_block_certificate_seconds": small_block_seconds,
        "physical_external_certificate_seconds": external_seconds,
        "total_seconds": time.perf_counter() - total_started,
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "limitations": [
            "The theorem concerns one exact finite stored binary64 discretization.",
            "It does not enclose discretization error relative to a continuum transfer operator.",
            "It does not prove a zero-noise or dimension limit.",
            "It makes no Hilbert-Polya, zeta-zero, or Riemann-hypothesis claim.",
        ],
    }
    output = arguments.output
    if output is None:
        output = (
            ROOT / "results" / f"packet_pair_certificate_sigma_{sigma:.0e}.json"
        )
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not physical_count_certified:
        raise RuntimeError("the RH-35 physical count transfer did not close")


if __name__ == "__main__":
    main()
