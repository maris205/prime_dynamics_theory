"""Build and independently validate the frozen RH-395 Stage-1 result."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from centered_three_window_capacity.core import (  # noqa: E402
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_SHA256,
    MUTATION_NAMES,
    TITLE,
    build_certificate,
    mutate_certificate,
    verify_certificate,
)
from source_locks import build_source_closure  # noqa: E402


PAPER = "RH-395"
CORE_FILE_BYTES = 127_045
CORE_FILE_SHA256 = "4abb5e4c61a9b71370d2e02c36a474655719740b91fdd247f64ed0af0b90509e"
CORE_TEST_BYTES = 8_934
CORE_TEST_SHA256 = "f8d51247f10ff9ce29103c7c8f76a7c21066c174711fad0ac61bbae2084cdf97"
SOURCE_BUILDER_BYTES = 28_680
SOURCE_BUILDER_SHA256 = "db36343bae5589dd59a125b89d48ec82200d6625d3db8b65d5fb2065f7463a52"
SOURCE_CLOSURE_BYTES = 53_906
SOURCE_CLOSURE_SHA256 = "f1efeeb0d0de94ced87438a5261f69c8f5e0408935374cbadfc7b8f0c84f3fcc"
THEOREM_CONTRACT_SHA256 = "4c1db06dd7c29ccd88669402415ca5cc1ace0f19883d2285de1929178799a67e"
SOURCE_ROLE_SHA256 = "72403cb9257faa742a03ffb4d6aa048ebab3932d1710c100d3899524c2dc825f"


GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}


FORBIDDEN = {
    "causal_or_online_centered_rule": False,
    "RH378_window_end_model_used": False,
    "growing_q": False,
    "q_depending_on_X": False,
    "growing_or_X_dependent_tables": False,
    "effective_uniform_rate": False,
    "ordinary_Cesaro_average": False,
    "maximum_before_terminal_limit": False,
    "adaptive_or_prelimit_capacity": False,
    "generic_graph_capacity": False,
    "even_odd_support_at_least_four": False,
    "RH375_used_as_terminal_clock_analytic_input": False,
    "four_state_compression_used_for_q_2": False,
    "four_state_compression_used_for_q_1": False,
    "finite_endpoint_attained": False,
    "finite_certificate_is_analytic_proof": False,
    "vendored_external_payload": False,
    "network_fetch_required": False,
    "operator_model": False,
    "trace_formula": False,
    "zero_model": False,
    "proof_of_Riemann_Hypothesis": False,
    "Gate_A": False,
    "Gate_B": False,
    "Gate_C": False,
    "Gate_D": False,
    "Gate_E": False,
}


THEOREM_CONTRACTS = {
    "model_and_quantifiers": {
        "alphabet": "T={-1,0,+1}",
        "mobius_extension": "mu_0(k)=mu(k) for integer k>=1 and mu_0(k)=0 for k<=0",
        "phase_table_type": "F_r:T^3->{-1,+1}, r in Z/qZ",
        "fixed_data": "q and every phase table F_r are fixed before X->infinity",
        "clock": "as X->infinity, 1<=omega(X)<=X and omega(X)->infinity, hence omega(X)>1 eventually",
        "window": "F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))",
        "terminal_functional": "L_(q,X)(F)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))/n",
        "limit": "L_q(F)=lim_(X->infinity)L_(q,X)(F) for every admissible terminal clock",
        "safety": "not(F_r(a,b,c)=+1 and F_(r+2)(c,d,e)=+1) for every r and a,b,c,d,e in T",
        "capacity": "C(q)=max_(universally safe fixed q-phase F)|L_q(F)|, with the finite maximum taken only after every fixed-table limit",
        "all_clock_order": "fixed q,F; X->infinity; finite maximum over safe F; then supremum over finite q",
        "centered_type": "noncausal because the future coordinate mu(n+1) is read",
    },
    "phase_densities": {
        "coordinate_shifts": "a_L=+1, a_C=0, a_R=-1",
        "B": "B_(p,S)={a_i mod p^2:i in S}, with duplicate residues removed",
        "nu": "nu_(p,S)=|B_(p,S)|",
        "tau": "tau_(p,S)(r)=#{b in B_(p,S):b mod p=r mod p}",
        "Theta": "Theta_(q,r)(S)=q^-1 product_(p not|q)(1-nu_(p,S)/p^2) product_(p||q)(1-tau_(p,S)(r)/p) product_(p^2|q)1_(r mod p^2 notin B_(p,S))",
        "empty": "Theta_(q,r)(empty)=1/q",
        "K": "K_j=product_p(1-j/p^2), j=0,1,2,3, and K_0=1",
        "phase_sum": "sum_(r mod q)Theta_(q,r)(S)=K_|S|",
        "Pi": "Pi_(q,r)(U)=sum_(W subset {L,C,R}\\U)(-1)^|W|Theta_(q,r)(U union W)",
        "Pi_role": "nonnegative exact-support density",
        "Pi_mass": "sum_(U subset {L,C,R})Pi_(q,r)(U)=1/q",
        "lambda": "lambda_r(x,y)=2^(-1_(x!=0)-1_(y!=0))Pi_(q,r)({C} union ({L}:x!=0) union ({R}:y!=0))",
    },
    "positive_projection_and_relation": {
        "projection": "delete +1 outputs at center z!=+1; this weakly increases zF and preserves safety",
        "fiber": "2^27 full sign tables map uniformly onto 512 relations with 2^18 preimages each",
        "relation": "A_r={(x,y):F_r(x,+1,y)=+1}",
        "safety": "Target(A_r) intersect Source(A_(r+2))=empty",
        "saturation": "with Y_r=Target(A_r), A_r=(T\\Y_(r-2)) cross Y_r",
        "projected_terminal_limit": "L_q(F_proj)=sum_(r mod q)sum_((x,y) in A_r)lambda_r(x,y), because the all-minus baseline sign cells cancel",
        "transition": "K_r(U,V)=sum_(x notin U,y in V)lambda_r(x,y)",
    },
    "tropical_capacity": {
        "cycles": "the +2 map on Z/qZ has gcd(q,2) cycles",
        "all_q_formula": "C(q)=sum_(+2 cycles gamma) max_(cyclic Y_i subset T) sum_i K_(r_i)(Y_(i-1),Y_i)",
        "all_q_state_count": 8,
        "matrix_description": "exact tropical trace of 8x8 transition matrices",
        "q_1_q_2": "self-loops are retained and require the full eight subset states",
        "q_ge_3": "multi-affinity makes some optimum antipodally symmetric, reducing to four states only for q>=3",
        "compressed_state": "u=(1_(0 in Y), |Y intersect {-1,+1}|/2) in {0,1}^2",
        "compressed_coefficients": "(a_r,b_r,c_r,d_r)=(Pi_r({C}),Pi_r({L,C}),Pi_r({C,R}),Pi_r({L,C,R}))",
        "compressed_transition": "a(1-u0)v0+b(1-u1)v0+c(1-u0)v1+d(1-u1)v1",
    },
    "small_clocks": {
        "C1": "K2-K3",
        "C2": "(3K2-K3)/4",
        "q2_even_phase": "one-sign self-loop contributes (K2-K3)/4",
        "q2_odd_phase": "zero endpoint contributes K2/2",
        "q2_forbidden_old_four_state_value": "K2-K3",
        "C3": "3K1/8=9/(4pi^2)",
        "C4": "2K1/3=4/pi^2",
        "C6": "K1/8+K2/2",
        "one_site_F6": "3K1/8",
        "strict_q6_gain": "C6-F_RH375(6)=(2K2-K1)/4>0",
        "ratio_inequalities": "K3/K2<1/2, K3/K2>1/3 in the respective q1 and q2 comparisons, and K2/K1>1/2 for the strict q6 gain",
    },
    "reflection_and_absolute_value": {
        "full_table_reflection": "F^rho(x,z,y)=F(-x,-z,-y)",
        "safety": "input reflection preserves universal safety",
        "terminal_sign": "L_q(F^rho)=-L_q(F)",
        "capacity_identity": "max_safe |L_q|=max_safe L_q",
        "attainment": "both signs are attained whenever a nonzero optimum is attained",
    },
    "divisibility_and_square_support": {
        "lift": "q|Q implies C(q)<=C(Q) by literal nonminimal-period repetition",
        "square_clock": "p_y is the y-th odd prime and q_y=4 product_(3<=p<=p_y, p prime)p^2, with q_1=36",
        "one_site_capacity": "F_RH375(q)=max_(I subset Z/qZ, I intersect (I+2)=empty)sum_(r in I)Theta_(q,r)({C})",
        "finite_endpoint": "B_y=F_RH375(q_y)",
        "limiting_endpoint": "B_infinity=lim_(y->infinity)B_y",
        "marginal_identity": "for adjacent positive-center phases and every t in T, sum_x lambda_r(x,t)=sum_z lambda_(r+2)(t,z)",
        "phase_contribution": "W_r:=K_r(Y_(r-2),Y_r)",
        "common_center_weight": "delta_Q:=Theta_(Q,r)({C}) for any positive-center phase r; it is constant over such phases for square support",
        "pair_charge": "W_r+W_(r+2)<=delta_Q and a positive run of length L costs at most ceil(L/2)delta_Q",
        "resets": "forced zero phases modulo 4 and 9 split both +2 cycles into positive runs",
        "same_support": "if q_y|Q and Q has the same prime support then C(Q)=F_RH375(Q)=B_y",
    },
    "all_clock_rigidity": {
        "cofinal_lcm_bridge": "for finite q choose y covering all prime divisors and Q=lcm(q,q_y), so C(q)<=C(Q)=B_y<B_infinity",
        "strict_nonattainment": "C(q)<B_infinity for every finite q",
        "lower_witness": "embedded one-site relations at q_y give sup_(q finite)C(q)>=B_infinity",
        "conclusion": "sup_(q finite)C(q)=B_infinity and the supremum is not attained at finite q",
    },
    "analytic_and_finite_roles": {
        "RH394": "sole terminal-log analytic input: complete fixed three-shift table law and Pi densities for every admissible terminal clock",
        "RH375": "squarefree phase densities, one-site MWIS values, square-clock endpoints, divisibility and same-support finite combinatorics only",
        "RH375_terminal_clock_analytic_input": False,
        "certificate": "finite exact reproduction of relation algebra and optimizers, not an analytic proof",
    },
}


SOURCE_ROLES = {
    "RH394": "direct frozen predecessor supplying the terminal-log three-shift table law and phase densities",
    "RH375": "direct frozen predecessor supplying finite-clock one-site MWIS, square endpoints, q|Q lift, and same-prime-support combinatorics only; no terminal-log analytic role",
    "johnston-yang-arxiv-2204.01980v2": "inherited closure-only via RH394",
    "maynard-annals-2015-small-gaps": "inherited closure-only via RH394",
    "tao-cambridge-2016-logarithmic-chowla": "inherited two-point provenance via RH394",
    "tao-teravainen-arxiv-1708.02610v2": "inherited odd-parity analytic input via RH394, not newly invoked directly",
    "finite_certificate": "finite exact reproduction, not analytic proof",
}


RESULT_MUTATION_NAMES = (
    "all_pass", "schema_version_float", "paper", "title", "status", "role",
    "core_bytes", "core_hash", "core_test_hash", "certificate_bytes",
    "certificate_hash", "source_builder_hash", "source_closure_bytes",
    "source_closure_hash", "network", "vendor", "analytic_proof",
    "git_count", "remote_count", "logical_count", "logical_digest",
    "rights", "payload_hit", "theorem_clock", "theorem_safety",
    "theorem_theta", "theorem_pi", "theorem_projected_limit",
    "theorem_square_charge", "theorem_ratio", "theorem_trace", "theorem_q2",
    "theorem_reflection", "theorem_lift", "theorem_endpoint",
    "source_RH375_role", "source_RH394_role", "forbidden_true",
    "forbidden_missing", "gate_true", "core_mutation_name",
    "core_mutation_rejected", "summary_q2", "summary_rows", "extra_key",
)
RESULT_BUILDER_NAMES = (
    "build_payload", "_core_mutation_rows", "build_certificate",
    "build_source_closure", "mutate_certificate", "verify_certificate",
)
RESULT_HELPER_NAMES = (
    "canonical_bytes", "pretty_json_bytes", "exact_equal", "loads_strict",
    "_validate_constants",
)


def _reject_constant(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")


def _pairs_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(
        text, object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def pretty_json_bytes(value: object) -> bytes:
    return (json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, indent=2,
    ) + "\n").encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def _validate_constants() -> None:
    expected = {
        "paper": "RH-395",
        "title": "All-Clock Rigidity for Centered Three-Window Möbius Capacity",
        "core_bytes": 127045,
        "core_sha": "4abb5e4c61a9b71370d2e02c36a474655719740b91fdd247f64ed0af0b90509e",
        "core_test_bytes": 8934,
        "core_test_sha": "f8d51247f10ff9ce29103c7c8f76a7c21066c174711fad0ac61bbae2084cdf97",
        "certificate_bytes": 32983,
        "certificate_sha": "31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9",
        "source_builder_bytes": 28680,
        "source_builder_sha": "db36343bae5589dd59a125b89d48ec82200d6625d3db8b65d5fb2065f7463a52",
        "source_closure_bytes": 53906,
        "source_closure_sha": "f1efeeb0d0de94ced87438a5261f69c8f5e0408935374cbadfc7b8f0c84f3fcc",
    }
    actual = {
        "paper": PAPER, "title": TITLE,
        "core_bytes": CORE_FILE_BYTES, "core_sha": CORE_FILE_SHA256,
        "core_test_bytes": CORE_TEST_BYTES, "core_test_sha": CORE_TEST_SHA256,
        "certificate_bytes": CERTIFICATE_FIXTURE_BYTES,
        "certificate_sha": CERTIFICATE_FIXTURE_SHA256,
        "source_builder_bytes": SOURCE_BUILDER_BYTES,
        "source_builder_sha": SOURCE_BUILDER_SHA256,
        "source_closure_bytes": SOURCE_CLOSURE_BYTES,
        "source_closure_sha": SOURCE_CLOSURE_SHA256,
    }
    if not exact_equal(actual, expected):
        raise ValueError("frozen core/source identity constants changed")
    if sha256(canonical_bytes(THEOREM_CONTRACTS)).hexdigest() != THEOREM_CONTRACT_SHA256:
        raise ValueError("theorem contract literal seal changed")
    if sha256(canonical_bytes(SOURCE_ROLES)).hexdigest() != SOURCE_ROLE_SHA256:
        raise ValueError("source-role literal seal changed")


def _core_mutation_rows(certificate: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for name in MUTATION_NAMES:
        changed = mutate_certificate(certificate, name)
        rows.append({
            "name": name,
            "existing_leaf_changed": canonical_bytes(changed) != canonical_bytes(certificate),
            "false_validator_rejected": verify_certificate(changed, compare_fresh=False) is False,
        })
    return rows


def build_payload() -> dict[str, object]:
    _validate_constants()
    core_path = ROOT / "src" / "centered_three_window_capacity" / "core.py"
    core_test_path = ROOT / "tests" / "test_core.py"
    source_path = ROOT / "experiments" / "source_locks.py"
    if len(core_path.read_bytes()) != CORE_FILE_BYTES or sha256(core_path.read_bytes()).hexdigest() != CORE_FILE_SHA256:
        raise RuntimeError("core file identity changed")
    if len(core_test_path.read_bytes()) != CORE_TEST_BYTES or sha256(core_test_path.read_bytes()).hexdigest() != CORE_TEST_SHA256:
        raise RuntimeError("core test identity changed")
    if len(source_path.read_bytes()) != SOURCE_BUILDER_BYTES or sha256(source_path.read_bytes()).hexdigest() != SOURCE_BUILDER_SHA256:
        raise RuntimeError("source builder identity changed")
    certificate = build_certificate()
    certificate_raw = canonical_bytes(certificate)
    source = build_source_closure()
    source_raw = canonical_bytes(source)
    mutation_rows = _core_mutation_rows(certificate)
    identities = {
        "core_file": {"bytes": CORE_FILE_BYTES, "sha256": CORE_FILE_SHA256},
        "core_test": {"bytes": CORE_TEST_BYTES, "sha256": CORE_TEST_SHA256},
        "certificate": {"canonical_bytes": CERTIFICATE_FIXTURE_BYTES, "canonical_sha256": CERTIFICATE_FIXTURE_SHA256, "rows": 72},
        "source_builder": {"bytes": SOURCE_BUILDER_BYTES, "sha256": SOURCE_BUILDER_SHA256},
        "source_closure": {"canonical_bytes": SOURCE_CLOSURE_BYTES, "canonical_sha256": SOURCE_CLOSURE_SHA256, "git": 148, "remote": 4, "logical": 152, "logical_sha256": "5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3"},
        "theorem_contract_sha256": THEOREM_CONTRACT_SHA256,
        "source_role_sha256": SOURCE_ROLE_SHA256,
    }
    declarations = {
        "network_opt_in": False,
        "requests_made": 0,
        "external_payload_vendored": False,
        "external_payload_hash_hits": [],
        "remote_redistributable_in_release": [False, False, True, False],
        "finite_reproduction_not_analytic_proof": True,
        "fixed_q_only": True,
        "limit_before_maximum": True,
    }
    summary = {
        "relation_pairs_scanned": 262144,
        "safe_relation_pairs": 3375,
        "certificate_rows": 72,
        "core_mutations": len(mutation_rows),
        "core_mutations_rejected": sum(row["false_validator_rejected"] is True for row in mutation_rows),
        "C1": "K2-K3",
        "C2": "(3K2-K3)/4",
        "C3": "3K1/8",
        "C4": "2K1/3",
        "C6": "K1/8+K2/2",
        "one_site_F6": "3K1/8",
        "q36": "B1=2K1/3",
        "q900": "B2=49K1/72",
        "finite_nonattainment": True,
        "all_clock_supremum": "B_infinity",
    }
    payload = {
        "schema_version": 1,
        "paper": PAPER,
        "title": TITLE,
        "status": "RH-395_STAGE1_CERTIFIED",
        "epistemic_role": "finite_exact_reproduction_plus_frozen_analytic_interfaces",
        "identities": identities,
        "declarations": declarations,
        "theorem_contracts": deepcopy(THEOREM_CONTRACTS),
        "source_roles": deepcopy(SOURCE_ROLES),
        "source_closure": source,
        "certificate": certificate,
        "core_mutation_audit": mutation_rows,
        "result_mutation_names": list(RESULT_MUTATION_NAMES),
        "gates": dict(GATES),
        "forbidden": dict(FORBIDDEN),
        "summary": summary,
        "all_pass": (
            len(certificate_raw) == CERTIFICATE_FIXTURE_BYTES
            and sha256(certificate_raw).hexdigest() == CERTIFICATE_FIXTURE_SHA256
            and verify_certificate(certificate, compare_fresh=False) is True
            and len(source_raw) == SOURCE_CLOSURE_BYTES
            and sha256(source_raw).hexdigest() == SOURCE_CLOSURE_SHA256
            and source["pass"] is True
            and source["git_count"] == 148
            and source["remote_count"] == 4
            and source["logical_count"] == 152
            and all(row["existing_leaf_changed"] is True and row["false_validator_rejected"] is True for row in mutation_rows)
            and all(value is False for value in GATES.values())
            and all(value is False for value in FORBIDDEN.values())
        ),
    }
    return payload


def _make_result_validator():
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    certificate_bytes_literal = 32983
    certificate_sha_literal = "31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9"
    source_bytes_literal = 53906
    source_sha_literal = "f1efeeb0d0de94ced87438a5261f69c8f5e0408935374cbadfc7b8f0c84f3fcc"
    theorem_sha_literal = "4c1db06dd7c29ccd88669402415ca5cc1ace0f19883d2285de1929178799a67e"
    source_role_sha_literal = "72403cb9257faa742a03ffb4d6aa048ebab3932d1710c100d3899524c2dc825f"
    result_mutations_literal = (
        "all_pass", "schema_version_float", "paper", "title", "status", "role",
        "core_bytes", "core_hash", "core_test_hash", "certificate_bytes",
        "certificate_hash", "source_builder_hash", "source_closure_bytes",
        "source_closure_hash", "network", "vendor", "analytic_proof",
        "git_count", "remote_count", "logical_count", "logical_digest", "rights",
        "payload_hit", "theorem_clock", "theorem_safety", "theorem_theta",
        "theorem_pi", "theorem_projected_limit", "theorem_square_charge",
        "theorem_ratio", "theorem_trace", "theorem_q2", "theorem_reflection",
        "theorem_lift", "theorem_endpoint", "source_RH375_role",
        "source_RH394_role", "forbidden_true", "forbidden_missing", "gate_true",
        "core_mutation_name", "core_mutation_rejected", "summary_q2",
        "summary_rows", "extra_key",
    )
    core_mutations_literal = (
        "shift_swap", "lambda_divisor", "all_q_trace_4x4", "q2_old_value",
        "q2_even_witness", "q2_odd_witness", "q2_selfloop_deleted",
        "q1_affinity_claim", "capacity_q1", "capacity_q2", "capacity_q3",
        "capacity_q4", "capacity_q6", "one_site_q6", "q1_ratio_direction",
        "q2_ratio_direction", "projection_point_case", "projection_deleted_count",
        "relation_safe_count", "saturation_changed_count", "multi_affinity_failure",
        "self_identification_q2", "marginal_left", "marginal_right",
        "marginal_only_sum", "marginal_omit_t0", "path_ceil_to_floor",
        "forced_reset_4", "forced_reset_9", "same_support_scale", "square_q36",
        "square_q900", "q_lift_direction", "q_lift_safety", "finite_attainment",
        "rh375_terminal_misrole", "growing_q", "prelimit_max", "causal_claim",
        "ordinary_cesaro", "generic_capacity", "source_stop",
        "reflection_sign_identity", "reflection_both_signs", "mu0_definition",
        "terminal_normalization", "phase_table_type", "safety_condition",
        "capacity_definition", "theta_formula", "pi_formula", "pi_mass",
        "endpoint_definition", "row_extra", "float_injection", "interval_cutoff",
        "interval_policy",
    )
    local_gates = {
        "A_intrinsic_determinant": False,
        "B_scattering_completion": False,
        "C_self_adjoint_generator": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    local_forbidden = {
        "causal_or_online_centered_rule": False,
        "RH378_window_end_model_used": False,
        "growing_q": False,
        "q_depending_on_X": False,
        "growing_or_X_dependent_tables": False,
        "effective_uniform_rate": False,
        "ordinary_Cesaro_average": False,
        "maximum_before_terminal_limit": False,
        "adaptive_or_prelimit_capacity": False,
        "generic_graph_capacity": False,
        "even_odd_support_at_least_four": False,
        "RH375_used_as_terminal_clock_analytic_input": False,
        "four_state_compression_used_for_q_2": False,
        "four_state_compression_used_for_q_1": False,
        "finite_endpoint_attained": False,
        "finite_certificate_is_analytic_proof": False,
        "vendored_external_payload": False,
        "network_fetch_required": False,
        "operator_model": False,
        "trace_formula": False,
        "zero_model": False,
        "proof_of_Riemann_Hypothesis": False,
        "Gate_A": False,
        "Gate_B": False,
        "Gate_C": False,
        "Gate_D": False,
        "Gate_E": False,
    }

    def encode(value: object) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(same(left[key], right[key]) for key in left)
        if type(left) is list:
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        return left == right

    def semantic(value: object) -> bool:
        top_keys = (
            "schema_version", "paper", "title", "status", "epistemic_role",
            "identities", "declarations", "theorem_contracts", "source_roles",
            "source_closure", "certificate", "core_mutation_audit",
            "result_mutation_names", "gates", "forbidden", "summary", "all_pass",
        )
        if type(value) is not dict or set(value) != set(top_keys):
            return False
        if not (
            type(value["schema_version"]) is int and value["schema_version"] == 1
            and value["paper"] == "RH-395"
            and value["title"] == "All-Clock Rigidity for Centered Three-Window Möbius Capacity"
            and value["status"] == "RH-395_STAGE1_CERTIFIED"
            and value["epistemic_role"] == "finite_exact_reproduction_plus_frozen_analytic_interfaces"
            and value["all_pass"] is True
            and same(value["gates"], local_gates)
            and same(value["forbidden"], local_forbidden)
            and same(value["result_mutation_names"], list(result_mutations_literal))
        ):
            return False
        identities = value["identities"]
        expected_identities = {
            "core_file": {"bytes": 127045, "sha256": "4abb5e4c61a9b71370d2e02c36a474655719740b91fdd247f64ed0af0b90509e"},
            "core_test": {"bytes": 8934, "sha256": "f8d51247f10ff9ce29103c7c8f76a7c21066c174711fad0ac61bbae2084cdf97"},
            "certificate": {"canonical_bytes": 32983, "canonical_sha256": certificate_sha_literal, "rows": 72},
            "source_builder": {"bytes": 28680, "sha256": "db36343bae5589dd59a125b89d48ec82200d6625d3db8b65d5fb2065f7463a52"},
            "source_closure": {"canonical_bytes": 53906, "canonical_sha256": source_sha_literal, "git": 148, "remote": 4, "logical": 152, "logical_sha256": "5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3"},
            "theorem_contract_sha256": theorem_sha_literal,
            "source_role_sha256": source_role_sha_literal,
        }
        if not same(identities, expected_identities):
            return False
        declarations = {
            "network_opt_in": False,
            "requests_made": 0,
            "external_payload_vendored": False,
            "external_payload_hash_hits": [],
            "remote_redistributable_in_release": [False, False, True, False],
            "finite_reproduction_not_analytic_proof": True,
            "fixed_q_only": True,
            "limit_before_maximum": True,
        }
        if not same(value["declarations"], declarations):
            return False
        certificate_raw = encode(value["certificate"])
        source_raw = encode(value["source_closure"])
        if not (
            len(certificate_raw) == certificate_bytes_literal
            and local_sha256(certificate_raw).hexdigest() == certificate_sha_literal
            and len(source_raw) == source_bytes_literal
            and local_sha256(source_raw).hexdigest() == source_sha_literal
            and local_sha256(encode(value["theorem_contracts"])).hexdigest() == theorem_sha_literal
            and local_sha256(encode(value["source_roles"])).hexdigest() == source_role_sha_literal
        ):
            return False
        certificate = value["certificate"]
        source = value["source_closure"]
        if not (
            certificate["row_count"] == 72 and certificate["all_pass"] is True
            and certificate["model"]["capacity_definition"] == "C(q)=max_(universally safe fixed q-phase F) |L_q(F)| after each fixed-table limit exists"
            and certificate["reflection_audit"]["terminal_sign_identity"] == "L_q(F^rho)=-L_q(F)"
            and source["git_count"] == 148 and source["remote_count"] == 4
            and source["logical_count"] == 152
            and source["logical_source_digest"] == "5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3"
            and source["pass"] is True
            and source["remote"]["network_fetch_performed"] is False
            and source["remote"]["external_payload_hash_hits"] == []
            and source["remote"]["redistributable_in_release"] == [False, False, True, False]
            and source["direct_predecessors"]["rh375_one_site_endpoint"]["terminal_clock_analytic_input"] is False
        ):
            return False
        theorem = value["theorem_contracts"]
        if not (
            theorem["model_and_quantifiers"]["safety"].startswith("not(F_r")
            and theorem["tropical_capacity"]["all_q_state_count"] == 8
            and theorem["tropical_capacity"]["q_ge_3"].endswith("only for q>=3")
            and theorem["positive_projection_and_relation"]["projected_terminal_limit"].startswith("L_q(F_proj)=")
            and theorem["tropical_capacity"]["compressed_coefficients"].startswith("(a_r,b_r,c_r,d_r)=")
            and theorem["small_clocks"]["C2"] == "(3K2-K3)/4"
            and "K2/K1>1/2" in theorem["small_clocks"]["ratio_inequalities"]
            and theorem["reflection_and_absolute_value"]["terminal_sign"] == "L_q(F^rho)=-L_q(F)"
            and theorem["divisibility_and_square_support"]["phase_contribution"] == "W_r:=K_r(Y_(r-2),Y_r)"
            and theorem["divisibility_and_square_support"]["common_center_weight"].startswith("delta_Q:=")
            and theorem["all_clock_rigidity"]["strict_nonattainment"] == "C(q)<B_infinity for every finite q"
            and theorem["analytic_and_finite_roles"]["RH375_terminal_clock_analytic_input"] is False
        ):
            return False
        rows = value["core_mutation_audit"]
        if type(rows) is not list or len(rows) != len(core_mutations_literal):
            return False
        for row, name in zip(rows, core_mutations_literal):
            if row != {"name": name, "existing_leaf_changed": True, "false_validator_rejected": True}:
                return False
        expected_summary = {
            "relation_pairs_scanned": 262144,
            "safe_relation_pairs": 3375,
            "certificate_rows": 72,
            "core_mutations": 57,
            "core_mutations_rejected": 57,
            "C1": "K2-K3", "C2": "(3K2-K3)/4", "C3": "3K1/8",
            "C4": "2K1/3", "C6": "K1/8+K2/2", "one_site_F6": "3K1/8",
            "q36": "B1=2K1/3", "q900": "B2=49K1/72",
            "finite_nonattainment": True, "all_clock_supremum": "B_infinity",
        }
        return same(value["summary"], expected_summary)

    independent_semantic = semantic
    fresh_builder = build_payload

    def verifier(value: object, *, compare_fresh: bool = True) -> bool:
        if type(compare_fresh) is not bool:
            return False
        try:
            if not independent_semantic(value):
                return False
            return not compare_fresh or same(value, fresh_builder())
        except (KeyError, TypeError, ValueError, RuntimeError, IndexError):
            return False

    return verifier


validate_result_payload = _make_result_validator()
del _make_result_validator


def mutate_result(value: dict[str, object], name: str) -> dict[str, object]:
    if type(name) is not str or name not in RESULT_MUTATION_NAMES:
        raise ValueError("unknown result mutation")
    changed = deepcopy(value)
    actions = {
        "all_pass": lambda: changed.__setitem__("all_pass", False),
        "schema_version_float": lambda: changed.__setitem__("schema_version", 1.0),
        "paper": lambda: changed.__setitem__("paper", "RH-394"),
        "title": lambda: changed.__setitem__("title", "wrong"),
        "status": lambda: changed.__setitem__("status", "draft"),
        "role": lambda: changed.__setitem__("epistemic_role", "analytic_proof"),
        "core_bytes": lambda: changed["identities"]["core_file"].__setitem__("bytes", 127044),
        "core_hash": lambda: changed["identities"]["core_file"].__setitem__("sha256", "0" * 64),
        "core_test_hash": lambda: changed["identities"]["core_test"].__setitem__("sha256", "0" * 64),
        "certificate_bytes": lambda: changed["identities"]["certificate"].__setitem__("canonical_bytes", 32982),
        "certificate_hash": lambda: changed["identities"]["certificate"].__setitem__("canonical_sha256", "0" * 64),
        "source_builder_hash": lambda: changed["identities"]["source_builder"].__setitem__("sha256", "0" * 64),
        "source_closure_bytes": lambda: changed["identities"]["source_closure"].__setitem__("canonical_bytes", 53905),
        "source_closure_hash": lambda: changed["identities"]["source_closure"].__setitem__("canonical_sha256", "0" * 64),
        "network": lambda: changed["declarations"].__setitem__("network_opt_in", True),
        "vendor": lambda: changed["declarations"].__setitem__("external_payload_vendored", True),
        "analytic_proof": lambda: changed["declarations"].__setitem__("finite_reproduction_not_analytic_proof", False),
        "git_count": lambda: changed["source_closure"].__setitem__("git_count", 147),
        "remote_count": lambda: changed["source_closure"].__setitem__("remote_count", 3),
        "logical_count": lambda: changed["source_closure"].__setitem__("logical_count", 151),
        "logical_digest": lambda: changed["source_closure"].__setitem__("logical_source_digest", "0" * 64),
        "rights": lambda: changed["source_closure"]["remote"].__setitem__("redistributable_in_release", [False] * 4),
        "payload_hit": lambda: changed["source_closure"]["remote"].__setitem__("external_payload_hash_hits", ["forbidden"]),
        "theorem_clock": lambda: changed["theorem_contracts"]["model_and_quantifiers"].__setitem__("clock", "omega=2"),
        "theorem_safety": lambda: changed["theorem_contracts"]["model_and_quantifiers"].__setitem__("safety", "observed words only"),
        "theorem_theta": lambda: changed["theorem_contracts"]["phase_densities"].__setitem__("Theta", "wrong"),
        "theorem_pi": lambda: changed["theorem_contracts"]["phase_densities"].__setitem__("Pi", "wrong"),
        "theorem_projected_limit": lambda: changed["theorem_contracts"]["positive_projection_and_relation"].__setitem__("projected_terminal_limit", "missing baseline factor"),
        "theorem_square_charge": lambda: changed["theorem_contracts"]["divisibility_and_square_support"].__setitem__("phase_contribution", "undefined W"),
        "theorem_ratio": lambda: changed["theorem_contracts"]["small_clocks"].__setitem__("ratio_inequalities", "K3/K2 bounds only"),
        "theorem_trace": lambda: changed["theorem_contracts"]["tropical_capacity"].__setitem__("all_q_state_count", 4),
        "theorem_q2": lambda: changed["theorem_contracts"]["small_clocks"].__setitem__("C2", "K2-K3"),
        "theorem_reflection": lambda: changed["theorem_contracts"]["reflection_and_absolute_value"].__setitem__("terminal_sign", "same sign"),
        "theorem_lift": lambda: changed["theorem_contracts"]["divisibility_and_square_support"].__setitem__("lift", "C(Q)<=C(q)"),
        "theorem_endpoint": lambda: changed["theorem_contracts"]["all_clock_rigidity"].__setitem__("strict_nonattainment", "attained"),
        "source_RH375_role": lambda: changed["source_roles"].__setitem__("RH375", "terminal analytic input"),
        "source_RH394_role": lambda: changed["source_roles"].__setitem__("RH394", "closure only"),
        "forbidden_true": lambda: changed["forbidden"].__setitem__("growing_q", True),
        "forbidden_missing": lambda: changed["forbidden"].pop("growing_q"),
        "gate_true": lambda: changed["gates"].__setitem__("A_intrinsic_determinant", True),
        "core_mutation_name": lambda: changed["core_mutation_audit"][0].__setitem__("name", "wrong"),
        "core_mutation_rejected": lambda: changed["core_mutation_audit"][0].__setitem__("false_validator_rejected", False),
        "summary_q2": lambda: changed["summary"].__setitem__("C2", "K2-K3"),
        "summary_rows": lambda: changed["summary"].__setitem__("certificate_rows", 71),
        "extra_key": lambda: changed.__setitem__("extra", 0),
    }
    actions[name]()
    return changed


def main() -> None:
    payload = build_payload()
    if validate_result_payload(payload, compare_fresh=False) is not True:
        raise RuntimeError("fresh result failed independent validation")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({
        "status": payload["status"], "all_pass": payload["all_pass"],
        "bytes": len(OUTPUT.read_bytes()),
        "sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
