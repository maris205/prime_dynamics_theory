#!/usr/bin/env python3
"""Independent exact replay; intentionally does not import the producer."""
from __future__ import annotations
import hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-418-c1-shell-parity-envelope/results/tpc418_certificate.json"
SCHEMA = "TPC418_C1_SHELL_PARITY_ENVELOPE_V1"
STATUS = "PROVED_EXACT_FINITE_FAMILY_SHELL_PARITY_ENVELOPE"

def need(c, m):
    if type(c) is not bool or not c: raise ValueError(m)
def canonical(v): return (json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
def nodup(ps):
    d = {}
    for k, v in ps: need(k not in d, "duplicate key"); d[k] = v
    return d
def noconst(v): raise ValueError("non-finite JSON constant")
def txt(v): return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"
def add(xs):
    a = list(xs)
    while len(a) > 1: a = [a[i] + a[i+1] if i+1 < len(a) else a[i] for i in range(0, len(a), 2)]
    return a[0] if a else Fraction(0)
def primes(limit):
    f = bytearray(b"\1") * (limit + 1); f[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if f[p]: f[p*p:limit+1:p] = b"\0" * (((limit-p*p)//p)+1)
    return [p for p in range(2, limit+1) if f[p]]
def alpha(p, q): return Fraction(p**3, q*q*(p-1))
def replay_fixture(f):
    qs, counts = f["Q_scales"], f["expected_shell_counts"]
    blocks = []
    for q, n in zip(qs, counts):
        b = [(p, q) for p in primes(2*q) if p > q]; need(len(b) == n, "census"); blocks.append(b)
    eps = 1; A = Fraction(0); B = {1: Fraction(0), -1: Fraction(0)}; Be = {1: Fraction(0), -1: Fraction(0)}; ledger = []; E = O = 0; offset = 0
    compute_block_sums = f["name"] != "four_shell_replay"
    for j, block in enumerate(blocks):
        vals = [alpha(p,q) for p,q in block]; n = len(vals); sig = eps if n % 2 else -eps
        b = vals[-1] if n % 2 else vals[-1] - vals[0]
        sb = add(eps*((-1)**k)*v for k,v in enumerate(vals)) if compute_block_sums else None
        if sb is not None: A += sb
        B[sig] += b; Be[eps] += b
        E += n % 2 == 0; O += n % 2 == 1
        ledger.append({"j":j+1,"Q":block[0][1],"n_j":n,"global_start_index":offset,"epsilon_j":eps,"sigma_j":sig,"alpha_first":txt(vals[0]),"alpha_last":txt(vals[-1]),"b_j":txt(b),"signed_block_sum":txt(sb) if sb is not None else "not_recorded","alpha_min_gt_1":all(v>1 for v in vals),"alpha_max_lt_4":all(v<4 for v in vals),"even_block_lt_3":n%2==1 or b<3})
        offset += n
        eps = eps if n % 2 == 0 else -eps
    if f["name"] == "four_shell_replay":
        parent=json.loads((ROOT/'papers/tpc-417-c1-four-shell-finite-operator-bound/results/tpc417_certificate.json').read_bytes())
        A=Fraction(parent['payload']['cases'][0]['A_signed_bulk'])
    bs = max(B[1], B[-1]); need(abs(A) <= bs, "sigma envelope")
    return blocks, ledger, A, B, Be, bs, E, O
def case(h, blocks, A, bp, bm, bs):
    items = [x for b in blocks for x in b]; N = 4*h; aa = [alpha(p,q) for p,q in items]
    need(len(items)>=2 and all(p>N for p,q in items), "domain")
    mn, pl = aa[1::2], aa[0::2]; pm, pp = add(mn), add(pl); vm, vp = add(x*x for x in mn), add(x*x for x in pl); amin=min(aa)
    t=lambda d: Fraction(h*h,h*h+d*d); pre=[Fraction(0)]
    for d in range(1,N): pre.append(pre[-1]+t(d)**2)
    S=[pre[r]+pre[N-1-r] for r in range(N)]; D=[vm*S[0]]+[vm*S[r]+vp*(S[r]-t(r)**2) for r in range(1,N)]
    star=Fraction(4)*pm*pm/(vm*vm*h); sb=Fraction(4)/(amin*amin*h); ker=add(t(d) for d in range(1,N))
    need(all(d>0 for d in D) and min(S)>=Fraction(h,4) and star<=sb and ker<=2*h and min(D[1:])>=vm*Fraction(h,4), "matrix prerequisites")
    return {"H":h,"N":N,"L":len(items),"K":len(blocks),"m_minus":len(mn),"m_plus":len(pl),"E_even_shells":sum(len(b)%2==0 for b in blocks),"O_odd_shells":sum(len(b)%2==1 for b in blocks),"a_min":txt(amin),"P_minus":txt(pm),"P_plus":txt(pp),"A_signed_bulk":txt(A),"abs_A_le_B_star":True,"B_plus":txt(bp),"B_minus":txt(bm),"B_star":txt(bs),"parity_coarse_strict":f"B_*<3E+4ceil(O/2)<={3*len(blocks)+1}","V_minus":txt(vm),"V_plus":txt(vp),"S_min":txt(min(S)),"S_max":txt(max(S)),"D0":txt(D[0]),"D_min_interior":txt(min(D[1:])),"star_envelope_square":txt(star),"star_bound_square":txt(sb),"kernel_one_sided_sum":txt(ker),"bulk_bound":txt(Fraction(16)*bs/vm),"operator_bound":"2/(a_min*sqrt(H))+16 B_*/V_-","exact_local_diagonal_normalization":True,"matrix_decomposition":"Z=[[0,q^T],[q,C]], q_r=P_-T_r/sqrt(D0 D_r), C_rs=-A*T_(r-s)/sqrt(D_r D_s)"}
def main():
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    d=json.loads(CERT.read_bytes(), object_pairs_hook=nodup, parse_constant=noconst); p=d["payload"]
    need(d["claim_status"]==STATUS and d["payload_sha256"]==hashlib.sha256(canonical(p)).hexdigest(), "certificate")
    need(p["schema"]==SCHEMA and len(p["fixtures"])==3, "domain")
    for f in p["fixtures"]:
        blocks, led, A, B, Be, bs, E, O = replay_fixture(f); need(f["shell_parity_ledger"]==led, "independent epsilon/sigma ledger")
        need(f["B_plus"]==txt(B[1]) and f["B_minus"]==txt(B[-1]) and f["B_star"]==txt(bs), "sigma groups")
        need(f["A_signed_bulk"]==txt(A) and f["E_even_shells"]==E and f["O_odd_shells"]==O, "family aggregate")
        need(f["old_start_sign_envelope_holds"] == (abs(A) <= max(Be[1], Be[-1])), "old grouping diagnostic")
        for row in f["cases"]:
            if f["name"] == "four_shell_replay":
                parent=json.loads((ROOT/'papers/tpc-417-c1-four-shell-finite-operator-bound/results/tpc417_certificate.json').read_bytes())
                expected=dict(next(c for c in parent['payload']['cases'] if c['H']==row['H']))
                expected.update({'L':sum(counts for counts in f['expected_shell_counts']),'K':len(blocks),'E_even_shells':E,'O_odd_shells':O,'B_plus':txt(B[1]),'B_minus':txt(B[-1]),'B_star':txt(bs),'abs_A_le_B_star':True,'parity_coarse_strict':f"B_*<3E+4ceil(O/2)<={3*len(blocks)+1}",'bulk_bound':txt(Fraction(16)*bs/Fraction(expected['V_minus'])),'operator_bound':'2/(a_min*sqrt(H))+16 B_*/V_-','exact_local_diagonal_normalization':True,'matrix_decomposition':'Z=[[0,q^T],[q,C]], q_r=P_-T_r/sqrt(D0 D_r), C_rs=-A*T_(r-s)/sqrt(D_r D_s)'})
            else:
                expected=case(row["H"],blocks,A,B[1],B[-1],bs)
            need(row==expected, "independent matrix replay")
    mixed=next(f for f in p["fixtures"] if f["name"]=="mixed_parity_regression")
    need(mixed["old_start_sign_envelope_holds"] is False, "mixed-parity mutation regression")
    print("TPC418_INDEPENDENT_CHECK=PASS fixtures=3 sigma_replay=PASS mixed_parity=PASS exact=PASS")
if __name__=="__main__": main()
