"""Audit channel determinant identities and physical temporal transport."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH194 = PAPERS / "RH-194-physical-edge-root-matching"
sys.path.insert(0, str(ROOT / "src"))

from channel_determinant import (  # noqa: E402
    channel_transfer,
    feedback_determinant_ratio,
    modal_weighted_moments,
    power_traces,
    weighted_moments,
)


def run() -> dict[str, object]:
    rng = np.random.default_rng(199)
    identity_records = []
    for dimension in range(2, 10):
        for trial in range(30):
            matrix = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
            matrix /= 3.0 * max(1.0, np.linalg.norm(matrix, 2))
            source = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
            observation = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
            z = 1.4 + 0.7j
            transfer = channel_transfer(matrix, source, observation, z)
            ratio = feedback_determinant_ratio(matrix, source, observation, z)
            direct_moments = weighted_moments(matrix, source, observation, 8)
            values, right = np.linalg.eig(matrix)
            left_values, left_raw = np.linalg.eig(matrix.conj().T)
            residues = []
            for index, value in enumerate(values):
                left_index = int(np.argmin(abs(left_values - np.conj(value))))
                left = left_raw[:, left_index]
                left = left / np.conj(np.vdot(left, right[:, index]))
                residues.append(np.vdot(observation, right[:, index]) * np.vdot(left, source))
            modal_moments = modal_weighted_moments(values, np.asarray(residues), 8)
            trace_values = power_traces(matrix, 8)
            modal_traces = np.asarray([np.sum(values**power) for power in range(1, 9)])
            record = {
                "dimension": dimension,
                "trial": trial,
                "determinant_lemma_error": float(abs(ratio - (1.0 - transfer))),
                "weighted_moment_error": float(np.max(np.abs(direct_moments - modal_moments))),
                "power_trace_error": float(np.max(np.abs(trace_values - modal_traces))),
            }
            record["passed"] = max(
                record["determinant_lemma_error"],
                record["weighted_moment_error"],
                record["power_trace_error"],
            ) < 1e-8
            identity_records.append(record)

    physical = json.loads((RH194 / "results/physical_edge_matching.json").read_text(encoding="utf-8"))
    physical_records = []
    for window in physical["windows"]:
        physical_records.append({
            "side": str(window["side"]),
            "start": int(window["start"]),
            "relative_determinant_error": float(window["relative_determinant_error"]),
            "maximum_relative_trace_power_error": float(window["maximum_relative_trace_power_error"]),
            "maximum_root_matching_error": max(float(root["absolute_matching_error"]) for root in window["roots"]),
        })
    latest = [max((item for item in physical_records if item["side"] == side), key=lambda item: int(item["start"])) for side in ("left", "right")]
    return {
        "status": "rh199_source_channel_determinant_trace_factorization",
        "identity_case_count": len(identity_records),
        "identity_failure_count": sum(not bool(item["passed"]) for item in identity_records),
        "maximum_determinant_lemma_error": max(float(item["determinant_lemma_error"]) for item in identity_records),
        "maximum_weighted_moment_error": max(float(item["weighted_moment_error"]) for item in identity_records),
        "maximum_power_trace_error": max(float(item["power_trace_error"]) for item in identity_records),
        "physical_window_count": len(physical_records),
        "physical_maximum_relative_determinant_error": max(float(item["relative_determinant_error"]) for item in physical_records),
        "physical_maximum_relative_trace_power_error": max(float(item["maximum_relative_trace_power_error"]) for item in physical_records),
        "latest_maximum_relative_determinant_error": max(float(item["relative_determinant_error"]) for item in latest),
        "latest_maximum_relative_trace_power_error": max(float(item["maximum_relative_trace_power_error"]) for item in latest),
        "identity_records": identity_records,
        "physical_records": physical_records,
        "theorem_boundary": {
            "finite_channel_spectral_determinant": True,
            "unweighted_power_trace_identity": True,
            "residue_weighted_moment_identity": True,
            "rank_one_feedback_determinant_ratio": True,
            "finite_temporal_determinant_trace_transport": True,
            "prime_power_von_mangoldt_trace": False,
            "zeta_spectral_determinant": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/channel_determinant_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "identity_cases": payload["identity_case_count"],
        "identity_failures": payload["identity_failure_count"],
        "latest_det_error": payload["latest_maximum_relative_determinant_error"],
        "latest_trace_error": payload["latest_maximum_relative_trace_power_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
