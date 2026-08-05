"""Build the RH-1--RH-361 provenance inventory for RH-MVP2."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = REPO / "papers"
NUMBERED = re.compile(r"RH-(\d+)-.+")
REVIEW_ANCHORS = (
    71, 81, 91, 100, 119, 129, 139, 149, 159, 171, 181, 191, 201, 211,
    221, 231, 241, 251, 261, 271, 281, 291, 301, 311, 321, 331, 341, 351,
    361,
)
SERIES_VOLUMES = (
    (1, 1, 160, "RH-MVP1-conditional-prime-dynamics-hilbert-polya-roadmap"),
    (2, 161, 241, "RH-VOL2-physical-riesz-cloud-trace-envelope-synthesis"),
    (3, 242, 281, "RH-VOL3-deterministic-numerator-anchor-counterloop-synthesis"),
    (4, 282, 361, "RH-VOL4-noisy-head-annulus-signed-completion-synthesis"),
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_record(directory: Path) -> dict[str, object]:
    files = sorted(path for path in directory.iterdir() if path.is_file())
    required = {
        "readme": (directory / "README.md").exists(),
        "main_tex": (directory / "main.tex").exists(),
        "pdf": bool(list(directory.glob("*.pdf"))),
    }
    return {
        "directory": directory.name,
        "required": required,
        "file_count": len(files),
        "nonempty_score": sum(required.values()),
    }


def main() -> None:
    records: dict[int, list[dict[str, object]]] = {}
    for directory in sorted(PAPERS.iterdir()):
        match = NUMBERED.fullmatch(directory.name)
        if match:
            number = int(match.group(1))
            if 1 <= number <= 361 and directory.is_dir():
                records.setdefault(number, []).append(source_record(directory))

    expected = list(range(1, 362))
    numbers = sorted(records)
    missing = [number for number in expected if number not in records]
    extras = [number for number in numbers if number not in expected]
    if missing or extras:
        raise RuntimeError(f"numbered corpus mismatch: missing={missing}, extras={extras}")

    canonical: dict[int, dict[str, object]] = {}
    aliases: dict[str, list[str]] = {}
    for number in expected:
        candidates = records[number]
        complete = [item for item in candidates if all(item["required"].values())]
        if len(complete) != 1:
            names = sorted(str(item["directory"]) for item in complete)
            raise RuntimeError(
                f"RH-{number} must have exactly one complete source: {names}"
            )
        chosen = complete[0]
        canonical[number] = chosen
        if len(candidates) > 1:
            aliases[str(number)] = [str(item["directory"]) for item in candidates]

    source_files: dict[str, str] = {}
    for number in expected:
        directory = PAPERS / str(canonical[number]["directory"])
        for relative in ("README.md", "main.tex", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "results/result.json"):
            path = directory / relative
            if path.exists():
                source_files[str(path.relative_to(REPO))] = sha(path)

    review_numbers = list(REVIEW_ANCHORS)
    if any(number not in canonical for number in review_numbers):
        raise RuntimeError("review anchor is missing from the numbered corpus")

    def phase(number: int) -> str:
        if number <= 160:
            return "foundation_and_stage_A"
        if number <= 241:
            return "physical_clouds_and_trace_envelope"
        if number <= 281:
            return "deterministic_anchor_selector_and_counterloop"
        return "actual_noisy_tail_endpoint_alias_and_signed_frontier"

    for number in expected:
        canonical[number]["phase"] = phase(number)

    volume_rows = []
    covered = []
    for volume, start, end, directory_name in SERIES_VOLUMES:
        directory = PAPERS / directory_name
        if not directory.is_dir():
            raise RuntimeError(f"series volume directory missing: {directory_name}")
        volume_rows.append({
            "volume": volume,
            "source_range": [start, end],
            "directory": directory_name,
        })
        covered.extend(range(start, end + 1))
    if covered != expected:
        raise RuntimeError("four-volume ranges do not cover RH-1--RH-361 exactly")

    payload = {
        "status": "rh_mvp2_corpus_frontier_inventory",
        "numbered_paper_count": len(expected),
        "unique_numbers": numbers,
        "consecutive_numbering": numbers == expected,
        "canonical": {str(number): canonical[number] for number in expected},
        "legacy_alias_groups": aliases,
        "review_anchor_numbers": review_numbers,
        "review_anchor_count": len(review_numbers),
        "review_anchor_coverage_union_count": 349,
        "series_volumes": volume_rows,
        "source_file_hash_count": len(source_files),
        "source_file_hashes": source_files,
        "route_coordinate": "actual_same_clock_unnormalized_head_transport_open",
        "first_missing_leaf": "D_(4k)(R)->0",
        "gates": {key: False for key in ("A", "B", "C", "D", "E")},
        "forbidden_claims": {
            "hilbert_polya_constructed": False,
            "riemann_zeros_identified": False,
            "von_mangoldt_trace_proved": False,
            "zeta_divisor_equality": False,
            "riemann_hypothesis_proved": False,
        },
    }
    output = ROOT / "results/corpus_inventory.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "numbered_paper_count": payload["numbered_paper_count"],
        "legacy_alias_groups": aliases,
        "review_anchor_count": len(review_numbers),
        "source_file_hash_count": len(source_files),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
