"""Build the RH-282--RH-361 provenance and frontier audit for Volume IV."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = REPO / "papers"
NUMBERED = re.compile(r"RH-(\d+)-.+")
START = 282
END = 361
REVIEW_ANCHORS = (291, 301, 311, 321, 331, 341, 351, 361)
PHASES = (
    (282, 291, "modulus_complete_heads_and_spectral_tails"),
    (292, 301, "weighted_prefix_clocks_and_analytic_criteria"),
    (302, 311, "annular_mass_and_endpoint_hardy_barriers"),
    (312, 321, "endpoint_expansions_and_synthetic_spectral_sharpness"),
    (322, 331, "first_alias_local_physical_and_affine_interfaces"),
    (332, 341, "actual_replacement_observation_and_signed_ledgers"),
    (342, 351, "boundary_atoms_and_lower_even_signed_completion"),
    (352, 361, "actual_selected_tails_and_deterministic_counterloops"),
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_record(directory: Path) -> dict[str, object]:
    required = {
        "readme": (directory / "README.md").exists(),
        "main_tex": (directory / "main.tex").exists(),
        "pdf": bool(list(directory.glob("*.pdf"))),
    }
    return {
        "directory": directory.name,
        "required": required,
        "nonempty_score": sum(required.values()),
        "file_count": sum(1 for path in directory.iterdir() if path.is_file()),
    }


def phase_for(number: int) -> str:
    for start, end, phase in PHASES:
        if start <= number <= end:
            return phase
    raise ValueError(number)


def main() -> None:
    candidates: dict[int, list[dict[str, object]]] = {}
    for directory in sorted(PAPERS.iterdir()):
        match = NUMBERED.fullmatch(directory.name)
        if match and directory.is_dir():
            number = int(match.group(1))
            if START <= number <= END:
                candidates.setdefault(number, []).append(source_record(directory))

    expected = list(range(START, END + 1))
    if sorted(candidates) != expected:
        missing = sorted(set(expected) - set(candidates))
        extras = sorted(set(candidates) - set(expected))
        raise RuntimeError(f"Volume IV range mismatch: missing={missing}, extras={extras}")

    canonical: dict[int, dict[str, object]] = {}
    aliases: dict[str, list[str]] = {}
    for number in expected:
        rows = candidates[number]
        complete = [row for row in rows if all(row["required"].values())]
        if len(complete) != 1:
            names = sorted(str(row["directory"]) for row in complete)
            raise RuntimeError(
                f"RH-{number} must have exactly one complete source: {names}"
            )
        chosen = complete[0]
        chosen["phase"] = phase_for(number)
        canonical[number] = chosen
        if len(rows) > 1:
            aliases[str(number)] = sorted(str(row["directory"]) for row in rows)

    source_hashes: dict[str, str] = {}
    for number in expected:
        directory = PAPERS / str(canonical[number]["directory"])
        for relative in (
            "README.md",
            "main.tex",
            "THEOREM_LEDGER.md",
            "UPDATED_ROADMAP.md",
            "results/result.json",
        ):
            path = directory / relative
            if path.exists():
                source_hashes[str(path.relative_to(REPO))] = sha(path)

    payload = {
        "status": "rh_volume_iv_noisy_head_annulus_signed_completion_audit",
        "series": {
            "volume": 4,
            "source_range": [START, END],
            "numbered_endpoint_changed": False,
            "atomic_sources_preserved": True,
        },
        "numbered_paper_count": len(expected),
        "atomic_index_count": len(expected),
        "unique_numbers": expected,
        "consecutive_numbering": True,
        "canonical": {str(number): canonical[number] for number in expected},
        "legacy_alias_groups": aliases,
        "review_anchor_numbers": list(REVIEW_ANCHORS),
        "phase_ranges": [
            {"start": start, "end": end, "phase": phase}
            for start, end, phase in PHASES
        ],
        "source_file_hash_count": len(source_hashes),
        "source_file_hashes": source_hashes,
        "typed_identities": ["p=tau-a=q-d", "d=h-s", "q=p+d", "h=s+d"],
        "actual_branch_range": [352, 354],
        "deterministic_branch_range": [355, 360],
        "same_clock_bridge_proved": False,
        "physical_obstruction_proved": False,
        "route_coordinate": "actual_same_clock_unnormalized_head_transport_open",
        "first_missing_leaf": "D_(4k)(R)->0",
        "rh_362_activated": False,
        "gates": {key: False for key in ("A", "B", "C", "D", "E")},
        "forbidden_claims": {
            "hilbert_polya_constructed": False,
            "riemann_zeros_identified": False,
            "von_mangoldt_trace_proved": False,
            "zeta_divisor_equality": False,
            "riemann_hypothesis_proved": False,
        },
    }
    index_lines = [
        r"\begin{longtable}{r >{\raggedright\arraybackslash}p{0.78\textwidth}}",
        r"\toprule", r"source & canonical directory\\", r"\midrule",
        r"\endfirsthead", r"\toprule", r"source & canonical directory\\",
        r"\midrule", r"\endhead",
    ]
    for number in expected:
        directory = canonical[number]["directory"].replace(
            "-", r"-\allowbreak{}"
        )
        index_lines.append(f"RH-{number} & \\texttt{{{directory}}}\\\\")
    index_lines.extend((r"\bottomrule", r"\end{longtable}"))
    (ROOT / "results/atomic_index.tex").write_text("\n".join(index_lines) + "\n")
    output = ROOT / "results/volume_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "numbered_paper_count": payload["numbered_paper_count"],
        "legacy_alias_group_count": len(aliases),
        "review_anchor_count": len(REVIEW_ANCHORS),
        "source_file_hash_count": len(source_hashes),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
