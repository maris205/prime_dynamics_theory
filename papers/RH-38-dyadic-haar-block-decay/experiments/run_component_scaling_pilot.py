"""Resolve dyadic Haar block scaling for P, Q, U=P-Q, and A=U^2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"


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


def factors_from_snapshot(data, prefix: str) -> dict[str, np.ndarray | csr_matrix]:
    return {
        "matrix": sparse_from_snapshot(data, f"{prefix}_matrix"),
        "right": np.asarray(data[f"{prefix}_right_modes"]),
        "left": np.asarray(data[f"{prefix}_left_modes"]),
        "values": np.asarray(data[f"{prefix}_peripheral_values"]),
    }


def component_actions(factors, component: str):
    matrix = factors["matrix"]
    right = np.asarray(factors["right"])
    left = np.asarray(factors["left"])
    values = np.asarray(factors["values"])
    weighted_right = right * values[None, :]

    def p(source):
        return matrix @ np.asarray(source)

    def pt(source):
        return matrix.T @ np.asarray(source)

    def q(source):
        array = np.asarray(source)
        return weighted_right @ (left.T @ array)

    def qt(source):
        array = np.asarray(source)
        return left @ (weighted_right.T @ array)

    def u(source):
        return p(source) - q(source)

    def ut(source):
        return pt(source) - qt(source)

    if component == "markov":
        return p, pt
    if component == "peripheral":
        return q, qt
    if component == "bulk_one_step":
        return u, ut
    if component == "physical_two_step":
        return lambda x: u(u(x)), lambda x: ut(ut(x))
    raise ValueError(component)


def prolong(source):
    return np.repeat(np.asarray(source), 2, axis=0)


def detail_injection(source):
    array = np.asarray(source)
    result = np.empty((2 * array.shape[0],) + array.shape[1:], dtype=array.dtype)
    result[0::2] = array
    result[1::2] = -array
    return result


def restrict(source):
    array = np.asarray(source)
    return 0.5 * (array[0::2] + array[1::2])


def detail_restriction(source):
    array = np.asarray(source)
    return 0.5 * (array[0::2] - array[1::2])


def block_actions(name, coarse, coarse_adjoint, fine, fine_adjoint):
    if name == "coarse_consistency":
        return (
            lambda x: restrict(fine(prolong(x))) - coarse(x),
            lambda x: restrict(fine_adjoint(prolong(x))) - coarse_adjoint(x),
        )
    if name == "coarse_to_detail":
        return (
            lambda x: detail_restriction(fine(prolong(x))),
            lambda x: restrict(fine_adjoint(detail_injection(x))),
        )
    if name == "detail_to_coarse":
        return (
            lambda x: restrict(fine(detail_injection(x))),
            lambda x: detail_restriction(fine_adjoint(prolong(x))),
        )
    if name == "detail_block":
        return (
            lambda x: detail_restriction(fine(detail_injection(x))),
            lambda x: detail_restriction(fine_adjoint(detail_injection(x))),
        )
    raise ValueError(name)


def leading_singular_values(dimension: int, action, adjoint, rank: int):
    operator = LinearOperator(
        (dimension, dimension),
        matvec=action,
        rmatvec=adjoint,
        dtype=np.float64,
    )
    values = svds(
        operator,
        k=int(rank),
        which="LM",
        return_singular_vectors=False,
        tol=1.0e-10,
        maxiter=10000,
        random_state=57721,
    )
    return np.sort(values)[::-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", type=int, default=6)
    arguments = parser.parse_args()
    inherited = RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    fine_object = (
        RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
    )
    with np.load(inherited) as data:
        level_zero = factors_from_snapshot(data, "coarse")
        level_one = factors_from_snapshot(data, "fine")
    with np.load(fine_object) as data:
        level_two = factors_from_snapshot(data, "fine")

    levels = [
        ("2048_to_4096", level_zero, level_one),
        ("4096_to_8192", level_one, level_two),
    ]
    components = (
        "markov",
        "peripheral",
        "bulk_one_step",
        "physical_two_step",
    )
    blocks = (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    )
    payload = {
        "status": "floating_componentwise_dyadic_scaling_pilot",
        "evidence_level": "floating_not_validated",
        "sigma": 1.0e-2,
        "svd_rank": int(arguments.rank),
        "levels": {},
    }
    for label, coarse_factors, fine_factors in levels:
        dimension = int(coarse_factors["matrix"].shape[0])
        level_payload = {
            "coarse_dimension": dimension,
            "fine_dimension": 2 * dimension,
            "components": {},
        }
        for component in components:
            coarse, coarse_adjoint = component_actions(coarse_factors, component)
            fine, fine_adjoint = component_actions(fine_factors, component)
            component_payload = {}
            for block in blocks:
                action, adjoint = block_actions(
                    block, coarse, coarse_adjoint, fine, fine_adjoint
                )
                begun = time.perf_counter()
                singular_values = leading_singular_values(
                    dimension, action, adjoint, int(arguments.rank)
                )
                component_payload[block] = {
                    "leading_singular_values": [
                        float(value) for value in singular_values
                    ],
                    "largest_singular_value": float(singular_values[0]),
                    "seconds": time.perf_counter() - begun,
                }
                print(
                    f"{label} {component} {block}: "
                    f"{singular_values[0]:.16e}",
                    flush=True,
                )
            level_payload["components"][component] = component_payload
        payload["levels"][label] = level_payload

    first = payload["levels"]["2048_to_4096"]["components"]
    second = payload["levels"]["4096_to_8192"]["components"]
    payload["second_to_first_ratios"] = {
        component: {
            block: (
                second[component][block]["largest_singular_value"]
                / first[component][block]["largest_singular_value"]
            )
            for block in blocks
        }
        for component in components
    }
    output = ROOT / "results" / "component_scaling_pilot_sigma_1e-02.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["second_to_first_ratios"], indent=2), flush=True)


if __name__ == "__main__":
    main()
