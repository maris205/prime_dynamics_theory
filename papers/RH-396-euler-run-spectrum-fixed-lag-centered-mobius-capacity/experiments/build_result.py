"""Build and independently validate the frozen RH-396 Stage-1 result."""

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

from fixed_lag_centered_capacity.core import (  # noqa: E402
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_ROWS,
    CERTIFICATE_FIXTURE_SHA256,
    MUTATION_NAMES,
    TITLE,
    build_certificate,
    mutate_certificate,
    verify_certificate,
)
from source_locks import build_source_closure  # noqa: E402


PAPER = "RH-396"
CORE_FILE_BYTES = 129_642
CORE_FILE_SHA256 = "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d"
CORE_TEST_BYTES = 10_631
CORE_TEST_SHA256 = "a02e4716f753aa3882ab9999cefc6be125bb8586214b18c15f921de2f64eea74"
SOURCE_BUILDER_BYTES = 26_866
SOURCE_BUILDER_SHA256 = "4805acbe541d8e5e4f07d9fa4cd621b87b7551afeb02a0b9fcc0d8684dfa75f6"
SOURCE_TEST_BYTES = 14_678
SOURCE_TEST_SHA256 = "ce61e6b9c9eef136013123ef0fb344a7f9d7f17f2f0507faf17900a997f02b43"
SOURCE_CLOSURE_BYTES = 57_336
SOURCE_CLOSURE_SHA256 = "c16456d58efd74edf1505c430a54459e359b5ba7e1e581773e9a0613b493385b"
ALL_GIT_SOURCE_SHA256 = "472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86"
LOGICAL_SOURCE_SHA256 = "72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287"
THEOREM_CONTRACT_SHA256 = "40fe1ffaef12c9cc65abdb2cc83e060078cf71a4ad14455324ca32b6a7902682"
SOURCE_ROLE_SHA256 = "2252ae2fb6c613cd998ce174df0646ef9f0934a8584536fd105124ef74b01640"


GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}


FORBIDDEN = {
    "causal_or_online_centered_rule": False,
    "causal_relabeling": False,
    "RH378_window_end_model_used": False,
    "growing_h": False,
    "h_depending_on_X": False,
    "growing_q": False,
    "q_depending_on_X": False,
    "growing_or_X_dependent_tables": False,
    "effective_uniform_rate_in_h_or_q": False,
    "ordinary_Cesaro_average": False,
    "maximum_before_terminal_limit": False,
    "adaptive_or_prelimit_capacity": False,
    "supremum_over_h_capacity_claim": False,
    "maximum_over_h_claim": False,
    "monotonicity_in_h_claim": False,
    "generic_graph_capacity": False,
    "unconditional_even_four_shift_terminal_law": False,
    "window_size_at_least_five": False,
    "RH375_used_as_terminal_clock_analytic_input": False,
    "RH395_used_as_terminal_clock_analytic_input": False,
    "four_state_compression_when_q_divides_2h": False,
    "four_state_compression_for_all_q": False,
    "same_support_scaling_without_p0_in_base": False,
    "strict_gain_at_every_square_support_prime_step": False,
    "limiting_endpoint_attained_at_finite_q": False,
    "lag_infimum_attained": False,
    "finite_certificate_is_analytic_proof": False,
    "vendored_external_payload": False,
    "network_fetch_required": False,
    "operator_model": False,
    "von_mangoldt_or_zeta_trace_formula": False,
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
        "fixed_lag": "h>=1 is fixed before X->infinity",
        "fixed_data": "q and every phase table F_r are fixed before X->infinity",
        "clock": "as X->infinity, 1<=omega(X)<=X and omega(X)->infinity, hence omega(X)>1 eventually",
        "window": "epsilon_F(n)=F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))",
        "terminal_functional": "L_(h,q,X)(F)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)epsilon_F(n)/n",
        "safety_step": "d=2h",
        "safety": "not(F_r(a,b,c)=+1 and F_(r+d)(c,e,f)=+1) for every r and a,b,c,e,f in T",
        "limit": "L_(h,q)(F)=lim_(X->infinity)L_(h,q,X)(F) for every admissible terminal clock",
        "capacity": "C_h(q)=max_(universally distance-d safe fixed q-phase F)|L_(h,q)(F)|, with the finite maximum taken only after every fixed-table limit",
        "order": "fix h,q,F; take X->infinity; take the finite maximum over safe F; then take supremum over finite q",
        "all_clock_scope": "the same terminal value holds for every admissible clock",
        "supremum_over_h_claim": False,
    },
    "phase_densities": {
        "coordinate_shifts": ["L=+h", "C=0", "R=-h"],
        "B": "B_(p,S)={a_i mod p^2:i in S}, with duplicate residues removed",
        "nu": "nu_(p,S)=|B_(p,S)|",
        "tau": "tau_(p,S)(r)=#{b in B_(p,S):b mod p=r mod p}, counted after mod-p^2 deduplication",
        "Theta": "Theta_(h,q,r)(S)=q^-1 product_(p not|q)(1-nu_(p,S)/p^2) product_(p||q)(1-tau_(p,S)(r)/p) product_(p^2|q)1_(r mod p^2 notin B_(p,S))",
        "empty": "Theta_(h,q,r)(empty)=1/q",
        "phase_sum": "sum_(r mod q)Theta_(h,q,r)(S)=kappa_h(S)=product_p(1-nu_(p,S)/p^2)=Theta_(h,1,0)(S)",
        "Pi": "Pi_(h,q,r)(U)=sum_(W subset {L,C,R}\\U)(-1)^|W|Theta_(h,q,r)(U union W)",
        "Pi_role": "nonnegative exact-support density",
        "Pi_mass": "sum_(U subset {L,C,R})Pi_(h,q,r)(U)=1/q",
        "Sxy": "S(x,y)={C} union ({L}:x!=0) union ({R}:y!=0)",
        "lambda": "lambda_(h,q,r)(x,y)=2^(-1_(x!=0)-1_(y!=0))Pi_(h,q,r)(S(x,y))",
        "K": "K_j=product_p(1-j/p^2), j=0,1,2,3, are the collision-free j-site constants and K_0=1",
        "K1": "every singleton has density K_1=6/pi^2",
    },
    "projection_relation_reflection": {
        "positive_projection": "delete +1 outputs at center z!=+1; this weakly increases the mu(n)-weighted score and preserves safety",
        "relation": "A_r={(x,y):F_r(x,+1,y)=+1}",
        "source_target": "Source(A)={x:exists y (x,y)in A}; Target(A)={y:exists x (x,y)in A}",
        "safety": "Target(A_r) intersect Source(A_(r+d))=empty",
        "state": "Y_r=Target(A_r)",
        "saturation": "A_r=(T\\Y_(r-d)) cross Y_r",
        "transition": "mathcalK_r(U,V)=sum_(x notin U,y in V)lambda_(h,q,r)(x,y)",
        "projected_terminal_limit": "L_(h,q)(F_proj)=sum_(r mod q)sum_((x,y) in A_r)lambda_(h,q,r)(x,y)",
        "full_table_reflection": "F^rho_r(x,z,y)=F_r(-x,-z,-y)",
        "reflection_safety": "input reflection preserves universal distance-d safety",
        "terminal_sign": "L_(h,q)(F^rho)=-L_(h,q)(F)",
        "capacity_identity": "max_safe |L_(h,q)|=max_safe L_(h,q)",
        "attainment": "both signs are attained whenever the optimum is nonzero",
    },
    "tropical_capacity": {
        "cycles": "the +d map on Z/qZ has gcd(q,2h) cycles",
        "cycle_length": "each +d cycle has length q/gcd(q,2h)",
        "all_q_formula": "C_h(q)=sum_(+d cycles gamma) max_(cyclic Y_i subset T) sum_i mathcalK_(r_i)(Y_(i-1),Y_i)",
        "all_q_state_count": 8,
        "matrix_description": "exact tropical trace of 8x8 transition matrices",
        "selfloop_criterion": "q divides 2h if and only if every +d cycle is a self-loop",
        "selfloop_rule": "when q divides 2h the theorem retains the full eight-state formula; no four-state reduction is asserted, and h=2,q=4 gives a strict obstruction in general",
        "four_state_scope": "four-state compression is proved when q does not divide 2h",
        "four_state_masks": [0, 2, 5, 7],
        "compressed_state": "u=(1_(0 in Y),|Y intersect {-1,+1}|/2) in {0,1}^2",
        "h2_q4_full8": ["0", "0", "1/2", "-1/2"],
        "h2_q4_forbidden_four": ["0", "0", "1", "-2"],
        "forbidden_all_q_four_state_claim": False,
    },
    "square_support_and_normalization": {
        "square_clock_domain": "for a finite prime set P, q_P=product_(p in P)p^2; the quantities N,alpha,M are defined on square-supported clocks, while the capacity equality and endpoint require p_0(h) in P",
        "positive_count": "N_h(q_P)=#{r mod q_P:Theta_(h,q_P,r)({C})>0}",
        "common_positive_weight": "Theta_(h,q_P,r)({C})=K_1/N_h(q_P) at every positive singleton phase",
        "raw_MWIS": "alpha_h(q_P)=max_(I subset positive phases, I intersect (I+2h)=empty)|I|",
        "weighted_capacity": "M_h(q_P)=K_1 alpha_h(q_P)/N_h(q_P)",
        "general_square_supported_quantities": "if q_P|Q and rad(Q)=rad(q_P), define N_h(Q) as the positive singleton phase count, alpha_h(Q) as the raw step-2h MWIS, M_h(Q)=K_1 alpha_h(Q)/N_h(Q), and delta_Q=K_1/N_h(Q)",
        "shared_coordinate_marginal": "for every adjacent pair of positive center phases r,r+d on square-supported Q and for every t in T, sum_x lambda_(h,Q,r)(x,t)=sum_y lambda_(h,Q,r+d)(t,y)=m_r(t), with sum_t m_r(t)=delta_Q",
        "collision_safe_marginal_cases": "m_r(0)=Theta_r({C})-Theta_r({C,R})=m'_(r+d)(0)=Theta_(r+d)({C})-Theta_(r+d)({L,C}); m_r(+/-1)=Theta_r({C,R})/2=m'_(r+d)(+/-1)=Theta_(r+d)({L,C})/2",
        "pair_charge": "mathcalK_r(U,V)+mathcalK_(r+d)(V,W)<=delta_Q for all U,V,W subset T",
        "path_charge": "a positive step-2h run of length L contributes at most ceil(L/2)delta_Q",
        "centered_square_clock_equality": "if p_0(h) is in P then C_h(q_P)=M_h(q_P)=K_1 alpha_h(q_P)/N_h(q_P)",
        "normalization_firewall": "on square-support clocks alpha_h(q_P) is raw and unweighted while M_h(q_P) is normalized and weighted; this formula is not asserted for arbitrary q with p||q",
        "divisibility_lift": "q|Q implies C_h(q)<=C_h(Q) by literal nonminimal-period repetition",
        "p0": "p_0(h)=min{prime p:p does not divide 2h}",
        "same_support_domain": "the base square support must contain p_0(h)^2 before same-support scaling is asserted",
        "same_support_equality": "if q_P|Q and rad(Q)=rad(q_P), with R=Q/q_P, then C_h(Q)=M_h(Q)=M_h(q_P), N_h(Q)=R N_h(q_P), and alpha_h(Q)=R alpha_h(q_P)",
        "pre_p0_counterexample": "h=6: (alpha,N)=(9,24) at q=36 but (24,48) at q=72; ratios 3/8 and 1/2 differ",
        "post_p0_fixture": "h=6: (alpha,N)=(291,576) at q=900 and (582,1152) at q=1800; ratios agree",
    },
    "euler_run_endpoint": {
        "finite_D": "D_(h,P)(J)=product_(p in P)(1-|{2hj mod p^2:j in J}|/p^2)",
        "infinite_D": "D_h(J)=product_p(1-|{2hj mod p^2:j in J}|/p^2)",
        "D_convergence": "for every finite J the Euler product D_h(J) converges absolutely, and D_(h,P_y)(J)->D_h(J) along prime-initial supports P_y",
        "run_density": "R_(ell,h)=D_h([0,ell-1])-D_h({-1} union [0,ell-1])-D_h([0,ell])+D_h([-1,ell])",
        "finite_run_density": "R_(ell,h,P) is the same four-term expression with D_(h,P)",
        "run_event": "R_(ell,h,P) and R_(ell,h) are nonnegative densities of zero at -1, positive at 0,...,ell-1, and zero at ell in step-2h coordinates",
        "finite_run_count": "on q_P the exact number of bracketed positive runs of length ell is q_P R_(ell,h,P)",
        "termwise_limit": "for each ell, R_(ell,h,P_y)->R_(ell,h), and the cutoff ell<p_0(h)^2 makes the endpoint sum finite",
        "run_cutoff": "every squarefree step-2h run has length ell<p_0(h)^2",
        "raw_alpha_identity": "alpha_h(q_P)=N_h(q_P)/2+(q_P/2)sum_(1<=ell<p_0^2, ell odd)R_(ell,h,P)",
        "finite_endpoint": "B_(h,P)=K_1/2+K_1/(2D_(h,P)({0})) sum_(1<=ell<p_0^2, ell odd)R_(ell,h,P)",
        "infinite_endpoint": "B_infinity(h)=3/pi^2+(1/2)sum_(1<=ell<p_0(h)^2, ell odd)R_(ell,h)",
        "fixed_clock_theorem": "sup_(q finite)C_h(q)=B_infinity(h)",
        "numerical_orientation": {"h1": "0.421926446", "h2": "0.328926097", "h3": "0.416224610"},
    },
    "strict_nonattainment": {
        "all_clock_endpoint": "sup_(q finite)C_h(q)=B_infinity(h) for each fixed h>=1",
        "finite_strictness": "C_h(q)<B_infinity(h) for every finite q",
        "fresh_prime_domain": "adjoin a prime P with P not dividing 2hq after a square base containing p_0(h)^2",
        "positive_lift": "N'=(P^2-1)N",
        "odd_deletion_charge": "O=sum_(odd positive runs of length L)ceil(L/2)",
        "even_excess": "E=sum_(even positive runs of length L)L/2",
        "alpha_lift": "alpha'=P^2 alpha-O=(P^2-1)alpha+E",
        "normalized_gain": "M'-M=K_1 E/((P^2-1)N)",
        "strict_iff_even": "a fresh-prime square lift is strict exactly when the old positive graph has an even run",
        "strict_every_step": False,
        "eventual_strictness": "for every finite P containing p_0(h), some larger prime-initial P' has B_(h,P')>B_(h,P): enlarge until two supported primes a,b do not divide 2h, use CRT for an exact length-2 run, then adjoin a fresh prime",
        "plateau": "M_9(36)=M_9(900)=2K_1/3 with raw (alpha,N)=(16,24) and (384,576)",
        "arbitrary_q_bridge": "for arbitrary finite q choose P containing p_0(h) and every prime divisor of q with B_(h,P)<B_infinity(h), and set Q=lcm(q,q_P); then q|Q, q_P|Q, rad(Q)=rad(q_P), and C_h(q)<=C_h(Q)=M_h(q_P)=B_(h,P)<B_infinity(h)",
        "cofinal_lower_witness": "C_h(q_P)=B_(h,P) along prime-initial supports and B_(h,P)->B_infinity(h)",
    },
    "lag_landscape_and_claim_ceiling": {
        "strict_baseline": "B_infinity(h)>3/pi^2 for every fixed finite h>=1",
        "length_one_witness": "choose supported a,b not dividing 2h to force both boundaries by CRT while keeping the center nonzero; avoidance for all remaining primes contributes a positive Euler product, hence R_(1,h)>0",
        "lag_sequence_domain": "Y>=2",
        "dY": "d_Y=product_(p<=Y,p prime)p^2, so 4 divides d_Y",
        "hY": "h_Y=d_Y/2 is a positive integer and 2h_Y=d_Y",
        "boundary_mechanism": "for lag h_Y every run boundary is caused by a prime p>Y",
        "run_start_density": "sum_(ell>=1)R_(ell,h_Y) is the density of step-d_Y run starts {r squarefree and r-d_Y nonsquarefree}",
        "odd_to_all_bound": "(1/2)sum_(ell odd)R_(ell,h_Y)<=(1/2)sum_(ell>=1)R_(ell,h_Y)",
        "tail_bound": "B_infinity(h_Y)-3/pi^2<=1/2 sum_(p>Y)1/p^2->0 by the boundary union bound",
        "infimum": "inf_(fixed h>=1)B_infinity(h)=3/pi^2",
        "infimum_attained": False,
        "supremum_or_maximum_over_h_claim": False,
        "monotonicity_in_h_claim": False,
        "growing_parameter_or_uniform_rate_claim": False,
    },
    "analytic_and_finite_roles": {
        "RH394": "sole analytic terminal-log input, instantiated at the fixed distinct shifts (+h,0,-h)",
        "RH375": "finite one-site MWIS and square-clock combinatorial precedent only",
        "RH395": "finite h=1 relation saturation and tropical optimizer precedent only",
        "RH375_terminal_clock_analytic_input": False,
        "RH395_terminal_clock_analytic_input": False,
        "certificate": "finite exact reproduction, not an analytic proof",
        "remote_sources": "four inherited closure sources only; no new direct remote analytic invocation",
    },
}


SOURCE_ROLES = {
    "RH394": {
        "analytic_input": True,
        "role": "sole_terminal_log_table_law_at_fixed_distinct_shifts",
        "shift_tuple": ["+h", "0", "-h"],
    },
    "RH375": {
        "analytic_input": False,
        "role": "finite_one_site_MWIS_and_square_clock_combinatorial_precedent_only",
    },
    "RH395": {
        "analytic_input": False,
        "role": "finite_h_equals_one_relation_saturation_and_tropical_precedent_only",
    },
    "johnston-yang-arxiv-2204.01980v2": "inherited_closure_only_via_RH394",
    "maynard-annals-2015-small-gaps": "inherited_closure_only_via_RH394",
    "tao-cambridge-2016-logarithmic-chowla": "inherited_two_point_provenance_via_RH394",
    "tao-teravainen-arxiv-1708.02610v2": "inherited_odd_parity_input_via_RH394",
    "finite_certificate": "finite_exact_reproduction_not_analytic_proof",
}


RESULT_MUTATION_NAMES = (
    "all_pass", "schema_version_float", "schema_version_bool", "paper", "title",
    "status", "role", "core_bytes", "core_hash", "core_test_hash",
    "certificate_bytes", "certificate_hash", "certificate_rows",
    "source_builder_hash", "source_test_hash", "source_closure_bytes",
    "source_closure_hash", "network", "vendor", "analytic_proof", "fixed_h",
    "fixed_q", "limit_order", "git_count", "remote_count", "logical_count",
    "logical_digest", "rights", "payload_hit", "theorem_clock",
    "theorem_h_fixed", "theorem_shift_tuple", "theorem_safety_step",
    "theorem_theta", "theorem_pi", "theorem_lambda", "theorem_projection",
    "theorem_saturation", "theorem_full8", "theorem_selfloop_exception",
    "theorem_four_state_scope", "theorem_reflection", "theorem_lift",
    "theorem_raw_weighted", "theorem_same_support_p0", "theorem_D",
    "theorem_R", "theorem_endpoint", "theorem_finite_nonattainment",
    "theorem_stepwise_strict", "theorem_infimum", "theorem_infimum_attained",
    "theorem_sup_h", "source_RH394_role", "source_RH375_role",
    "source_RH395_role", "forbidden_true", "forbidden_missing", "gate_true",
    "core_mutation_name", "core_mutation_rejected", "summary_rows",
    "summary_normalization", "summary_endpoint", "extra_key",
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
        "paper": "RH-396",
        "title": "Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity",
        "core_bytes": 129642,
        "core_sha": "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d",
        "core_test_bytes": 10631,
        "core_test_sha": "a02e4716f753aa3882ab9999cefc6be125bb8586214b18c15f921de2f64eea74",
        "certificate_bytes": 83309,
        "certificate_sha": "7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba",
        "certificate_rows": 96,
        "source_builder_bytes": 26866,
        "source_builder_sha": "4805acbe541d8e5e4f07d9fa4cd621b87b7551afeb02a0b9fcc0d8684dfa75f6",
        "source_test_bytes": 14678,
        "source_test_sha": "ce61e6b9c9eef136013123ef0fb344a7f9d7f17f2f0507faf17900a997f02b43",
        "source_closure_bytes": 57336,
        "source_closure_sha": "c16456d58efd74edf1505c430a54459e359b5ba7e1e581773e9a0613b493385b",
        "all_git_sha": "472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86",
        "logical_sha": "72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287",
        "theorem_sha": "40fe1ffaef12c9cc65abdb2cc83e060078cf71a4ad14455324ca32b6a7902682",
        "source_role_sha": "2252ae2fb6c613cd998ce174df0646ef9f0934a8584536fd105124ef74b01640",
    }
    actual = {
        "paper": PAPER, "title": TITLE,
        "core_bytes": CORE_FILE_BYTES, "core_sha": CORE_FILE_SHA256,
        "core_test_bytes": CORE_TEST_BYTES, "core_test_sha": CORE_TEST_SHA256,
        "certificate_bytes": CERTIFICATE_FIXTURE_BYTES,
        "certificate_sha": CERTIFICATE_FIXTURE_SHA256,
        "certificate_rows": CERTIFICATE_FIXTURE_ROWS,
        "source_builder_bytes": SOURCE_BUILDER_BYTES,
        "source_builder_sha": SOURCE_BUILDER_SHA256,
        "source_test_bytes": SOURCE_TEST_BYTES,
        "source_test_sha": SOURCE_TEST_SHA256,
        "source_closure_bytes": SOURCE_CLOSURE_BYTES,
        "source_closure_sha": SOURCE_CLOSURE_SHA256,
        "all_git_sha": ALL_GIT_SOURCE_SHA256,
        "logical_sha": LOGICAL_SOURCE_SHA256,
        "theorem_sha": THEOREM_CONTRACT_SHA256,
        "source_role_sha": SOURCE_ROLE_SHA256,
    }
    if not exact_equal(actual, expected):
        raise ValueError("frozen core/source identity constants changed")
    if sha256(canonical_bytes(THEOREM_CONTRACTS)).hexdigest() != THEOREM_CONTRACT_SHA256:
        raise ValueError("theorem contract literal seal changed")
    if sha256(canonical_bytes(SOURCE_ROLES)).hexdigest() != SOURCE_ROLE_SHA256:
        raise ValueError("source-role literal seal changed")
    if len(RESULT_MUTATION_NAMES) != 65 or len(set(RESULT_MUTATION_NAMES)) != 65:
        raise ValueError("result mutation contract changed")
    if len(FORBIDDEN) != 38 or any(value is not False for value in FORBIDDEN.values()):
        raise ValueError("forbidden claim contract changed")


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
    paths = {
        "core": ROOT / "src" / "fixed_lag_centered_capacity" / "core.py",
        "core_test": ROOT / "tests" / "test_core.py",
        "source": ROOT / "experiments" / "source_locks.py",
        "source_test": ROOT / "tests" / "test_source_locks.py",
    }
    expected_files = {
        "core": (CORE_FILE_BYTES, CORE_FILE_SHA256),
        "core_test": (CORE_TEST_BYTES, CORE_TEST_SHA256),
        "source": (SOURCE_BUILDER_BYTES, SOURCE_BUILDER_SHA256),
        "source_test": (SOURCE_TEST_BYTES, SOURCE_TEST_SHA256),
    }
    for name, path in paths.items():
        raw = path.read_bytes()
        expected_bytes, expected_sha = expected_files[name]
        if len(raw) != expected_bytes or sha256(raw).hexdigest() != expected_sha:
            raise RuntimeError(f"{name} file identity changed")

    certificate = build_certificate()
    certificate_raw = canonical_bytes(certificate)
    source = build_source_closure()
    source_raw = canonical_bytes(source)
    mutation_rows = _core_mutation_rows(certificate)

    identities = {
        "core_file": {"bytes": CORE_FILE_BYTES, "sha256": CORE_FILE_SHA256},
        "core_test": {"bytes": CORE_TEST_BYTES, "sha256": CORE_TEST_SHA256},
        "certificate": {
            "canonical_bytes": CERTIFICATE_FIXTURE_BYTES,
            "canonical_sha256": CERTIFICATE_FIXTURE_SHA256,
            "rows": CERTIFICATE_FIXTURE_ROWS,
        },
        "source_builder": {"bytes": SOURCE_BUILDER_BYTES, "sha256": SOURCE_BUILDER_SHA256},
        "source_test": {"bytes": SOURCE_TEST_BYTES, "sha256": SOURCE_TEST_SHA256},
        "source_closure": {
            "canonical_bytes": SOURCE_CLOSURE_BYTES,
            "canonical_sha256": SOURCE_CLOSURE_SHA256,
            "git": 160,
            "remote": 4,
            "logical": 164,
            "all_git_sha256": ALL_GIT_SOURCE_SHA256,
            "logical_sha256": LOGICAL_SOURCE_SHA256,
        },
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
        "fixed_h_only": True,
        "fixed_q_only": True,
        "phase_tables_fixed_before_limit": True,
        "limit_before_finite_maximum": True,
        "supremum_over_finite_q_after_limits": True,
        "supremum_over_h_claim": False,
    }
    summary = {
        "certificate_rows": 96,
        "core_mutations": 32,
        "core_mutations_rejected": 32,
        "source_git": 160,
        "source_remote": 4,
        "source_logical": 164,
        "relation_pairs_scanned": 262144,
        "safe_relation_pairs": 3375,
        "normalization": "on square-support q_P, alpha_h(q_P) is raw MWIS cardinality and M_h(q_P)=K_1 alpha_h(q_P)/N_h(q_P) is weighted",
        "all_clock_endpoint": "sup_(q finite)C_h(q)=B_infinity(h)",
        "finite_endpoint_attained": False,
        "lag_infimum": "inf_(fixed h>=1)B_infinity(h)=3/pi^2",
        "lag_infimum_attained": False,
        "four_state_scope": "proved when q does not divide 2h",
        "strict_every_square_support_step": False,
    }
    payload = {
        "schema_version": 1,
        "paper": PAPER,
        "title": TITLE,
        "status": "RH-396_STAGE1_CERTIFIED",
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
            and certificate.get("row_count") == 96
            and verify_certificate(certificate, compare_fresh=False) is True
            and len(source_raw) == SOURCE_CLOSURE_BYTES
            and sha256(source_raw).hexdigest() == SOURCE_CLOSURE_SHA256
            and source.get("pass") is True
            and source.get("git_count") == 160
            and source.get("remote_count") == 4
            and source.get("logical_count") == 164
            and source.get("logical_source_digest") == LOGICAL_SOURCE_SHA256
            and source.get("git", {}).get("all_git_source_digest") == ALL_GIT_SOURCE_SHA256
            and len(mutation_rows) == 32
            and all(
                row["existing_leaf_changed"] is True
                and row["false_validator_rejected"] is True
                for row in mutation_rows
            )
            and all(value is False for value in GATES.values())
            and all(value is False for value in FORBIDDEN.values())
        ),
    }
    return payload


def _make_result_validator():
    """Capture a false-mode validator independent of public builders/helpers."""

    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    certificate_bytes_literal = 83309
    certificate_sha_literal = "7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba"
    source_bytes_literal = 57336
    source_sha_literal = "c16456d58efd74edf1505c430a54459e359b5ba7e1e581773e9a0613b493385b"
    theorem_sha_literal = "40fe1ffaef12c9cc65abdb2cc83e060078cf71a4ad14455324ca32b6a7902682"
    source_role_sha_literal = "2252ae2fb6c613cd998ce174df0646ef9f0934a8584536fd105124ef74b01640"
    all_git_sha_literal = "472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86"
    logical_sha_literal = "72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287"
    result_mutations_literal = (
        "all_pass", "schema_version_float", "schema_version_bool", "paper",
        "title", "status", "role", "core_bytes", "core_hash",
        "core_test_hash", "certificate_bytes", "certificate_hash",
        "certificate_rows", "source_builder_hash", "source_test_hash",
        "source_closure_bytes", "source_closure_hash", "network", "vendor",
        "analytic_proof", "fixed_h", "fixed_q", "limit_order", "git_count",
        "remote_count", "logical_count", "logical_digest", "rights",
        "payload_hit", "theorem_clock", "theorem_h_fixed",
        "theorem_shift_tuple", "theorem_safety_step", "theorem_theta",
        "theorem_pi", "theorem_lambda", "theorem_projection",
        "theorem_saturation", "theorem_full8", "theorem_selfloop_exception",
        "theorem_four_state_scope", "theorem_reflection", "theorem_lift",
        "theorem_raw_weighted", "theorem_same_support_p0", "theorem_D",
        "theorem_R", "theorem_endpoint", "theorem_finite_nonattainment",
        "theorem_stepwise_strict", "theorem_infimum",
        "theorem_infimum_attained", "theorem_sup_h", "source_RH394_role",
        "source_RH375_role", "source_RH395_role", "forbidden_true",
        "forbidden_missing", "gate_true", "core_mutation_name",
        "core_mutation_rejected", "summary_rows", "summary_normalization",
        "summary_endpoint", "extra_key",
    )
    core_mutations_literal = (
        "fixed_h_to_growing", "fixed_q_to_growing", "d_equals_h",
        "shift_orientation_swap", "safety_step_h", "safety_unshares_letter",
        "Bp_no_dedup", "tau_counts_multiplicity", "theta_parallel_branch",
        "theta_square_branch", "Pi_sign_flip", "Pi_wrong_complement",
        "lambda_drop_x_half", "lambda_drop_y_half", "projected_wrong_center",
        "composition_reverse", "saturation_r_plus_d", "transition_includes_U",
        "tropical_drop_cycle", "four_state_on_selfloop",
        "q_divides_condition_flip", "reflection_no_input_negation",
        "p0_uses_p2_nondivisor", "base_omits_p0",
        "same_support_unconditional", "R_drop_left", "R_drop_right",
        "R_last_sign_flip", "By_drop_K1_over_D", "deletion_odd_even_swap",
        "Nprime_uses_p2N", "claim_sup_h",
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
        "causal_relabeling": False,
        "RH378_window_end_model_used": False,
        "growing_h": False,
        "h_depending_on_X": False,
        "growing_q": False,
        "q_depending_on_X": False,
        "growing_or_X_dependent_tables": False,
        "effective_uniform_rate_in_h_or_q": False,
        "ordinary_Cesaro_average": False,
        "maximum_before_terminal_limit": False,
        "adaptive_or_prelimit_capacity": False,
        "supremum_over_h_capacity_claim": False,
        "maximum_over_h_claim": False,
        "monotonicity_in_h_claim": False,
        "generic_graph_capacity": False,
        "unconditional_even_four_shift_terminal_law": False,
        "window_size_at_least_five": False,
        "RH375_used_as_terminal_clock_analytic_input": False,
        "RH395_used_as_terminal_clock_analytic_input": False,
        "four_state_compression_when_q_divides_2h": False,
        "four_state_compression_for_all_q": False,
        "same_support_scaling_without_p0_in_base": False,
        "strict_gain_at_every_square_support_prime_step": False,
        "limiting_endpoint_attained_at_finite_q": False,
        "lag_infimum_attained": False,
        "finite_certificate_is_analytic_proof": False,
        "vendored_external_payload": False,
        "network_fetch_required": False,
        "operator_model": False,
        "von_mangoldt_or_zeta_trace_formula": False,
        "zero_model": False,
        "proof_of_Riemann_Hypothesis": False,
        "Gate_A": False,
        "Gate_B": False,
        "Gate_C": False,
        "Gate_D": False,
        "Gate_E": False,
    }
    local_identities = {
        "core_file": {
            "bytes": 129642,
            "sha256": "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d",
        },
        "core_test": {
            "bytes": 10631,
            "sha256": "a02e4716f753aa3882ab9999cefc6be125bb8586214b18c15f921de2f64eea74",
        },
        "certificate": {
            "canonical_bytes": 83309,
            "canonical_sha256": certificate_sha_literal,
            "rows": 96,
        },
        "source_builder": {
            "bytes": 26866,
            "sha256": "4805acbe541d8e5e4f07d9fa4cd621b87b7551afeb02a0b9fcc0d8684dfa75f6",
        },
        "source_test": {
            "bytes": 14678,
            "sha256": "ce61e6b9c9eef136013123ef0fb344a7f9d7f17f2f0507faf17900a997f02b43",
        },
        "source_closure": {
            "canonical_bytes": 57336,
            "canonical_sha256": source_sha_literal,
            "git": 160,
            "remote": 4,
            "logical": 164,
            "all_git_sha256": all_git_sha_literal,
            "logical_sha256": logical_sha_literal,
        },
        "theorem_contract_sha256": theorem_sha_literal,
        "source_role_sha256": source_role_sha_literal,
    }
    local_declarations = {
        "network_opt_in": False,
        "requests_made": 0,
        "external_payload_vendored": False,
        "external_payload_hash_hits": [],
        "remote_redistributable_in_release": [False, False, True, False],
        "finite_reproduction_not_analytic_proof": True,
        "fixed_h_only": True,
        "fixed_q_only": True,
        "phase_tables_fixed_before_limit": True,
        "limit_before_finite_maximum": True,
        "supremum_over_finite_q_after_limits": True,
        "supremum_over_h_claim": False,
    }
    local_summary = {
        "certificate_rows": 96,
        "core_mutations": 32,
        "core_mutations_rejected": 32,
        "source_git": 160,
        "source_remote": 4,
        "source_logical": 164,
        "relation_pairs_scanned": 262144,
        "safe_relation_pairs": 3375,
        "normalization": "on square-support q_P, alpha_h(q_P) is raw MWIS cardinality and M_h(q_P)=K_1 alpha_h(q_P)/N_h(q_P) is weighted",
        "all_clock_endpoint": "sup_(q finite)C_h(q)=B_infinity(h)",
        "finite_endpoint_attained": False,
        "lag_infimum": "inf_(fixed h>=1)B_infinity(h)=3/pi^2",
        "lag_infimum_attained": False,
        "four_state_scope": "proved when q does not divide 2h",
        "strict_every_square_support_step": False,
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
            return set(left) == set(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right

    def semantic(value: object) -> bool:
        top_keys = (
            "schema_version", "paper", "title", "status", "epistemic_role",
            "identities", "declarations", "theorem_contracts", "source_roles",
            "source_closure", "certificate", "core_mutation_audit",
            "result_mutation_names", "gates", "forbidden", "summary",
            "all_pass",
        )
        if type(value) is not dict or set(value) != set(top_keys):
            return False
        if not (
            type(value["schema_version"]) is int
            and value["schema_version"] == 1
            and value["paper"] == "RH-396"
            and value["title"] == "Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity"
            and value["status"] == "RH-396_STAGE1_CERTIFIED"
            and value["epistemic_role"] == "finite_exact_reproduction_plus_frozen_analytic_interfaces"
            and value["all_pass"] is True
            and same(value["identities"], local_identities)
            and same(value["declarations"], local_declarations)
            and same(value["gates"], local_gates)
            and same(value["forbidden"], local_forbidden)
            and same(value["result_mutation_names"], list(result_mutations_literal))
            and same(value["summary"], local_summary)
        ):
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
            type(certificate) is dict
            and certificate.get("row_count") == 96
            and certificate.get("title") == "Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity"
            and certificate.get("mutation_names") == list(core_mutations_literal)
            and certificate.get("all_pass") is True
            and type(source) is dict
            and source.get("git_count") == 160
            and source.get("remote_count") == 4
            and source.get("logical_count") == 164
            and source.get("logical_source_digest") == logical_sha_literal
            and source.get("logical_digest_pass") is True
            and source.get("pass") is True
            and source.get("git", {}).get("all_git_source_digest") == all_git_sha_literal
            and source.get("remote", {}).get("network_fetch_performed") is False
            and source.get("remote", {}).get("external_payload_hash_hits") == []
            and source.get("remote", {}).get("redistributable_in_release") == [False, False, True, False]
            and source.get("source_roles", {}).get("RH375", {}).get("analytic_input") is False
        ):
            return False

        theorem = value["theorem_contracts"]
        roles = value["source_roles"]
        if not (
            type(theorem) is dict
            and set(theorem) == {
                "model_and_quantifiers", "phase_densities",
                "projection_relation_reflection", "tropical_capacity",
                "square_support_and_normalization", "euler_run_endpoint",
                "strict_nonattainment", "lag_landscape_and_claim_ceiling",
                "analytic_and_finite_roles",
            }
            and theorem["model_and_quantifiers"]["fixed_lag"] == "h>=1 is fixed before X->infinity"
            and theorem["model_and_quantifiers"]["safety_step"] == "d=2h"
            and theorem["model_and_quantifiers"]["supremum_over_h_claim"] is False
            and theorem["phase_densities"]["coordinate_shifts"] == ["L=+h", "C=0", "R=-h"]
            and theorem["phase_densities"]["Theta"].startswith("Theta_(h,q,r)(S)=")
            and theorem["phase_densities"]["phase_sum"].startswith("sum_(r mod q)Theta_(h,q,r)(S)=kappa_h(S)")
            and theorem["phase_densities"]["Pi"].startswith("Pi_(h,q,r)(U)=")
            and theorem["phase_densities"]["lambda"].startswith("lambda_(h,q,r)(x,y)=")
            and theorem["projection_relation_reflection"]["safety"] == "Target(A_r) intersect Source(A_(r+d))=empty"
            and theorem["projection_relation_reflection"]["saturation"] == "A_r=(T\\Y_(r-d)) cross Y_r"
            and theorem["projection_relation_reflection"]["terminal_sign"] == "L_(h,q)(F^rho)=-L_(h,q)(F)"
            and theorem["tropical_capacity"]["all_q_state_count"] == 8
            and theorem["tropical_capacity"]["selfloop_rule"].startswith("when q divides 2h")
            and theorem["tropical_capacity"]["four_state_scope"] == "four-state compression is proved when q does not divide 2h"
            and theorem["tropical_capacity"]["h2_q4_full8"] == ["0", "0", "1/2", "-1/2"]
            and theorem["tropical_capacity"]["h2_q4_forbidden_four"] == ["0", "0", "1", "-2"]
            and theorem["square_support_and_normalization"]["square_clock_domain"].startswith("for a finite prime set P")
            and theorem["square_support_and_normalization"]["normalization_firewall"].startswith("on square-support clocks")
            and "M_h(Q)=K_1 alpha_h(Q)/N_h(Q)" in theorem["square_support_and_normalization"]["general_square_supported_quantities"]
            and "for every t in T" in theorem["square_support_and_normalization"]["shared_coordinate_marginal"]
            and theorem["square_support_and_normalization"]["collision_safe_marginal_cases"].startswith("m_r(0)=Theta_r({C})-Theta_r({C,R})")
            and theorem["square_support_and_normalization"]["pair_charge"].startswith("mathcalK_r(U,V)+mathcalK_(r+d)(V,W)<=delta_Q")
            and theorem["square_support_and_normalization"]["centered_square_clock_equality"].startswith("if p_0(h) is in P then C_h(q_P)=M_h(q_P)")
            and "p_0(h)^2" in theorem["square_support_and_normalization"]["same_support_domain"]
            and "C_h(Q)=M_h(Q)=M_h(q_P)" in theorem["square_support_and_normalization"]["same_support_equality"]
            and theorem["euler_run_endpoint"]["infinite_D"].startswith("D_h(J)=product_p")
            and "converges absolutely" in theorem["euler_run_endpoint"]["D_convergence"]
            and theorem["euler_run_endpoint"]["run_density"].startswith("R_(ell,h)=")
            and theorem["euler_run_endpoint"]["run_event"].startswith("R_(ell,h,P) and R_(ell,h) are nonnegative densities")
            and theorem["euler_run_endpoint"]["finite_run_count"].endswith("q_P R_(ell,h,P)")
            and theorem["euler_run_endpoint"]["infinite_endpoint"].startswith("B_infinity(h)=3/pi^2")
            and theorem["strict_nonattainment"]["finite_strictness"] == "C_h(q)<B_infinity(h) for every finite q"
            and theorem["strict_nonattainment"]["strict_every_step"] is False
            and theorem["strict_nonattainment"]["eventual_strictness"].startswith("for every finite P containing p_0(h)")
            and theorem["strict_nonattainment"]["plateau"].startswith("M_9(36)=M_9(900)=2K_1/3")
            and "rad(Q)=rad(q_P)" in theorem["strict_nonattainment"]["arbitrary_q_bridge"]
            and theorem["strict_nonattainment"]["cofinal_lower_witness"].startswith("C_h(q_P)=B_(h,P)")
            and theorem["lag_landscape_and_claim_ceiling"]["infimum"] == "inf_(fixed h>=1)B_infinity(h)=3/pi^2"
            and theorem["lag_landscape_and_claim_ceiling"]["lag_sequence_domain"] == "Y>=2"
            and theorem["lag_landscape_and_claim_ceiling"]["hY"].endswith("2h_Y=d_Y")
            and theorem["lag_landscape_and_claim_ceiling"]["run_start_density"].startswith("sum_(ell>=1)R_(ell,h_Y)")
            and theorem["lag_landscape_and_claim_ceiling"]["infimum_attained"] is False
            and theorem["lag_landscape_and_claim_ceiling"]["supremum_or_maximum_over_h_claim"] is False
            and type(roles) is dict
            and roles["RH394"]["analytic_input"] is True
            and roles["RH394"]["shift_tuple"] == ["+h", "0", "-h"]
            and roles["RH375"]["analytic_input"] is False
            and roles["RH395"]["analytic_input"] is False
        ):
            return False

        rows = value["core_mutation_audit"]
        if type(rows) is not list or len(rows) != len(core_mutations_literal):
            return False
        for row, name in zip(rows, core_mutations_literal):
            if not same(row, {
                "name": name,
                "existing_leaf_changed": True,
                "false_validator_rejected": True,
            }):
                return False
        return True

    independent_semantic = semantic
    fresh_builder = build_payload

    def verifier(value: object, *, compare_fresh: bool = True) -> bool:
        if type(compare_fresh) is not bool:
            return False
        try:
            if not independent_semantic(value):
                return False
            return not compare_fresh or same(value, fresh_builder())
        except (
            ArithmeticError, AttributeError, KeyError, TypeError, ValueError,
            RuntimeError, IndexError,
        ):
            return False

    return verifier


validate_result_payload = _make_result_validator()
del _make_result_validator


def mutate_result(value: dict[str, object], name: str) -> dict[str, object]:
    if type(value) is not dict or type(name) is not str or name not in RESULT_MUTATION_NAMES:
        raise ValueError("unknown result mutation")
    changed = deepcopy(value)
    actions = {
        "all_pass": lambda: changed.__setitem__("all_pass", False),
        "schema_version_float": lambda: changed.__setitem__("schema_version", 1.0),
        "schema_version_bool": lambda: changed.__setitem__("schema_version", True),
        "paper": lambda: changed.__setitem__("paper", "RH-395"),
        "title": lambda: changed.__setitem__("title", "wrong"),
        "status": lambda: changed.__setitem__("status", "draft"),
        "role": lambda: changed.__setitem__("epistemic_role", "analytic_proof"),
        "core_bytes": lambda: changed["identities"]["core_file"].__setitem__("bytes", 129641),
        "core_hash": lambda: changed["identities"]["core_file"].__setitem__("sha256", "0" * 64),
        "core_test_hash": lambda: changed["identities"]["core_test"].__setitem__("sha256", "0" * 64),
        "certificate_bytes": lambda: changed["identities"]["certificate"].__setitem__("canonical_bytes", 83308),
        "certificate_hash": lambda: changed["identities"]["certificate"].__setitem__("canonical_sha256", "0" * 64),
        "certificate_rows": lambda: changed["identities"]["certificate"].__setitem__("rows", 95),
        "source_builder_hash": lambda: changed["identities"]["source_builder"].__setitem__("sha256", "0" * 64),
        "source_test_hash": lambda: changed["identities"]["source_test"].__setitem__("sha256", "0" * 64),
        "source_closure_bytes": lambda: changed["identities"]["source_closure"].__setitem__("canonical_bytes", 57335),
        "source_closure_hash": lambda: changed["identities"]["source_closure"].__setitem__("canonical_sha256", "0" * 64),
        "network": lambda: changed["declarations"].__setitem__("network_opt_in", True),
        "vendor": lambda: changed["declarations"].__setitem__("external_payload_vendored", True),
        "analytic_proof": lambda: changed["declarations"].__setitem__("finite_reproduction_not_analytic_proof", False),
        "fixed_h": lambda: changed["declarations"].__setitem__("fixed_h_only", False),
        "fixed_q": lambda: changed["declarations"].__setitem__("fixed_q_only", False),
        "limit_order": lambda: changed["declarations"].__setitem__("limit_before_finite_maximum", False),
        "git_count": lambda: changed["source_closure"].__setitem__("git_count", 159),
        "remote_count": lambda: changed["source_closure"].__setitem__("remote_count", 3),
        "logical_count": lambda: changed["source_closure"].__setitem__("logical_count", 163),
        "logical_digest": lambda: changed["source_closure"].__setitem__("logical_source_digest", "0" * 64),
        "rights": lambda: changed["source_closure"]["remote"].__setitem__("redistributable_in_release", [False] * 4),
        "payload_hit": lambda: changed["source_closure"]["remote"].__setitem__("external_payload_hash_hits", ["forbidden"]),
        "theorem_clock": lambda: changed["theorem_contracts"]["model_and_quantifiers"].__setitem__("clock", "omega=2"),
        "theorem_h_fixed": lambda: changed["theorem_contracts"]["model_and_quantifiers"].__setitem__("fixed_lag", "h=h(X)"),
        "theorem_shift_tuple": lambda: changed["theorem_contracts"]["phase_densities"].__setitem__("coordinate_shifts", ["L=-h", "C=0", "R=+h"]),
        "theorem_safety_step": lambda: changed["theorem_contracts"]["model_and_quantifiers"].__setitem__("safety_step", "d=h"),
        "theorem_theta": lambda: changed["theorem_contracts"]["phase_densities"].__setitem__("Theta", "wrong"),
        "theorem_pi": lambda: changed["theorem_contracts"]["phase_densities"].__setitem__("Pi", "wrong"),
        "theorem_lambda": lambda: changed["theorem_contracts"]["phase_densities"].__setitem__("lambda", "wrong"),
        "theorem_projection": lambda: changed["theorem_contracts"]["projection_relation_reflection"].__setitem__("positive_projection", "keep every output"),
        "theorem_saturation": lambda: changed["theorem_contracts"]["projection_relation_reflection"].__setitem__("saturation", "A_r=(T\\Y_(r+d)) cross Y_r"),
        "theorem_full8": lambda: changed["theorem_contracts"]["tropical_capacity"].__setitem__("all_q_state_count", 4),
        "theorem_selfloop_exception": lambda: changed["theorem_contracts"]["tropical_capacity"].__setitem__("selfloop_rule", "self-loops use four states"),
        "theorem_four_state_scope": lambda: changed["theorem_contracts"]["tropical_capacity"].__setitem__("four_state_scope", "all q"),
        "theorem_reflection": lambda: changed["theorem_contracts"]["projection_relation_reflection"].__setitem__("terminal_sign", "same sign"),
        "theorem_lift": lambda: changed["theorem_contracts"]["square_support_and_normalization"].__setitem__("divisibility_lift", "C_h(Q)<=C_h(q)"),
        "theorem_raw_weighted": lambda: changed["theorem_contracts"]["square_support_and_normalization"].__setitem__("normalization_firewall", "alpha is already weighted"),
        "theorem_same_support_p0": lambda: changed["theorem_contracts"]["square_support_and_normalization"].__setitem__("same_support_domain", "same prime support is sufficient"),
        "theorem_D": lambda: changed["theorem_contracts"]["euler_run_endpoint"].__setitem__("infinite_D", "D_h(J)=1"),
        "theorem_R": lambda: changed["theorem_contracts"]["euler_run_endpoint"].__setitem__("run_density", "R_(ell,h)=D_h([0,ell-1])"),
        "theorem_endpoint": lambda: changed["theorem_contracts"]["euler_run_endpoint"].__setitem__("infinite_endpoint", "B_infinity(h)=3/pi^2"),
        "theorem_finite_nonattainment": lambda: changed["theorem_contracts"]["strict_nonattainment"].__setitem__("finite_strictness", "equality at a finite q"),
        "theorem_stepwise_strict": lambda: changed["theorem_contracts"]["strict_nonattainment"].__setitem__("strict_every_step", True),
        "theorem_infimum": lambda: changed["theorem_contracts"]["lag_landscape_and_claim_ceiling"].__setitem__("infimum", "inf=0"),
        "theorem_infimum_attained": lambda: changed["theorem_contracts"]["lag_landscape_and_claim_ceiling"].__setitem__("infimum_attained", True),
        "theorem_sup_h": lambda: changed["theorem_contracts"]["lag_landscape_and_claim_ceiling"].__setitem__("supremum_or_maximum_over_h_claim", True),
        "source_RH394_role": lambda: changed["source_roles"]["RH394"].__setitem__("analytic_input", False),
        "source_RH375_role": lambda: changed["source_roles"]["RH375"].__setitem__("analytic_input", True),
        "source_RH395_role": lambda: changed["source_roles"]["RH395"].__setitem__("analytic_input", True),
        "forbidden_true": lambda: changed["forbidden"].__setitem__("growing_h", True),
        "forbidden_missing": lambda: changed["forbidden"].pop("growing_h"),
        "gate_true": lambda: changed["gates"].__setitem__("A_intrinsic_determinant", True),
        "core_mutation_name": lambda: changed["core_mutation_audit"][0].__setitem__("name", "wrong"),
        "core_mutation_rejected": lambda: changed["core_mutation_audit"][0].__setitem__("false_validator_rejected", False),
        "summary_rows": lambda: changed["summary"].__setitem__("certificate_rows", 95),
        "summary_normalization": lambda: changed["summary"].__setitem__("normalization", "alpha is weighted"),
        "summary_endpoint": lambda: changed["summary"].__setitem__("all_clock_endpoint", "attained maximum"),
        "extra_key": lambda: changed.__setitem__("extra", 0),
    }
    if set(actions) != set(RESULT_MUTATION_NAMES):
        raise RuntimeError("result mutation action table changed")
    actions[name]()
    return changed


def main() -> None:
    payload = build_payload()
    if validate_result_payload(payload, compare_fresh=False) is not True:
        raise RuntimeError("fresh result failed independent validation")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({
        "status": payload["status"],
        "all_pass": payload["all_pass"],
        "bytes": len(OUTPUT.read_bytes()),
        "sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
