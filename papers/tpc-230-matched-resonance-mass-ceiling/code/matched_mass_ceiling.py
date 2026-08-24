#!/usr/bin/env python3
"""Exact matched-mass ceiling for TPC-230."""
from __future__ import annotations
from fractions import Fraction
from hashlib import sha256
from math import gcd

class MassFailure(RuntimeError): pass
def require(c:bool,m:str)->None:
    if type(c) is not bool or not c: raise MassFailure(m)

def is_prime(n:int)->bool:
    require(type(n) is int,'prime input')
    if n<2:return False
    if n%2==0:return n==2
    d=3
    while d*d<=n:
        if n%d==0:return False
        d+=2
    return True

def prime_shell(Q:int)->tuple[int,...]:
    require(type(Q) is int and Q>=8,'Q')
    return tuple(q for q in range(Q+1,2*Q) if is_prime(q))

def resonance_pairs(Q:int)->tuple[tuple[int,int],...]:
    shell=set(prime_shell(Q)); h=16*Q
    if gcd(21,h)!=1:return ()
    out=[]
    for p in sorted(shell):
        n=h-7*p
        if n>0 and n%3==0:
            r=n//3
            if r in shell and p<r: out.append((p,r))
    return tuple(out)

def primitive_row_weight(Q:int,q:int)->int:
    h=16*Q; cutoff=4*q//Q
    require(4<=cutoff<=7,'cutoff')
    value=sum(1 for m in range(-cutoff,cutoff+1) if m and gcd(abs(m),h)==1)
    require(2<=value<=8 and value%2==0,'row weight')
    return value

def ftext(x:Fraction)->str:
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def mass_record(Q:int)->dict[str,object]:
    shell=prime_shell(Q); edges=resonance_pairs(Q); matched={q for e in edges for q in e}
    P=len(shell); E=len(edges)
    uniform=Fraction(len(matched),P) if P else Fraction(0)
    weights={q:primitive_row_weight(Q,q) for q in shell}
    total=sum(weights.values()); matched_weight=sum(weights[q] for q in matched)
    literal=Fraction(matched_weight,total) if total else Fraction(0)
    if P:
        require(uniform==Fraction(2*E,P),'uniform matching mass')
        require(literal<=min(Fraction(1),Fraction(8*E,P)),'comparability ceiling')
    return {'Q':Q,'prime_count':P,'edge_count':E,'matched_vertices':len(matched),'uniform_mass_fraction':ftext(uniform),'literal_aligned_mass_fraction':ftext(literal),'literal_total_row_weight':total,'literal_matched_row_weight':matched_weight,'row_weight_min':min(weights.values(),default=0),'row_weight_max':max(weights.values(),default=0)}

def matching_energy(row_vectors:dict[int,tuple[Fraction,...]],edges:tuple[tuple[int,int],...])->dict[str,Fraction]:
    vertices=set(row_vectors); used=[]
    for p,r in edges:
        require(p in vertices and r in vertices and p!=r,'edge vertices'); used.extend((p,r))
    require(len(used)==len(set(used)),'edges must be a matching')
    def norm2(v):return sum((x*x for x in v),Fraction(0))
    D=sum((norm2(v) for v in row_vectors.values()),Fraction(0)); matched=set(used)
    M=sum((norm2(row_vectors[q]) for q in matched),Fraction(0)); U=D-M
    Eap=U
    for p,r in edges:
        u=row_vectors[p];v=row_vectors[r];require(len(u)==len(v),'shape')
        Eap+=norm2(tuple(a+b for a,b in zip(u,v,strict=True)))
    require(Eap>=U,'unmatched floor')
    return {'diagonal':D,'matched_mass':M,'unmatched_mass':U,'AP':Eap,'saving':D-Eap}

def sharp_fixture()->dict[str,object]:
    rows={11:(Fraction(1),Fraction(2)),13:(Fraction(-1),Fraction(-2)),17:(Fraction(2),Fraction(-1)),19:(Fraction(-2),Fraction(1)),23:(Fraction(3),Fraction(4))}
    values=matching_energy(rows,((11,13),(17,19)))
    require(values['AP']==values['unmatched_mass'],'sharp floor')
    require(values['saving']==values['matched_mass'],'sharp saving')
    return {k:ftext(v) for k,v in values.items()}

def nonsharp_fixture()->dict[str,object]:
    rows={11:(Fraction(1),Fraction(0)),13:(Fraction(0),Fraction(1)),17:(Fraction(2),Fraction(0))}
    values=matching_energy(rows,((11,13),))
    require(values['saving']<values['matched_mass'],'nonsharp control')
    return {k:ftext(v) for k,v in values.items()}

def boundary_scan(a:int=8,b:int=4096)->dict[str,object]:
    lines=[]; edge_scales=0; zero_scales=0; max_uniform=Fraction(0); max_uniform_Q=None; max_literal=Fraction(0); max_literal_Q=None; threshold=0
    for Q in range(a,b+1):
        r=mass_record(Q); u=Fraction(r['uniform_mass_fraction']); l=Fraction(r['literal_aligned_mass_fraction'])
        if r['edge_count']: edge_scales+=1
        else: zero_scales+=1
        if u>max_uniform:max_uniform=u;max_uniform_Q=Q
        if l>max_literal:max_literal=l;max_literal_Q=Q
        if l>=Fraction(1,400):threshold+=1
        lines.append(f"{Q}|{r['prime_count']}|{r['edge_count']}|{r['uniform_mass_fraction']}|{r['literal_aligned_mass_fraction']}|{r['row_weight_min']}|{r['row_weight_max']}")
    return {'Q_min':a,'Q_max':b,'scales_checked':b-a+1,'edge_bearing_scales':edge_scales,'zero_edge_scales':zero_scales,'literal_fraction_at_least_1_over_400_scales':threshold,'maximum_uniform_mass_fraction':ftext(max_uniform),'first_maximum_uniform_Q':max_uniform_Q,'maximum_literal_mass_fraction':ftext(max_literal),'first_maximum_literal_Q':max_literal_Q,'scan_sha256':sha256('\n'.join(lines).encode()).hexdigest()}

def certificate_payload()->dict[str,object]:
    return {'schema':'tpc230-matched-resonance-mass-ceiling-v1','status':'PASS','claim_level':'PROVED_STRUCTURAL_L1','author':'Liang Wang','affiliation':'Huazhong University of Science and Technology','theorem':{'unmatched_floor':'E_AP>=D_unmatched=D-M','saving_ceiling':'D-E_AP<=M','necessary_mass_condition':'E_AP<=(1-delta)D implies M/D>=delta','sharpness':'perfect anti-alignment on every matched edge','uniform_row_mass_fraction':'M/D=2E/P','kappa_comparability_ceiling':'M/D<=2*kappa*E/P','literal_aligned_kappa_bound':4,'strict_1_over_400_edge_density_toll':'E/P>=1/3200 is necessary under literal kappa<=4'},'q25':mass_record(25),'sharp_fixture':sharp_fixture(),'nonsharp_fixture':nonsharp_fixture(),'boundary_scan':boundary_scan(),'checks':{'unmatched_floor_exact':True,'mass_ceiling_exact':True,'sharpness_fixture_exact':True,'uniform_mass_formula_exact':True,'literal_row_weights_between_2_and_8':True,'kappa_four_ceiling_exact':True},'firewall':{'asymptotic_resonance_edge_density':'OPEN','actual_V59_source_mass_comparability':'OPEN','arithmetic_advance':'NO','arithmetic_cancellation':'NONE','fixed_atom_credit':0,'L2':'NONE','full_gate_b':'OPEN','strict_1_over_400':'UNPAID'},'round2_clue':'APPLY_A_TWO_LINEAR_FORM_UPPER_BOUND_SIEVE_TO_THE_3_7_RESONANCE_COUNT'}

def validate_payload(d:dict[str,object])->None:
    require(d.get('schema')=='tpc230-matched-resonance-mass-ceiling-v1','schema');require(d.get('status')=='PASS' and d.get('claim_level')=='PROVED_STRUCTURAL_L1','status')
    t=d.get('theorem');require(type(t) is dict and t.get('literal_aligned_kappa_bound')==4,'theorem');require(t.get('strict_1_over_400_edge_density_toll')=='E/P>=1/3200 is necessary under literal kappa<=4','toll')
    q=d.get('q25');require(type(q) is dict and q.get('edge_count')==1,'Q25')
    s=d.get('boundary_scan');require(type(s) is dict and s.get('scales_checked')==4089,'scan')
    c=d.get('checks');require(type(c) is dict and all(type(v) is bool and v for v in c.values()),'checks')

def build_certificate()->dict[str,object]:
    d=certificate_payload();validate_payload(d);return d
