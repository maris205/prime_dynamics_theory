#!/usr/bin/env python3
"""Fail-closed local Bridge-B checker for TPC-369."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-369-third-origin-family-audit"
BRIDGE = ROOT / (
    "research/tpc-big-road/bridge_b_tpc369_third_origin_family_audit.md")
PRODUCER = PROJECT / "code/tpc369_third_origin_family_audit.py"
INDEPENDENT = PROJECT / "experiments/tpc369_independent_checker.py"
STRESS = PROJECT / "experiments/tpc369_adversarial_certificate_stress.py"
CERTIFICATE = PROJECT / "results/tpc369_certificate.json"
MAIN_TEX = PROJECT / "paper/main.tex"
MAIN_PDF = PROJECT / "paper/main.pdf"
PDF = PROJECT / "paper/paper.pdf"
LOG = PROJECT / "paper/compile.log"
README = PROJECT / "README.md"
PLAN = PROJECT / "PAPER_PLAN.md"
DERIVATION = PROJECT / "DERIVATION_PACKAGE.md"
PROOF = PROJECT / "PROOF_PACKAGE.md"
CLAIM = PROJECT / "notes/claim_firewall.md"
ROUTE = PROJECT / "notes/route_evaluation.md"
PROTOCOL = PROJECT / "notes/computational_protocol.md"

# Filled after all claim-bearing files are final.  Digests use normalized LF.
LOCKS = {
    "producer": "45d8895b3a5db445d6464b6d5a728373c3dc4b8a247161315b54dad7b9ae21b9",
    "independent": "473f3d4abfa22e2d8f494829afcb9068a056accf692cf04d990a4eaea8686291",
    "stress": "fdb2b9413ff704caff464c9d94fc5acbb7a2f9c074660a6cdb88ed4971c46fba",
    "certificate": "ea6d3f8916b8ae099bfe8831f6feb765aede68b24a7df5f229226b6c931a69b6",
    "main_tex": "9ef67952e78f286d375990863c722c2705ca3474f4c05404d019c370ad30775c",
    "main_pdf": "d83f61e39f07fb34758ab34a8217731ae7e790eda324ef4bb52496c11026ea83",
    "pdf": "d83f61e39f07fb34758ab34a8217731ae7e790eda324ef4bb52496c11026ea83",
    "log": "177ac4da4548fba495d15bfb51d4aefe294591deec2011e8df38f70255f9e15d",
    "readme": "b66ef466e24066debdb57e4af36e571e560e53cb12277d961e72a6cee63d1977",
    "plan": "96f89e9deba0542270f0b2e84d7d6f23dd3fbbc2bc7f7ee81e7aaaf9520c94a9",
    "derivation": "fab5f661f7a1ce0e9ed7a7abae7734d022eb3d23a6e645a3d77d8700594ff334",
    "proof": "1c5f637703d4fd7a6f3ed4cf841715969d968c363e610a8caa7a9e2eefd5efff",
    "claim": "0b24cdaa477ed3364c5a5830d198b47bd0cdaca395068397c904b2bd8995cd53",
    "route": "2cc2e32e12ac62133564a0e63eec75e8f78572b4e8a5bc056ea2b2f2946984b8",
    "protocol": "49afe8a53a1dc9767bad17ed1d0f4e71a75a64945e88f651954288dce05c36c7",
    "bridge": "ae208828463a75826251b9e7665bef60adfc3b580f699e817e20bd95946a1ffa",
}

STATUS = "NUMERICALLY_CERTIFIED_FINITE_THIRD_ORIGIN_FAMILY_AUDIT"
SCHEMA = "TPC369_THIRD_ORIGIN_FAMILY_AUDIT_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def lock(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED" and path.is_file() and
         digest(path.read_bytes()) == expected, label + " provenance")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and payload.get("status") == STATUS and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "schema/hash")
    origin = payload.get("origin_protocol", {})
    need(origin.get("candidate_count") == 41 and
         origin.get("grid_start") == 1010001 and origin.get("grid_step") == 401 and
         origin.get("grid_indices") == [0, 20, 40] and
         origin.get("selected_origins") == [1010001, 1018021, 1026041] and
         origin.get("response_used") is False and
         origin.get("geometry_used_for_selection") is False and
         origin.get("source_used") is False, "origin protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [1010001, 1018021, 1026041] and
         protocol.get("counts") == [512, 1024] and
         protocol.get("q_anchors") == [512, 2048, 8192] and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus", "alternating_index",
                                    "mod4_character", "half_split"] and
         protocol.get("betas") == [0, 2] and protocol.get("height") == 66 and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 144 and
         len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 144, "row census")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    need(phase.get("cap_repair_betas") == [], "repair beta")
    for beta, violations, schur_violations in ((0, 18, 18), (2, 6, 0)):
        item = phase.get("by_beta", {}).get(str(beta), {})
        need(item.get("rows") == 72 and
             item.get("spectral_cap_violations") == violations and
             item.get("schur_cap_violations") == schur_violations,
             "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 144 and audit.get("settings_per_beta") == 72 and
         audit.get("beta_count") == 2 and audit.get("spectral_rows") == 144 and
         audit.get("beta2_rows") == 72 and
         audit.get("beta2_spectral_cap_violations") == 6 and
         audit.get("beta2_schur_cap_violations") == 0 and
         audit.get("baseline_beta0_spectral_cap_violations") == 18 and
         audit.get("baseline_beta0_schur_cap_violations") == 18 and
         audit.get("q_min") == 512 and audit.get("q_max") == 8192 and
         audit.get("count_min") == 512 and audit.get("count_max") == 1024 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    expected_failure_keys = [
        [origin, 1024, q0, 1, "all_plus"]
        for origin in [1010001, 1018021, 1026041]
        for q0 in (2048, 8192)
    ]
    need(audit.get("expected_parent_failure_pattern") == expected_failure_keys and
         audit.get("replicated_failure_keys") == expected_failure_keys and
         audit.get("failure_pattern_matches_parent") is True,
         "failure pattern comparison")
    need(payload.get("exact_theorem", {}).get("anchor_repair") == {
        "initial_interval": [1010342, 1010355],
        "initial_geometry_positive_beta0": False,
        "initial_geometry_positive_beta2": False,
        "selected_interval": [1010346, 1010359],
        "selected_offset": 4,
    }, "anchor repair")
    expected = {
        "TPC369_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
        "TPC369_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC369_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC369_THIRD_ORIGIN_FAMILY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC369_BETA2_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC369_BETA2_FAILURE_PATTERN": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC369_INITIAL_ANCHOR_POSITIVITY": "REFUTED_SCOPED",
        "TPC369_REPAIRED_ANCHOR_RULE": "PROVED_EXACT_FINITE",
        "TPC369_ORIGIN_UNIFORMITY": "OPEN",
        "TPC369_WINDOW_UNIFORMITY": "OPEN",
        "TPC369_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC369_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC369_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC369_SOURCE_UNIFORM_L2": "OPEN",
        "TPC369_ARITHMETIC_ADVANCE": "NO",
        "TPC369_FIXED_POWER_CREDIT": 0,
        "TPC369_FULL_GATE_B": "OPEN",
        "TPC369_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected.items():
        need(firewall.get(key) == value, "firewall " + key)
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in (
            "TPC369_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
            "TPC369_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC369_INITIAL_ANCHOR_POSITIVITY = REFUTED_SCOPED",
            "TPC369_ARITHMETIC_ADVANCE = NO",
            "TPC369_FULL_GATE_B = OPEN"):
        need(marker in text, "bridge marker")
    log = LOG.read_text(encoding="utf-8", errors="replace")
    for bad in ("Warning:", "undefined", "Overfull \\hbox",
                "Underfull \\hbox", "LaTeX Error", "Fatal error",
                "Citation", "Empty"):
        need(bad not in log, "LaTeX diagnostic " + bad)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes() and
         PDF.read_bytes().startswith(b"%PDF-") and PDF.stat().st_size > 100000,
         "PDF identity")


def run(script: Path, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(script), "--check"])
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1",
                        "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    result = subprocess.run(command, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0 and result.stderr == b"",
         "subcheck failed " + script.name)
    return result.stdout


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        paths = {
            "producer": PRODUCER, "independent": INDEPENDENT, "stress": STRESS,
            "certificate": CERTIFICATE, "main_tex": MAIN_TEX,
            "main_pdf": MAIN_PDF, "pdf": PDF, "log": LOG, "readme": README,
            "plan": PLAN, "derivation": DERIVATION, "proof": PROOF,
            "claim": CLAIM, "route": ROUTE, "protocol": PROTOCOL,
            "bridge": BRIDGE,
        }
        for key, path in paths.items():
            lock(path, LOCKS[key], key)
        check_certificate()
        scripts = (PRODUCER, INDEPENDENT, STRESS)
        jobs = (tuple((script, False) for script in scripts) +
                tuple((script, True) for script in scripts))
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            outputs = tuple(pool.map(lambda job: run(*job), jobs))
        normal, optimized = outputs[:3], outputs[3:]
        need(normal == optimized, "normal/optimized stdout mismatch")
        need(normal[0] == b"TPC369_CERTIFICATE=PASS rows=144 beta2_rows=72\n",
             "producer output")
        need(normal[1] == b"TPC369_INDEPENDENT_CHECK=PASS rows=144 beta2_rows=72 "
             b"beta2_violations=6 baseline_beta0_violations=18\n",
             "independent output")
        need(normal[2] == b"TPC369_STRESS=PASS exact_baseline=1 mutations=30\n",
             "stress output")
        print("TPC369_BRIDGE_CHECK=PASS rows=144 beta2_rows=72 "
              "beta2_violations=6 baseline_beta0_violations=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC369_BRIDGE_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
