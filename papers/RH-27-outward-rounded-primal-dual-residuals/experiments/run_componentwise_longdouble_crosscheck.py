"""Physical 80-bit cross-check of the componentwise outward graph."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH26 = PAPERS / "RH-26-primal-dual-directional-certificate"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH26 / "src"),
    str(RH26 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_directional_closure_audit as rh25  # noqa: E402
import run_primal_dual_audit as rh26  # noqa: E402
from directional_rouche import fom_external_solution  # noqa: E402
from outward_residuals import (  # noqa: E402
    ComponentwiseStoredFactorGraph,
    LongDoubleFactorGraph,
    ball_utilization,
)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    sigma = 1.0e-2
    node_number = 0
    begun = time.time()
    data = rh25.build_physical_extended_model(
        sigma, rh24.physical_settings()[sigma]
    )
    environment = rh26.attach_adjoint_environment(data)
    dual_model, _, _ = rh26.build_dual_arnoldi(
        environment, data["maximum_depth"]
    )
    arguments = (
        data["matrix"],
        data["spectrum"]["right_modes"],
        data["spectrum"]["left_modes"],
        data["spectrum"]["peripheral_values"],
        data["pair"].synthesis,
        data["pair"].analysis,
    )
    graph = ComponentwiseStoredFactorGraph(*arguments)
    reference_graph = LongDoubleFactorGraph(*arguments)
    blocks = graph.build_blocks()
    reference_blocks = reference_graph.build_blocks()
    _, points = rh26.contour_points(sigma)
    zeta = points[node_number]
    base = data["model"].evaluate(zeta, depth=data["base_depth"])
    base_solution = fom_external_solution(
        data["model"], zeta, depth=data["base_depth"]
    )
    deep_solution = fom_external_solution(
        data["model"], zeta, depth=data["maximum_depth"]
    )
    dual_solution = fom_external_solution(
        dual_model, np.conj(zeta), depth=data["maximum_depth"]
    )
    node = graph.node(
        blocks,
        zeta,
        base.feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    reference = reference_graph.node(
        reference_blocks,
        zeta,
        base.feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    row = {
        "sigma": sigma,
        "node": node_number,
        "longdouble_mantissa_bits": int(np.finfo(np.longdouble).nmant),
        "direct_ball_utilization": ball_utilization(
            reference_blocks.direct,
            blocks.direct.as_frobenius_ball(),
        ),
        "forcing_ball_utilization": ball_utilization(
            reference_blocks.forcing,
            blocks.forcing.as_frobenius_ball(),
        ),
        "observation_adjoint_ball_utilization": ball_utilization(
            reference_blocks.observation_adjoint,
            blocks.observation_adjoint.as_frobenius_ball(),
        ),
        "primal_residual_ball_utilization": ball_utilization(
            reference.primal_residual,
            node.primal_residual.as_frobenius_ball(),
        ),
        "dual_residual_ball_utilization": ball_utilization(
            reference.dual_residual,
            node.dual_residual.as_frobenius_ball(),
        ),
        "base_consistency_ball_utilization": ball_utilization(
            reference.base_consistency,
            node.base_consistency.as_frobenius_ball(),
        ),
        "total_correction_ball_utilization": ball_utilization(
            reference.total_computed_correction,
            node.total_computed_correction.as_frobenius_ball(),
        ),
        "elapsed_seconds": time.time() - begun,
    }
    path = RESULTS / "componentwise_longdouble_crosscheck.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "maximum_ball_utilization": max(
            float(value)
            for key, value in row.items()
            if key.endswith("_ball_utilization")
        ),
        "source_hashes": {
            "crosscheck.py": source_hash(Path(__file__)),
            "componentwise.py": source_hash(
                ROOT / "src" / "outward_residuals" / "componentwise.py"
            ),
            "componentwise_graph.py": source_hash(
                ROOT / "src" / "outward_residuals" / "componentwise_graph.py"
            ),
        },
    }
    with (RESULTS / "componentwise_longdouble_metadata.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated componentwise long-double cross-check", flush=True)


if __name__ == "__main__":
    main()
