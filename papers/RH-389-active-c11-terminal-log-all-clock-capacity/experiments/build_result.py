"""Build the offline immutable-source-locked RH-389 result."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from terminal_log_capacity import core  # noqa: E402
from source_locks import (  # noqa: E402
    EXPECTED_LOGICAL_SOURCE_DIGEST,
    JY_CANONICAL_SHA256,
    MAYNARD_CANONICAL_SHA256,
    TAO_CANONICAL_SHA256,
    build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 208_648
CERTIFICATE_FIXTURE_SHA256 = "b31187db4ea284152b0c1cb895439e29cfa80a4e564c87814ee182f87be0a020"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}

FORBIDDEN = {
    "ordinary_Cesaro_limit": False,
    "growing_q_or_q_of_X": False,
    "uniformity_over_unbounded_clocks": False,
    "max_before_terminal_log_limit": False,
    "K_N_or_projective_selector": False,
    "quantitative_rate_or_power_saving": False,
    "operator_trace_or_zeros": False,
    "proof_of_RH": False,
    "vendored_external_payload": False,
}


def _validate_constants() -> None:
    hashes = (
        CERTIFICATE_FIXTURE_SHA256,
        EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256,
        MAYNARD_CANONICAL_SHA256,
        TAO_CANONICAL_SHA256,
    )
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(CERTIFICATE_FIXTURE_BYTES) is not int or CERTIFICATE_FIXTURE_BYTES <= 0:
        raise ValueError("certificate fixture bytes must be a positive exact int")
    if set(GATES) != {
        "A_intrinsic_determinant",
        "B_scattering_completion",
        "C_self_adjoint_generator",
        "D_von_mangoldt_weighted_prime_power_traces",
        "E_completed_zeta_divisor_equality",
    }:
        raise ValueError("Gate A--E membership changed")
    if any(type(value) is not bool for value in (*GATES.values(), *FORBIDDEN.values())):
        raise TypeError("gate/firewall values must be exact booleans")


def mutation_results(certificate: dict[str, object]) -> dict[str, object]:
    if type(certificate) is not dict:
        raise TypeError("certificate must be an exact object")
    rows = []
    for name in core.MUTATION_NAMES:
        candidate = core.apply_mutation(certificate, name)
        changed = not core.exact_equal(candidate, certificate)
        rejected = changed and not core.verify_certificate(candidate, compare_fresh=False)
        rows.append({"changed": changed, "name": name, "rejected": rejected})
    return {
        "all_pass": len(rows) == 24 and all(row["changed"] is True and row["rejected"] is True for row in rows),
        "count": len(rows),
        "rows": rows,
        "verification_mode": "independently recomputed field-level semantic verification without certificate/group builders",
    }


def build_payload() -> dict[str, object]:
    _validate_constants()
    certificate = core.build_certificate()
    field_verified = core.verify_certificate(certificate, compare_fresh=False)
    fresh_verified = core.verify_certificate(certificate, compare_fresh=True)
    certificate_bytes = len(core.canonical_json(certificate).encode("utf-8"))
    certificate_sha = core.payload_sha256(certificate)
    fixture_pass = (
        certificate_bytes == CERTIFICATE_FIXTURE_BYTES
        and certificate_sha == CERTIFICATE_FIXTURE_SHA256
        and field_verified
        and fresh_verified
    )
    mutations = mutation_results(certificate)
    source_locks = build_source_closure()
    source_pass = (
        source_locks["pass"] is True
        and source_locks["git_count"] == 95
        and source_locks["remote_count"] == 3
        and source_locks["logical_count"] == 98
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_locks["remote"]["canonical_digests"] == [  # type: ignore[index]
            JY_CANONICAL_SHA256,
            MAYNARD_CANONICAL_SHA256,
            TAO_CANONICAL_SHA256,
        ]
    )
    global_contracts_pass = (
        certificate["contracts"]["projection_global_contract"]["pass"] is True  # type: ignore[index]
        and certificate["analytic_rows"][4]["charge_contract"]["pass"] is True  # type: ignore[index]
        and certificate["analytic_rows"][5]["global_reflection_contract"]["pass"] is True  # type: ignore[index]
    )
    all_pass = all((
        fixture_pass,
        certificate["all_pass"] is True,
        mutations["all_pass"] is True,
        source_pass,
        global_contracts_pass,
        not any(GATES.values()),
        not any(FORBIDDEN.values()),
    ))
    return {
        "all_pass": all_pass,
        "certificate": certificate,
        "certificate_fixture": {
            "canonical_bytes": certificate_bytes,
            "field_verified": field_verified,
            "fresh_verified": fresh_verified,
            "pass": fixture_pass,
            "sha256": certificate_sha,
        },
        "declarations": {
            "active_c11_is_in_scope": True,
            "analytic_source_for_full_mobius_correlation": "TPC-137 fixed determinant-two full-squarefree closure",
            "certificate_rows_are_analytic_proof": False,
            "external_payload_vendored": False,
            "git_source_rows": 95,
            "inherited_Johnston_Yang_and_Maynard_are_RH389_proof_inputs": False,
            "network_fetch_performed_by_build": False,
            "remote_logical_objects": 3,
            "Tao_role": "upstream Liouville input to TPC-137 only",
        },
        "forbidden_claims": FORBIDDEN,
        "gates": GATES,
        "mutations": mutations,
        "paper": "RH-389",
        "source_locks": source_locks,
        "status": "RH-389_active_c11_terminal_log_all_clock_capacity_certified",
        "theorem": {
            "absolute_capacity": "for every fixed q>=1, G_log(q)=6/pi^2-kappa2/2",
            "action_projection": "E_plus=E intersect (T x {+1}) is a subset of E, has nonnegative finite-X pointwise z*f gain, and preserves compatibility/universal safety",
            "active_c11_input": "D(n)=n-2,V(n)=n,determinant=2,fixed periodic rho; terminal-log contribution is zero",
            "all_clock_order": "sup_(fixed integers q>=1) G_log(q)=6/pi^2-kappa2/2 only after the individual fixed-q limits are formed; q=1 attains; no lim_X sup_q claim",
            "capacity_definition": "G_log(q):=max_(f in A_q)|L_q(f)|, where A_q is the finite family of universally distance-two-safe q-periodic lag-two tables",
            "charge_upper": "sum_r phase_weight_r <= sum_r [delta_(q,r)-theta_(q,r)/2]",
            "density_totals": "sum_r delta_(q,r)=6/pi^2 and sum_r theta_(q,r)=kappa2=prod_p(1-2/p^2)",
            "fixed_data_quantifier": "q and the safe q-periodic table family are fixed before X tends to infinity",
            "limit_formula": "L_q(f)=sum_(r mod q)[c02(r)*delta_(q,r)+c22(r)*theta_(q,r)]",
            "limit_theorem": "for every fixed q>=1, every fixed f in A_q, and every 1<=omega(X)<=X with omega(X)->infinity, lim_(X->infinity) S_X^omega(q,f)=L_q(f)",
            "limit_order": "take each fixed-table terminal-log limit, then maximize over the finite fixed-q family",
            "normalization": "1<=omega(X)<=X,omega(X)->infinity;(log omega(X))^-1*sum_(X/omega(X)<n<=X) score_n/n",
            "optimizer": "the constant action {-1,0}, table 36, attains the positive capacity for every fixed q",
            "reflection": "input reflection preserves safety; c02,c11,c22 negate, c01,c12,c21 remain and have zero limits; table 72 attains the negative capacity",
            "terminal_score": "S_X^omega(q,f):=(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)f_(n mod q)(mu0(n-2),mu(n))/n, with mu0(m)=mu(m) for m>=1 and 0 for m<=0",
        },
        "title": "Active-c11 Terminal-Log All-Clock Capacity",
    }


def main() -> None:
    payload = build_payload()
    if payload["all_pass"] is not True:
        raise RuntimeError("RH-389 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "git": 95, "remote": 3, "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
