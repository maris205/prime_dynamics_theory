"""Build the RH-242--RH-281 provenance and frontier audit for Volume III."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = REPO / "papers"
NUMBERED = re.compile(r"RH-(\d+)-.+")
START, END = 242, 281
REVIEW_ANCHORS = (251, 261, 271, 281)
PHASES = (
    (242, 251, "superloop_quotient_and_frozen_anchor"),
    (252, 261, "analytic_tail_and_legal_selector_barriers"),
    (262, 271, "deterministic_all_order_envelope_and_radius"),
    (272, 281, "counterloop_and_quotient_frontier"),
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def phase_for(number: int) -> str:
    for start, end, phase in PHASES:
        if start <= number <= end:
            return phase
    raise ValueError(number)


def main() -> None:
    records: dict[int, Path] = {}
    for directory in sorted(PAPERS.iterdir()):
        match = NUMBERED.fullmatch(directory.name)
        if match and directory.is_dir():
            number = int(match.group(1))
            if START <= number <= END:
                if number in records:
                    raise RuntimeError(f"duplicate Volume III source: RH-{number}")
                records[number] = directory

    expected = list(range(START, END + 1))
    if sorted(records) != expected:
        raise RuntimeError("Volume III sources are not consecutive RH-242--RH-281")

    canonical = {}
    source_hashes: dict[str, str] = {}
    for number in expected:
        directory = records[number]
        required = {
            "readme": (directory / "README.md").exists(),
            "main_tex": (directory / "main.tex").exists(),
            "pdf": bool(list(directory.glob("*.pdf"))),
        }
        if not all(required.values()):
            raise RuntimeError(f"incomplete source: RH-{number}")
        canonical[str(number)] = {
            "directory": directory.name,
            "phase": phase_for(number),
            "required": required,
        }
        for relative in (
            "README.md", "main.tex", "THEOREM_LEDGER.md",
            "UPDATED_ROADMAP.md", "results/result.json",
        ):
            path = directory / relative
            if path.exists():
                source_hashes[str(path.relative_to(REPO))] = sha(path)

    payload = {
        "status": "rh_volume_iii_deterministic_anchor_counterloop_audit",
        "series": {
            "volume": 3,
            "source_range": [START, END],
            "numbered_endpoint_changed": False,
            "atomic_sources_preserved": True,
        },
        "numbered_paper_count": len(expected),
        "atomic_index_count": len(expected),
        "unique_numbers": expected,
        "consecutive_numbering": True,
        "canonical": canonical,
        "review_anchor_numbers": list(REVIEW_ANCHORS),
        "phase_ranges": [
            {"start": start, "end": end, "phase": phase}
            for start, end, phase in PHASES
        ],
        "source_file_hash_count": len(source_hashes),
        "source_file_hashes": source_hashes,
        "deterministic_envelope": {
            "proved": True,
            "constant": 48,
            "q_star": "0.7008752258547757",
            "start_order": 2,
            "sharp_ratio_limit": 1,
            "rho_star": "1.4267874838640739",
        },
        "deterministic_counterloop_bridge_proved": True,
        "actual_cloud_coefficient_bridge_proved": False,
        "aggregate_noisy_cloud_transport_proved": False,
        "variable_rank_quotient_instantiated": False,
        "route_coordinate": "deterministic_all_order_closed_actual_cloud_identification_open",
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
        directory = records[number].name.replace("-", r"-\allowbreak{}")
        index_lines.append(f"RH-{number} & \\texttt{{{directory}}}\\\\")
    index_lines.extend((r"\bottomrule", r"\end{longtable}"))
    (ROOT / "results/atomic_index.tex").write_text("\n".join(index_lines) + "\n")
    output = ROOT / "results/volume_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "numbered_paper_count": len(expected),
        "output": str(output.relative_to(ROOT)),
        "review_anchor_count": len(REVIEW_ANCHORS),
        "source_file_hash_count": len(source_hashes),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
