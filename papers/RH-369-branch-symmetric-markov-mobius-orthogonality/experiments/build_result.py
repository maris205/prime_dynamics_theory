"""Build the RH-369 theorem and finite-audit ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from fractions import Fraction

from branch_markov import finite_checks, mobius_prefix, parameter_checks, variance_formula


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "henon_mobius_correlations/henon_mobius/sft.py": "42d1567b7b746bf2dd775b94bd539cf781ea45812a7dca092d0bbd0a46d191d7",
    "henon_mobius_correlations/paper/sections/3_henon_setup.tex": "5bee8e61f615d674d92bafb9b00163003dc2f8b91b5c4e63316c46dd27980eb7",
    "henon_mobius_correlations/paper/sections/5_parry_typical.tex": "045ff9554dae44d923255b8d33d0509b47e01335390839d2253effcad42cd5a7",
    "henon_mobius_correlations/THEOREM_PACKAGE.md": "634fd9543ceab91c19766015141e83636d64213f131d5c1b098385ef68c3b102",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md": "d357192bfb80da578459cdac4add37840b8e1e47c5b2188ca0e49e7b096cbb23",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json": "6a125ca90b0964945f95b39397b6e83f15a23ad24c94d2e8b9c90d320db8e418",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json": "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
}

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "prime_dynamics_theory_rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


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
    t = Fraction(1, 2)
    values = mobius_prefix(14)
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "markov_family_is_henon_selected": False,
        "uniform_in_t_theorem": False,
        "parry_family_extension_is_new_physical_trace": False,
        "variance_density_is_unconditional": False,
        "markov_covariance_is_prime_trace": False,
        "canonical_spectral_determinant_constructed": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-369_branch_symmetric_markov_mobius_orthogonality",
        "route_verdict": {"route_a": "GO", "route_b": "STOP_SCOPED"},
        "gates": gates,
        "false_claims": false_claims,
        "source_commits": SOURCE_COMMITS,
        "source_audit": source_audit(),
        "exact_theorems": {
            "transition_family": "P_t=[[t,0,1-t,0],[1,0,0,0],[0,t,0,1-t],[0,1,0,0]], 0<t<1",
            "stationary_law": "pi_t=(1,1-t,1-t,(1-t)^2)/(2-t)^2",
            "normalized_covariance": "odd lags 0; lag 2k equals (-(1-t))^k",
            "fixed_parameter_orthogonality": "for every fixed t, nu_t-a.e. simultaneous all-continuous-observable Mobius cancellation",
            "variance_formula": "V_N=sum mu^2+2 sum_{k>=1} (-(1-t))^k sum_n mu(n)mu(n+2k)",
            "variance_bound": "0<=V_N<=((2-t)/t)N",
            "conditional_density": "V_N/N -> 6/pi^2 only under ordinary fixed-shift two-point Chowla",
        },
        "parameter_checks": [
            parameter_checks(Fraction(1, 2)),
            parameter_checks(Fraction(2, 3)),
            parameter_checks(Fraction(3, 4)),
        ],
        "finite_checks": finite_checks(),
        "endpoint_diagnostic": {
            "N": len(values),
            "t": "1/2",
            "variance": str(variance_formula(values, t)),
            "interpretation": "finite exact reproduction only; no asymptotic fit",
        },
        "overlap_ledger": {
            "RH-366": "supplies the frozen graph, sign observable, Parry specialization, and a.s. proof template",
            "henon_mobius_correlations": "supplies the source theorem and exact Parry covariance anchors",
            "RH-367": "not used as a continuum spectral bridge",
            "RH-368": "distinct PCF parity-factor capacity; not identified with this family",
            "distinct_edge": True,
        },
        "claim_boundary": {
            "route_b_first_blocker": "externally selected symbolic Markov parameter; no canonical arithmetic/operator identification",
            "physical_coordinate": "actual_same_clock_unnormalized_head_transport_open",
            "notes": [
                "The theorem is pointwise in fixed t and has no common full-measure set over all t.",
                "The Parry value t=phi^{-1} is an overlap, not a new physical construction.",
                "The conditional variance density is not an unconditional Chowla result.",
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
        "parameter_checks": all(row["pass"] for row in payload["parameter_checks"]),
        "finite_checks": payload["finite_checks"]["all_pass"],
        "endpoint_variance": payload["endpoint_diagnostic"]["variance"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
