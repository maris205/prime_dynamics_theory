"""Build the RH-370 theorem ledger and finite algebra audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from fold_ulam import ROOT_U, finite_checks, spike_jump, spike_values


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "cyclic_ulam_map/cyclic_ulam/ulam.py": "63928805abbd528c8d80d644dca21ac4aa31bc2ebae0f4f83b5fc6cd91e654e3",
    "cyclic_ulam_map/cyclic_ulam/spectrum.py": "e8bf22f058030d4024982be9ef3953e50bb70fbf15f61c90c0671f81decd63da",
    "cyclic_ulam_map/README.md": "bda637e0838b156ae3b147e70c82770151756ab01c57cd463991067aaf538c28",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/main.tex": "b6d59b16169a73b386db927618e3be198c2a369e13c907fd837d3057f8369ecb",
    "prime_dynamics_theory/papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/THEOREM_LEDGER.md": "429b0d8a921a6e29c1ec55c10361d9eef3db126da3bcb810337fe9f24605439d",
    "prime_dynamics_theory/papers/RH-14-square-root-parity-boundary-layer/main.tex": "199d5abee0aaf7d16090cdedbb50688f177739a2d142b8e927d45e0fd5f5bb34",
    "prime_dynamics_theory/papers/RH-52-intrinsic-peripheral-residue-transfer/main.tex": "4e218afbe13241db1f90afefba3ba75b00c794ec1c876bab18f4ee1504371255",
    "prime_dynamics_theory/papers/RH-55-strong-weak-riesz-cutoff-transfer/main.tex": "c353086ffd925592a4b70baed356414514fbd819fe1de44d499afc58495fd2ac",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json": "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
}

SOURCE_COMMITS = {
    "cyclic_ulam_map": "e7d21f646498d77e1c3213d1e4f35dc8466038ff",
    "prime_dynamics_theory_rh367_release": "ed2076391759499d46a3d5f64d223cf469d63bbb",
    "prime_dynamics_theory_rh14": "d5807dd061ad9ca48cf2f406f4b35c15b343d3d2",
    "prime_dynamics_theory_rh52": "d50fc86981e6a02f9c12d2a5aa150b8acd192f73",
    "prime_dynamics_theory_rh55": "72af2d407592cd6c697e673e3d64267747b01021",
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
        path = WORKSPACE / relative
        actual = digest(path) if path.is_file() else "MISSING"
        rows.append({
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "pass": actual == expected,
        })
    return {"rows": rows, "pass": all(row["pass"] for row in rows)}


def spike_audit() -> list[dict[str, object]]:
    rows = []
    coefficient = (2.0 - 2.0**0.5) / ROOT_U**0.5
    for h in (1 / 4, 1 / 16, 1 / 64, 1 / 256):
        first, second = spike_values(ROOT_U, h)
        jump = spike_jump(ROOT_U, h)
        rows.append({
            "h": str(h),
            "first_average": first,
            "second_average": second,
            "jump": jump,
            "scaled_jump": jump * h**0.5,
            "coefficient": coefficient,
            "pass": abs(jump * h**0.5 - coefficient) < 1e-12,
        })
    return rows


def build_payload() -> dict[str, object]:
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "finite_nonzero_spectrum_is_continuum_spectrum": False,
        "l1_exterior_bridge_is_riesz_bridge_at_minus_one": False,
        "bv_projection_is_uniformly_bounded": False,
        "arbitrary_aligned_partition_is_fold_compatible": False,
        "noise_schedule_extends_to_zero_noise": False,
        "canonical_spectral_determinant_constructed": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
    }
    finite = finite_checks()
    spikes = spike_audit()
    return {
        "status": "RH-370_fold_compatible_ulam_spike_barrier",
        "route_verdict": {"route_a": "GO", "route_b": "STOP_SCOPED"},
        "gates": gates,
        "false_claims": false_claims,
        "source_commits": SOURCE_COMMITS,
        "source_audit": source_audit(),
        "exact_theorems": {
            "fold_map": "q(x)=|x|, T(y)=|1-u y^2|, T q=q f",
            "finite_quotient": "chi_full(z)=z^m chi_fold(z) for mirror-compatible cells",
            "kernel": "P_full^T ker(A)=0",
            "weak_bridge": "E_h P_T E_h g -> P_T g in L1 for fixed g",
            "exterior_resolvent": "uniform strong L1 resolvent convergence on compact subsets of |z|>1",
            "spike": "P_T 1=(2 sqrt(u))^(-1)(1-y)^(-1/2) on (u-1,1)",
            "bv_barrier": "terminal jump=(2-sqrt(2))/sqrt(u h), hence BV norm grows as h^(-1/2)",
        },
        "finite_checks": finite,
        "spike_checks": {
            "rows": spikes,
            "all_pass": all(row["pass"] for row in spikes),
            "coefficient": (2.0 - 2.0**0.5) / ROOT_U**0.5,
        },
        "exterior_bound_checks": [
            {"z": z, "bound": 1.0 / (z - 1.0)} for z in (1.1, 1.5, 2.0, 3.0)
        ],
        "upstream_protocol": {
            "cyclic_ulam_tests": "12/12",
            "finite_phase_rows": 136,
            "interpretation": "source reproduction only; no phase row is a spectral-limit observation",
        },
        "overlap_ledger": {
            "RH-367": "supplies aligned finite block/sign theorem; leaves common strong projector/resolvent open",
            "RH-14": "supplies the folded PCF tower/spike setting and deterministic peripheral context",
            "RH-52": "positive-noise strong/weak stability requires h=o(sigma^2), not sigma=0",
            "RH-55": "positive-noise common contour transfer; does not furnish the deterministic endpoint",
            "cyclic_ulam_map": "source-level exact cell-overlap and finite spectral code",
            "distinct_edge": True,
        },
        "claim_boundary": {
            "route_b_first_blocker": "no uniform deterministic natural-strong-space projector bound at the terminal spike",
            "physical_coordinate": "actual_same_clock_unnormalized_head_transport_open",
            "notes": [
                "The quotient applies only to mirror-compatible partitions.",
                "The L1 bridge is exterior to the unit circle and does not isolate -1.",
                "The BV spike bound is a scoped obstruction, not a theorem about every conceivable fractional space.",
                "No noisy finite matrix is identified with the deterministic operator.",
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
        "spike_checks": payload["spike_checks"]["all_pass"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
