#!/usr/bin/env python3
from __future__ import annotations
import argparse, cmath, copy, hashlib, json, math
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PAYLOAD=HERE/"tpc195_block_prefix_power_profile_equivalence.json"
AUDIT=HERE/"tpc195_block_prefix_power_profile_equivalence_audit.json"
SCHEMA=HERE.parent/"schemas"/"tpc195-block-prefix-power-profile-equivalence-v1.schema.json"
AUDIT_SCHEMA=HERE.parent/"schemas"/"tpc195-block-prefix-power-profile-equivalence-audit-v1.schema.json"
EXPECTED_SHA="d90642b85e34218fd0e208b0f5638b6b8f3a10797352bb8b78f276bd449f5615"
EXPECTED_AUDIT_SHA="9671bd1ade4df68d9d533ac2a4a69740c7691ef45a27eb02e0c51202d238c5fa"
EXPECTED_SCHEMA_SHA="229ccd4aa52e95daa57f867a743152de868456c30d90a7027ae9bf52a5134e63"
EXPECTED_AUDIT_SCHEMA_SHA="e93c5de9796357d450d6693ebe5bf78228655729d7dfa8da551a1e100e16d176"
MUTATIONS=['promote_L2', 'promote_fixed_atom_decay', 'grant_endpoint_credit', 'mark_strict_budget_paid', 'stop_bad_endpoint_parent', 'stop_global_architecture', 'promote_hash_to_theorem', 'change_verdict', 'delete_first_missing', 'inject_extra_field']
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def text_hash(path):
    text=path.read_text(encoding="utf-8").replace("\r\n","\n").replace("\r","\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
def accepts(s,v):
    if "const" in s: return type(v) is type(s["const"]) and v==s["const"]
    if s.get("type")=="object":
        return isinstance(v,dict) and set(v)==set(s["required"]) and all(accepts(s["properties"][k],v[k]) for k in s["required"])
    if s.get("type")=="array":
        return isinstance(v,list) and len(v)==s["minItems"] and all(accepts(a,b) for a,b in zip(s["prefixItems"],v))
    return False
def mutated(p,name):
    x=copy.deepcopy(p)
    if name=="promote_L2": x["progress"]["L2"]="POSITIVE"
    elif name=="promote_fixed_atom_decay": x["fixed_atom_decay_obtained"]=True
    elif name=="grant_endpoint_credit": x["endpoint_ledger"]["named_atom_sigma_credit"]={"numerator":1,"denominator":400}
    elif name=="mark_strict_budget_paid": x["endpoint_ledger"]["state"]="PAID"
    elif name=="stop_bad_endpoint_parent": x["route_state"]["bad_endpoint_O161_parent"]="STOPPED"
    elif name=="stop_global_architecture": x["route_state"]["global_architecture"]="STOPPED"
    elif name=="promote_hash_to_theorem": x["source_locks"][0]["hash_semantics"]="THEOREM_EVIDENCE"
    elif name=="change_verdict": x["verdict"]="PROMOTED"
    elif name=="delete_first_missing":
        if "first_missing_literal_theorem" in x: del x["first_missing_literal_theorem"]
        else: del x["first_missing_nodes"]["direct_production"]
    elif name=="inject_extra_field": x["schema_exploit"]=True
    return x
def mobius(n):
    if n==1:return 1
    value=n; primes=0; p=2
    while p*p<=value:
        if value%p==0:
            value//=p
            if value%p==0:return 0
            primes+=1
            while value%p==0:value//=p
        p+=1
    if value>1:primes+=1
    return -1 if primes%2 else 1
def rs(level):
    p=[1];q=[1]
    for _ in range(level):p,q=p+q,p+[-x for x in q]
    return p,q
def finite(p):
    n=p["paper"];c=p["finite_certificate"]
    if n==194:
        f=c["affine_fixture"]; assert f["s"]*f["u"]-f["a"]*f["d"]==2
        assert len({x["id"] for x in c["formula_type_registry"]})==3
        assert len({x["domain"] for x in c["formula_type_registry"]})==3
        assert c["resolved_packet_formula"]["phase_slope"]=="Omega_xi=ell_theta*v_theta*sigma_theta*B_theta_b"
        assert "mfrak_K_X(r)" in c["resolved_packet_formula"]["outer_multiplier"]
        assert c["resolved_packet_formula"]["complete_per_key_contribution"]=="P_xi_X_le_T=cfrak_xi_X*S_xi_X_le_T"
        return {"determinant":2,"distinct_formula_types":3,"literal_formula_fields_verified":9}
    elif n==195:
        t=c["dyadic_fixture_T"]; seen=[];hi=t
        while hi>1:lo=hi//2;seen.extend(range(lo+1,hi+1));hi=lo
        seen.append(1);assert sorted(seen)==list(range(1,t+1))
        assert 19>10+1 and 19<2*10
        assert c["truncated_tail_raw_strict_bound"]=="2*B*M"
        sigma=Fraction(c["sigma_fixture"]["numerator"],c["sigma_fixture"]["denominator"])
        return {"dyadic_partition_exact":True,"forward_constant":round(1/(2**(1-float(sigma))-1),12),"reverse_constant":round(2**(1-float(sigma))+1,12),"truncated_tail_counterexample_to_M_plus_1":{"M":10,"T":19,"old_bound_terms":11,"possible_tail_terms":19,"new_strict_bound_terms":20}}
    elif n==196:
        f=c["fixture"];co=[(-1)**(z*z+3*z) for z in range(20)]
        direct=sum(co[z]*cmath.exp(-2j*math.pi*f["r"]*z/f["R"]) for z in range(20))
        split=sum(cmath.exp(-2j*math.pi*f["r"]*b/f["R"])*sum(co[z] for z in range(b,20,f["R"])) for b in range(f["R"]))
        assert abs(direct-split)<1e-10 and f["residue_determinant"]==10
        return {"residue_identity_error":abs(direct-split),"determinant":10}
    elif n==197:
        f=Fraction(c["fixed_atom_fixture"]["numerator"],c["fixed_atom_fixture"]["denominator"])
        matches=[q for q in c["prime_conductors"] if q==f.denominator]
        assert matches==[5]
        assert len(c["conductor_one_native_requirements"])==5
        return {"reduced_denominator":f.denominator,"matches":matches}
    elif n==198:
        pp,qq=rs(c["rudin_shapiro_level"]);L=len(pp)
        max_p=0.0;max_error=0.0
        for j in range(257):
            z=cmath.exp(2j*math.pi*j/257);pv=sum(a*z**k for k,a in enumerate(pp));qv=sum(a*z**k for k,a in enumerate(qq))
            max_p=max(max_p,abs(pv));max_error=max(max_error,abs(abs(pv)**2+abs(qv)**2-2*L))
            assert max_error<1e-8
        assert sum(a*a for a in pp)==L
        return {"length":L,"sampled_sup":round(max_p,12),"energy_error":max_error,"product_resonance":L}
    elif n==199:
        cc=lambda k:mobius(k)*mobius(k+2)
        assert (cc(3),cc(5),cc(15))==(1,1,-1) and math.gcd(3,5)==1
        return {"pair_values":{"3":1,"5":1,"15":-1},"multiplicative":False}
    elif n==200:
        zeros=[{"q":q,"h":h,"pair":"L2,L3"} for q in range(1,20,2) for h in range(1,21) if q*h-2==0]
        assert zeros==c["enumeration"]["zero_cells"]
        forms=[1+7,3+7,1+(7+2),3+(7+2)];assert forms[1]==forms[2]
        return {"zero_cells":zeros,"coincident_value":forms[1]}
    elif n==201:
        assert c["normalized_diagonal_coefficient"]+c["degenerate_shift_added_coefficient"]==6
        assert c["native_domain"]==["V>0","3<=H<=N"] and c["positive_part_split"]=="(x+y)_+<=|x|+y_+"
        return {"absorbed_coefficient":6,"remaining_gate_nonempty":True}
    elif n==202:
        row_average=1/c["selector_fixture"]["columns"];column_average=1/c["selector_fixture"]["rows"]
        assert max(row_average,column_average)<=1/64 and c["selector_fixture"]["prescribed_value"]==1
        assert c["new_stop_scoped_cell_created"] is False
        rr=p["external_primary_source"]["native_theorem_records"]
        assert rr[0]["range"]=="X>=h>=10" and "(1/X)" in rr[0]["lhs"] and "(1/h)" in rr[0]["lhs"]
        assert rr[1]["range"]=="natural k>=2 and X>=H>=10" and "(1/H^(k-1))" in rr[1]["lhs"] and rr[1]["rhs"].startswith("k*(")
        return {"row_average":row_average,"column_average":column_average,"prescribed_cell":1,"native_theorem_records_verified":2}
    elif n==203:
        locks={x["source_id"]:x for x in p["source_locks"]}
        seen_stops=set()
        for ns,v in c["expected_verdicts"].items():
            u=json.loads((REPO/locks[f"TPC{ns}.payload"]["path"]).read_text(encoding="utf-8"))
            assert u["verdict"]==v and u["progress"]["L2"]=="NONE"
            assert u["route_state"]["bad_endpoint_O161_parent"]=="OPEN"
            assert u["route_state"]["direct_twist_O161_parent"]=="OPEN"
            for cell in u["stop_scoped"]: seen_stops.add(cell["cell"])
        assert p["first_missing_nodes"]=={"global":"H1.source_backed_local_occurrence_edge_family","selected_pointwise":"LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION","direct_production":"SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"}
        assert p["batch_stop"]=={"state":"USER_CONFIRMATION_REQUIRED","next_paper":None,"tpc204_authorized":False}
        assert [x["route"] for x in c["exact_reopen_triggers"]]==["DIRECT","METRIC","BAD_ENDPOINT","STRUCTURAL","DECLARED_CORPUS"]
        assert "schedule-specific exceptional-limsup avoidance theorem" in c["exact_reopen_triggers"][1]["requires"]
        return {"upstreams_verified":len(c["expected_verdicts"]),"new_scoped_cells":len(seen_stops)}
    else:raise AssertionError(n)
def validate(p,a,s,a_s):
    assert hashlib.sha256(canonical(p).encode()).hexdigest()==EXPECTED_SHA==a["payload_canonical_sha256"]
    assert hashlib.sha256(canonical(a).encode()).hexdigest()==EXPECTED_AUDIT_SHA
    assert hashlib.sha256(canonical(s).encode()).hexdigest()==EXPECTED_SCHEMA_SHA
    assert hashlib.sha256(canonical(a_s).encode()).hexdigest()==EXPECTED_AUDIT_SCHEMA_SHA
    assert accepts(s,p)
    assert accepts(a_s,a)
    assert p["fixed_atom_decay_obtained"] is False and p["progress"]["L2"]=="NONE"
    assert p["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0
    assert p["endpoint_ledger"]["state"]=="UNPAID"
    assert p["route_state"]["bad_endpoint_O161_parent"]=="OPEN"
    assert p["route_state"]["direct_twist_O161_parent"]=="OPEN"
    assert p["route_state"]["global_architecture"]=="OPEN"
    assert all(v is False for v in p["claim_boundary"].values())
    for lock in p["source_locks"]:
        assert text_hash(REPO/lock["path"])==lock["canonical_utf8_lf_sha256"]
        assert lock["hash_semantics"]=="INTEGRITY_ONLY"
    assert finite(p)==a["finite_check_result"]
    outcomes=[{"name":name,"rejected":not accepts(s,mutated(p,name))} for name in MUTATIONS]
    assert outcomes==a["mutation_registry"] and all(x["rejected"] for x in outcomes)
    assert all(a["checks"].values()) and a["all_checks_pass"] is True
def main():
    if not __debug__: raise RuntimeError("optimized Python disables assertions; validation fails closed")
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ns=ap.parse_args()
    p=json.loads(PAYLOAD.read_text(encoding="utf-8"));a=json.loads(AUDIT.read_text(encoding="utf-8"));s=json.loads(SCHEMA.read_text(encoding="utf-8"));a_s=json.loads(AUDIT_SCHEMA.read_text(encoding="utf-8"))
    validate(p,a,s,a_s)
    if ns.check:
        assert PAYLOAD.read_text(encoding="utf-8")==canonical(p)
        assert AUDIT.read_text(encoding="utf-8")==canonical(a)
        assert SCHEMA.read_text(encoding="utf-8")==canonical(s)
        assert AUDIT_SCHEMA.read_text(encoding="utf-8")==canonical(a_s)
    print(json.dumps({"paper":p["paper"],"verdict":p["verdict"],"finite":True,"mutations":len(MUTATIONS),"check":ns.check},sort_keys=True))
if __name__=="__main__":main()
