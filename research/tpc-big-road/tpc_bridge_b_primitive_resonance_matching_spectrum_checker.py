#!/usr/bin/env python3
"""Fail-closed release checker for TPC-229."""
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'papers/tpc-229-primitive-resonance-matching-spectrum'
PROOF=ROOT/'research/tpc-big-road/bridge_b_primitive_resonance_matching_spectrum.md'
CERT=PROJECT/'results/certificate.json'
PROOF_SHA256='fa539dab581ac655780cccc4d5fbbc4171d10828c0ca14a4db81e669e16852a4'
class Failure(RuntimeError): pass
def req(c:bool,m:str)->None:
 if type(c) is not bool or not c: raise Failure(m)
def digest(p:Path)->str: return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()
def run(cmd:list[str])->str:
 env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; r=subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 req(r.returncode==0,f"command failed: {' '.join(cmd)}"); req(r.stderr=='',f"stderr: {' '.join(cmd)}"); return r.stdout
def nodup(pairs):
 d={}
 for k,v in pairs:
  if k in d: raise Failure(f'duplicate key {k}')
  d[k]=v
 return d
def layout()->None:
 files=('README.md','PAPER_PLAN.md','DERIVATION_PACKAGE.md','PROOF_PACKAGE.md','paper/main.tex','paper/references.bib','paper/main.pdf','paper/paper.pdf','paper/sections/0_abstract.tex','paper/sections/1_introduction.tex','paper/sections/2_matching.tex','paper/sections/3_spectrum.tex','paper/sections/4_source_block.tex','paper/sections/5_certification.tex','paper/sections/6_conclusion.tex','code/resonance_matching.py','experiments/run_certificate.py','experiments/independent_checker.py','experiments/matching_adversary.py','results/certificate.json','notes/theorem_ledger.md','notes/source_lock.md','notes/route_evaluation.md')
 for f in files: req((PROJECT/f).is_file(),f'missing {f}')
 req((PROJECT/'paper/main.pdf').read_bytes()==(PROJECT/'paper/paper.pdf').read_bytes(),'PDF mismatch')
 req(PROOF_SHA256!='TO_BE_FILLED' and digest(PROOF)==PROOF_SHA256,'proof hash')
 text=PROOF.read_text()
 for a in ('TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT','TPC229_EDGE_SPECTRUM = PROVED_EXACT','TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT','TPC229_ARITHMETIC_ADVANCE = NO','TPC229_ROUND2_CLUE = QUANTIFY_MATCHED_RESONANCE_MASS_BEFORE_SEEKING_A_FIXED_PROPORTIONAL_SAVING'): req(a in text,f'anchor {a}')
 readme=(PROJECT/'README.md').read_text(); req('Liang Wang' in readme and 'Huazhong University of Science and Technology' in readme,'author')
def certificate()->None:
 d=json.loads(CERT.read_text(),object_pairs_hook=nodup); req(d['schema']=='tpc229-primitive-resonance-matching-spectrum-v1','schema'); req(d['status']=='PASS' and d['claim_level']=='PROVED_STRUCTURAL_L1','status')
 t=d['theorem']; req(t['edge_operator_spectrum']==[-1,-1,1,1],'spectrum'); req(t['endpoint_ranges']=='10Q/7<p<8Q/5<r<2Q','ranges')
 s=d['boundary_scan']; req(s['scales_checked']==4089 and s['maximum_degree']==1,'scan'); req(s['total_edges']==13754 and s['maximum_edges']==18 and s['first_maximum_Q']==3440,'census')
 req(d['q25']['pairs']==[[37,47]],'Q25')
 expected={'aligned':Fraction(2),'anti_aligned':Fraction(0),'orthogonal':Fraction(1),'partial_negative':Fraction(2,3)}
 for k,v in expected.items(): req(Fraction(d['symmetric_fixtures'][k]['AP_over_diagonal'])==v,k)
 req(d['sharp_bilinear_fixture']['ratio_to_bound']=='1','sharpness'); f=d['firewall']; req(f['arithmetic_advance']=='NO' and f['fixed_atom_credit']==0 and f['L2']=='NONE' and f['strict_1_over_400']=='UNPAID','firewall')
def subchecks()->None:
 req('TPC229_CERTIFICATE=PASS' in run([sys.executable,'-B',str(PROJECT/'experiments/run_certificate.py'),'--check']),'producer')
 a=run([sys.executable,'-B',str(PROJECT/'experiments/independent_checker.py')]); b=run([sys.executable,'-O','-B',str(PROJECT/'experiments/independent_checker.py')]); req(a==b and 'TPC229_INDEPENDENT_CHECK=PASS' in a,'independent')
 req('TPC229_MATCHING_ADVERSARY=PASS' in run([sys.executable,'-B',str(PROJECT/'experiments/matching_adversary.py')]),'adversary')
def main()->int:
 try: layout(); certificate(); subchecks()
 except (OSError,ValueError,json.JSONDecodeError,Failure) as e: print(f'TPC229_BRIDGE_CHECK=FAIL: {e}',file=sys.stderr); return 1
 print('TPC229_BRIDGE_CHECK=PASS'); print('claim_level=PROVED_STRUCTURAL_L1'); print('arithmetic_advance=NO'); return 0
if __name__=='__main__': raise SystemExit(main())
