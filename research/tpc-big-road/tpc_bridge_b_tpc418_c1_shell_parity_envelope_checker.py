#!/usr/bin/env python3
"""Bridge-B checker for the TPC-418 exclusive finite-family release."""
from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'papers/tpc-418-c1-shell-parity-envelope'
F={'producer':P/'code/tpc418_c1_shell_parity_envelope.py','independent':P/'experiments/tpc418_independent_checker.py','stress':P/'experiments/tpc418_adversarial_certificate_stress.py','certificate':P/'results/tpc418_certificate.json','counterexample':P/'results/tpc418_counterexample.json','readme':P/'README.md','plan':P/'PAPER_PLAN.md','derivation':P/'DERIVATION_PACKAGE.md','proof':P/'PROOF_PACKAGE.md','claim':P/'notes/claim_firewall.md','protocol':P/'notes/computational_protocol.md','route':P/'notes/route_evaluation.md','theorem':P/'notes/theorem_ledger.md','main_tex':P/'paper/main.tex','main_pdf':P/'paper/main.pdf','pdf':P/'paper/paper.pdf','log':P/'paper/compile.log','bridge':ROOT/'research/tpc-big-road/bridge_b_tpc418_c1_shell_parity_envelope.md'}
LOCK={'producer':'1be353e891d3ca3395c6e9a26b0ddce7e0ccbfb877e2db8d1acd6af8e04d5f54','independent':'e1b01776439471201175147a00523f16de753f04a71be672d90421206a3fe511','stress':'e17a81abdc3f4e5bc85d0fdfde0e6468f74e2e5f4cfe193fa16fcb165836d391','certificate':'797c68e7d3de47197541ffe1cb78cdb78c19f062afb4d636926d10595906716b','counterexample':'1def6912490fe212b252f62995e1099c04e21489e94d7081cfd77833a071ad50','readme':'b41dd07bac9fe86a93398346868ad90a2804ff2f7ae84a40d6a6961c4d4c0f8d','plan':'54958bfbcd735de8f896add6c378c2321c276e7c908d3ba21b15c5171a47ac98','derivation':'5bec7cf6fe008a50721eb07442ee1f1c68ec6ecc6a4e616cca6665f5ef599db8','proof':'a09715f2d35b2bb02c62bae240225f3ebddac8bd28615afa7b4767aa5b6589fc','claim':'99db64703be63730711a888450b5d08e5136815e21b8fac709a08ccc2b6b6be0','protocol':'ce29d9c7fd4ff0e32a4e3f2bad9666046d0567bfa9a038d2b661cde108ef238a','route':'4e34264ac7dd18ee29a7af234d8ffa07a0514dc5984fd0bb1fb57d447b73775f','theorem':'1265c33505264839bb1c39bca01596fc6fe95978726fcdbc4a365936f181c931','main_tex':'2ed5fa45c0bdd4b406431901e7dc9bd6566da0d7322fb79abe69440cf645cd76','main_pdf':'61919cb38b2dee011292c11d8d96ec8542b896fc102b8dece22bb13dcd34b049','pdf':'61919cb38b2dee011292c11d8d96ec8542b896fc102b8dece22bb13dcd34b049','log':'09896f9b091314b59ec2873d4e63e9a54a3b13169f2f0d4c75c70ff3ae9c11f3','bridge':'6fe83ee5bbe024e5c27b453b482f24509b657e66558fd6810e64ed981b11a025'}
def need(c,m):
    if not c: raise SystemExit(m)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(p,opt):
    r=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-B',str(p),'--check'],cwd=ROOT,text=True,capture_output=True)
    need(r.returncode==0,f'{p.name} failed: {r.stderr}'); need(r.stderr=='',f'{p.name} stderr'); return r.stdout
def check():
    for k,p in F.items(): need(p.is_file(),f'missing {k}'); need(digest(p)==LOCK[k],f'provenance {k}')
    d=json.loads(F['certificate'].read_bytes()); p=d['payload']
    need(d['claim_status']=='PROVED_EXACT_FINITE_FAMILY_SHELL_PARITY_ENVELOPE','status')
    need(p['schema']=='TPC418_C1_SHELL_PARITY_ENVELOPE_V1' and len(p['fixtures'])==3,'domain')
    need('sigma_j' in p['theorem']['sigma'] and p['claim_firewall']['GROWING_UNIFORM_THEOREM']=='OPEN_UNASSUMED','firewall')
    normal=[run(F[k],False) for k in ('producer','independent','stress')]
    optimized=[run(F[k],True) for k in ('producer','independent','stress')]
    need(normal==optimized,'normal/optimized mismatch')
    print('TPC418_BRIDGE_CHECK=PASS fixtures=3 sigma=PASS independent=PASS stress=PASS paper_artifacts=PASS strict_firewall=PASS')
if __name__=='__main__':
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    check()
