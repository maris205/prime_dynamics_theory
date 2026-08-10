"""Build the offline immutable-source-locked RH-391 result."""

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

from moving_rank_necessity import (  # noqa: E402
    MUTATION_NAMES, build_certificate, canonical_json_bytes, mutation_results,
    payload_sha256, verify_certificate,
)
from source_locks import (  # noqa: E402
    EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
    JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, RH390_RELEASE,
    build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 10_062
CERTIFICATE_FIXTURE_SHA256 = "cc2874435e62205a3e969e841d80d37243d95826855bd242f0eff3478dccf367"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}
FORBIDDEN = {
    "arbitrary_single_vertex_rank_schedule": False,
    "different_rank_at_two_endpoints": False,
    "arbitrary_surrogate_necessity": False,
    "superlinear_r_over_x_to_infinity": False,
    "linear_rank_prime_tail_asymptotic": False,
    "johnston_yang_used_for_linear_rank": False,
    "complex_c": False,
    "active_c11": False,
    "ordinary_Cesaro_or_growing_clock": False,
    "K_N": False,
    "operator_trace_or_zeros": False,
    "proof_of_RH": False,
    "RH389_TPC137_or_Tao_proof_dependency": False,
    "vendored_external_source": False,
}
EXPECTED_FORBIDDEN_KEYS = frozenset({
    "arbitrary_single_vertex_rank_schedule", "different_rank_at_two_endpoints",
    "arbitrary_surrogate_necessity", "superlinear_r_over_x_to_infinity",
    "linear_rank_prime_tail_asymptotic", "johnston_yang_used_for_linear_rank",
    "complex_c", "active_c11", "ordinary_Cesaro_or_growing_clock", "K_N",
    "operator_trace_or_zeros", "proof_of_RH", "RH389_TPC137_or_Tao_proof_dependency",
    "vendored_external_source",
})


def _validate_constants() -> None:
    hashes = (CERTIFICATE_FIXTURE_SHA256, EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST, JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256)
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(RH390_RELEASE) is not str or not COMMIT_RE.fullmatch(RH390_RELEASE):
        raise ValueError("sealed release commit is malformed")
    if type(CERTIFICATE_FIXTURE_BYTES) is not int or type(CERTIFICATE_FIXTURE_BYTES) is bool or CERTIFICATE_FIXTURE_BYTES <= 0:
        raise ValueError("certificate fixture bytes must be a positive exact int")
    if set(GATES) != {"A_intrinsic_determinant", "B_scattering_completion", "C_self_adjoint_generator", "D_von_mangoldt_weighted_prime_power_traces", "E_completed_zeta_divisor_equality"}:
        raise ValueError("Gate A--E membership changed")
    if type(EXPECTED_FORBIDDEN_KEYS) is not frozenset or set(FORBIDDEN) != EXPECTED_FORBIDDEN_KEYS:
        raise ValueError("claim-firewall membership changed")
    if any(type(value) is not bool for value in (*GATES.values(), *FORBIDDEN.values())):
        raise TypeError("gate/firewall values must be exact booleans")


def pretty_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def build_payload() -> dict[str, object]:
    _validate_constants()
    certificate = build_certificate()
    verify_certificate(certificate, compare_fresh=False)
    certificate_bytes = len(canonical_json_bytes(certificate))
    certificate_sha = payload_sha256(certificate)
    fixture_pass = certificate_bytes == CERTIFICATE_FIXTURE_BYTES and certificate_sha == CERTIFICATE_FIXTURE_SHA256
    mutation_rows = mutation_results()
    mutation_pass = (
        type(mutation_rows) is list and len(mutation_rows) == 24
        and [row.get("name") for row in mutation_rows] == list(MUTATION_NAMES)
        and all(type(row) is dict and set(row) == {"name", "rejected"} and row["rejected"] is True for row in mutation_rows)
    )
    source_locks = build_source_closure()
    source_pass = (
        source_locks["pass"] is True and source_locks["git_count"] == 97
        and source_locks["remote_count"] == 2 and source_locks["logical_count"] == 99
        and source_locks["git"]["all_git_source_digest"] == EXPECTED_ALL_GIT_SOURCE_DIGEST
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
    )
    all_pass = all((fixture_pass, certificate["all_pass"] is True, mutation_pass, source_pass, not any(GATES.values()), not any(FORBIDDEN.values())))
    return {
        "status": "RH-391_linear_scale_moving_rank_prime_tail_retention_necessity_certified",
        "paper": "RH-391",
        "title": "Linear-Scale Moving-Rank Prime-Tail Retention Necessity",
        "certificate_fixture": {"canonical_bytes": certificate_bytes, "sha256": certificate_sha, "pass": fixture_pass},
        "certificate": certificate,
        "mutations": {
            "count": len(mutation_rows), "names": list(MUTATION_NAMES), "results": mutation_rows,
            "verification_mode": "exact per-row leaf seals plus independently recomputed semantic cross-contracts; false mode invokes no group or fresh builders",
            "all_pass": mutation_pass,
        },
        "source_locks": source_locks,
        "theorem": {
            "fixed_gap_extraction": "there exist one fixed positive integer h_*<=600 and infinitely many consecutive-prime edges x=p_y,q=p_(y+1)=x+h_*",
            "linear_rank_regime": "for each fixed C>0, exact same-edge ranks r=r_y satisfy r->infinity and r<=C*x",
            "optional_profile_regime": "the lambda profile additionally assumes r/x->lambda in [0,infinity)",
            "scalar_errors": "E_I=P_r-I_(2r), E_J=P_r-J_r",
            "endpoint_errors": "Delta_I=pi^2*(GapP-GapI_(<r)), Delta_J=pi^2*(GapP-GapJ_(<r))",
            "edge_factors": "a=(x^2/(q^2-1))^r, rho=(x/q)^(2r), rho/a=(1-q^(-2))^r",
            "scalar_edge_jumps": "x^(2r)*(E_I(x)-E_I(q))=a+o(1) and x^(2r)*(E_J(x)-E_J(q))=a+o(1)",
            "gamma_formula": "gamma_r=4/r*(3^r*u4-2^r*u3+5^r*u6-4^r*u5+7^r*u8-6^r*u7+2*(u3-u4+u5-u6+u7-u8))",
            "gamma_lower": "for exact r>=7,gamma_r>=kappa_gamma*7^r/r, kappa_gamma=4*u8_lower/7>0",
            "endpoint_edge_jumps": "x^(2r)*(Delta_I(x)-Delta_I(q))/gamma_r=a+o(1), and likewise for Delta_J",
            "natural_pair_profile": "for each of E_I,E_J,Delta_I/gamma_r,Delta_J/gamma_r, liminf ((1+rho)/a)*max{x^(2r)|left|,q^(2r)|right|}>=1",
            "lambda_pair_lower": "if r/x->lambda, a0=exp(-2*lambda*h_*), and every natural pair max has liminf at least a0/(1+a0)",
            "coarse_pair_lower": "under r<=C*x, every natural pair max has liminf at least exp(-1200*C)/2",
            "sublinear_pair_lower": "if r=o(x) and r->infinity, every natural pair max has liminf at least 1/2",
            "next_rank_divergence": "the scalar pair errors and gamma-normalized endpoint pair errors, divided by P_(r+1), tend to infinity",
            "necessity_scope": "same rank at both endpoints; pairwise P/J/I hierarchy only",
        },
        "source_roles": {
            "maynard": "bounded consecutive gaps plus finite-pigeonhole extraction of one repeated h_*",
            "johnston_yang": "inherited provenance only; not invoked for linear-r prime-tail asymptotics",
            "excluded_as_irrelevant": ["RH-389", "TPC-137", "Tao active-log source"],
        },
        "gates": GATES,
        "forbidden_claims": FORBIDDEN,
        "declarations": {
            "network_fetch_performed_by_build": False,
            "external_payload_vendored": False,
            "finite_rows_are_analytic_proof": False,
            "effective_edge_or_rank_threshold_computed": False,
            "git_source_rows": 97,
            "remote_logical_objects": 2,
            "logical_source_rows": 99,
        },
        "all_pass": all_pass,
    }


def main() -> None:
    payload = build_payload()
    if payload["all_pass"] is not True:
        raise RuntimeError("RH-391 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({"status": payload["status"], "all_pass": True, "git": 97, "remote": 2}, sort_keys=True))


if __name__ == "__main__":
    main()
