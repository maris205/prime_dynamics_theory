from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from mvp_roadmap import classify_claim, completion_bundles, first_missing_gate  # noqa: E402


MILESTONES = (1, 10, 20, 30, 40, 50, 60, 71, 81, 91, 100, 119, 129, 139, 149, 159, 160)
REVIEW_NUMBERS = (71, 81, 91, 100, 119, 129, 139, 149, 159, 160)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def numbered_papers() -> dict[int, Path]:
    records: dict[int, list[Path]] = {}
    for directory in PAPERS.iterdir():
        match = re.fullmatch(r"RH-(\d+)-.+", directory.name)
        if match and int(match.group(1)) <= 160:
            records.setdefault(int(match.group(1)), []).append(directory)
    if set(records) != set(range(1, 161)) or any(len(items) != 1 for items in records.values()):
        raise RuntimeError("RH-1 through RH-160 must be present exactly once")
    return {number: items[0] for number, items in records.items()}


def declared_archive_matches(directory: Path) -> tuple[int, int]:
    path = directory / "results/archive_verification.json"
    if not path.exists():
        return 0, 0
    payload = json.loads(path.read_text())
    checks = [sha(directory / relative) == expected for relative, expected in payload.get("files", {}).items()]
    return len(checks), sum(not value for value in checks)


def main() -> None:
    papers = numbered_papers()
    inventory = []
    for number in range(1, 161):
        directory = papers[number]
        hash_count, hash_failures = declared_archive_matches(directory)
        inventory.append({
            "paper": number,
            "directory": directory.name,
            "readme": (directory / "README.md").exists(),
            "main_tex": (directory / "main.tex").exists(),
            "pdf": bool(list(directory.glob("*.pdf"))),
            "summary": (directory / "results/summary.json").exists(),
            "archive": (directory / "results/archive_verification.json").exists(),
            "tests": (directory / "tests").is_dir(),
            "declared_publication_hash_count": hash_count,
            "declared_publication_hash_failure_count": hash_failures,
        })

    gates = [
        {
            "key": "F",
            "name": "rigorous dynamical foundation",
            "status": "proved",
            "evidence": "RH-1--45",
            "content": "ordered sieve-kneading coordinate, parity geometry, fixed-noise intrinsic determinant, and deterministic pole data",
            "falsifier": "none within stated scope; stronger conjugacy and direct Markov self-adjointness are already rejected",
        },
        {
            "key": "A",
            "name": "canonical all-level intrinsic determinant",
            "status": "open",
            "evidence": "RH-46--160 conditional reset-support spine; typed determinant assembly still absent",
            "content": "joint small-noise/mesh limit with an exact moving-cloud quotient, tracked pole divisor, and target-independent normalization",
            "falsifier": "reset overlap, tail separation, selected spread, or typed assembly fails along an infinite scale sequence",
        },
        {
            "key": "B",
            "name": "order-sensitive canonical scattering completion",
            "status": "open",
            "evidence": "RH-8, RH-80 and roadmap",
            "content": "inner/unitary completion retaining directed temporal traces and independent of arbitrary packet gauges",
            "falsifier": "every completion is noncanonical, orientation-blind, or introduces arbitrary spectrum",
        },
        {
            "key": "C",
            "name": "self-adjoint generator and intrinsic counting law",
            "status": "open",
            "evidence": "not reached",
            "content": "canonical self-adjoint realization whose own high-energy law has the Riemann--von Mangoldt form",
            "falsifier": "the canonical object has bounded phase, logarithmic rank, power-law Weyl growth, or wrong multiplicities",
        },
        {
            "key": "D",
            "name": "prime-power explicit trace formula",
            "status": "open",
            "evidence": "arithmetic interface absent",
            "content": "target-independent transform producing von Mangoldt prime-power weights, archimedean terms, and a controlled test class",
            "falsifier": "weights require inserted zero/prime data or cannot match the completed explicit formula uniformly",
        },
        {
            "key": "E",
            "name": "complete spectral-divisor identity",
            "status": "open",
            "evidence": "not reached",
            "content": "completed-zeta determinant identity with no missing or spurious levels and correct multiplicity",
            "falsifier": "unmatched gamma/trivial-zero factors, extra spectral points, missing levels, or multiplicity mismatch",
        },
    ]
    statuses = {gate["key"]: gate["status"] for gate in gates}

    mvp_formula = {
        "op": "and",
        "children": [
            {"gate": "F"}, {"gate": "A"}, {"gate": "B"},
            {"gate": "C"}, {"gate": "D"}, {"gate": "E"},
        ],
    }
    hp_formula = {
        "op": "and",
        "children": [{"gate": "F"}, {"gate": "A"}, {"gate": "B"}, {"gate": "C"}],
    }
    completion = completion_bundles(mvp_formula, statuses)
    hp_completion = completion_bundles(hp_formula, statuses)

    stage_requirements = {
        "intrinsic_determinant": ["F", "A"],
        "canonical_scattering": ["F", "A", "B"],
        "hilbert_polya_candidate": ["F", "A", "B", "C"],
        "arithmetic_spectral_model": ["F", "A", "B", "C", "D"],
        "completed_zeta_identity": ["F", "A", "B", "C", "D", "E"],
    }
    active_proved = [key for key, status in statuses.items() if status == "proved"]
    active_mvp_assumed = list(statuses)

    assumptions = [
        {
            "key": "A",
            "bold_form": "the RH-160 reset interfaces O/E/S (and L when directional output is required) persist eventually and feed a typed all-level assembly",
            "careful_target": "prove a moving-cloud-relative, pole-tracked, target-independent small-noise determinant limit",
        },
        {
            "key": "B",
            "bold_form": "the renormalized determinant has a unique order-sensitive inner/scattering completion",
            "careful_target": "derive unitarity, directed-trace retention, and normalization uniqueness",
        },
        {
            "key": "C",
            "bold_form": "the scattering phase is generated by a canonical self-adjoint operator with Riemann--von Mangoldt counting",
            "careful_target": "construct the domain and prove the counting law before any ordinate fit",
        },
        {
            "key": "D",
            "bold_form": "the oriented dynamical trace admits a target-independent arithmetic transform with von Mangoldt weights",
            "careful_target": "prove equality of test-function traces including prime powers and archimedean terms",
        },
        {
            "key": "E",
            "bold_form": "the resulting spectral divisor equals the completed-zeta divisor exactly",
            "careful_target": "exclude missing/spurious levels and prove multiplicities and functional symmetry",
        },
    ]

    milestone_records = []
    for number in MILESTONES:
        directory = papers[number]
        milestone_records.append({
            "paper": number,
            "directory": directory.name,
            "readme_sha256": sha(directory / "README.md"),
            "main_tex_sha256": sha(directory / "main.tex"),
            "summary_sha256": sha(directory / "results/summary.json") if (directory / "results/summary.json").exists() else None,
            "role": (
                "symbolic foundation" if number == 1 else
                "periodic determinant" if number == 10 else
                "critical-branch structure" if number == 20 else
                "finite contour certificate" if number == 30 else
                "continuum Riesz bridge" if number == 40 else
                "directional Hardy reduction" if number == 50 else
                "phase-aware tail completion" if number == 60 else
                "route review"
            ),
        })

    rejected_shortcuts = [
        {"shortcut": "full topological conjugacy from one kneading word", "evidence": "RH-1 entropy obstruction"},
        {"shortcut": "noisy Markov operator as the Hilbert--Polya operator", "evidence": "RH-7 irreversibility"},
        {"shortcut": "two-factor eigenphases encode temporal order", "evidence": "RH-8 AB/BA blindness"},
        {"shortcut": "unrenormalized entire small-noise determinant", "evidence": "RH-15 and RH-46 pole obstructions"},
        {"shortcut": "uniform fixed-step global complement contraction", "evidence": "RH-50 no-go"},
        {"shortcut": "finite-anchor fitting proves an all-level law", "evidence": "RH-117 barrier"},
        {"shortcut": "independent packet balls preserve correlated positivity", "evidence": "RH-153 information loss"},
        {"shortcut": "contemporaneous spectral reset supplies recent cross rank", "evidence": "RH-157 exact cancellation"},
        {"shortcut": "inverse prime encoding is a prime-power trace formula", "evidence": "RH-1--2 claim boundary"},
    ]

    summary = {
        "numbered_paper_count": len(inventory),
        "consecutive_numbering": [item["paper"] for item in inventory] == list(range(1, 161)),
        "readme_count": sum(item["readme"] for item in inventory),
        "main_tex_count": sum(item["main_tex"] for item in inventory),
        "pdf_directory_count": sum(item["pdf"] for item in inventory),
        "summary_archive_count": sum(item["summary"] for item in inventory),
        "verification_archive_count": sum(item["archive"] for item in inventory),
        "test_directory_count": sum(item["tests"] for item in inventory),
        "declared_publication_hash_count": sum(item["declared_publication_hash_count"] for item in inventory),
        "declared_publication_hash_failure_count": sum(item["declared_publication_hash_failure_count"] for item in inventory),
        "milestone_input_count": len(milestone_records),
        "review_anchor_count": len(REVIEW_NUMBERS),
        "macro_gate_count": len(gates),
        "proved_macro_gate_count": sum(gate["status"] == "proved" for gate in gates),
        "conditional_macro_gate_count": sum(gate["status"] == "conditional" for gate in gates),
        "open_macro_gate_count": sum(gate["status"] == "open" for gate in gates),
        "rejected_shortcut_count": len(rejected_shortcuts),
        "full_mvp_completion_bundle_count": len(completion),
        "full_mvp_completion_bundle": sorted(next(iter(completion))) if completion else [],
        "hilbert_polya_completion_bundle": sorted(next(iter(hp_completion))) if hp_completion else [],
        "current_unconditional_claim_level": classify_claim(active_proved, stage_requirements),
        "mvp_assumption_claim_level": classify_claim(active_mvp_assumed, stage_requirements),
        "current_first_missing_gate": first_missing_gate(active_proved, ["F", "A", "B", "C", "D", "E"]),
    }
    payload = {
        "status": "rh_mvp1_conditional_prime_dynamics_hilbert_polya_roadmap",
        "inventory": inventory,
        "milestone_records": milestone_records,
        "gates": gates,
        "assumptions": assumptions,
        "stage_requirements": stage_requirements,
        "rejected_shortcuts": rejected_shortcuts,
        "audit_summary": summary,
        "claim_ladder": {
            "proved_now": "rigorous dynamical and fixed-noise spectral foundation only",
            "conditional_if_A_B_C": "a Hilbert--Polya candidate with the required intrinsic counting law, but no arithmetic zero identity",
            "conditional_if_A_through_E": "a self-adjoint realization of the completed-zeta spectral divisor; only at this point does the usual Hilbert--Polya implication place represented nontrivial zeros on the critical line",
            "unconditional_riemann_hypothesis": False,
        },
        "status_legend": {
            "proved": "analytic theorem in its stated scope",
            "finite": "finite exact-stored or outward certificate only",
            "conditional": "proved implication whose physical hypotheses remain open",
            "open": "the complete required implication has not yet been constructed",
            "no_go": "the named branch is rigorously rejected",
        },
        "theorem_boundary": {
            "conditional_macro_implication": True,
            "completion_debt_audited": True,
            "all_160_numbered_papers_present": summary["consecutive_numbering"],
            "all_macro_assumptions_proved": False,
            "stage_A_proved": False,
            "canonical_self_adjoint_operator_constructed": False,
            "prime_power_trace_formula_proved": False,
            "zeta_spectral_identity_proved": False,
            "riemann_hypothesis_proved": False,
        },
        "route_consequence": (
            "The 160-paper program supports a rigorous dynamical and fixed-noise determinant foundation and a sharply falsifiable conditional Stage-A spine. "
            "A complete Hilbert--Polya route can be stated as five additional macro interfaces A--E, but none may be inferred from finite certification or numerical resemblance. "
            "Assuming all five yields a completed-zeta spectral identity for a self-adjoint generator and hence the standard conditional Hilbert--Polya implication; proving the interfaces is the remaining mathematics."
        ),
    }
    output = ROOT / "results/mvp_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
