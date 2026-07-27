import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_archived_residue_obstruction():
 p=json.loads((R/"results/residue_cocycle_audit.json").read_text())
 assert p["adjacent_case_count"]==4
 assert p["maximum_common_scalar_relative_residual"]>0.999
 assert p["minimum_common_scalar_relative_residual"]>0.32
 assert p["maximum_diagonal_cocycle_relative_residual"]<1e-12
 assert p["maximum_conjugate_multiplier_error"]<1e-10
 assert not p["theorem_boundary"]["source_independent_cocycle"]
