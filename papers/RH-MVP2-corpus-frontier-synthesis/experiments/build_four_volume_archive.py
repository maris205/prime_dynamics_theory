"""Build the outer SHA-256 manifest for the four-volume RH synthesis."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
VOLUMES = (
    {
        "volume": 1,
        "root": "papers/RH-MVP1-conditional-prime-dynamics-hilbert-polya-roadmap",
        "source_range": [1, 160],
        "distribution_pdf": "conditional-prime-dynamics-hilbert-polya-roadmap.pdf",
    },
    {
        "volume": 2,
        "root": "papers/RH-VOL2-physical-riesz-cloud-trace-envelope-synthesis",
        "source_range": [161, 241],
        "distribution_pdf": "physical-riesz-cloud-trace-envelope-synthesis.pdf",
    },
    {
        "volume": 3,
        "root": "papers/RH-VOL3-deterministic-numerator-anchor-counterloop-synthesis",
        "source_range": [242, 281],
        "distribution_pdf": "deterministic-numerator-anchor-counterloop-synthesis.pdf",
    },
    {
        "volume": 4,
        "root": "papers/RH-VOL4-noisy-head-annulus-signed-completion-synthesis",
        "source_range": [282, 361],
        "distribution_pdf": "noisy-head-annulus-signed-completion-synthesis.pdf",
    },
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    volume_rows = []
    aggregate_archive_file_count = 0
    for spec in VOLUMES:
        volume_root = REPO / spec["root"]
        archive_relative = "results/archive_verification.json"
        archive_path = volume_root / archive_relative
        main_pdf = volume_root / "main.pdf"
        distribution_pdf = volume_root / spec["distribution_pdf"]
        required = (archive_path, main_pdf, distribution_pdf)
        missing = [str(path.relative_to(REPO)) for path in required if not path.is_file()]
        if missing:
            raise RuntimeError(f"four-volume archive input missing: {missing}")

        archive = json.loads(archive_path.read_text())
        if archive.get("file_count") != len(archive.get("files", {})):
            raise RuntimeError(f"invalid archive file count: {archive_path}")
        archive_file_count = int(archive["file_count"])
        aggregate_archive_file_count += archive_file_count
        volume_rows.append({
            **spec,
            "archive": archive_relative,
            "archive_sha256": sha(archive_path),
            "archive_file_count": archive_file_count,
            "main_pdf_sha256": sha(main_pdf),
            "distribution_pdf_sha256": sha(distribution_pdf),
        })

    output = ROOT / "results/four_volume_archive_manifest.json"
    payload = {
        "schema": "rh-four-volume-archive-v1",
        "status": "rh_four_volume_synthesis_archived",
        "numbered_source_count": 361,
        "aggregate_archive_file_count": aggregate_archive_file_count,
        "numbered_endpoint_changed": False,
        "atomic_sources_preserved": True,
        "route_coordinate": "actual_same_clock_unnormalized_head_transport_open",
        "gates": {key: False for key in ("A", "B", "C", "D", "E")},
        "volumes": volume_rows,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "volume_count": len(volume_rows),
        "aggregate_archive_file_count": aggregate_archive_file_count,
        "status": payload["status"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
