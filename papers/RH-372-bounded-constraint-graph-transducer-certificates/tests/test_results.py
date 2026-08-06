from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results/result.json"
SCHEMA_PATH = ROOT / "results/result.schema.json"


def _result() -> dict[str, object]:
    assert RESULT_PATH.is_file(), "run `make result` before the result firewall"
    payload = json.loads(RESULT_PATH.read_text())
    assert isinstance(payload, dict)
    return payload


def test_result_is_valid_json_and_matches_required_schema_shape() -> None:
    result = _result()
    schema = json.loads(SCHEMA_PATH.read_text())
    assert schema["$schema"].endswith("2020-12/schema")
    required = {
        "status",
        "source_locks",
        "source_commits",
        "graph_instances",
        "graph_capacity",
        "finite_audit",
        "theorem_contract",
        "claim_boundary",
        "gates",
    }
    assert required <= result.keys()
    assert result["source_locks"]["pass"] is True
    assert result["source_locks"]["count"] == len(result["source_locks"]["files"]) == 9
    assert len(result["graph_instances"]) == 3
    assert result["finite_audit"]["endpoint_N"] == 1 << 16
    assert result["finite_audit"]["prefix_witness_rows"] == 128 * 3


def test_claim_firewall_and_finite_audits() -> None:
    result = _result()
    assert result["status"] == "RH-372_bounded_constraint_graph_transducer_certificates"
    assert result["claim_boundary"]["route_a"] == "GO"
    assert result["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert all(value is False for value in result["gates"].values())
    assert result["finite_audit"]["all_safe_and_one_site"] is True
    enumeration = result["finite_audit"]["small_certificate_enumeration"]
    assert enumeration["total_tables"] == 729
    assert enumeration["safe_one_site_tables"] == 16
    assert enumeration["max_abs_coefficient_of_pi^-2"] == "4"
    assert all(
        row["safe"] and row["one_site"] and row["path_check"]
        for row in result["graph_instances"]
    )
    frozen = {
        row["name"]: (
            row["clock"],
            row["memory_states"],
            row["coefficient_of_pi^-2"],
            row["limit_constant"],
        )
        for row in result["graph_instances"]
    }
    assert frozen == {
        "RH-366-q4": (4, 2, "4", "4/pi^2"),
        "RH-368-q2": (2, 1, "4", "4/pi^2"),
        "RH-366-q3-switch": (3, 2, "9/4", "9/(4*pi^2)"),
    }


def test_schema_declares_all_gates_false() -> None:
    result = _result()
    schema = json.loads(SCHEMA_PATH.read_text())
    gate_names = schema["properties"]["gates"]["required"]
    assert set(gate_names) == set(result["gates"])
    assert all(result["gates"][name] is False for name in gate_names)
