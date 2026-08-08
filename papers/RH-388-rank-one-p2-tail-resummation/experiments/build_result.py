"""Build the offline immutable-source-locked RH-388 result."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from rank_one_p2 import (  # noqa: E402
    build_certificate,
    canonical_json_bytes,
    mutation_results,
    payload_sha256,
    verify_certificate,
)
from source_locks import (  # noqa: E402
    EXPECTED_LOGICAL_SOURCE_DIGEST,
    MAYNARD_CANONICAL_SHA256,
    JY_CANONICAL_SHA256,
    build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 14_531
CERTIFICATE_FIXTURE_SHA256 = "373d870847bb0bf134aa1eba30c5e4d2c3a01dba470af9c75ebacadd81976371"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}

FORBIDDEN = {
    "convergent_factorial_series": False,
    "P3_or_cubic_precision": False,
    "complex_c": False,
    "growing_clock": False,
    "active_phasewise_c11": False,
    "K_N": False,
    "operator_trace_or_zeros": False,
    "proof_of_RH": False,
    "universal_impossibility_for_every_surrogate": False,
    "vendored_external_source": False,
}


def _validate_constants() -> None:
    hashes = (
        CERTIFICATE_FIXTURE_SHA256,
        EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256,
        MAYNARD_CANONICAL_SHA256,
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


def build_payload() -> dict[str, object]:
    _validate_constants()
    certificate = build_certificate()
    verify_certificate(certificate, compare_fresh=False)
    certificate_bytes = len(canonical_json_bytes(certificate))
    certificate_sha = payload_sha256(certificate)
    fixture_pass = (
        certificate_bytes == CERTIFICATE_FIXTURE_BYTES
        and certificate_sha == CERTIFICATE_FIXTURE_SHA256
    )
    mutations = mutation_results()
    source_locks = build_source_closure()
    source_pass = (
        source_locks["pass"] is True
        and source_locks["git_count"] == 77
        and source_locks["remote_count"] == 2
        and source_locks["logical_count"] == 79
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
    )
    all_pass = all(
        (
            fixture_pass,
            certificate["all_pass"] is True,
            mutations["all_pass"] is True,
            source_pass,
            not any(GATES.values()),
            not any(FORBIDDEN.values()),
        )
    )
    return {
        "status": "RH-388_rank_one_P2_tail_resummation_certified",
        "paper": "RH-388",
        "title": "Rank-One P_2-Scale Prime-Tail Resummation and Bounded-Gap Necessity",
        "certificate_fixture": {
            "canonical_bytes": certificate_bytes,
            "sha256": certificate_sha,
            "pass": fixture_pass,
        },
        "certificate": certificate,
        "mutations": {
            **mutations,
            "verification_mode": "independently recomputed field-level semantic verification without row/fresh builders",
        },
        "source_locks": source_locks,
        "theorem": {
            "range": "x=p_y,L=log(x)>=512,c in {1,...,7},integer 1<=K<=floor(3L)",
            "rank_one_surrogate": "Psi_c^[K]=c*P_1+sum_(r>=2)c^r*K_r*S_K(a_r)/r",
            "finite_bound": "pi^2*|GapP-GapK|<=x^-3/L*(7560*epsilon+1638/x^2+1176*K!/(3L)^K)",
            "uniform_window": "as y->infinity,max_(1<=K<=floor(3L))|GapP-GapK|/P_2 -> 0",
            "limit_variable": "y->infinity",
            "P2_scale": "P_2~1/(3*x^3*L)",
            "bounded_gap_scalar_necessity": "limsup_y p_y^2*|P_1(y)-I_2(p_y)|>=1/2",
            "bounded_gap_endpoint_necessity_I": "limsup_y p_y^2*pi^2*|GapP-GapI|>=X_infinity",
            "bounded_gap_endpoint_necessity_J": "limsup_y p_y^2*pi^2*|GapP-GapJ|>=X_infinity",
            "necessity_scope": "the frozen P/J/I smooth-surrogate hierarchy only",
            "endpoint_gradient_bound": "sup_[0,1/2]^7 ||grad F||_1<126",
            "endpoint_Hessian_bound": "sup_[0,1/2]^7 sum_ij|partial_ij F|<224",
            "Taylor_remainder": "|F(z)-gradF(0).z|<=112*||z||_infinity^2",
            "rank_one_direction": "gradF(0).(1,2,3,4,5,6,7)=2*X_infinity",
        },
        "gates": GATES,
        "forbidden_claims": FORBIDDEN,
        "declarations": {
            "network_fetch_performed_by_build": False,
            "external_payload_vendored": False,
            "finite_rows_are_analytic_proof": False,
            "Maynard_first_effective_gap_index_computed": False,
            "remote_logical_objects": 2,
            "git_source_rows": 77,
        },
        "all_pass": all_pass,
    }


def main() -> None:
    payload = build_payload()
    if payload["all_pass"] is not True:
        raise RuntimeError("RH-388 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "all_pass": True, "git": 77, "remote": 2}, sort_keys=True))


if __name__ == "__main__":
    main()
