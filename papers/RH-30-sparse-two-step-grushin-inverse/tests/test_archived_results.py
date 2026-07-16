from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def strict_json(path: Path) -> dict[str, object]:
    def reject(value: str):
        raise ValueError(f"non-finite JSON constant {value} in {path}")

    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_archived_certificates_close_their_budgets() -> None:
    for name in (
        "stored_inverse_certificate_sigma_1e-2.json",
        "stored_inverse_certificate_sigma_4e-3.json",
    ):
        data = strict_json(RESULTS / name)
        assert data["status"] == "rigorous_selected_arc_stored_model_closure"
        assert float(data["residual_frobenius_upper"]) < 1.0
        assert float(data["lifted_inverse_two_norm_upper"]) < float(
            data["lifted_inverse_budget_lower"]
        )
        assert float(data["selected_arc_inverse_two_norm_upper"]) < float(
            data["rh28_selected_arc_resolvent_budget_lower"]
        )
        assert data["source_sha256"]["run_stored_inverse_certificate.py"] == sha256(
            ROOT / "experiments" / "run_stored_inverse_certificate.py"
        )


def test_coarse_chunking_crosscheck_agrees() -> None:
    first = strict_json(RESULTS / "stored_inverse_certificate_sigma_1e-2.json")
    second = strict_json(
        RESULTS / "stored_inverse_certificate_sigma_1e-2_chunk128.json"
    )
    difference = abs(
        float(first["lifted_inverse_two_norm_upper"])
        - float(second["lifted_inverse_two_norm_upper"])
    )
    assert difference < 1.0e-7
