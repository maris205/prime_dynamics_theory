#!/usr/bin/env python3
"""Fail-closed Bridge-B release checker for TPC-417."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[2]; P=ROOT/'papers/tpc-417-c1-four-shell-finite-operator-bound'
F={'producer':P/'code/tpc417_c1_four_shell_finite_operator_bound.py','independent':P/'experiments/tpc417_independent_checker.py','stress':P/'experiments/tpc417_adversarial_certificate_stress.py','certificate':P/'results/tpc417_certificate.json','main_tex':P/'paper/main.tex','main_pdf':P/'paper/main.pdf','pdf':P/'paper/paper.pdf','log':P/'paper/compile.log','readme':P/'README.md','plan':P/'PAPER_PLAN.md','derivation':P/'DERIVATION_PACKAGE.md','proof':P/'PROOF_PACKAGE.md','claim':P/'notes/claim_firewall.md','route':P/'notes/route_evaluation.md','protocol':P/'notes/computational_protocol.md','theorem':P/'notes/theorem_ledger.md','bridge':ROOT/'research/tpc-big-road/bridge_b_tpc417_c1_four_shell_finite_operator_bound.md'}
LOCK={'producer':'f65d9d6b944cc0076d4e6367c18647cd648e829ca0d74b1743c1774ec2605f43','independent':'e0409f09b330861ccf55aed420f9a00acc42f08b2c4c94b186bf46ab1dd0ec98','stress':'404284300104238250fba92f1b01b64f94f6e0c76c62193bc356c42a5eaaa940','certificate':'1008a948634ae8472c6a25036dfeb56469e35be53e38df5afb064cc31e93c3b0','main_tex':'f92f1bd23b6c5738216ebbb91f1336f133346e4c3e3f28333ba0d560ec0fb780','main_pdf':'7484892d443c4115bbb7329ac9408d4aec3aef7fd46da83136f1acd5faa9e842','pdf':'7484892d443c4115bbb7329ac9408d4aec3aef7fd46da83136f1acd5faa9e842','log':'3ae1759f2c9edb4703b8e9bd89c38d06cc0475d8beb869fdaa86cd662148f731','readme':'8e3c38f464a7aaefbddb6294f8cd30a02ad016a62730571d49847eacd9ba2ac6','plan':'eec451f8ac476f55ec7eb048041a3960857ee85a430363a676f952bf5948522a','derivation':'2e7294f4fd8558c2ef5541e6581b43e039a2598989495e65e68eccda381bd515','proof':'52b29f22878041fc7301d9bb2b1e9a66eb189490a048f8c950068d2c967f35ca','claim':'48074e8118c268e497a3558a01359c417b615bbaaf04790dc635d7dc9a32688f','route':'a0cdd35a9b8eefdf6ef28e53194a577665e1451920cef2063ee96aed209d08f4','protocol':'b67f4c47164b980f3d988012dedbe0b3c822f7ce57855299f036b55100451486','theorem':'2798a807009d2ea373b46294bb9eea58b2931a20451d3b1f12155b5539e4d0ab','bridge':'976c93d245c107f831eec4dd15004bb4d2c25c2ff17d847b44730d4110934d27'}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c: raise SystemExit(m)
def run(p,opt):
    r=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-B',str(p),'--check'],cwd=ROOT,text=True,capture_output=True,check=False)
    need(r.returncode==0,f'{p.name} failed: {r.stderr}'); need(r.stderr=='',f'{p.name} wrote stderr'); return r.stdout
def check():
    for k,p in F.items(): need(p.is_file(),f'missing {k}'); need(LOCK[k]!='__LOCK__' and digest(p)==LOCK[k],f'provenance {k}')
    d=json.loads(F['certificate'].read_bytes()); p=d['payload']; need(d['claim_status']=='PROVED_EXACT_FINITE_FULL_OPERATOR_BOUND','status')
    need(p['schema']=='TPC417_C1_FOUR_SHELL_FINITE_OPERATOR_BOUND_V1' and p['heights']==[16,32,66,128],'domain')
    need(p['shell_counts']==[5709,10749,20390,38635] and len(p['cases'])==4,'census')
    need(p['claim_firewall']['FULL_FINITE_OPERATOR_BOUND']=='PROVED_EXACT_FINITE' and p['claim_firewall']['FULL_OPERATOR_GROWING_THEOREM']=='OPEN','firewall')
    normal=[run(F[k],False) for k in ('producer','independent','stress')]; optimized=[run(F[k],True) for k in ('producer','independent','stress')]
    need(normal==optimized,'normal/optimized mismatch')
    print('TPC417_BRIDGE_CHECK=PASS cases=4 heights=4 shells=4 shell_count=75483 full_operator_bound=PASS strict_firewall=PASS')
if __name__=='__main__':
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    check()
