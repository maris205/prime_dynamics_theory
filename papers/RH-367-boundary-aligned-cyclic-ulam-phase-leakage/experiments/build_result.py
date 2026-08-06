"""Build the RH-367 source-lock and finite theorem ledger."""

from __future__ import annotations

import json
from pathlib import Path

from cyclic_ulam_edge.core import (
    digest,
    finite_checks,
    load_json,
    phase_summary,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"
CYCLIC = WORKSPACE / "cyclic_ulam_map"

SOURCE_LOCKS = {
    "cyclic_ulam_map/README.md": "bda637e0838b156ae3b147e70c82770151756ab01c57cd463991067aaf538c28",
    "cyclic_ulam_map/research/PROOF_PACKAGE.md": "f14d98e5b13c6332a058e5c9aebc3d906aae1f70ef6781dbc15f05d5ac9640ae",
    "cyclic_ulam_map/research/PAPER2_GATE_REPORT.md": "0bac05d7fa0f2519b6b8b51c3a570522111342fad50a44a140158c212d046eec",
    "cyclic_ulam_map/paper/main.tex": "a577012779940e5f3efde148cbf41779553234feaabc9167889ba97665b3399a",
    "cyclic_ulam_map/paper/sections/3_map_observables.tex": "8cd15c1628153cdabef03f767f0fc9ba5b49e15695c1cf5c4e2f08096a16adb5",
    "cyclic_ulam_map/paper/sections/4_ulam_theory.tex": "dcb68b82a385eb24d49b11bb3d447e0566aee643ae2af0d8eb00894f7100c14f",
    "cyclic_ulam_map/paper/sections/5_experiments.tex": "c3080f3a94d21ccc265c7f69598ab21b53ac1ff3bd2aa4dee9a92e0564b17f46",
    "cyclic_ulam_map/paper/sections/6_limitations_conclusion.tex": "064c002cd5e3684324ba8fce317bc2d6cef97be6ce6748faea31425a69932328",
    "cyclic_ulam_map/results/geometry_certificate.json": "376efa023edb53414f879443b9a9e98aaf6eeda9cbf1a904a5445fbaf439bc17",
    "cyclic_ulam_map/results/deterministic_gate.json": "c86f803b25e7f7e51e4ff07306f30f2e9d4c3e71d23e5e367277e6c3b09e03a0",
    "cyclic_ulam_map/results/phase_scan.json": "dbe7f9b888aea977c737b906436797dccd87df1478e2e2da1dbc82f798e66d9a",
    "cyclic_ulam_map/results/noise_gate.json": "679715a0b418044f8b8e6ec0a3672b0887e1ed14c25eb811372322586a8d3981",
    "cyclic_ulam_map/cyclic_ulam/ulam.py": "63928805abbd528c8d80d644dca21ac4aa31bc2ebae0f4f83b5fc6cd91e654e3",
    "cyclic_ulam_map/cyclic_ulam/geometry.py": "a4f0763375dc26af223d2a03ca8af791e4204cd770aa8c2a97079b7136cec37c",
    "prime_dynamics_theory/papers/RH-3-parity-resolved-band-merging-spectrum/README.md": "3112e88cb673040b94268370d816cac2483fd4139793d1adb2d2d60ac9a67e52",
    "prime_dynamics_theory/papers/RH-3-parity-resolved-band-merging-spectrum/main.tex": "5d9cf065571a2877301abc7c1eabdc3e75670f56615d9fca2454ba5a690acc3c",
    "prime_dynamics_theory/papers/RH-10-parity-renormalized-long-cycle-determinant/README.md": "d7058208aa5ae160f3b1222ac37d4d57d0fd49fe50929e7b7a2ea3329c3face8",
    "prime_dynamics_theory/papers/RH-10-parity-renormalized-long-cycle-determinant/main.tex": "dba591e47d7082d78f2f31d44f4499a5fcf5361046b39947d793816ff733d63b",
    "prime_dynamics_theory/papers/RH-55-strong-weak-riesz-cutoff-transfer/README.md": "d25bf4082145b1486c3477a338d1c55b1d014380d7ee2bf42101da1d39e64dfb",
    "prime_dynamics_theory/papers/RH-55-strong-weak-riesz-cutoff-transfer/main.tex": "c353086ffd925592a4b70baed356414514fbd819fe1de44d499afc58495fd2ac",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json": "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md": "d357192bfb80da578459cdac4add37840b8e1e47c5b2188ca0e49e7b096cbb23",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json": "6a125ca90b0964945f95b39397b6e83f15a23ad24c94d2e8b9c90d320db8e418",
}

SOURCE_COMMITS = {
    "cyclic_ulam_map": "e7d21f646498d77e1c3213d1e4f35dc8466038ff",
    "prime_dynamics_theory_rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
}


def source_audit() -> dict[str, object]:
    rows = []
    for relative, expected in SOURCE_LOCKS.items():
        actual = digest(WORKSPACE / relative)
        rows.append({
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "pass": actual == expected,
        })
    return {"rows": rows, "pass": all(row["pass"] for row in rows)}


def build_payload() -> dict[str, object]:
    geometry = load_json(CYCLIC / "results/geometry_certificate.json")
    phase = load_json(CYCLIC / "results/phase_scan.json")
    finite = finite_checks()
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "continuum_projector_or_resolvent_theorem": False,
        "sqrt_sigma_leakage_is_a_theorem": False,
        "universal_noise_exponent": False,
        "isolated_continuum_minus_one_resonance": False,
        "finite_ulam_matrix_is_canonical_operator": False,
        "finite_phase_scan_is_an_asymptotic_law": False,
        "arithmetic_coupling_constructed": False,
        "von_mangoldt_trace_constructed": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-367_fixed_boundary_aligned_cyclic_ulam_ledger",
        "route_verdict": {"route_a": "GO", "route_b": "STOP_SCOPED"},
        "gates": gates,
        "false_claims": false_claims,
        "source_commits": SOURCE_COMMITS,
        "source_audit": source_audit(),
        "geometry": {
            "u": geometry["geometry"]["u"],
            "r": geometry["geometry"]["r"],
            "interval": [geometry["geometry"]["interval_left"], geometry["geometry"]["interval_right"]],
            "max_residual": geometry["max_residual"],
        },
        "exact_theorems": {
            "aligned_block": "P=[[0,A],[B,0]] and P s=-s for any exact partition with r as a boundary",
            "crossing_projection": "1-(2 theta-1)^2=4 theta(1-theta)",
            "weighted_local_defect": "4 h theta(1-theta)",
            "global_projection_mass": "zero for aligned exact Ulam; positive phase diagnostic when crossing",
        },
        "finite_checks": finite,
        "phase_scan": phase_summary(phase),
        "phase_protocol": {
            "source": "cyclic_ulam_map/results/phase_scan.json",
            "phase_count": phase["phase_count"],
            "cells": phase["cells"],
            "rows": len(phase["rows"]),
            "interpretation": "finite diagnostic; no universal power law",
        },
        "overlap_ledger": {
            "RH-3": "continuum parity eigenmode and periodograms; no crossing-cell Ulam theorem",
            "RH-10": "long-cycle/noise traces and parity determinant; no phase-local Ulam defect",
            "RH-55": "folded-Gaussian midpoint-Ulam strong-weak transfer; no PCF block inheritance",
            "distinct_edge": True,
        },
        "claim_boundary": {
            "route_b_first_blocker": "common strong-space projector/resolvent theorem is absent",
            "physical_coordinate": "actual_same_clock_unnormalized_head_transport_open",
            "notes": [
                "Finite Ulam/L1 statements are not continuum spectral statements.",
                "Noise slopes are finite-range diagnostics only.",
                "No arithmetic, zeta, prime, operator, or RH identification is supplied.",
            ],
        },
    }


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "source_lock_pass": payload["source_audit"]["pass"],
        "phase_rows": payload["phase_scan"]["row_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
