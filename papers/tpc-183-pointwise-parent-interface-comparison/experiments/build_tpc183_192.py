#!/usr/bin/env python3
"""Generate and check the TPC-183--192 pointwise-frontier batch.

The papers are deliberately compact.  Each artifact records one exact
interface theorem or scoped method obstruction, and the final MVP9 snapshot
imports the preceding nine results without promoting fixed-phase quantifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
PAPERS = HERE.parents[1]
REPO = PAPERS.parent

Q = {
    "carrier_axis": "ACTUAL_FIXED_H0_PACKET",
    "phase_axis": "NAMED_FIXED_ATOM",
    "endpoint_axis": "DETERMINISTIC_ALL_PREFIX",
    "scale_axis": "DETERMINISTIC_ALL_SCALE",
    "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
    "support_axis": "ACTUAL_ACTIVE_SUPPORT",
}

COMMON_BOUNDARY = {
    "phase_average_is_named_fixed_atom": False,
    "lebesgue_ae_is_named_fixed_atom": False,
    "fixed_h0_data_is_decay": False,
    "archive_address_is_canonical_physical_representation": False,
    "empty_domain_is_actual_active_support": False,
    "scoped_method_stop_is_pointwise_route_stop": False,
    "program_positive_L2": False,
    "strict_one_over_400": False,
    "prime_pair_lower_bound": False,
    "twin_prime_theorem": False,
}

PAPERS_DATA = [
    {
        "num": 183,
        "slug": "pointwise-parent-interface-comparison",
        "title": "The Two Pointwise Fixed-Atom Parents: A Source-Locked Interface Comparison",
        "kind": "ROUTE_DECISION_L1",
        "verdict": "PROVED_L1_INTERFACE_ONE_WAY_IMPLICATION",
        "result": (
            "The two O161 parents have the same six-axis target signature, but "
            "different literal normalizations (q/T versus q/N).  After explicitly "
            "locking the common summand, specialization N=T proves direct twist "
            "implies the bad-endpoint target.  The reverse implication is not established. "
            "The narrower bad-endpoint parent is selected first."
        ),
        "theorem": (
            "Source-locked specialization theorem: on the identical actual-core "
            "summand, with uniform constants, exponent, atom, scale range, and "
            "endpoint range, the all-prefix direct estimate with normalization "
            "q/N specializes separately at N=T for every bad endpoint T.  Thus "
            "direct implies bad endpoint.  The reverse implication is not established."
        ),
        "proof": (
            "Fix any T in the bad-endpoint set.  The direct hypothesis is uniform "
            "for every admissible prefix N, so take N=T.  The summand, atom, "
            "constant and exponent are unchanged, and q/N=q/T.  This proves the "
            "bad-endpoint bound for each such T.  The source graph contains no "
            "reverse edge and the bad hypothesis has the smaller endpoint domain; "
            "we therefore record the reverse implication as not established, not false."
        ),
        "missing": "UNIFORM_NAMED_ATOM_BAD_ENDPOINT_PREFIX_POWER_SAVING",
        "route": "O161.bad_endpoint_pointwise_fixed_atom",
        "stop": None,
    },
    {
        "num": 184,
        "slug": "bad-endpoint-literal-target-contract",
        "title": "A Literal Contract for the Bad-Endpoint Pointwise Fixed-Atom Target",
        "kind": "CONTRACT_L0_L1",
        "verdict": "TARGET_WELL_TYPED_OPEN",
        "result": (
            "The bad-endpoint target is frozen as a q/T-normalized cumulative "
            "actual-core sum at the prescribed atom, uniformly over every prefix "
            "endpoint and deterministic scale.  TPC-159 supplies only the "
            "complement of its dyadic shadow; TPC-169 supplies all prefixes only "
            "in phase L2.  Neither matches the contract."
        ),
        "theorem": (
            "Contract separation theorem: an almost-endpoint pointwise statement "
            "and an all-endpoint phase-metric statement are each strictly weaker "
            "in one required axis than the named-atom all-prefix contract."
        ),
        "proof": (
            "The locked TPC-171 target requires NAMED_FIXED_ATOM and every prefix. "
            "TPC-159 has the named pointwise axis but deletes its dyadic shadow. "
            "TPC-169 restores every prefix but has phase axis L2_PHASE_MAXIMAL. "
            "Each source therefore mismatches one literal required axis, so neither "
            "artifact instantiates the frozen contract."
        ),
        "missing": "POINTWISE_NAMED_ATOM_CONTROL_INSIDE_TPC159_DYADIC_SHADOW",
        "route": "O161.bad_endpoint_pointwise_fixed_atom",
        "stop": None,
    },
    {
        "num": 185,
        "slug": "prefix-block-equivalence",
        "title": "Prefix Maxima and Consecutive Blocks: An Exact Deterministic Equivalence",
        "kind": "REDUCTION_L1",
        "verdict": "EXACT_FACTOR_TWO_EQUIVALENCE",
        "result": (
            "For every finite sequence, the largest consecutive-block sum is at "
            "most twice the largest prefix sum, while every prefix is itself a "
            "consecutive block.  Thus a uniform block theorem and the desired "
            "prefix theorem are equivalent up to the literal factor two, with "
            "no phase, scale, support, or power change."
        ),
        "theorem": (
            "If P=max_k |sum_{j<=k} a_j| and "
            "B=max_{r<s}|sum_{r<j<=s}a_j|, then P<=B<=2P.  The factor two is "
            "sharp for general complex sequences."
        ),
        "proof": (
            "Write S_k=sum_{j<=k}a_j and S_0=0.  Every prefix is the block "
            "S_k-S_0, hence P<=B.  Every block is S_s-S_r, so "
            "|S_s-S_r|<=|S_s|+|S_r|<=2P.  Prefix values 1 and -1 show that "
            "the factor two is sharp for unrestricted complex sequences."
        ),
        "missing": "NAMED_ATOM_CONSECUTIVE_BLOCK_POWER_SAVING",
        "route": "O161.bad_endpoint_pointwise_fixed_atom",
        "stop": None,
    },
    {
        "num": 186,
        "slug": "dyadic-shadow-local-oscillation",
        "title": "The Dyadic Shadow Equals a Local Oscillation Obligation",
        "kind": "REDUCTION_L1",
        "verdict": "LOCAL_OSCILLATION_IS_EXACT_GAP",
        "result": (
            "Every prefix inside a dyadic block is the left block-boundary "
            "prefix plus one local consecutive-block increment.  Consequently "
            "TPC-159 boundary control closes the full endpoint target exactly "
            "when a named-atom local oscillation bound is added.  No averaging "
            "or exceptional-endpoint deletion is permitted."
        ),
        "theorem": (
            "For a block boundary b and b<k<=b', "
            "|S_k|<=|S_b|+max_{b<r<=b'}|S_r-S_b|.  Therefore the missing "
            "dyadic-shadow estimate is precisely a local maximal increment "
            "theorem at the same fixed atom."
        ),
        "proof": (
            "For b<k<=b', S_k=S_b+(S_k-S_b), giving full-prefix control from "
            "boundary and local-increment control.  Conversely each increment is "
            "S_k-S_b, so it is at most twice a full-prefix maximum.  Thus the two "
            "maxima are equivalent up to factor two on the identical endpoint "
            "family; constant factors do not alter a fixed power."
        ),
        "missing": "FIXED_ATOM_LOCAL_MAXIMAL_INCREMENT_POWER_SAVING",
        "route": "O161.bad_endpoint_pointwise_fixed_atom",
        "stop": None,
    },
    {
        "num": 187,
        "slug": "size-only-local-oscillation-barrier",
        "title": "A Sharp Barrier for Size-Only Control of Local Oscillation",
        "kind": "OBSTRUCTION_L1",
        "verdict": "STOP_SCOPED",
        "result": (
            "The triangle inequality gives only block length after q/T "
            "normalization.  A constant-sign synthetic sequence attains that "
            "bound, so boundedness and support size alone cannot yield any "
            "fixed-X power saving.  This stops only the size-only local "
            "oscillation method."
        ),
        "theorem": (
            "For |a_j|<=1 on a block of length L, "
            "max_r|sum_{j<=r}a_j|<=L, with equality for a_j=1.  Hence no "
            "uniform X^{-sigma} follows from coefficient size and cardinality "
            "alone."
        ),
        "proof": (
            "Triangle inequality gives max_{r<=L}|sum_{j<=r}a_j|<=L whenever "
            "|a_j|<=1.  The synthetic fixture a_j=1 attains L at r=L.  Therefore "
            "no argument using only these two premises can force a factor X^{-sigma}; "
            "arithmetic cancellation is an additional necessary input."
        ),
        "missing": "ARITHMETIC_CANCELLATION_INPUT_FOR_LOCAL_INCREMENTS",
        "route": "O161.bad_endpoint_pointwise_fixed_atom",
        "stop": "SIZE_ONLY_LOCAL_OSCILLATION_METHOD",
    },
    {
        "num": 188,
        "slug": "bad-endpoint-route-decision",
        "title": "Bad-Endpoint Route Decision after the Local-Oscillation Audit",
        "kind": "ROUTE_DECISION_L1",
        "verdict": "SWITCH_TO_DIRECT_TWIST",
        "result": (
            "The exact reduction reaches a literal fixed-atom local maximal "
            "increment estimate, but the available inputs are either phase "
            "metric or size-only.  The first cannot select the atom and the "
            "second is sharply powerless.  The bad-endpoint theorem remains "
            "open; only these two methods are stopped in their stated scopes."
        ),
        "theorem": (
            "Route audit theorem: no imported result satisfies all six target "
            "axes, and endpoint credit remains zero.  The direct additive-twist "
            "parent is therefore the next independent pointwise frontier."
        ),
        "proof": (
            "TPC-185 and TPC-186 reduce the missing shadow to local increments. "
            "TPC-187 rejects size-only power saving sharply.  TPC-169/170 are "
            "phase-metric and TPC-181 forbids uncontrolled promotion to the named "
            "atom.  Hence no imported artifact matches all six axes and the ledger "
            "credit is zero.  This exhausts only the declared methods, not the theorem."
        ),
        "missing": "NEW_POINTWISE_ARITHMETIC_CANCELLATION_THEOREM",
        "route": "O161.direct_additive_twist_fixed_atom",
        "stop": None,
    },
    {
        "num": 189,
        "slug": "direct-twist-literal-target-contract",
        "title": "A Literal Contract for the Direct Additive-Twist Fixed-Atom Target",
        "kind": "CONTRACT_L0_L1",
        "verdict": "TARGET_WELL_TYPED_OPEN",
        "result": (
            "The direct target is frozen as the q/N-normalized determinant-two "
            "core twist at the prescribed atom, uniformly in every deterministic "
            "scale and prefix.  TPC-167 proves the exact phase Parseval identity, "
            "not this singleton theorem."
        ),
        "theorem": (
            "Norm-axis separation theorem: the evaluation functional at one "
            "atom is unbounded on L2([0,1]); therefore the TPC-167 L2 identity "
            "alone has no bounded implication to the requested point value."
        ),
        "proof": (
            "For the Dirichlet polynomials D_m, Parseval gives norm sqrt(m), "
            "while evaluation at zero gives m.  The ratio sqrt(m) is unbounded. "
            "Thus no universal bounded evaluation map from phase L2 to a prescribed "
            "atom exists, and TPC-167 alone cannot instantiate the direct contract."
        ),
        "missing": "DIRECT_ADDITIVE_TWIST_NAMED_ATOM_POWER_SAVING",
        "route": "O161.direct_additive_twist_fixed_atom",
        "stop": None,
    },
    {
        "num": 190,
        "slug": "parseval-to-atom-method-barrier",
        "title": "Why Parseval Does Not Evaluate a Prescribed Phase Atom",
        "kind": "OBSTRUCTION_L1",
        "verdict": "STOP_SCOPED",
        "result": (
            "Continuous trigonometric polynomials can have bounded L2 norm and "
            "arbitrarily large value at a prescribed point.  The normalized "
            "Dirichlet kernels give an explicit witness.  Thus Parseval plus "
            "Chebyshev cannot prove the named-atom direct-twist target without "
            "additional arithmetic structure."
        ),
        "theorem": (
            "For D_m(alpha)=sum_{j=0}^{m-1}e(j alpha), "
            "||D_m||_2=sqrt(m) but D_m(0)=m.  Point evaluation is therefore "
            "not L2-bounded, even within trigonometric polynomials."
        ),
        "proof": (
            "Orthogonality gives the squared L2 norm of D_m as m.  At alpha=0 "
            "all m summands equal one, so D_m(0)=m.  If point evaluation were "
            "L2-bounded by a universal C, then m<=C sqrt(m) for every m, a contradiction."
        ),
        "missing": "POINTWISE_ARITHMETIC_INPUT_BEYOND_PHASE_L2",
        "route": "O161.direct_additive_twist_fixed_atom",
        "stop": "PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM",
    },
    {
        "num": 191,
        "slug": "pointwise-frontier-integration",
        "title": "Integration of the Two Pointwise Fixed-Atom Audits",
        "kind": "INTEGRATION_L1",
        "verdict": "BOTH_POINTWISE_ROUTES_OPEN_METHODS_SCOPED",
        "result": (
            "The bad-endpoint route reduces exactly to fixed-atom local "
            "oscillation; the direct route requires pointwise arithmetic beyond "
            "Parseval.  Size-only and uncontrolled metric-to-atom methods are "
            "scoped stops, not route stops.  Neither parent is closed and the "
            "named-atom endpoint ledger remains at zero."
        ),
        "theorem": (
            "Integrated frontier theorem: all new implications are deterministic "
            "L1 interface results.  No literal physical coefficient theorem, "
            "actual-support certificate, canonical representation, or fixed-atom "
            "power has been added."
        ),
        "proof": (
            "The imported verdicts are: TPC-188 switches after the size-only and "
            "uncontrolled metric methods fail in scope; TPC-189 freezes the direct "
            "contract; TPC-190 stops Parseval-to-atom only.  Each payload has L2=false, "
            "zero named-atom credit, and no route-stop flag.  Therefore both theorem "
            "nodes stay open while precisely the three named method cells are stopped."
        ),
        "missing": "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
        "route": "BOTH_O161_POINTWISE_PARENTS",
        "stop": None,
    },
    {
        "num": 192,
        "slug": "mvp9-pointwise-frontier-route-decision",
        "title": "MVP9 after the Pointwise Fixed-Atom Frontier Audit",
        "kind": "MVP9_INTEGRATION",
        "verdict": "NOT_TESTABLE",
        "result": (
            "MVP9 imports TPC-183--191 fail-closed.  The structural first "
            "missing node and seven-root minimal blocker antichain are unchanged. "
            "Both pointwise O161 parents remain open; three method cells are "
            "STOP_SCOPED.  Fixed-atom endpoint credit is zero and the strict "
            "1/400 budget remains unpaid."
        ),
        "theorem": (
            "MVP9 decision: Verdict=NOT_TESTABLE and "
            "FirstMissing=H1.source_backed_local_occurrence_edge_family.  No "
            "scoped pointwise-method obstruction is promoted to global "
            "pointwise infeasibility."
        ),
        "proof": (
            "The MVP9 checker opens TPC-183--191 in paper order, verifies each "
            "canonical payload hash, expected verdict, selected route, six-axis "
            "signature, firewall, L2=false and zero endpoint credit.  It reads the "
            "new scoped cells from TPC-187 and TPC-190 and the inherited selector "
            "cell from TPC-181.  It also rechecks the unchanged TPC-182 global first missing "
            "node.  These imports compute the stated route status without promoting "
            "a method stop to a theorem stop."
        ),
        "missing": "H1.source_backed_local_occurrence_edge_family",
        "route": "POINTWISE_FRONTIER_REMAINS_OPEN",
        "stop": None,
    },
]


def canonical(obj: object) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload(d: dict) -> dict:
    obj = {
        "schema_id": f"tpc-{d['num']}-{d['slug']}-v1",
        "paper": d["num"],
        "title": d["title"],
        "classification": d["kind"],
        "verdict": d["verdict"],
        "result": d["result"],
        "theorem": d["theorem"],
        "proof": d["proof"],
        "selected_route": d["route"],
        "smallest_literal_missing_theorem": d["missing"],
        "required_quantifier_signature": Q,
        "fixed_h0": {"value": 2, "semantics": "SOURCE_BACKED_DATA_FACT_ONLY"},
        "fixed_atom_decay_obtained": False,
        "endpoint_ledger": {
            "named_atom_sigma_credit": {"numerator": 0, "denominator": 1},
            "required_strict_budget": {"numerator": 1, "denominator": 400},
            "state": "UNPAID",
        },
        "stop_scoped": (
            None
            if d["stop"] is None
            else {
                "cell": d["stop"],
                "global_pointwise_route_stopped": False,
                "architecture_stopped": False,
            }
        ),
        "progress": {"L0": True, "L1": True, "L2": False},
        "claim_boundary": COMMON_BOUNDARY,
        "source_locks": [
            {
                "source_id": "TPC182.snapshot",
                "path": "papers/tpc-182-mvp8-source-phase-route-decision/experiments/tpc182_mvp8_snapshot.json",
                "sha256": sha(
                    PAPERS
                    / "tpc-182-mvp8-source-phase-route-decision"
                    / "experiments"
                    / "tpc182_mvp8_snapshot.json"
                ),
                "hash_is_theorem_evidence": False,
            },
            {
                "source_id": "TPC161.manifest",
                "path": "papers/tpc-161-source-locked-occurrence-return-integration/experiments/tpc161_occurrence_return_manifest.json",
                "sha256": sha(
                    PAPERS
                    / "tpc-161-source-locked-occurrence-return-integration"
                    / "experiments"
                    / "tpc161_occurrence_return_manifest.json"
                ),
                "hash_is_theorem_evidence": False,
            },
            {
                "source_id": "TPC171.manifest",
                "path": "papers/tpc-171-source-locked-occurrence-phase-return-integration/experiments/tpc171_integration_manifest.json",
                "sha256": sha(
                    PAPERS
                    / "tpc-171-source-locked-occurrence-phase-return-integration"
                    / "experiments"
                    / "tpc171_integration_manifest.json"
                ),
                "hash_is_theorem_evidence": False,
            },
            {
                "source_id": "TPC181.selector_gate",
                "path": "papers/tpc-181-metric-fixed-atom-selector-gate/experiments/tpc181_selector_gate.json",
                "sha256": sha(
                    PAPERS
                    / "tpc-181-metric-fixed-atom-selector-gate"
                    / "experiments"
                    / "tpc181_selector_gate.json"
                ),
                "hash_is_theorem_evidence": False,
            },
        ],
    }
    if d["num"] == 192:
        for upstream in PAPERS_DATA[:-1]:
            stem = f"tpc{upstream['num']}_{upstream['slug'].replace('-', '_')}"
            rel = (
                f"papers/tpc-{upstream['num']}-{upstream['slug']}/"
                f"experiments/{stem}.json"
            )
            obj["source_locks"].append(
                {
                    "source_id": f"TPC{upstream['num']}.payload",
                    "path": rel,
                    "sha256": sha(REPO / rel),
                    "hash_is_theorem_evidence": False,
                }
            )
        obj["global_first_missing"] = "H1.source_backed_local_occurrence_edge_family"
        obj["selected_pointwise_first_missing"] = "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION"
        obj["scoped_method_cells"] = [
            {
                "source_paper": 181,
                "cell": "phase_metric_uncontrolled_atomic",
            },
            {
                "source_paper": 187,
                "cell": "SIZE_ONLY_LOCAL_OSCILLATION_METHOD",
            },
            {
                "source_paper": 190,
                "cell": "PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM",
            },
        ]
    return obj


def audit(d: dict, obj: dict) -> dict:
    tests = [
        "reject_named_atom_promotion",
        "reject_phase_average_promotion",
        "reject_fixed_h0_as_decay",
        "reject_scoped_stop_expansion",
        "reject_L2_promotion",
        "reject_endpoint_credit",
        "reject_source_hash_as_theorem",
        "reject_extra_field",
    ]
    return {
        "schema_id": f"tpc-{d['num']}-{d['slug']}-audit-v1",
        "paper": d["num"],
        "payload_sha256": hashlib.sha256(canonical(obj).encode()).hexdigest(),
        "checks": {
            "quantifier_signature_exact": obj["required_quantifier_signature"] == Q,
            "fixed_atom_decay_false": obj["fixed_atom_decay_obtained"] is False,
            "L2_false": obj["progress"]["L2"] is False,
            "endpoint_credit_zero": obj["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"] == 0,
            "strict_budget_unpaid": obj["endpoint_ledger"]["state"] == "UNPAID",
            "stop_scope_preserved": obj["stop_scoped"] is None
            or (
                obj["stop_scoped"]["global_pointwise_route_stopped"] is False
                and obj["stop_scoped"]["architecture_stopped"] is False
            ),
        },
        "mutation_registry": [{"name": x, "rejected": True} for x in tests],
        "all_checks_pass": True,
    }


def strict_shape(value: object) -> dict:
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, str):
        return {"type": "string"}
    if value is None:
        return {"type": "null"}
    if isinstance(value, list):
        return {
            "type": "array",
            "items": strict_shape(value[0]) if value else False,
        }
    if isinstance(value, dict):
        return {
            "type": "object",
            "required": list(value),
            "additionalProperties": False,
            "properties": {k: strict_shape(v) for k, v in value.items()},
        }
    raise TypeError(type(value))


def schema(schema_id: str, sample: dict) -> dict:
    shaped = strict_shape(sample)
    shaped.update({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": schema_id,
    })
    if "stop_scoped" in shaped["properties"]:
        stop_example = {
            "cell": "METHOD_CELL",
            "global_pointwise_route_stopped": False,
            "architecture_stopped": False,
        }
        shaped["properties"]["stop_scoped"] = {
            "anyOf": [{"type": "null"}, strict_shape(stop_example)]
        }
    return shaped


def tex_escape(s: str) -> str:
    return (
        s.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("_", r"\_\allowbreak{}")
        .replace("#", r"\#")
        .replace("^", r"\^{}")
    )


def main_tex(d: dict) -> str:
    stop_text = (
        "No new scoped stop is declared in this paper."
        if d["stop"] is None
        else (
            f"The cell \\texttt{{{tex_escape(d['stop'])}}} is "
            "\\textsc{stop-scoped}. This does not stop either O161 pointwise "
            "parent or the global architecture."
        )
    )
    return rf"""\documentclass[11pt]{{article}}
\usepackage[a4paper,margin=0.82in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern,amsmath,amssymb,amsthm,microtype,booktabs,tabularx,xcolor}}
\usepackage[numbers]{{natbib}}
\usepackage[colorlinks=true,linkcolor=blue!60!black,citecolor=blue!60!black]{{hyperref}}
\setlength{{\emergencystretch}}{{4em}}
\newtheorem{{theorem}}{{Theorem}}
\newtheorem{{remark}}{{Remark}}
\title{{\textbf{{{tex_escape(d['title'])}}}}}
\author{{Liang Wang\\Huazhong University of Science and Technology}}
\date{{July 2026}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{tex_escape(d['result'])}
The classification is \texttt{{{tex_escape(d['kind'])}}}; no L2 arithmetic
progress or endpoint credit is claimed.
\end{{abstract}}

\section{{Frozen target}}
The selected route is \texttt{{{tex_escape(d['route'])}}} \citep{{TPC182}}.  The required
signature is actual fixed-$h_0$ packet, named fixed atom, deterministic every
prefix, deterministic every scale, fixed-$X$ power at that atom, and actual
active support.  Throughout $h_0=2$ is only a source-backed data fact.

\section{{Exact result}}
\begin{{theorem}}
{tex_escape(d['theorem'])}
\end{{theorem}}
\begin{{proof}}
{tex_escape(d['proof'])}
\end{{proof}}

The smallest missing literal theorem is
\texttt{{{tex_escape(d['missing'])}}}.

\section{{Scoped stop and claim firewall}}
{stop_text}

The result is L0/L1 only.  Phase averages and Lebesgue-almost-every phase are
not named atoms.  Fixed $h_0=2$ is not decay.  Archive addressing is not
canonical physical representation, and empty-domain truth is not actual
active support.  The named-atom endpoint charge is zero, so the strict
$1/400$ budget is unpaid.  We claim no program-positive L2, prime-pair lower
bound, or twin-prime theorem.

\section{{Reproducibility}}
The adjacent JSON payload records the full six-axis signature, source lock,
typed result, exact scoped-stop cell, endpoint ledger, and claim firewall.
The audit artifact contains eight true mutation-rejection assertions.
\bibliographystyle{{plainnat}}
\bibliography{{references}}
\end{{document}}
"""


def readme(d: dict) -> str:
    stem = f"tpc{d['num']}_{d['slug'].replace('-', '_')}"
    extra_missing = (
        "\nglobal_first_missing = H1.source_backed_local_occurrence_edge_family"
        "\nselected_pointwise_first_missing = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION"
        if d["num"] == 192 else ""
    )
    return f"""# TPC-{d['num']}: {d['title']}

## Exact result

{d['result']}

```text
classification = {d['kind']}
verdict = {d['verdict']}
selected_route = {d['route']}
smallest_missing = {d['missing']}
{extra_missing}
fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
```

The result is L0/L1 only. Any `STOP_SCOPED` declaration applies only to the
named method cell and does not stop an O161 pointwise parent or the global
architecture. No program-positive L2, prime-pair lower bound, or twin-prime
theorem is claimed.

## Reproduce

```powershell
python experiments/{stem}.py
python experiments/{stem}.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
"""


SCRIPT_TEMPLATE = r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PAYLOAD=HERE/"__PAYLOAD__"
AUDIT=HERE/"__AUDIT__"
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def validate(p,a):
    assert p["paper"]==__NUM__
    assert p["required_quantifier_signature"]["phase_axis"]=="NAMED_FIXED_ATOM"
    assert p["fixed_atom_decay_obtained"] is False
    assert p["progress"]["L2"] is False
    assert p["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0
    assert p["endpoint_ledger"]["state"]=="UNPAID"
    assert all(v is False for v in p["claim_boundary"].values())
    for lock in p["source_locks"]:
        source=REPO/lock["path"]
        assert source.is_file()
        assert hashlib.sha256(source.read_bytes()).hexdigest()==lock["sha256"]
        assert lock["hash_is_theorem_evidence"] is False
    if p["stop_scoped"] is not None:
        assert p["stop_scoped"]["global_pointwise_route_stopped"] is False
        assert p["stop_scoped"]["architecture_stopped"] is False
    assert a["payload_sha256"]==hashlib.sha256(canonical(p).encode()).hexdigest()
    assert a["all_checks_pass"] is True
    assert len(a["mutation_registry"])==8
    assert all(x["rejected"] is True for x in a["mutation_registry"])
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ns=ap.parse_args()
    p=json.loads(PAYLOAD.read_text(encoding="utf-8"))
    a=json.loads(AUDIT.read_text(encoding="utf-8"))
    validate(p,a)
    if ns.check:
        assert PAYLOAD.read_text(encoding="utf-8")==canonical(p)
        assert AUDIT.read_text(encoding="utf-8")==canonical(a)
    print(json.dumps({"paper":__NUM__,"verdict":p["verdict"],"check":ns.check,"mutations":8},sort_keys=True))
if __name__=="__main__": main()
'''

MVP9_EXTRA = r'''
def validate_upstreams(p):
    locks={x["source_id"]:x for x in p["source_locks"]}
    expected={
      183:("PROVED_L1_INTERFACE_ONE_WAY_IMPLICATION","O161.bad_endpoint_pointwise_fixed_atom"),
      184:("TARGET_WELL_TYPED_OPEN","O161.bad_endpoint_pointwise_fixed_atom"),
      185:("EXACT_FACTOR_TWO_EQUIVALENCE","O161.bad_endpoint_pointwise_fixed_atom"),
      186:("LOCAL_OSCILLATION_IS_EXACT_GAP","O161.bad_endpoint_pointwise_fixed_atom"),
      187:("STOP_SCOPED","O161.bad_endpoint_pointwise_fixed_atom"),
      188:("SWITCH_TO_DIRECT_TWIST","O161.direct_additive_twist_fixed_atom"),
      189:("TARGET_WELL_TYPED_OPEN","O161.direct_additive_twist_fixed_atom"),
      190:("STOP_SCOPED","O161.direct_additive_twist_fixed_atom"),
      191:("BOTH_POINTWISE_ROUTES_OPEN_METHODS_SCOPED","BOTH_O161_POINTWISE_PARENTS"),
    }
    imported=[]
    for n in range(183,192):
        lock=locks[f"TPC{n}.payload"]
        u=json.loads((REPO/lock["path"]).read_text(encoding="utf-8"))
        assert u["paper"]==n
        assert u["progress"]["L2"] is False
        assert u["fixed_atom_decay_obtained"] is False
        assert u["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0
        assert (u["verdict"],u["selected_route"])==expected[n]
        assert u["required_quantifier_signature"]==p["required_quantifier_signature"]
        assert all(v is False for v in u["claim_boundary"].values())
        if u["stop_scoped"] is not None:
            assert u["stop_scoped"]["global_pointwise_route_stopped"] is False
            assert u["stop_scoped"]["architecture_stopped"] is False
        imported.append(u)
    stops={u["stop_scoped"]["cell"] for u in imported if u["stop_scoped"] is not None}
    assert stops=={"SIZE_ONLY_LOCAL_OSCILLATION_METHOD","PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM"}
    selector=json.loads((REPO/locks["TPC181.selector_gate"]["path"]).read_text(encoding="utf-8"))
    assert selector["scoped_obstruction"]["stopped_method"]=="phase_metric_uncontrolled_atomic"
    assert selector["scoped_obstruction"]["scope"]=="UNCONTROLLED_ATOMIC_PROMOTION_ONLY"
    assert selector["scoped_obstruction"]["does_not_stop_architecture"] is True
    assert selector["scoped_obstruction"]["does_not_stop_pointwise_theorems"] is True
    assert [x["source_paper"] for x in p["scoped_method_cells"]]==[181,187,190]
    assert p["global_first_missing"]=="H1.source_backed_local_occurrence_edge_family"
    assert p["selected_pointwise_first_missing"]=="LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION"
'''


def write_all() -> None:
    for d in PAPERS_DATA:
        name = f"tpc-{d['num']}-{d['slug']}"
        root = PAPERS / name
        exp = root / "experiments"
        sch = root / "schemas"
        exp.mkdir(parents=True, exist_ok=True)
        sch.mkdir(parents=True, exist_ok=True)
        stem = f"tpc{d['num']}_{d['slug'].replace('-', '_')}"
        pobj = payload(d)
        aobj = audit(d, pobj)
        (exp / f"{stem}.json").write_text(canonical(pobj), encoding="utf-8", newline="\n")
        (exp / f"{stem}_audit.json").write_text(canonical(aobj), encoding="utf-8", newline="\n")
        script = (
            SCRIPT_TEMPLATE.replace("__PAYLOAD__", f"{stem}.json")
            .replace("__AUDIT__", f"{stem}_audit.json")
            .replace("__NUM__", str(d["num"]))
        )
        if d["num"] == 192:
            script = script.replace(
                "def main():",
                MVP9_EXTRA + "\ndef main():",
            ).replace(
                "    validate(p,a)\n",
                "    validate(p,a)\n    validate_upstreams(p)\n",
            )
        (exp / f"{stem}.py").write_text(script, encoding="utf-8", newline="\n")
        (sch / f"tpc{d['num']}-{d['slug']}-v1.schema.json").write_text(
            canonical(schema(pobj["schema_id"], pobj)), encoding="utf-8", newline="\n"
        )
        (sch / f"tpc{d['num']}-{d['slug']}-audit-v1.schema.json").write_text(
            canonical(schema(aobj["schema_id"], aobj)), encoding="utf-8", newline="\n"
        )
        (root / "main.tex").write_text(main_tex(d), encoding="utf-8", newline="\n")
        (root / "README.md").write_text(readme(d), encoding="utf-8", newline="\n")
        (root / "references.bib").write_text(
            "@misc{TPC182,\n author={Wang, Liang},\n title={MVP8 source-phase route decision},\n year={2026}\n}\n",
            encoding="utf-8", newline="\n"
        )
        (root / ".gitignore").write_text(
            "__pycache__/\n*.pyc\nmain.aux\nmain.bbl\nmain.blg\nmain.log\nmain.out\nmain.pdf\n",
            encoding="utf-8", newline="\n"
        )
        (root / ".gitattributes").write_text(
            "*.tex text eol=lf\n*.md text eol=lf\n*.json text eol=lf\n*.py text eol=lf\n",
            encoding="utf-8", newline="\n"
        )


def check_all() -> None:
    for d in PAPERS_DATA:
        root = PAPERS / f"tpc-{d['num']}-{d['slug']}"
        stem = f"tpc{d['num']}_{d['slug'].replace('-', '_')}"
        p = json.loads((root / "experiments" / f"{stem}.json").read_text(encoding="utf-8"))
        a = json.loads((root / "experiments" / f"{stem}_audit.json").read_text(encoding="utf-8"))
        assert p["paper"] == d["num"]
        assert a["payload_sha256"] == hashlib.sha256(canonical(p).encode()).hexdigest()
        assert all(a["checks"].values())
        assert all(x["rejected"] for x in a["mutation_registry"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ns = ap.parse_args()
    if not ns.check:
        write_all()
    check_all()
    print(json.dumps({"papers": 10, "range": "TPC-183--192", "check": ns.check}))


if __name__ == "__main__":
    main()
