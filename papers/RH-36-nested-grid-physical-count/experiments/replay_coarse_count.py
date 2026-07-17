"""Replay the RH-35 coarse physical count against the RH-36 snapshot."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import csv
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
RH35 = PAPERS / "RH-35-exact-packet-pair-physical-count"
sys.path[:0] = [
    str(RH27 / "src"),
    str(RH30 / "src"),
    str(RH35 / "src"),
    str(RH35 / "experiments"),
]

import run_packet_pair_certificate as rh35_driver  # noqa: E402
from outward_residuals import ComponentwiseBall, ComponentwiseStoredFactorGraph  # noqa: E402
from packet_pair import (  # noqa: E402
    certify_leaf_transfer,
    exact_real_gram,
    pair_correction_majorant,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def sparse_from_snapshot(data, prefix: str) -> csr_matrix:
    shape = tuple(int(value) for value in data[f"{prefix}_shape"])
    return csr_matrix(
        (
            np.asarray(data[f"{prefix}_data"]),
            np.asarray(data[f"{prefix}_indices"]),
            np.asarray(data[f"{prefix}_indptr"]),
        ),
        shape=shape,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("results/nested_grid_snapshot_sigma_1e-02.npz"),
    )
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--precision", type=int, default=256)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    snapshot = arguments.snapshot
    if not snapshot.is_absolute():
        snapshot = ROOT / snapshot
    begun = time.perf_counter()
    with np.load(snapshot) as data:
        sigma = float(data["sigma"])
        matrix = sparse_from_snapshot(data, "coarse_matrix")
        right = np.asarray(data["coarse_right_modes"])
        left = np.asarray(data["coarse_left_modes"])
        values = np.asarray(data["coarse_peripheral_values"])
        synthesis = np.asarray(data["coarse_synthesis"])
        analysis = np.asarray(data["coarse_analysis"])
        graph = ComponentwiseStoredFactorGraph(
            matrix, right, left, values, synthesis, analysis
        )

        pair_defect = exact_real_gram(
            analysis,
            synthesis,
            subtract_identity=True,
            precision=int(arguments.precision),
        )
        synthesis_gram = exact_real_gram(
            synthesis.T,
            synthesis,
            precision=int(arguments.precision),
        )
        analysis_gram = exact_real_gram(
            analysis,
            analysis.T,
            precision=int(arguments.precision),
        )
        blocks = graph.build_blocks()
        physical_on_packet = graph.two_step(
            ComponentwiseBall.exact(synthesis)
        )
        physical_external_upper, external_seconds = (
            rh35_driver.physical_on_external_upper(
                graph, chunk_size=int(arguments.chunk_size)
            )
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
        precision=int(arguments.precision),
    )
    parent_rows = {
        int(row["arc"]): row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == sigma
    }
    leaves = read_csv(
        RH33 / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    )
    transfer_rows = []
    for leaf in leaves:
        parent = parent_rows[int(leaf["parent_arc"])]
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
            precision=int(arguments.precision),
        )
        transfer_rows.append(
            {
                "parent_arc": int(leaf["parent_arc"]),
                "start_numerator": int(leaf["start_numerator"]),
                "end_numerator": int(leaf["end_numerator"]),
                "turn_denominator": int(leaf["turn_denominator"]),
                "theta_midpoint": float(leaf["theta_midpoint"]),
                "center_id": leaf["center_id"],
                **asdict(certificate),
            }
        )
    transfer_path = ROOT / "results" / "coarse_count_replay_transfer.csv"
    write_csv(transfer_path, transfer_rows)

    pair_payload = {
        "status": "exact_dyadic_packet_gram_defect",
        "sigma": sigma,
        "packet_rank": int(analysis.shape[0]),
        "precision_bits_for_reported_roots": int(arguments.precision),
        "pair_defect_frobenius_upper": pair_defect.frobenius_upper,
        "pair_defect_spectral_upper": pair_defect.spectral_upper,
        "pair_defect_entries": pair_defect.serializable_entries(),
        "synthesis_gram_spectral_upper": synthesis_gram.spectral_upper,
        "analysis_gram_spectral_upper": analysis_gram.spectral_upper,
        "synthesis_two_norm_upper": synthesis_gram.factor_spectral_upper,
        "analysis_two_norm_upper": analysis_gram.factor_spectral_upper,
    }
    pair_path = ROOT / "results" / "coarse_count_replay_pair_defect.json"
    pair_path.write_text(
        json.dumps(pair_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    inherited_path = RH35 / "results" / "packet_pair_certificate_sigma_1e-02.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    transfer_hash = sha256_file(transfer_path)
    pair_hash = sha256_file(pair_path)
    transfer_match = transfer_hash == inherited["transfer_ledger_sha256"]
    pair_match = pair_hash == inherited["exact_pair_defect_sha256"]
    count_certified = bool(
        transfer_match
        and pair_match
        and inherited["physical_two_step_inside_count_certified"]
        and int(inherited["physical_two_step_inside_count"]) == 1
    )
    payload = {
        "status": (
            "bitwise_replayed_coarse_physical_count_one"
            if count_certified
            else "coarse_physical_count_replay_mismatch"
        ),
        "sigma": sigma,
        "dimension": int(matrix.shape[0]),
        "snapshot": str(snapshot.relative_to(ROOT)),
        "snapshot_sha256": sha256_file(snapshot),
        "replayed_pair_defect": str(pair_path.relative_to(ROOT)),
        "replayed_pair_defect_sha256": pair_hash,
        "inherited_pair_defect_sha256": inherited[
            "exact_pair_defect_sha256"
        ],
        "pair_defect_hash_match": pair_match,
        "replayed_transfer_ledger": str(transfer_path.relative_to(ROOT)),
        "replayed_transfer_ledger_sha256": transfer_hash,
        "inherited_transfer_ledger_sha256": inherited[
            "transfer_ledger_sha256"
        ],
        "transfer_ledger_hash_match": transfer_match,
        "leaf_count": len(transfer_rows),
        "maximum_complement_neumann_product_upper": max(
            float(row["complement_neumann_product_upper"])
            for row in transfer_rows
        ),
        "maximum_feshbach_rouche_product_upper": max(
            float(row["feshbach_rouche_product_upper"])
            for row in transfer_rows
        ),
        "coarse_physical_inside_count_certified": count_certified,
        "coarse_physical_inside_count": 1 if count_certified else None,
        "physical_external_certificate_seconds": external_seconds,
        "total_seconds": time.perf_counter() - begun,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "coarse_count_replay.json"
    if not output.is_absolute():
        output = ROOT / output
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not count_certified:
        raise RuntimeError("the RH-35 coarse count did not replay bitwise")


if __name__ == "__main__":
    main()
