"""Verify principal RH-31 certificate archives and their provenance hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CERTIFICATES = (
    RESULTS / "exact_target_inertia_sigma_1e-2_op24.json",
    RESULTS / "exact_target_inertia_sigma_4e-3_op24.json",
    RESULTS / "exact_target_inertia_sigma_2e-3.json",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_derived_source(data: dict[str, object]) -> list[dict[str, str]]:
    verified: list[dict[str, str]] = []
    derived = data.get("derived_from")
    if isinstance(derived, dict):
        path = ROOT / str(derived["path"])
        actual = digest(path)
        if actual != str(derived["sha256"]):
            raise ValueError(f"derived source hash mismatch: {path}")
        verified.append({"path": str(path.relative_to(ROOT)), "sha256": actual})
    sources = data.get("source_results")
    if isinstance(sources, dict):
        for source in sources.values():
            path = ROOT / str(source["path"])
            actual = digest(path)
            if actual != str(source["sha256"]):
                raise ValueError(f"combined source hash mismatch: {path}")
            verified.append(
                {"path": str(path.relative_to(ROOT)), "sha256": actual}
            )
    return verified


def main() -> None:
    certificate_rows = []
    provenance = []
    for path in CERTIFICATES:
        data = json.loads(path.read_text(encoding="utf-8"))
        bracket = data["inertia_bracket"]
        dimension = int(data["grushin_dimension"])
        if data["status"] != (
            "rigorous_exact_target_asymmetric_threshold_inertia_certificate"
        ):
            raise ValueError(f"certificate status failed: {path}")
        if not bool(bracket["admissible"]):
            raise ValueError(f"inertia bracket failed: {path}")
        if (
            int(bracket["positive_count"]),
            int(bracket["negative_count"]),
        ) != (dimension, dimension):
            raise ValueError(f"inertia count failed: {path}")
        if not (
            float(bracket["lower_shift_error_upper"])
            < float(bracket["lower_shift"])
            and float(bracket["upper_shift_error_upper"])
            < float(bracket["upper_shift"])
        ):
            raise ValueError(f"shift error failed: {path}")
        for factor in data["shifted_factorizations"]:
            if not (
                factor["row_permutation_is_identity"]
                and factor["column_permutation_is_identity"]
            ):
                raise ValueError(f"nonidentity factor permutation: {path}")
            if int(
                factor["backward_error"]["elimination_operation_factor"]
            ) != 24:
                raise ValueError(f"operation factor mismatch: {path}")
        certificate_rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": digest(path),
                "sigma": float(data["sigma"]),
                "grushin_dimension": dimension,
                "lower_utilization": float(
                    bracket["lower_shift_error_upper"]
                )
                / float(bracket["lower_shift"]),
                "upper_utilization": float(
                    bracket["upper_shift_error_upper"]
                )
                / float(bracket["upper_shift"]),
            }
        )
        provenance.extend(verify_derived_source(data))

    summary_path = RESULTS / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for relative, expected in summary["source_hashes"].items():
        actual = digest(ROOT / relative)
        if actual != expected:
            raise ValueError(f"summary source hash mismatch: {relative}")

    code_paths = (
        ROOT / "experiments" / "enclosed_grushin.py",
        ROOT / "experiments" / "run_inertia_pilot.py",
        ROOT / "experiments" / "combine_asymmetric_bracket.py",
        ROOT / "experiments" / "rebound_archived_factorization.py",
        ROOT / "experiments" / "make_summary.py",
        ROOT / "src" / "threshold_inertia" / "rounding.py",
        ROOT / "src" / "threshold_inertia" / "transforms.py",
        ROOT / "tests" / "test_threshold_inertia.py",
        ROOT / "tests" / "test_archived_results.py",
        ROOT / "main.tex",
        ROOT / "references.bib",
    )
    result = {
        "status": "verified",
        "certificates": certificate_rows,
        "provenance_sources": provenance,
        "summary": {
            "path": str(summary_path.relative_to(ROOT)),
            "sha256": digest(summary_path),
        },
        "code_hashes": {
            str(path.relative_to(ROOT)): digest(path) for path in code_paths
        },
    }
    manuscript = ROOT / "sparse-threshold-inertia.pdf"
    if manuscript.exists():
        result["manuscript"] = {
            "path": str(manuscript.relative_to(ROOT)),
            "sha256": digest(manuscript),
        }
    output = RESULTS / "archive_verification.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
