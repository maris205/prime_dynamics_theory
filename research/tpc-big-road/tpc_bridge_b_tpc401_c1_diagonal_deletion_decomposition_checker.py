#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the exact finite TPC-401 release."""
from __future__ import annotations
import hashlib, os, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'papers/tpc-401-c1-diagonal-deletion-decomposition'
BRIDGE=ROOT/'research/tpc-big-road/bridge_b_tpc401_c1_diagonal_deletion_decomposition.md'
FILES={'producer':PROJECT/'code/tpc401_c1_diagonal_deletion_decomposition.py',
 'independent':PROJECT/'experiments/tpc401_independent_checker.py',
 'stress':PROJECT/'experiments/tpc401_adversarial_certificate_stress.py',
 'certificate':PROJECT/'results/tpc401_certificate.json','main_tex':PROJECT/'paper/main.tex',
 'main_pdf':PROJECT/'paper/main.pdf','pdf':PROJECT/'paper/paper.pdf','log':PROJECT/'paper/compile.log',
 'readme':PROJECT/'README.md','plan':PROJECT/'PAPER_PLAN.md','derivation':PROJECT/'DERIVATION_PACKAGE.md',
 'proof':PROJECT/'PROOF_PACKAGE.md','claim':PROJECT/'notes/claim_firewall.md',
 'route':PROJECT/'notes/route_evaluation.md','protocol':PROJECT/'notes/computational_protocol.md',
 'theorem':PROJECT/'notes/theorem_ledger.md','bridge':BRIDGE}
LOCKS={'producer':'b845632fed6b75c852eaad48cd430228866082d83779fd13bfd2a671e3634343','independent':'8f329e68c91577dd381d32e5280e58c039adb2e8dab6154d11770645f1dc7b9d','stress':'90f708552aac1d018cf921c65fdad4cd13e32492d3f7dd7e8ddb450092230abc','certificate':'a5dfdb714a94671bd88edefcd6ac020d6c0616bdb21d2add2067129c51f4b469','main_tex':'b3982c08680e5acb3f79e485fb6133e93680694d44e2ab8b7db9e48e977dd415','main_pdf':'1c2fdbddcdc7e5e078f9ef603a770f567e00e15c109546edeac3724ee65529f9','pdf':'1c2fdbddcdc7e5e078f9ef603a770f567e00e15c109546edeac3724ee65529f9','log':'69b9e8b0d82dfbef6c73a515c3f28a7cf2a3e3c21bfcd2078414c12e3dd2e115','readme':'f9c44038413a5379ecae5b7d7f1dd3be1b86524002bb691d2cc2220a63283f43','plan':'c468e7725d7b1be8fcd5e04b1a08971a27056e70a1731c964745ba579077ae14','derivation':'491aba0fb2895eb42d4f2fffc1f312c7370e217457b54c31e9c183f3c76bca1c','proof':'f43ca4a3fba97498b340c0c07eb4d4b1ec324d10af62f66d63c4fd9f508c154e','claim':'441ae330dec8d858d1858a398225a99820eef5daab39b78fd438348f7c99f45c','route':'ee09ec4e1e5556ed769af88aaa415ca12378b44f0242b1b3d6ce991a1ab5cc38','protocol':'9cef1f2d76c66f582e893df26d123c359e2ff2f47501c2565287e4b9faac9a58','theorem':'94a3b989f0ab629c5a9f49ea4e45055eade98d346939c5ec59d349980eb5613f','bridge':'e4fdef1699f41b18e691b2d85be89b89b3c2ea41cc58110c7d4f6f0b331e4271'}
def digest(p): return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()
def fail(c,m):
    if type(c) is not bool or not c: raise RuntimeError(m)
def run(path,opt):
    cmd=[sys.executable]+(['-O'] if opt else [])+['-B',str(path),'--check']
    e=dict(os.environ); e.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    r=subprocess.run(cmd,cwd=ROOT,env=e,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    fail(r.returncode==0 and not r.stderr,path.name+' subcheck'); return r.stdout
def main():
    fail(sys.argv[1:]==['--check'],'explicit --check required')
    for name,path in FILES.items(): fail(path.is_file(),name+' missing')
    import json
    d=json.loads(FILES['certificate'].read_bytes()); p=d['payload']; a=p['production_domain']['audit']
    fail(d['claim_status']=='PROVED_EXACT_FINITE_PRODUCTION_DOMAIN_DIAGONAL_DELETION_AUDIT','status')
    fail(p['schema']=='TPC401_C1_DIAGONAL_DELETION_DECOMPOSITION_V1','schema')
    fail(a['component_rows']==104640 and a['congruence_zero_rows']==104640 and a['component_decomposition_equal_rows']==104640,'census')
    fail(p['exact_anchor_boundary']['unit_masks_active'] is True and p['exact_anchor_boundary']['nonzero_difference']!='0','active anchor')
    for n,path in FILES.items(): fail(digest(path)==LOCKS[n],n+' provenance')
    jobs=((FILES['producer'],False),(FILES['independent'],False),(FILES['stress'],False),(FILES['producer'],True),(FILES['independent'],True),(FILES['stress'],True))
    with ThreadPoolExecutor(max_workers=6) as pool: out=tuple(pool.map(lambda x:run(*x),jobs))
    fail(out[0]==out[3] and out[1]==out[4] and out[2]==out[5],'normal optimized mismatch')
    fail(out[0].startswith(b'TPC401_CERTIFICATE=PASS') and out[1].startswith(b'TPC401_INDEPENDENT_CHECK=PASS') and out[2].startswith(b'TPC401_STRESS=PASS'),'outputs')
    print('TPC401_BRIDGE_CHECK=PASS component_rows=104640 shell=872 exact_production_identity=PASS active_anchor_counterexample=PASS')
if __name__=='__main__': main()
