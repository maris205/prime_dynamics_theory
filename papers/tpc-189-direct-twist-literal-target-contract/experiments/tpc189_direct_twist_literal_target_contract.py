#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PAYLOAD=HERE/"tpc189_direct_twist_literal_target_contract.json"
AUDIT=HERE/"tpc189_direct_twist_literal_target_contract_audit.json"
PAYLOAD_SCHEMA=HERE.parent/"schemas"/"tpc189-direct-twist-literal-target-contract-v1.schema.json"
AUDIT_SCHEMA=HERE.parent/"schemas"/"tpc189-direct-twist-literal-target-contract-audit-v1.schema.json"
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def schema_accepts(schema, value):
    if "anyOf" in schema:
        return any(schema_accepts(option, value) for option in schema["anyOf"])
    kind=schema.get("type")
    if kind is not None:
        if kind=="integer":
            valid=type(value) is int
        elif kind=="number":
            valid=type(value) in (int,float)
        else:
            valid=type(value) is {
                "object":dict,"array":list,"null":type(None),
                "boolean":bool,"string":str,
            }.get(kind)
        if not valid:
            return False
    if "const" in schema and not (
        type(value) is type(schema["const"]) and value==schema["const"]
    ):
        return False
    if "enum" in schema and not any(
        type(value) is type(option) and value==option for option in schema["enum"]
    ):
        return False
    if kind=="object":
        properties=schema.get("properties",{})
        required=schema.get("required",[])
        if type(properties) is not dict or type(required) is not list:
            return False
        if not set(required).issubset(value):
            return False
        if schema.get("additionalProperties") is False and not set(value).issubset(properties):
            return False
        return all(
            key not in properties or schema_accepts(properties[key], child)
            for key,child in value.items()
        )
    if kind=="array":
        if "minItems" in schema and len(value)<schema["minItems"]:
            return False
        if "maxItems" in schema and len(value)>schema["maxItems"]:
            return False
        item_schema=schema.get("items")
        return item_schema is None or all(schema_accepts(item_schema, child) for child in value)
    return True

def validate_payload(p):
    payload_schema=json.loads(PAYLOAD_SCHEMA.read_text(encoding="utf-8"))
    require(schema_accepts(payload_schema,p),"PAYLOAD_SCHEMA_REJECTED")
    require(type(p["paper"]) is int and p["paper"]==189,"PAPER")
    require(p["required_quantifier_signature"]["phase_axis"]=="NAMED_FIXED_ATOM","PHASE_AXIS")
    require(p["fixed_atom_decay_obtained"] is False,"FIXED_ATOM_DECAY")
    require(p["progress"]["L2"] is False,"L2")
    require(
        type(p["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]) is int
        and p["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0,
        "ENDPOINT_CREDIT",
    )
    require(p["endpoint_ledger"]["state"]=="UNPAID","ENDPOINT_STATE")
    require(all(v is False for v in p["claim_boundary"].values()),"CLAIM_BOUNDARY")
    for lock in p["source_locks"]:
        source=REPO/lock["path"]
        require(source.is_file(),f"SOURCE_MISSING:{lock['source_id']}")
        require(
            hashlib.sha256(source.read_bytes()).hexdigest()==lock["sha256"],
            f"SOURCE_HASH:{lock['source_id']}",
        )
        require(lock["hash_is_theorem_evidence"] is False,"HASH_IS_THEOREM")
    if p["stop_scoped"] is not None:
        require(p["stop_scoped"]["global_pointwise_route_stopped"] is False,"GLOBAL_ROUTE_STOP")
        require(p["stop_scoped"]["architecture_stopped"] is False,"ARCHITECTURE_STOP")

def mutated_payload(p,name):
    candidate=copy.deepcopy(p)
    if name=="reject_named_atom_promotion":
        candidate["claim_boundary"]["lebesgue_ae_is_named_fixed_atom"]=True
    elif name=="reject_phase_average_promotion":
        candidate["claim_boundary"]["phase_average_is_named_fixed_atom"]=True
    elif name=="reject_fixed_h0_as_decay":
        candidate["claim_boundary"]["fixed_h0_data_is_decay"]=True
    elif name=="reject_scoped_stop_expansion":
        candidate["stop_scoped"]={
            "cell":"FORGED_GLOBAL_STOP",
            "global_pointwise_route_stopped":True,
            "architecture_stopped":True,
        }
    elif name=="reject_L2_promotion":
        candidate["progress"]["L2"]=True
    elif name=="reject_endpoint_credit":
        candidate["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]=1
    elif name=="reject_source_hash_as_theorem":
        candidate["source_locks"][0]["hash_is_theorem_evidence"]=True
    elif name=="reject_extra_field":
        candidate["forged_extra_field"]=True
    else:
        raise ValueError(f"UNKNOWN_MUTATION:{name}")
    return candidate

def validate(p,a):
    audit_schema=json.loads(AUDIT_SCHEMA.read_text(encoding="utf-8"))
    require(schema_accepts(audit_schema,a),"AUDIT_SCHEMA_REJECTED")
    validate_payload(p)
    require(
        a["payload_sha256"]==hashlib.sha256(canonical(p).encode()).hexdigest(),
        "PAYLOAD_SHA256",
    )
    require(a["all_checks_pass"] is True,"AUDIT_STATUS")
    require(len(a["mutation_registry"])==8,"MUTATION_COUNT")
    require(all(x["rejected"] is True for x in a["mutation_registry"]),"MUTATION_LEDGER")
    for row in a["mutation_registry"]:
        rejected=False
        try:
            validate_payload(mutated_payload(p,row["name"]))
        except (KeyError,TypeError,ValueError):
            rejected=True
        require(rejected,f"MUTATION_ACCEPTED:{row['name']}")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ns=ap.parse_args()
    p=json.loads(PAYLOAD.read_text(encoding="utf-8"))
    a=json.loads(AUDIT.read_text(encoding="utf-8"))
    validate(p,a)
    if ns.check:
        require(PAYLOAD.read_text(encoding="utf-8")==canonical(p),"PAYLOAD_NOT_CANONICAL")
        require(AUDIT.read_text(encoding="utf-8")==canonical(a),"AUDIT_NOT_CANONICAL")
    print(json.dumps({"paper":189,"verdict":p["verdict"],"check":ns.check,"mutations":8},sort_keys=True))
if __name__=="__main__": main()
