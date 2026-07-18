"""Compose the analytic-rate and stored-model scaling ledger for RH-38."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
sys.path.insert(0, str(ROOT / "src"))

from haar_decay import HaarBlockBounds, renormalized_constants  # noqa: E402


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def up(value: float) -> float:
    return float(np.nextafter(float(value), np.inf))


def block_bounds(record: dict[str, object]) -> HaarBlockBounds:
    blocks = record["block_certificates"]
    return HaarBlockBounds(
        coarse_consistency=float(
            blocks["coarse_consistency"]["block_two_norm_upper"]
        ),
        coarse_to_detail=float(
            blocks["coarse_to_detail"]["block_two_norm_upper"]
        ),
        detail_to_coarse=float(
            blocks["detail_to_coarse"]["block_two_norm_upper"]
        ),
        detail_block=float(blocks["detail_block"]["block_two_norm_upper"]),
    )


def serializable(bounds: HaarBlockBounds) -> dict[str, float]:
    return {
        "coarse_consistency": float(bounds.coarse_consistency),
        "coarse_to_detail": float(bounds.coarse_to_detail),
        "detail_to_coarse": float(bounds.detail_to_coarse),
        "detail_block": float(bounds.detail_block),
    }


def main() -> None:
    first_path = RH36 / "results" / "nested_block_certificate_sigma_1e-02.json"
    second_path = (
        RH37 / "results" / "second_dyadic_block_certificate_sigma_1e-02.json"
    )
    pilot_path = ROOT / "results" / "component_scaling_pilot_sigma_1e-02.json"
    first_record = load(first_path)
    second_record = load(second_path)
    pilot = load(pilot_path)
    first = block_bounds(first_record)
    second = block_bounds(second_record)
    first_scaled = renormalized_constants(first, 1.0 / 2048.0)
    second_scaled = renormalized_constants(second, 1.0 / 4096.0)
    names = (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    )
    exponents = {
        "coarse_consistency": 2,
        "coarse_to_detail": 1,
        "detail_to_coarse": 1,
        "detail_block": 2,
    }
    rigorous_upper_ratios = {
        name: up(getattr(second, name) / getattr(first, name)) for name in names
    }
    normalized_spreads = {
        name: up(
            max(getattr(first_scaled, name), getattr(second_scaled, name))
            / min(getattr(first_scaled, name), getattr(second_scaled, name))
        )
        for name in names
    }
    floating_ratios = pilot["second_to_first_ratios"]
    maximum_ratio_error = 0.0
    floating_exponents = {}
    for component, rows in floating_ratios.items():
        floating_exponents[component] = {}
        for name, ratio in rows.items():
            target = 2.0 ** (-exponents[name])
            maximum_ratio_error = max(maximum_ratio_error, abs(float(ratio) - target))
            floating_exponents[component][name] = float(-math.log2(float(ratio)))

    theorem_gate = bool(maximum_ratio_error < 1.0e-3)
    rigorous_gate = bool(
        max(normalized_spreads.values()) < 1.001
        and rigorous_upper_ratios["coarse_consistency"] < 0.251
        and rigorous_upper_ratios["detail_block"] < 0.251
        and rigorous_upper_ratios["coarse_to_detail"] < 0.501
        and rigorous_upper_ratios["detail_to_coarse"] < 0.501
    )
    payload = {
        "status": (
            "analytic_quarter_half_law_with_closed_physical_scaling_ledger"
            if theorem_gate and rigorous_gate
            else "dyadic_block_decay_ledger_incomplete"
        ),
        "scope": (
            "analytic C2 midpoint-kernel Haar estimates plus exact stored "
            "binary64 physical block uppers at sigma=1e-2"
        ),
        "evidence_levels": {
            "analytic_theorem": "exact inequalities proved in the manuscript",
            "physical_block_ledger": "rigorous inherited stored-binary64 uppers",
            "component_mechanism": "floating singular-value diagnostic",
        },
        "analytic_rate_law": {
            "coarse_consistency": "O(h^2)",
            "coarse_to_detail": "O(h)",
            "detail_to_coarse": "O(h)",
            "detail_block": "O(h^2)",
            "preserved_by_discrete_row_normalization": True,
            "preserved_by_smooth_finite_rank_subtraction": True,
            "preserved_by_operator_squaring": True,
        },
        "rigorous_physical_levels": {
            "2048_to_4096": {
                "coarse_mesh": 1.0 / 2048.0,
                "block_norm_uppers": serializable(first),
                "renormalized_uppers": serializable(first_scaled),
                "source": str(first_path.relative_to(REPOSITORY)),
                "source_sha256": sha256_file(first_path),
            },
            "4096_to_8192": {
                "coarse_mesh": 1.0 / 4096.0,
                "block_norm_uppers": serializable(second),
                "renormalized_uppers": serializable(second_scaled),
                "source": str(second_path.relative_to(REPOSITORY)),
                "source_sha256": sha256_file(second_path),
            },
        },
        "rigorous_upper_ratios": rigorous_upper_ratios,
        "renormalized_upper_spreads": normalized_spreads,
        "rigorous_scaling_ledger_closed": rigorous_gate,
        "floating_component_ratios": floating_ratios,
        "floating_component_effective_exponents": floating_exponents,
        "maximum_floating_ratio_error_from_exact_quarter_half": (
            maximum_ratio_error
        ),
        "all_four_components_follow_quarter_half_law": theorem_gate,
        "component_pilot": {
            "path": str(pilot_path.relative_to(ROOT)),
            "sha256": sha256_file(pilot_path),
        },
        "limitations": [
            "The analytic theorem applies directly to full smooth midpoint kernels.",
            "The stored matrices use an eight-sigma hard cutoff whose uniform tail defect is not enclosed here.",
            "Uniform convergence of the computed peripheral projectors to a smooth continuum projector is not certified here.",
            "Two rigorous physical refinement levels do not establish an all-level uniform constant.",
            "Block decay alone does not control the hierarchical nonnormal resolvent recursion.",
            "No zero-noise, zeta-zero, Hilbert-Polya, or Riemann-hypothesis claim is made.",
        ],
    }
    output = ROOT / "results" / "dyadic_haar_block_decay_certificate.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if payload["status"] != "analytic_quarter_half_law_with_closed_physical_scaling_ledger":
        raise RuntimeError("the dyadic scaling ledger did not close")


if __name__ == "__main__":
    main()
