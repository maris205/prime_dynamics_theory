"""Verify RH-38 hashes and independently replay the finite scaling gates."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
BLOCKS = (
    "coarse_consistency",
    "coarse_to_detail",
    "detail_to_coarse",
    "detail_block",
)
EXPONENTS = {
    "coarse_consistency": 2,
    "coarse_to_detail": 1,
    "detail_to_coarse": 1,
    "detail_block": 2,
}
TARGETS = {name: 2.0 ** (-power) for name, power in EXPONENTS.items()}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_close(actual: float, expected: float, label: str) -> None:
    if not math.isclose(float(actual), float(expected), rel_tol=2.0e-15, abs_tol=0.0):
        raise RuntimeError(f"{label} mismatch: {actual} != {expected}")


def block_uppers(record: dict[str, object]) -> dict[str, float]:
    blocks = record["block_certificates"]
    return {
        name: float(blocks[name]["block_two_norm_upper"]) for name in BLOCKS
    }


def verify_hash_ledgers() -> tuple[dict[str, object], dict[str, object]]:
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


def verify_rigorous_ledger(
    certificate: dict[str, object], dependency: dict[str, object]
) -> tuple[float, float]:
    external = dependency["external_inputs"]
    first = block_uppers(
        load(REPOSITORY / external["rh36_first_block_certificate"]["path"])
    )
    second = block_uppers(
        load(REPOSITORY / external["rh37_second_block_certificate"]["path"])
    )
    levels = certificate["rigorous_physical_levels"]
    meshes = {
        "2048_to_4096": 1.0 / 2048.0,
        "4096_to_8192": 1.0 / 4096.0,
    }
    records = {
        "2048_to_4096": first,
        "4096_to_8192": second,
    }
    source_keys = {
        "2048_to_4096": "rh36_first_block_certificate",
        "4096_to_8192": "rh37_second_block_certificate",
    }
    for level, values in records.items():
        archived = levels[level]
        source = external[source_keys[level]]
        if archived["source"] != source["path"]:
            raise RuntimeError(f"{level} source path mismatch")
        if archived["source_sha256"] != source["sha256"]:
            raise RuntimeError(f"{level} source hash mismatch")
        assert_close(archived["coarse_mesh"], meshes[level], f"{level} mesh")
        for name in BLOCKS:
            assert_close(
                archived["block_norm_uppers"][name],
                values[name],
                f"{level} {name} upper",
            )
            scaled = values[name] / meshes[level] ** EXPONENTS[name]
            assert_close(
                archived["renormalized_uppers"][name],
                scaled,
                f"{level} {name} renormalized upper",
            )

    ratios = {name: second[name] / first[name] for name in BLOCKS}
    first_scaled = {
        name: first[name] / meshes["2048_to_4096"] ** EXPONENTS[name]
        for name in BLOCKS
    }
    second_scaled = {
        name: second[name] / meshes["4096_to_8192"] ** EXPONENTS[name]
        for name in BLOCKS
    }
    spreads = {
        name: max(first_scaled[name], second_scaled[name])
        / min(first_scaled[name], second_scaled[name])
        for name in BLOCKS
    }
    for name in BLOCKS:
        assert_close(
            certificate["rigorous_upper_ratios"][name],
            ratios[name],
            f"{name} rigorous ratio",
        )
        assert_close(
            certificate["renormalized_upper_spreads"][name],
            spreads[name],
            f"{name} renormalized spread",
        )
    if max(spreads.values()) >= 1.001:
        raise RuntimeError("the rigorous renormalized ledger does not close")
    if any(ratios[name] >= TARGETS[name] + 0.001 for name in BLOCKS):
        raise RuntimeError("a rigorous finite-level ratio gate does not close")
    return max(ratios.values()), max(spreads.values())


def verify_floating_ledger(
    certificate: dict[str, object]
) -> tuple[float, int]:
    pilot = load(ROOT / "results" / "component_scaling_pilot_sigma_1e-02.json")
    if pilot["status"] != "floating_componentwise_dyadic_scaling_pilot":
        raise RuntimeError("unexpected component-pilot status")
    first = pilot["levels"]["2048_to_4096"]["components"]
    second = pilot["levels"]["4096_to_8192"]["components"]
    maximum_error = 0.0
    count = 0
    for component, archived_ratios in pilot["second_to_first_ratios"].items():
        for name in BLOCKS:
            ratio = float(second[component][name]["largest_singular_value"]) / float(
                first[component][name]["largest_singular_value"]
            )
            assert_close(
                archived_ratios[name], ratio, f"{component} {name} pilot ratio"
            )
            assert_close(
                certificate["floating_component_ratios"][component][name],
                ratio,
                f"{component} {name} certificate ratio",
            )
            maximum_error = max(maximum_error, abs(ratio - TARGETS[name]))
            count += 1
    assert_close(
        certificate["maximum_floating_ratio_error_from_exact_quarter_half"],
        maximum_error,
        "maximum floating ratio error",
    )
    if maximum_error >= 1.0e-3:
        raise RuntimeError("the floating component quarter/half gate does not close")
    return maximum_error, count


def main() -> None:
    summary, dependency = verify_hash_ledgers()
    certificate = load(
        ROOT / "results" / "dyadic_haar_block_decay_certificate.json"
    )
    expected_status = (
        "analytic_quarter_half_law_with_closed_physical_scaling_ledger"
    )
    if (
        certificate["status"] != expected_status
        or summary["status"] != expected_status
    ):
        raise RuntimeError("the final decay-certificate status is not closed")
    if not certificate["rigorous_scaling_ledger_closed"]:
        raise RuntimeError("the rigorous scaling flag is false")
    if not certificate["all_four_components_follow_quarter_half_law"]:
        raise RuntimeError("the component scaling flag is false")

    maximum_rigorous_ratio, maximum_spread = verify_rigorous_ledger(
        certificate, dependency
    )
    maximum_floating_error, component_block_count = verify_floating_ledger(
        certificate
    )

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "dyadic-haar-block-decay.pdf",
        ROOT / "figures" / "dyadic_haar_block_decay.pdf",
        ROOT / "figures" / "dyadic_haar_block_decay.png",
        ROOT / "results" / "component_scaling_pilot_sigma_1e-02.json",
        ROOT / "results" / "dyadic_haar_block_decay_certificate.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": "all_archived_hashes_and_decay_gates_verified",
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "analytic_rate_law": certificate["analytic_rate_law"],
            "rigorous_level_count": 2,
            "floating_component_block_count": component_block_count,
            "maximum_rigorous_upper_ratio": maximum_rigorous_ratio,
            "maximum_renormalized_upper_spread": maximum_spread,
            "maximum_floating_ratio_error": maximum_floating_error,
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
