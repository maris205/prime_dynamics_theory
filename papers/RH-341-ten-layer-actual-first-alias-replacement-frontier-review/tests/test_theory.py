import pytest

from actual_frontier_review import (
    DIRECTORY_NAMES,
    LAYER_LEDGER,
    ROUTE_COORDINATE,
    abstract_completion_witness,
    review_status,
)


def test_ten_layers_and_route_coordinate_are_locked():
    data = review_status()
    assert data["paper_numbers"] == list(range(332, 342))
    assert len(DIRECTORY_NAMES) == 10
    assert len(LAYER_LEDGER) == 10
    assert data["layer_count"] == 10
    assert data["proved_scoped_conclusion_count"] == 10
    assert data["discharged_aggregate_actual_replacement_count"] == 0
    assert data["route_coordinate"] == ROUTE_COORDINATE


def test_rh241_deterministic_frontier_is_distinguished_from_noisy_bridge():
    ancestry = review_status()["rh241_ancestry"]
    assert ancestry["deterministic_numerator_anchor_later_proved_by_RH263"] is True
    assert ancestry["deterministic_all_order_envelope_later_proved_by_RH267"] is True
    assert ancestry["deterministic_sharp_radius_later_proved_by_RH268"] is True
    assert ancestry["moving_noisy_all_order_coefficient_bridge_still_open"] is True
    assert ancestry["gate_A_still_open"] is True


def test_common_clock_chain_and_three_budget_requirement_are_exactly_typed():
    data = review_status()
    coordinate = data["common_coordinate"]
    assert coordinate["cut"] == "u=4k"
    assert coordinate["hardy_full_trace_identity"].startswith("q_n=B_n+S_n+R_n")
    assert coordinate["direct_identity"] == "p_n=q_n-d_n"
    assert coordinate["prefix_bound"] == "abs(P_u-E_u)<=D_u"
    three = data["conditional_three_budget_requirement"]
    assert three["head"] == "D_(4k)->0"
    assert three["off_alias"] == "E_off,(4k)->0"
    assert three["critical"] == "q_(sigma,k,2k)=o(H_k)"
    assert three["proved_in_repository"] is False


def test_abstract_cancelling_and_noncancelling_witnesses_are_exact():
    for k in (2, 4, 8, 16):
        row = abstract_completion_witness(k)
        cancelling = row["cancelling_completion"]
        noncancelling = row["noncancelling_completion"]
        assert cancelling["critical_residual"] == 0
        assert cancelling["lower_residual"] == 0
        assert noncancelling["critical_residual"] == -row["critical_atom"]
        assert noncancelling["lower_residual"] == -row["lower_atom"]
        assert noncancelling["two_atom_unsigned_size"] == (
            row["critical_atom"] + row["lower_atom"]
        )
        assert row["physical_operator_constructed"] is False


def test_invalid_abstract_witness_domain_fails_closed():
    with pytest.raises(ValueError):
        abstract_completion_witness(1)
    with pytest.raises(ValueError):
        abstract_completion_witness(True)


def test_claim_firewall_and_archive_counts_remain_open():
    data = review_status()
    assert data["open_obligation_count"] == 5
    assert not any(data["open_obligations"].values())
    assert data["expected_upstream_publication_files"] == 135
    assert data["expected_review_publication_files"] == 19
    assert data["expected_batch_publication_files"] == 154
    assert data["expected_batch_tree_files"] == 176
    assert len(data["false_claims"]) == 17
    assert not any(data["false_claims"].values())
    assert not any(data["gates"].values())
