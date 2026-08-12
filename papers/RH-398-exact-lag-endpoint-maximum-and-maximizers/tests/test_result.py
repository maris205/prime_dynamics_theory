"""Adversarial tests for the frozen RH-398 result payload."""
from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import build_result as result  # noqa: E402

def require(value: object, message: str) -> None:
    if value is not True: raise RuntimeError(message)

def test_payload_and_file_literal_seals() -> None:
    value = result.build_payload()
    require(value["all_pass"] is True, "baseline failed")
    require(result.validate_result_payload(value, compare_fresh=True) is True, "validator rejected baseline")
    raw=result.canonical_bytes(value); pretty=result.pretty_json_bytes(value)
    require((len(raw),sha256(raw).hexdigest())==(116612,"82698f0b7720ac3efcb589c38a9bf8b7b7c285637cab54c7389bd9343925178d"),"canonical seal drift")
    require((len(pretty),sha256(pretty).hexdigest())==(187434,"b22bd32fd515cbe98ee1fc946cef7e695273fdffd002cb5e29281ceba7e263f7"),"pretty seal drift")
    loaded=result.loads_strict((ROOT/"results/result.json").read_text())
    require(result.exact_equal(loaded,value),"stored result drift")

def test_frozen_identities_and_closed_theorems() -> None:
    v=result.build_payload(); ids=v["identities"]; th=v["theorem_contracts"]
    scope=th["scope_and_order"]; product=th["product_second_difference_telescope"]
    require(ids["core_file"]=={"bytes":61751,"sha256":"ce728df064b2538e49a1f47de5db0ee7e6eabee3d99283be5dc3eb3c122df9da"},"core identity")
    require(ids["certificate"]["mutations"]==66 and ids["certificate"]["rows"]==72,"certificate identity")
    require(ids["source_closure"]["git"]==184 and ids["source_closure"]["remote"]==4 and ids["source_closure"]["logical"]==188,"closure counts")
    require(v["declarations"]["remote_redistributable_in_release"]==[False,False,True,False],"rights")
    require((scope["h_domain"],scope["q_domain"],scope["residue_domain"])==("h in Z_{>=1}","q in Z_{>=1}","r in Z/qZ"),"integer domains")
    require(scope["clock"]=="omega is admissible: 1<=omega(X)<=X and omega(X)->infinity","clock")
    require(scope["fixed_data"]=="h,q,F,omega are fixed before X->infinity","fixed data")
    require(scope["centered_output"]=="epsilon_F(n)=F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))","centered output")
    require(scope["terminal_functional"]=="L_(h,q,X)(F)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)epsilon_F(n)/n","terminal functional")
    require(scope["limit"]=="L_(h,q)(F)=lim_(X->infinity)L_(h,q,X)(F), with the same value for every admissible omega","limit")
    require(scope["capacity"]=="C_h(q)=max_(universally distance-d safe fixed q-phase F)|L_(h,q)(F)| after every fixed-table terminal-log limit","capacity")
    require((product["d"],product["p0"])==("d=2h","p0=min prime p with p not dividing d"),"d and p0")
    require(product["A_m"]=="A_m=prod_p(1-min(m,t_p)/p^2)","A product")
    require(th["maximum_and_maximizers"]["exact_set"]=="{h>=1:mu^2(h)=1 and gcd(h,210)=1}","maximizers")
    require(th["complement_and_gap"]["attained"] is False,"complement nonattainment")
    require(th["joint_and_retained_endpoints"]["retained_infimum"]=="inf_(h>=1)B_infinity(h)=3/pi^2","infimum")
    require(th["source_and_claim_ceiling"]["RH396_locator"]=="definitions equations (18)-(21), Theorem 1.3 equation (22), and Corollary 1.4 equation (23), PDF page 3","RH396 locator")
    require(v["declarations"]["outer_theorem_contract_closed"] is True,"outer contract")
    require(v["summary"]["result_mutations"]==44==len(result.RESULT_MUTATION_NAMES),"result mutation count")

def test_every_new_outer_contract_leaf_has_a_named_mutation() -> None:
    required={"h_domain","q_domain","r_domain","alphabet","phase_table","mobius_extension","omega","fixed_data","centered_output","terminal_functional","safety","limit","capacity","d_to_h","p0","RH396_locator","outer_contract","result_mutation_count"}
    require(required <= set(result.RESULT_MUTATION_NAMES),"missing outer-contract mutation")
    base=result.build_payload()
    for name in sorted(required):
        changed=result.mutate_result(base,name)
        require(result.exact_equal(changed,base) is False,f"outer mutation did not change: {name}")
        require(result.validate_result_payload(changed,compare_fresh=False) is False,f"outer mutation escaped: {name}")

def test_every_result_mutation_hits_real_leaf_and_is_rejected() -> None:
    base=result.build_payload(); digests=set()
    for name in result.RESULT_MUTATION_NAMES:
        changed=result.mutate_result(base,name)
        require(result.exact_equal(changed,base) is False,f"mutation did not change: {name}")
        digest=sha256(result.canonical_bytes(changed)).hexdigest()
        require(digest not in digests,f"duplicate mutation: {name}"); digests.add(digest)
        require(result.validate_result_payload(changed) is False,f"mutation escaped: {name}")

def test_recursive_exact_json_types_topology_and_parser_attacks() -> None:
    base=result.build_payload(); attacks=[]
    x=deepcopy(base); x["schema_version"]=1.0; attacks.append(x)
    x=deepcopy(base); x["schema_version"]=True; attacks.append(x)
    x={key:base[key] for key in reversed(tuple(base))}; attacks.append(x)
    x=deepcopy(base); x["summary"]["certificate_rows"]=72.0; attacks.append(x)
    x=deepcopy(base); x["certificate"]["rows"][0]["data"]["extra"]=0; attacks.append(x)
    for attack in attacks: require(result.validate_result_payload(attack) is False,"type/topology attack escaped")
    for text in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'):
        try: result.loads_strict(text)
        except ValueError: pass
        else: raise RuntimeError("strict parser attack escaped")

def test_false_validator_survives_builder_helper_and_global_rebinding() -> None:
    base=result.build_payload(); saved={}
    def bomb(*_a: object,**_k: object)->object: raise RuntimeError("forbidden rebound helper called")
    names=("build_payload","build_certificate","build_source_closure","mutate_certificate","verify_certificate","canonical_bytes","pretty_json_bytes","exact_equal","loads_strict")
    try:
        for name in names: saved[name]=getattr(result,name); setattr(result,name,bomb)
        require(result.validate_result_payload(base,compare_fresh=False) is True,"false validator used rebound helper")
    finally:
        for name,value in saved.items(): setattr(result,name,value)

def test_false_validator_survives_coordinated_constant_rebinding() -> None:
    base=result.build_payload(); old=(result.PAPER,result.TITLE,result.ALL_GIT_SHA,result.LOGICAL_SHA,result.THEOREM_CONTRACTS)
    try:
        result.PAPER="RH-999"; result.TITLE="drift"; result.ALL_GIT_SHA="0"*64; result.LOGICAL_SHA="1"*64; result.THEOREM_CONTRACTS={}
        require(result.validate_result_payload(base) is True,"false validator read rebound constants")
        changed=deepcopy(base); changed["paper"]="RH-999"
        require(result.validate_result_payload(changed) is False,"coordinated drift escaped")
    finally:
        result.PAPER,result.TITLE,result.ALL_GIT_SHA,result.LOGICAL_SHA,result.THEOREM_CONTRACTS=old

def test_validator_factory_is_pinned_and_assert_optimization_safe() -> None:
    source=(ROOT/"experiments/build_result.py").read_text(); tree=ast.parse(source)
    asserts=[node for node in ast.walk(tree) if isinstance(node,ast.Assert)]
    require(asserts==[],"builder contains assert")
    base=result.build_payload(); original=result.build_payload
    try:
        result.build_payload=lambda:{"all_pass":True}
        require(result.validate_result_payload(base) is True,"validator not pinned")
        require(result.validate_result_payload({"all_pass":True}) is False,"rebound builder attack escaped")
    finally: result.build_payload=original
    tuple_payload=deepcopy(base)
    tuple_payload["theorem_contracts"]["scope_and_order"]["order"]=tuple(
        tuple_payload["theorem_contracts"]["scope_and_order"]["order"]
    )
    def tuple_builder() -> dict[str, object]:
        return deepcopy(tuple_payload)
    try:
        result._make_result_validator(tuple_builder)
    except RuntimeError as error:
        require("non-exact JSON type" in str(error),"wrong tuple-factory error")
    else:
        raise RuntimeError("tuple-producing result factory escaped")

def test_compare_fresh_exact_bool_and_missing_extra_rejected() -> None:
    base=result.build_payload()
    for bad in (0,1,None,1.0):
        try: result.validate_result_payload(base,compare_fresh=bad)
        except TypeError: pass
        else: raise RuntimeError("compare_fresh accepted non-bool")
    missing=deepcopy(base); missing.pop("summary")
    extra=deepcopy(base); extra["extra"]=0
    require(result.validate_result_payload(missing) is False and result.validate_result_payload(extra) is False,"key attack escaped")
