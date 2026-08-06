"""Build the RH-368 exact parity-factor capacity ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from parity_capacity import capacity_formula, finite_checks, mobius_prefix


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "dyna_zeta_map/README.md": "231e406921bd55edc9e8d0d25379e0e62c3880286158f60a30caf7db60069fd2",
    "dyna_zeta_map/research/PROOF_PACKAGE.md": "2407f5ae8312eb8bfdcffe21c5a198cf841c3b282e35a0453e3e8725b1c5d834",
    "dyna_zeta_map/paper/main.tex": "eb0d0af61482716688393af75a2c7800078fd252b9b327e5d392e6dc839c2b95",
    "dyna_zeta_map/paper/sections/6_quadratic_application.tex": "673ffc337012b47eff79a6bbba2d76580dc6a6792714a2a4036c8a28d5882a4e",
    "dyna_zeta_map/results/verification_summary.md": "443fdb557772e0267a16064798de3a7912f84c181f52afc448f93278395bbfad",
    "dyna_zeta_map/results/wheel_zeta_data.json": "3ca528ca159f067e51a6657110039997d0115e6f63fa10fbdf1bb11eeada4f7b",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md": "d357192bfb80da578459cdac4add37840b8e1e47c5b2188ca0e49e7b096cbb23",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json": "6a125ca90b0964945f95b39397b6e83f15a23ad24c94d2e8b9c90d320db8e418",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/README.md": "f26a3654c1ad996763d7e49b2a2f74f2d8775881467252788f8476c8be804193",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/results/result.json": "473fb75147bf38c47f38d1f2254ae1ca0cef64cd30e3731eafa51e59ef39be7f",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json": "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
}

SOURCE_COMMITS = {
    "dyna_zeta_map": "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
    "prime_dynamics_theory_rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
    "prime_dynamics_theory_rh367_release": "032316d0e0bfd5b07f161d9bed05d552efd5dd97",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_audit() -> dict[str, object]:
    rows = []
    for relative, expected in SOURCE_LOCKS.items():
        actual = digest(WORKSPACE / relative)
        rows.append({"path": relative, "expected_sha256": expected,
                     "actual_sha256": actual, "pass": actual == expected})
    return {"rows": rows, "pass": all(row["pass"] for row in rows)}


def build_payload() -> dict[str, object]:
    n = 2**20
    values = mobius_prefix(n)
    endpoint = capacity_formula(values)
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "parity_capacity_is_distance_two_capacity": False,
        "adaptive_capacity_is_canonical_arithmetic_coupling": False,
        "quadratic_factor_is_hasse_weil_or_full_h_p_zeta": False,
        "capacity_limit_is_a_prime_trace": False,
        "finite_endpoint_is_asymptotic_evidence": False,
        "canonical_spectral_determinant_constructed": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-368_parity_factor_mobius_capacity_limit",
        "route_verdict": {"route_a": "GO", "route_b": "STOP_SCOPED"},
        "gates": gates,
        "false_claims": false_claims,
        "source_commits": SOURCE_COMMITS,
        "source_audit": source_audit(),
        "exact_theorems": {
            "quadratic_markov_matrix": "A=[[0,0,1],[0,0,1],[1,1,0]] on the PCF invariant interval",
            "parity_factor": "positive positions lie in one parity class (A_{2})",
            "finite_capacity": "K_N=max_{r in {0,1}} max(|-M_N+2P_r|,|-M_N-2N_r|)",
            "capacity_limit": "K_N/N -> 4/pi^2",
            "parity_squarefree_densities": "S_odd/N -> 4/pi^2 and S_even/N -> 2/pi^2",
        },
        "finite_checks": finite_checks(12),
        "endpoint_diagnostic": {
            "N": n,
            "capacity": endpoint["capacity"],
            "capacity_over_N": endpoint["capacity"] / n,
            "best_candidate": endpoint["best_key"],
            "candidates": endpoint["candidates"],
            "parity_statistics": endpoint["statistics"],
            "interpretation": "finite reproduction only; not an asymptotic estimate",
        },
        "overlap_ledger": {
            "RH-362": "prime-return bouquets and entropy towers; no A_{2} parity-factor capacity limit",
            "RH-363": "return-rank entropy data; no Möbius sign capacity",
            "RH-366": "distance-two four-state MWIS capacity remains bracket/open; this paper uses the distinct A_{2} factor",
            "RH-367": "two-band finite-Ulam alignment; no three-cell parity-factor capacity theorem",
            "dyna_zeta_map": "source-backed PCF three-cell realization and boundary-aware zeta identity",
            "distinct_edge": True,
        },
        "claim_boundary": {
            "route_b_first_blocker": "the optimizing sign word reads the complete Möbius prefix and is not an intrinsic operator trace",
            "physical_coordinate": "actual_same_clock_unnormalized_head_transport_open",
            "notes": [
                "The A_{2} capacity limit is not the RH-366 distance-two capacity limit.",
                "The PCF zeta identity is a finite symbolic factor, not a completed-zeta divisor.",
                "No Hilbert--Polya operator, von Mangoldt trace, zero identification, or RH implication is claimed.",
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
        "finite_checks": payload["finite_checks"]["all_pass"],
        "endpoint_capacity": payload["endpoint_diagnostic"]["capacity"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
