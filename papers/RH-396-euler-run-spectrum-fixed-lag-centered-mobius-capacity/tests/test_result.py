from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest

import build_result as result


EXPECTED_FORBIDDEN = (
    "causal_or_online_centered_rule", "causal_relabeling",
    "RH378_window_end_model_used", "growing_h", "h_depending_on_X",
    "growing_q", "q_depending_on_X", "growing_or_X_dependent_tables",
    "effective_uniform_rate_in_h_or_q", "ordinary_Cesaro_average",
    "maximum_before_terminal_limit", "adaptive_or_prelimit_capacity",
    "supremum_over_h_capacity_claim", "maximum_over_h_claim",
    "monotonicity_in_h_claim", "generic_graph_capacity",
    "unconditional_even_four_shift_terminal_law",
    "window_size_at_least_five",
    "RH375_used_as_terminal_clock_analytic_input",
    "RH395_used_as_terminal_clock_analytic_input",
    "four_state_compression_when_q_divides_2h",
    "four_state_compression_for_all_q",
    "same_support_scaling_without_p0_in_base",
    "strict_gain_at_every_square_support_prime_step",
    "limiting_endpoint_attained_at_finite_q", "lag_infimum_attained",
    "finite_certificate_is_analytic_proof", "vendored_external_payload",
    "network_fetch_required", "operator_model",
    "von_mangoldt_or_zeta_trace_formula", "zero_model",
    "proof_of_Riemann_Hypothesis", "Gate_A", "Gate_B", "Gate_C",
    "Gate_D", "Gate_E",
)


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


@pytest.fixture(scope="module")
def stored() -> dict[str, object]:
    value = result.loads_strict(result.OUTPUT.read_text(encoding="utf-8"))
    require(type(value) is dict)
    require(result.validate_result_payload(value, compare_fresh=False) is True)
    return value


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_stored_pretty_and_canonical_identities(stored: dict[str, object]) -> None:
    pretty = result.OUTPUT.read_bytes()
    canonical = result.canonical_bytes(stored)
    require(len(pretty) == 290629)
    require(sha256(pretty).hexdigest() == "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4")
    require(len(canonical) == 159548)
    require(sha256(canonical).hexdigest() == "acda92bfc13344aced86dcae698c75a41ca0fe5097aaaf6141bc2ca88563db12")
    require(stored["all_pass"] is True)


def test_fresh_payload_matches_stored(stored: dict[str, object]) -> None:
    fresh = result.build_payload()
    require(result.exact_equal(fresh, stored) is True)
    require(result.validate_result_payload(stored, compare_fresh=True) is True)


def test_frozen_core_source_and_literal_seals(stored: dict[str, object]) -> None:
    identities = stored["identities"]
    require(identities["core_file"] == {
        "bytes": 129642,
        "sha256": "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d",
    })
    require(identities["core_test"] == {
        "bytes": 10631,
        "sha256": "a02e4716f753aa3882ab9999cefc6be125bb8586214b18c15f921de2f64eea74",
    })
    require(identities["certificate"] == {
        "canonical_bytes": 83309,
        "canonical_sha256": "7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba",
        "rows": 96,
    })
    require(identities["source_builder"]["sha256"] == "4805acbe541d8e5e4f07d9fa4cd621b87b7551afeb02a0b9fcc0d8684dfa75f6")
    require(identities["source_test"]["sha256"] == "ce61e6b9c9eef136013123ef0fb344a7f9d7f17f2f0507faf17900a997f02b43")
    require(identities["source_closure"] == {
        "canonical_bytes": 57336,
        "canonical_sha256": "c16456d58efd74edf1505c430a54459e359b5ba7e1e581773e9a0613b493385b",
        "git": 160,
        "remote": 4,
        "logical": 164,
        "all_git_sha256": "472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86",
        "logical_sha256": "72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287",
    })
    require(identities["theorem_contract_sha256"] == "40fe1ffaef12c9cc65abdb2cc83e060078cf71a4ad14455324ca32b6a7902682")
    require(identities["source_role_sha256"] == "2252ae2fb6c613cd998ce174df0646ef9f0934a8584536fd105124ef74b01640")


def test_exact_quantifier_density_and_relation_contracts(stored: dict[str, object]) -> None:
    theorem = stored["theorem_contracts"]
    model = theorem["model_and_quantifiers"]
    require(model["fixed_lag"] == "h>=1 is fixed before X->infinity")
    require(model["fixed_data"].startswith("q and every phase table"))
    require(model["safety_step"] == "d=2h")
    require("for every r and a,b,c,e,f in T" in model["safety"])
    require(model["supremum_over_h_claim"] is False)
    density = theorem["phase_densities"]
    require(density["coordinate_shifts"] == ["L=+h", "C=0", "R=-h"])
    require("p||q" in density["Theta"] and "p^2|q" in density["Theta"])
    require("duplicate residues removed" in density["B"])
    require(density["phase_sum"].startswith("sum_(r mod q)Theta_(h,q,r)(S)=kappa_h(S)"))
    require(density["K1"] == "every singleton has density K_1=6/pi^2")
    require(density["Pi_mass"].endswith("=1/q"))
    require("2^(-1_(x!=0)-1_(y!=0))" in density["lambda"])
    relation = theorem["projection_relation_reflection"]
    require(relation["safety"] == "Target(A_r) intersect Source(A_(r+d))=empty")
    require(relation["saturation"] == "A_r=(T\\Y_(r-d)) cross Y_r")
    require(relation["terminal_sign"] == "L_(h,q)(F^rho)=-L_(h,q)(F)")


def test_full8_selfloop_and_four_state_scope(stored: dict[str, object]) -> None:
    tropical = stored["theorem_contracts"]["tropical_capacity"]
    require(tropical["all_q_state_count"] == 8)
    require(tropical["cycles"] == "the +d map on Z/qZ has gcd(q,2h) cycles")
    require(tropical["selfloop_criterion"].startswith("q divides 2h"))
    require(tropical["four_state_scope"] == "four-state compression is proved when q does not divide 2h")
    require(tropical["four_state_masks"] == [0, 2, 5, 7])
    require(tropical["h2_q4_full8"] == ["0", "0", "1/2", "-1/2"])
    require(tropical["h2_q4_forbidden_four"] == ["0", "0", "1", "-2"])
    require(tropical["forbidden_all_q_four_state_claim"] is False)


def test_raw_weighted_endpoint_strictness_and_landscape(stored: dict[str, object]) -> None:
    theorem = stored["theorem_contracts"]
    square = theorem["square_support_and_normalization"]
    require(square["square_clock_domain"].startswith("for a finite prime set P"))
    require(square["raw_MWIS"].startswith("alpha_h(q_P)=max_"))
    require(square["weighted_capacity"] == "M_h(q_P)=K_1 alpha_h(q_P)/N_h(q_P)")
    require(square["common_positive_weight"] == "Theta_(h,q_P,r)({C})=K_1/N_h(q_P) at every positive singleton phase")
    require("M_h(Q)=K_1 alpha_h(Q)/N_h(Q)" in square["general_square_supported_quantities"])
    require("not asserted for arbitrary q with p||q" in square["normalization_firewall"])
    require("for every t in T" in square["shared_coordinate_marginal"])
    require(square["collision_safe_marginal_cases"].startswith("m_r(0)=Theta_r({C})-Theta_r({C,R})"))
    require("m_r(+/-1)=Theta_r({C,R})/2" in square["collision_safe_marginal_cases"])
    require(square["pair_charge"].startswith("mathcalK_r(U,V)+mathcalK_(r+d)(V,W)<=delta_Q"))
    require(square["centered_square_clock_equality"].startswith("if p_0(h) is in P then C_h(q_P)=M_h(q_P)"))
    require("C_h(Q)=M_h(Q)=M_h(q_P)" in square["same_support_equality"])
    require("p_0(h)^2" in square["same_support_domain"])
    require("(9,24)" in square["pre_p0_counterexample"])
    require("(291,576)" in square["post_p0_fixture"])
    endpoint = theorem["euler_run_endpoint"]
    require(endpoint["infinite_D"].startswith("D_h(J)=product_p"))
    require("converges absolutely" in endpoint["D_convergence"])
    require(endpoint["run_density"].startswith("R_(ell,h)=D_h([0,ell-1])"))
    require(endpoint["run_event"].startswith("R_(ell,h,P) and R_(ell,h) are nonnegative densities"))
    require(endpoint["finite_run_count"].endswith("q_P R_(ell,h,P)"))
    require("endpoint sum finite" in endpoint["termwise_limit"])
    require("ell<p_0(h)^2" in endpoint["run_cutoff"])
    require(endpoint["infinite_endpoint"].startswith("B_infinity(h)=3/pi^2"))
    strict = theorem["strict_nonattainment"]
    require(strict["finite_strictness"] == "C_h(q)<B_infinity(h) for every finite q")
    require(strict["alpha_lift"] == "alpha'=P^2 alpha-O=(P^2-1)alpha+E")
    require(strict["strict_every_step"] is False)
    require(strict["eventual_strictness"].startswith("for every finite P containing p_0(h)"))
    require(strict["plateau"] == "M_9(36)=M_9(900)=2K_1/3 with raw (alpha,N)=(16,24) and (384,576)")
    require("rad(Q)=rad(q_P)" in strict["arbitrary_q_bridge"])
    require(strict["cofinal_lower_witness"].startswith("C_h(q_P)=B_(h,P)"))
    landscape = theorem["lag_landscape_and_claim_ceiling"]
    require(landscape["infimum"] == "inf_(fixed h>=1)B_infinity(h)=3/pi^2")
    require(landscape["lag_sequence_domain"] == "Y>=2")
    require(landscape["hY"].endswith("2h_Y=d_Y"))
    require(landscape["run_start_density"].startswith("sum_(ell>=1)R_(ell,h_Y)"))
    require(landscape["odd_to_all_bound"].startswith("(1/2)sum_(ell odd)"))
    require(landscape["infimum_attained"] is False)
    require(landscape["supremum_or_maximum_over_h_claim"] is False)


def test_source_roles_and_declarations_are_firewalled(stored: dict[str, object]) -> None:
    roles = stored["source_roles"]
    require(roles["RH394"] == {
        "analytic_input": True,
        "role": "sole_terminal_log_table_law_at_fixed_distinct_shifts",
        "shift_tuple": ["+h", "0", "-h"],
    })
    require(roles["RH375"]["analytic_input"] is False)
    require(roles["RH395"]["analytic_input"] is False)
    declarations = stored["declarations"]
    require(declarations["network_opt_in"] is False)
    require(declarations["remote_redistributable_in_release"] == [False, False, True, False])
    require(declarations["fixed_h_only"] is True)
    require(declarations["fixed_q_only"] is True)
    require(declarations["supremum_over_h_claim"] is False)
    require(tuple(result.FORBIDDEN) == EXPECTED_FORBIDDEN)
    require(set(stored["forbidden"]) == set(EXPECTED_FORBIDDEN))
    require(all(value is False for value in stored["forbidden"].values()))


def test_all_core_mutations_are_real_and_rejected(stored: dict[str, object]) -> None:
    rows = stored["core_mutation_audit"]
    require(len(rows) == 32)
    require([row["name"] for row in rows] == list(stored["certificate"]["mutation_names"]))
    require(len({row["name"] for row in rows}) == 32)
    require(all(row["existing_leaf_changed"] is True for row in rows))
    require(all(row["false_validator_rejected"] is True for row in rows))


def test_every_result_mutation_is_distinct_and_rejected(stored: dict[str, object]) -> None:
    require(len(result.RESULT_MUTATION_NAMES) == 65)
    require(len(set(result.RESULT_MUTATION_NAMES)) == 65)
    require(stored["result_mutation_names"] == list(result.RESULT_MUTATION_NAMES))
    digests = []
    for name in result.RESULT_MUTATION_NAMES:
        changed = result.mutate_result(stored, name)
        require(result.validate_result_payload(changed, compare_fresh=False) is False, name)
        digests.append(sha256(result.canonical_bytes(changed)).hexdigest())
    require(len(set(digests)) == 65)
    with pytest.raises(ValueError):
        result.mutate_result(stored, "not_a_mutation")


def test_false_mode_uses_no_builder_helper_or_rebindable_global(
    stored: dict[str, object], monkeypatch: pytest.MonkeyPatch,
) -> None:
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden global called")

    for name in result.RESULT_BUILDER_NAMES + result.RESULT_HELPER_NAMES:
        monkeypatch.setattr(result, name, bomb)
    for name in ("sha256", "json", "deepcopy", "TITLE", "MUTATION_NAMES"):
        monkeypatch.setattr(result, name, bomb)
    require(result.validate_result_payload(stored, compare_fresh=False) is True)


def test_public_constant_and_comparator_rebinding_cannot_open_false_mode(
    stored: dict[str, object], monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(result, "PAPER", "wrong")
    monkeypatch.setattr(result, "TITLE", "wrong")
    monkeypatch.setattr(result, "CORE_FILE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "SOURCE_CLOSURE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "THEOREM_CONTRACT_SHA256", "0" * 64)
    monkeypatch.setattr(result, "SOURCE_ROLE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "RESULT_MUTATION_NAMES", ("fake",))
    monkeypatch.setattr(result, "FORBIDDEN", {"fake": False})
    monkeypatch.setattr(result, "GATES", {"fake": False})
    monkeypatch.setattr(result, "exact_equal", lambda _left, _right: True)
    monkeypatch.setattr(result, "canonical_bytes", lambda _value: b"{}")
    require(result.validate_result_payload(stored, compare_fresh=False) is True)

    coordinated = deepcopy(stored)
    coordinated["identities"]["core_file"]["sha256"] = "0" * 64
    coordinated["identities"]["certificate"]["canonical_sha256"] = "0" * 64
    coordinated["identities"]["source_closure"]["canonical_sha256"] = "0" * 64
    require(result.validate_result_payload(coordinated, compare_fresh=False) is False)
    coordinated = deepcopy(stored)
    coordinated["forbidden"] = {"fake": False}
    coordinated["result_mutation_names"] = ["fake"]
    require(result.validate_result_payload(coordinated, compare_fresh=False) is False)


def test_exact_types_membership_and_list_order_fail_closed(stored: dict[str, object]) -> None:
    attacks: list[dict[str, object]] = []
    changed = deepcopy(stored)
    changed["schema_version"] = 1.0
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["schema_version"] = True
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["summary"]["certificate_rows"] = True
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["core_mutation_audit"] = list(reversed(changed["core_mutation_audit"]))
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["result_mutation_names"] = list(reversed(changed["result_mutation_names"]))
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["declarations"]["remote_redistributable_in_release"] = [False, True, False, False]
    attacks.append(changed)
    changed = deepcopy(stored)
    del changed["theorem_contracts"]["phase_densities"]["Pi"]
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["extra"] = 0
    attacks.append(changed)
    for attack in attacks:
        require(result.validate_result_payload(attack, compare_fresh=False) is False)


def test_strict_json_no_bare_asserts_no_duplicate_dict_keys_and_factory_deleted() -> None:
    require(result.loads_strict('{"a":1}') == {"a": 1})
    with pytest.raises(ValueError):
        result.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        result.loads_strict('{"a":Infinity}')
    require(not hasattr(result, "_make_result_validator"))

    package_root = Path(__file__).resolve().parents[1]
    for path in (Path(__file__), package_root / "experiments" / "build_result.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            keys = [
                key.value for key in node.keys
                if isinstance(key, ast.Constant) and type(key.value) is str
            ]
            require(len(keys) == len(set(keys)), f"duplicate dict key in {path.name}")
