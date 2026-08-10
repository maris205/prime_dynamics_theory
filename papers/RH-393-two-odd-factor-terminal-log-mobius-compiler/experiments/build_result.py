"""Build the offline immutable-source-locked RH-393 Stage-1 result."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.json"
for directory in (ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from two_odd_compiler.core import (  # noqa: E402
    MUTATION_NAMES, TITLE, build_certificate, canonical_json_bytes,
    exact_equal, mutate_certificate, verify_certificate,
)
from source_locks import (  # noqa: E402
    EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
    JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, SOURCE_RELEASE,
    TAO_CANONICAL_SHA256, build_source_closure,
)


CERTIFICATE_FIXTURE_BYTES = 117_096
CERTIFICATE_FIXTURE_SHA256 = "f109da241722796418f39708b16fa162cce0b85a6e448998d3ede593b7bd697b"
CORE_FILE_SHA256 = "f92c4f21cd487bff84f40cdc20ca3605d986acfe132fd7e493b126936024a342"
SOURCE_CLOSURE_SHA256 = "1d256d0fd52b034b4d74b82c48248a18a56d328c28b8be7e3ac28354386925ae"
THEOREM_CONTRACT_SHA256 = "db738720ed1d830f874ad5962ba6bbd642c876d860771cb8a2d36fadc82f282a"
SOURCE_ROLE_SHA256 = "573afd710cd32f055f07992e1dc3ab7162ae7a0e6f46330a31eed31c4484ddb8"
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
    "odd_support_at_least_3": False,
    "unrestricted_three_coordinate_truth_tables": False,
    "generic_multishift_safe_table_capacity": False,
    "growing_m": False,
    "growing_q": False,
    "growing_shift_family": False,
    "growing_periodic_masks": False,
    "X_dependent_coefficients": False,
    "effective_uniform_rate": False,
    "ordinary_Cesaro_average": False,
    "maximum_before_terminal_limit": False,
    "adaptive_capacity": False,
    "other_320_tables_have_nonzero_limit": False,
    "other_320_tables_fail_to_converge": False,
    "higher_order_Chowla_input_proved": False,
    "Mirsky_used_as_unlocked_black_box": False,
    "TPC137_used_as_arbitrary_determinant_theorem": False,
    "new_remote_analytic_source": False,
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
EXPECTED_FORBIDDEN_KEYS = frozenset(FORBIDDEN)


THEOREM_CONTRACTS = {
    "terminal_clock": {
        "mobius_extension": "mu_0(t)=mu(t) for every integer t>=1 and mu_0(t)=0 for t<=0",
        "admissible": (
            "1<=omega(X)<=X for all sufficiently large X and omega(X)->infinity"
        ),
        "normalization": "1/log(omega(X))",
        "interval": "X/omega(X)<n<=X",
        "limit": "X->infinity",
    },
    "two_odd_factor_compiler": {
        "quantifiers": (
            "for every fixed integer m>=1, fixed integer q>=1, fixed pairwise-distinct "
            "integer shifts a_1,...,a_m, fixed q-periodic coefficients c_alpha(r), "
            "and every admissible terminal clock omega"
        ),
        "coordinates": "z_i(n)=mu_0(n-a_i)",
        "polynomial": (
            "P_r(z)=sum_(alpha in {0,1,2}^m, |O(alpha)|<=2) "
            "c_alpha(r)prod_i z_i^alpha_i"
        ),
        "odd_support": "O(alpha)={i:alpha_i=1}",
        "even_support": "E(alpha)={i:alpha_i=2}",
        "functional": (
            "T_X(P;omega)=[log omega(X)]^-1 sum_(X/omega(X)<n<=X) "
            "P_(n mod q)(z_1(n),...,z_m(n))/n"
        ),
        "limit": (
            "sum_(r mod q)sum_(alpha in {0,2}^m)c_alpha(r)"
            "Theta_(q,r)(E(alpha))"
        ),
        "surviving_channels": "exactly O(alpha)=empty",
        "vanishing_channels": "every admissible monomial with |O(alpha)| in {1,2}",
        "dimension": (
            "D_m=2^m+m*2^(m-1)+binom(m,2)*2^(m-2), "
            "with absent terms interpreted as zero"
        ),
        "m3_dimension": "D_3=26 of 27; the unique excluded monomial is z_1*z_2*z_3",
        "m3_table_criterion": (
            "for every f:{-1,0,1}^3->R, c111(f)=2^-3 "
            "sum_(epsilon in {-1,+1}^3)epsilon_1epsilon_2epsilon_3*f(epsilon); "
            "the coordinatewise-quadratic interpolant is covered iff c111(f)=0"
        ),
    },
    "phase_density": {
        "B_p": "distinct set {a_i mod p^2:i in E}",
        "nu_p": "cardinality of B_p",
        "tau_p_r": "#{b in B_p:b mod p=r mod p}, counting distinct mod-p^2 classes",
        "formula": (
            "Theta_(q,r)(E)=q^-1 product_(p not|q)(1-nu_p/p^2) "
            "product_(p||q)(1-tau_p_r/p) "
            "product_(p^2|q)1_(r mod p^2 notin B_p)"
        ),
        "empty_support": "Theta_(q,r)(empty)=1/q",
        "phase_sum": "sum_(r mod q)Theta_(q,r)(E)=kappa_E",
        "global_density": "kappa_E=product_p(1-nu_p/p^2)",
        "collision_rule": (
            "deduplicate modulo p^2 before tau; distinct mod-p^2 classes may collide mod p"
        ),
    },
    "proof_decomposition": {
        "odd_zero": "local finite-prime CRT plus a union tail proves Theta and kappa",
        "odd_one": (
            "truncate every even-coordinate square mask; the remaining fixed periodic mask "
            "is cancelled by frozen RH392 equation (19)"
        ),
        "odd_two": (
            "truncate every even-coordinate square mask; the remaining two distinct affine "
            "forms have nonzero determinant and are cancelled by frozen RH392 Theorem 2.2"
        ),
        "boolean_tail": "O_m(log(omega(X))/P+1)",
        "normalized_tail": "O_m(1/P+1/log(omega(X)))",
        "limit_order": ["P_fixed", "X_to_infinity", "P_to_infinity"],
    },
    "squarefree_landscape": {
        "configuration": "A={a_1,...,a_m} with distinct integers",
        "density": "kappa_A=product_p(1-nu_p(A)/p^2)",
        "lower_m_at_most_3": "kappa_A>=C_m:=product_p(1-m/p^2)>0",
        "lower_equality": (
            "for m<=3 equality holds iff every nonzero pairwise difference is squarefree"
        ),
        "lower_witness": "A={0,...,m-1}",
        "zero": (
            "for m>=4 inf_A kappa_A=0 and is attained; kappa_A=0 iff some B_p "
            "covers all p^2 residue classes"
        ),
        "zero_witness": "{0,1,2,3} modulo 4, extended by arbitrary distinct shifts",
        "upper": "for fixed m>=2, sup_A kappa_A=6/pi^2 and is not attained",
        "approach": (
            "Q_y=product_(p<=y)p^2 and A_(m,y)={jQ_y:0<=j<m}; "
            "product_(p<=y)(1-p^-2)product_(p>y)(1-mp^-2)<=kappa_A<=6/pi^2"
        ),
        "m1": "the upper value 6/pi^2 is attained",
        "phase_warning": "individual Theta phases may vanish while global kappa is positive",
    },
    "distinguished_current_corollary": {
        "quantifiers": (
            "for each fixed q, each fixed triple of distinct integer shifts, every fixed "
            "q-phase family of eligible tables, and every admissible terminal clock"
        ),
        "tables": "f_r:{-1,0,1}^2->{-1,+1}",
        "score": "mu_0(n-a_3)f_(n mod q)(mu_0(n-a_1),mu_0(n-a_2))",
        "criterion": (
            "c11=[f(1,1)-f(1,-1)-f(-1,1)+f(-1,-1)]/4=0"
        ),
        "census": "exactly 192 of 512 tables: six corner patterns times 32 free bits",
        "conclusion": "the terminal-log score tends to zero",
        "m3_link": (
            "for g(x,y,z)=z*f(x,y), c111(g)=2^-3 sum_e epsilon_1epsilon_2"
            "epsilon_3g(epsilon)=c11(f)"
        ),
        "outside": "the remaining 320 tables are outside the theorem only",
    },
}


SOURCE_ROLES = {
    "RH392": (
        "direct frozen predecessor: equation (19) supplies fixed-periodic one-form "
        "cancellation and Theorem 2.2 supplies arbitrary-nonzero-determinant two-form "
        "terminal-log cancellation"
    ),
    "tao-cambridge-2016-logarithmic-chowla": (
        "inherited remote analytic provenance through RH392; fixed nonparallel forms only"
    ),
    "johnston-yang-arxiv-2204.01980v2": "closure-only; not used in the RH393 proof",
    "maynard-annals-2015-small-gaps": "closure-only; not used in the RH393 proof",
    "Davenport": "inherited underlying provenance for RH392 equation (19); no new remote",
    "Mirsky": "historical framework only; all multishift densities are proved locally",
    "TPC137": "historical blueprint only; not used as an arbitrary-determinant theorem",
    "RH390_and_RH391": "not dependencies and not included in the source closure",
}


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def pretty_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _validate_constants() -> None:
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    def sealed_sha(value: object) -> str:
        raw = local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return local_sha256(raw).hexdigest()

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list or type(left) is tuple:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right

    expected_title = (
        "Two-Odd-Factor Terminal-Log Möbius Compiler and the Multi-Shift "
        "Squarefree Landscape"
    )
    expected_hashes = {
        "certificate": "f109da241722796418f39708b16fa162cce0b85a6e448998d3ede593b7bd697b",
        "core": "f92c4f21cd487bff84f40cdc20ca3605d986acfe132fd7e493b126936024a342",
        "source_closure": "1d256d0fd52b034b4d74b82c48248a18a56d328c28b8be7e3ac28354386925ae",
        "theorem_contract": "db738720ed1d830f874ad5962ba6bbd642c876d860771cb8a2d36fadc82f282a",
        "source_roles": "573afd710cd32f055f07992e1dc3ab7162ae7a0e6f46330a31eed31c4484ddb8",
        "all_git": "2c187ec15a427ffb0b06a48679f8419be82152fe16ea914c2a86437549117220",
        "logical": "9315d7c01651ed8b4d94f98c3e4019ad11e28469ee6722903721db280b9f92eb",
        "jy": "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786",
        "maynard": "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e",
        "tao": "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84",
    }
    actual_hashes = {
        "certificate": CERTIFICATE_FIXTURE_SHA256,
        "core": CORE_FILE_SHA256,
        "source_closure": SOURCE_CLOSURE_SHA256,
        "theorem_contract": THEOREM_CONTRACT_SHA256,
        "source_roles": SOURCE_ROLE_SHA256,
        "all_git": EXPECTED_ALL_GIT_SOURCE_DIGEST,
        "logical": EXPECTED_LOGICAL_SOURCE_DIGEST,
        "jy": JY_CANONICAL_SHA256,
        "maynard": MAYNARD_CANONICAL_SHA256,
        "tao": TAO_CANONICAL_SHA256,
    }
    expected_gate_keys = frozenset({
        "A_intrinsic_determinant", "B_scattering_completion",
        "C_self_adjoint_generator", "D_von_mangoldt_weighted_prime_power_traces",
        "E_completed_zeta_divisor_equality",
    })
    expected_forbidden_keys = frozenset({
        "odd_support_at_least_3", "unrestricted_three_coordinate_truth_tables",
        "generic_multishift_safe_table_capacity", "growing_m", "growing_q",
        "growing_shift_family", "growing_periodic_masks", "X_dependent_coefficients",
        "effective_uniform_rate", "ordinary_Cesaro_average",
        "maximum_before_terminal_limit", "adaptive_capacity",
        "other_320_tables_have_nonzero_limit", "other_320_tables_fail_to_converge",
        "higher_order_Chowla_input_proved", "Mirsky_used_as_unlocked_black_box",
        "TPC137_used_as_arbitrary_determinant_theorem", "new_remote_analytic_source",
        "operator_model", "trace_formula", "zero_model", "proof_of_Riemann_Hypothesis",
        "Gate_A", "Gate_B", "Gate_C", "Gate_D", "Gate_E",
        "vendored_external_payload",
    })
    if (
        type(TITLE) is not str or TITLE != expected_title
        or type(actual_hashes) is not dict
        or not same(actual_hashes, expected_hashes)
    ):
        raise ValueError("independent title/hash seal changed")
    if any(
        type(value) is not str or not SHA256_RE.fullmatch(value)
        for value in actual_hashes.values()
    ):
        raise ValueError("sealed SHA-256 constant is malformed")
    if (
        type(SOURCE_RELEASE) is not str
        or SOURCE_RELEASE != "9768c1cb5f56d959406c19119315afd542b6c30f"
        or not COMMIT_RE.fullmatch(SOURCE_RELEASE)
    ):
        raise ValueError("sealed source release is malformed")
    if (
        type(CERTIFICATE_FIXTURE_BYTES) is not int
        or type(CERTIFICATE_FIXTURE_BYTES) is bool
        or CERTIFICATE_FIXTURE_BYTES != 117_096
    ):
        raise ValueError("certificate byte seal changed")
    if (
        type(EXPECTED_GATE_KEYS) is not frozenset
        or EXPECTED_GATE_KEYS != expected_gate_keys
        or set(GATES) != expected_gate_keys
    ):
        raise ValueError("Gate membership changed")
    if (
        type(EXPECTED_FORBIDDEN_KEYS) is not frozenset
        or EXPECTED_FORBIDDEN_KEYS != expected_forbidden_keys
        or set(FORBIDDEN) != expected_forbidden_keys
    ):
        raise ValueError("claim-firewall membership changed")
    if any(type(value) is not bool or value is not False for value in (*GATES.values(), *FORBIDDEN.values())):
        raise TypeError("Gate/firewall values must be exact false booleans")
    expected_mutations = (
        "title", "role", "partition_float", "row_count_float",
        "truth_c11", "truth_eligible", "truth_outside", "truth_corner_sum",
        "monomial_allowed", "monomial_odd_count", "monomial_odd_support",
        "monomial_even_support", "monomial_survives", "dimension_odd_zero",
        "dimension_allowed", "dimension_missing", "theta_local_tau",
        "theta_collision_nu", "theta_forced", "theta_direct_count",
        "theta_formula_vector", "theta_phase_mass", "theta_global_density",
        "theta_composite_prime", "landscape_lower", "landscape_cover",
        "landscape_nonattainment", "landscape_primorial", "analytic_source",
        "analytic_limit_order", "analytic_census", "analytic_firewall",
    )
    if type(MUTATION_NAMES) is not tuple or not same(MUTATION_NAMES, expected_mutations):
        raise ValueError("independent mutation-name contract changed")
    if (
        THEOREM_CONTRACT_SHA256 != expected_hashes["theorem_contract"]
        or sealed_sha(THEOREM_CONTRACTS) != expected_hashes["theorem_contract"]
    ):
        raise ValueError("theorem contract seal changed")
    if (
        SOURCE_ROLE_SHA256 != expected_hashes["source_roles"]
        or sealed_sha(SOURCE_ROLES) != expected_hashes["source_roles"]
    ):
        raise ValueError("source-role contract seal changed")


def _mutation_rows(certificate: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            "name": name,
            "rejected": not verify_certificate(
                mutate_certificate(certificate, name), compare_fresh=False
            ),
        }
        for name in MUTATION_NAMES
    ]


def build_payload() -> dict[str, object]:
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    def sealed_bytes(value: object) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    _validate_constants()
    certificate = build_certificate()
    certificate_raw = sealed_bytes(certificate)
    certificate_bytes = len(certificate_raw)
    certificate_sha = local_sha256(certificate_raw).hexdigest()
    fixture_pass = (
        certificate_bytes == CERTIFICATE_FIXTURE_BYTES
        and certificate_sha == CERTIFICATE_FIXTURE_SHA256
    )
    core_sha = local_sha256(
        (ROOT / "src" / "two_odd_compiler" / "core.py").read_bytes()
    ).hexdigest()
    core_pass = core_sha == CORE_FILE_SHA256
    baseline_false = verify_certificate(certificate, compare_fresh=False)
    baseline_fresh = verify_certificate(certificate, compare_fresh=True)
    mutation_rows = _mutation_rows(certificate)
    mutation_pass = (
        len(mutation_rows) == len(MUTATION_NAMES) == 32
        and all(row["rejected"] is True for row in mutation_rows)
    )
    source_locks = build_source_closure()
    source_sha = local_sha256(sealed_bytes(source_locks)).hexdigest()
    source_pass = (
        source_sha == SOURCE_CLOSURE_SHA256
        and source_locks["pass"] is True
        and (source_locks["git_count"], source_locks["remote_count"], source_locks["logical_count"])
        == (117, 3, 120)
        and source_locks["git"]["all_git_source_digest"] == EXPECTED_ALL_GIT_SOURCE_DIGEST
        and source_locks["logical_source_digest"] == EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_locks["remote"]["network_fetch_performed"] is False
        and source_locks["remote"]["external_payload_hash_hits"] == []
    )
    finite_contracts = {
        "row_partition": deepcopy(certificate["row_partition"]),
        "truth_census": {
            "eligible": sum(row["eligible"] for row in certificate["truth_rows"]),
            "outside": sum(row["outside_theorem"] for row in certificate["truth_rows"]),
        },
        "m3_dimension": deepcopy(certificate["dimension_rows"][2]),
        "theta_phase_masses": [
            [row["phase_mass_numerator"], row["phase_mass_denominator"]]
            for row in certificate["theta_rows"]
        ],
        "landscape_claims": [row["claim"] for row in certificate["landscape_rows"]],
        "analytic_claims": [row["claim"] for row in certificate["analytic_rows"]],
    }
    declarations = {
        "network_fetch_performed_by_build": False,
        "external_payload_vendored": False,
        "finite_rows_are_analytic_proof": False,
        "effective_rate_computed": False,
        "git_source_rows": 117,
        "remote_logical_objects": 3,
        "logical_source_rows": 120,
    }
    all_pass = all((
        fixture_pass, core_pass, baseline_false, baseline_fresh,
        certificate["all_pass"] is True, mutation_pass, source_pass,
        finite_contracts["truth_census"] == {"eligible": 192, "outside": 320},
        finite_contracts["m3_dimension"]["allowed_dimension"] == 26,
        not any(GATES.values()), not any(FORBIDDEN.values()),
    ))
    return {
        "all_pass": all_pass,
        "certificate": certificate,
        "certificate_fixture": {
            "canonical_bytes": certificate_bytes,
            "sha256": certificate_sha,
            "pass": fixture_pass,
        },
        "core_fixture": {"sha256": core_sha, "pass": core_pass},
        "declarations": declarations,
        "finite_contracts": finite_contracts,
        "forbidden_claims": deepcopy(FORBIDDEN),
        "gates": deepcopy(GATES),
        "mutations": {
            "count": len(mutation_rows), "names": list(MUTATION_NAMES),
            "results": mutation_rows, "all_pass": mutation_pass,
        },
        "paper": "RH-393",
        "source_fixture": {"sha256": source_sha, "pass": source_pass},
        "source_locks": source_locks,
        "source_roles": deepcopy(SOURCE_ROLES),
        "status": "RH-393_two_odd_factor_terminal_log_mobius_compiler_certified",
        "theorems": deepcopy(THEOREM_CONTRACTS),
        "title": TITLE,
    }


def validate_result_payload(payload: object, *, compare_fresh: bool = True) -> bool:
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be exact bool")
    def sealed_bytes(value: object) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list or type(left) is tuple:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right
    try:
        _validate_constants()
        if type(payload) is not dict or set(payload) != {
            "all_pass", "certificate", "certificate_fixture", "core_fixture",
            "declarations", "finite_contracts", "forbidden_claims", "gates",
            "mutations", "paper", "source_fixture", "source_locks", "source_roles",
            "status", "theorems", "title",
        }:
            raise ValueError("result membership changed")
        if (
            payload["title"] != TITLE or payload["paper"] != "RH-393"
            or payload["status"]
            != "RH-393_two_odd_factor_terminal_log_mobius_compiler_certified"
        ):
            raise ValueError("result identity changed")
        certificate = payload["certificate"]
        certificate_raw = sealed_bytes(certificate)
        if not verify_certificate(certificate, compare_fresh=False):
            raise ValueError("certificate failed")
        if (
            len(certificate_raw) != CERTIFICATE_FIXTURE_BYTES
            or local_sha256(certificate_raw).hexdigest() != CERTIFICATE_FIXTURE_SHA256
        ):
            raise ValueError("certificate body seal changed")
        if not same(payload["certificate_fixture"], {
            "canonical_bytes": CERTIFICATE_FIXTURE_BYTES,
            "sha256": CERTIFICATE_FIXTURE_SHA256, "pass": True,
        }):
            raise ValueError("certificate fixture changed")
        if not same(payload["core_fixture"], {"sha256": CORE_FILE_SHA256, "pass": True}):
            raise ValueError("core fixture changed")
        if not same(payload["theorems"], THEOREM_CONTRACTS):
            raise ValueError("theorem contract changed")
        if not same(payload["source_roles"], SOURCE_ROLES):
            raise ValueError("source roles changed")
        if not same(payload["gates"], GATES) or not same(payload["forbidden_claims"], FORBIDDEN):
            raise ValueError("Gate/firewall changed")
        source = payload["source_locks"]
        if (
            type(source) is not dict or source.get("pass") is not True
            or (source.get("git_count"), source.get("remote_count"), source.get("logical_count"))
            != (117, 3, 120)
            or local_sha256(sealed_bytes(source)).hexdigest() != SOURCE_CLOSURE_SHA256
        ):
            raise ValueError("source closure changed")
        if not same(payload["source_fixture"], {"sha256": SOURCE_CLOSURE_SHA256, "pass": True}):
            raise ValueError("source fixture changed")
        if (
            source["git"].get("all_git_source_digest") != EXPECTED_ALL_GIT_SOURCE_DIGEST
            or source.get("logical_source_digest") != EXPECTED_LOGICAL_SOURCE_DIGEST
            or source["remote"].get("network_fetch_performed") is not False
            or source["remote"].get("external_payload_hash_hits") != []
        ):
            raise ValueError("source digest/offline gate changed")
        mutations = payload["mutations"]
        if (
            type(mutations) is not dict or set(mutations) != {
                "count", "names", "results", "all_pass"
            }
            or type(mutations["count"]) is not int or type(mutations["count"]) is bool
            or mutations["count"] != 32 or mutations["names"] != list(MUTATION_NAMES)
            or mutations["all_pass"] is not True or type(mutations["results"]) is not list
            or len(mutations["results"]) != 32
        ):
            raise ValueError("mutation contract changed")
        if any(
            type(row) is not dict or set(row) != {"name", "rejected"}
            or row["name"] != name or row["rejected"] is not True
            for name, row in zip(MUTATION_NAMES, mutations["results"])
        ):
            raise ValueError("mutation result changed")
        expected_finite = {
            "row_partition": deepcopy(certificate["row_partition"]),
            "truth_census": {"eligible": 192, "outside": 320},
            "m3_dimension": deepcopy(certificate["dimension_rows"][2]),
            "theta_phase_masses": [
                [row["phase_mass_numerator"], row["phase_mass_denominator"]]
                for row in certificate["theta_rows"]
            ],
            "landscape_claims": [row["claim"] for row in certificate["landscape_rows"]],
            "analytic_claims": [row["claim"] for row in certificate["analytic_rows"]],
        }
        if not same(payload["finite_contracts"], expected_finite):
            raise ValueError("finite contract consumption changed")
        if not same(payload["declarations"], {
            "network_fetch_performed_by_build": False,
            "external_payload_vendored": False,
            "finite_rows_are_analytic_proof": False,
            "effective_rate_computed": False,
            "git_source_rows": 117,
            "remote_logical_objects": 3,
            "logical_source_rows": 120,
        }):
            raise ValueError("declarations changed")
        if payload["all_pass"] is not True:
            raise ValueError("all_pass changed")
    except (KeyError, TypeError, ValueError):
        return False
    return not compare_fresh or same(payload, build_payload())


def main() -> None:
    payload = build_payload()
    if not validate_result_payload(payload, compare_fresh=False):
        raise RuntimeError("RH-393 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(payload))
    print(json.dumps({
        "status": payload["status"], "all_pass": True,
        "git": 117, "remote": 3, "logical": 120,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
