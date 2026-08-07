"""Build the immutable-source-locked RH-380 exact result ledger."""

from __future__ import annotations

import hashlib
import json
import subprocess
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

from finite_clock_gap import verify_certificate
from finite_clock_gap.core import H_HIGH, H_LOW


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_COMMITS = {
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh375_release": "071fed1b2a5d8488b9d2e35a99a753953b233584",
    "rh379_release": "9ae9802ed17529ef4adfb81d7e2158d47c3c8d22",
    "rh_mvp2_archive": "c0aed13a34b8bbc53061aed23738660adcd3624c",
}

SOURCE_GROUPS = {
    "rh374_release": (
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/README.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/main.tex",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/src/square_clock/core.py",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json",
    ),
    "rh375_release": (
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/README.md",
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/main.tex",
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/references.bib",
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/src/all_clock_capacity/core.py",
        "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/results/result.json",
    ),
    "rh379_release": (
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/README.md",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/main.tex",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/references.bib",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/src/phasewise_memory/core.py",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.json",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.schema.json",
    ),
    "rh_mvp2_archive": (
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json",
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    ),
}

SOURCE_FILES = tuple(path for group in SOURCE_GROUPS.values() for path in group)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _release_blob(relative: str, release: str) -> bytes:
    prefix = "prime_dynamics_theory/"
    if not relative.startswith(prefix):
        raise ValueError(f"source path is outside the repository namespace: {relative}")
    repository_relative = relative[len(prefix) :]
    completed = subprocess.run(
        ["git", "-C", str(REPOSITORY), "show", f"{release}:{repository_relative}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def build_source_locks() -> tuple[list[dict[str, str]], bool]:
    entries: list[dict[str, str]] = []
    release_blob_identity_pass = True
    for release_name, files in SOURCE_GROUPS.items():
        release = SOURCE_COMMITS[release_name]
        for relative in files:
            live_hash = digest(WORKSPACE / relative)
            blob_hash = hashlib.sha256(_release_blob(relative, release)).hexdigest()
            release_blob_identity_pass = release_blob_identity_pass and live_hash == blob_hash
            entries.append(
                {"path": relative, "sha256": live_hash, "release": release_name}
            )
    return entries, release_blob_identity_pass


def _load_rh379() -> dict[str, object]:
    path = (
        WORKSPACE
        / "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.json"
    )
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("RH-379 result root is not an object")
    return value


def predecessor_checks() -> dict[str, object]:
    prior = _load_rh379()
    certificate = prior["certificate"]
    constants = certificate["certified_constants"]
    h_low_text, h_high_text = constants["pi2_kappa2_interval"]
    h_low = Fraction(h_low_text)
    h_high = Fraction(h_high_text)
    h_enclosure_pass = H_LOW < h_low < h_high < H_HIGH

    fixtures = {row["q"]: row["G"] for row in certificate["fixture_clocks"]}
    expected_36 = {"inv_pi2": "9/2", "kappa2": "-1/7"}
    expected_180 = {"inv_pi2": "73/16", "kappa2": "-25/161"}
    expected_900 = {"inv_pi2": "73/16", "kappa2": "-1/7"}
    negative_control_pass = (
        fixtures[36] == expected_36
        and fixtures[180] == expected_180
        and fixtures[900] == expected_900
        and fixtures[180] != fixtures[36]
    )
    negative_control_sign_pass = Fraction(1, 16) - Fraction(2, 161) * H_HIGH > 0
    return {
        "rh379_status": prior["status"],
        "h_interval_from_rh379": [h_low_text, h_high_text],
        "coarse_h_interval": [str(H_LOW), str(H_HIGH)],
        "h_enclosure_pass": h_enclosure_pass,
        "negative_control": {
            "q36": fixtures[36],
            "q180": fixtures[180],
            "q900": fixtures[900],
            "q180_minus_q36": {"inv_pi2": "1/16", "kappa2": "-2/161"},
            "scope": "Q=180 adds prime 5 to q_1=36 and is not a same-prime-support cover",
            "sign_from_h_upper_bound_pass": negative_control_sign_pass,
            "pass": negative_control_pass and negative_control_sign_pass,
        },
        "all_pass": h_enclosure_pass and negative_control_pass and negative_control_sign_pass,
    }


@lru_cache(maxsize=1)
def build_payload() -> dict[str, object]:
    entries, release_blob_identity_pass = build_source_locks()
    if len(entries) != 24 or len({entry["path"] for entry in entries}) != 24:
        raise RuntimeError("RH-380 source-lock membership is not the frozen 24-file set")
    if not release_blob_identity_pass:
        raise RuntimeError("a live source differs from its declared release blob")
    certificate = verify_certificate()
    predecessor = predecessor_checks()
    if not certificate["all_pass"] or not predecessor["all_pass"]:
        raise RuntimeError("RH-380 exact certificate failed")
    return {
        "status": "RH-380_square_clock_monotonicity_and_finite_clock_nonattainment",
        "source_locks": {
            "count": len(entries),
            "entries": entries,
            "release_blob_identity_pass": release_blob_identity_pass,
            "pass": True,
        },
        "source_commits": SOURCE_COMMITS,
        "predecessor_checks": predecessor,
        "certificate": certificate,
        "theorem": {
            "factor_class": "fixed finite q before N tends to infinity; universally safe phasewise lag-two tables with c11(r)=0 at every phase",
            "even_run_recurrence": "mathcal_E_(y+1)=(p_(y+1)^2-2)*mathcal_E_y+M_y",
            "increment": "G(q_(y+1))-G(q_y)=2*(L_y-2*mathcal_E_y)/(pi^2*A_y*(s-1))+M_y*(4/pi^2-H_(y+1))/(A_y*(s-1))",
            "strictness": "L_y-2*mathcal_E_y=2*R_4+4*R_6+6*R_8>=6, hence G(q_y) is strictly increasing",
            "special_saturation": "if q_y divides Q and Q has exactly the same prime support, separator-specific replication gives G(Q)=G(q_y)",
            "finite_clock_nonattainment": "for every fixed finite q, G(q)<B_infinity",
            "explicit_gap": "if y contains every odd prime divisor of q, then B_infinity-G(q)>=12/(pi^2*A_y*(p_(y+1)^2-1))",
            "absolute_optimum": "the positive optimum is G(q); RH-379 input reflection supplies the matching absolute optimum",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "nonzero phasewise c11 terms require phase-weighted shift-two Chowla input",
            "notes": [
                "The N-limit is taken at a fixed finite q; no q=q(N) statement is made.",
                "The theorem is restricted to the RH-379 phasewise c11=0 class.",
                "Same-support saturation uses square-clock zero-weight separators; it is not a general cyclic-cover theorem.",
                "The lcm argument allows arbitrary 2-adic exponent and arbitrary exponents on supported odd primes.",
                "No monotonicity statement is made for Delta_y.",
                "Finite rows certify identities and fixtures; they do not prove the all-y theorem by fitting.",
                "No adaptive-capacity convergence, intrinsic operator, trace formula, zero identification, Hilbert--Polya construction, RH implication, or Gate promotion is claimed.",
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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "source_lock_count": payload["source_locks"]["count"],
                "release_blob_identity_pass": payload["source_locks"]["release_blob_identity_pass"],
                "all_pass": payload["certificate"]["all_pass"],
                "same_support_rows": len(payload["certificate"]["same_support_saturation"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
