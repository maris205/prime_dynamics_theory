"""Build the compact RH-35 theorem and dependency archives."""

from __future__ import annotations

from fractions import Fraction
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
PAPERS = ROOT.parent
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
RH34 = PAPERS / "RH-34-interior-complement-pole-count"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    results = ROOT / "results"
    certificate_path = results / "packet_pair_certificate_sigma_1e-02.json"
    certificate = load_json(certificate_path)
    if certificate["status"] != (
        "rigorous_exact_packet_pair_correction_physical_count_one"
    ):
        raise RuntimeError("the RH-35 packet-pair certificate is not closed")
    defect_path = ROOT / str(certificate["exact_pair_defect_path"])
    ledger_path = ROOT / str(certificate["transfer_ledger"])
    if sha256_file(defect_path) != certificate["exact_pair_defect_sha256"]:
        raise RuntimeError("exact packet-defect hash mismatch")
    if sha256_file(ledger_path) != certificate["transfer_ledger_sha256"]:
        raise RuntimeError("packet-pair transfer ledger hash mismatch")

    defect = load_json(defect_path)
    entries = [
        [
            Fraction(item["numerator"], item["denominator"])
            for item in row
        ]
        for row in defect["pair_defect_entries"]
    ]
    square = sum(
        (value * value for row in entries for value in row), Fraction(0)
    )
    if not float(square) ** 0.5 <= float(
        defect["pair_defect_frobenius_upper"]
    ):
        raise RuntimeError("the exact packet-defect norm did not reverify")

    rows = read_csv(ledger_path)
    if not (
        len(rows) == 949
        and all(row["complement_homotopy_certified"] == "True" for row in rows)
        and all(row["feshbach_homotopy_certified"] == "True" for row in rows)
        and max(
            float(row["complement_neumann_product_upper"]) for row in rows
        )
        < 1.0
        and max(float(row["feshbach_rouche_product_upper"]) for row in rows)
        < 1.0
    ):
        raise RuntimeError("the leafwise transfer ledger is not closed")

    input_paths = {
        "rh28_arcwise_contour_arcs": RH28
        / "results"
        / "arcwise_contour_arcs.csv",
        "rh28_arcwise_scale_summary": RH28
        / "results"
        / "arcwise_scale_summary.csv",
        "rh33_refined_leaf_ledger": RH33
        / "results"
        / "refined_atlas_sigma_1e-02_leaves.csv",
        "rh34_summary": RH34 / "results" / "summary.json",
    }
    source_paths = {
        "rh24_physical_model": PAPERS
        / "RH-24-contour-feshbach-root-count"
        / "experiments"
        / "run_contour_feshbach_audit.py",
        "rh25_environment_builder": PAPERS
        / "RH-25-directional-rouche-closure"
        / "experiments"
        / "run_global_resolvent_probe.py",
        "rh27_componentwise_arithmetic": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "componentwise.py",
        "rh27_componentwise_factor_graph": PAPERS
        / "RH-27-outward-rounded-primal-dual-residuals"
        / "src"
        / "outward_residuals"
        / "componentwise_graph.py",
        "rh35_certificate_core": ROOT
        / "src"
        / "packet_pair"
        / "certificate.py",
        "rh35_certificate_driver": ROOT
        / "experiments"
        / "run_packet_pair_certificate.py",
        "rh35_floating_pilot": ROOT
        / "experiments"
        / "run_packet_pair_pilot.py",
        "rh35_archive_builder": ROOT / "experiments" / "build_archive.py",
        "rh35_figure_builder": ROOT / "experiments" / "make_figures.py",
        "rh35_archive_verifier": ROOT / "experiments" / "verify_archive.py",
    }
    dependency = {
        "status": "all_consumed_inputs_and_sources_hashed",
        "inputs": {
            name: {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256_file(path),
            }
            for name, path in input_paths.items()
        },
        "sources": {
            name: {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256_file(path),
            }
            for name, path in source_paths.items()
        },
    }
    dependency_path = results / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result_paths = {
        "packet_pair_certificate_sigma_1e-02.json": certificate_path,
        "exact_packet_defect_sigma_1e-02.json": defect_path,
        "packet_pair_transfer_sigma_1e-02.csv": ledger_path,
        "floating_packet_pair_sigma_1e-02.json": results
        / "floating_packet_pair_sigma_1e-02.json",
        "floating_packet_pair_sigma_1e-02.npz": results
        / "floating_packet_pair_sigma_1e-02.npz",
        "dependency_manifest.json": dependency_path,
    }
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "sigma": certificate["sigma"],
        "dimension": certificate["dimension"],
        "packet_rank": certificate["packet_rank"],
        "pair_defect_frobenius_upper": certificate["exact_pair_defect"][
            "pair_defect_frobenius_upper"
        ],
        "analysis_correction_upper": certificate["majorant"][
            "analysis_correction_upper"
        ],
        "external_correction_upper": certificate["majorant"][
            "external_correction_upper"
        ],
        "complement_correction_upper": certificate["majorant"][
            "complement_correction_upper"
        ],
        "maximum_complement_neumann_product_upper": certificate[
            "maximum_complement_neumann_product_upper"
        ],
        "maximum_feshbach_rouche_product_upper": certificate[
            "maximum_feshbach_rouche_product_upper"
        ],
        "minimum_feshbach_homotopy_denominator_lower": certificate[
            "minimum_feshbach_homotopy_denominator_lower"
        ],
        "corrected_complement_count": certificate[
            "corrected_complement_count"
        ],
        "corrected_feshbach_winding": certificate[
            "corrected_feshbach_winding"
        ],
        "zero_outside_counting_circle_exact": certificate[
            "zero_outside_counting_circle_exact"
        ],
        "physical_two_step_inside_count_certified": certificate[
            "physical_two_step_inside_count_certified"
        ],
        "physical_two_step_inside_count": certificate[
            "physical_two_step_inside_count"
        ],
        "leaf_count": len(rows),
        "result_hashes": {
            name: sha256_file(path) for name, path in result_paths.items()
        },
        "limitations": certificate["limitations"],
    }
    (results / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
