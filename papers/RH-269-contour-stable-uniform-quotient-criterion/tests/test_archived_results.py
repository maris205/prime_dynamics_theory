import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_archived_criterion():
 p=json.loads((ROOT/"results/criterion_audit.json").read_text());assert len(p["missing_hypotheses"])==4;assert p["archived_inputs"]["fixed_noise_orthogonal_quotient_identity"] is True;assert p["archived_inputs"]["finite_power_12_contractions"] is True;assert p["theorem_boundary"]["criterion_hypotheses_verified_in_archive"] is False;assert all(p["theorem_boundary"][f"gate_{x}"] is False for x in "ABCDE")
