from copy import deepcopy

import pytest

import build_result as result
import fixed_lag_capacity.core as core


def _fresh() -> dict[str, object]:
    payload = result.build_payload()
    assert payload["all_pass"] is True
    return payload


def _reject(edit: object) -> None:
    payload = _fresh()
    edit(payload)
    assert not result.validate_result_payload(payload, compare_fresh=False)


def test_baseline_false_and_fresh_result_verification() -> None:
    payload = _fresh()
    assert result.validate_result_payload(payload, compare_fresh=False)
    assert result.validate_result_payload(payload, compare_fresh=True)
    assert payload["certificate_fixture"] == {
        "canonical_bytes": 220832,
        "sha256": result.CERTIFICATE_FIXTURE_SHA256,
        "pass": True,
    }
    assert payload["source_fixture"] == {
        "sha256": result.SOURCE_CLOSURE_SHA256,
        "pass": True,
    }


def test_stored_result_is_strict_and_fresh_byte_identical() -> None:
    stored_bytes = result.OUTPUT.read_bytes()
    stored = core.loads_strict(stored_bytes.decode("utf-8"))
    fresh = _fresh()
    assert core.exact_equal(stored, fresh)
    assert stored_bytes == result.pretty_json_bytes(fresh)
    assert result.validate_result_payload(stored, compare_fresh=False)


def test_terminal_clock_biquadratic_and_truth_table_objects_are_separate() -> None:
    theorem = _fresh()["theorems"]
    assert theorem["terminal_clock"] == {
        "admissible": "1<=omega(X)<=X for all sufficiently large X and omega(X)->infinity",
        "normalization": "1/log omega(X)",
        "interval": "X/omega(X)<n<=X",
        "limit": "X->infinity",
    }
    finite = theorem["finite_shift_diagonalization"]
    assert finite["polynomial_domain"] == "total degree at most 2 in coordinates mu0(n-a_i)"
    assert "every admissible terminal clock omega" in finite["quantifiers"]
    assert "X->infinity" in finite["functional"]
    compiler = theorem["fixed_lag_compiler"]
    diagonal = compiler["biquadratic_diagonalization"]
    truth = compiler["truth_table_specialization"]
    assert diagonal["polynomial_domain"] == "P_r(x,z)=sum_(0<=i,j<=2)c_ij(r)x^i z^j"
    assert diagonal["zero_channels"] == ["c10", "c01", "c11", "c12", "c21"]
    assert truth["alphabet"] == "T={-1,0,+1}"
    assert truth["zero_coefficients"] == ["c00", "c10", "c20"]
    assert truth["compiler_coordinates"] == ["c01", "c02", "c11", "c12", "c21", "c22"]
    assert "z*f_r(x,z)" in truth["interpolant"]
    assert "mu(n)f_" in truth["capacity_score"]
    assert "A_r={x:(x,+1) in E_r}" in compiler["projection"]


def test_capacity_max_attainment_and_landscape_are_exact() -> None:
    theorem = _fresh()["theorems"]
    capacity = theorem["capacity"]
    landscape = theorem["square_divisor_landscape"]
    assert "finite set of fixed q-phase tuples" in capacity["safe_table_set"]
    assert "max_" in capacity["definition"] and "|L_" in capacity["definition"]
    assert "limit formed before the finite maximum" in capacity["definition"]
    assert capacity["maximum_order"] == "finite fixed-table maximum after, never before, the terminal limit; no X-dependent table family"
    assert capacity["omega_independence"] is True
    assert capacity["formula"] == "G_log(q,h)=6/pi^2-kappa_h/2 for every fixed q,h"
    assert capacity["positive_witness"] == "constant table 36 gives +G_log(q,h)"
    assert capacity["negative_witness"] == "constant reflected table 72 gives -G_log(q,h)"
    assert landscape["maximum"] == "G_log(q,h)=6/pi^2-kappa_star/2 exactly for squarefree h"
    assert landscape["range"] == "3/pi^2<G_log(q,h)<=6/pi^2-kappa_star/2"
    assert landscape["infimum"] == "3/pi^2"
    assert landscape["infimum_attained"] is False


def test_source_closure_roles_and_offline_nonvendor_seals() -> None:
    payload = _fresh()
    source = payload["source_locks"]
    assert (source["git_count"], source["remote_count"], source["logical_count"]) == (106, 3, 109)
    assert source["git"]["all_git_source_digest"] == result.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert source["logical_source_digest"] == result.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert source["remote"]["network_fetch_performed"] is False
    assert source["remote"]["external_payload_hash_hits"] == []
    assert core.payload_sha256(source) == result.SOURCE_CLOSURE_SHA256
    roles = payload["source_roles"]
    assert roles["johnston-yang-arxiv-2204.01980v2"].startswith("closure-only")
    assert roles["maynard-annals-2015-small-gaps"].startswith("closure-only")
    assert roles["tao-cambridge-2016-logarithmic-chowla"].startswith("actual remote analytic input only")
    assert "proved locally here" in roles["local_precursors"]


def test_false_mode_calls_no_result_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _fresh()

    def forbidden() -> object:
        raise AssertionError("fresh result builder was called")

    monkeypatch.setattr(result, "build_payload", forbidden)
    assert result.validate_result_payload(payload, compare_fresh=False)
    with pytest.raises(AssertionError, match="fresh result builder"):
        result.validate_result_payload(payload, compare_fresh=True)


def test_gate_and_firewall_membership_is_hard_gated(monkeypatch: pytest.MonkeyPatch) -> None:
    assert type(result.EXPECTED_GATE_KEYS) is frozenset
    assert set(result.GATES) == result.EXPECTED_GATE_KEYS
    assert type(result.EXPECTED_FORBIDDEN_KEYS) is frozenset
    assert set(result.FORBIDDEN) == result.EXPECTED_FORBIDDEN_KEYS
    assert len(result.FORBIDDEN) == 23
    assert result.FORBIDDEN["X_dependent_phase_table_or_periodic_mask"] is False

    missing = dict(result.FORBIDDEN)
    del missing["growing_h"]
    monkeypatch.setattr(result, "FORBIDDEN", missing)
    with pytest.raises(ValueError, match="claim-firewall membership changed"):
        result._validate_constants()
    monkeypatch.undo()

    extra = dict(result.FORBIDDEN)
    extra["new_escape"] = False
    monkeypatch.setattr(result, "FORBIDDEN", extra)
    with pytest.raises(ValueError, match="claim-firewall membership changed"):
        result._validate_constants()
    monkeypatch.undo()

    gates = dict(result.GATES)
    del gates["A_intrinsic_determinant"]
    monkeypatch.setattr(result, "GATES", gates)
    with pytest.raises(ValueError, match="Gate membership changed"):
        result._validate_constants()


def test_theorem_source_finite_and_firewall_attacks_are_rejected() -> None:
    attacks = [
        lambda p: p["theorems"]["capacity"].__setitem__("formula", "G_log(q,h)=6/pi^2+kappa_h/2"),
        lambda p: p["theorems"]["capacity"].__setitem__("definition", "limsup_X max_f score_X(f)"),
        lambda p: p["theorems"]["capacity"].__setitem__("omega_independence", False),
        lambda p: p["theorems"]["square_divisor_landscape"].__setitem__("infimum_attained", True),
        lambda p: p["theorems"]["square_divisor_landscape"].__setitem__("maximum", "all h"),
        lambda p: p["theorems"]["finite_shift_diagonalization"].__setitem__("polynomial_domain", "total degree at most 3"),
        lambda p: p["theorems"]["fixed_lag_compiler"]["truth_table_specialization"].__setitem__("quantifiers", "an X-dependent table family"),
        lambda p: p["theorems"]["theta_local_density"].__setitem__("tau_p_r", "count site labels with multiplicity"),
        lambda p: p["source_roles"].__setitem__("tao-cambridge-2016-logarithmic-chowla", "closure-only"),
        lambda p: p["source_locks"].__setitem__("logical_source_digest", "0" * 64),
        lambda p: p["finite_contracts"]["global_closure"].__setitem__("compatible_pair_count", 3374),
        lambda p: p["finite_contracts"].__setitem__("row_partition", [640]),
        lambda p: p["declarations"].__setitem__("network_fetch_performed_by_build", 0),
        lambda p: p["forbidden_claims"].pop("growing_q"),
        lambda p: p["forbidden_claims"].__setitem__("extra_escape", False),
        lambda p: p.__setitem__("extra", False),
    ]
    for attack in attacks:
        _reject(attack)


def test_mutation_rows_and_exact_types_fail_closed() -> None:
    payload = _fresh()
    mutations = payload["mutations"]
    assert mutations["count"] == 24
    assert mutations["names"] == list(core.MUTATION_NAMES)
    assert [row["name"] for row in mutations["results"]] == list(core.MUTATION_NAMES)
    assert all(row["rejected"] is True for row in mutations["results"])

    _reject(lambda p: p.__setitem__("all_pass", 1))
    _reject(lambda p: p["certificate_fixture"].__setitem__("pass", 1))
    _reject(lambda p: p["mutations"].__setitem__("count", 24.0))
    _reject(lambda p: p["mutations"]["results"][0].__setitem__("rejected", 1))
    _reject(lambda p: p["mutations"]["results"].reverse())


def test_constant_seals_and_strict_json_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    wrong_theorem = deepcopy(result.THEOREM_CONTRACTS)
    wrong_theorem["capacity"]["formula"] = "wrong"
    monkeypatch.setattr(result, "THEOREM_CONTRACTS", wrong_theorem)
    with pytest.raises(ValueError, match="theorem contract seal changed"):
        result._validate_constants()
    monkeypatch.undo()

    wrong_roles = dict(result.SOURCE_ROLES)
    wrong_roles["local_precursors"] = "imported black box"
    monkeypatch.setattr(result, "SOURCE_ROLES", wrong_roles)
    with pytest.raises(ValueError, match="source-role contract seal changed"):
        result._validate_constants()
    monkeypatch.undo()

    with pytest.raises(ValueError, match="duplicate JSON key"):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError, match="non-finite"):
        core.loads_strict('{"a":NaN}')
    with pytest.raises(TypeError, match="compare_fresh"):
        result.validate_result_payload(_fresh(), compare_fresh=1)
