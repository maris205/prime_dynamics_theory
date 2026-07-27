"""Random audit of balanced exact source-channel packets."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH195 = PAPERS / "RH-195-source-observation-riesz-channels"
sys.path[:0] = [str(ROOT / "src"), str(RH195 / "src")]

from canonical_packet import balanced_packet, determinant_trace_ledger, exact_packet_metrics  # noqa: E402
from riesz_channels import normalized_eigenprojector, source_observation_channel  # noqa: E402


def run() -> dict[str, object]:
    rng = np.random.default_rng(196)
    records = []
    for dimension in range(4, 11):
        for width in range(1, 5):
            for trial in range(5):
                values = np.linspace(-0.72, 0.78, dimension) + 0.025j * np.arange(dimension)
                similarity = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
                while np.linalg.cond(similarity) > 15.0:
                    similarity = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
                operator = similarity @ np.diag(values) @ np.linalg.inv(similarity)
                source = rng.normal(size=(dimension, width)) + 1j * rng.normal(size=(dimension, width))
                observation = rng.normal(size=(width, dimension)) + 1j * rng.normal(size=(width, dimension))
                computed, left, right = eig(operator, left=True, right=True)
                selected = np.argsort(np.abs(computed))[-4:]
                channels = []
                for index in selected:
                    projector = normalized_eigenprojector(right[:, index], left[:, index])
                    channels.append(source_observation_channel(projector, source, observation))
                right_synthesis = np.column_stack([np.asarray(item["right_state"]).reshape(-1) for item in channels])
                left_synthesis = np.column_stack([np.asarray(item["left_state"]).reshape(-1) for item in channels])
                packet = balanced_packet(right_synthesis, left_synthesis)
                metrics = exact_packet_metrics(
                    operator,
                    np.asarray(packet["right_frame"]),
                    np.asarray(packet["left_frame"]),
                    source.shape,
                )
                compressed = np.asarray(metrics["compressed"])
                expected = np.asarray(computed[selected])
                observed = np.linalg.eigvals(compressed)
                spectral_error = max(min(abs(value - candidate) for candidate in observed) for value in expected)
                ledger = determinant_trace_ledger(compressed, 8)
                trace_error = float(np.max(np.abs(np.asarray(ledger["traces"]) - np.asarray(ledger["modal_traces"]))))
                record = {
                    "dimension": dimension,
                    "width": width,
                    "trial": trial,
                    "minimum_cross_singular_value": float(packet["minimum_cross_singular_value"]),
                    "balanced_frame_norm_difference": float(abs(np.linalg.norm(packet["right_frame"], 2) - np.linalg.norm(packet["left_frame"], 2))),
                    "biorthogonality_defect": float(metrics["biorthogonality_defect"]),
                    "right_residual_norm": float(metrics["right_residual_norm"]),
                    "left_residual_norm": float(metrics["left_residual_norm"]),
                    "maximum_eigenvalue_error": float(spectral_error),
                    "maximum_newton_trace_identity_error": trace_error,
                }
                record["passed"] = max(
                    record["balanced_frame_norm_difference"],
                    record["biorthogonality_defect"],
                    record["right_residual_norm"],
                    record["left_residual_norm"],
                    record["maximum_eigenvalue_error"],
                    record["maximum_newton_trace_identity_error"],
                ) < 1e-8
                records.append(record)
    keys = [
        "balanced_frame_norm_difference",
        "biorthogonality_defect",
        "right_residual_norm",
        "left_residual_norm",
        "maximum_eigenvalue_error",
        "maximum_newton_trace_identity_error",
    ]
    return {
        "status": "rh196_canonical_biorthogonal_spectral_packet_identity_audit",
        "case_count": len(records),
        "failure_count": sum(not bool(item["passed"]) for item in records),
        "maxima": {key: max(float(item[key]) for item in records) for key in keys},
        "minimum_audited_cross_singular_value": min(float(item["minimum_cross_singular_value"]) for item in records),
        "records": records,
        "theorem_boundary": {
            "balanced_source_channel_packet": True,
            "exact_two_sided_invariance": True,
            "optimal_subspace_conditioning": True,
            "exact_packet_determinant_and_traces": True,
            "physical_uniform_transversality": False,
            "intrinsic_all_level_selection": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/canonical_packet_identity_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["case_count"],
        "failures": payload["failure_count"],
        "max_eigenvalue_error": payload["maxima"]["maximum_eigenvalue_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
