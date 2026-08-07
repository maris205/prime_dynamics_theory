"""Build the source-locked RH-379 exact result ledger."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

from phasewise_memory import verify_certificate


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_FILES = [
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/README.md",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/UPDATED_ROADMAP.md",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/main.tex",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/src/square_clock/core.py",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/README.md",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/main.tex",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/references.bib",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/src/all_clock_capacity/core.py",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/results/result.json",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/README.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/main.tex",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/references.bib",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/src/shift_two_chowla/core.py",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/results/result.json",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/README.md",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/UPDATED_ROADMAP.md",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/main.tex",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/references.bib",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/src/safe_window_transducers/core.py",
    "prime_dynamics_theory/papers/RH-378-safe-window-memory-and-online-capacity-transducers/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh375_release": "071fed1b2a5d8488b9d2e35a99a753953b233584",
    "rh376_release": "0cf6179084bc8151318bb8f0955e529c12c0661a",
    "rh378_release": "08574b1bab1b9f549d4c07df97bb548d40aae51f",
    "rh_mvp2_archive": "c0aed13a34b8bbc53061aed23738660adcd3624c",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@lru_cache(maxsize=1)
def build_payload() -> dict[str, object]:
    """Recompute the complete source-locked payload without writing it."""

    sources = {relative: digest(WORKSPACE / relative) for relative in SOURCE_FILES}
    certificate = verify_certificate()
    if not certificate["all_pass"]:
        raise RuntimeError("RH-379 exact certificate failed")
    return {
        "status": "RH-379_phasewise_chowla_free_memory_supremum",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "factor_class": "fixed finite q, universally safe phasewise lag-two tables with c11(r)=0 at every phase",
            "table_census": "all 512 local tables are exhausted; exactly 192 have c11=0",
            "canonical_reduction": "subset dominance first reduces to 0,J,K,I; only then identical canonical compatibility and I=J+K delete K",
            "fixed_clock_formula": "G(q) is the exact three-state cyclic max-plus optimum on actions {0,J,I}",
            "phasewise_cancellation": "all non-main terms are o(N) at fixed q by fixed-AP Davenport cancellation and a fixed square-divisor cutoff",
            "q36_gain": "G(36)=9/(2*pi^2)-kappa2/7 > F(36)=4/pi^2",
            "square_clock_refinement": "G(q_y)=B_y+Delta_y with Delta_y=mathcal_E_y*(4/(A_y*pi^2)-kappa2/D_y)>0 and Delta_y->0",
            "all_clock_supremum": "sup_{q finite} G(q)=B_infinity",
            "reverse_inequality": "the RH-375 one-site class embeds by f_r(x,z)=g_r(z)",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "phase-weighted shift-two correlations D2 in phases with c11(r)!=0",
            "notes": [
                "Every N-limit is taken at a fixed finite q; the cofinal y-limit is taken only afterward.",
                "The theorem is phasewise c11=0 and does not cover unrestricted memory tables.",
                "The q=36 result is an exact square-clock strict gain, not the first same-clock gain; already G(1)>F(1)=0.",
                "The arbitrary-clock upper bound is a retained-phase plus tail-charge union bound, not memory saturation at same prime support.",
                "No finite-clock attainment or nonattainment statement is made for G.",
                "No monotonicity statement is made for Delta_y.",
                "Finite decimals and finite clock rows are reproduction only.",
                "No adaptive-capacity limit, intrinsic operator, trace, zero identification, Hilbert--Polya construction, or RH implication is claimed.",
            ],
        },
        "gates": {
            "A_canonical_intrinsic_dynamical_spectral_determinant": False,
            "B_time_oriented_scattering_or_unitary_completion": False,
            "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
    }


def main() -> None:
    payload = build_payload()
    sources = payload["source_locks"]["files"]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "source_lock_count": len(sources),
                "all_pass": payload["certificate"]["all_pass"],
                "c11_zero_tables": payload["certificate"]["census"]["c11_zero_tables"],
                "largest_clock": max(row["q"] for row in payload["certificate"]["fixture_clocks"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
