"""Verify RH-39 hashes, formulas, Arb uppers, and schedule gates."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cutoff_bridge import (  # noqa: E402
    adaptive_cutoff_multiple,
    cutoff_bound,
    haar_cutoff_defect,
    support_half_width,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_close(actual: float, expected: float, label: str) -> None:
    if not math.isclose(float(actual), float(expected), rel_tol=3.0e-15, abs_tol=0.0):
        raise RuntimeError(f"{label} mismatch: {actual} != {expected}")


def verify_hashes() -> tuple[dict[str, object], dict[str, object]]:
    summary = load(ROOT / "results" / "summary.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external input mismatch: {path}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"local source mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication artifact mismatch: {relative}")
    return summary, dependency


def verify_fixed_levels(certificate: dict[str, object]) -> dict[int, object]:
    bounds = {}
    for dimension in (2048, 4096, 8192):
        calculated = cutoff_bound(dimension, 0.01, 8.0)
        archived = certificate["fixed_eight_sigma_levels"][str(dimension)]
        if archived["support_half_width"] != support_half_width(
            dimension, 0.01, 8.0
        ):
            raise RuntimeError(f"support half-width mismatch at {dimension}")
        assert_close(
            archived["effective_support_multiple"],
            calculated.effective_multiple,
            f"effective multiple at {dimension}",
        )
        if float(archived["omitted_mass_upper"]) < calculated.omitted_mass_upper:
            raise RuntimeError(f"Arb omitted-mass upper is too small at {dimension}")
        if float(archived["two_norm_upper"]) < calculated.two_norm_upper:
            raise RuntimeError(f"Arb two-norm upper is too small at {dimension}")
        if (
            float(archived["two_norm_upper"]) / calculated.two_norm_upper
            > 1.0 + 5.0e-15
        ):
            raise RuntimeError(f"Arb two-norm upper is unexpectedly loose at {dimension}")
        bounds[dimension] = calculated
    return bounds


def verify_haar_ledger(
    certificate: dict[str, object], bounds: dict[int, object]
) -> None:
    ledgers = {
        "2048_to_4096": haar_cutoff_defect(bounds[2048], bounds[4096]),
        "4096_to_8192": haar_cutoff_defect(bounds[4096], bounds[8192]),
    }
    for level, calculated in ledgers.items():
        archived = certificate["haar_cutoff_defect_uppers"][level]
        for name, value in calculated.__dict__.items():
            assert_close(archived[name], value, f"{level} {name}")


def verify_pilot(certificate: dict[str, object]) -> None:
    pilot = load(ROOT / "results" / "cutoff_pilot_sigma_1e-02.json")
    if pilot["status"] != "floating_full_versus_archived_cutoff_pilot":
        raise RuntimeError("unexpected pilot status")
    for row in pilot["dimensions"]:
        if float(row["tail_identity_maximum_error"]) >= 1.0e-28:
            raise RuntimeError("the floating twice-tail identity did not close")
        if float(row["maximum_omitted_mass"]) >= float(
            row["analytic_omitted_mass_upper"]
        ):
            raise RuntimeError("a floating omitted mass exceeds its analytic upper")
        if float(row["frobenius_norm"]) >= float(row["analytic_two_norm_upper"]):
            raise RuntimeError("a floating Frobenius norm exceeds its analytic upper")
    if certificate["maximum_cutoff_upper_over_floating_markov_block"] >= 4.0e-9:
        raise RuntimeError("the stored-grid relative cutoff gate did not close")


def verify_schedule(certificate: dict[str, object]) -> None:
    crossover = int(math.floor(math.exp(16.0)))
    if certificate["schedule"]["eight_sigma_crossover_dimension_floor"] != crossover:
        raise RuntimeError("the eight-sigma crossover dimension is incorrect")
    ratios = []
    for dimension in (1024, 4096, 16384, 65536, 262144, 1048576):
        h = 1.0 / dimension
        multiple = adaptive_cutoff_multiple(h)
        ratios.append(cutoff_bound(dimension, 0.01, multiple).two_norm_upper / h**2)
    if max(ratios) >= 20.0:
        raise RuntimeError("the sampled adaptive second-order ledger did not close")
    limit = certificate["fixed_eight_sigma_nonvanishing_limit"]
    if float(limit["mean_zero_continuum_omitted_mass_lower"]) <= 0.0:
        raise RuntimeError("the fixed-window lower tail is not positive")


def main() -> None:
    summary, dependency = verify_hashes()
    certificate = load(
        ROOT / "results" / "uniform_gaussian_cutoff_bridge_certificate.json"
    )
    expected_status = (
        "analytic_uniform_cutoff_bridge_with_arb_finite_grid_enclosures"
    )
    if certificate["status"] != expected_status or summary["status"] != expected_status:
        raise RuntimeError("the final cutoff certificate status is not closed")
    for name, record in certificate["dependencies"].items():
        if record != dependency["external_inputs"][name]:
            raise RuntimeError(f"certificate dependency mismatch: {name}")

    bounds = verify_fixed_levels(certificate)
    verify_haar_ledger(certificate, bounds)
    verify_pilot(certificate)
    verify_schedule(certificate)

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "uniform-gaussian-cutoff-bridge.pdf",
        ROOT / "figures" / "uniform_gaussian_cutoff_bridge.pdf",
        ROOT / "figures" / "uniform_gaussian_cutoff_bridge.png",
        ROOT / "results" / "cutoff_pilot_sigma_1e-02.json",
        ROOT / "results" / "uniform_gaussian_cutoff_bridge_certificate.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": "all_archived_hashes_cutoff_bounds_and_schedule_gates_verified",
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "arb_fixed_grid_count": 3,
            "maximum_fixed_eight_sigma_two_norm_upper": max(
                bound.two_norm_upper for bound in bounds.values()
            ),
            "maximum_relative_markov_block_ratio": certificate[
                "maximum_cutoff_upper_over_floating_markov_block"
            ],
            "fixed_continuum_tail_positive": True,
            "adaptive_schedule_sampled_second_order": True,
            "eight_sigma_crossover_dimension_floor": certificate["schedule"][
                "eight_sigma_crossover_dimension_floor"
            ],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
