"""Build the offline immutable-source-locked RH-390 result."""

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

from growing_rank_filtration import (  # noqa: E402
    MUTATION_NAMES,
    build_certificate,
    canonical_json_bytes,
    mutation_results,
    payload_sha256,
    verify_certificate,
)
from source_locks import (  # noqa: E402
    EXPECTED_ALL_GIT_SOURCE_DIGEST,
    EXPECTED_LOGICAL_SOURCE_DIGEST,
    JY_CANONICAL_SHA256,
    MAYNARD_CANONICAL_SHA256,
    RH388_RELEASE,
    build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 17_571
CERTIFICATE_FIXTURE_SHA256 = "e2116abd4aeb910c24ee470a520623f29f1f454bb9b5293840875da091682b3b"
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
    "convergent_factorial_series": False,
    "growing_s_necessity": False,
    "arbitrary_surrogate_necessity": False,
    "complex_c": False,
    "active_c11": False,
    "growing_clock": False,
    "K_N": False,
    "operator_trace_or_zeros": False,
    "proof_of_RH": False,
    "RH389_TPC137_or_Tao_proof_dependency": False,
    "vendored_external_source": False,
}
EXPECTED_FORBIDDEN_KEYS = frozenset(
    {
        "convergent_factorial_series",
        "growing_s_necessity",
        "arbitrary_surrogate_necessity",
        "complex_c",
        "active_c11",
        "growing_clock",
        "K_N",
        "operator_trace_or_zeros",
        "proof_of_RH",
        "RH389_TPC137_or_Tao_proof_dependency",
        "vendored_external_source",
    }
)


def _validate_constants() -> None:
    hashes = (
        CERTIFICATE_FIXTURE_SHA256,
        EXPECTED_ALL_GIT_SOURCE_DIGEST,
        EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256,
        MAYNARD_CANONICAL_SHA256,
    )
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(RH388_RELEASE) is not str or not COMMIT_RE.fullmatch(RH388_RELEASE):
        raise ValueError("sealed release commit is malformed")
    if type(CERTIFICATE_FIXTURE_BYTES) is not int or type(CERTIFICATE_FIXTURE_BYTES) is bool or CERTIFICATE_FIXTURE_BYTES <= 0:
        raise ValueError("certificate fixture bytes must be a positive exact int")
    expected_gates = {
        "A_intrinsic_determinant",
        "B_scattering_completion",
        "C_self_adjoint_generator",
        "D_von_mangoldt_weighted_prime_power_traces",
        "E_completed_zeta_divisor_equality",
    }
    if set(GATES) != expected_gates:
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
        type(mutation_rows) is list
        and len(mutation_rows) == 24
        and [row.get("name") for row in mutation_rows] == list(MUTATION_NAMES)
        and all(type(row) is dict and set(row) == {"name", "rejected"} and row["rejected"] is True for row in mutation_rows)
    )
    source_locks = build_source_closure()
    source_pass = (
        source_locks["pass"] is True
        and source_locks["git_count"] == 87
        and source_locks["remote_count"] == 2
        and source_locks["logical_count"] == 89
        and source_locks["git"]["all_git_source_digest"] == EXPECTED_ALL_GIT_SOURCE_DIGEST  # type: ignore[index]
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
    )
    all_pass = all(
        (
            fixture_pass,
            certificate["all_pass"] is True,
            mutation_pass,
            source_pass,
            not any(GATES.values()),
            not any(FORBIDDEN.values()),
        )
    )
    return {
        "status": "RH-390_growing_rank_prime_tail_filtration_certified",
        "paper": "RH-390",
        "title": "Growing-Rank Prime-Tail Filtration and Fixed-Rank Necessity",
        "certificate_fixture": {
            "canonical_bytes": certificate_bytes,
            "sha256": certificate_sha,
            "pass": fixture_pass,
        },
        "certificate": certificate,
        "mutations": {
            "count": len(mutation_rows),
            "names": list(MUTATION_NAMES),
            "results": mutation_rows,
            "verification_mode": "independently recomputed field-level semantic verification without group or fresh builders",
            "all_pass": mutation_pass,
        },
        "source_locks": source_locks,
        "theorem": {
            "range": "x=p_y,L=log(x)>=512,fixed 0<delta<1,c in {1,...,7}",
            "rank_window": "exact integers 2<=s<=S_y=floor((1-delta)*log(L)/log(7))",
            "factorial_window": "exact integers 1<=K<=floor((2s-1)*L)",
            "retained_surrogate": "Psi_(c;s,K)=sum_(r<s)c^r*P_r/r+sum_(r>=s)c^r*K_r*S_K(a_r)/r",
            "kernel_definitions": "K_r=x^(1-2r)/((2r-1)*L),a_r=1/((2r-1)*L),S_K(a)=sum_(j=0)^(K-1)(-1)^j*j!*a^j",
            "A_s_c": "1/((1-x^-2)^s*(1-c/(x^2-1)))",
            "B_s_c": "1/((1-x^-2)^(s+1)*(1-c/(x^2-1)))",
            "C_c": "1/(1-c/x^2)",
            "normalized_coordinate_bound": "|PhiP_c-Psi_(c;s,K)|/K_s<=c^s*((4-1/s)*A_s_c*epsilon+((2s-1)/(2s+1))*B_s_c/x^2+C_c*K!/(s*((2s-1)*L)^K))",
            "endpoint_bound": "pi^2*|GapP-Gap_(s,K)|<=126*K_s*max_(1<=c<=7){normalized_coordinate_bound_rhs}",
            "uniform_window": "as y->infinity,max_(2<=s<=S_y,1<=K<=floor((2s-1)*L))|GapP-Gap_(s,K)|/P_s->0",
            "limit_variable": "y->infinity",
            "eventual_nonempty": "eventually S_y>=2",
            "gamma_formula": "gamma_(r)=4/r*(3^r*u4-2^r*u3+5^r*u6-4^r*u5+7^r*u8-6^r*u7+2*(u3-u4+u5-u6+u7-u8))",
            "gamma_positivity": "gamma_(r)>0 for every exact integer r>=1",
            "fixed_s_scalar_necessity": "for fixed exact integer s>=2,r=s-1,limsup_y p_y^(2r)*|P_r-I_(2r)|>=1/2",
            "GapI_less_r_definition": "F((sum_(j<r)c^j*P_j/j+sum_(j>=r)c^j*I_(2j)/j)_(c=1)^7)/pi^2",
            "GapJ_less_r_definition": "F((sum_(j<r)c^j*P_j/j+sum_(j>=r)c^j*J_j/j)_(c=1)^7)/pi^2",
            "fixed_s_endpoint_necessity_I": "limsup_y p_y^(2r)*pi^2*|GapP-GapI_(<r)|>=gamma_(r)/2",
            "fixed_s_endpoint_necessity_J": "limsup_y p_y^(2r)*pi^2*|GapP-GapJ_(<r)|>=gamma_(r)/2",
            "P_s_scale": "P_s~x^(1-2s)/((2s-1)*L)",
            "necessity_scope": "fixed s only in the frozen P/J/I hierarchy",
        },
        "source_roles": {
            "johnston_yang": "prime-counting envelope inherited through the RH-386/RH-388 closure",
            "maynard": "fixed-s consecutive bounded-gap necessity",
            "excluded_as_irrelevant": ["RH-389", "TPC-137", "Tao active-log source"],
        },
        "gates": GATES,
        "forbidden_claims": FORBIDDEN,
        "declarations": {
            "network_fetch_performed_by_build": False,
            "external_payload_vendored": False,
            "finite_rows_are_analytic_proof": False,
            "effective_least_y_computed": False,
            "git_source_rows": 87,
            "remote_logical_objects": 2,
            "logical_source_rows": 89,
        },
        "all_pass": all_pass,
    }


def main() -> None:
    payload = build_payload()
    if payload["all_pass"] is not True:
        raise RuntimeError("RH-390 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({"status": payload["status"], "all_pass": True, "git": 87, "remote": 2}, sort_keys=True))


if __name__ == "__main__":
    main()
