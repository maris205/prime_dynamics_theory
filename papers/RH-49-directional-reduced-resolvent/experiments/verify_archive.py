"""Verify RH-49 hashes, theorem boundaries, and numerical gates."""

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
        "rigorous_quarter_power_stable_rank_reduction_with_hilbert_schmidt_directional_gate"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    if not certificate["exact_residue_deflation"][
        "branch_pole_removed_exactly"
    ]:
        raise RuntimeError("exact branch deflation was lost")
    if certificate["stable_rank_transfer"][
        "global_resolvent_norm_needed_for_the_inequality"
    ]:
        raise RuntimeError("global resolvent was incorrectly required")
    endpoint = certificate["critical_endpoint_coupling_theorem"]
    if endpoint["sqrt_stable_rank_upper"] != (
        "||B||_S2/||B||=O(sigma^(-1/4))"
    ):
        raise RuntimeError("quarter-power endpoint theorem mismatch")
    if endpoint["stored_sparse_cutoff_family_proved_by_this_theorem"]:
        raise RuntimeError("stored sparse transfer was overclaimed")
    closure = certificate["quarter_power_closure"]
    if closure["rh48_gamma"] != "gamma=1/4+delta":
        raise RuntimeError("gamma transfer mismatch")
    if closure["preserves_every_strict_p_greater_than_2_when"] != (
        "delta<=1/4"
    ):
        raise RuntimeError("delta threshold mismatch")
    if closure["hilbert_schmidt_gain_bound_proved_for_full_family_here"]:
        raise RuntimeError("Hilbert-Schmidt gain was overclaimed")


def verify_numerics(certificate) -> None:
    audit = certificate["floating_five_scale_audit"]
    if audit["noise_levels"] != 5 or audit["largest_dimension"] != 40960:
        raise RuntimeError("five-scale audit dimensions mismatch")
    fits = audit["fits"]
    b_rank = fits["B_sqrt_stable_rank_candidate"]
    if not 0.24 < b_rank["growth_exponent"] < 0.25:
        raise RuntimeError("B stable-rank exponent missed the quarter power")
    if b_rank["maximum_log_residual"] >= 0.002:
        raise RuntimeError("B stable-rank regression residual is too large")
    if fits["full_hilbert_schmidt_gain_sum"]["growth_exponent"] != 0.0:
        raise RuntimeError("full Hilbert-Schmidt plateau gate failed")
    if fits["stable_rank_transferred_full_candidate"][
        "growth_exponent"
    ] >= 0.25:
        raise RuntimeError("transferred candidate exceeded quarter power")
    if fits["direct_mixed_gain_sum_candidate"]["growth_exponent"] >= 0.20:
        raise RuntimeError("direct mixed candidate gate failed")
    if audit["last_three_level_fits"]["direct_mixed_gain_sum_candidate"][
        "growth_exponent"
    ] >= 0.13:
        raise RuntimeError("tail mixed exponent gate failed")
    finest = audit["rows"][-1]
    if finest["maximum_gmres_iterations"] != 41:
        raise RuntimeError("finest GMRES ledger mismatch")
    if finest["maximum_gmres_relative_residual"] >= 2.0e-10:
        raise RuntimeError("GMRES residual gate failed")
    if finest["maximum_branch_leakage"] >= 3.0e-13:
        raise RuntimeError("branch leakage gate failed")
    if audit["operator_candidates_are_validated_uppers"]:
        raise RuntimeError("operator candidate was overclaimed")
    if audit["hutchinson_gains_are_validated_uppers"]:
        raise RuntimeError("Hutchinson candidate was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "hard-cutoff",
        "not a validated asymptotic upper",
        "not validated uppers",
        "worst real contour node",
        "arithmetic trace formula",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    ):
        if phrase not in text:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary = load(ROOT / "results" / "summary.json")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    certificate = load(
        ROOT / "results" / "directional_reduced_resolvent_certificate.json"
    )
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
        ROOT / "residue-deflated-directional-resolvents.pdf",
        ROOT / "figures" / "directional_reduced_resolvent.pdf",
        ROOT / "figures" / "directional_reduced_resolvent.png",
        ROOT / "results" / "directional_reduced_resolvent_certificate.json",
        ROOT / "results" / "reduced_directional_pilot.json",
        ROOT / "results" / "mixed_operator_gain_pilot.json",
        ROOT / "results" / "coupling_stable_rank_pilot.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_deflation_quarter_power_hilbert_schmidt_and_floating_boundary_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "exact_branch_deflation": certificate[
                "exact_residue_deflation"
            ]["branch_pole_removed_exactly"],
            "stable_rank_inequality_needs_global_resolvent": certificate[
                "stable_rank_transfer"
            ]["global_resolvent_norm_needed_for_the_inequality"],
            "endpoint_sqrt_stable_rank": certificate[
                "critical_endpoint_coupling_theorem"
            ]["sqrt_stable_rank_upper"],
            "stored_sparse_transfer_proved": certificate[
                "critical_endpoint_coupling_theorem"
            ]["stored_sparse_cutoff_family_proved_by_this_theorem"],
            "delta_threshold": certificate["quarter_power_closure"][
                "preserves_every_strict_p_greater_than_2_when"
            ],
            "B_stable_rank_fitted_exponent": certificate[
                "floating_five_scale_audit"
            ]["fits"]["B_sqrt_stable_rank_candidate"]["growth_exponent"],
            "direct_mixed_fitted_exponent": certificate[
                "floating_five_scale_audit"
            ]["fits"]["direct_mixed_gain_sum_candidate"]["growth_exponent"],
            "largest_dimension": certificate["floating_five_scale_audit"][
                "largest_dimension"
            ],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "file_count": len(files),
                "status": payload["status"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
