"""Certify stored Perron circles at dimensions 2048, 4096, and 8192."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"
ENGINE_PATH = RH43 / "experiments" / "run_multilevel_euclidean_grushin.py"
SNAPSHOT_36 = (
    RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
)
SNAPSHOT_37 = (
    RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
)
OUTPUT = ROOT / "results" / "multilevel_perron_grushin.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def load_engine():
    specification = importlib.util.spec_from_file_location(
        "rh43_multilevel_grushin", ENGINE_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the RH-43 Grushin engine")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--levels", default="2048,4096,8192", help="comma-separated levels"
    )
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--radius", type=float, default=0.05)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    if not 0.0 < arguments.radius < 1.0:
        raise ValueError("the Perron radius must lie in (0,1)")

    engine = load_engine()
    original_load_level = engine.load_level

    def load_perron_level(dimension: int) -> dict[str, object]:
        level = original_load_level(dimension)
        with np.load(level["snapshot"]) as data:
            prefix = str(level["prefix"])
            level["right"] = np.asarray(
                data[f"{prefix}_right_modes"][:, 0], dtype=np.float64
            )
            level["left"] = np.asarray(
                data[f"{prefix}_left_modes"][:, 0], dtype=np.float64
            )
            level["eigenvalue"] = float(
                data[f"{prefix}_peripheral_values"][0]
            )
        return level

    engine.load_level = load_perron_level
    engine.CONTOUR_RADIUS = float(arguments.radius)
    levels = tuple(
        int(value.strip())
        for value in arguments.levels.split(",")
        if value.strip()
    )
    rows = {
        str(dimension): engine.certify_level(dimension, arguments.chunk_size)
        for dimension in levels
    }
    all_closed = all(
        row["status"]
        == "rigorous_exact_stored_euclidean_parity_circle_count_one"
        for row in rows.values()
    )
    for row in rows.values():
        row["status"] = (
            "rigorous_exact_stored_euclidean_perron_circle_count_one"
            if row["status"]
            == "rigorous_exact_stored_euclidean_parity_circle_count_one"
            else "stored_euclidean_perron_grushin_circle_not_closed"
        )
    payload = {
        "status": (
            "rigorous_multilevel_exact_stored_euclidean_perron_factors"
            if all_closed
            else "multilevel_exact_stored_perron_factor_gate_not_closed"
        ),
        "scope": (
            "exact stored binary64 Perron factors at dimensions "
            "2048, 4096, and 8192"
        ),
        "evidence_level": (
            "componentwise_outward_binary64_bordered_inverse_certificates"
        ),
        "contour_radius": float(arguments.radius),
        "levels": rows,
        "dependencies": {
            "rh36_snapshot": repository_entry(SNAPSHOT_36),
            "rh37_snapshot": repository_entry(SNAPSHOT_37),
            "rh43_multilevel_grushin_engine": repository_entry(ENGINE_PATH),
        },
        "source_sha256": sha256_file(Path(__file__)),
        "limitations": [
            "Each contour is centered at its stored binary64 Perron eigenvalue approximation.",
            "The result validates the stored matrices and factors, not every future binary64 Gaussian rebuild.",
        ],
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not all_closed:
        raise RuntimeError("at least one multilevel Perron Grushin gate failed")


if __name__ == "__main__":
    main()
