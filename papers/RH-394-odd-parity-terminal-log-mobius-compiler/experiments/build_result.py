"""Build and independently validate the frozen RH-394 Stage-1 result."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from odd_parity_compiler.core import (  # noqa: E402
    MUTATION_NAMES, TITLE, build_certificate, mutate_certificate,
    verify_certificate,
)
from source_locks import (  # noqa: E402
    EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
    EXPECTED_REMOTE_ROLES, JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256,
    SOURCE_RELEASE, TAO_CANONICAL_SHA256, TAO_TERAVAINEN_CANONICAL_SHA256,
    build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 108_636
CERTIFICATE_FIXTURE_SHA256 = "3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998"
CORE_FILE_SHA256 = "3b24da1f1c54e69f98b2e1d07209d24928dbb3493a3fcc386c0bcf751dde4c85"
SOURCE_BUILDER_SHA256 = "2171aa240afbc8add45fec589545fc2e1490a971da3fc72cf772559e17de51e9"
SOURCE_CLOSURE_BYTES = 47_785
SOURCE_CLOSURE_SHA256 = "8028373a8e8d7f10061c70872a72dc9c55654f9730de9fe2de19b7a4b3696501"
THEOREM_CONTRACT_SHA256 = "1270f9adb52072305c0bfb56b420fe508bb2a66ba49e4cdab9469a194179a644"
SOURCE_ROLE_SHA256 = "a599d8e2128cc6060141fab94b2738da5dc388866c3852ea3015b83fd0d2b4f6"
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
    "even_odd_support_at_least_four": False,
    "unrestricted_m_at_least_four_truth_tables": False,
    "growing_m": False,
    "growing_q": False,
    "growing_shift_family": False,
    "growing_periodic_masks": False,
    "growing_phase_coefficients": False,
    "X_dependent_coefficients": False,
    "effective_uniform_rate": False,
    "ordinary_Cesaro_average": False,
    "maximum_before_terminal_limit": False,
    "adaptive_or_prelimit_capacity": False,
    "generic_graph_coupled_capacity": False,
    "even_order_Chowla_input_proved": False,
    "missing_m4_channel_classified_as_nonzero": False,
    "missing_m4_channel_classified_as_nonconvergent": False,
    "finite_certificate_is_analytic_proof": False,
    "Tao_Teravainen_used_for_even_total_power": False,
    "RH393_used_for_odd_support_at_least_three": False,
    "new_squarefree_density_landscape_claim": False,
    "operator_model": False,
    "trace_formula": False,
    "zero_model": False,
    "proof_of_Riemann_Hypothesis": False,
    "Gate_A": False,
    "Gate_B": False,
    "Gate_C": False,
    "Gate_D": False,
    "Gate_E": False,
    "vendored_external_payload": False,
}


THEOREM_CONTRACTS = {
    "terminal_clock": {
        "mobius_extension": "mu_0(t)=mu(t) for t>=1 and mu_0(t)=0 for t<=0",
        "admissible": "1<=omega(X)<=X eventually and omega(X)->infinity",
        "interval": "X/omega(X)<n<=X",
        "normalization": "1/log(omega(X))",
        "limit": "X->infinity",
    },
    "odd_parity_compiler": {
        "quantifiers": (
            "for every fixed integer m>=1, fixed integer q>=1, fixed pairwise-distinct "
            "integer shifts a_1,...,a_m, fixed q-periodic coefficients c_alpha(r), "
            "and every admissible terminal clock omega"
        ),
        "coordinates": "z_i(n)=mu_0(n-a_i)",
        "odd_support": "O(alpha)={i:alpha_i=1}",
        "even_support": "E(alpha)={i:alpha_i=2}",
        "admitted_support_sizes": "|O(alpha)| is 0, 2, or a positive odd integer",
        "polynomial": (
            "P_r(z)=sum over admitted alpha in {0,1,2}^m of "
            "c_alpha(r) product_i z_i^alpha_i"
        ),
        "functional": (
            "T_X=[log omega(X)]^-1 sum_(X/omega(X)<n<=X) "
            "P_(n mod q)(z_1(n),...,z_m(n))/n"
        ),
        "limit": (
            "sum_(r mod q) sum_(alpha in {0,2}^m) "
            "c_alpha(r) Theta_(q,r)(E(alpha))"
        ),
        "surviving_channels": "exactly O(alpha)=empty",
        "vanishing_channels": "every admitted alpha with nonempty O(alpha)",
        "dimension": "D'_m=2^m+binom(m,2)2^(m-2)+(3^m-1)/2, absent m<2 term zero",
    },
    "phase_density": {
        "B_p": "distinct set {a_i mod p^2:i in E}",
        "nu_p": "cardinality of B_p",
        "tau_p_r": "#{b in B_p:b mod p=r mod p}, after mod-p^2 deduplication",
        "Theta": (
            "Theta_(q,r)(E)=q^-1 product_(p not|q)(1-nu_p/p^2) "
            "product_(p||q)(1-tau_p_r/p) "
            "product_(p^2|q)1_(r mod p^2 notin B_p)"
        ),
        "empty_support": "Theta_(q,r)(empty)=1/q",
        "phase_sum": "sum_(r mod q)Theta_(q,r)(E)=product_p(1-nu_p/p^2)",
        "collision_rule": "distinct mod-p^2 classes may collide modulo p",
    },
    "exact_support_table_law": {
        "stratum": "U={i:z_i is nonzero}",
        "Pi": (
            "Pi_(q,r)(U)=sum_(W subset [m]\\U)(-1)^|W| "
            "Theta_(q,r)(U union W)"
        ),
        "probability": "Pi_(q,r)(U)>=0 and sum_U Pi_(q,r)(U)=1/q",
        "sign_average": "bar f_(r,U)=2^(-|U|)sum_(epsilon in {+1,-1}^U)f_r(epsilon_U,0)",
        "limit": "sum_(r mod q)sum_(U subset [m])Pi_(q,r)(U) bar f_(r,U)",
    },
    "proof_decomposition": {
        "odd_zero": "local finite-prime CRT and union tail prove Theta and Pi",
        "odd_two": "frozen RH393 compiler, ultimately RH392 two-form terminal cancellation",
        "positive_odd": (
            "Tao--Teravainen Corollary 1.8 with positive exponents alpha_i in {1,2}; "
            "the exponent sum is odd"
        ),
        "phase_bridge": (
            "on n=q*t+r use Remark 1.5 and Theorem A.1; "
            "1/(q*t+r)=1/(q*t)+O(t^-2), endpoint error O(1), and the "
            "terminal harmonic denominator divided by log omega tends to one"
        ),
        "fixed_only": "all data are fixed before X->infinity",
    },
    "intrinsic_classification": {
        "full_table": (
            "on every nonzero-support Boolean stratum U, the even part "
            "h_U^+(epsilon)=[h_U(epsilon)+h_U(-epsilon)]/2 has Fourier degree <=2"
        ),
        "coefficient_relation": (
            "hat h_S(O)=sum_(E subset S\\O)c_(O,E); Boolean-stratum vanishing "
            "and subset inversion are equivalent to the coefficient rule"
        ),
        "current_table": (
            "for g(x,z)=z f(x), every stratum odd part h_U^- has Fourier degree <=1"
        ),
        "linear_forms": "L=0, +/-x_i, or (+/-x_i+/-x_j)/2",
        "M_0": 2,
        "M_1": 4,
        "M_k": (
            "2^(2^(k-1))+2k+4*binom(k,2)*2^(2^(k-2)) for k>=2"
        ),
        "B_d": "product_(k=0)^d M_k^binom(d,k)",
        "phase_families": "B_d^q",
    },
    "complete_three_shift_law": {
        "dimension": "D'_3=27=3^3",
        "full_tables": "every f:{-1,0,1}^3->R is covered",
        "full_sign_table_phase_families": "2^(27q)",
        "distinguished_current": "B_2=512, hence all 512^q fixed q-phase families cancel",
        "conclusion": "every fixed three-shift coordinatewise-quadratic table has the exact Pi limit",
    },
    "four_shift_boundary": {
        "dimension": "D'_4=80 of 81",
        "excluded_coefficient": "only c_1111",
        "criterion": (
            "c_1111=2^-4 sum_(epsilon in {+1,-1}^4) "
            "epsilon_1 epsilon_2 epsilon_3 epsilon_4 f(epsilon)=0"
        ),
        "boolean_corner_patterns": "binom(16,8)=12870",
        "ternary_truth_tables_per_phase": "binom(16,8)*2^65",
        "q_phase_families": "[binom(16,8)*2^65]^q",
        "outside": "failure of the criterion means outside this theorem only",
    },
}


SOURCE_ROLES = {
    "RH393": (
        "direct frozen predecessor for the all-even local Theta law and the "
        "two-odd channel; RH394's release-bound Git base has 128 objects, while "
        "the three prior canonical remotes are inherited and TT is the fourth"
    ),
    "tao-teravainen-arxiv-1708.02610v2": (
        "new direct analytic input: Corollary 1.8 gives odd-total-power Mobius "
        "cancellation; Remark 1.5 and Theorem A.1 give the fixed affine bridge"
    ),
    "tao-cambridge-2016-logarithmic-chowla": (
        "inherited through RH393 for the two-form channel; not the new odd-order input"
    ),
    "johnston-yang-arxiv-2204.01980v2": "closure-only; not used in the RH394 proof",
    "maynard-annals-2015-small-gaps": "closure-only; not used in the RH394 proof",
    "finite_certificate": "exact reproduction and mutation audit, not analytic proof",
}


RESULT_MUTATION_NAMES = (
    "all_pass", "title", "paper", "status", "certificate_body",
    "certificate_bytes", "certificate_hash", "core_hash", "declaration_network",
    "declaration_vendor", "declaration_proof", "declaration_rate",
    "declaration_git_count", "finite_m3", "finite_m4", "finite_cube",
    "finite_B2", "forbidden_true", "forbidden_missing", "gate_true",
    "mutation_count", "mutation_name", "mutation_rejected", "source_fixture_hash",
    "source_git_count", "source_logical_digest", "source_offline", "source_payload",
    "source_rights", "source_role", "theorem_clock", "theorem_support",
)

RESULT_BUILDER_NAMES = (
    "build_payload", "_certificate_mutation_rows", "build_certificate",
    "build_source_closure", "mutate_certificate", "verify_certificate",
)

RESULT_HELPER_NAMES = (
    "canonical_bytes", "payload_sha256", "pretty_json_bytes", "exact_equal",
    "loads_strict", "_validate_constants",
)


def _reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def loads_strict(text: str) -> Any:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(
        text, object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def pretty_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def payload_sha256(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def exact_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def _validate_constants() -> None:
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    def same(left: Any, right: Any) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(same(left[key], right[key]) for key in left)
        if type(left) in (list, tuple):
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        return left == right

    def sealed_sha(value: Any) -> str:
        raw = local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return local_sha256(raw).hexdigest()

    expected_hashes = {
        "certificate": "3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998",
        "core": "3b24da1f1c54e69f98b2e1d07209d24928dbb3493a3fcc386c0bcf751dde4c85",
        "source_builder": "2171aa240afbc8add45fec589545fc2e1490a971da3fc72cf772559e17de51e9",
        "source_closure": "8028373a8e8d7f10061c70872a72dc9c55654f9730de9fe2de19b7a4b3696501",
        "theorems": "1270f9adb52072305c0bfb56b420fe508bb2a66ba49e4cdab9469a194179a644",
        "source_roles": "a599d8e2128cc6060141fab94b2738da5dc388866c3852ea3015b83fd0d2b4f6",
        "all_git": "90f427889b714a7544e4eb68e6df565e32dab4114e656d99f7a24074a7a56951",
        "logical": "07c9ed6c0c79d77098e19d8102b4267ea4af637ae2d72148c412cc626af738ac",
        "jy": "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786",
        "maynard": "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e",
        "tao": "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84",
        "tt": "a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058",
    }
    actual_hashes = {
        "certificate": CERTIFICATE_FIXTURE_SHA256,
        "core": CORE_FILE_SHA256,
        "source_builder": SOURCE_BUILDER_SHA256,
        "source_closure": SOURCE_CLOSURE_SHA256,
        "theorems": THEOREM_CONTRACT_SHA256,
        "source_roles": SOURCE_ROLE_SHA256,
        "all_git": EXPECTED_ALL_GIT_SOURCE_DIGEST,
        "logical": EXPECTED_LOGICAL_SOURCE_DIGEST,
        "jy": JY_CANONICAL_SHA256,
        "maynard": MAYNARD_CANONICAL_SHA256,
        "tao": TAO_CANONICAL_SHA256,
        "tt": TAO_TERAVAINEN_CANONICAL_SHA256,
    }
    expected_gates = {
        "A_intrinsic_determinant": False,
        "B_scattering_completion": False,
        "C_self_adjoint_generator": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    expected_forbidden = {
        "even_odd_support_at_least_four", "unrestricted_m_at_least_four_truth_tables",
        "growing_m", "growing_q", "growing_shift_family", "growing_periodic_masks",
        "growing_phase_coefficients", "X_dependent_coefficients",
        "effective_uniform_rate", "ordinary_Cesaro_average",
        "maximum_before_terminal_limit", "adaptive_or_prelimit_capacity",
        "generic_graph_coupled_capacity", "even_order_Chowla_input_proved",
        "missing_m4_channel_classified_as_nonzero",
        "missing_m4_channel_classified_as_nonconvergent",
        "finite_certificate_is_analytic_proof",
        "Tao_Teravainen_used_for_even_total_power",
        "RH393_used_for_odd_support_at_least_three",
        "new_squarefree_density_landscape_claim", "operator_model", "trace_formula",
        "zero_model", "proof_of_Riemann_Hypothesis", "Gate_A", "Gate_B", "Gate_C",
        "Gate_D", "Gate_E", "vendored_external_payload",
    }
    expected_mutations = (
        "title", "role", "schema_version_float", "row_partition_float", "row_count",
        "monomial_alpha", "monomial_odd_count", "monomial_admitted", "monomial_channel",
        "histogram_numerator", "histogram_count", "histogram_eligible",
        "current_table_id", "current_corner_alt", "current_eligible",
        "dimension_admitted", "dimension_total", "stratum_count", "current_count",
        "phase_pi", "phase_theta", "phase_recovered", "analytic_clock",
        "analytic_source", "analytic_phase_bridge", "analytic_support_rule",
        "analytic_limit", "firewall_true", "summary_m3", "summary_m4",
        "summary_table_count", "summary_phase_mass",
    )
    expected_result_mutations = (
        "all_pass", "title", "paper", "status", "certificate_body",
        "certificate_bytes", "certificate_hash", "core_hash", "declaration_network",
        "declaration_vendor", "declaration_proof", "declaration_rate",
        "declaration_git_count", "finite_m3", "finite_m4", "finite_cube",
        "finite_B2", "forbidden_true", "forbidden_missing", "gate_true",
        "mutation_count", "mutation_name", "mutation_rejected", "source_fixture_hash",
        "source_git_count", "source_logical_digest", "source_offline", "source_payload",
        "source_rights", "source_role", "theorem_clock", "theorem_support",
    )
    if not same(actual_hashes, expected_hashes):
        raise ValueError("independent result hash contract changed")
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in actual_hashes.values()):
        raise ValueError("result SHA-256 constant malformed")
    if (
        type(TITLE) is not str
        or TITLE != "Odd-Parity Terminal-Log Möbius Compiler and the Complete Three-Shift Table Law"
        or SOURCE_RELEASE != "6fed36f44183a2794a3a814493ff602c5dc9314b"
        or not COMMIT_RE.fullmatch(SOURCE_RELEASE)
        or CERTIFICATE_FIXTURE_BYTES != 108_636
        or SOURCE_CLOSURE_BYTES != 47_785
    ):
        raise ValueError("frozen identity/size contract changed")
    if not same(GATES, expected_gates):
        raise ValueError("Gate contract changed")
    if set(FORBIDDEN) != expected_forbidden or any(value is not False for value in FORBIDDEN.values()):
        raise ValueError("forbidden-claim membership changed")
    if MUTATION_NAMES != expected_mutations or RESULT_MUTATION_NAMES != expected_result_mutations:
        raise ValueError("mutation-name contract changed")
    if len(set(MUTATION_NAMES)) != 32 or len(set(RESULT_MUTATION_NAMES)) != 32:
        raise ValueError("mutation names must be 32 unique strings")
    if sealed_sha(THEOREM_CONTRACTS) != THEOREM_CONTRACT_SHA256:
        raise ValueError("theorem contract body changed")
    if sealed_sha(SOURCE_ROLES) != SOURCE_ROLE_SHA256:
        raise ValueError("source-role contract body changed")
    expected_remote_roles = {
        "johnston-yang-arxiv-2204.01980v2": "closure_only_quantitative_PNT_input",
        "maynard-annals-2015-small-gaps": "closure_only_bounded_gap_input",
        "tao-cambridge-2016-logarithmic-chowla": "inherited_direct_two_point_odd_support_input",
        "tao-teravainen-arxiv-1708.02610v2": "direct_odd_parity_terminal_log_Mobius_input",
    }
    if not same(EXPECTED_REMOTE_ROLES, expected_remote_roles):
        raise ValueError("remote role contract changed")


def _certificate_mutation_rows(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "rejected": verify_certificate(
                mutate_certificate(certificate, name), compare_fresh=False
            ) is False,
        }
        for name in MUTATION_NAMES
    ]


def _finite_contracts(certificate: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_partition": deepcopy(certificate["row_partition"]),
        "dimensions": {
            "m3": deepcopy(certificate["dimension_rows"][2]),
            "m4": deepcopy(certificate["dimension_rows"][3]),
        },
        "signed_four_cube": {
            "eligible_corner_patterns": certificate["summary"]["m4_boolean_corner_eligible"],
            "ternary_truth_tables": certificate["summary"]["m4_ternary_table_count"],
            "free_noncorner_bits": 65,
        },
        "current_tables": {
            "two_input": certificate["summary"]["B_2"],
            "three_input": certificate["summary"]["B_3"],
            "all_two_input_tables_cancel": all(
                row["eligible"] is True for row in certificate["current_table_rows"]
            ),
            "M_0_through_4": [row["M_k"] for row in certificate["stratum_rows"][:5]],
        },
        "phase_fixture": {
            "rows": len(certificate["phase_rows"]),
            "all_inversion_pass": all(row["pass"] is True for row in certificate["phase_rows"]),
            "mass_numerator": certificate["summary"]["phase_pi_mass_numerator"],
        },
        "analytic_claims": [row["claim"] for row in certificate["analytic_rows"]],
        "firewall_names": [row["claim"] for row in certificate["firewall_rows"]],
    }


def build_payload() -> dict[str, Any]:
    _validate_constants()
    certificate = build_certificate()
    certificate_raw = canonical_bytes(certificate)
    certificate_pass = (
        len(certificate_raw) == CERTIFICATE_FIXTURE_BYTES
        and sha256(certificate_raw).hexdigest() == CERTIFICATE_FIXTURE_SHA256
        and verify_certificate(certificate, compare_fresh=False) is True
        and verify_certificate(certificate, compare_fresh=True) is True
    )
    core_sha = sha256((ROOT / "src" / "odd_parity_compiler" / "core.py").read_bytes()).hexdigest()
    core_pass = core_sha == CORE_FILE_SHA256
    source_builder_sha = sha256((ROOT / "experiments" / "source_locks.py").read_bytes()).hexdigest()
    source_locks = build_source_closure()
    source_raw = canonical_bytes(source_locks)
    source_sha = sha256(source_raw).hexdigest()
    source_pass = (
        source_builder_sha == SOURCE_BUILDER_SHA256
        and len(source_raw) == SOURCE_CLOSURE_BYTES
        and source_sha == SOURCE_CLOSURE_SHA256
        and source_locks["pass"] is True
        and (source_locks["git_count"], source_locks["remote_count"], source_locks["logical_count"])
        == (128, 4, 132)
        and source_locks["git"]["all_git_source_digest"] == EXPECTED_ALL_GIT_SOURCE_DIGEST
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_locks["remote"]["network_fetch_performed"] is False
        and source_locks["remote"]["external_payload_hash_hits"] == []
        and source_locks["remote"]["redistributable_in_release"] == [False, False, True, False]
    )
    mutation_rows = _certificate_mutation_rows(certificate)
    mutations_pass = (
        len(mutation_rows) == 32
        and len({row["name"] for row in mutation_rows}) == 32
        and all(row["rejected"] is True for row in mutation_rows)
    )
    finite = _finite_contracts(certificate)
    declarations = {
        "network_fetch_performed_by_build": False,
        "external_payload_vendored": False,
        "finite_certificate_is_analytic_proof": False,
        "effective_rate_computed": False,
        "git_source_rows": 128,
        "remote_logical_objects": 4,
        "logical_source_rows": 132,
        "rights_vector": [False, False, True, False],
    }
    all_pass = all((
        certificate_pass,
        core_pass,
        source_pass,
        mutations_pass,
        certificate["all_pass"] is True,
        finite["dimensions"]["m3"]["admitted"] == 27,
        finite["dimensions"]["m3"]["total"] == 27,
        finite["dimensions"]["m4"]["admitted"] == 80,
        finite["dimensions"]["m4"]["total"] == 81,
        finite["signed_four_cube"]["eligible_corner_patterns"] == 12_870,
        finite["signed_four_cube"]["ternary_truth_tables"] == 12_870 * 2**65,
        finite["current_tables"]["two_input"] == 512,
        finite["current_tables"]["three_input"] == 36_700_160,
        finite["current_tables"]["all_two_input_tables_cancel"] is True,
        not any(GATES.values()),
        not any(FORBIDDEN.values()),
    ))
    return {
        "all_pass": all_pass,
        "certificate": certificate,
        "certificate_fixture": {
            "canonical_bytes": len(certificate_raw),
            "sha256": sha256(certificate_raw).hexdigest(),
            "pass": certificate_pass,
        },
        "core_fixture": {"sha256": core_sha, "pass": core_pass},
        "declarations": declarations,
        "finite_contracts": finite,
        "forbidden_claims": deepcopy(FORBIDDEN),
        "gates": deepcopy(GATES),
        "mutations": {
            "count": len(mutation_rows),
            "names": list(MUTATION_NAMES),
            "results": mutation_rows,
            "all_pass": mutations_pass,
        },
        "paper": "RH-394",
        "source_fixture": {
            "canonical_bytes": len(source_raw),
            "sha256": source_sha,
            "builder_sha256": source_builder_sha,
            "pass": source_pass,
        },
        "source_locks": source_locks,
        "source_roles": deepcopy(SOURCE_ROLES),
        "status": "RH-394_odd_parity_terminal_log_mobius_compiler_certified",
        "theorems": deepcopy(THEOREM_CONTRACTS),
        "title": TITLE,
    }


def _make_result_validator():
    sealed_validate = _validate_constants
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    def local_bytes(value: Any) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def same(left: Any, right: Any) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(same(left[key], right[key]) for key in left)
        if type(left) in (list, tuple):
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        return left == right

    def validator(payload: Any, *, compare_fresh: bool = True) -> bool:
        if type(compare_fresh) is not bool:
            return False
        try:
            sealed_validate()
            if type(payload) is not dict or set(payload) != {
                "all_pass", "certificate", "certificate_fixture", "core_fixture",
                "declarations", "finite_contracts", "forbidden_claims", "gates",
                "mutations", "paper", "source_fixture", "source_locks", "source_roles",
                "status", "theorems", "title",
            }:
                return False
            if not (
                payload["all_pass"] is True
                and payload["paper"] == "RH-394"
                and payload["title"]
                == "Odd-Parity Terminal-Log Möbius Compiler and the Complete Three-Shift Table Law"
                and payload["status"]
                == "RH-394_odd_parity_terminal_log_mobius_compiler_certified"
            ):
                return False
            cert_raw = local_bytes(payload["certificate"])
            if not (
                len(cert_raw) == 108_636
                and local_sha256(cert_raw).hexdigest()
                == "3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998"
                and payload["certificate"].get("all_pass") is True
                and payload["certificate"].get("summary", {}).get("m3_admitted") == 27
                and payload["certificate"].get("summary", {}).get("m4_admitted") == 80
            ):
                return False
            if not same(payload["certificate_fixture"], {
                "canonical_bytes": 108_636,
                "sha256": "3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998",
                "pass": True,
            }):
                return False
            if not same(payload["core_fixture"], {
                "sha256": "3b24da1f1c54e69f98b2e1d07209d24928dbb3493a3fcc386c0bcf751dde4c85",
                "pass": True,
            }):
                return False
            expected_declarations = {
                "network_fetch_performed_by_build": False,
                "external_payload_vendored": False,
                "finite_certificate_is_analytic_proof": False,
                "effective_rate_computed": False,
                "git_source_rows": 128,
                "remote_logical_objects": 4,
                "logical_source_rows": 132,
                "rights_vector": [False, False, True, False],
            }
            if not same(payload["declarations"], expected_declarations):
                return False
            finite = payload["finite_contracts"]
            expected_finite = {
                "row_partition": [81, 17, 512, 8, 8, 8, 8, 8, 8],
                "dimensions": {
                    "m3": {
                        "m": 3, "all_even": 8, "two_odd": 6, "positive_odd": 13,
                        "admitted": 27, "total": 27,
                    },
                    "m4": {
                        "m": 4, "all_even": 16, "two_odd": 24, "positive_odd": 40,
                        "admitted": 80, "total": 81,
                    },
                },
                "signed_four_cube": {
                    "eligible_corner_patterns": 12_870,
                    "ternary_truth_tables": 12_870 * 2**65,
                    "free_noncorner_bits": 65,
                },
                "current_tables": {
                    "two_input": 512,
                    "three_input": 36_700_160,
                    "all_two_input_tables_cancel": True,
                    "M_0_through_4": [2, 4, 16, 70, 648],
                },
                "phase_fixture": {
                    "rows": 8, "all_inversion_pass": True, "mass_numerator": 20,
                },
                "analytic_claims": [
                    "fixed_terminal_quantifiers", "odd_total_power_source",
                    "fixed_affine_phase_bridge", "admitted_supports", "coefficient_limit",
                    "table_limit", "intrinsic_full_table_test", "intrinsic_current_test",
                ],
                "firewall_names": [
                    "even_odd_support_at_least_four", "unrestricted_m_at_least_four_tables",
                    "growing_m_q_shifts_masks_or_coefficients", "effective_uniform_rate",
                    "ordinary_cesaro", "maximum_before_limit",
                    "generic_graph_coupled_capacity", "operator_trace_zero_or_gate",
                ],
            }
            if not same(finite, expected_finite):
                return False
            expected_gate_keys = {
                "A_intrinsic_determinant", "B_scattering_completion",
                "C_self_adjoint_generator", "D_von_mangoldt_weighted_prime_power_traces",
                "E_completed_zeta_divisor_equality",
            }
            expected_forbidden_keys = {
                "even_odd_support_at_least_four", "unrestricted_m_at_least_four_truth_tables",
                "growing_m", "growing_q", "growing_shift_family", "growing_periodic_masks",
                "growing_phase_coefficients", "X_dependent_coefficients",
                "effective_uniform_rate", "ordinary_Cesaro_average",
                "maximum_before_terminal_limit", "adaptive_or_prelimit_capacity",
                "generic_graph_coupled_capacity", "even_order_Chowla_input_proved",
                "missing_m4_channel_classified_as_nonzero",
                "missing_m4_channel_classified_as_nonconvergent",
                "finite_certificate_is_analytic_proof",
                "Tao_Teravainen_used_for_even_total_power",
                "RH393_used_for_odd_support_at_least_three",
                "new_squarefree_density_landscape_claim", "operator_model", "trace_formula",
                "zero_model", "proof_of_Riemann_Hypothesis", "Gate_A", "Gate_B", "Gate_C",
                "Gate_D", "Gate_E", "vendored_external_payload",
            }
            if (
                type(payload["gates"]) is not dict
                or set(payload["gates"]) != expected_gate_keys
                or any(value is not False for value in payload["gates"].values())
                or type(payload["forbidden_claims"]) is not dict
                or set(payload["forbidden_claims"]) != expected_forbidden_keys
                or any(value is not False for value in payload["forbidden_claims"].values())
            ):
                return False
            mutations = payload["mutations"]
            expected_names = [
                "title", "role", "schema_version_float", "row_partition_float", "row_count",
                "monomial_alpha", "monomial_odd_count", "monomial_admitted", "monomial_channel",
                "histogram_numerator", "histogram_count", "histogram_eligible",
                "current_table_id", "current_corner_alt", "current_eligible",
                "dimension_admitted", "dimension_total", "stratum_count", "current_count",
                "phase_pi", "phase_theta", "phase_recovered", "analytic_clock",
                "analytic_source", "analytic_phase_bridge", "analytic_support_rule",
                "analytic_limit", "firewall_true", "summary_m3", "summary_m4",
                "summary_table_count", "summary_phase_mass",
            ]
            if not (
                type(mutations) is dict
                and set(mutations) == {"count", "names", "results", "all_pass"}
                and type(mutations["count"]) is int and type(mutations["count"]) is not bool
                and mutations["count"] == 32
                and mutations["names"] == expected_names
                and mutations["all_pass"] is True
                and type(mutations["results"]) is list
                and len(mutations["results"]) == 32
                and all(
                    type(row) is dict
                    and set(row) == {"name", "rejected"}
                    and row["name"] == name
                    and row["rejected"] is True
                    for name, row in zip(expected_names, mutations["results"])
                )
            ):
                return False
            source_raw = local_bytes(payload["source_locks"])
            if not (
                len(source_raw) == 47_785
                and local_sha256(source_raw).hexdigest()
                == "8028373a8e8d7f10061c70872a72dc9c55654f9730de9fe2de19b7a4b3696501"
                and payload["source_locks"].get("pass") is True
                and (
                    payload["source_locks"].get("git_count"),
                    payload["source_locks"].get("remote_count"),
                    payload["source_locks"].get("logical_count"),
                ) == (128, 4, 132)
                and payload["source_locks"].get("logical_source_digest")
                == "07c9ed6c0c79d77098e19d8102b4267ea4af637ae2d72148c412cc626af738ac"
                and payload["source_locks"]["remote"].get("network_fetch_performed") is False
                and payload["source_locks"]["remote"].get("external_payload_hash_hits") == []
                and payload["source_locks"]["remote"].get("redistributable_in_release")
                == [False, False, True, False]
            ):
                return False
            if not same(payload["source_fixture"], {
                "canonical_bytes": 47_785,
                "sha256": "8028373a8e8d7f10061c70872a72dc9c55654f9730de9fe2de19b7a4b3696501",
                "builder_sha256": "2171aa240afbc8add45fec589545fc2e1490a971da3fc72cf772559e17de51e9",
                "pass": True,
            }):
                return False
            if not same(payload["theorems"], THEOREM_CONTRACTS):
                return False
            if not same(payload["source_roles"], SOURCE_ROLES):
                return False
        except (KeyError, TypeError, ValueError, OverflowError):
            return False
        if compare_fresh:
            return same(payload, build_payload())
        return True

    return validator


validate_result_payload = _make_result_validator()
del _make_result_validator


def mutate_result_payload(payload: dict[str, Any], name: str) -> dict[str, Any]:
    if type(name) is not str or name not in RESULT_MUTATION_NAMES:
        raise ValueError("unknown result mutation")
    changed = deepcopy(payload)
    actions = {
        "all_pass": lambda: changed.__setitem__("all_pass", False),
        "title": lambda: changed.__setitem__("title", "wrong"),
        "paper": lambda: changed.__setitem__("paper", "RH-393"),
        "status": lambda: changed.__setitem__("status", "wrong"),
        "certificate_body": lambda: changed["certificate"]["summary"].__setitem__("m3_admitted", 26),
        "certificate_bytes": lambda: changed["certificate_fixture"].__setitem__("canonical_bytes", 108635),
        "certificate_hash": lambda: changed["certificate_fixture"].__setitem__("sha256", "0" * 64),
        "core_hash": lambda: changed["core_fixture"].__setitem__("sha256", "0" * 64),
        "declaration_network": lambda: changed["declarations"].__setitem__("network_fetch_performed_by_build", True),
        "declaration_vendor": lambda: changed["declarations"].__setitem__("external_payload_vendored", True),
        "declaration_proof": lambda: changed["declarations"].__setitem__("finite_certificate_is_analytic_proof", True),
        "declaration_rate": lambda: changed["declarations"].__setitem__("effective_rate_computed", True),
        "declaration_git_count": lambda: changed["declarations"].__setitem__("git_source_rows", 127),
        "finite_m3": lambda: changed["finite_contracts"]["dimensions"]["m3"].__setitem__("admitted", 26),
        "finite_m4": lambda: changed["finite_contracts"]["dimensions"]["m4"].__setitem__("admitted", 81),
        "finite_cube": lambda: changed["finite_contracts"]["signed_four_cube"].__setitem__("eligible_corner_patterns", 12871),
        "finite_B2": lambda: changed["finite_contracts"]["current_tables"].__setitem__("two_input", 511),
        "forbidden_true": lambda: changed["forbidden_claims"].__setitem__("effective_uniform_rate", True),
        "forbidden_missing": lambda: changed["forbidden_claims"].pop("ordinary_Cesaro_average"),
        "gate_true": lambda: changed["gates"].__setitem__("Gate_A" if "Gate_A" in changed["gates"] else "A_intrinsic_determinant", True),
        "mutation_count": lambda: changed["mutations"].__setitem__("count", 31),
        "mutation_name": lambda: changed["mutations"]["names"].__setitem__(0, "wrong"),
        "mutation_rejected": lambda: changed["mutations"]["results"][0].__setitem__("rejected", False),
        "source_fixture_hash": lambda: changed["source_fixture"].__setitem__("sha256", "0" * 64),
        "source_git_count": lambda: changed["source_locks"].__setitem__("git_count", 127),
        "source_logical_digest": lambda: changed["source_locks"].__setitem__("logical_source_digest", "0" * 64),
        "source_offline": lambda: changed["source_locks"]["remote"].__setitem__("network_fetch_performed", True),
        "source_payload": lambda: changed["source_locks"]["remote"].__setitem__("external_payload_hash_hits", ["payload.pdf"]),
        "source_rights": lambda: changed["source_locks"]["remote"]["redistributable_in_release"].__setitem__(3, True),
        "source_role": lambda: changed["source_roles"].__setitem__("tao-teravainen-arxiv-1708.02610v2", "closure-only"),
        "theorem_clock": lambda: changed["theorems"]["terminal_clock"].__setitem__("normalization", "1/log X"),
        "theorem_support": lambda: changed["theorems"]["odd_parity_compiler"].__setitem__("admitted_support_sizes", "all"),
    }
    actions[name]()
    return changed


def main() -> None:
    payload = build_payload()
    if not validate_result_payload(payload, compare_fresh=False):
        raise RuntimeError("RH-394 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({
        "status": payload["status"], "all_pass": True,
        "git": 128, "remote": 4, "logical": 132,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
