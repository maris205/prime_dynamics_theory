import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_pilot_records_the_radial_block_boundary() -> None:
    payload = json.loads(
        (ROOT / "results" / "mixed_overlap_pilot.json").read_text(encoding="utf-8")
    )
    assert len(payload["rows"]) == 5
    smallest = payload["rows"][-1]
    maximum_projector = max(
        block["projector_norm"]
        for side in ("left", "right")
        for block in smallest[side]["blocks"]
    )
    assert maximum_projector > 1000.0
    assert smallest["right"]["signed_fusion_ratio"] < 1.0e-4


def test_arb_scalar_certificate_is_limited_to_its_scope() -> None:
    payload = json.loads(
        (ROOT / "results" / "arb_block_audit.json").read_text(encoding="utf-8")
    )
    assert payload["precision_bits"] == 256
    assert payload["gram_positive_certified"]
    assert not payload["production_interval_riesz_projector_executed"]
