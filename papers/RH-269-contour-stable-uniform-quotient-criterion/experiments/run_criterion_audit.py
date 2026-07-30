"""Audit archived quotient results against the contour-stability criterion."""

from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent
RH222=PAPERS/"RH-222-rank-growing-conjugate-cloud-atlas";RH245=PAPERS/"RH-245-orthogonal-quotient-superloop-compression";RH259=PAPERS/"RH-259-extended-quotient-block-power-diagnostic"
sys.path.insert(0,str(ROOT/"src"))
from contour_criterion import criterion_status  # noqa:E402


def run():
 cloud=json.loads((RH222/"results/cloud_atlas.json").read_text());quot=json.loads((RH245/"results/orthogonal_quotient_audit.json").read_text());block=json.loads((RH259/"results/extended_quotient_audit.json").read_text())
 status=criterion_status(hilbert_schmidt_convergence=False,common_finite_rank_isolating_contour=False,uniform_resolvent_bound=False,limit_block_contraction=False)
 inherited={
  "fixed_noise_orthogonal_quotient_identity":quot["theorem_boundary"]["orthogonal_quotient_trace_identity_fixed_noise"],
  "finite_power_12_contractions":block["theorem_boundary"]["all_eligible_power_12_blocks_contractive"],
  "uniform_selected_subspace_stability":quot["theorem_boundary"]["uniform_selected_subspace_stability"],
  "locally_uniform_determinant_limit":cloud["theorem_boundary"]["locally_uniform_determinant_limit"],
  "uniform_small_noise_block_power":block["theorem_boundary"]["uniform_small_noise_block_power"],
  "all_archived_endpoints_audited":block["theorem_boundary"]["all_archived_endpoints_audited"],
 }
 return {
  "status":"rh269_contour_stable_uniform_quotient_criterion",
  "criterion_hypotheses":status,
  "archived_inputs":inherited,
  "missing_hypotheses":[name for name,value in status.items() if name in {"hilbert_schmidt_convergence","common_finite_rank_isolating_contour","uniform_resolvent_bound","limit_block_contraction"} and not value],
  "exact_conclusion":"If all four hypotheses hold, the orthogonal quotient compressions are locally S2-continuous and RH-246 obtains uniform K_m, eta_m<1, and L_r.",
  "theorem_boundary":{"sufficient_uniform_quotient_criterion":True,"criterion_hypotheses_verified_in_archive":False,"uniform_quotient_tail":False,"underlying_family_proved_nonuniform":False,"cloud_coefficient_bridge":False,"gate_A":False,"gate_B":False,"gate_C":False,"gate_D":False,"gate_E":False,"hilbert_polya_operator":False,"riemann_zero_identification":False,"zeta_divisor_equality":False,"riemann_hypothesis_implication":False},
  "route_coordinate":"uniform_quotient_sufficient_criterion_exact_four_hypotheses_open",
 }
def main():
 p=run();o=ROOT/"results/criterion_audit.json";o.write_text(json.dumps(p,indent=2,sort_keys=True)+"\n");print(json.dumps({"output":str(o.relative_to(ROOT)),"missing":len(p["missing_hypotheses"])},sort_keys=True))
if __name__=="__main__":main()
