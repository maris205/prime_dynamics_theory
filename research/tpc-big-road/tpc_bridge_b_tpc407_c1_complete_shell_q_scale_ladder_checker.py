#!/usr/bin/env python3
"""Fail-closed Bridge-B checker for the TPC-407 Q-scale ladder release."""
from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/"papers/tpc-407-c1-complete-shell-q-scale-ladder"
FILES={"producer":PROJECT/"code/tpc407_c1_complete_shell_q_scale_ladder.py","independent":PROJECT/"experiments/tpc407_independent_checker.py","stress":PROJECT/"experiments/tpc407_adversarial_certificate_stress.py","certificate":PROJECT/"results/tpc407_certificate.json","main_tex":PROJECT/"paper/main.tex","main_pdf":PROJECT/"paper/main.pdf","pdf":PROJECT/"paper/paper.pdf","log":PROJECT/"paper/compile.log","readme":PROJECT/"README.md","plan":PROJECT/"PAPER_PLAN.md","derivation":PROJECT/"DERIVATION_PACKAGE.md","proof":PROJECT/"PROOF_PACKAGE.md","claim":PROJECT/"notes/claim_firewall.md","route":PROJECT/"notes/route_evaluation.md","protocol":PROJECT/"notes/computational_protocol.md","theorem":PROJECT/"notes/theorem_ledger.md","ledger":ROOT/"research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md","bridge":ROOT/"research/tpc-big-road/bridge_b_tpc407_c1_complete_shell_q_scale_ladder.md"}
LOCKS={"producer":"812432e5c791b1b70bdc67517e0fc2cc6dc92de0c6b0b244a65ff709105b087d","independent":"7bdaf9e1dc8702012c98645fcf8be1fd7096e2bdb4d773dd1c62a9fe86f248dd","stress":"cdfb859c8d190d604658eb86ace54a2346cba324526fa71b4f1e834fc8333074","certificate":"01805bc9420585f8983179c6f2971e971039d006853216c405c770b1c87f938a","main_tex":"844ebc959958ca5fe75f793261371ce0a40b0a8a4b59d325a574bc5347623860","main_pdf":"b3332f81bb2b932dae04bf374074971474e752df87859d1fab73fb2df5b98335","pdf":"b3332f81bb2b932dae04bf374074971474e752df87859d1fab73fb2df5b98335","log":"9432b72a16a5bbab2594de8fbd7b437bd4c051917463256c612c52cea728fba3","readme":"5b9a2be23d1160d0d496a10ee6c3bedb25a9c9d0d424909e68c35a6695856238","plan":"b377f1e657723edf08d899ad20d846898f453b59f6a8c82c798f4c838861be33","derivation":"a89dbdb1f4033e2aa5b6aefd4a3145221f9b34a8b02f53caba202ae47bd128f9","proof":"17c4e2d588353214fb529b111eec115196d5aeaadbb88e93d9cabe6016321078","claim":"3f0fb53a463c2c642a0f311a11f4d5194958265d4f8a451bb08da9cef9ea0619","route":"df045456a65192a513375a13b43b8f1360db0e18498d854454adbe9e22bf0e18","protocol":"b66a253a7bf98138f34e2edfba8c667f011b854a791d8c9738541d13feb2a142","theorem":"77f36c07c15dd2bc940569ae3aafb51628f4ff01fa332b1e3feed3f001cac2a2","ledger":"58b488dd3fdbdbbd25defc33f26c1940f928ebf38d8f2f96624b9678613247fb","bridge":"43911c18b02e2b9ade174335640241e7daefc40a33e24e1942b55bace5a01532"}
def digest(p):return hashlib.sha256(p.read_bytes().replace(b"\r\n",b"\n").replace(b"\r",b"\n")).hexdigest()
def fail(c,m):
 if not c:raise SystemExit(m)
def run(p,opt):
 q=subprocess.run([sys.executable]+(["-O"]if opt else[])+["-B",str(p),"--check"],cwd=ROOT,text=True,capture_output=True,check=False);fail(q.returncode==0,f"{p.name} failed: {q.stderr}");fail(q.stderr=="",f"{p.name} wrote stderr");return q.stdout
def check():
 for n,p in FILES.items():fail(p.is_file(),f"missing {n}");fail(digest(p)==LOCKS[n],f"provenance {n}")
 d=json.loads(FILES["certificate"].read_bytes());p=d["payload"];fail(d["claim_status"]=="PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_LADDER","claim status");fail(p["schema"]=="TPC407_C1_COMPLETE_SHELL_Q_SCALE_LADDER_V1","schema");fail(p["Q_scales"]==[4096,8192,16384,32768]and p["shell_counts"]==[464,872,1612,3030],"scale census");fail(p["window_rule"]=="N=264=4H","window");fail(p["theorem"]["coarse_uniform_bound"]=="z<=4/(a_min*H)<=4/H","bound");fail(p["claim_firewall"]["FULL_OPERATOR_NORM"]=="OPEN","operator firewall");fail(len(p["cases"])==4,"case census")
 n=[run(FILES[k],False)for k in("producer","independent","stress")];o=[run(FILES[k],True)for k in("producer","independent","stress")];fail(n==o,"normal/optimized mismatch");print("TPC407_BRIDGE_CHECK=PASS cases=4 q_scales=4 strict_firewall=PASS")
if __name__=="__main__":
 if sys.argv[1:]!=["--check"]:raise SystemExit("explicit --check required")
 check()
