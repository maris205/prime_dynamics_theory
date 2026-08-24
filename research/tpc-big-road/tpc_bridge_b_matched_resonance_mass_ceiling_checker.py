#!/usr/bin/env python3
"""Fail-closed release checker for TPC-230."""
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'papers/tpc-230-matched-resonance-mass-ceiling';PROOF=ROOT/'research/tpc-big-road/bridge_b_matched_resonance_mass_ceiling.md';CERT=P/'results/certificate.json';PROOF_SHA256='c411065eed9a1c7e935afea13fb6c9a597bcba9ab8a7e5e7528e86edea73d88c'
class F(RuntimeError):pass
def req(c,m):
 if type(c) is not bool or not c:raise F(m)
def sha(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()
def run(c):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';r=subprocess.run(c,cwd=ROOT,env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);req(r.returncode==0,f'failed {c}');req(r.stderr=='',f'stderr {c}');return r.stdout
def nodup(ps):
 d={}
 for k,v in ps:
  if k in d:raise F('duplicate')
  d[k]=v
 return d
def layout():
 fs=('README.md','PAPER_PLAN.md','DERIVATION_PACKAGE.md','PROOF_PACKAGE.md','paper/main.tex','paper/references.bib','paper/main.pdf','paper/paper.pdf','paper/sections/0_abstract.tex','paper/sections/1_introduction.tex','paper/sections/2_mass_ceiling.tex','paper/sections/3_density_toll.tex','paper/sections/4_literal_rows.tex','paper/sections/5_certification.tex','paper/sections/6_conclusion.tex','code/matched_mass_ceiling.py','experiments/run_certificate.py','experiments/independent_checker.py','experiments/mass_adversary.py','results/certificate.json','notes/theorem_ledger.md','notes/source_lock.md','notes/route_evaluation.md')
 for f in fs:req((P/f).is_file(),f'missing {f}')
 req((P/'paper/main.pdf').read_bytes()==(P/'paper/paper.pdf').read_bytes(),'PDF');req(PROOF_SHA256!='TO_BE_FILLED' and sha(PROOF)==PROOF_SHA256,'proof hash')
 t=PROOF.read_text()
 for a in ('TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP','TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200','TPC230_ARITHMETIC_ADVANCE = NO','TPC230_ROUND2_CLUE = APPLY_A_TWO_LINEAR_FORM_UPPER_BOUND_SIEVE_TO_THE_3_7_RESONANCE_COUNT'):req(a in t,a)
 r=(P/'README.md').read_text();req('Liang Wang' in r and 'Huazhong University of Science and Technology' in r,'author')
def cert():
 d=json.loads(CERT.read_text(),object_pairs_hook=nodup);req(d['schema']=='tpc230-matched-resonance-mass-ceiling-v1','schema');req(d['status']=='PASS' and d['claim_level']=='PROVED_STRUCTURAL_L1','status')
 t=d['theorem'];req(t['literal_aligned_kappa_bound']==4 and t['strict_1_over_400_edge_density_toll']=='E/P>=1/3200 is necessary under literal kappa<=4','toll')
 q=d['q25'];req(q['uniform_mass_fraction']=='1/3' and q['literal_aligned_mass_fraction']=='5/13','Q25')
 s=d['boundary_scan'];req(s['scales_checked']==4089 and s['edge_bearing_scales']==2268 and s['zero_edge_scales']==1821,'scan')
 x=d['sharp_fixture'];req(Fraction(x['AP'])==Fraction(x['unmatched_mass']) and Fraction(x['saving'])==Fraction(x['matched_mass']),'sharp')
 f=d['firewall'];req(f['arithmetic_advance']=='NO' and f['fixed_atom_credit']==0 and f['L2']=='NONE' and f['strict_1_over_400']=='UNPAID','firewall')
def subs():
 req('TPC230_CERTIFICATE=PASS' in run([sys.executable,'-B',str(P/'experiments/run_certificate.py'),'--check']),'producer');a=run([sys.executable,'-B',str(P/'experiments/independent_checker.py')]);b=run([sys.executable,'-O','-B',str(P/'experiments/independent_checker.py')]);req(a==b and 'TPC230_INDEPENDENT_CHECK=PASS' in a,'independent');req('TPC230_MASS_ADVERSARY=PASS' in run([sys.executable,'-B',str(P/'experiments/mass_adversary.py')]),'adversary')
def main():
 try:layout();cert();subs()
 except (OSError,ValueError,json.JSONDecodeError,F) as e:print(f'TPC230_BRIDGE_CHECK=FAIL: {e}',file=sys.stderr);return 1
 print('TPC230_BRIDGE_CHECK=PASS');print('claim_level=PROVED_STRUCTURAL_L1');print('arithmetic_advance=NO');return 0
if __name__=='__main__':raise SystemExit(main())
