"""Build and independently validate the frozen RH-398 result artifact."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from lag_endpoint_extrema.core import (  # noqa: E402
    CERTIFICATE_FIXTURE_BYTES, CERTIFICATE_FIXTURE_ROWS,
    CERTIFICATE_FIXTURE_SHA256, MUTATION_NAMES, MUTATION_TARGETS, TITLE,
    build_certificate, mutate_certificate, verify_certificate,
)
from source_locks import build_source_closure  # noqa: E402

PAPER = "RH-398"
CORE_FILE = (61_751, "ce728df064b2538e49a1f47de5db0ee7e6eabee3d99283be5dc3eb3c122df9da")
CORE_TEST = (9_451, "bd2599e3d312088798c128e17f9b7f1dc8904c63f65319c7e46dd30faf603f18")
SOURCE_FILE = (30_176, "65a1a1e4a038c1166b033565bbfd18fb2c3f188593341945dbc83db9a223df6b")
SOURCE_TEST = (21_551, "4bc4db756727ad6b7df819d08b3c402ab9a399e49c0e27dd12cf78d4bb8a9227")
SOURCE_CANONICAL = (64_997, "5cb3a2f4339ba0b2f11654092496bf7caf255d0d0e7ccf23524355d9f3fa97d7")
SOURCE_GROUP_SIZES = {"rh397_immutable_closure": 172, "rh397_standard8": 8, "rh397_prior_external_locks": 4}
SOURCE_GROUP_DIGESTS = {
    "rh397_immutable_closure": "fd2d749a09316b9c412780e61882e5f1ac050af609cd0a96c0d1aea79ac4c82d",
    "rh397_standard8": "eb7355565e8429765cb967192c00e261998147abb68fb0307517695621bdfd62",
    "rh397_prior_external_locks": "e044509ee377c35cea8642b67a75ca5dc4ba861f455228bde7341418791bce20",
}
ALL_GIT_SHA = "e7341caa25f0787a2e48a4d9c156e0d785b6c2a5516172bdfb25c2ac45377ea8"
LOGICAL_SHA = "4cc752fb7baae977bb15a9420101c5ed37727b1f3f7eecf72afce9dec3c73b13"
RIGHTS = [False, False, True, False]

GATES = {name: False for name in (
    "A_intrinsic_determinant", "B_scattering_completion", "C_self_adjoint_generator",
    "D_von_mangoldt_weighted_prime_power_traces", "E_completed_zeta_divisor_equality",
)}
FORBIDDEN = {name: False for name in (
    "growing_h", "h_depending_on_X", "growing_q", "q_depending_on_X",
    "prelimit_maximum", "ordinary_Cesaro_average", "causal_or_online_rule",
    "monotonicity_in_h", "finite_certificate_is_analytic_proof", "network_fetch_required",
    "external_payload_vendored", "operator_model", "zero_model", "proof_of_Riemann_Hypothesis",
)}

THEOREM_CONTRACTS = {
    "scope_and_order": {
        "h_domain": "h in Z_{>=1}",
        "q_domain": "q in Z_{>=1}",
        "residue_domain": "r in Z/qZ",
        "alphabet": "T={-1,0,+1}",
        "phase_table": "F_r:T^3->{-1,+1}",
        "mobius_extension": "mu_0(k)=mu(k) for integer k>=1 and mu_0(k)=0 for k<=0",
        "clock": "omega is admissible: 1<=omega(X)<=X and omega(X)->infinity",
        "centered_output": "epsilon_F(n)=F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))",
        "terminal_functional": "L_(h,q,X)(F)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)epsilon_F(n)/n",
        "safety": "not(F_r(a,b,c)=+1 and F_(r+d)(c,e,f)=+1) for every r in Z/qZ and a,b,c,e,f in T",
        "limit": "L_(h,q)(F)=lim_(X->infinity)L_(h,q,X)(F), with the same value for every admissible omega",
        "capacity": "C_h(q)=max_(universally distance-d safe fixed q-phase F)|L_(h,q)(F)| after every fixed-table terminal-log limit",
        "fixed_data": "h,q,F,omega are fixed before X->infinity",
        "order": ["fix_h_q_F_omega", "X_to_infinity", "finite_safe_table_maximum", "scalar_q_supremum", "fixed_scalar_h_comparison"],
        "fixed_scalar_endpoints_only": True,
        "growing_h_or_q_claim": False,
    },
    "product_second_difference_telescope": {
        "d": "d=2h",
        "p0": "p0=min prime p with p not dividing d",
        "t_p": "t_p(d)=p^2/gcd(d,p^2)",
        "A_m": "A_m=prod_p(1-min(m,t_p)/p^2)",
        "cutoff": "A_m=0 for m>=p0^2",
        "R_l": "R_l=A_l-2A_(l+1)+A_(l+2)",
        "R_nonnegative": True,
        "telescope": "B_infinity(h)=sum_(m=1)^(p0^2-1)(-1)^(m+1)A_m",
        "event": "odd_forward_positive_run_probability",
    },
    "maximum_and_maximizers": {
        "maximum": "max_(h>=1)B_infinity(h)=B_infinity(1)",
        "exact_set": "{h>=1:mu^2(h)=1 and gcd(h,210)=1}",
        "iff": "B_infinity(h)=B_infinity(1) iff mu^2(h)=1 and gcd(h,210)=1",
        "small_prime_product": 210,
    },
    "complement_and_gap": {
        "domain": "h>=1 outside the exact maximizer set",
        "supremum": "B_infinity(1)",
        "attained": False,
        "cofinal_sequence": "h=p^2 for primes p>=11",
        "sequence_bound": "0<B_infinity(1)-B_infinity(p^2)<=1/p^2",
        "p0_ge5_gap": "B_infinity(1)-B_infinity(h)>2/1334025",
        "proved_stronger_chain": "B_infinity(1)-B_infinity(h)>=B_infinity(1)-B_infinity(3)>1/36750>2/1334025",
    },
    "joint_and_retained_endpoints": {
        "finite_pair": "C_h(q)<B_infinity(h)<=B_infinity(1)",
        "joint_supremum": "sup_(h>=1,q finite)C_h(q)=B_infinity(1)",
        "finite_pair_attains": False,
        "retained_infimum": "inf_(h>=1)B_infinity(h)=3/pi^2",
        "infimum_attained": False,
    },
    "source_and_claim_ceiling": {
        "RH396": "sole_load_bearing_theorem_and_analytic_endpoint_input",
        "RH396_locator": "definitions equations (18)-(21), Theorem 1.3 equation (22), and Corollary 1.4 equation (23), PDF page 3",
        "RH397": "direct_release_and_provenance_predecessor_only",
        "certificate": "finite_exact_reproduction_not_analytic_proof",
        "RH_or_Gates_A_E": False,
    },
}
SOURCE_ROLES = {
    "RH396": {"analytic_input": True, "role": "sole_load_bearing_theorem_and_analytic_endpoint_input"},
    "RH397": {"analytic_input": False, "role": "direct_release_and_provenance_predecessor_only"},
    "RH394": {"analytic_input": False, "role": "transitive_three_shift_provenance_only_via_RH396"},
    "external_sources": "inherited_closure_only; no live fetch and no vendored payload",
}

def _reject_constant(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")

def _pairs_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out

def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(text, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant)

def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode()

def pretty_json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=False, indent=2) + "\n").encode()

def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right): return False
    if type(left) is dict:
        return tuple(left) == tuple(right) and all(exact_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right

def _mutation_audit(certificate: dict[str, object]) -> list[dict[str, object]]:
    targets = dict(MUTATION_TARGETS)
    rows = []
    for name in MUTATION_NAMES:
        changed = mutate_certificate(certificate, name)
        ids = [a["id"] for a, b in zip(certificate["rows"], changed["rows"]) if a != b]
        rows.append({"name": name, "target_id": targets[name], "existing_leaf_changed": ids == [targets[name]], "false_validator_rejected": verify_certificate(changed, compare_fresh=False) is False})
    return rows

def build_payload() -> dict[str, object]:
    paths = {
        "core_file": (ROOT / "src/lag_endpoint_extrema/core.py", CORE_FILE),
        "core_test": (ROOT / "tests/test_core.py", CORE_TEST),
        "source_builder": (ROOT / "experiments/source_locks.py", SOURCE_FILE),
        "source_test": (ROOT / "tests/test_source_locks.py", SOURCE_TEST),
    }
    for name, (path, seal) in paths.items():
        raw = path.read_bytes()
        if (len(raw), sha256(raw).hexdigest()) != seal:
            raise RuntimeError(f"{name} identity changed")
    certificate = build_certificate()
    source = build_source_closure()
    source_raw = canonical_bytes(source)
    audit = _mutation_audit(certificate)
    identities = {
        "core_file": {"bytes": CORE_FILE[0], "sha256": CORE_FILE[1]},
        "core_test": {"bytes": CORE_TEST[0], "sha256": CORE_TEST[1]},
        "certificate": {"canonical_bytes": CERTIFICATE_FIXTURE_BYTES, "canonical_sha256": CERTIFICATE_FIXTURE_SHA256, "rows": CERTIFICATE_FIXTURE_ROWS, "mutations": 66},
        "source_builder": {"bytes": SOURCE_FILE[0], "sha256": SOURCE_FILE[1]},
        "source_test": {"bytes": SOURCE_TEST[0], "sha256": SOURCE_TEST[1]},
        "source_closure": {"canonical_bytes": SOURCE_CANONICAL[0], "canonical_sha256": SOURCE_CANONICAL[1], "git": 184, "remote": 4, "logical": 188, "group_sizes": dict(SOURCE_GROUP_SIZES), "group_digests": dict(SOURCE_GROUP_DIGESTS), "all_git_sha256": ALL_GIT_SHA, "logical_sha256": LOGICAL_SHA},
        "theorem_contract_sha256": sha256(canonical_bytes(THEOREM_CONTRACTS)).hexdigest(),
        "source_role_sha256": sha256(canonical_bytes(SOURCE_ROLES)).hexdigest(),
    }
    declarations = {"network_opt_in": False, "requests_made": 0, "external_payload_vendored": False, "external_payload_hash_hits": [], "remote_redistributable_in_release": list(RIGHTS), "finite_reproduction_not_analytic_proof": True, "fixed_scalar_endpoints_only": True, "limit_before_finite_maximum": True, "outer_theorem_contract_closed": True}
    summary = {"certificate_rows": 72, "core_mutations": 66, "core_mutations_rejected": 66, "result_mutations": len(RESULT_MUTATION_NAMES), "source_git": 184, "source_remote": 4, "source_logical": 188, "maximum": "B_infinity(1)", "maximizers": "mu^2(h)=1 and gcd(h,210)=1", "complement": "same supremum, not attained", "joint": "same supremum, no finite pair", "retained_infimum": "3/pi^2, not attained"}
    payload = {"all_pass": False, "certificate": certificate, "core_mutation_audit": audit, "declarations": declarations, "epistemic_role": "finite_exact_reproduction_plus_frozen_analytic_interfaces", "forbidden": dict(FORBIDDEN), "gates": dict(GATES), "identities": identities, "paper": PAPER, "result_mutation_names": list(RESULT_MUTATION_NAMES), "schema_version": 1, "source_closure": source, "source_roles": deepcopy(SOURCE_ROLES), "status": "RH-398_STAGE1_CERTIFIED", "summary": summary, "theorem_contracts": deepcopy(THEOREM_CONTRACTS), "title": TITLE}
    payload["all_pass"] = (len(canonical_bytes(certificate)) == CERTIFICATE_FIXTURE_BYTES and sha256(canonical_bytes(certificate)).hexdigest() == CERTIFICATE_FIXTURE_SHA256 and verify_certificate(certificate, compare_fresh=False) is True and (len(source_raw), sha256(source_raw).hexdigest()) == SOURCE_CANONICAL and source["pass"] is True and source["git_count"] == 184 and source["remote_count"] == 4 and source["logical_count"] == 188 and source["logical_source_digest"] == LOGICAL_SHA and source["git"]["all_git_source_digest"] == ALL_GIT_SHA and len(audit) == 66 and all(r["existing_leaf_changed"] and r["false_validator_rejected"] for r in audit) and all(v is False for v in FORBIDDEN.values()) and all(v is False for v in GATES.values()))
    return payload

RESULT_MUTATION_NAMES = ("all_pass", "schema_float", "schema_bool", "paper", "status", "core_hash", "certificate_hash", "source_hash", "rights", "network", "fixed_scope", "h_domain", "q_domain", "r_domain", "alphabet", "phase_table", "mobius_extension", "omega", "fixed_data", "centered_output", "terminal_functional", "safety", "limit", "capacity", "d_to_h", "p0", "A_product", "R_difference", "telescope", "maximum", "maximizers", "complement_attained", "gap", "joint_attained", "infimum", "source_role", "RH396_locator", "forbidden", "gate", "mutation_leaf", "outer_contract", "result_mutation_count", "summary", "extra")

def mutate_result(value: dict[str, object], name: str) -> dict[str, object]:
    if type(value) is not dict or name not in RESULT_MUTATION_NAMES: raise ValueError("unknown result mutation")
    out = deepcopy(value)
    edits = {
        "all_pass": (("all_pass",), False), "schema_float": (("schema_version",), 1.0), "schema_bool": (("schema_version",), True), "paper": (("paper",), "RH-397"), "status": (("status",), "draft"),
        "core_hash": (("identities","core_file","sha256"), "0"*64), "certificate_hash": (("identities","certificate","canonical_sha256"), "1"*64), "source_hash": (("identities","source_closure","canonical_sha256"), "2"*64), "rights": (("declarations","remote_redistributable_in_release",2), False), "network": (("declarations","network_opt_in"), True), "fixed_scope": (("theorem_contracts","scope_and_order","fixed_scalar_endpoints_only"), False),
        "h_domain": (("theorem_contracts","scope_and_order","h_domain"), "h in R"), "q_domain": (("theorem_contracts","scope_and_order","q_domain"), "q in R"), "r_domain": (("theorem_contracts","scope_and_order","residue_domain"), "r in Z"), "alphabet": (("theorem_contracts","scope_and_order","alphabet"), "T={-1,+1}"), "phase_table": (("theorem_contracts","scope_and_order","phase_table"), "wrong"), "mobius_extension": (("theorem_contracts","scope_and_order","mobius_extension"), "wrong"), "omega": (("theorem_contracts","scope_and_order","clock"), "omega arbitrary"), "fixed_data": (("theorem_contracts","scope_and_order","fixed_data"), "h may grow with X"), "centered_output": (("theorem_contracts","scope_and_order","centered_output"), "wrong"), "terminal_functional": (("theorem_contracts","scope_and_order","terminal_functional"), "wrong"), "safety": (("theorem_contracts","scope_and_order","safety"), "wrong"), "limit": (("theorem_contracts","scope_and_order","limit"), "wrong"), "capacity": (("theorem_contracts","scope_and_order","capacity"), "wrong"),
        "d_to_h": (("theorem_contracts","product_second_difference_telescope","d"), "d=h"), "p0": (("theorem_contracts","product_second_difference_telescope","p0"), "p0=min prime p with p not dividing h"), "A_product": (("theorem_contracts","product_second_difference_telescope","A_m"), "wrong"), "R_difference": (("theorem_contracts","product_second_difference_telescope","R_l"), "wrong"), "telescope": (("theorem_contracts","product_second_difference_telescope","telescope"), "wrong"), "maximum": (("theorem_contracts","maximum_and_maximizers","maximum"), "wrong"), "maximizers": (("theorem_contracts","maximum_and_maximizers","exact_set"), "wrong"), "complement_attained": (("theorem_contracts","complement_and_gap","attained"), True), "gap": (("theorem_contracts","complement_and_gap","p0_ge5_gap"), "wrong"), "joint_attained": (("theorem_contracts","joint_and_retained_endpoints","finite_pair_attains"), True), "infimum": (("theorem_contracts","joint_and_retained_endpoints","retained_infimum"), "6/pi^2"), "source_role": (("source_roles","RH396","analytic_input"), False), "RH396_locator": (("theorem_contracts","source_and_claim_ceiling","RH396_locator"), "wrong"), "forbidden": (("forbidden","growing_h"), True), "gate": (("gates","A_intrinsic_determinant"), True), "mutation_leaf": (("core_mutation_audit",0,"false_validator_rejected"), False), "outer_contract": (("declarations","outer_theorem_contract_closed"), False), "result_mutation_count": (("summary","result_mutations"), 0), "summary": (("summary","maximum"), "wrong")}
    if name == "extra": out["extra"] = 0; return out
    path, replacement = edits[name]; parent: object = out
    for key in path[:-1]: parent = parent[key]  # type: ignore[index]
    parent[path[-1]] = replacement  # type: ignore[index]
    return out

def _make_result_validator(fresh_builder=build_payload):
    from copy import deepcopy as local_copy
    from hashlib import sha256 as local_sha
    from json import dumps as local_dumps
    anchor_length = 116_612
    anchor_sha = "82698f0b7720ac3efcb589c38a9bf8b7b7c285637cab54c7389bd9343925178d"
    pretty_length = 187_434
    pretty_sha = "b22bd32fd515cbe98ee1fc946cef7e695273fdffd002cb5e29281ceba7e263f7"
    theorem_sha = "cedc5c59a7476ecef897b99d3fa9cc5ee004c8840da5f127a967fa4e3276edbe"
    roles_sha = "76f8d79f7fed8052c5caf0858d6fa1916a88a26a55eac3278b93369d663b0a9b"
    audit_sha = "52fc83b25b1adb6e1b51329df5b24d1ee27250276799c15d2d94436c46481f44"
    expected_top = ("all_pass", "certificate", "core_mutation_audit", "declarations", "epistemic_role", "forbidden", "gates", "identities", "paper", "result_mutation_names", "schema_version", "source_closure", "source_roles", "status", "summary", "theorem_contracts", "title")
    def json_types(v: object) -> bool:
        if type(v) is dict: return all(type(k) is str and json_types(x) for k, x in v.items())
        if type(v) is list: return all(json_types(x) for x in v)
        return type(v) in (str, bool, int, type(None))
    expected = local_copy(fresh_builder())
    if not json_types(expected):
        raise RuntimeError("result factory emitted a non-exact JSON type")
    canonical = local_dumps(expected, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode()
    pretty = (local_dumps(expected, ensure_ascii=False, allow_nan=False, sort_keys=False, indent=2)+"\n").encode()
    if (len(canonical), local_sha(canonical).hexdigest()) != (anchor_length, anchor_sha) or (len(pretty), local_sha(pretty).hexdigest()) != (pretty_length, pretty_sha): raise RuntimeError("independent result seal drift")
    def same(a: object, b: object) -> bool:
        if type(a) is not type(b): return False
        if type(a) is dict: return tuple(a) == tuple(b) and all(same(a[k],b[k]) for k in a)
        if type(a) is list: return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
        return a == b
    def public(value: object, *, compare_fresh: bool=False) -> bool:
        if type(compare_fresh) is not bool: raise TypeError("compare_fresh must be exact bool")
        try:
            if type(value) is not dict or not json_types(value) or not same(value, expected): return False
            raw=local_dumps(value,ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":")).encode(); p=(local_dumps(value,ensure_ascii=False,allow_nan=False,sort_keys=False,indent=2)+"\n").encode()
            if (len(raw),local_sha(raw).hexdigest())!=(anchor_length,anchor_sha) or (len(p),local_sha(p).hexdigest())!=(pretty_length,pretty_sha): return False
            if tuple(value)!=expected_top or value["all_pass"] is not True or type(value["schema_version"]) is not int: return False
            if value["paper"]!="RH-398" or value["status"]!="RH-398_STAGE1_CERTIFIED" or value["title"]!="Exact Lag Endpoint Maximum and Maximizers": return False
            ids=value["identities"]; si=ids["source_closure"]
            if ids["certificate"] != {"canonical_bytes":36635,"canonical_sha256":"d47de091a8fe5a134ba4bbf8ac4689f53b54786d45dc3bfc7061c99b46bea741","rows":72,"mutations":66}: return False
            if (si["git"],si["remote"],si["logical"],si["all_git_sha256"],si["logical_sha256"])!=(184,4,188,"e7341caa25f0787a2e48a4d9c156e0d785b6c2a5516172bdfb25c2ac45377ea8","4cc752fb7baae977bb15a9420101c5ed37727b1f3f7eecf72afce9dec3c73b13"): return False
            tr=local_dumps(value["theorem_contracts"],ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":")).encode(); rr=local_dumps(value["source_roles"],ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":")).encode(); ar=local_dumps(value["core_mutation_audit"],ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":")).encode()
            if (local_sha(tr).hexdigest(),local_sha(rr).hexdigest(),local_sha(ar).hexdigest())!=(theorem_sha,roles_sha,audit_sha): return False
            scope=value["theorem_contracts"]["scope_and_order"]
            product=value["theorem_contracts"]["product_second_difference_telescope"]
            source=value["theorem_contracts"]["source_and_claim_ceiling"]
            if (scope["h_domain"],scope["q_domain"],scope["residue_domain"]) != ("h in Z_{>=1}","q in Z_{>=1}","r in Z/qZ"): return False
            if (scope["alphabet"],scope["phase_table"],scope["mobius_extension"]) != ("T={-1,0,+1}","F_r:T^3->{-1,+1}","mu_0(k)=mu(k) for integer k>=1 and mu_0(k)=0 for k<=0"): return False
            if scope["clock"] != "omega is admissible: 1<=omega(X)<=X and omega(X)->infinity": return False
            if scope["fixed_data"] != "h,q,F,omega are fixed before X->infinity": return False
            if scope["centered_output"] != "epsilon_F(n)=F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))": return False
            if scope["terminal_functional"] != "L_(h,q,X)(F)=(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)epsilon_F(n)/n": return False
            if scope["safety"] != "not(F_r(a,b,c)=+1 and F_(r+d)(c,e,f)=+1) for every r in Z/qZ and a,b,c,e,f in T": return False
            if scope["limit"] != "L_(h,q)(F)=lim_(X->infinity)L_(h,q,X)(F), with the same value for every admissible omega": return False
            if scope["capacity"] != "C_h(q)=max_(universally distance-d safe fixed q-phase F)|L_(h,q)(F)| after every fixed-table terminal-log limit": return False
            if (product["d"],product["p0"]) != ("d=2h","p0=min prime p with p not dividing d"): return False
            if source["RH396_locator"] != "definitions equations (18)-(21), Theorem 1.3 equation (22), and Corollary 1.4 equation (23), PDF page 3": return False
            if len(value["result_mutation_names"]) != 44 or value["summary"]["result_mutations"] != 44: return False
            if len(value["core_mutation_audit"])!=66 or value["declarations"]["remote_redistributable_in_release"] != [False,False,True,False]: return False
            if value["declarations"]["outer_theorem_contract_closed"] is not True: return False
            return not compare_fresh or same(value, fresh_builder())
        except (KeyError,TypeError,ValueError): return False
    return public

validate_result_payload = _make_result_validator()

def main() -> None:
    payload=build_payload()
    if not validate_result_payload(payload,compare_fresh=True): raise RuntimeError("result validation failed")
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({"all_pass":True,"canonical_sha256":sha256(canonical_bytes(payload)).hexdigest(),"pretty_sha256":sha256(OUTPUT.read_bytes()).hexdigest()},sort_keys=True))

if __name__ == "__main__": main()
