"""Build and independently validate the frozen RH-397 Stage-1 result."""

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

from odd_lag_half_span_capacity.core import (  # noqa: E402
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_ROWS,
    CERTIFICATE_FIXTURE_SHA256,
    MUTATION_NAMES,
    MUTATION_TARGETS,
    TITLE,
    build_certificate,
    mutate_certificate,
    verify_certificate,
)
from source_locks import build_source_closure  # noqa: E402


PAPER = "RH-397"
CORE_FILE_BYTES = 75_206
CORE_FILE_SHA256 = "4b247c0a580c06cfaeb22f29d5b9f80d52bee44fcb44ebd978153bc79e04bcd0"
CORE_TEST_BYTES = 6_648
CORE_TEST_SHA256 = "2ae8870ec42bc4c5b0c01d0445665adc6f04f17e5befeafe8b4c0944659e0af2"
SOURCE_BUILDER_BYTES = 28_217
SOURCE_BUILDER_SHA256 = "e39d4d874ae1aaa21480db9d99837d6c681164e6b667990e90be0ee97da98d91"
SOURCE_TEST_BYTES = 18_252
SOURCE_TEST_SHA256 = "45fedbdd12120a02e4dfbf5095e8d83d966696bac29a13cc6acd939cfa3e01a6"
SOURCE_CLOSURE_BYTES = 61_297
SOURCE_CLOSURE_SHA256 = "e942185086d79e5c7925082ad3edbb21b0b25c9ac98b24b6af76564abb52740d"
ALL_GIT_SOURCE_SHA256 = "b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4"
LOGICAL_SOURCE_SHA256 = "e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0"
SOURCE_GROUP_SIZES = {
    "rh396_immutable_closure": 160,
    "rh396_standard8": 8,
    "rh396_prior_external_locks": 4,
}
SOURCE_GROUP_DIGESTS = {
    "rh396_immutable_closure": "c331c37d3447ac1f54063287f5c79034b117e5c9516f3727d5eac5a148d9bd12",
    "rh396_standard8": "dbe2380bc2a6a060c69ca852625d9c2a7f20d82797108ed17fd1c0d231fa541a",
    "rh396_prior_external_locks": "57d0e03fff2be3fb1466834fefdc5fdc001e87686eb1e5898918d820163a57ea",
}

GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}

FORBIDDEN = {
    key: False for key in (
        "causal_or_online_rule", "causal_relabeling", "growing_h",
        "h_depending_on_X", "growing_q", "q_depending_on_X",
        "growing_or_X_dependent_tables", "effective_uniform_rate_in_h_or_q",
        "ordinary_Cesaro_average", "maximum_before_terminal_limit",
        "adaptive_or_prelimit_capacity", "safety_step_2h",
        "safety_unshares_one_of_two_overlap_symbols", "four_shift_analytic_input",
        "unconditional_even_four_shift_terminal_law", "c1111_analytic_call",
        "collision_free_kappa2_substitution", "collision_free_kappa3_substitution",
        "unweighted_independent_set_formula",
        "minimal_period_required_for_even_attainment",
        "odd_q_attainment_for_odd_h", "even_h_all_clock_classification",
        "growing_parameter_attainment", "generic_graph_capacity",
        "finite_certificate_is_analytic_proof", "vendored_external_payload",
        "network_fetch_required", "operator_model",
        "von_mangoldt_or_zeta_trace_formula", "zero_model",
        "proof_of_Riemann_Hypothesis", "Gate_A", "Gate_B", "Gate_C",
        "Gate_D", "Gate_E",
    )
}

THEOREM_CONTRACTS = {
    "model_and_quantifiers": {
        "alphabet": "T={-1,0,+1}",
        "mobius_extension": "mu_0(k)=mu(k) for k>=1 and 0 for k<=0",
        "phase_table_type": "F_r:T^3->{-1,+1}",
        "phase_domain": "q>=1 is a finite integer and r lies in Z/qZ; r+h is read modulo q",
        "fixed_data": "h>=1, finite q>=1, every table F_r, and the function omega are fixed before X->infinity",
        "terminal_clock": "for every omega with 1<=omega(X)<=X and omega(X)->infinity",
        "window": "F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))",
        "score": "mu(n) times the table output",
        "terminal_functional": "(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))/n",
        "fixed_table_limit": "For every fixed h>=1, q>=1, phase family F, and every admissible terminal clock omega, lim_(X->infinity)L_(h,q,X)(F;omega) exists and has the same value for all omega; denote it L_hq(F)",
        "safety": "for every r in Z/qZ and x,z,y,w in T, not(F_r(x,z,y)=+1 and F_(r+h)(z,y,w)=+1)",
        "capacity_definition": "C_h^hs(q)=max_(F universally half-span safe)|L_hq(F)| over all q-phase families F_r:T^3->{-1,+1}, with every fixed-table limit taken before the finite maximum",
        "order": ["fix_h_q_F_omega", "X_to_infinity", "finite_safe_table_maximum", "for_odd_h_only_finite_q_maximum"],
    },
    "collision_aware_densities": {
        "coordinate_shifts": ["L=+h", "C=0", "R=-h"],
        "B": "B_(p,S)={a_i mod p^2:i in S}, with duplicate residues removed",
        "nu": "nu_(p,S)=|B_(p,S)|",
        "tau": "tau_(p,S)(r)=#{b in B_(p,S):b mod p=r mod p}, after mod-p^2 deduplication",
        "Theta": "q^-1 product_(p not divide q)(1-nu/p^2) product_(p parallel q)(1-tau/p) product_(p^2 divides q)1_(r mod p^2 notin B)",
        "Theta_empty": "1/q",
        "phase_sum": "sum_(r mod q)Theta_(h,q,r)(S)=kappa_h(S)",
        "deduplicate_mod_p2_before_nu_tau": True,
        "theta_branches": ["p_not_divide_q", "p_parallel_q", "p2_divides_q"],
        "Pi": "Pi(U)=sum_(W subset {L,C,R}\\U)(-1)^|W|Theta(U union W)",
        "Pi_nonnegative": True,
        "Pi_mass": "sum_U Pi_(h,q,r)(U)=1/q",
        "Sxy": "{C} union ({L}:x!=0) union ({R}:y!=0)",
        "lambda": "Pi(S(x,y))/2^(1_(x!=0)+1_(y!=0))",
        "lambda_nonnegative_event_density": True,
        "K1": "K1=product_p(1-1/p^2)=6/pi^2",
        "kappa2": "kappa2(h)=kappa_h({L,C})=kappa_h({C,R})=product_p(1-|{0,h} mod p^2|/p^2)",
        "kappa3": "product_p(1-|{-h,0,h} mod p^2|/p^2)",
        "unconditional_K2_K3_substitution": False,
    },
    "projection_flags_rectangles_reflection": {
        "positive_projection": "retain + outputs only at center +1",
        "all_minus_baseline": "the sign-stratum average of -z is zero",
        "relation": "A_r={(x,y):F_r(x,+1,y)=+1}",
        "source_flag": "s_r=1_(+1 in Source(A_r))",
        "target_flag": "t_r=1_(+1 in Target(A_r))",
        "safety": "t_r*s_(r+h)=0",
        "relation_count": 512, "ordered_pairs": 262144, "safe_pairs": 61440,
        "flag_order": ["00", "10", "01", "11"],
        "flag_class_counts": [16, 48, 48, 400],
        "rectangle_sizes": [4, 6, 6, 9],
        "projected_terminal_limit": "sum_(r mod q)sum_((x,y) in A_r)lambda_(h,q,r)(x,y)",
        "reflection": "F^rho_r(x,z,y)=F_r(-x,-z,-y)",
        "reflection_terminal_sign": "negative",
        "both_signs_attained": True,
    },
    "phase_weights_and_edge_saturation": {
        "M": "Theta(C)", "U": "Theta(L,C)/2",
        "V": "Theta(C,R)/2", "W": "Theta(L,C,R)/4",
        "rectangle_value": "M-(1-s)U-(1-t)V+(1-s)(1-t)W",
        "bounds": ["W<=U/2", "W<=V/2"],
        "translation": "V_r=U_(r+h)",
        "phase_sums": ["sum M=K1", "sum U=sum V=kappa2(h)/2", "sum W=kappa3(h)/4"],
        "addition_gain": "U_(r+h)-(1-t_(r+h))*W_(r+h)>=0",
        "saturated_identity": "t_r=1-s_(r+h)",
    },
    "weighted_independent_set_capacity": {
        "scope": "each fixed h>=1 and finite q>=1",
        "rising_set": "J={r:s_r=0,s_(r+h)=1}",
        "independence": "J intersect (J+h)=empty, including self-loop empty",
        "surjective": True,
        "formula": "C_h^hs(q)=K1-kappa2(h)/2+(1/4)max_(J subset Z/qZ, J intersect (J+h)=empty) sum_(r in J)Theta_(h,q,r)({L,C,R})",
        "weighted_not_cardinality": True,
    },
    "odd_lag_all_clock_attainment": {
        "scope": "each fixed odd integer h>=1",
        "clock_maximum": "max_(finite q>=1)C_h^hs(q)=C_h^hs(2)=K1-kappa2(h)/2+kappa3(h)/4",
        "q2_attains": True,
        "attainment_classification": "C_h^hs(q)=K1-kappa2(h)/2+kappa3(h)/4 iff the declared finite phase clock q is even",
        "odd_clock_strictness": "C_h^hs(q)<K1-kappa2(h)/2+kappa3(h)/4 for every odd q",
        "maximum_attained": True,
        "even_lift": "literal nonminimal-period repetition; minimal period not required",
        "odd_q_strict": "CRT: p>=5, three p=3 cases, and four-class p^2 avoidance",
        "p3_cases": ["3_not_divide_h", "3_divide_h_9_not_divide_h", "9_divide_h"],
        "p2_forbidden_classes": ["h", "0", "-h", "-2h"],
        "outside_q_factors_positive": True,
        "control_basis": ["K0", "K1", "K2", "K3"],
        "controls": {
            "h1q1": ["0", "1", "-1/2", "0"],
            "h1q2": ["0", "1", "-1/2", "1/4"],
            "h1q3": ["0", "1", "-1/2", "1/12"],
            "h4q4": ["0", "1", "-3/4", "0"],
            "h9q2": ["0", "1", "-4/7", "1/3"],
        },
    },
    "analytic_source_roles_and_claim_ceiling": {
        "RH394": "sole analytic fixed-three-shift terminal law inherited through RH396",
        "RH396": "direct collision-aware density/projection finite predecessor",
        "analytic_shift_tuple": ["+h", "0", "-h"],
        "fourth_symbol_role": "w occurs only in the finite universal safety condition and is not a fourth analytic shift",
        "analytic_shift_count": 3,
        "c1111_invoked": False,
        "certificate_role": "finite reproduction not analytic proof",
    },
}

SOURCE_ROLES = {
    "RH396": "direct_collision_aware_fixed_table_density_projection_and_finite_optimizer_predecessor",
    "RH394": {"analytic_input": True, "role": "sole_fixed_three_shift_terminal_table_law_inherited_through_RH396"},
    "RH392": {"analytic_input": False, "role": "transitive_comparison_only"},
    "RH395": {"analytic_input": False, "role": "transitive_comparison_only"},
    "RH375": {"analytic_input": False, "role": "transitive_comparison_only"},
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
    "source_closure_hash", "source_git_count", "source_remote_count",
    "source_logical_count", "source_logical_digest", "rights", "payload_hit",
    "network", "vendor", "fixed_h", "fixed_q", "limit_order", "safety_step",
    "safety_shared_symbols", "safety_domain_q", "safety_domain_T4",
    "limit_not_every_clock", "limit_clock_dependent", "capacity_drops_absolute",
    "capacity_unsafe_range", "K1_wrong", "three_shift_only", "kappa_collision",
    "safe_pair_count", "flag_order", "flag_counts", "rectangle_sizes", "weight_U", "weight_W",
    "corner_sign", "translation_shift", "edge_gain", "independent_step",
    "independent_weight", "capacity_formula", "reflection", "odd_h_scope", "odd_max_omits_C2",
    "attainment_iff_even", "q2_attainment", "odd_q_strict", "even_lift",
    "control_q1", "control_q2", "control_q3", "control_h4", "control_h9",
    "predecessor_commit", "predecessor_result", "source_RH396_role",
    "source_RH394_role", "forbidden_true", "forbidden_missing", "gate_true",
    "core_mutation_name", "core_mutation_target", "core_mutation_rejected", "source_group_digest",
    "summary_rows", "summary_formula", "summary_attainment", "extra_key",
)

RESULT_BUILDER_NAMES = ("build_payload", "build_certificate", "build_source_closure", "mutate_certificate", "verify_certificate")
RESULT_HELPER_NAMES = ("canonical_bytes", "pretty_json_bytes", "exact_equal", "loads_strict")


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
    return json.loads(text, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty_json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=False, indent=2) + "\n").encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return tuple(left) == tuple(right) and all(exact_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def _core_mutation_rows(certificate: dict[str, object]) -> list[dict[str, object]]:
    targets = dict(MUTATION_TARGETS)
    output = []
    for name in MUTATION_NAMES:
        changed = mutate_certificate(certificate, name)
        changed_ids = [before["id"] for before, after in zip(certificate["rows"], changed["rows"]) if before != after]
        output.append({
            "name": name, "target_id": targets[name],
            "existing_leaf_changed": changed_ids == [targets[name]],
            "false_validator_rejected": verify_certificate(changed, compare_fresh=False) is False,
        })
    return output


def build_payload() -> dict[str, object]:
    paths = {
        "core": ROOT / "src" / "odd_lag_half_span_capacity" / "core.py",
        "core_test": ROOT / "tests" / "test_core.py",
        "source": ROOT / "experiments" / "source_locks.py",
        "source_test": ROOT / "tests" / "test_source_locks.py",
    }
    expected = {
        "core": (CORE_FILE_BYTES, CORE_FILE_SHA256), "core_test": (CORE_TEST_BYTES, CORE_TEST_SHA256),
        "source": (SOURCE_BUILDER_BYTES, SOURCE_BUILDER_SHA256), "source_test": (SOURCE_TEST_BYTES, SOURCE_TEST_SHA256),
    }
    for name, path in paths.items():
        raw = path.read_bytes()
        if (len(raw), sha256(raw).hexdigest()) != expected[name]:
            raise RuntimeError(f"{name} file identity changed")
    certificate = build_certificate()
    source = build_source_closure()
    certificate_raw = canonical_bytes(certificate)
    source_raw = canonical_bytes(source)
    mutation_rows = _core_mutation_rows(certificate)
    identities = {
        "core_file": {"bytes": CORE_FILE_BYTES, "sha256": CORE_FILE_SHA256},
        "core_test": {"bytes": CORE_TEST_BYTES, "sha256": CORE_TEST_SHA256},
        "certificate": {"canonical_bytes": CERTIFICATE_FIXTURE_BYTES, "canonical_sha256": CERTIFICATE_FIXTURE_SHA256, "rows": CERTIFICATE_FIXTURE_ROWS},
        "source_builder": {"bytes": SOURCE_BUILDER_BYTES, "sha256": SOURCE_BUILDER_SHA256},
        "source_test": {"bytes": SOURCE_TEST_BYTES, "sha256": SOURCE_TEST_SHA256},
        "source_closure": {
            "canonical_bytes": SOURCE_CLOSURE_BYTES,
            "canonical_sha256": SOURCE_CLOSURE_SHA256,
            "git": 172,
            "remote": 4,
            "logical": 176,
            "group_sizes": dict(SOURCE_GROUP_SIZES),
            "group_digests": dict(SOURCE_GROUP_DIGESTS),
            "all_git_sha256": ALL_GIT_SOURCE_SHA256,
            "logical_sha256": LOGICAL_SOURCE_SHA256,
        },
        "theorem_contract_sha256": sha256(canonical_bytes(THEOREM_CONTRACTS)).hexdigest(),
        "source_role_sha256": sha256(canonical_bytes(SOURCE_ROLES)).hexdigest(),
    }
    declarations = {
        "network_opt_in": False, "requests_made": 0,
        "external_payload_vendored": False, "external_payload_hash_hits": [],
        "remote_redistributable_in_release": [False, False, True, False],
        "finite_reproduction_not_analytic_proof": True,
        "fixed_h_only": True, "fixed_q_only": True, "phase_tables_fixed_before_limit": True,
        "terminal_clock_fixed_before_limit": True,
        "every_admissible_terminal_clock": True,
        "limit_before_finite_maximum": True,
        "all_fixed_h_q_formula": True,
        "odd_h_clock_maximum_only": True,
        "odd_h_maximum_after_limits": True,
    }
    summary = {
        "certificate_rows": 72, "core_mutations": 60, "core_mutations_rejected": 60,
        "source_git": 172, "source_remote": 4, "source_logical": 176,
        "relation_pairs_scanned": 262144, "safe_relation_pairs": 61440,
        "formula": THEOREM_CONTRACTS["weighted_independent_set_capacity"]["formula"],
        "odd_h_attainment": "C_h^hs(q)=C_h^hs(2) iff declared finite q is even",
    }
    payload = {
        "all_pass": False, "certificate": certificate, "core_mutation_audit": mutation_rows,
        "declarations": declarations, "epistemic_role": "finite_exact_reproduction_plus_frozen_analytic_interfaces",
        "forbidden": dict(FORBIDDEN), "gates": dict(GATES), "identities": identities,
        "paper": PAPER, "result_mutation_names": list(RESULT_MUTATION_NAMES),
        "schema_version": 1, "source_closure": source, "source_roles": deepcopy(SOURCE_ROLES),
        "status": "RH-397_STAGE1_CERTIFIED", "summary": summary,
        "theorem_contracts": deepcopy(THEOREM_CONTRACTS), "title": TITLE,
    }
    payload["all_pass"] = (
        len(certificate_raw) == CERTIFICATE_FIXTURE_BYTES
        and sha256(certificate_raw).hexdigest() == CERTIFICATE_FIXTURE_SHA256
        and verify_certificate(certificate, compare_fresh=False) is True
        and len(source_raw) == SOURCE_CLOSURE_BYTES
        and sha256(source_raw).hexdigest() == SOURCE_CLOSURE_SHA256
        and source["pass"] is True and source["git_count"] == 172
        and source["remote_count"] == 4 and source["logical_count"] == 176
        and source["logical_source_digest"] == LOGICAL_SOURCE_SHA256
        and source["git"]["all_git_source_digest"] == ALL_GIT_SOURCE_SHA256
        and len(mutation_rows) == 60
        and all(row["existing_leaf_changed"] and row["false_validator_rejected"] for row in mutation_rows)
        and all(value is False for value in FORBIDDEN.values())
        and all(value is False for value in GATES.values())
    )
    return payload


_RESULT_MUTATION_EDITS = {
    "all_pass": (("all_pass",), True, False),
    "schema_version_float": (("schema_version",), 1, 1.0),
    "schema_version_bool": (("schema_version",), 1, True),
    "paper": (("paper",), "RH-397", "RH-396"),
    "title": (("title",), TITLE, "mutated title"),
    "status": (("status",), "RH-397_STAGE1_CERTIFIED", "draft"),
    "role": (("epistemic_role",), "finite_exact_reproduction_plus_frozen_analytic_interfaces", "analytic proof"),
    "core_bytes": (("identities", "core_file", "bytes"), CORE_FILE_BYTES, CORE_FILE_BYTES + 1),
    "core_hash": (("identities", "core_file", "sha256"), CORE_FILE_SHA256, "0" * 64),
    "core_test_hash": (("identities", "core_test", "sha256"), CORE_TEST_SHA256, "1" * 64),
    "certificate_bytes": (("identities", "certificate", "canonical_bytes"), 24297, 24298),
    "certificate_hash": (("identities", "certificate", "canonical_sha256"), CERTIFICATE_FIXTURE_SHA256, "2" * 64),
    "certificate_rows": (("identities", "certificate", "rows"), 72, 71),
    "source_builder_hash": (("identities", "source_builder", "sha256"), SOURCE_BUILDER_SHA256, "3" * 64),
    "source_test_hash": (("identities", "source_test", "sha256"), SOURCE_TEST_SHA256, "4" * 64),
    "source_closure_bytes": (("identities", "source_closure", "canonical_bytes"), 61297, 61298),
    "source_closure_hash": (("identities", "source_closure", "canonical_sha256"), SOURCE_CLOSURE_SHA256, "5" * 64),
    "source_git_count": (("identities", "source_closure", "git"), 172, 171),
    "source_remote_count": (("identities", "source_closure", "remote"), 4, 5),
    "source_logical_count": (("identities", "source_closure", "logical"), 176, 175),
    "source_logical_digest": (("identities", "source_closure", "logical_sha256"), LOGICAL_SOURCE_SHA256, "6" * 64),
    "rights": (("declarations", "remote_redistributable_in_release", 2), True, False),
    "payload_hit": (("declarations", "external_payload_hash_hits"), [], ["0" * 64]),
    "network": (("declarations", "network_opt_in"), False, True),
    "vendor": (("declarations", "external_payload_vendored"), False, True),
    "fixed_h": (("declarations", "fixed_h_only"), True, False),
    "fixed_q": (("declarations", "fixed_q_only"), True, False),
    "limit_order": (("declarations", "limit_before_finite_maximum"), True, False),
    "safety_step": (("theorem_contracts", "model_and_quantifiers", "safety"), "for every r in Z/qZ and x,z,y,w in T, not(F_r(x,z,y)=+1 and F_(r+h)(z,y,w)=+1)", "step 2h"),
    "safety_shared_symbols": (("theorem_contracts", "model_and_quantifiers", "safety"), "for every r in Z/qZ and x,z,y,w in T, not(F_r(x,z,y)=+1 and F_(r+h)(z,y,w)=+1)", "unshared outputs"),
    "safety_domain_q": (("theorem_contracts", "model_and_quantifiers", "phase_domain"), "q>=1 is a finite integer and r lies in Z/qZ; r+h is read modulo q", "q is arbitrary"),
    "safety_domain_T4": (("theorem_contracts", "model_and_quantifiers", "safety"), "for every r in Z/qZ and x,z,y,w in T, not(F_r(x,z,y)=+1 and F_(r+h)(z,y,w)=+1)", "for some ternary word"),
    "limit_not_every_clock": (("theorem_contracts", "model_and_quantifiers", "fixed_table_limit"), "For every fixed h>=1, q>=1, phase family F, and every admissible terminal clock omega, lim_(X->infinity)L_(h,q,X)(F;omega) exists and has the same value for all omega; denote it L_hq(F)", "the limit exists for one clock"),
    "limit_clock_dependent": (("theorem_contracts", "model_and_quantifiers", "fixed_table_limit"), "For every fixed h>=1, q>=1, phase family F, and every admissible terminal clock omega, lim_(X->infinity)L_(h,q,X)(F;omega) exists and has the same value for all omega; denote it L_hq(F)", "the limit may depend on omega"),
    "capacity_drops_absolute": (("theorem_contracts", "model_and_quantifiers", "capacity_definition"), "C_h^hs(q)=max_(F universally half-span safe)|L_hq(F)| over all q-phase families F_r:T^3->{-1,+1}, with every fixed-table limit taken before the finite maximum", "C_h^hs(q)=max_F L_hq(F)"),
    "capacity_unsafe_range": (("theorem_contracts", "model_and_quantifiers", "capacity_definition"), "C_h^hs(q)=max_(F universally half-span safe)|L_hq(F)| over all q-phase families F_r:T^3->{-1,+1}, with every fixed-table limit taken before the finite maximum", "maximum over all tables"),
    "K1_wrong": (("theorem_contracts", "collision_aware_densities", "K1"), "K1=product_p(1-1/p^2)=6/pi^2", "K1=1"),
    "three_shift_only": (("theorem_contracts", "analytic_source_roles_and_claim_ceiling", "analytic_shift_count"), 3, 4),
    "kappa_collision": (("theorem_contracts", "collision_aware_densities", "unconditional_K2_K3_substitution"), False, True),
    "safe_pair_count": (("theorem_contracts", "projection_flags_rectangles_reflection", "safe_pairs"), 61440, 61439),
    "flag_order": (("theorem_contracts", "projection_flags_rectangles_reflection", "flag_order", 1), "10", "01"),
    "flag_counts": (("theorem_contracts", "projection_flags_rectangles_reflection", "flag_class_counts", 0), 16, 17),
    "rectangle_sizes": (("theorem_contracts", "projection_flags_rectangles_reflection", "rectangle_sizes", 0), 4, 5),
    "weight_U": (("theorem_contracts", "phase_weights_and_edge_saturation", "U"), "Theta(L,C)/2", "Theta(L,C)"),
    "weight_W": (("theorem_contracts", "phase_weights_and_edge_saturation", "W"), "Theta(L,C,R)/4", "Theta(L,C,R)"),
    "corner_sign": (("theorem_contracts", "phase_weights_and_edge_saturation", "rectangle_value"), "M-(1-s)U-(1-t)V+(1-s)(1-t)W", "M-(1-s)U-(1-t)V-(1-s)(1-t)W"),
    "translation_shift": (("theorem_contracts", "phase_weights_and_edge_saturation", "translation"), "V_r=U_(r+h)", "V_r=U_(r+2h)"),
    "edge_gain": (("theorem_contracts", "phase_weights_and_edge_saturation", "addition_gain"), "U_(r+h)-(1-t_(r+h))*W_(r+h)>=0", "U_(r+h)+(1-t_r)*W_(r+h)>=0"),
    "independent_step": (("theorem_contracts", "weighted_independent_set_capacity", "independence"), "J intersect (J+h)=empty, including self-loop empty", "J intersect (J+2h)=empty"),
    "independent_weight": (("theorem_contracts", "weighted_independent_set_capacity", "weighted_not_cardinality"), True, False),
    "capacity_formula": (("theorem_contracts", "weighted_independent_set_capacity", "formula"), "C_h^hs(q)=K1-kappa2(h)/2+(1/4)max_(J subset Z/qZ, J intersect (J+h)=empty) sum_(r in J)Theta_(h,q,r)({L,C,R})", "wrong formula"),
    "reflection": (("theorem_contracts", "projection_flags_rectangles_reflection", "reflection"), "F^rho_r(x,z,y)=F_r(-x,-z,-y)", "F^rho=F"),
    "odd_h_scope": (("theorem_contracts", "odd_lag_all_clock_attainment", "scope"), "each fixed odd integer h>=1", "all h"),
    "odd_max_omits_C2": (("theorem_contracts", "odd_lag_all_clock_attainment", "clock_maximum"), "max_(finite q>=1)C_h^hs(q)=C_h^hs(2)=K1-kappa2(h)/2+kappa3(h)/4", "max_q C_h^hs(q)=K1-kappa2(h)/2+kappa3(h)/4"),
    "attainment_iff_even": (("theorem_contracts", "odd_lag_all_clock_attainment", "attainment_classification"), "C_h^hs(q)=K1-kappa2(h)/2+kappa3(h)/4 iff the declared finite phase clock q is even", "all q"),
    "q2_attainment": (("theorem_contracts", "odd_lag_all_clock_attainment", "q2_attains"), True, False),
    "odd_q_strict": (("theorem_contracts", "odd_lag_all_clock_attainment", "odd_q_strict"), "CRT: p>=5, three p=3 cases, and four-class p^2 avoidance", "odd q attains"),
    "even_lift": (("theorem_contracts", "odd_lag_all_clock_attainment", "even_lift"), "literal nonminimal-period repetition; minimal period not required", "minimal period required"),
    "control_q1": (("theorem_contracts", "odd_lag_all_clock_attainment", "controls", "h1q1", 3), "0", "1/4"),
    "control_q2": (("theorem_contracts", "odd_lag_all_clock_attainment", "controls", "h1q2", 3), "1/4", "0"),
    "control_q3": (("theorem_contracts", "odd_lag_all_clock_attainment", "controls", "h1q3", 3), "1/12", "1/4"),
    "control_h4": (("theorem_contracts", "odd_lag_all_clock_attainment", "controls", "h4q4", 2), "-3/4", "-1/2"),
    "control_h9": (("theorem_contracts", "odd_lag_all_clock_attainment", "controls", "h9q2", 3), "1/3", "1/4"),
    "predecessor_commit": (("source_closure", "direct_predecessor", "commit"), "cd57086fa90939d56656c3f952a08ffad9aabefe", "0" * 40),
    "predecessor_result": (("source_closure", "direct_predecessor", "result_sha256"), "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4", "7" * 64),
    "source_RH396_role": (("source_roles", "RH396"), "direct_collision_aware_fixed_table_density_projection_and_finite_optimizer_predecessor", "analytic theorem"),
    "source_RH394_role": (("source_roles", "RH394", "analytic_input"), True, False),
    "forbidden_true": (("forbidden", "growing_q"), False, True),
    "gate_true": (("gates", "A_intrinsic_determinant"), False, True),
    "core_mutation_name": (("core_mutation_audit", 0, "name"), "mu0_to_mu", "wrong"),
    "core_mutation_target": (("core_mutation_audit", 0, "target_id"), "A01_mu0_boundary", "A02_fixed_h_q_F_clock"),
    "core_mutation_rejected": (("core_mutation_audit", 0, "false_validator_rejected"), True, False),
    "source_group_digest": (("identities", "source_closure", "group_digests", "rh396_standard8"), "dbe2380bc2a6a060c69ca852625d9c2a7f20d82797108ed17fd1c0d231fa541a", "8" * 64),
    "summary_rows": (("summary", "certificate_rows"), 72, 71),
    "summary_formula": (("summary", "formula"), "C_h^hs(q)=K1-kappa2(h)/2+(1/4)max_(J subset Z/qZ, J intersect (J+h)=empty) sum_(r in J)Theta_(h,q,r)({L,C,R})", "wrong"),
    "summary_attainment": (("summary", "odd_h_attainment"), "C_h^hs(q)=C_h^hs(2) iff declared finite q is even", "all q"),
}


def mutate_result(value: dict[str, object], name: str) -> dict[str, object]:
    if type(value) is not dict or type(name) is not str or name not in RESULT_MUTATION_NAMES:
        raise ValueError("unknown result mutation")
    changed = deepcopy(value)
    if name == "forbidden_missing":
        changed["forbidden"].pop("growing_h")
        return changed
    if name == "extra_key":
        changed["extra"] = 0
        return changed
    path, expected, replacement = _RESULT_MUTATION_EDITS[name]
    parent: object = changed
    for key in path[:-1]:
        parent = parent[key]  # type: ignore[index]
    leaf = path[-1]
    actual = parent[leaf]  # type: ignore[index]
    if not exact_equal(actual, expected):
        raise ValueError(f"mutation old leaf drifted: {name}")
    parent[leaf] = deepcopy(replacement)  # type: ignore[index]
    return changed


def _make_result_validator(fresh_builder=build_payload):
    from copy import deepcopy as local_deepcopy
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    anchor_length = 105_495
    anchor_sha = "d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a"
    pretty_anchor_length = 151_768
    pretty_anchor_sha = "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f"
    theorem_sha = "d57255a60dde7c7b0e6e87b2ea4282df96df5af8c4d4448626c7b40a98bb302b"
    source_role_sha = "154dec725c117116cf488edf3fb04ecd51724df6321a2affa5eddf83e7e76fe0"
    core_audit_sha = "4ef90633d59f3052e80b70c77eaa837db09d5e9449fb7ed1e1d6bf6d9a91b41c"
    expected_top = (
        "all_pass", "certificate", "core_mutation_audit", "declarations",
        "epistemic_role", "forbidden", "gates", "identities", "paper",
        "result_mutation_names", "schema_version", "source_closure",
        "source_roles", "status", "summary", "theorem_contracts", "title",
    )

    def json_types(value: object) -> bool:
        if type(value) is dict:
            return all(type(key) is str and json_types(item) for key, item in value.items())
        if type(value) is list:
            return all(json_types(item) for item in value)
        return type(value) in (str, bool, int, type(None))

    expected = local_deepcopy(fresh_builder())
    if not json_types(expected):
        raise RuntimeError("result producer emitted a non-exact JSON type")
    expected_bytes = local_dumps(expected, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if len(expected_bytes) != anchor_length or local_sha256(expected_bytes).hexdigest() != anchor_sha:
        raise RuntimeError("result producer disagrees with independent canonical seal")
    expected_pretty = (local_dumps(expected, ensure_ascii=False, allow_nan=False, sort_keys=False, indent=2) + "\n").encode("utf-8")
    if len(expected_pretty) != pretty_anchor_length or local_sha256(expected_pretty).hexdigest() != pretty_anchor_sha:
        raise RuntimeError("result producer disagrees with independent ordered seal")

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return tuple(left) == tuple(right) and all(same(left[key], right[key]) for key in left)
        if type(left) is list:
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        return left == right

    def public(value: object, *, compare_fresh: bool = False) -> bool:
        if type(compare_fresh) is not bool:
            raise TypeError("compare_fresh must be exact bool")
        try:
            if type(value) is not dict or not json_types(value) or not same(value, expected):
                return False
            raw = local_dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            if len(raw) != anchor_length or local_sha256(raw).hexdigest() != anchor_sha:
                return False
            pretty = (local_dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=False, indent=2) + "\n").encode("utf-8")
            if len(pretty) != pretty_anchor_length or local_sha256(pretty).hexdigest() != pretty_anchor_sha:
                return False
            if tuple(value) != expected_top or value["all_pass"] is not True:
                return False
            if type(value["schema_version"]) is not int or value["schema_version"] != 1:
                return False
            if value["paper"] != "RH-397" or value["title"] != "Odd-Lag Half-Span Overlap Mobius Capacity" or value["status"] != "RH-397_STAGE1_CERTIFIED":
                return False
            identities = value["identities"]
            if identities["certificate"] != {"canonical_bytes": 24297, "canonical_sha256": "23f714236b53c2b89caa72b53f8139cfeab74cd07132082061c3ab0dfc048697", "rows": 72}:
                return False
            source_identity = identities["source_closure"]
            if source_identity["canonical_bytes"] != 61297 or source_identity["canonical_sha256"] != "e942185086d79e5c7925082ad3edbb21b0b25c9ac98b24b6af76564abb52740d":
                return False
            if source_identity["git"] != 172 or source_identity["remote"] != 4 or source_identity["logical"] != 176:
                return False
            if source_identity["group_sizes"] != {"rh396_immutable_closure": 160, "rh396_standard8": 8, "rh396_prior_external_locks": 4}:
                return False
            if source_identity["group_digests"] != {"rh396_immutable_closure": "c331c37d3447ac1f54063287f5c79034b117e5c9516f3727d5eac5a148d9bd12", "rh396_standard8": "dbe2380bc2a6a060c69ca852625d9c2a7f20d82797108ed17fd1c0d231fa541a", "rh396_prior_external_locks": "57d0e03fff2be3fb1466834fefdc5fdc001e87686eb1e5898918d820163a57ea"}:
                return False
            if source_identity["all_git_sha256"] != "b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4" or source_identity["logical_sha256"] != "e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0":
                return False
            theorem_raw = local_dumps(value["theorem_contracts"], ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            roles_raw = local_dumps(value["source_roles"], ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            audit_raw = local_dumps(value["core_mutation_audit"], ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            if local_sha256(theorem_raw).hexdigest() != theorem_sha or identities["theorem_contract_sha256"] != theorem_sha:
                return False
            if local_sha256(roles_raw).hexdigest() != source_role_sha or identities["source_role_sha256"] != source_role_sha:
                return False
            if local_sha256(audit_raw).hexdigest() != core_audit_sha or len(value["core_mutation_audit"]) != 60:
                return False
            model = value["theorem_contracts"]["model_and_quantifiers"]
            densities = value["theorem_contracts"]["collision_aware_densities"]
            odd = value["theorem_contracts"]["odd_lag_all_clock_attainment"]
            if model["phase_domain"] != "q>=1 is a finite integer and r lies in Z/qZ; r+h is read modulo q":
                return False
            if "every admissible terminal clock omega" not in model["fixed_table_limit"] or "same value for all omega" not in model["fixed_table_limit"]:
                return False
            if model["capacity_definition"] != "C_h^hs(q)=max_(F universally half-span safe)|L_hq(F)| over all q-phase families F_r:T^3->{-1,+1}, with every fixed-table limit taken before the finite maximum":
                return False
            if densities["K1"] != "K1=product_p(1-1/p^2)=6/pi^2":
                return False
            if odd["clock_maximum"] != "max_(finite q>=1)C_h^hs(q)=C_h^hs(2)=K1-kappa2(h)/2+kappa3(h)/4":
                return False
            if odd["attainment_classification"] != "C_h^hs(q)=K1-kappa2(h)/2+kappa3(h)/4 iff the declared finite phase clock q is even":
                return False
            if value["summary"]["safe_relation_pairs"] != 61440:
                return False
            return not compare_fresh or same(value, fresh_builder())
        except (KeyError, TypeError, ValueError):
            return False

    return public


validate_result_payload = _make_result_validator()


def main() -> None:
    payload = build_payload()
    if not validate_result_payload(payload, compare_fresh=True):
        raise RuntimeError("result validation failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({"all_pass": True, "canonical_sha256": sha256(canonical_bytes(payload)).hexdigest(), "pretty_sha256": sha256(OUTPUT.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
