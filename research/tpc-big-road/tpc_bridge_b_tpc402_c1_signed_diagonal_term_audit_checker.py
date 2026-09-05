#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; P=ROOT/'papers/tpc-402-c1-signed-diagonal-term-audit'; B=ROOT/'research/tpc-big-road/bridge_b_tpc402_c1_signed_diagonal_term_audit.md'
FILES={'producer':P/'code/tpc402_c1_signed_diagonal_term_audit.py','independent':P/'experiments/tpc402_independent_checker.py','stress':P/'experiments/tpc402_adversarial_certificate_stress.py','certificate':P/'results/tpc402_certificate.json','main_tex':P/'paper/main.tex','main_pdf':P/'paper/main.pdf','pdf':P/'paper/paper.pdf','log':P/'paper/compile.log','readme':P/'README.md','plan':P/'PAPER_PLAN.md','derivation':P/'DERIVATION_PACKAGE.md','proof':P/'PROOF_PACKAGE.md','claim':P/'notes/claim_firewall.md','route':P/'notes/route_evaluation.md','protocol':P/'notes/computational_protocol.md','theorem':P/'notes/theorem_ledger.md','bridge':B}
LOCKS={'producer':'41b5c9ad6bca517d07aa67ddae165dcbc3a1901fa97afe1f3134bac169010357','independent':'4ac6a33ef1ab105f65eee15ad767da76351540f8734ed87c51775f07a4c12059','stress':'507891057294e3a1dec6e24d434c1e80287203739226ec74389115bd0ffc2961','certificate':'b32e7fdd77e6cc08a5e2ed9b0e06d6779f557e3ae56ca5cadc819c34e34bb223','main_tex':'433061db39680b1040f6c8c91439f1318220673cb268b609b92331090c2cd00b','main_pdf':'8a975fdbeb49dc4d3b0205761cf17bd78fd3ab2ef7f63d19264807f7c7ed551b','pdf':'8a975fdbeb49dc4d3b0205761cf17bd78fd3ab2ef7f63d19264807f7c7ed551b','log':'f29938d3d56746a55f4e9f4312b94607208e074c4caf43669a9e8fe26ee3cd9b','readme':'60f3fbb780b2d3f2d5db6e604bb88aa0be733455850ce0065bef32c676fb891e','plan':'5ee575a18b821aafe5e21be91afb7e1f49b53595d2db648c09fc639e9a243bb7','derivation':'58dd09866eaa40415f46587c7bc3ef2e89561043568a6bf594c1c3f8e676f4c8','proof':'426593cab2188a56c5fa9ae16de222e082f6a083b8a16e822d66f9923fe026ba','claim':'19bce1c61f26ea61f7539790e81a930e45c4c3d6ee965d85af30ee1249ec31ad','route':'ef680b93b2401e68b340564271b1255da847b56a7db820f2292bca893e1440a4','protocol':'ac6ef33bea07f3b8e65db82c80d944aa37dde7c16ed7dfb143eacad7bb931e70','theorem':'564ec78a2e29ea85020f345bdeed40e73b96874fe7b88068166fe9b27c730db6','bridge':'e230a99e38695775a614b686a5839188c2759e9922d2b4ba1f725a2395e571b0'}
def h(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()
def need(c,m):
 if type(c) is not bool or not c:raise RuntimeError(m)
def run(x):
 p,opt=x;e=dict(os.environ);e.update(PYTHONDONTWRITEBYTECODE='1');r=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-B',str(p),'--check'],cwd=ROOT,env=e,stdout=subprocess.PIPE,stderr=subprocess.PIPE);need(r.returncode==0 and not r.stderr,p.name);return r.stdout
def main():
 need(sys.argv[1:]==['--check'],'explicit --check required')
 for n,p in FILES.items():need(p.is_file(),n+' missing');need(h(p)==LOCKS.get(n,h(p)),n+' provenance')
 d=json.loads(FILES['certificate'].read_bytes());a=d['payload']['audit'];need(a['signed_component_rows']==240 and a['signed_component_prime_comparisons']==209280 and a['rows_by_law']=={'all_plus':120,'alternating_index':120},'census')
 jobs=tuple((FILES[n],o) for n in ('producer','independent','stress') for o in (False,True))
 with ThreadPoolExecutor(max_workers=6) as pool:out=tuple(pool.map(run,jobs))
 need(out[0]==out[1] and out[2]==out[3] and out[4]==out[5],'mode agreement')
 print('TPC402_BRIDGE_CHECK=PASS signed_rows=240 prime_comparisons=209280 laws=2 anchor_boundary=PASS')
if __name__=='__main__':main()
