"""Verify RH-53 hashes, theorem boundaries, and numerical gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_hashes(summary, dependency) -> None:
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
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


def verify_theory(certificate) -> None:
    expected = (
        "rigorous_deterministic_block_tail_and_adaptive_exact_real_cutoff_"
        "route_with_production_interval_gap"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    main = certificate["deterministic_main_sum"]
    if "no Hutchinson" not in main["algorithm"]:
        raise RuntimeError("Hutchinson replacement was lost")
    tail = certificate["infinite_tail_theorem"]
    if "q_M=||A^M||_2<1" not in tail["condition"]:
        raise RuntimeError("block contraction condition mismatch")
    if "1-q_M^2" not in tail["stein_tail"]:
        raise RuntimeError("Stein tail formula mismatch")
    cutoff = certificate["cutoff_result"]
    if "strictly positive" not in cutoff["fixed_window_no_go"]:
        raise RuntimeError("fixed-window no-go missing")
    if "2 sqrt(log(1/h))" not in cutoff["adaptive_schedule"]:
        raise RuntimeError("adaptive schedule mismatch")
    conclusion = certificate["program_conclusion"]
    if not conclusion["deterministic_finite_matrix_tail_mechanism_closed"]:
        raise RuntimeError("finite tail mechanism was not closed")
    if not conclusion["adaptive_exact_real_cutoff_route_closed"]:
        raise RuntimeError("adaptive cutoff route was not closed")
    for gate in (
        "fixed_eight_is_canonical_joint_limit",
        "production_scale_interval_trace_executed",
        "intrinsic_factor_cutoff_transfer_executed",
        "stage_A3_fully_closed",
        "stage_A1_uniform_trace_budget_closed",
        "stage_A4_intrinsic_identification_closed",
    ):
        if conclusion[gate]:
            raise RuntimeError(f"theorem boundary overclaimed: {gate}")


def verify_numerics(certificate) -> None:
    audit = certificate["floating_five_scale_audit"]
    if audit["noise_levels"] != 5 or audit["largest_dimension"] != 512:
        raise RuntimeError("five-scale dimensions mismatch")
    if audit["maximum_relative_energy_excess"] >= 5.0e-4:
        raise RuntimeError("deterministic tail excess gate failed")
    if not audit["all_column_deterministic"]:
        raise RuntimeError("all-column mechanism missing")
    if audit["hutchinson_probes_used"] or audit["interval_validated"]:
        raise RuntimeError("floating evidence was misclassified")
    for row in audit["rows"]:
        for side in ("left", "right"):
            data = row[side]
            if data["full_energy_upper"] < data["exact_dense_energy"]:
                raise RuntimeError("stored energy upper failed")
            if data["block_power_norm"] >= 0.04:
                raise RuntimeError("stored block contraction failed")
    production = certificate["rh50_production_cutoff_ledger"]
    if production["largest_dimension"] != 40960:
        raise RuntimeError("production cutoff dimension mismatch")
    if production["maximum_fixed_eight_two_norm_upper"] >= 5.7e-13:
        raise RuntimeError("production cutoff gate failed")
    if not production["all_stored_multiples_above_adaptive_requirement"]:
        raise RuntimeError("stored adaptive crossover gate failed")
    arb_cutoff = certificate["arb_production_cutoff_ledger"]
    if arb_cutoff["precision_bits"] != 256:
        raise RuntimeError("production cutoff precision mismatch")
    if arb_cutoff["largest_dimension"] != 40960:
        raise RuntimeError("Arb production cutoff dimension mismatch")
    if arb_cutoff["maximum_fixed_eight_two_norm_upper"] >= 5.7e-13:
        raise RuntimeError("Arb production cutoff upper failed")
    arb = certificate["arb_audit"]
    if not arb["certified_block_contraction"]:
        raise RuntimeError("small Arb contraction failed")
    if arb["production_matrix_interval_executed"]:
        raise RuntimeError("small Arb audit was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "binary64",
        "not an interval",
        "not the n=40960",
        "not executed here",
        "stage a1",
        "stage a3",
        "stage a4",
        "arithmetic trace formula",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
        "independent tpc",
    ):
        if phrase not in text:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary = load(ROOT / "results" / "summary.json")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    certificate = load(ROOT / "results" / "hardy_tail_cutoff_certificate.json")
    verify_hashes(summary, dependency)
    verify_theory(certificate)
    verify_numerics(certificate)
    verify_limitations(certificate)
    if summary["status"] != certificate["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "deterministic-block-tail-hardy-cutoff.pdf",
        ROOT / "figures" / "deterministic_hardy_tail_cutoff.pdf",
        ROOT / "figures" / "deterministic_hardy_tail_cutoff.png",
        ROOT / "results" / "hardy_tail_cutoff_certificate.json",
        ROOT / "results" / "deterministic_tail_pilot.json",
        ROOT / "results" / "deterministic_tail_pilot_smoke.json",
        ROOT / "results" / "arb_tail_audit.json",
        ROOT / "results" / "arb_production_cutoff_ledger.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_deterministic_tail_adaptive_cutoff_and_"
            "boundary_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "finite_tail_mechanism_closed": certificate["program_conclusion"][
                "deterministic_finite_matrix_tail_mechanism_closed"
            ],
            "adaptive_cutoff_route_closed": certificate["program_conclusion"][
                "adaptive_exact_real_cutoff_route_closed"
            ],
            "stage_A3_fully_closed": certificate["program_conclusion"][
                "stage_A3_fully_closed"
            ],
            "production_interval_executed": certificate["program_conclusion"][
                "production_scale_interval_trace_executed"
            ],
            "largest_dense_dimension": certificate["floating_five_scale_audit"][
                "largest_dimension"
            ],
            "largest_cutoff_dimension": certificate[
                "rh50_production_cutoff_ledger"
            ]["largest_dimension"],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "file_count": len(files),
                "status": payload["status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
