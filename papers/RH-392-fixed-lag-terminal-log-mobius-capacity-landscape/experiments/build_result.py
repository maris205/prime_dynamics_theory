"""Build the offline immutable-source-locked RH-392 result."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from fixed_lag_capacity.core import (  # noqa: E402
    MUTATION_NAMES, TITLE, build_certificate, canonical_json_bytes,
    exact_equal, mutate_certificate, payload_sha256, verify_certificate,
)
from source_locks import (  # noqa: E402
    EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
    JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, SOURCE_RELEASE,
    TAO_CANONICAL_SHA256, build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 220_832
CERTIFICATE_FIXTURE_SHA256 = "614297795d4d4dfeadfb5667d3e0d405d04fbe8e07e9d87a743faed9cb267a96"
CORE_FILE_SHA256 = "a4e297f4c324ba1fce1829e5c1caf1b8a7e451a9b90c1f78be5f00d44cd97397"
THEOREM_CONTRACT_SHA256 = "8c435179e5ba56093981b8f9a36e85d42cc32b53557002a6847e06e05547a96f"
SOURCE_CLOSURE_SHA256 = "4f05530cfe4a8cc99aff7dafeae6496969ec20cea6e7da2b03b75c97870f5610"
SOURCE_ROLE_SHA256 = "483ccb0dc95f5049c95dbbd185c1e90f9388f9daf57f3710bf059f59540c2664"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}
EXPECTED_GATE_KEYS = frozenset(GATES)
FORBIDDEN = {
    "growing_q": False,
    "growing_h": False,
    "growing_shift_family": False,
    "ordinary_Cesaro_average": False,
    "effective_uniform_rate": False,
    "degree_ge_3_multicoordinate_truth_tables": False,
    "multiple_interacting_lags": False,
    "all_h_claim_from_determinant_two_precursor": False,
    "black_box_local_density_formula": False,
    "coprime_cutoff_divisors_assumed": False,
    "maximum_before_terminal_limit": False,
    "uniform_simultaneous_q_h_capacity": False,
    "X_dependent_phase_table_or_periodic_mask": False,
    "operator_model": False,
    "trace_formula": False,
    "zero_model": False,
    "proof_of_Riemann_Hypothesis": False,
    "Gate_A": False,
    "Gate_B": False,
    "Gate_C": False,
    "Gate_D": False,
    "Gate_E": False,
    "vendored_external_payload": False,
}
EXPECTED_FORBIDDEN_KEYS = frozenset({
    "growing_q", "growing_h", "growing_shift_family", "ordinary_Cesaro_average",
    "effective_uniform_rate", "degree_ge_3_multicoordinate_truth_tables",
    "multiple_interacting_lags", "all_h_claim_from_determinant_two_precursor",
    "black_box_local_density_formula", "coprime_cutoff_divisors_assumed",
    "maximum_before_terminal_limit", "uniform_simultaneous_q_h_capacity",
    "X_dependent_phase_table_or_periodic_mask",
    "operator_model", "trace_formula", "zero_model", "proof_of_Riemann_Hypothesis",
    "Gate_A", "Gate_B", "Gate_C", "Gate_D", "Gate_E", "vendored_external_payload",
})

THEOREM_CONTRACTS = {
    "terminal_clock": {
        "admissible": "1<=omega(X)<=X for all sufficiently large X and omega(X)->infinity",
        "normalization": "1/log omega(X)",
        "interval": "X/omega(X)<n<=X",
        "limit": "X->infinity",
    },
    "finite_shift_diagonalization": {
        "quantifiers": "for each fixed q>=1, fixed finite pairwise-distinct integer shifts a_1,...,a_m, fixed phasewise coefficients, and every admissible terminal clock omega",
        "functional": "L_(q,a)(P;omega)=lim_(X->infinity)[log omega(X)]^-1 sum_(X/omega(X)<n<=X)P_(n mod q)(mu0(n-a_1),...,mu0(n-a_m))/n",
        "polynomial_domain": "total degree at most 2 in coordinates mu0(n-a_i)",
        "surviving_channels": ["constant", "diagonal coordinate squares"],
        "vanishing_channels": ["all linear monomials", "all off-diagonal quadratic monomials"],
        "limit": "sum_(r mod q)[c_empty(r)/q+sum_i c_ii(r)*delta_(q,r-a_i)]",
        "off_diagonal_determinant": "a_i-a_j!=0 for i!=j",
    },
    "terminal_full_mu_lemma": {
        "forms": "D(n)=a1*n+b1,V(n)=a2*n+b2 with fixed a1,a2 in N and fixed b1,b2 in Z",
        "quantifiers": "for every fixed bounded periodic rho and every admissible terminal clock omega",
        "determinant": "Delta=a1*b2-a2*b1 is arbitrary nonzero",
        "periodic_mask": "fixed bounded periodic rho",
        "conclusion": "as X->infinity, sum_(X/omega(X)<n<=X)mu(D(n))mu(V(n))rho(n)/n=o(log omega(X))",
        "boolean_cutoff": "mu=lambda*1_sf; use S_P and lcm(M,k^2,l^2)<=M(P#)^2",
        "coprime_k_l_assumed": False,
        "reduced_determinant": "L*Delta/(c_D*c_V)!=0 after progression and content extraction",
        "limit_order": ["fix P", "X->infinity", "P->infinity"],
        "remote_input": "Tao Theorem 2 equation (3), fixed nonparallel affine forms only",
    },
    "fixed_lag_compiler": {
        "biquadratic_diagonalization": {
            "quantifiers": "for each pair of fixed integers h>=1 and q>=1, every fixed family of q phase polynomials P_r, and every admissible terminal clock omega",
            "coordinates": "x=mu0(n-h), z=mu(n)",
            "polynomial_domain": "P_r(x,z)=sum_(0<=i,j<=2)c_ij(r)x^i z^j",
            "functional": "L_(q,h)(P;omega)=lim_(X->infinity)[log omega(X)]^-1 sum_(X/omega(X)<n<=X)P_(n mod q)(mu0(n-h),mu(n))/n",
            "limit": "sum_r[c00(r)/q+c20(r)delta_(q,r-h)+c02(r)delta_(q,r)+c22(r)theta^(h)_(q,r)]",
            "clock_independence": "the displayed limit exists and has the same value for every admissible omega",
            "zero_channels": ["c10", "c01", "c11", "c12", "c21"],
        },
        "truth_table_specialization": {
            "quantifiers": "for each pair of fixed integers q,h>=1, every fixed safe phase tuple f=(f_r)_(r in Z/qZ), and every admissible terminal clock omega",
            "alphabet": "T={-1,0,+1}",
            "phase_tables": "f_r:T^2->{-1,+1}",
            "edge_sets": "E_r={(x,z) in T^2:f_r(x,z)=+1}",
            "safety": "there are no (x,z) in E_r and (z,w) in E_(r+h)",
            "interpolant": "Q_(f,r) is the unique coordinatewise-bidegree<=2 interpolant of z*f_r(x,z) on T^2",
            "zero_coefficients": ["c00", "c10", "c20"],
            "compiler_coordinates": ["c01", "c02", "c11", "c12", "c21", "c22"],
            "capacity_score": "L_(q,h)(f;omega):=L_(q,h)(Q_f;omega)=lim_(X->infinity)[log omega(X)]^-1 sum_(X/omega(X)<n<=X)mu(n)f_(n mod q)(mu0(n-h),mu(n))/n",
        },
        "safety": "no edge in E_r is composable with an edge in E_(r+h)",
        "projection": "A_r={x:(x,+1) in E_r}; 512 truth tables -> 8 actions A_r subset T with 64 preimages each",
        "compatibility": "A_r is empty or +1 is absent from A_(r+h)",
    },
    "one_site_density": {
        "meaning": "delta_(q,r) is the terminal density of mu0(n)^2 on the phase n=r mod q",
        "formula": "delta_(q,r)=q^-1 prod_(p not|q)(1-p^-2) prod_(p||q)(1-1_(p|r)/p) prod_(p^2|q)1_(p^2 not|r)",
        "phase_sum": "sum_(r mod q)delta_(q,r)=6/pi^2",
    },
    "theta_local_density": {
        "A_p": "distinct set {0,h mod p^2}",
        "nu_p": "|A_p|",
        "tau_p_r": "#{a in A_p:a=r mod p}, retaining collisions modulo p",
        "formula": "theta_(q,r)^(h)=q^-1 prod_(p not|q)(1-nu_p/p^2) prod_(p||q)(1-tau_p_r/p) prod_(p^2|q)1_(r mod p^2 notin A_p)",
        "cone": ["0<=theta_(q,r)^(h)<=delta_(q,r)", "theta_(q,r)^(h)<=delta_(q,r-h)"],
        "total": "kappa_h=prod_(p^2|h)(1-p^-2)prod_(p^2 not|h)(1-2p^-2)",
    },
    "charge_and_cycles": {
        "plus_charge": "a plus phase r charges the forced-empty predecessor r-h",
        "identity": "H_(r-h)-theta_r/2=(delta_(r-h)-theta_(r-h))/2+(delta_(r-h)-theta_r)/2",
        "translation": "r->r+h is a permutation of Z/qZ",
        "cycles": "gcd(q,h) cycles, each of length q/gcd(q,h)",
        "self_loop": "q divides h forces the plus-phase set empty",
    },
    "capacity": {
        "safe_table_set": "mathcal A_(q,h) is the finite set of fixed q-phase tuples satisfying the typed E_r/E_(r+h) safety condition",
        "definition": "G_log(q,h)=max_(f in mathcal A_(q,h))|L_(q,h)(f;omega)|, with each fixed-table X->infinity limit formed before the finite maximum",
        "maximum_order": "finite fixed-table maximum after, never before, the terminal limit; no X-dependent table family",
        "omega_independence": True,
        "formula": "G_log(q,h)=6/pi^2-kappa_h/2 for every fixed q,h",
        "positive_witness": "constant table 36 gives +G_log(q,h)",
        "negative_witness": "constant reflected table 72 gives -G_log(q,h)",
        "reflection_parity": ["+", "-", "-", "+", "+", "-"],
        "fixed_q_independence": True,
    },
    "square_divisor_landscape": {
        "kappa_star": "prod_p(1-2/p^2)",
        "maximum": "G_log(q,h)=6/pi^2-kappa_star/2 exactly for squarefree h",
        "range": "3/pi^2<G_log(q,h)<=6/pi^2-kappa_star/2",
        "infimum": "3/pi^2",
        "infimum_attained": False,
        "approach_sequence": "h_y=(prod_(p<=y)p)^2",
    },
    "countercases": [
        {"h": 2, "q": 2, "r": 0, "p": 2, "nu": 2, "tau": 2, "p_exact_factor": "0"},
        {"h": 6, "q": 3, "r": 0, "p": 3, "nu": 2, "tau": 2, "p_exact_factor": "1/3"},
        {"h": 4, "q": 2, "r": 0, "p": 2, "nu": 1, "tau": 1, "p_exact_factor": "1/2"},
        {"h": 9, "q": 3, "r": 0, "p": 3, "nu": 1, "tau": 1, "p_exact_factor": "2/3"},
        {"q": 6, "h": 4, "gcd": 2, "cycle_count": 2, "cycle_length": 3},
    ],
}

SOURCE_ROLES = {
    "johnston-yang-arxiv-2204.01980v2": "closure-only inherited global explicit theta/VK source; not used in the RH-392 proof",
    "maynard-annals-2015-small-gaps": "closure-only inherited bounded consecutive-prime-gap source; not used in the RH-392 proof",
    "tao-cambridge-2016-logarithmic-chowla": "actual remote analytic input only: Theorem 2 equation (3), fixed nonparallel two-affine logarithmic Liouville cancellation; no uniform h, q, or rate",
    "local_precursors": "the released terminal-log package and its local prime-square precursor supply reduction provenance; the arbitrary-determinant completion and all-h CRT density formula are proved locally here, not imported as all-h corollaries",
}


def pretty_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def _validate_constants() -> None:
    hashes = (
        CERTIFICATE_FIXTURE_SHA256, CORE_FILE_SHA256, THEOREM_CONTRACT_SHA256,
        SOURCE_CLOSURE_SHA256, SOURCE_ROLE_SHA256,
        EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256,
    )
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(SOURCE_RELEASE) is not str or not COMMIT_RE.fullmatch(SOURCE_RELEASE):
        raise ValueError("sealed source release is malformed")
    if type(CERTIFICATE_FIXTURE_BYTES) is not int or type(CERTIFICATE_FIXTURE_BYTES) is bool or CERTIFICATE_FIXTURE_BYTES <= 0:
        raise ValueError("certificate byte seal is malformed")
    if type(EXPECTED_GATE_KEYS) is not frozenset or set(GATES) != EXPECTED_GATE_KEYS:
        raise ValueError("Gate membership changed")
    if type(EXPECTED_FORBIDDEN_KEYS) is not frozenset or set(FORBIDDEN) != EXPECTED_FORBIDDEN_KEYS:
        raise ValueError("claim-firewall membership changed")
    if any(type(value) is not bool or value is not False for value in (*GATES.values(), *FORBIDDEN.values())):
        raise TypeError("Gate/firewall values must be exact false booleans")
    if payload_sha256(THEOREM_CONTRACTS) != THEOREM_CONTRACT_SHA256:
        raise ValueError("theorem contract seal changed")
    if payload_sha256(SOURCE_ROLES) != SOURCE_ROLE_SHA256:
        raise ValueError("source-role contract seal changed")


def _mutation_rows(certificate: dict[str, object]) -> list[dict[str, object]]:
    return [
        {"name": name, "rejected": not verify_certificate(mutate_certificate(certificate, name), compare_fresh=False)}
        for name in MUTATION_NAMES
    ]


def build_payload() -> dict[str, object]:
    _validate_constants()
    certificate = build_certificate()
    certificate_bytes = len(canonical_json_bytes(certificate))
    certificate_sha = payload_sha256(certificate)
    fixture_pass = certificate_bytes == CERTIFICATE_FIXTURE_BYTES and certificate_sha == CERTIFICATE_FIXTURE_SHA256
    core_path = ROOT / "src" / "fixed_lag_capacity" / "core.py"
    from hashlib import sha256
    core_sha = sha256(core_path.read_bytes()).hexdigest()
    core_pass = core_sha == CORE_FILE_SHA256
    baseline_false = verify_certificate(certificate, compare_fresh=False)
    baseline_fresh = verify_certificate(certificate, compare_fresh=True)
    mutation_rows = _mutation_rows(certificate)
    mutation_pass = len(mutation_rows) == 24 and all(row["rejected"] is True for row in mutation_rows)
    source_locks = build_source_closure()
    source_sha = payload_sha256(source_locks)
    source_fixture_pass = source_sha == SOURCE_CLOSURE_SHA256
    source_pass = (
        source_fixture_pass and source_locks["pass"] is True
        and (source_locks["git_count"], source_locks["remote_count"], source_locks["logical_count"]) == (106, 3, 109)
        and source_locks["git"]["all_git_source_digest"] == EXPECTED_ALL_GIT_SOURCE_DIGEST
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_locks["remote"]["network_fetch_performed"] is False
        and source_locks["remote"]["external_payload_hash_hits"] == []
    )
    finite_contracts = {
        "global_closure": deepcopy(certificate["contracts"]["global_closure"]),
        "translation_oracle": deepcopy(certificate["contracts"]["translation_oracle"]),
        "row_partition": deepcopy(certificate["contracts"]["row_partition"]),
    }
    declarations = {
        "network_fetch_performed_by_build": False,
        "external_payload_vendored": False,
        "finite_rows_are_analytic_proof": False,
        "effective_rate_computed": False,
        "git_source_rows": 106,
        "remote_logical_objects": 3,
        "logical_source_rows": 109,
    }
    all_pass = all((
        fixture_pass, core_pass, baseline_false, baseline_fresh, certificate["all_pass"] is True,
        mutation_pass, source_pass, finite_contracts["global_closure"]["pass"] is True,
        all(row["pass"] is True for row in finite_contracts["translation_oracle"]),
        not any(GATES.values()), not any(FORBIDDEN.values()),
    ))
    payload = {
        "all_pass": all_pass,
        "certificate": certificate,
        "certificate_fixture": {"canonical_bytes": certificate_bytes, "sha256": certificate_sha, "pass": fixture_pass},
        "core_fixture": {"sha256": core_sha, "pass": core_pass},
        "declarations": declarations,
        "finite_contracts": finite_contracts,
        "forbidden_claims": deepcopy(FORBIDDEN),
        "gates": deepcopy(GATES),
        "mutations": {"count": len(mutation_rows), "names": list(MUTATION_NAMES), "results": mutation_rows, "all_pass": mutation_pass},
        "paper": "RH-392",
        "source_locks": source_locks,
        "source_fixture": {"sha256": source_sha, "pass": source_fixture_pass},
        "source_roles": deepcopy(SOURCE_ROLES),
        "status": "RH-392_fixed_lag_terminal_log_mobius_capacity_landscape_certified",
        "theorems": deepcopy(THEOREM_CONTRACTS),
        "title": TITLE,
    }
    return payload


def validate_result_payload(payload: object, *, compare_fresh: bool = True) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be exact bool")
    try:
        _validate_constants()
        if type(payload) is not dict or set(payload) != {
            "all_pass", "certificate", "certificate_fixture", "core_fixture", "declarations",
            "finite_contracts", "forbidden_claims", "gates", "mutations", "paper",
            "source_fixture", "source_locks", "source_roles", "status", "theorems", "title",
        }:
            raise ValueError("result membership changed")
        if payload["title"] != TITLE or payload["paper"] != "RH-392" or payload["status"] != "RH-392_fixed_lag_terminal_log_mobius_capacity_landscape_certified":
            raise ValueError("result identity changed")
        certificate = payload["certificate"]
        if not verify_certificate(certificate, compare_fresh=False):
            raise ValueError("certificate failed")
        if not exact_equal(payload["certificate_fixture"], {"canonical_bytes": CERTIFICATE_FIXTURE_BYTES, "sha256": CERTIFICATE_FIXTURE_SHA256, "pass": True}):
            raise ValueError("certificate fixture changed")
        if not exact_equal(payload["core_fixture"], {"sha256": CORE_FILE_SHA256, "pass": True}):
            raise ValueError("core fixture changed")
        if not exact_equal(payload["theorems"], THEOREM_CONTRACTS) or not exact_equal(payload["source_roles"], SOURCE_ROLES):
            raise ValueError("theorem/source role changed")
        if not exact_equal(payload["gates"], GATES) or not exact_equal(payload["forbidden_claims"], FORBIDDEN):
            raise ValueError("Gate/firewall changed")
        source = payload["source_locks"]
        if type(source) is not dict or source.get("pass") is not True or (source.get("git_count"), source.get("remote_count"), source.get("logical_count")) != (106, 3, 109):
            raise ValueError("source closure changed")
        if payload_sha256(source) != SOURCE_CLOSURE_SHA256:
            raise ValueError("source closure seal changed")
        if not exact_equal(payload["source_fixture"], {"sha256": SOURCE_CLOSURE_SHA256, "pass": True}):
            raise ValueError("source fixture changed")
        if source.get("logical_source_digest") != EXPECTED_LOGICAL_SOURCE_DIGEST or source["git"].get("all_git_source_digest") != EXPECTED_ALL_GIT_SOURCE_DIGEST:
            raise ValueError("source digest changed")
        if source["remote"].get("network_fetch_performed") is not False or source["remote"].get("external_payload_hash_hits") != []:
            raise ValueError("source offline/nonvendor contract changed")
        mutations = payload["mutations"]
        if (type(mutations) is not dict or type(mutations.get("count")) is not int or type(mutations.get("count")) is bool
                or mutations.get("count") != 24 or mutations.get("names") != list(MUTATION_NAMES)
                or mutations.get("all_pass") is not True or type(mutations.get("results")) is not list
                or len(mutations["results"]) != 24):
            raise ValueError("mutation contract changed")
        if ([row.get("name") if type(row) is dict else None for row in mutations["results"]] != list(MUTATION_NAMES)
                or any(type(row) is not dict or set(row) != {"name", "rejected"}
                       or type(row["name"]) is not str or row["rejected"] is not True for row in mutations["results"])):
            raise ValueError("mutation result changed")
        finite = payload["finite_contracts"]
        if type(finite) is not dict or set(finite) != {"global_closure", "translation_oracle", "row_partition"}:
            raise ValueError("finite contract membership changed")
        if (not exact_equal(finite["global_closure"], certificate["contracts"]["global_closure"])
                or not exact_equal(finite["translation_oracle"], certificate["contracts"]["translation_oracle"])
                or not exact_equal(finite["row_partition"], certificate["contracts"]["row_partition"])):
            raise ValueError("finite contract consumption changed")
        if not exact_equal(payload["declarations"], {"network_fetch_performed_by_build": False, "external_payload_vendored": False, "finite_rows_are_analytic_proof": False, "effective_rate_computed": False, "git_source_rows": 106, "remote_logical_objects": 3, "logical_source_rows": 109}):
            raise ValueError("declarations changed")
        if payload["all_pass"] is not True:
            raise ValueError("all_pass changed")
    except (KeyError, TypeError, ValueError):
        return False
    return not compare_fresh or exact_equal(payload, build_payload())


def main() -> None:
    payload = build_payload()
    if not validate_result_payload(payload, compare_fresh=False):
        raise RuntimeError("RH-392 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({"status": payload["status"], "all_pass": True, "git": 106, "remote": 3}, sort_keys=True))


if __name__ == "__main__":
    main()
