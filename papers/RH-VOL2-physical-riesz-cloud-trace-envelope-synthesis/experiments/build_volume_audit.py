"""Build the RH-161--RH-241 provenance and frontier audit for Volume II."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = REPO / "papers"
NUMBERED = re.compile(r"RH-(\d+)-.+")
START, END = 161, 241
REVIEW_ANCHORS = (161, 171, 181, 191, 201, 211, 221, 231, 241)
PHASES = (
    (161, 161, "typed_packet_riesz_relative_determinant_assembly"),
    (162, 171, "physical_riesz_shells"),
    (172, 181, "history_cycle_realization"),
    (182, 191, "biorthogonal_feshbach_frontier"),
    (192, 201, "source_channel_quotient"),
    (202, 211, "transport_failures_and_divisor_first_pivot"),
    (212, 221, "quartet_shape_gauge_and_fixed_degree_obstruction"),
    (222, 231, "rank_growing_reciprocal_cloud_and_det2"),
    (232, 241, "projection_free_factor_and_trace_envelope"),
)
FINITE_REVIEW_ITEMS = {
    "171": 3584,
    "181": 2600,
    "191": 2960,
    "201": 1352,
    "211": 649,
    "221": 2140,
    "231": 9870,
    "241": 7280,
}


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
                    raise RuntimeError(f"duplicate Volume II source: RH-{number}")
                records[number] = directory

    expected = list(range(START, END + 1))
    if sorted(records) != expected:
        raise RuntimeError("Volume II sources are not consecutive RH-161--RH-241")

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
        "status": "rh_volume_ii_physical_riesz_cloud_trace_envelope_audit",
        "series": {
            "volume": 2,
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
        "finite_review_item_counts": FINITE_REVIEW_ITEMS,
        "finite_review_item_total": sum(FINITE_REVIEW_ITEMS.values()),
        "source_file_hash_count": len(source_hashes),
        "source_file_hashes": source_hashes,
        "typed_assembly": {
            "abstract_implication_proved": True,
            "determinant_types": [1, 2],
            "physical_interfaces": {key: False for key in ("R", "Q", "U", "Z", "T")},
        },
        "fixed_order_trace_envelope_max_order": 12,
        "moving_noisy_all_order_trace_envelope_proved": False,
        "no_over_extraction_coefficient_anchor_proved": False,
        "route_coordinate": "physical_riesz_cloud_assembled_moving_noisy_trace_envelope_open",
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
        "finite_review_item_total": payload["finite_review_item_total"],
        "numbered_paper_count": len(expected),
        "output": str(output.relative_to(ROOT)),
        "review_anchor_count": len(REVIEW_ANCHORS),
        "source_file_hash_count": len(source_hashes),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
