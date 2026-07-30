"""Audit the certified sharp base and finite approach-to-one diagnostics."""

from __future__ import annotations
import json
from pathlib import Path
import sys
from flint import arb,ctx

ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent
RH13=PAPERS/"RH-13-validated-reduced-sector-spectral-gap";RH253=PAPERS/"RH-253-extended-deterministic-anchor-atlas"
sys.path[:0]=[str(ROOT/"src"),str(RH13/"src")]
from validated_gap.certificate import certify_reduced_gap  # noqa:E402


def run():
 ctx.dps=150;b=certify_reduced_gap(decimal_precision=150,dimension=50,tail_degree=100)
 r_h=arb(17)/20;q=(1/(r_h*b.lam)).upper();rho=(r_h*b.lam).lower();scaled=(b.beta_one_cube_bound*b.lam**6).upper()
 if not scaled<arb("0.801254"):raise RuntimeError("scaled trace decay not certified")
 atlas=json.loads((RH253/"results/extended_anchor_atlas.json").read_text()); qf=float(q)
 rows=[{"order":row["order"],"normalized_ratio":row["hardy_scaled_anchor"]/qf**row["order"]} for row in atlas["coefficient_rows"]]
 return {
  "status":"rh268_sharp_deterministic_coefficient_radius_law",
  "q_star":{"interval":str(q),"float_midpoint":float(q)},
  "rho_star":{"interval":str(rho),"float_midpoint":float(rho)},
  "scaled_trace_cube":{"interval":str(scaled),"float_midpoint":float(scaled)},
  "exact_conclusions":{"a_n_over_q_star_n_tends_to_one":True,"coefficient_root_rate_equals_q_star":True,"logarithm_radius_equals_rho_star":True,"critical_absolute_log_series_diverges":True,"smaller_geometric_base_impossible":True},
  "finite_order_2_to_28_diagnostic":{"row_count":len(rows),"last_six":rows[-6:],"maximum_distance_to_one_last_six":max(abs(row["normalized_ratio"]-1.0) for row in rows[-6:])},
  "theorem_boundary":{"deterministic_sharp_rate":True,"moving_cloud_sharp_rate":False,"cloud_coefficient_bridge":False,"uniform_quotient_tail":False,"gate_A":False,"gate_B":False,"gate_C":False,"gate_D":False,"gate_E":False,"hilbert_polya_operator":False,"riemann_zero_identification":False,"zeta_divisor_equality":False,"riemann_hypothesis_implication":False},
  "route_coordinate":"deterministic_envelope_sharp_at_rho_star_cloud_and_quotient_open",
 }
def main():
 p=run();o=ROOT/"results/sharp_coefficient_law.json";o.write_text(json.dumps(p,indent=2,sort_keys=True)+"\n");print(json.dumps({"output":str(o.relative_to(ROOT)),"q_star":p["q_star"]["float_midpoint"],"rho_star":p["rho_star"]["float_midpoint"]},sort_keys=True))
if __name__=="__main__":main()
